# 模块 16 — 未来路线

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**待开始**
> 模块目标字数：**≥ 12,000 字**
> 最后更新：2026-07-29

## 模块定位

本模块讨论尚未定型的技术方向。写作纪律的重点是**把已发生的事实与情景推演严格分开**：每条路线都必须给出可验证的里程碑与明确的失败条件，而不是单向的乐观叙事。

## 前置阅读

全部技术模块（02–12）

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | `01_inference_roadmap_overview.md` | 推理技术路线全景 | 待开始 |
| 02 | `02_kv_cache_as_a_system_resource.md` | KV cache 作为一等系统资源 | 待开始 |
| 03 | `03_disaggregated_serving_and_memory_fabric.md` | 解耦式服务与内存 fabric | 待开始 |
| 04 | `04_next_generation_speculative_decoding.md` | 下一代投机解码 | 待开始 |
| 05 | `05_reasoning_test_time_compute_and_cost.md` | reasoning 与 test-time compute 经济学 | 待开始 |
| 06 | `06_inference_aware_model_architecture.md` | 面向推理的模型架构设计 | 待开始 |
| 07 | `07_moe_at_scale_and_expert_routing.md` | 大规模 MoE 与专家路由 | 待开始 |
| 08 | `08_optical_interconnect_and_photonic_compute.md` | 光互连与光子计算 | 待开始 |
| 09 | `09_processing_in_memory_and_memory_centric_compute.md` | 存内计算与内存中心架构 | 待开始 |
| 10 | `10_compiler_autotuning_and_ai_for_systems.md` | 编译器自动调优与 AI for systems | 待开始 |
| 11 | `11_edge_agents_and_private_inference.md` | 端侧 agent 与私有推理 | 待开始 |
| 12 | `12_open_questions_and_scenarios.md` | 开放问题与情景推演 | 待开始 |

## 写作要求

1. **必须讨论的 25 条路线**：KV cache 作为系统资源；remote/disaggregated KV；prefill/decode disaggregation；inference-aware model design；KV-efficient architecture；multi-token prediction；speculative decoding；reasoning 与 test-time compute 成本；agent memory；MoE at scale；dynamic expert placement；optical interconnect；co-packaged optics；photonic compute；processing-in-memory；memory-centric compute；CXL memory；edge agents；private local inference；compiler autotuning；AI for systems；automatic performance optimization；sustainable inference；standardization；open vs proprietary stack
2. **每条路线必须包含**：问题、技术机制、公开证据、关键论文/公司、工程限制、成本和供应链限制、**可验证里程碑**、**失败条件**、1/3/5 年情景、对芯片/网络/内存/云和模型公司的影响
3. 情景推演必须显式标注为推论，不得与已披露事实混写

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
