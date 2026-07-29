# 推理指标速查卡

> 位置：[InferenceAtlas](../../INDEX.md) > [模块 01](README.md) > 当前文档
> 信息截至：2026-07-29 ｜ 最后核验：2026-07-29 ｜ 内容版本：v0.1
> 时效性等级：低
> 相关主题：[模块 01 全部文档](README.md)｜[全库速查](../00_start_here/06_metrics_units_and_quick_reference.md)

> **定位**：模块 01 的公式与判据压缩版。推导与讨论见各章。适合打印、贴屏、面试前复习。

---

## A. 六个必记公式

| # | 公式 | 用途 | 出处 |
|---:|---|---|---|
| 1 | $T_{E2E}=T_{queue}+T_{tokenize}+T_{prefill}+T_{decode}+T_{network}+T_{post}$ | 时延定位 | [02](02_latency_throughput_and_slo.md) |
| 2 | $L=\lambda W$ | 容量估算 | [03](03_queueing_theory_for_inference.md) |
| 3 | $W_q \propto \dfrac{\rho}{1-\rho}\cdot(1+C_S^2)$ | 利用率与方差对排队的影响 | [03](03_queueing_theory_for_inference.md) |
| 4 | $\text{Attainable}=\min(P,\ I\times BW)$ | 瓶颈判定 | [04](04_roofline_and_performance_modeling.md) |
| 5 | $\text{tokens/s}\le \dfrac{BW}{P_{params}\times b_w}$ | 单序列 decode 上界 | [05](05_memory_bandwidth_and_arithmetic_intensity.md) |
| 6 | $\text{Cost/Token}=\dfrac{\sum C_i}{\text{Capacity}\times U}$ | 单位经济性 | [06](06_cost_modeling_and_unit_economics.md) |

---

## B. 时延指标定义

设请求 $t_0$ 到达，首 token 于 $t_1$ 返回，共 $N$ 个输出 token，末 token 于 $t_N$。

| 指标 | 定义 | 单位 | 口径 |
|---|---|---|---|
| TTFT | $t_1-t_0$ | ms | **含**排队与分词 |
| 端到端 | $t_N-t_0$ | ms | 全六段 |
| TPOT | $\dfrac{t_N-t_1}{N-1}$ | ms/token | 分母 $N-1$ |
| ITL | $\{t_i-t_{i-1}\}$ | ms | **分布**，非均值 |

**报告必带**：分位数 + 样本量 + 观测窗口 + workload 条件 + 测量边界。

---

## C. 利用率对排队时延的放大

| $\rho$ | $\frac{\rho}{1-\rho}$ | 相对 0.5 |
|---:|---:|---:|
| 0.50 | 1.00 | 1× |
| 0.70 | 2.33 | 2.3× |
| 0.80 | 4.00 | 4× |
| 0.90 | 9.00 | 9× |
| 0.95 | 19.00 | 19× |
| 0.99 | 99.00 | 99× |

**再乘以 $(1+C_S^2)$**。LLM 输出长度跨两个数量级时 $C_S$ 可远大于 1 —— 这是推理系统尾时延比 Web 服务敏感得多的原因。

---

## D. 算术强度速查

| 阶段 | 算术强度 | 判定 |
|---|---|---|
| Decode | $I \approx \dfrac{2B}{b_w}$ | $B$ 小 → memory-bound |
| Prefill | $I \approx \dfrac{2S_{in}}{b_w}$ | 通常 compute-bound |

脊点 $I^*=P/BW$（纯硬件属性）。$I<I^*$ → memory-bound。

$b_w$：BF16=2，INT8=1，INT4=0.5（byte/参数）。

---

## E. 带宽预算的两个区间

临界并发：

$$
B^* = \frac{P_{params}\times b_w}{2LSH_{KV}D_h\, b_{kv}}
$$

| 区间 | 条件 | 优化手段 |
|---|---|---|
| 权重主导 | $B<B^*$ | 批处理、权重量化、投机解码、MoE |
| KV 主导 | $B>B^*$ | KV 量化、GQA/MLA、驱逐/滑窗、FlashAttention 类 |

**$B^*$ 与上下文长度成反比** —— 上下文越长越早进入 KV 主导区。

---

## F. 利用率对成本的放大

| $U$ | 相对满载单位成本 |
|---:|---:|
| 100% | 1.0× |
| 70% | 1.4× |
| 50% | 2.0× |
| 30% | **3.3×** |
| 15% | 6.7× |

