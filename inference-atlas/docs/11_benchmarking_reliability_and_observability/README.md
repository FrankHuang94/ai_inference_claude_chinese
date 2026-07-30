# 模块 11 — Benchmark、可靠性、可观测性与安全

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**进行中（2/11 篇）**
> 模块目标字数：**≥ 12,000 字**
> 最后更新：2026-07-29

## 模块定位

推理 benchmark 极易被无意或有意地做成不可比。本模块给出一份**严谨 benchmark 的最小充分条件清单**，并说明 MLPerf 能回答与不能回答的问题。可靠性与可观测性部分则关注：当系统在生产中劣化时，需要哪些信号才能在数分钟内定位到层。

## 前置阅读

[模块 01](../01_foundations_and_metrics/)、[模块 03](../03_serving_engines_and_scheduling/)

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | [01_inference_benchmarking_methodology.md](01_inference_benchmarking_methodology.md) | 严谨推理 benchmark 的设计方法论 | 已完成 |
| 02 | `02_mlperf_inference.md` | MLPerf Inference 能回答与不能回答的问题 | 待开始 |
| 03 | [03_ttft_tpot_itl_and_end_to_end_latency.md](03_ttft_tpot_itl_and_end_to_end_latency.md) | 时延指标的精确定义与测量陷阱 | 已完成 |
| 04 | `04_throughput_concurrency_and_goodput.md` | 吞吐、并发与 goodput | 待开始 |
| 05 | `05_power_energy_and_cost_benchmarks.md` | 功耗、能耗与成本基准 | 待开始 |
| 06 | `06_profiling_gpu_cpu_network_and_memory.md` | 全栈 profiling 方法 | 待开始 |
| 07 | `07_observability_metrics_logs_traces.md` | 指标、日志与 trace 体系 | 待开始 |
| 08 | `08_slos_slas_and_error_budgets.md` | SLO/SLA 与错误预算 | 待开始 |
| 09 | `09_reliability_incidents_and_capacity_failures.md` | 可靠性事故与容量失效模式 | 待开始 |
| 10 | `10_safety_security_and_abuse_controls.md` | 安全、滥用防护与租户隔离 | 待开始 |
| 11 | `11_benchmark_case_studies.md` | benchmark 案例研究 | 待开始 |

## 写作要求

1. **方法论**：offline vs online；synthetic vs production；prompt/output length；concurrency；warmup；quantization；software version；cache state；tokenizer；streaming；latency histogram；throughput；goodput；energy；cost；reproducibility；cherry-picking
2. **MLPerf**：作用；能回答的问题；**不能回答的问题**；closed/open division；为什么不能直接把结果外推到所有生产 workload
3. **可观测性**：metrics、logs、traces、GPU/CPU/memory profiling、network telemetry、queue depth、cache hit rate、batch size、scheduler decisions、kernel time、error rate、model quality signals、incident response
4. **可靠性**：availability、SLO、SLA、error budget、overload、rate limiting、fallback、multi-region、chaos testing、canary、rollback、capacity incident、cascading failure、backpressure
5. **安全**：API abuse、prompt injection、data exfiltration、tenant isolation、cache privacy、model theft、tool safety、supply-chain security
6. **伪代码**：benchmark harness；incident triage

## 完成标准

- [ ] 全部规划文档已按 [`templates/chapter_template.md`](../../templates/chapter_template.md) 完成
- [ ] 模块正文合计 ≥ 12,000 字
- [ ] 上述"写作要求"逐条覆盖
- [ ] 所有事实性数字带来源链接与披露标签
- [ ] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md)
- [ ] 相关 [`data/`](../../data/) CSV 已更新
- [ ] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [ ] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
