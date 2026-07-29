# 模块 06 — 分布式、MoE 与 Disaggregated Inference

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**待开始**
> 模块目标字数：**≥ 17,000 字**
> 最后更新：2026-07-29

## 模块定位

当模型放不进单卡、或单卡吞吐不足时，推理进入分布式领域。与训练不同，推理的分布式设计被**每个 token 都要付一次通信代价**这一事实主导：TP 的 all-reduce 落在 decode 的关键路径上，MoE 的 all-to-all 受 token 分布倾斜影响，prefill/decode 分离则用 KV 迁移换取资源画像的匹配。

## 前置阅读

[模块 02](../02_transformer_and_kv_cache/)、[模块 03](../03_serving_engines_and_scheduling/)

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | `01_distributed_inference_overview.md` | 何时需要分布式推理及其代价 | 待开始 |
| 02 | `02_tensor_parallel_inference.md` | TP 的通信模式与时延影响 | 待开始 |
| 03 | `03_pipeline_parallel_inference.md` | PP 的气泡、微批与推理适配性 | 待开始 |
| 04 | `04_sequence_context_parallel_inference.md` | 长上下文的序列/上下文并行 | 待开始 |
| 05 | `05_moe_inference_and_expert_parallelism.md` | MoE 推理与专家并行 | 待开始 |
| 06 | `06_moe_routing_all_to_all_and_load_balancing.md` | all-to-all、token 倾斜与热专家治理 | 待开始 |
| 07 | `07_prefill_decode_disaggregation.md` | prefill/decode 池分离的收益与边界 | 待开始 |
| 08 | `08_kv_cache_transfer_and_remote_memory.md` | KV 迁移、RDMA 与远端内存 | 待开始 |
| 09 | `09_multi_node_serving_topologies.md` | 多节点部署拓扑与放置策略 | 待开始 |
| 10 | `10_fault_tolerance_and_graceful_degradation.md` | 故障域、容错与优雅降级 | 待开始 |
| 11 | `11_distributed_serving_case_studies.md` | 公开分布式推理案例研究 | 待开始 |

## 写作要求

1. **并行方式**：tensor parallel、pipeline parallel、sequence parallel、context parallel、expert parallel、replica、multi-node serving；collective communication、NCCL、topology-aware placement、rank mapping、communication overlap；scale-up、scale-out、failure domain
2. **MoE serving**：router、active expert、expert placement、expert parallel、all-to-all、dispatch、combine、token skew、expert imbalance、hot expert、routing locality、shared expert、load-aware routing、capacity planning、quality implications
3. **Prefill/decode disaggregation**：两阶段资源需求差异、prefill pool、decode pool、KV transfer、GPU-to-GPU、RDMA、remote memory、scheduling、state consistency、failure recovery、cost、utilization；**何时不适合使用 disaggregation**
4. **必须包含**：分布式推理并行图；MoE all-to-all 图；prefill/decode disaggregation 图；KV transfer 数据路径；dense vs MoE serving 表；scale-up vs scale-out 决策框架；disaggregation 经济性模型；网络瓶颈排查表
5. **伪代码**：TP/EP placement；MoE dispatch；disaggregated prefill/decode coordinator

## 完成标准

- [ ] 全部规划文档已按 [`templates/chapter_template.md`](../../templates/chapter_template.md) 完成
- [ ] 模块正文合计 ≥ 17,000 字
- [ ] 上述"写作要求"逐条覆盖
- [ ] 所有事实性数字带来源链接与披露标签
- [ ] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md)
- [ ] 相关 [`data/`](../../data/) CSV 已更新
- [ ] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [ ] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
