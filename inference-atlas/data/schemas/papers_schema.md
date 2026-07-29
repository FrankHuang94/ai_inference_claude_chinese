# papers.csv — 论文与技术报告 — Schema

> 最后更新：2026-07-29 ｜ 对应文件：[`../papers.csv`](../papers.csv)

**ID 格式**：`P-XXX`（三位数字，如 `P-001`）

## 通用规则

| 规则 | 说明 |
|---|---|
| 编码 | UTF-8，无 BOM；换行 `\n` |
| 日期 | 一律 `YYYY-MM-DD` |
| URL | 必须 `https://` 开头，且为**一手来源** |
| 空值 | 禁止留空。无信息时填 `未公开`（确认厂商未披露）或 `待核实`（有线索未证实） |
| 多值 | 用 `;` 分隔（如多个作者、多个硬件平台） |
| 含逗号字段 | 由 CSV 双引号包裹（`csv` 模块自动处理） |
| 布尔类字段 | 取 `是` / `否` / `部分` / `待核实` |
| ID | 全库唯一，格式见下表；一经分配不得复用 |
| 数字 | 不得写超出来源精度的位数（避免伪精确）；带单位的数字必须在字段名或值中明确单位 |
| 枚举字段限定说明 | 允许写作 `枚举值（限定说明）`，如 `是（tensor parallel、pipeline parallel）`；校验时只比对括号前的枚举值 |

**披露等级枚举**（唯一合法取值）：`官方披露` / `技术文档披露` / `开源代码/配置披露` / `独立可复现实验` / `可信第三方估计` / `未公开` / `待核实`

由 [`scripts/validate_csv_schema.py`](../../scripts/validate_csv_schema.py) 强制校验。

## 字段定义

| 字段 | 类型 | 必填 | 说明 |
|---|---|:---:|---|
| `paper_id` | string | 是 | 全库唯一标识，格式 `P-XXX` |
| `title` | string | 是 | 论文原始英文标题，保持原文大小写 |
| `authors` | string | 是 | `姓, 名` 格式，多作者用 `;` 分隔；超过 8 位可写前 8 位加 `et al.` |
| `year` | integer | 是 | 正式发表年份；仅预印本时填预印本年份 |
| `venue` | string | 是 | 会议/期刊名称与年份，如 `SOSP 2023`；仅预印本填 `arXiv preprint` |
| `arxiv_or_doi_url` | url | 是 | arXiv abs 页、DOI 或会议论文官方页面 |
| `official_code_url` | url / `未公开` | 是 | 作者发布的官方实现；无则填 `未公开`（不得填第三方复现） |
| `category` | enum | 是 | 见下方分类枚举 |
| `sub_category` | string | 是 | 自由文本细分主题 |
| `one_sentence_contribution` | string | 是 | 一句话说清这篇论文改变了什么 |
| `technical_summary` | string | 是 | 2–5 句机制说明；不得复制摘要原文 |
| `key_equations_or_ideas` | string | 是 | 关键公式或核心思想的紧凑表述 |
| `inference_relevance` | string | 是 | 对推理系统的具体意义 |
| `hardware_or_system_relevance` | string | 是 | 对硬件/系统层的意义；无则填 `未公开` |
| `limitations` | string | 是 | **必填**：作者自述局限 + 工程视角局限。写 `无` 视为未完成 |
| `citation_status` | enum | 是 | `已核验` / `待核实`。`已核验` 表示已打开原文确认标题、作者、年份、venue |
| `last_verified_date` | date | 是 | 最后核验日期 |
| `document_link` | string | 是 | 对应论文卡片的仓库相对路径；尚未撰写填 `待创建` |

## category 枚举（唯一合法取值）

```text
Transformer Inference   KV Cache              Attention Optimization
Serving and Scheduling  Batching              Speculative Decoding
Quantization            Compression           Compilers
Runtime Systems         Kernels               Distributed Inference
MoE Serving             Hardware Architecture Memory Systems
Networking              Datacenter Systems    Edge Inference
Benchmarking            Reliability           Security
Agents                  Reasoning             Multimodal
Economics
```

## 录入纪律

1. `citation_status` 只有在**实际打开一手来源确认**元数据后才能填 `已核验`；
2. 不得凭记忆填写 arXiv 编号或会议年份；
3. `limitations` 是本表最容易被敷衍的字段，也是最有价值的字段之一；
4. 每新增一条记录，必须同步在 [`references.bib`](../references.bib) 追加 BibTeX 条目，`note` 字段写入 `paper_id`。
