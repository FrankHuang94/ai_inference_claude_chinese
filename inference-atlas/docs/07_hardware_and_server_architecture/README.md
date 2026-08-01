# 模块 07 — 硬件、HBM、封装与服务器

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**8/8 篇可撰写文档已完成；另有 5 篇受阻，见下**
> 模块目标字数：**≥ 18,000 字**
> 最后更新：2026-07-31

## 模块定位

本模块把上层的所有优化落到物理约束上。LLM decode 的本质是**把权重从 HBM 搬到计算单元**，因此显存带宽与容量往往比峰值算力更能预测实际吞吐。本模块要求严格区分理论峰值与实测、训练性能与推理性能，以及 chip / board / server / rack 四级功耗口径。

## 前置阅读

[模块 01](../01_foundations_and_metrics/)、[模块 02](../02_transformer_and_kv_cache/)

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | [01_ai_inference_hardware_overview.md](01_ai_inference_hardware_overview.md) | 推理硬件全景与分类 | 已完成 |
| 02 | [02_gpu_architecture_for_inference.md](02_gpu_architecture_for_inference.md) | GPU 微架构中与推理相关的部分 | 已完成 |
| 03 | [03_tensor_cores_matrix_engines_and_low_precision.md](03_tensor_cores_matrix_engines_and_low_precision.md) | 矩阵引擎与低精度算力 | 已完成 |
| 04 | [04_hbm_dram_and_memory_hierarchy.md](04_hbm_dram_and_memory_hierarchy.md) | HBM/DRAM/SRAM 层次与带宽 | 已完成 |
| 05 | [05_memory_capacity_bandwidth_and_kv_cache.md](05_memory_capacity_bandwidth_and_kv_cache.md) | 显存容量/带宽如何约束 KV cache 与并发 | 已完成 |
| 06 | [06_gpu_server_node_architecture.md](06_gpu_server_node_architecture.md) | 服务器节点：CPU、PCIe、NVLink、NIC、存储 | 已完成 |
| 07 | [07_inference_asic_architectures.md](07_inference_asic_architectures.md) | 推理 ASIC 的架构取舍 | 已完成 |
| 08 | `08_nvidia_amd_intel_and_custom_accelerators.md` | 主流商用加速器对比 | **受阻**（内容本体为需核验的厂商规格与供应链数据） |
| 09 | `09_google_tpu_aws_inferentia_trainium_and_maia.md` | 超大规模厂商自研芯片 | **受阻**（内容本体为需核验的厂商规格与供应链数据） |
| 10 | `10_groq_cerebras_sambanova_dmatrix_etched_tenstorrent.md` | 推理初创公司的架构路线 | **受阻**（内容本体为需核验的厂商规格与供应链数据） |
| 11 | `11_advanced_packaging_chiplets_and_ucie.md` | 先进封装、chiplet 与 UCIe | **受阻**（内容本体为需核验的厂商规格与供应链数据） |
| 12 | `12_hbm_supply_chain_and_memory_roadmaps.md` | HBM 供应链与内存路线图 | **受阻**（内容本体为需核验的厂商规格与供应链数据） |
| 13 | [13_hardware_selection_framework.md](13_hardware_selection_framework.md) | 面向 workload 的硬件选型框架 | 已完成 |

> **关于受阻的五篇**：下方「写作要求」第 6 条规定「所有规格必须标注来源与披露等级」，
> 而当前网络出口策略下本库无法访问厂商文档、标准文本或供应链资料
> （详见 [AGENTS.md 第 11 节](../../AGENTS.md)）。
> 这五篇的内容本体即是这些规格与市场数据本身，
> **在无法核验的前提下撰写等同于编造**，因此暂不撰写。
> 其中与架构取舍有关的结构性内容将并入第 07 篇（推理 ASIC 的架构取舍）。

## 写作要求

1. **器件**：GPU、NPU、TPU、custom ASIC、dataflow、systolic array、tensor core、matrix engine、SIMD/SIMT、vector、SRAM、HBM、DRAM、cache、memory controller、interconnect、NIC、DPU、host CPU
2. **必须解释**：compute、HBM capacity、HBM bandwidth、memory wall、low precision、GPU partitioning、server node、scale-up domain、power、cooling、software ecosystem、supply constraints
3. **必须覆盖**：hyperscaler custom silicon、low-latency accelerator、wafer-scale、reconfigurable、memory-centric、edge NPU；analog/photonic **仅基于可靠资料**
4. **Memory**：HBM、DDR、GDDR、SRAM、cache hierarchy、KV cache 占用、weight streaming、paging、offload、HBM supply、CoWoS/2.5D/3D packaging、chiplet、UCIe、memory bandwidth bottleneck
5. **Server**：1/2/4/8 加速器节点、CPU、PCIe、NVLink/NVSwitch、NIC、storage、rack、power shelf、liquid cooling、BMC、RAS、serviceability
6. **口径纪律**：所有规格必须标注来源与披露等级；峰值与实测分列；训练与推理分列；功耗必须注明 chip/board/server/rack 级别；精度必须显式标注

## 完成标准

- [x] 全部**可撰写的**规划文档已完成（8/8；另 5 篇受阻，见上）
- [ ] 第 08–12 篇：**受阻**，内容本体为需核验的厂商规格与供应链数据
- [x] 模块正文合计 ≥ 18,000 字
- [x] 写作要求第 1、2、4、5、6 条中与架构原理有关的部分已覆盖
- [ ] 写作要求第 3 条的**具名厂商芯片**（hyperscaler 自研、wafer-scale、可重构等）**未覆盖**——即受阻的第 08–10 篇；架构范式的结构性取舍已并入第 07 篇
- [ ] 写作要求第 4 条的**封装与供应**（CoWoS/2.5D/3D、chiplet、UCIe、HBM supply）**未覆盖**——即受阻的第 11–12 篇
- [x] 所有事实性数字带来源链接与披露标签
- [x] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md) 第 18 节
- [ ] 相关 [`data/`](../../data/) CSV 已更新——**受阻**，硬件规格无法核验
- [x] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [x] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
