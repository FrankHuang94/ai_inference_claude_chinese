# accelerators.csv — 加速器 — Schema

> 最后更新：2026-07-29 ｜ 对应文件：[`../accelerators.csv`](../accelerators.csv)

**ID 格式**：`A-XXX`

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
| `accelerator_id` | string | 是 | 全库唯一，格式 `A-XXX` |
| `vendor` | string | 是 | 厂商 |
| `product_family` | string | 是 | 产品family/架构代号 |
| `product_name` | string | 是 | 具体型号；不同显存/功耗版本应分列 |
| `release_or_announce_date` | date | 是 | 发布或公告日期；须区分二者，在 `architecture_summary` 注明 |
| `market_segment` | enum | 是 | `训练` / `推理` / `训推一体` / `边缘` / `PC` |
| `architecture_summary` | string | 是 | 架构要点 |
| `process_node_disclosure` | string | 是 | 制程节点；厂商未确认填 `未公开` 或标 `可信第三方估计` |
| `compute_precision_modes` | string | 是 | 支持的精度，`;` 分隔 |
| `peak_compute_claim` | string | 是 | **理论峰值**，必须注明精度与是否含稀疏加速（如 `X TFLOPS BF16 dense`） |
| `hbm_or_memory_type` | string | 是 | 内存类型与代际 |
| `memory_capacity` | string | 是 | 容量，注明 `GB` 还是 `GiB` |
| `memory_bandwidth` | string | 是 | 带宽，单位 `TB/s`（字节） |
| `interconnect` | string | 是 | 互连类型与速率，注明 `GB/s` 或 `Gb/s` 及是否为双向合计 |
| `tdp_or_power` | string | 是 | 功耗，**必须注明 chip / board / module 级别** |
| `form_factor` | string | 是 | SXM / OAM / PCIe / 板卡 等 |
| `server_platform` | string | 是 | 对应服务器平台；关联 `server_platforms.csv` |
| `software_stack` | string | 是 | 驱动、runtime、编译器与框架支持 |
| `official_benchmark_or_source` | url | 是 | 官方规格页或 MLPerf 结果链接 |
| `disclosure_level` | enum | 是 | `官方披露` / `技术文档披露` / `开源代码/配置披露` / `独立可复现实验` / `可信第三方估计` / `未公开` / `待核实` |
| `last_verified_date` | date | 是 | 最后核验日期（时效性等级：**高**，180 天复核） |
| `hardware_profile_link` | string | 是 | 对应硬件卡片路径；未撰写填 `待创建` |

## 强制区分（本表的核心纪律）

| 必须区分 | 说明 |
|---|---|
| 理论峰值 vs 实际 benchmark | `peak_compute_claim` **只放理论峰值**；实测结果进 `benchmarks.csv` |
| 推理性能 vs 训练性能 | 不得用训练 benchmark 论证推理能力 |
| 官方宣称 vs 第三方测试 | 由 `disclosure_level` 区分 |
| 稀疏 vs dense 算力 | 峰值必须注明是否含 2:4 稀疏等加速 |
| chip / board / server / rack 功耗 | `tdp_or_power` 必须写明级别，跨级比较无效 |
| GB vs GiB、TB/s vs Tb/s | 见 [GLOSSARY](../../GLOSSARY.md) 单位书写规范 |

由 [`scripts/hardware_spec_audit.py`](../../scripts/hardware_spec_audit.py) 检查。

## 录入纪律

1. 未公开的制程、die size、成本一律填 `未公开`——**芯片规格是本库最禁止猜测的领域**；
2. 路线图产品在正式发布前，规格应标 `可信第三方估计` 或 `待核实`，不得标 `官方披露`；
3. 内存带宽须核对是**单卡合计**还是**每堆栈**。
