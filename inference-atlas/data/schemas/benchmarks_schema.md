# benchmarks.csv — benchmark 结果 — Schema

> 最后更新：2026-07-29 ｜ 对应文件：[`../benchmarks.csv`](../benchmarks.csv)

**ID 格式**：`B-XXX`

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
| `benchmark_id` | string | 是 | 全库唯一，格式 `B-XXX` |
| `benchmark_name` | string | 是 | benchmark 名称 |
| `organization` | string | 是 | 发布方 |
| `date` | date | 是 | 结果发布日期 |
| `workload` | string | 是 | workload 类型 |
| `model` | string | 是 | 模型名 |
| `model_version` | string | 是 | 版本/checkpoint；未注明填 `未公开` |
| `model_parameterization` | string | 是 | dense/MoE、参数量、激活参数量 |
| `hardware` | string | 是 | 加速器型号 |
| `accelerator_count` | integer / `未公开` | 是 | 加速器数量 |
| `memory_configuration` | string | 是 | 显存与主机内存配置 |
| `network_configuration` | string | 是 | 网络配置；单机填 `不适用` |
| `software_stack` | string | 是 | **引擎与版本号**、驱动、CUDA 等 |
| `quantization` | string | 是 | 量化方案；未量化填 `无` |
| `input_tokens` | string | 是 | 输入长度或其分布 |
| `output_tokens` | string | 是 | 输出长度或其分布 |
| `batch_or_concurrency` | string | 是 | batch size 或并发数 |
| `ttft_ms` | number / `未公开` | 是 | 注明分位数 |
| `tpot_ms` | number / `未公开` | 是 | 同上 |
| `itl_ms` | number / `未公开` | 是 | 同上 |
| `end_to_end_latency_ms` | number / `未公开` | 是 | 同上 |
| `throughput_tokens_per_sec` | number / `未公开` | 是 | 注明是 output token 还是 total token |
| `requests_per_sec` | number / `未公开` | 是 | — |
| `goodput_definition` | string | 是 | 所用 SLO 定义；未报告 goodput 填 `未公开` |
| `power_w` | number / `未公开` | 是 | **注明测量边界**（chip/node/rack/facility） |
| `energy_per_token_j` | number / `未公开` | 是 | 同上 |
| `cost_basis` | string | 是 | 计费基准与假设；未报告填 `未公开` |
| `source_type` | enum | 是 | `MLPerf 官方` / `厂商官方` / `第三方独立` / `论文` / `本库复现` |
| `source_url` | url | 是 | 结果原始链接 |
| `reproducibility_level` | enum | 是 | `完整可复现` / `部分可复现` / `不可复现` |
| `caveats` | string | 是 | **必填**：可比性限制、cherry-picking 风险、口径差异 |
| `last_verified_date` | date | 是 | 最后核验日期 |

## 最低充分条件

以下任一项缺失，该 benchmark **不可跨来源比较**，必须在 `caveats` 中显式说明：

模型版本、硬件、软件栈版本、量化方案、输入长度、输出长度、batch/concurrency、
warmup 方式、latency 定义、throughput 定义、功耗测量边界、来源 URL、可复现性、caveat。

由 [`scripts/benchmark_audit.py`](../../scripts/benchmark_audit.py) 检查。

## 录入纪律

1. **没有公开的数据填 `未公开`，绝对不得猜测或从其他配置外推**；
2. 时延数字必须绑定分位数——只写"平均 TTFT"而不写样本量与分布，价值极低；
3. 理论峰值算力**不属于本表**，应放 `accelerators.csv` 的 `peak_compute_claim`；
4. 厂商 benchmark 与第三方 benchmark 必须由 `source_type` 区分，不得混合排名；
5. `caveats` 写 `无` 视为未完成——任何 benchmark 都有适用边界。
