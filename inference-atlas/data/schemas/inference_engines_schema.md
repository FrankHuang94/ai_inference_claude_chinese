# inference_engines.csv — 推理引擎 — Schema

> 最后更新：2026-07-29 ｜ 对应文件：[`../inference_engines.csv`](../inference_engines.csv)

**ID 格式**：`E-XXX`

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
| `engine_id` | string | 是 | 全库唯一，格式 `E-XXX` |
| `name` | string | 是 | 项目官方名称与大小写 |
| `organization_or_community` | string | 是 | 维护方；若治理归属发生变化须注明 |
| `license` | string | 是 | SPDX 标识（如 `Apache-2.0`） |
| `primary_language` | string | 是 | 主要实现语言，`;` 分隔 |
| `supported_frameworks` | string | 是 | 支持的框架与模型格式 |
| `supported_hardware` | string | 是 | 支持的硬件；**成熟度不同的后端须注明** |
| `continuous_batching` | bool | 是 | `是` / `否` / `部分` / `待核实` |
| `paged_kv_cache` | bool | 是 | 同上 |
| `prefix_caching` | bool | 是 | 同上；若为特定实现（如 RadixAttention）在此注明 |
| `speculative_decoding` | bool | 是 | 同上 |
| `moe_support` | bool | 是 | 同上 |
| `distributed_inference_support` | bool | 是 | 同上；注明支持的并行方式 |
| `quantization_support` | bool | 是 | 同上；具体格式矩阵随版本变化，不在本字段穷举 |
| `observability_support` | bool | 是 | 同上；注明指标导出方式 |
| `key_differentiators` | string | 是 | 与同类项目的实质差异，不写营销语 |
| `official_source_url` | url | 是 | 官方仓库或官方文档 |
| `last_verified_date` | date | 是 | 最后核验日期（时效性等级：**高**，90 天复核） |
| `related_docs` | string | 是 | 对应文档相对路径；未撰写标注 `（待创建）` |

## 最低覆盖清单（最终目标 ≥ 40 条）

vLLM、SGLang、Hugging Face TGI、TensorRT-LLM、DeepSpeed-FastGen、Triton Inference Server、
Ray Serve、KServe、llama.cpp、MLX、Ollama、ONNX Runtime、OpenVINO、LMDeploy、LightLLM、
Aphrodite Engine，以及其他有可靠来源的项目。

## 录入纪律

1. 特性字段（`continuous_batching` 等）必须以**官方文档或可在仓库中直接验证的代码/配置**为依据，
   `disclosure_level` 概念上对应 `开源代码/配置披露`；
2. 开源项目演进快：特性矩阵**必须绑定核验日期**，且不写具体版本号以外的推断；
3. 不确定的后端支持填 `待核实`，不要凭 README 的宣称直接填 `是`；
4. `key_differentiators` 不得使用"最快""性能最强"等无来源绝对化表达。