**与 C 表的张力**：C 表说利用率不能太高（时延），F 表说不能太低（成本）。二者共同决定经济利用率上限。

---

## G. 容量规划计算链

1. $\lambda_{peak}=\bar{\lambda}\times\beta$
2. $B_{max}=\min\left(\dfrac{M_{avail}-M_W-M_{rt}}{M_{KV,\text{per-seq}}},\ B_{sat}\right)$ ← **两个约束取小**
3. $\lambda_{inst}=\dfrac{B_{max}\times\rho^{max}}{W}$
4. $N_{base}=\lceil \lambda_{peak}/\lambda_{inst}\rceil$
5. $N_{total}=N_{base}\times f_{redundancy}\times f_{growth}\times f_{region}$ ← **三因子相乘**

**长度 $S$ 用 P95，不用均值。**

---

## H. Workload 分类判据

$$
R = \frac{S_{in}}{S_{out}}
$$

| $R$ | 主导 | 瓶颈 | 优化方向 |
|---|---|---|---|
| ≫1 | prefill | 算力 + KV 容量 | chunked prefill、前缀缓存、上下文并行 |
| ≈1 | 均衡 | 综合 | continuous batching + 前缀缓存 |
| ≪1 | decode | 带宽 | 大批处理、量化、投机解码 |

---

## I. 单位红线

| 易混 | 区分 |
|---|---|
| GB / GiB | $10^9$ vs $2^{30}$ |
| **TB/s / Tb/s** | 内存带宽用 TB/s（字节）；网络用 Gb/s、Tb/s（比特） |
| TFLOPS / TOPS | 必须注明精度与是否含稀疏 |
| W / kW / MW | 必须注明 chip / board / server / rack / facility |
| $/1M tokens | 不用 $/token（诱发伪精确） |
| J/token | **必须注明测量边界** |

---

## J. 症状 → 首查

| 症状 | 首查 | 常见根因 |
|---|---|---|
| TTFT 高、TPOT 正常 | 队列深度 | 排队积压、长 prompt 未分块 |
| TPOT 高、TTFT 正常 | 带宽利用率 | 批太小、未量化、kernel 慢路径 |
| 均值正常、P99 差 | ITL 分布、抢占次数 | 批内长短干扰、KV 不足 |
| 并发升高后吞吐骤降 | KV 占用率 | cache thrashing（正反馈） |
| 吞吐低且利用率低 | 调度器组批 | 静态批处理、窗口设置不当 |
| 加显存后吞吐没变 | 带宽利用率 | 实际瓶颈是带宽不是容量 |
| 运行一段时间后变慢 | **温度与频率曲线** | 热降频、功率封顶 |
| 过载后不能自行恢复 | 抢占率 | 抢占重算正反馈，缺准入控制 |
| 成本高于预期 | **有效利用率** | 分母用了理论产能 |

---

## K. 精度纪律

| 输入 | 典型有效位数 |
|---|---|
| 利用率 | 1 |
| 运维分摊 | 1 |
| 折旧年限 | 1 |
| 硬件价格 | 2–3 |
| 电价、PUE | 2 |

→ **成本输出保留 1–2 位有效数字并给出区间。**

正确：`约 $0.4/1M tokens（利用率 50%，±50%）`
错误：`$0.42731/1M tokens`

---

## L. 三个"必须"与三个"不得"

**必须**：

1. 长度、到达率**必须**用分布（P50/P95/P99），不用均值；
2. 时延数字**必须**带分位数、样本量、观测窗口；
3. J/token、功耗**必须**注明测量边界。

**不得**：

1. **不得**用峰值算力预测 decode 性能；
2. **不得**只报吞吐不报时延（用 goodput）；
3. **不得**给出超出输入精度的有效位数。

---

## 主要来源

本速查卡汇总模块 01 各章结论，外部来源见对应章节：
[01](01_inference_workload_taxonomy.md) · [02](02_latency_throughput_and_slo.md) · [03](03_queueing_theory_for_inference.md) · [04](04_roofline_and_performance_modeling.md) · [05](05_memory_bandwidth_and_arithmetic_intensity.md) · [06](06_cost_modeling_and_unit_economics.md) · [07](07_energy_efficiency_and_joules_per_token.md) · [08](08_capacity_planning.md)

## 更新记录

| 日期 | 版本 | 变更 | 核验人 |
|---|---|---|---|
| 2026-07-29 | v0.1 | 初稿 | — |
