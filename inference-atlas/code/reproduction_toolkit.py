#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""InferenceAtlas 复现工具箱（模块 12 第 12 章配套）。

把本库前 11 个模块的核心判据实现为可直接调用的函数，
使读者能把自己实测的数字代入，得到可行性判断，而不必手工推导。

设计约束：
  * 仅用标准库，无第三方依赖；
  * 每个函数对应本库一处明确的推导，docstring 标注出处；
  * 所有函数为纯函数，便于自测；
  * 运行本文件即执行全部自测：python3 code/reproduction_toolkit.py

注意：本工具箱只做换算与判定，**不产生任何测量数据**。
输入必须来自读者自己的实测（见第 12 章的实验清单）。
"""
from __future__ import annotations

import math
from dataclasses import dataclass

# ---------------------------------------------------------------- 单位

GiB = 1024 ** 3
MiB = 1024 ** 2
KiB = 1024


# ------------------------------------------------- 模块 02：KV 容量

def kv_bytes_per_token(n_layers: int, n_kv_heads: int, head_dim: int,
                       bytes_per_elem: float = 2.0) -> float:
    """每 token 每请求的 KV 字节数 k = 2·L·n_kv·d_h·b_kv。

    出处：模块 02 第 5 章。因子 2 来自 K 与 V 各一份。
    """
    return 2 * n_layers * n_kv_heads * head_dim * bytes_per_elem


# --------------------------------- 模块 07 第 5 章：容量与带宽的联合约束

@dataclass(frozen=True)
class DecodeCapacity:
    """decode 稳态的三个上界与派生量。"""
    ceiling_tok_s: float      # 饱和吞吐上限 BW/(S·k)
    b_half: float             # 半饱和批 W/(S·k)
    c_max: float              # 容量并发上限 (M_eff - W)/(S·k)
    reachable_fraction: float # 可达吞吐占上限的比例 1 - W/M_eff


def decode_capacity(weight_bytes: float, mem_eff_bytes: float,
                    bandwidth_bytes_s: float, seq_len: int,
                    kv_per_token: float) -> DecodeCapacity:
    """由 W、M_eff、BW、S、k 算出 decode 的三个上界。

    出处：模块 07 第 5 章第 2.2–2.4 节。

    关键恒等式（S 与 k 会完全约掉）：
        c_max / b_half        = M_eff/W - 1
        reachable_fraction    = 1 - W/M_eff
    """
    if mem_eff_bytes <= weight_bytes:
        raise ValueError("有效显存必须大于权重体积，否则装不下")
    sk = seq_len * kv_per_token
    return DecodeCapacity(
        ceiling_tok_s=bandwidth_bytes_s / sk,
        b_half=weight_bytes / sk,
        c_max=(mem_eff_bytes - weight_bytes) / sk,
        reachable_fraction=1.0 - weight_bytes / mem_eff_bytes,
    )


def decode_throughput(batch: float, weight_bytes: float,
                      bandwidth_bytes_s: float, seq_len: int,
                      kv_per_token: float) -> float:
    """给定批大小的 decode 吞吐 = B·BW / (W + B·S·k)。

    出处：模块 07 第 5 章第 2.2 节。
    """
    sk = seq_len * kv_per_token
    return batch * bandwidth_bytes_s / (weight_bytes + batch * sk)


# ------------------------------ 模块 08：α-β 模型与集合通信

def half_power_size(alpha_s: float, beta_bytes_s: float) -> float:
    """半功率消息尺寸 n_half = α·β（字节）。

    出处：模块 08 第 1 章第 2.2 节。
    n << n_half 时时延主导（应减少通信次数）；
    n >> n_half 时带宽主导（应减少通信字节）。
    """
    return alpha_s * beta_bytes_s


def allreduce_ring(msg_bytes: float, p: int, alpha_s: float,
                   beta_bytes_s: float) -> float:
    """环状 all-reduce 耗时：2(P-1)α + 2(P-1)/P · D/β。

    出处：模块 08 第 5 章第 2.2 节。时延项随 P 线性增长。
    """
    if p < 2:
        return 0.0
    return 2 * (p - 1) * alpha_s + 2 * (p - 1) / p * msg_bytes / beta_bytes_s


def allreduce_rhd(msg_bytes: float, p: int, alpha_s: float,
                  beta_bytes_s: float) -> float:
    """递归折半-倍增 all-reduce：2·log2(P)·α + 2(P-1)/P · D/β。

    出处：模块 08 第 5 章第 2.2 节。
    字节数与 ring 相同（同为带宽下界），时延步数降为 O(log P)。
    注意：α-β 模型不含争用，实际收益需实测（该章第 2.5 节）。
    """
    if p < 2:
        return 0.0
    return 2 * math.log2(p) * alpha_s + 2 * (p - 1) / p * msg_bytes / beta_bytes_s


def comm_share_of_tpot(t_allreduce_s: float, n_layers: int,
                       tpot_s: float) -> float:
    """每 token 通信（每层 2 次）占 TPOT 的比例。

    出处：模块 08 第 1 章第 2.5 节。这是判断网络是否为瓶颈的核心判据。
    """
    return 2 * n_layers * t_allreduce_s / tpot_s


def jitter_amplification(p_single: float, n_ops: int) -> float:
    """单次异常率经 n 次操作后「至少碰上一次」的概率 1-(1-p)^n。

    出处：模块 08 第 1 章第 2.6 节（n = 2L）；
          第 9 章第 2.2 节亦用于网关串联层数。
    """
    return 1.0 - (1.0 - p_single) ** n_ops


def queueing_amplification(rho: float) -> float:
    """排队放大 ρ/(1-ρ)。出处：模块 08 第 10 章第 2.1 节。"""
    if not 0.0 <= rho < 1.0:
        raise ValueError("利用率 rho 必须在 [0,1) 内")
    return rho / (1.0 - rho)


# --------------------------- 模块 07 第 13 章：扣除通信后的 SLO 上界

def b_slo(tpot_s: float, comm_s: float, weight_bytes: float,
          bandwidth_bytes_s: float, seq_len: int,
          kv_per_token: float) -> float:
    """扣除通信后的 SLO 批上界：((TPOT - T_comm)·BW - W)/(S·k)。

    出处：模块 07 第 13 章第 2.1 节。
    不扣通信会系统性高估，且 P 越大高估越多。
    返回值可能为负，表示该 TPOT 目标在此配置下不可达。
    """
    remaining = tpot_s - comm_s
    return (remaining * bandwidth_bytes_s - weight_bytes) / (seq_len * kv_per_token)


# ------------------------------ 模块 07 第 3、6 章：量化与主机瓶颈

def effective_bit_width(b_w: float, b_scale: float, group_size: int) -> float:
    """含缩放因子开销的有效位宽 b_w + b_s/g。出处：模块 07 第 3 章第 2.4 节。"""
    return b_w + b_scale / group_size


def host_bound_batch(t_device_s: float, per_request_host_s: float) -> float:
    """主机成为瓶颈的批 B* = t_dev / h。出处：模块 07 第 6 章第 2.1 节。

    设备越快 B* 越低——加速器优化会把瓶颈推给主机。
    """
    return t_device_s / per_request_host_s


# ------------------------------ 模块 07 第 4 章 / 模块 12 第 7 章：卸载

def hybrid_step_time(weight_bytes: float, resident_fraction: float,
                     bw_fast_bytes_s: float, bw_slow_bytes_s: float) -> float:
    """混合推理每步时间 φ·W/BW_fast + (1-φ)·W/BW_slow。

    出处：模块 12 第 7 章第 2.1 节（本地 batch=1 场景）。
    """
    if not 0.0 <= resident_fraction <= 1.0:
        raise ValueError("驻留比例 φ 必须在 [0,1] 内")
    return (resident_fraction * weight_bytes / bw_fast_bytes_s
            + (1 - resident_fraction) * weight_bytes / bw_slow_bytes_s)


def slow_side_share(resident_fraction: float, bw_fast_bytes_s: float,
                    bw_slow_bytes_s: float) -> float:
    """慢侧占总时间的比例。出处：模块 12 第 7 章第 2.1 节。

    两段各半的临界点是 (1-φ) = 1/(1+r)，其中 r = BW_fast/BW_slow。
    """
    fast = resident_fraction / bw_fast_bytes_s
    slow = (1 - resident_fraction) / bw_slow_bytes_s
    return slow / (fast + slow) if (fast + slow) > 0 else 0.0


# --------------------------- 模块 10 第 9 章：云边混合的交叉长度

def crossover_length(rtt_s: float, ttft_cloud_s: float, ttft_local_s: float,
                     rate_local: float, rate_cloud: float) -> float:
    """本地与云端耗时相等的输出长度 n*。

    出处：模块 10 第 9 章第 2.5 节。
    分母为负（本地更快）时返回 inf，表示本地在任意长度上都更快。
    """
    denom = 1.0 / rate_local - 1.0 / rate_cloud
    if denom <= 0:
        return math.inf
    return (rtt_s + ttft_cloud_s - ttft_local_s) / denom


def posthoc_fallback_ok(t_local_s: float, t_cloud_s: float,
                        local_success_rate: float) -> bool:
    """事后回退是否优于「总是走云端」：T_local < q·T_cloud。

    出处：模块 10 第 9 章第 2.5 节。该条件比 T_local < T_cloud 更严。
    """
    return t_local_s < local_success_rate * t_cloud_s


# --------------------------- 模块 10 第 9 章：聚合指标的稀释倍数

def dilution_local_delta(ppl_before: float, ppl_after: float,
                         affected_fraction: float) -> float:
    """把困惑度变化换算成受影响 token 上的局部 NLL 增量 Δ/f（nat）。

    出处：模块 10 第 9 章第 2.4 节。
    聚合指标把集中的损伤稀释了 1/f 倍。
    """
    if not 0.0 < affected_fraction <= 1.0:
        raise ValueError("受影响占比必须在 (0,1] 内")
    delta = math.log(ppl_after) - math.log(ppl_before)
    return delta / affected_fraction


def sample_size_two_proportion(p1: float, p2: float, power: float = 0.8,
                               alpha: float = 0.05) -> int:
    """检出两个比例之差所需的每组样本量（正态近似）。

    出处：模块 10 第 9 章第 3.4 节。用于逐能力验收门禁的样本量倒推。
    仅支持常用的 alpha=0.05 与 power in {0.8, 0.9}。
    """
    z_a = {0.05: 1.959964, 0.01: 2.575829}.get(alpha)
    z_b = {0.8: 0.841621, 0.9: 1.281552}.get(power)
    if z_a is None or z_b is None:
        raise ValueError("仅支持 alpha in {0.05,0.01} 与 power in {0.8,0.9}")
    if p1 == p2:
        raise ValueError("两个比例相同，无法定义可检出的效应量")
    p_bar = (p1 + p2) / 2
    n = (z_a + z_b) ** 2 * 2 * p_bar * (1 - p_bar) / (p1 - p2) ** 2
    return math.ceil(n)


# ------------------------------------------------------------ 自测

def _close(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def _run_self_tests() -> None:
    print("InferenceAtlas 复现工具箱 — 自测")
    print("=" * 62)

    # T1 KV 每 token 字节数（模块 02 第 5 章）
    k = kv_bytes_per_token(n_layers=80, n_kv_heads=8, head_dim=128,
                           bytes_per_elem=2)
    assert k == 2 * 80 * 8 * 128 * 2, k
    assert _close(k / KiB, 320.0)
    print("T1 KV 每 token 字节数          320.0 KiB           ✓")

    # T2 三个上界与恒等式（模块 07 第 5 章）
    W, Mt, BW, S = 140e9, 560e9, 3e12, 8192
    cap = decode_capacity(W, Mt, BW, S, k)
    assert _close(cap.reachable_fraction, 1 - W / Mt)
    assert _close(cap.c_max / cap.b_half, Mt / W - 1)
    print("T2 C_max/B_half = M/W - 1     %.3f  (M/W=%.1f)   ✓"
          % (cap.c_max / cap.b_half, Mt / W))

    # T2b 恒等式与 S、k 无关（模块 07 第 5 章的核心结论）
    for s2 in (1024, 65536):
        for k2 in (320 * KiB, 384 * KiB):
            c2 = decode_capacity(W, Mt, BW, s2, k2)
            assert _close(c2.reachable_fraction, cap.reachable_fraction)
            assert _close(c2.c_max / c2.b_half, cap.c_max / cap.b_half)
    print("T2b 恒等式与 S、k 无关                                ✓")

    # T3 吞吐在 B_half 处恰为上限的一半
    thr_half = decode_throughput(cap.b_half, W, BW, S, k)
    assert _close(thr_half, cap.ceiling_tok_s / 2)
    print("T3 B_half 处吞吐 = 上限/2                             ✓")

    # T4 半功率尺寸（模块 08 第 1 章）
    n_half = half_power_size(5e-6, 50e9)
    assert _close(n_half / KiB, 244.140625)
    print("T4 半功率尺寸                 244.1 KiB           ✓")

    # T5 ring 与 RHD 的带宽项相同、时延项不同（模块 08 第 5 章）
    D, P, a, b = 512 * KiB, 8, 1.5e-6, 900e9
    t_ring, t_rhd = allreduce_ring(D, P, a, b), allreduce_rhd(D, P, a, b)
    bw_term = 2 * (P - 1) / P * D / b
    assert _close(t_ring - 2 * (P - 1) * a, bw_term)
    assert _close(t_rhd - 2 * math.log2(P) * a, bw_term)
    assert t_rhd < t_ring
    print("T5 ring/RHD 带宽项相同, RHD 更快  %.1f vs %.1f us   ✓"
          % (t_ring * 1e6, t_rhd * 1e6))

    # T6 通信占 TPOT（模块 08 第 1 章第 2.5 节）
    share = comm_share_of_tpot(allreduce_ring(D, 8, 5e-6, 50e9), 80, 20e-3)
    assert 0.70 < share < 0.71, share
    print("T6 跨节点通信占 20ms TPOT      %.1f%%              ✓" % (share * 100))

    # T7 抖动放大（模块 08 第 1 章第 2.6 节）
    assert _close(jitter_amplification(1e-3, 160), 1 - 0.999 ** 160)
    assert 0.147 < jitter_amplification(1e-3, 160) < 0.149
    print("T7 抖动放大 p=1e-3, n=160     %.1f%%              ✓"
          % (jitter_amplification(1e-3, 160) * 100))

    # T8 排队放大（模块 08 第 10 章）
    assert _close(queueing_amplification(0.85), 0.85 / 0.15)
    assert 5.66 < queueing_amplification(0.85) < 5.68
    print("T8 排队放大 rho=0.85          %.2f                ✓"
          % queueing_amplification(0.85))

    # T9 扣通信前后的 B_SLO（模块 07 第 13 章）
    # P=16、域内 ring：每 token 通信 = 2L·T_AR
    t_ar_16 = allreduce_ring(D, 16, 1.5e-6, 900e9)
    comm = 2 * 80 * t_ar_16
    assert 7.3e-3 < comm < 7.4e-3, comm          # 约 7.37 ms
    assert 0.29 < comm / 25e-3 < 0.30            # 占 25ms TPOT 的 29.5%
    b_no = b_slo(25e-3, 0.0, W, 3e12 * 16, S, k)
    b_yes = b_slo(25e-3, comm, W, 3e12 * 16, S, k)
    assert b_yes < b_no, (b_no, b_yes)
    assert b_no / b_yes > 1.4, (b_no, b_yes)     # 不扣会显著高估
    print("T9 扣通信后 B_SLO 下降         %.0f -> %.0f (高估 %.2fx) ✓"
          % (b_no, b_yes, b_no / b_yes))

    # T10 有效位宽（模块 07 第 3 章）
    assert _close(effective_bit_width(4, 16, 32), 4.5)
    assert _close(effective_bit_width(4, 16, 128), 4.125)
    print("T10 有效位宽 g=32/128         4.500 / 4.125       ✓")

    # T11 主机瓶颈批（模块 07 第 6 章）
    assert _close(host_bound_batch(25e-3, 20e-6), 1250.0)
    print("T11 主机瓶颈批 B*             1250                ✓")

    # T12 混合推理：慢侧占比与临界点（模块 12 第 7 章）
    r = 800e9 / 50e9
    phi_crit = 1 - 1 / (1 + r)
    assert _close(slow_side_share(phi_crit, 800e9, 50e9), 0.5)
    assert 0.63 < slow_side_share(0.9, 800e9, 50e9) < 0.65
    print("T12 慢侧占比 phi=0.9          %.1f%%  (临界 phi=%.3f) ✓"
          % (slow_side_share(0.9, 800e9, 50e9) * 100, phi_crit))

    # T13 交叉输出长度（模块 10 第 9 章）
    n_star = crossover_length(1.5, 0.3, 0.4, 20.0, 60.0)
    assert 41 < n_star < 43, n_star
    assert crossover_length(1.5, 0.3, 0.4, 60.0, 20.0) == math.inf
    print("T13 交叉长度 RTT=1.5s         %.0f token           ✓" % n_star)

    # T14 事后回退的盈亏平衡比 T_l<T_c 更严
    assert not posthoc_fallback_ok(15.4, 5.45, 0.6)
    assert not posthoc_fallback_ok(4.0, 5.45, 0.6)   # 虽 T_l<T_c 但仍不满足
    assert posthoc_fallback_ok(3.0, 5.45, 0.6)
    print("T14 事后回退条件 T_l < q·T_c                          ✓")

    # T15 稀释倍数（模块 10 第 9 章）
    d_local = dilution_local_delta(8.20, 8.41, 0.02)
    assert 1.25 < d_local < 1.27, d_local
    assert 0.28 < math.exp(-d_local) < 0.29
    print("T15 局部 NLL 增量             %.2f nat (概率 x%.2f)  ✓"
          % (d_local, math.exp(-d_local)))

    # T16 样本量倒推（模块 10 第 9 章）
    n = sample_size_two_proportion(0.86, 0.81)
    assert 850 < n < 880, n
    print("T16 检出 86%%->81%% 每组样本    %d                 ✓" % n)

    # T17 边界与错误处理
    for bad in (lambda: decode_capacity(10, 5, 1, 1, 1),
                lambda: queueing_amplification(1.0),
                lambda: effective_bit_width(4, 16, 0),
                lambda: hybrid_step_time(1, 1.5, 1, 1),
                lambda: dilution_local_delta(8.2, 8.4, 0.0),
                lambda: sample_size_two_proportion(0.8, 0.8)):
        try:
            bad()
        except (ValueError, ZeroDivisionError):
            pass
        else:
            raise AssertionError("应当抛出异常但没有")
    print("T17 边界与错误处理                                    ✓")

    print("=" * 62)
    print("全部 17 项自测通过。")
    print()
    print("用法：把你实测的数字代入上述函数，得到可行性判断。")
    print("本工具箱不产生测量数据——输入必须来自你自己的实验。")


if __name__ == "__main__":
    _run_self_tests()
