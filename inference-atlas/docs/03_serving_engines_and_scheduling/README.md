# 模块 03 — Serving Engines、调度与 QoS

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**已完成**
> 模块目标字数：**≥ 17,000 字**
> 最后更新：2026-07-29

## 模块定位

本模块讨论**把模型变成服务**所需的一切。同一个模型、同一块 GPU，不同的批处理与调度策略可以带来数倍的吞吐差异和完全不同的 tail latency 形态。本模块的核心命题是：吞吐优化与时延优化在调度层是直接冲突的，工程价值在于**显式地选择冲突点**而非假装它不存在。

## 前置阅读

[模块 01](../01_foundations_and_metrics/)、[模块 02](../02_transformer_and_kv_cache/)

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | [01_serving_architecture_overview.md](01_serving_architecture_overview.md) | 从 gateway 到 worker 的 serving 架构全貌 | 已完成 |
| 02 | [02_static_dynamic_and_continuous_batching.md](02_static_dynamic_and_continuous_batching.md) | 三种 batching 的机制、收益与 tail latency 代价 | 已完成 |
| 03 | [03_pagedattention_and_kv_memory_management.md](03_pagedattention_and_kv_memory_management.md) | 分页式 KV 内存管理与碎片消除 | 已完成 |
| 04 | [04_request_scheduling_and_admission_control.md](04_request_scheduling_and_admission_control.md) | 调度策略、准入控制与 backpressure | 已完成 |
| 05 | [05_prefill_decode_scheduling.md](05_prefill_decode_scheduling.md) | chunked prefill 与 prefill/decode 干扰治理 | 已完成 |
| 06 | [06_multi_tenant_isolation_and_qos.md](06_multi_tenant_isolation_and_qos.md) | 多租户隔离、公平性与 QoS 分层 | 已完成 |
| 07 | [07_model_routing_and_cascade_systems.md](07_model_routing_and_cascade_systems.md) | 模型路由与级联：质量/成本自适应 | 已完成 |
| 08 | [08_prompt_caching_and_prefix_caching.md](08_prompt_caching_and_prefix_caching.md) | 前缀缓存的命中率、收益与隐私边界 | 已完成 |
| 09 | [09_session_memory_and_conversation_state.md](09_session_memory_and_conversation_state.md) | 会话状态与多轮对话的缓存复用 | 已完成 |
| 10 | [10_autoscaling_and_load_balancing.md](10_autoscaling_and_load_balancing.md) | 自动扩缩容、warm pool 与冷启动 | 已完成 |
| 11 | [11_serverless_and_burst_inference.md](11_serverless_and_burst_inference.md) | serverless 与突发容量的适用边界 | 已完成 |
| 12 | [12_serving_incident_playbook.md](12_serving_incident_playbook.md) | 线上事故分级、排查与降级手册 | 已完成 |

## 写作要求

1. **架构**：API gateway、auth、rate limit、request classification、model routing、tokenizer、queue、scheduler、worker、KV manager、output streaming、tool execution、logging、billing、autoscaling、regional failover
2. **深入比较**：static batching、dynamic batching、continuous batching、iteration-level scheduling、chunked prefill、preemption、priority scheduling、deadline-aware scheduling、fairness、throughput-first、latency-first、cost-first、quality-tiered serving
3. **必须解释**：为什么 continuous batching 能提高 utilization；何时它会损害 tail latency；长 prompt、长 output 与短 query 混合时的干扰；如何隔离 workload；backpressure；admission control；multi-tenant QoS；SLO design；degraded mode；routing 与 cascade；autoscaling；warm pool；cold start；model loading；capacity reservation；spot/interruptible capacity 的边界
4. **必须包含**：serving 请求生命周期图；batching 对比；PagedAttention 图；scheduler 决策树；SLO 分层表；queue/throughput/tail latency 关系图；cascade 架构图；incident response playbook；vLLM、SGLang、TGI、TensorRT-LLM 等**公开**架构对比表
5. **伪代码**：continuous batching scheduler；paged KV block allocator；prefix cache lookup；admission controller；model router；autoscaler

## 完成标准

- [x] 全部规划文档已按 [`templates/chapter_template.md`](../../templates/chapter_template.md) 完成
- [x] 模块正文合计 ≥ 17,000 字
- [x] 上述"写作要求"逐条覆盖
- [x] 所有事实性数字带来源链接与披露标签
- [x] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md)
- [x] 相关 [`data/`](../../data/) CSV 已更新
- [x] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [x] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
