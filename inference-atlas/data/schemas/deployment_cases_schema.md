# deployment_cases.csv — 部署案例 — Schema

> 最后更新：2026-07-29 ｜ 对应文件：[`../deployment_cases.csv`](../deployment_cases.csv)

**ID 格式**：`D-XXX`

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
| `case_id` | string | 是 | 全库唯一，格式 `D-XXX` |
| `organization` | string | 是 | 部署方 |
| `application` | string | 是 | 应用场景 |
| `workload_type` | string | 是 | workload 分类 |
| `model_or_engine` | string | 是 | 模型与推理引擎 |
| `deployment_environment` | enum | 是 | `自建` / `公有云` / `混合` / `边缘` / `未公开` |
| `hardware` | string | 是 | 硬件；未披露填 `未公开` |
| `serving_architecture` | string | 是 | 架构要点 |
| `scale` | string | 是 | 规模；**只填公开数字**，未披露填 `未公开` |
| `slo` | string | 是 | 公开的 SLO；无则 `未公开` |
| `key_optimization` | string | 是 | 公开报告的关键优化 |
| `reported_outcome` | string | 是 | **原文口径复述**，不做外推 |
| `source_type` | enum | 是 | `官方博客` / `技术报告` / `会议演讲` / `论文` / `财报` / `第三方报道` |
| `source_url` | url | 是 | 一手来源 |
| `disclosure_level` | enum | 是 | `官方披露` / `技术文档披露` / `开源代码/配置披露` / `独立可复现实验` / `可信第三方估计` / `未公开` / `待核实` |
| `last_verified_date` | date | 是 | 最后核验日期 |
| `related_docs` | string | 是 | 关联文档路径 |

## 录入纪律

1. 本表**只记录公开披露**的内容。未披露部分填 `未公开`，
   不得用行业常识、类比或推测填充——这是本库最容易出现虚构的地方；
2. `reported_outcome` 必须是原文口径的复述。原文说"吞吐提升约 2 倍"就写"约 2 倍"并注明基线，
   不得换算成绝对数值；
3. 本库自身的解读必须写在对应文档的"本库解读"小节并显式标注为**本库推论**，不进入本字段；
4. 第三方报道（`source_type` = `第三方报道`）的 `disclosure_level` 不得填 `官方披露`。
