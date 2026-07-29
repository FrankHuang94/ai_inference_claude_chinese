# 模块 13 — 论文与技术报告地图

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**待开始**
> 模块目标字数：**≥ 12,000 字**
> 最后更新：2026-07-29

## 模块定位

本模块为推理领域的关键文献提供**结构化卡片**与阅读顺序，而非引用列表。每张卡片都要求写清适用边界与局限——论文的实验条件往往与生产环境相距甚远，识别这一差距本身就是核心能力。

## 前置阅读

[模块 02](../02_transformer_and_kv_cache/) 起的各技术模块

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | `01_paper_map.md` | 论文全景地图与阅读顺序 | 待开始 |
| 02 | `02_transformer_inference_and_kv_cache_papers.md` | Transformer 推理与 KV cache 论文卡片 | 待开始 |
| 03 | `03_batching_serving_and_scheduler_papers.md` | batching、serving 与调度器论文 | 待开始 |
| 04 | `04_speculative_decoding_papers.md` | 投机解码论文 | 待开始 |
| 05 | `05_quantization_and_compression_papers.md` | 量化与压缩论文 | 待开始 |
| 06 | `06_compiler_runtime_and_kernel_papers.md` | 编译器、runtime 与 kernel 论文 | 待开始 |
| 07 | `07_distributed_and_moe_inference_papers.md` | 分布式与 MoE 推理论文 | 待开始 |
| 08 | `08_hardware_and_architecture_papers.md` | 硬件与体系结构论文 | 待开始 |
| 09 | `09_networking_and_datacenter_papers.md` | 网络与数据中心论文 | 待开始 |
| 10 | `10_edge_inference_papers.md` | 边缘推理论文 | 待开始 |
| 11 | `11_reliability_and_benchmarking_papers.md` | 可靠性与基准测试论文 | 待开始 |
| 12 | `12_recent_reading_tracker.md` | 近期阅读追踪 | 待开始 |

## 写作要求

1. **每张论文卡片必须包括**：问题、背景、核心创新、算法或系统机制、实验设置、关键结果、适用边界、局限、后续影响、代码或实现、面试讨论角度、关联文档
2. **必须覆盖的主题**：Transformer inference、FlashAttention、PagedAttention、vLLM、Orca、Sarathi、FastServe、speculative decoding、Medusa、EAGLE、quantization、SmoothQuant、GPTQ、AWQ、TensorRT-LLM、distributed serving、MoE serving、HBM/memory systems、networking、edge inference、benchmarking、AI datacenter、serving reliability、agent inference、reasoning test-time compute
3. **每 session 最多深入完成 8–15 篇卡片**，避免低质量批量罗列
4. 每篇论文须同步录入 [`data/papers.csv`](../../data/papers.csv) 与 [`data/references.bib`](../../data/references.bib)
5. 不得大段复制论文原文；只做摘要、结构化与链接

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
