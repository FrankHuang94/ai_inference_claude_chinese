# techniques.csv — 技术卡片 — Schema

> 最后更新：2026-07-29 ｜ 对应文件：[`../techniques.csv`](../techniques.csv)

**ID 格式**：`T-XXX`

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
| `technique_id` | string | 是 | 全库唯一，格式 `T-XXX` |
| `name` | string | 是 | `中文名 / English` 形式 |
| `category` | string | 是 | 所属技术类别 |
| `problem_solved` | string | 是 | 不用该技术时的具体痛点及其出现条件 |
| `core_idea` | string | 是 | 核心思想 |
| `math_or_algorithm` | string | 是 | 关键公式或算法要点 |
| `implementation_notes` | string | 是 | 工程实现要点与组件交互 |
| `latency_effect` | string | 是 | 对 TTFT/TPOT 的影响方向与条件 |
| `throughput_effect` | string | 是 | 对吞吐的影响 |
| `memory_effect` | string | 是 | 对显存的影响 |
| `quality_effect` | string | 是 | 对输出质量的影响；无影响填 `无（不改变数值计算）` |
| `energy_effect` | string | 是 | 对能耗的影响 |
| `common_failures` | string | 是 | **必填**：常见失败模式 |
| `key_papers` | string | 是 | 关联 `paper_id`，`;` 分隔 |
| `open_source_implementations` | string | 是 | 开源实现，`;` 分隔 |
| `maturity` | enum | 是 | `研究阶段` / `早期采用` / `生产成熟` / `事实标准` |
| `related_docs` | string | 是 | 关联文档路径 |
| `last_verified_date` | date | 是 | 最后核验日期 |

## 最低覆盖清单（最终目标 ≥ 90 条）

continuous batching、PagedAttention、prefix caching、prompt caching、KV cache quantization、
KV cache offloading、MQA、GQA、MLA、FlashAttention、speculative decoding、Medusa、EAGLE、
multi-token prediction、tensor parallel、pipeline parallel、expert parallel、disaggregated serving、
load balancing、admission control、INT8、INT4、FP8、FP4、AWQ、GPTQ、SmoothQuant、structured output、
grammar decoding、LoRA serving、multi-LoRA、model routing、cascade、autoscaling、energy-aware scheduling。

## 录入纪律

1. 效果字段（`latency_effect` 等）必须写**影响方向 + 条件**，不能只写"提升"。
   带量级的数字必须有公开可核验来源，否则填 `待核实`；
2. `common_failures` 与"何时不该用"是本表最有价值的部分，写 `无` 视为未完成；
3. `quality_effect` 必须明确该技术是否改变数值结果——这是选型时的关键判据。
