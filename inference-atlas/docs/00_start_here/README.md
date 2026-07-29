# 模块 00 — 入门与端到端总览

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**待开始**
> 模块目标字数：**≥ 8,000 字**
> 最后更新：2026-07-29

## 模块定位

本模块是 InferenceAtlas 的入口。它回答两个问题：**一次用户请求在推理系统中究竟经历了什么**，以及**这些环节各自决定了哪一个性能、成本或可靠性指标**。读完本模块，读者应能在脑中重建从 HTTP 请求到最后一个 token 返回的完整路径，并知道当某个指标劣化时应该去哪一层排查。

## 前置阅读

无（本模块为全库起点）

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | `00_database_guide.md` | 如何使用本数据库：结构、约定、披露等级与检索路径 | 待开始 |
| 02 | `01_executive_summary.md` | AI 推理全景的一页式摘要：技术栈、瓶颈与产业格局 | 待开始 |
| 03 | `02_end_to_end_inference_lifecycle.md` | 从用户请求到 token 返回的完整路径与各层责任 | 待开始 |
| 04 | `03_how_to_read_inference_benchmarks.md` | 如何判断一份推理 benchmark 是否可比、可复现、可采信 | 待开始 |
| 05 | `04_how_to_design_an_inference_system.md` | 推理系统设计的通用方法论与决策顺序 | 待开始 |
| 06 | `05_how_to_prepare_for_inference_interviews.md` | 推理相关岗位的能力地图与准备策略 | 待开始 |
| 07 | `06_metrics_units_and_quick_reference.md` | 全库指标、单位与口径速查表 | 待开始 |

## 写作要求

1. AI inference 的定义；训练 / batch inference / 实时推理 / agent 推理 / edge 推理的区别
2. 用户请求到 token 返回的全路径：prompt ingestion、tokenization、API gateway、auth、rate limiting、queue、scheduler、prefill、decode、KV cache、streaming、safety、tool calling、logging、billing、autoscaling、observability
3. GPU/ASIC、网络、存储、电力、散热之间的关系
4. 为什么推理工作负载不同于传统分类模型
5. 为什么 TTFT、TPOT、tail latency、goodput、cost/token 必须同时优化
6. **必须包含**端到端请求生命周期 Mermaid 图（client → gateway → auth/rate limit → router → queue/scheduler → tokenizer → prefill worker → KV cache manager → decode worker → streaming → logging/tracing/billing → autoscaler）
7. **必须包含**：推理关键指标速查表；推理系统层级与责任矩阵；性能问题定位到层的排查表；工程师学习路径；硬件与网络学习路径；战略与投资学习路径

## 完成标准

- [ ] 全部规划文档已按 [`templates/chapter_template.md`](../../templates/chapter_template.md) 完成
- [ ] 模块正文合计 ≥ 8,000 字
- [ ] 上述"写作要求"逐条覆盖
- [ ] 所有事实性数字带来源链接与披露标签
- [ ] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md)
- [ ] 相关 [`data/`](../../data/) CSV 已更新
- [ ] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [ ] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
