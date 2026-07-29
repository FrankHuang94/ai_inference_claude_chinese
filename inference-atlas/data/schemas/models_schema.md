# models.csv — 模型记录 — Schema

> 最后更新：2026-07-29 ｜ 对应文件：[`../models.csv`](../models.csv)

**ID 格式**：`M-XXX`

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
| `model_id` | string | 是 | 全库唯一，格式 `M-XXX` |
| `model_family` | string | 是 | 模型系列名 |
| `version` | string | 是 | 具体版本/日期标识；无版本号填 `未公开` |
| `organization` | string | 是 | 发布组织 |
| `release_date` | date / `未公开` | 是 | 公开发布日期 |
| `open_or_closed` | enum | 是 | `开放权重` / `闭源` / `部分开放` |
| `architecture` | string | 是 | 架构族（如 decoder-only Transformer） |
| `dense_or_moe` | enum | 是 | `dense` / `MoE` / `未公开` |
| `parameter_count` | string | 是 | 总参数量，注明单位（如 `70B`）；未披露填 `未公开`，**不得估算** |
| `active_parameter_count` | string | 是 | MoE 每 token 激活参数量；dense 模型填 `不适用` |
| `context_length` | string | 是 | 官方声明的最大上下文长度，注明 token 单位 |
| `modality` | string | 是 | 输入/输出模态，`;` 分隔 |
| `tokenizer` | string | 是 | 分词器类型与词表大小；未披露填 `未公开` |
| `kv_cache_design_disclosure` | string | 是 | KV 相关设计（MHA/GQA/MQA/MLA、KV heads 数等）；未披露填 `未公开` |
| `inference_optimization_disclosure` | string | 是 | 官方披露的推理优化（如 MTP、稀疏注意力）；无则 `未公开` |
| `quantization_official_support` | string | 是 | 官方发布或官方文档支持的量化格式；无则 `未公开` |
| `official_source_url` | url | 是 | 模型卡、技术报告或官方公告 |
| `disclosure_level` | enum | 是 | `官方披露` / `技术文档披露` / `开源代码/配置披露` / `独立可复现实验` / `可信第三方估计` / `未公开` / `待核实` |
| `last_verified_date` | date | 是 | 最后核验日期（时效性等级：**高**，90 天复核） |
| `model_profile_link` | string | 是 | 对应文档相对路径；未撰写填 `待创建` |

## 录入纪律

1. **参数量、上下文长度、KV 设计是最常被误传的三个字段**。只填官方模型卡、技术报告或官方公告中的数字；
   第三方拆解或社区推测一律填 `未公开`，或另起一行并把 `disclosure_level` 标为 `可信第三方估计`；
2. 同一模型不同版本（如不同上下文长度变体）应分列为不同记录，而非在单条记录中混写；
3. 闭源模型的架构细节通常 `未公开`——填 `未公开` 是正确答案，猜测是错误答案；
4. 本表时效性等级为**高**，`last_verified_date` 超过 90 天将被 `freshness_report.py` 标记。
