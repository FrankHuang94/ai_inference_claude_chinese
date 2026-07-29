# 模块 05 — 解码、Speculative 与 Reasoning 推理

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**待开始**
> 模块目标字数：**≥ 13,000 字**
> 最后更新：2026-07-29

## 模块定位

解码算法是少数能同时改变**质量、时延和成本**三条曲线的杠杆。投机解码可以在不改变输出分布的前提下降低时延，但收益强依赖于接受率、draft 开销与 batch 状态；reasoning 模型则把 test-time compute 变成了一个需要被显式治理的成本变量。本模块要求对"何时无收益"给出同样清晰的判据。

## 前置阅读

[模块 02](../02_transformer_and_kv_cache/)、[模块 03](../03_serving_engines_and_scheduling/)

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | `01_decoding_basics.md` | 自回归解码循环与采样接口 | 待开始 |
| 02 | `02_greedy_sampling_topk_topp_temperature.md` | 采样参数对质量、时延与可复现性的影响 | 待开始 |
| 03 | `03_beam_search_and_constrained_decoding.md` | beam search 与约束解码的推理代价 | 待开始 |
| 04 | `04_speculative_decoding.md` | draft/verify 机制、接受率与真实收益判定 | 待开始 |
| 05 | `05_medusa_eagle_and_multi_token_prediction.md` | 多头/树形投机与多 token 预测 | 待开始 |
| 06 | `06_draft_model_selection_and_acceptance_rate.md` | draft 模型选型与接受率工程 | 待开始 |
| 07 | `07_reasoning_inference_and_test_time_scaling.md` | test-time compute 的质量-成本曲线 | 待开始 |
| 08 | `08_tool_use_and_agent_inference.md` | 工具调用与 agent 循环的推理特征 | 待开始 |
| 09 | `09_structured_output_and_grammar_constrained_decoding.md` | JSON mode 与语法约束解码 | 待开始 |
| 10 | `10_generation_quality_latency_tradeoffs.md` | 生成质量与时延的系统级权衡 | 待开始 |

## 写作要求

1. **解码基础**：greedy、temperature、top-k、top-p、min-p、beam search、constrained decoding、grammar constrained decoding、JSON mode、tool-call constrained generation、repetition penalty、stop token
2. **投机解码深入**：draft model、target model、proposal、verification、acceptance、rejection、expected speedup、acceptance rate、draft overhead、target batch interaction、multi-token、tree speculation、Medusa、EAGLE、multi-token prediction、self-speculative；硬件依赖性；**为什么某些 workload 上不一定加速**；质量一致性与采样兼容性
3. **Reasoning / test-time compute**：longer rollout、self-consistency、verifier、search、tool use、code execution、multi-agent、compute budget、quality vs cost、latency governance、user tiering、rate limiting、safety
4. **伪代码**：speculative decoding；top-k/top-p sampler

## 完成标准

- [ ] 全部规划文档已按 [`templates/chapter_template.md`](../../templates/chapter_template.md) 完成
- [ ] 模块正文合计 ≥ 13,000 字
- [ ] 上述"写作要求"逐条覆盖
- [ ] 所有事实性数字带来源链接与披露标签
- [ ] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md)
- [ ] 相关 [`data/`](../../data/) CSV 已更新
- [ ] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [ ] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
