# 模块 01 — 基础、指标、排队论与成本

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**已完成**（26,531 字 ／ 9 篇 ／ 91 表 ／ 8 图）
> 模块目标字数：**≥ 14,000 字**
> 最后更新：2026-07-29

## 模块定位

本模块建立全库共用的**度量语言**。推理领域大量争论源于口径不一致：同一个 "TTFT" 在两份 benchmark 中可能相差一个排队时延，同一个 "吞吐" 可能是 output token 也可能是 total token。本模块把每个指标的测量边界钉死，并给出排队论与成本模型这两套贯穿全库的分析工具。

## 前置阅读

[模块 00](../00_start_here/)

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | [01_inference_workload_taxonomy.md](01_inference_workload_taxonomy.md) | 交互式、长上下文、RAG、reasoning、批量与 agent workload 的分类与特征 | 已完成 |
| 02 | [02_latency_throughput_and_slo.md](02_latency_throughput_and_slo.md) | TTFT/TPOT/ITL/端到端时延、吞吐与 SLO 的定义与测量口径 | 已完成 |
| 03 | [03_queueing_theory_for_inference.md](03_queueing_theory_for_inference.md) | Little's Law、M/M/1、M/M/c 与 tail latency 放大 | 已完成 |
| 04 | [04_roofline_and_performance_modeling.md](04_roofline_and_performance_modeling.md) | Roofline 模型与推理阶段的 compute/memory bound 判定 | 已完成 |
| 05 | [05_memory_bandwidth_and_arithmetic_intensity.md](05_memory_bandwidth_and_arithmetic_intensity.md) | 算术强度、带宽墙与 decode 阶段的内存受限本质 | 已完成 |
| 06 | [06_cost_modeling_and_unit_economics.md](06_cost_modeling_and_unit_economics.md) | cost/token 模型、假设边界与避免伪精确 | 已完成 |
| 07 | [07_energy_efficiency_and_joules_per_token.md](07_energy_efficiency_and_joules_per_token.md) | J/token、功耗测量口径与能效优化路径 | 已完成 |
| 08 | [08_capacity_planning.md](08_capacity_planning.md) | 容量规划：负载预测、余量、突发与预留 | 已完成 |
| 09 | [09_inference_metrics_cheat_sheet.md](09_inference_metrics_cheat_sheet.md) | 指标速查卡 | 已完成 |

## 写作要求

1. **指标**：TTFT、TPOT、ITL、端到端时延、P50/P95/P99、throughput、requests/s、tokens/s、goodput、concurrency、queue delay、GPU/加速器/内存利用率、cost per request、cost per input token、cost per output token、J/token、carbon intensity —— 每个指标都必须定义测量口径，并强调不同 benchmark 可能采用不同定义
2. **排队论**：Little's Law、M/M/1、M/M/c、arrival rate、service rate、utilization、queue delay、burst traffic、priority queues、preemption、head-of-line blocking、admission control、tail latency amplification
3. **至少三个带数字的教学案例**：交互式 chat 服务；企业 RAG 服务；高并发 agent workload
4. **必须给出并解释**：$\text{Latency}_{E2E} = \text{Queueing} + \text{Tokenization} + \text{Prefill} + \text{Decode} + \text{Network} + \text{Post-processing}$
5. **必须给出并解释**：$\text{Cost per Token} = \frac{C_{accelerator} + C_{power} + C_{network} + C_{software} + C_{operations}}{\text{Delivered Tokens}}$
6. 成本模型必须说明：假设、输入变量、单位、**不包括**的成本项、如何避免伪精确、为什么硬件单价低不必然意味着服务成本低、utilization/batching/输入长度/输出长度如何影响单位经济性

## 完成标准

- [x] 全部规划文档已按 [`templates/chapter_template.md`](../../templates/chapter_template.md) 完成
- [x] 模块正文合计 ≥ 14,000 字
- [x] 上述"写作要求"逐条覆盖
- [x] 所有事实性数字带来源链接与披露标签
- [x] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md)
- [x] 相关 [`data/`](../../data/) CSV 已更新
- [x] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [x] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
