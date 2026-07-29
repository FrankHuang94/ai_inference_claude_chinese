# interview_questions.csv — 面试题库 — Schema

> 最后更新：2026-07-29 ｜ 对应文件：[`../interview_questions.csv`](../interview_questions.csv)

**ID 格式**：`Q01`–`Q100`（两位数字，零填充）

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
| `question_id` | string | 是 | `QNN`，全库唯一，最终恰好 100 条 |
| `topic` | enum | 是 | 见下方类别配额表；**必须使用表中的精确名称** |
| `subtopic` | string | 是 | 细分主题 |
| `difficulty` | enum | 是 | `中等` / `高` / `专家` |
| `question` | string | 是 | 题目全文 |
| `interviewer_intent` | string | 是 | 面试官通过此题考察什么 |
| `what_a_strong_answer_must_cover` | string | 是 | 强答案必须覆盖的要点，`;` 分隔 |
| `reference_answer` | string | 是 | **完整参考答案**。只给提纲视为未完成 |
| `common_mistakes` | string | 是 | **必填**：常见错误 |
| `follow_up_questions` | string | 是 | **必填**：可能追问，`;` 分隔 |
| `related_docs` | string | 是 | **必填**：至少一个本库文档路径 |
| `company_relevance` | string | 是 | 相关公司/岗位类型；无特定关联填 `通用` |
| `format` | enum | 是 | `概念` / `系统设计` / `计算` / `排查` / `编码` / `战略讨论` |
| `last_updated` | date | 是 | 最后更新日期 |
| `source_or_basis` | string | 是 | 题目依据（论文、公开技术报告、公开实践） |

## 类别配额（硬性约束，总计恰好 100）

| `topic` 取值 | 题数 |
|---|---:|
| 推理基础、指标、排队论、成本 | 12 |
| Transformer、prefill/decode 与 KV Cache | 16 |
| Serving、batching、调度、QoS | 16 |
| Compiler、kernel、量化与 runtime | 14 |
| 分布式、MoE、网络与 disaggregation | 18 |
| 硬件、HBM、数据中心、edge | 12 |
| Debug、benchmark、可靠性、安全 | 7 |
| 公司、论文与战略讨论 | 5 |
| **合计** | **100** |

由 [`scripts/interview_coverage_report.py`](../../scripts/interview_coverage_report.py) 强制校验：
总数、类别分布、答案完整性、必填字段、重复题目检测。

## 每题必须满足（10 条）

1. 直接包含完整参考答案；
2. 支持 2–5 分钟口头回答；
3. 包含明确结论；
4. 解释核心原理；
5. 给出设计、计算或排查路径；
6. 分析 trade-off；
7. 给出一个真实工程、论文或公开案例；
8. 写出局限或常见错误；
9. 链接至少一个数据库文档；
10. 涉及公司时，只能以公开资料为依据。

## 录入纪律

1. **每 session 最多完成 10–15 道**，不得一次性生成全部 100 道；
2. `reference_answer` 中的换行使用 `\n` 转义或保持单段紧凑表述，避免破坏 CSV 结构；
   完整排版版本写在 `docs/17_interview_prep/` 对应文档中；
3. 题目不得重复——`interview_coverage_report.py` 会做相似度检测。
