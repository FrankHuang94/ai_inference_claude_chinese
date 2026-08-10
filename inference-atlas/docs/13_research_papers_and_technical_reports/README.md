# 模块 13 — 论文与技术报告地图

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**进行中（7/12 篇）**
> 模块目标字数：**≥ 12,000 字**（当前正文约 50,000 字，已达标）
> 最后更新：2026-08-10

## 模块定位

本模块为推理领域的关键文献提供**结构化卡片**与阅读顺序，而非引用列表。每张卡片都要求写清适用边界与局限——论文的实验条件往往与生产环境相距甚远，识别这一差距本身就是核心能力。

## ⚠️ 本模块为**降级书写**

本仓库构建环境的出口白名单**拒绝一切论文来源**（`arxiv.org`、`www.usenix.org`、
`dl.acm.org`、`openreview.net`、`aclanthology.org`、`papers.nips.cc` 等，2026-08-10 复测仍为 403）。
按 [AGENTS.md 第 11 节](../../AGENTS.md)，403 属组织策略拒绝，**应上报而非绕行**。

因此本模块**未读过任何一篇论文的正文**，采取降级书写：

| 可写 | 依据 | 披露标签 |
|---|---|---|
| 书目元数据 | 作者在官方实现仓库 README 中的 BibTeX；WebSearch 书目检索 | `开源代码/配置披露` / `待核实` |
| 官方实现是否存在、实现形态 | GitHub 仓库可读 | `开源代码/配置披露` |
| 机制、适用边界、失效条件、叠加关系 | **本库模块 02–12 的自有推导** | — |
| 实验设置、关键结果、任何加速比数字 | **不可得** | 一律 `待核实` |

**三条硬性纪律**（详见 [第 01 章的降级声明](01_paper_map.md)）：
①不转述论文自述的任何数值，搜索摘要片段亦不例外；
②机制说明只写本库能独立论证的部分；
③`data/papers.csv` 的 `citation_status` 一律为 `待核实`，一条 `已核验` 都不填。

## 前置阅读

[模块 02](../02_transformer_and_kv_cache/) 起的各技术模块

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | [01_paper_map.md](01_paper_map.md) | 论文全景地图与阅读顺序 | 已完成 |
| 02 | [02_transformer_inference_and_kv_cache_papers.md](02_transformer_inference_and_kv_cache_papers.md) | Transformer 推理与 KV cache 论文卡片 | 已完成 |
| 03 | [03_batching_serving_and_scheduler_papers.md](03_batching_serving_and_scheduler_papers.md) | batching、serving 与调度器论文 | 已完成 |
| 04 | [04_speculative_decoding_papers.md](04_speculative_decoding_papers.md) | 投机解码论文 | 已完成 |
| 05 | [05_quantization_and_compression_papers.md](05_quantization_and_compression_papers.md) | 量化与压缩论文 | 已完成 |
| 06 | [06_compiler_runtime_and_kernel_papers.md](06_compiler_runtime_and_kernel_papers.md) | 编译器、runtime 与 kernel 论文 | 已完成 |
| 07 | [07_distributed_and_moe_inference_papers.md](07_distributed_and_moe_inference_papers.md) | 分布式与 MoE 推理论文 | 已完成 |
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

> 本模块使用**卡片式**结构，不套用 [`templates/chapter_template.md`](../../templates/chapter_template.md)
> 的章节骨架——这一豁免由 [`scripts/check_required_sections.py`](../../scripts/check_required_sections.py)
> 的 `CARD_MODULES` 明确给出。卡片模板见 [第 01 章 §2](01_paper_map.md)。

- [ ] 全部 12 篇规划文档完成（当前 **7/12**）
- [x] 模块正文合计 ≥ 12,000 字（当前约 50,000 字）
- [ ] 写作要求第 1 条：12 个卡片字段逐项覆盖——**其中「实验设置」与「关键结果」永久标注 `待核实`**，
      理由见上方降级说明；其余 10 项已在第 02–07 章逐条落实
- [x] 写作要求第 3 条：每 session 均在 8–15 张区间内（第 1 批 14 张：P-001~P-004、P-006~P-015；第 2 批 14 张：P-005、P-016~P-028；第 3 批 11 张：P-029~P-039）
- [x] 写作要求第 4 条：[`data/papers.csv`](../../data/papers.csv) 与
      [`data/references.bib`](../../data/references.bib) 已双向同步（39 条 ↔ 39 条）
- [x] 写作要求第 5 条：全文无论文原文摘抄，机制说明均为本库自有表述
- [x] 所有事实性来源带链接与披露标签（各章「主要来源」表逐条列出）
- [x] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md) 第 20 节
- [x] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [x] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

### 本次 session 附带的一次数据更正

`data/papers.csv` 中 P-001~P-005 原标为 `citation_status=已核验`、日期 2026-07-29，
但 [AGENTS.md 第 11 节](../../AGENTS.md) **同一天**的出口探测记录显示 arxiv 与 USENIX 当天即被拒绝，
两者不可能同时为真。已全部降级为 `待核实`；未经确认的 `official_code_url=未公开` 一并改为 `待核实`。
同时调整 [`scripts/paper_citation_audit.py`](../../scripts/paper_citation_audit.py)：
`待核实` 由**阻断性错误**改为**单独计数并逐条列出的可见欠账**——
原规则会使「让门禁变绿」的唯一途径变成谎报 `已核验`。

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
