# companies.csv — 公司与组织 — Schema

> 最后更新：2026-07-29 ｜ 对应文件：[`../companies.csv`](../companies.csv)

**ID 格式**：`organization` 字段本身即主键（组织官方英文名）

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
| `organization` | string | 是 | **主键**：组织官方名称，全库唯一且拼写一致 |
| `type` | enum | 是 | `芯片公司` / `云厂商` / `模型公司` / `推理软件公司` / `网络设备` / `光互连` / `内存` / `EMS/ODM` / `研究机构` / `其他` |
| `headquarters` | string | 是 | 总部所在地 |
| `founded_or_established` | string | 是 | 成立年份 |
| `core_business` | string | 是 | 主营业务 |
| `inference_positioning` | string | 是 | 在推理价值链中的位置 |
| `model_strategy` | string | 是 | 模型战略；不适用填 `不适用` |
| `hardware_strategy` | string | 是 | 硬件战略 |
| `software_strategy` | string | 是 | 软件与生态战略 |
| `networking_or_datacenter_strategy` | string | 是 | 网络/数据中心战略 |
| `edge_strategy` | string | 是 | 边缘战略 |
| `key_products` | string | 是 | 关键产品，`;` 分隔 |
| `key_customers_or_partners` | string | 是 | **仅限公开确认**的客户/伙伴；未确认填 `未公开` |
| `public_performance_claims` | string | 是 | 公开性能主张摘要，须可追溯到来源 |
| `business_model` | string | 是 | 商业模式 |
| `key_strengths` | string | 是 | 技术/商业优势 |
| `key_risks` | string | 是 | **必填**：风险与竞争压力 |
| `latest_material_event` | string | 是 | 最近重大事件；详细条目另录 `company_events.csv` |
| `official_source_url` | url | 是 | 官网、投资者关系页或官方公告 |
| `last_verified_date` | date | 是 | 最后核验日期（时效性等级：**高**，90 天复核） |
| `company_profile_link` | string | 是 | 深度档案路径；未撰写填 `待创建` |

## 录入纪律（本表风险最高）

1. **客户关系是最容易出错的字段**。只有官方新闻稿、财报、双方共同公告确认的关系才能写入
   `key_customers_or_partners`；媒体报道的"据悉""知情人士"一律填 `未公开`；
2. 不得将第三方估计、匿名爆料、社交媒体内容写成官方确认；
3. 不得在无可靠来源时编造任何公司的内部推理基础设施细节、集群规模、产能或财务数字；
4. `public_performance_claims` 记录的是"该公司主张了什么"，**不是**"该主张为真"——
   证据质量评估写在深度档案的对应小节；
5. 不使用"最快""最低成本""领先"等无来源绝对化表达；
6. 所有财务、capex、市场份额、融资数字必须链接一手来源（财报 / 10-K / 20-F / 正式公告）。

由 [`scripts/company_disclosure_audit.py`](../../scripts/company_disclosure_audit.py) 检查。
