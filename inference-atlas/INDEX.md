# INDEX — InferenceAtlas 全库导航

> 本文件是 InferenceAtlas 的**唯一入口**。
> 信息截至：2026-08-10 ｜ 最后更新：2026-08-10 ｜ 版本：v0.1.0

**链接约定**：已完成的文档以链接形式给出；`待开始` 与 `受阻` 的文档以 `代码体` 给出文件名（尚未创建，避免死链）。模块目录始终可点击。

**状态图例**：`已完成` ｜ `已完成*`（可撰写部分已完成，余下受阻） ｜ `进行中` ｜ `待开始`

**关于 `受阻`**：部分文档的内容本体即是需核验的外部资料（厂商规格、标准文本、论文、公司披露）。
当前网络出口策略下本库无法访问这些来源（见 [AGENTS.md 第 11 节](AGENTS.md)），
**在无法核验的前提下撰写等同于编造**，因此这些文档暂不撰写，并在各模块 README 中逐篇标注原因。
**受阻不是待推进的工作量**。

---

## 0. 模块状态总览

| # | 模块 | 状态 | 字数 | 表格 | 图示 | 最后更新 |
|---|---|---|---:|---:|---:|---|
| 00 | [入门与端到端总览](docs/00_start_here/) | 已完成 | 21,824 | 64 | 3 | 2026-08-10 |
| 01 | [基础、指标、排队论与成本](docs/01_foundations_and_metrics/) | 已完成 | 26,531 | 91 | 8 | 2026-08-10 |
| 02 | [Transformer 推理与 KV Cache](docs/02_transformer_and_kv_cache/) | 已完成 | 30,961 | 110 | 10 | 2026-08-10 |
| 03 | [Serving Engines、调度与 QoS](docs/03_serving_engines_and_scheduling/) | 已完成 | 38,095 | 133 | 11 | 2026-08-10 |
| 04 | [Compiler、Runtime、Kernel 与量化](docs/04_compilers_runtimes_and_kernels/) | 已完成 | 37,186 | 138 | 11 | 2026-08-10 |
| 05 | [解码、Speculative 与 Reasoning 推理](docs/05_decoding_and_generation_algorithms/) | 已完成 | 69,325 | 162 | 25 | 2026-08-10 |
| 06 | [分布式、MoE 与 Disaggregated Inference](docs/06_distributed_and_moe_inference/) | 已完成 | 85,544 | 202 | 27 | 2026-08-10 |
| 07 | [硬件、HBM、封装与服务器](docs/07_hardware_and_server_architecture/) | 已完成* | 46,763 | 177 | 12 | 2026-08-10 |
| 08 | [网络、互连与光学](docs/08_networking_and_interconnect/) | 已完成* | 39,947 | 156 | 13 | 2026-08-10 |
| 09 | [数据中心、电力、散热与运维](docs/09_datacenter_power_thermal_and_operations/) | 已完成 | 53,456 | 141 | 10 | 2026-08-10 |
| 10 | [Edge 与 On-Device Inference](docs/10_edge_and_on_device_inference/) | 已完成* | 47,932 | 129 | 11 | 2026-08-10 |
| 11 | [Benchmark、可靠性、可观测性与安全](docs/11_benchmarking_reliability_and_observability/) | 已完成 | 58,453 | 159 | 11 | 2026-08-10 |
| 12 | [开源部署、复现与参考架构](docs/12_open_source_deployment_and_reproduction/) | 已完成 | 56,607 | 246 | 12 | 2026-08-10 |
| 13 | [论文与技术报告地图](docs/13_research_papers_and_technical_reports/) | 已完成 | 78,943 | 131 | 11 | 2026-08-10 |
| 14 | [公司与生态](docs/14_company_and_ecosystem_landscape/) | 待开始 | 0 | 0 | 0 | — |
| 15 | [市场、经济学与战略](docs/15_market_economics_and_strategy/) | 待开始 | 0 | 0 | 0 | — |
| 16 | [未来路线](docs/16_research_frontiers/) | 待开始 | 0 | 0 | 0 | — |
| 17 | [面试准备](docs/17_interview_prep/) | 已完成 | 180,274 | 160 | 12 | 2026-08-10 |
| — | **合计** | — | **871,841** | **2199** | **187** | 2026-08-10 |

> **`已完成*`**：可撰写的规划文档已全部完成，
> 余下文档因其内容本体为需核验的外部资料、在当前网络出口策略下无法撰写而**受阻**
> （见 [AGENTS.md 第 11 节](AGENTS.md)）。
> 受阻文档在各模块 README 的规划表中逐篇标注了原因。
> **这与「进行中」不同**：受阻不是待推进的工作量。

---

## 1. 完整目录

### [00 — 入门与端到端总览](docs/00_start_here/) `已完成`

| 文档 | 一句话说明 |
|---|---|
| [00_database_guide.md](docs/00_start_here/00_database_guide.md) | 如何使用本数据库：结构、约定、披露等级与检索路径 |
| [01_executive_summary.md](docs/00_start_here/01_executive_summary.md) | AI 推理全景的一页式摘要：技术栈、瓶颈与产业格局 |
| [02_end_to_end_inference_lifecycle.md](docs/00_start_here/02_end_to_end_inference_lifecycle.md) | 从用户请求到 token 返回的完整路径与各层责任 |
| [03_how_to_read_inference_benchmarks.md](docs/00_start_here/03_how_to_read_inference_benchmarks.md) | 如何判断一份推理 benchmark 是否可比、可复现、可采信 |
| [04_how_to_design_an_inference_system.md](docs/00_start_here/04_how_to_design_an_inference_system.md) | 推理系统设计的通用方法论与决策顺序 |
| [05_how_to_prepare_for_inference_interviews.md](docs/00_start_here/05_how_to_prepare_for_inference_interviews.md) | 推理相关岗位的能力地图与准备策略 |
| [06_metrics_units_and_quick_reference.md](docs/00_start_here/06_metrics_units_and_quick_reference.md) | 全库指标、单位与口径速查表 |

### [01 — 基础、指标、排队论与成本](docs/01_foundations_and_metrics/) `已完成`

| 文档 | 一句话说明 |
|---|---|
| [01_inference_workload_taxonomy.md](docs/01_foundations_and_metrics/01_inference_workload_taxonomy.md) | 交互式、长上下文、RAG、reasoning、批量与 agent workload 的分类与特征 |
| [02_latency_throughput_and_slo.md](docs/01_foundations_and_metrics/02_latency_throughput_and_slo.md) | TTFT/TPOT/ITL/端到端时延、吞吐与 SLO 的定义与测量口径 |
| [03_queueing_theory_for_inference.md](docs/01_foundations_and_metrics/03_queueing_theory_for_inference.md) | Little's Law、M/M/1、M/M/c 与 tail latency 放大 |
| [04_roofline_and_performance_modeling.md](docs/01_foundations_and_metrics/04_roofline_and_performance_modeling.md) | Roofline 模型与推理阶段的 compute/memory bound 判定 |
| [05_memory_bandwidth_and_arithmetic_intensity.md](docs/01_foundations_and_metrics/05_memory_bandwidth_and_arithmetic_intensity.md) | 算术强度、带宽墙与 decode 阶段的内存受限本质 |
| [06_cost_modeling_and_unit_economics.md](docs/01_foundations_and_metrics/06_cost_modeling_and_unit_economics.md) | cost/token 模型、假设边界与避免伪精确 |
| [07_energy_efficiency_and_joules_per_token.md](docs/01_foundations_and_metrics/07_energy_efficiency_and_joules_per_token.md) | J/token、功耗测量口径与能效优化路径 |
| [08_capacity_planning.md](docs/01_foundations_and_metrics/08_capacity_planning.md) | 容量规划：负载预测、余量、突发与预留 |
| [09_inference_metrics_cheat_sheet.md](docs/01_foundations_and_metrics/09_inference_metrics_cheat_sheet.md) | 指标速查卡 |

### [02 — Transformer 推理与 KV Cache](docs/02_transformer_and_kv_cache/) `已完成`

| 文档 | 一句话说明 |
|---|---|
| [01_transformer_inference_from_first_principles.md](docs/02_transformer_and_kv_cache/01_transformer_inference_from_first_principles.md) | 从 tensor shape 出发重建一次 forward pass |
| [02_prefill_vs_decode.md](docs/02_transformer_and_kv_cache/02_prefill_vs_decode.md) | 两个阶段的计算特征、资源画像与调度含义 |
| [03_attention_complexity_during_inference.md](docs/02_transformer_and_kv_cache/03_attention_complexity_during_inference.md) | 推理期 attention 的复杂度与长序列代价 |
| [04_kv_cache_fundamentals.md](docs/02_transformer_and_kv_cache/04_kv_cache_fundamentals.md) | KV cache 的必要性、结构与生命周期 |
| [05_kv_cache_capacity_and_memory_models.md](docs/02_transformer_and_kv_cache/05_kv_cache_capacity_and_memory_models.md) | KV 容量公式、教学案例与真实实现的偏差来源 |
| [06_gqa_mqa_mla_and_kv_reduction.md](docs/02_transformer_and_kv_cache/06_gqa_mqa_mla_and_kv_reduction.md) | MHA/MQA/GQA/MLA 对 KV 体积与质量的影响 |
| [07_long_context_inference.md](docs/02_transformer_and_kv_cache/07_long_context_inference.md) | 长上下文的时延、显存与质量三重压力 |
| [08_kv_cache_compression_quantization_and_eviction.md](docs/02_transformer_and_kv_cache/08_kv_cache_compression_quantization_and_eviction.md) | KV 压缩、量化、驱逐与 offload 策略 |
| [09_multimodal_inference.md](docs/02_transformer_and_kv_cache/09_multimodal_inference.md) | 图像/视频/语音输入对 prefill 与 cache 的影响 |
| [10_reasoning_workloads_and_test_time_compute.md](docs/02_transformer_and_kv_cache/10_reasoning_workloads_and_test_time_compute.md) | reasoning 模型的长输出与 test-time compute 特征 |

### [03 — Serving Engines、调度与 QoS](docs/03_serving_engines_and_scheduling/) `已完成`

| 文档 | 一句话说明 |
|---|---|
| [01_serving_architecture_overview.md](docs/03_serving_engines_and_scheduling/01_serving_architecture_overview.md) | 从 gateway 到 worker 的 serving 架构全貌 |
| [02_static_dynamic_and_continuous_batching.md](docs/03_serving_engines_and_scheduling/02_static_dynamic_and_continuous_batching.md) | 三种 batching 的机制、收益与 tail latency 代价 |
| [03_pagedattention_and_kv_memory_management.md](docs/03_serving_engines_and_scheduling/03_pagedattention_and_kv_memory_management.md) | 分页式 KV 内存管理与碎片消除 |
| [04_request_scheduling_and_admission_control.md](docs/03_serving_engines_and_scheduling/04_request_scheduling_and_admission_control.md) | 调度策略、准入控制与 backpressure |
| [05_prefill_decode_scheduling.md](docs/03_serving_engines_and_scheduling/05_prefill_decode_scheduling.md) | chunked prefill 与 prefill/decode 干扰治理 |
| [06_multi_tenant_isolation_and_qos.md](docs/03_serving_engines_and_scheduling/06_multi_tenant_isolation_and_qos.md) | 多租户隔离、公平性与 QoS 分层 |
| [07_model_routing_and_cascade_systems.md](docs/03_serving_engines_and_scheduling/07_model_routing_and_cascade_systems.md) | 模型路由与级联：质量/成本自适应 |
| [08_prompt_caching_and_prefix_caching.md](docs/03_serving_engines_and_scheduling/08_prompt_caching_and_prefix_caching.md) | 前缀缓存的命中率、收益与隐私边界 |
| [09_session_memory_and_conversation_state.md](docs/03_serving_engines_and_scheduling/09_session_memory_and_conversation_state.md) | 会话状态与多轮对话的缓存复用 |
| [10_autoscaling_and_load_balancing.md](docs/03_serving_engines_and_scheduling/10_autoscaling_and_load_balancing.md) | 自动扩缩容、warm pool 与冷启动 |
| [11_serverless_and_burst_inference.md](docs/03_serving_engines_and_scheduling/11_serverless_and_burst_inference.md) | serverless 与突发容量的适用边界 |
| [12_serving_incident_playbook.md](docs/03_serving_engines_and_scheduling/12_serving_incident_playbook.md) | 线上事故分级、排查与降级手册 |

### [04 — Compiler、Runtime、Kernel 与量化](docs/04_compilers_runtimes_and_kernels/) `已完成`

| 文档 | 一句话说明 |
|---|---|
| [01_inference_software_stack.md](docs/04_compilers_runtimes_and_kernels/01_inference_software_stack.md) | framework → IR → compiler → runtime → kernel → driver 全栈 |
| [02_graph_compilers_and_ir.md](docs/04_compilers_runtimes_and_kernels/02_graph_compilers_and_ir.md) | 图捕获、IR 设计与图优化 |
| [03_tensorrt_llm.md](docs/04_compilers_runtimes_and_kernels/03_tensorrt_llm.md) | TensorRT-LLM 的架构、优化与适用边界 |
| [04_torch_compile_inductor_and_triton.md](docs/04_compilers_runtimes_and_kernels/04_torch_compile_inductor_and_triton.md) | TorchDynamo/Inductor/Triton 的推理路径 |
| [05_xla_jax_and_tpu_runtime.md](docs/04_compilers_runtimes_and_kernels/05_xla_jax_and_tpu_runtime.md) | XLA/JAX 与 TPU runtime |
| [06_onnx_runtime_openvino_and_portability.md](docs/04_compilers_runtimes_and_kernels/06_onnx_runtime_openvino_and_portability.md) | 跨硬件可移植性与代价 |
| [07_kernel_fusion_and_operator_optimization.md](docs/04_compilers_runtimes_and_kernels/07_kernel_fusion_and_operator_optimization.md) | 算子融合与 kernel 优化基本功 |
| [08_flashattention_and_memory_efficient_attention.md](docs/04_compilers_runtimes_and_kernels/08_flashattention_and_memory_efficient_attention.md) | IO-aware attention 与显存/带宽优化 |
| [09_quantization_kernels.md](docs/04_compilers_runtimes_and_kernels/09_quantization_kernels.md) | 量化 GEMM 与低精度 kernel 实现 |
| [10_cuda_graphs_and_execution_overhead.md](docs/04_compilers_runtimes_and_kernels/10_cuda_graphs_and_execution_overhead.md) | launch overhead 与 CUDA Graphs |
| [11_compiler_debugging_and_profiling.md](docs/04_compilers_runtimes_and_kernels/11_compiler_debugging_and_profiling.md) | 编译与 kernel 层的调试与 profiling |

### [05 — 解码、Speculative 与 Reasoning 推理](docs/05_decoding_and_generation_algorithms/) `已完成`

| 文档 | 一句话说明 |
|---|---|
| [01_decoding_basics.md](docs/05_decoding_and_generation_algorithms/01_decoding_basics.md) | 自回归解码循环与采样接口 |
| [02_greedy_sampling_topk_topp_temperature.md](docs/05_decoding_and_generation_algorithms/02_greedy_sampling_topk_topp_temperature.md) | 采样参数对质量、时延与可复现性的影响 |
| [03_beam_search_and_constrained_decoding.md](docs/05_decoding_and_generation_algorithms/03_beam_search_and_constrained_decoding.md) | beam search 与约束解码的推理代价 |
| [04_speculative_decoding.md](docs/05_decoding_and_generation_algorithms/04_speculative_decoding.md) | draft/verify 机制、接受率与真实收益判定 |
| [05_medusa_eagle_and_multi_token_prediction.md](docs/05_decoding_and_generation_algorithms/05_medusa_eagle_and_multi_token_prediction.md) | 多头/树形投机与多 token 预测 |
| [06_draft_model_selection_and_acceptance_rate.md](docs/05_decoding_and_generation_algorithms/06_draft_model_selection_and_acceptance_rate.md) | draft 模型选型与接受率工程 |
| [07_reasoning_inference_and_test_time_scaling.md](docs/05_decoding_and_generation_algorithms/07_reasoning_inference_and_test_time_scaling.md) | test-time compute 的质量-成本曲线 |
| [08_tool_use_and_agent_inference.md](docs/05_decoding_and_generation_algorithms/08_tool_use_and_agent_inference.md) | 工具调用与 agent 循环的推理特征 |
| [09_structured_output_and_grammar_constrained_decoding.md](docs/05_decoding_and_generation_algorithms/09_structured_output_and_grammar_constrained_decoding.md) | JSON mode 与语法约束解码 |
| [10_generation_quality_latency_tradeoffs.md](docs/05_decoding_and_generation_algorithms/10_generation_quality_latency_tradeoffs.md) | 生成质量与时延的系统级权衡 |

### [06 — 分布式、MoE 与 Disaggregated Inference](docs/06_distributed_and_moe_inference/) `已完成`

| 文档 | 一句话说明 |
|---|---|
| [01_distributed_inference_overview.md](docs/06_distributed_and_moe_inference/01_distributed_inference_overview.md) | 何时需要分布式推理及其代价 |
| [02_tensor_parallel_inference.md](docs/06_distributed_and_moe_inference/02_tensor_parallel_inference.md) | TP 的通信模式与时延影响 |
| [03_pipeline_parallel_inference.md](docs/06_distributed_and_moe_inference/03_pipeline_parallel_inference.md) | PP 的气泡、微批与推理适配性 |
| [04_sequence_context_parallel_inference.md](docs/06_distributed_and_moe_inference/04_sequence_context_parallel_inference.md) | 长上下文的序列/上下文并行 |
| [05_moe_inference_and_expert_parallelism.md](docs/06_distributed_and_moe_inference/05_moe_inference_and_expert_parallelism.md) | MoE 推理与专家并行 |
| [06_moe_routing_all_to_all_and_load_balancing.md](docs/06_distributed_and_moe_inference/06_moe_routing_all_to_all_and_load_balancing.md) | all-to-all、token 倾斜与热专家治理 |
| [07_prefill_decode_disaggregation.md](docs/06_distributed_and_moe_inference/07_prefill_decode_disaggregation.md) | prefill/decode 池分离的收益与边界 |
| [08_kv_cache_transfer_and_remote_memory.md](docs/06_distributed_and_moe_inference/08_kv_cache_transfer_and_remote_memory.md) | KV 迁移、RDMA 与远端内存 |
| [09_multi_node_serving_topologies.md](docs/06_distributed_and_moe_inference/09_multi_node_serving_topologies.md) | 多节点部署拓扑与放置策略 |
| [10_fault_tolerance_and_graceful_degradation.md](docs/06_distributed_and_moe_inference/10_fault_tolerance_and_graceful_degradation.md) | 故障域、容错与优雅降级 |
| [11_distributed_serving_case_studies.md](docs/06_distributed_and_moe_inference/11_distributed_serving_case_studies.md) | 公开分布式推理案例研究 |

### [07 — 硬件、HBM、封装与服务器](docs/07_hardware_and_server_architecture/) `已完成*`

| 文档 | 一句话说明 |
|---|---|
| [01_ai_inference_hardware_overview.md](docs/07_hardware_and_server_architecture/01_ai_inference_hardware_overview.md) | 推理硬件全景与分类 |
| [02_gpu_architecture_for_inference.md](docs/07_hardware_and_server_architecture/02_gpu_architecture_for_inference.md) | GPU 微架构中与推理相关的部分 |
| [03_tensor_cores_matrix_engines_and_low_precision.md](docs/07_hardware_and_server_architecture/03_tensor_cores_matrix_engines_and_low_precision.md) | 矩阵引擎与低精度算力 |
| [04_hbm_dram_and_memory_hierarchy.md](docs/07_hardware_and_server_architecture/04_hbm_dram_and_memory_hierarchy.md) | HBM/DRAM/SRAM 层次与带宽 |
| [05_memory_capacity_bandwidth_and_kv_cache.md](docs/07_hardware_and_server_architecture/05_memory_capacity_bandwidth_and_kv_cache.md) | 显存容量/带宽如何约束 KV cache 与并发 |
| [06_gpu_server_node_architecture.md](docs/07_hardware_and_server_architecture/06_gpu_server_node_architecture.md) | 服务器节点：CPU、PCIe、NVLink、NIC、存储 |
| [07_inference_asic_architectures.md](docs/07_hardware_and_server_architecture/07_inference_asic_architectures.md) | 推理 ASIC 的架构取舍 |
| `08_nvidia_amd_intel_and_custom_accelerators.md` | 主流商用加速器对比 |
| `09_google_tpu_aws_inferentia_trainium_and_maia.md` | 超大规模厂商自研芯片 |
| `10_groq_cerebras_sambanova_dmatrix_etched_tenstorrent.md` | 推理初创公司的架构路线 |
| `11_advanced_packaging_chiplets_and_ucie.md` | 先进封装、chiplet 与 UCIe |
| `12_hbm_supply_chain_and_memory_roadmaps.md` | HBM 供应链与内存路线图 |
| [13_hardware_selection_framework.md](docs/07_hardware_and_server_architecture/13_hardware_selection_framework.md) | 面向 workload 的硬件选型框架 |

### [08 — 网络、互连与光学](docs/08_networking_and_interconnect/) `已完成*`

| 文档 | 一句话说明 |
|---|---|
| [01_inference_networking_overview.md](docs/08_networking_and_interconnect/01_inference_networking_overview.md) | 从 die-to-die 到跨数据中心的互连层次 |
| `02_pcie_cxl_nvlink_nvswitch.md` | 节点内与 scale-up 互连 |
| `03_infiniband_for_ai_inference.md` | InfiniBand 在推理集群中的角色 |
| `04_ethernet_roce_and_ultra_ethernet.md` | 以太网、RoCE 与 Ultra Ethernet |
| [05_collectives_rdma_and_communication_libraries.md](docs/08_networking_and_interconnect/05_collectives_rdma_and_communication_libraries.md) | 集合通信、RDMA 与通信库 |
| [06_scale_up_vs_scale_out.md](docs/08_networking_and_interconnect/06_scale_up_vs_scale_out.md) | scale-up 与 scale-out 的决策框架 |
| [07_network_topologies_fat_tree_dragonfly_rail_optimized.md](docs/08_networking_and_interconnect/07_network_topologies_fat_tree_dragonfly_rail_optimized.md) | 拓扑设计与 rail 优化 |
| `08_optical_transceivers_aec_dac_and_cpo.md` | DAC/AEC/可插拔光模块与 CPO |
| `09_optical_switching_and_photonic_interconnect.md` | 光交换与光子互连 |
| [10_network_congestion_tail_latency_and_qos.md](docs/08_networking_and_interconnect/10_network_congestion_tail_latency_and_qos.md) | 拥塞控制、incast 与 tail latency |
| [11_network_observability_and_debugging.md](docs/08_networking_and_interconnect/11_network_observability_and_debugging.md) | 网络可观测性与排查 |
| [12_inference_network_case_studies.md](docs/08_networking_and_interconnect/12_inference_network_case_studies.md) | 公开推理网络案例 |

### [09 — 数据中心、电力、散热与运维](docs/09_datacenter_power_thermal_and_operations/) `已完成`

| 文档 | 一句话说明 |
|---|---|
| [01_ai_datacenter_overview.md](docs/09_datacenter_power_thermal_and_operations/01_ai_datacenter_overview.md) | AI 数据中心与传统数据中心的差异 |
| [02_rack_power_and_density.md](docs/09_datacenter_power_thermal_and_operations/02_rack_power_and_density.md) | 机架功率密度与扩容速度 |
| [03_power_delivery_48v_and_busbar.md](docs/09_datacenter_power_thermal_and_operations/03_power_delivery_48v_and_busbar.md) | 48V 供电、busbar 与配电链路 |
| [04_cooling_air_direct_liquid_and_immersion.md](docs/09_datacenter_power_thermal_and_operations/04_cooling_air_direct_liquid_and_immersion.md) | 风冷、冷板液冷与浸没式散热 |
| [05_power_usage_effectiveness_and_energy_modeling.md](docs/09_datacenter_power_thermal_and_operations/05_power_usage_effectiveness_and_energy_modeling.md) | PUE/WUE 与能耗建模 |
| [06_cluster_capacity_and_site_planning.md](docs/09_datacenter_power_thermal_and_operations/06_cluster_capacity_and_site_planning.md) | 集群容量与选址规划 |
| [07_reliability_redundancy_and_maintenance.md](docs/09_datacenter_power_thermal_and_operations/07_reliability_redundancy_and_maintenance.md) | 冗余、可维护性与 RAS |
| [08_storage_logging_and_data_plane.md](docs/09_datacenter_power_thermal_and_operations/08_storage_logging_and_data_plane.md) | 存储、日志与数据面 |
| [09_security_compliance_and_data_residency.md](docs/09_datacenter_power_thermal_and_operations/09_security_compliance_and_data_residency.md) | 安全、合规与数据驻留 |
| [10_operations_case_studies.md](docs/09_datacenter_power_thermal_and_operations/10_operations_case_studies.md) | 运维案例研究 |

### [10 — Edge 与 On-Device Inference](docs/10_edge_and_on_device_inference/) `已完成*`

| 文档 | 一句话说明 |
|---|---|
| [01_edge_inference_overview.md](docs/10_edge_and_on_device_inference/01_edge_inference_overview.md) | 边缘推理的约束条件与价值主张 |
| [02_mobile_npu_soc_and_memory_constraints.md](docs/10_edge_and_on_device_inference/02_mobile_npu_soc_and_memory_constraints.md) | 移动 SoC、NPU 与 LPDDR 约束 |
| `03_qualcomm_apple_mediatek_google_samsung_platforms.md` | 主要移动平台的端侧推理能力 |
| [04_pc_ai_inference.md](docs/10_edge_and_on_device_inference/04_pc_ai_inference.md) | AI PC 的推理路径 |
| [05_automotive_robotics_and_embedded_inference.md](docs/10_edge_and_on_device_inference/05_automotive_robotics_and_embedded_inference.md) | 车载、机器人与嵌入式推理 |
| [06_small_language_models_and_on_device_agents.md](docs/10_edge_and_on_device_inference/06_small_language_models_and_on_device_agents.md) | 小模型与端侧 agent |
| [07_quantization_distillation_and_pruning_for_edge.md](docs/10_edge_and_on_device_inference/07_quantization_distillation_and_pruning_for_edge.md) | 面向端侧的模型压缩 |
| [08_private_hybrid_cloud_edge_architectures.md](docs/10_edge_and_on_device_inference/08_private_hybrid_cloud_edge_architectures.md) | 云-边混合与隐私优先架构 |
| [09_edge_deployment_case_studies.md](docs/10_edge_and_on_device_inference/09_edge_deployment_case_studies.md) | 端侧部署案例 |

### [11 — Benchmark、可靠性、可观测性与安全](docs/11_benchmarking_reliability_and_observability/) `已完成`

| 文档 | 一句话说明 |
|---|---|
| [01_inference_benchmarking_methodology.md](docs/11_benchmarking_reliability_and_observability/01_inference_benchmarking_methodology.md) | 严谨推理 benchmark 的设计方法论 |
| [02_mlperf_inference.md](docs/11_benchmarking_reliability_and_observability/02_mlperf_inference.md) | MLPerf Inference 能回答与不能回答的问题 |
| [03_ttft_tpot_itl_and_end_to_end_latency.md](docs/11_benchmarking_reliability_and_observability/03_ttft_tpot_itl_and_end_to_end_latency.md) | 时延指标的精确定义与测量陷阱 |
| [04_throughput_concurrency_and_goodput.md](docs/11_benchmarking_reliability_and_observability/04_throughput_concurrency_and_goodput.md) | 吞吐、并发与 goodput |
| [05_power_energy_and_cost_benchmarks.md](docs/11_benchmarking_reliability_and_observability/05_power_energy_and_cost_benchmarks.md) | 功耗、能耗与成本基准 |
| [06_profiling_gpu_cpu_network_and_memory.md](docs/11_benchmarking_reliability_and_observability/06_profiling_gpu_cpu_network_and_memory.md) | 全栈 profiling 方法 |
| [07_observability_metrics_logs_traces.md](docs/11_benchmarking_reliability_and_observability/07_observability_metrics_logs_traces.md) | 指标、日志与 trace 体系 |
| [08_slos_slas_and_error_budgets.md](docs/11_benchmarking_reliability_and_observability/08_slos_slas_and_error_budgets.md) | SLO/SLA 与错误预算 |
| [09_reliability_incidents_and_capacity_failures.md](docs/11_benchmarking_reliability_and_observability/09_reliability_incidents_and_capacity_failures.md) | 可靠性事故与容量失效模式 |
| [10_safety_security_and_abuse_controls.md](docs/11_benchmarking_reliability_and_observability/10_safety_security_and_abuse_controls.md) | 安全、滥用防护与租户隔离 |
| [11_benchmark_case_studies.md](docs/11_benchmarking_reliability_and_observability/11_benchmark_case_studies.md) | benchmark 案例研究 |

### [12 — 开源部署、复现与参考架构](docs/12_open_source_deployment_and_reproduction/) `已完成`

| 文档 | 一句话说明 |
|---|---|
| [01_open_source_inference_ecosystem.md](docs/12_open_source_deployment_and_reproduction/01_open_source_inference_ecosystem.md) | 开源推理生态全景 |
| [02_vllm.md](docs/12_open_source_deployment_and_reproduction/02_vllm.md) | vLLM 架构、优化与适用边界 |
| [03_sglang.md](docs/12_open_source_deployment_and_reproduction/03_sglang.md) | SGLang 架构与结构化生成 |
| [04_tgi.md](docs/12_open_source_deployment_and_reproduction/04_tgi.md) | Hugging Face TGI |
| [05_tensorrt_llm_deployment.md](docs/12_open_source_deployment_and_reproduction/05_tensorrt_llm_deployment.md) | TensorRT-LLM 部署实践 |
| [06_deepspeed_fastgen.md](docs/12_open_source_deployment_and_reproduction/06_deepspeed_fastgen.md) | DeepSpeed-FastGen |
| [07_llama_cpp_mlx_ollama_and_local_serving.md](docs/12_open_source_deployment_and_reproduction/07_llama_cpp_mlx_ollama_and_local_serving.md) | 本地与端侧 serving |
| [08_ray_serve_kubernetes_kserve_and_triton.md](docs/12_open_source_deployment_and_reproduction/08_ray_serve_kubernetes_kserve_and_triton.md) | 编排层与推理服务器 |
| [09_litellm_gateways_and_model_routing.md](docs/12_open_source_deployment_and_reproduction/09_litellm_gateways_and_model_routing.md) | 网关与多模型路由 |
| [10_observability_stack.md](docs/12_open_source_deployment_and_reproduction/10_observability_stack.md) | Prometheus/Grafana/OpenTelemetry 观测栈 |
| [11_reference_architectures.md](docs/12_open_source_deployment_and_reproduction/11_reference_architectures.md) | 10 个教学性参考架构 |
| [12_reproduction_playbooks.md](docs/12_open_source_deployment_and_reproduction/12_reproduction_playbooks.md) | 可复现实验手册 |

### [13 — 论文与技术报告地图](docs/13_research_papers_and_technical_reports/) `已完成`

> **降级书写**：出口策略拒绝一切论文来源，本模块**未读过任何论文正文**。
> 卡片的「实验设置」与「关键结果」一律 `待核实`，机制与适用边界由本库自有推导支撑。
> 详见 [第 01 章的降级声明](docs/13_research_papers_and_technical_reports/01_paper_map.md)。

| 文档 | 一句话说明 |
|---|---|
| [01_paper_map.md](docs/13_research_papers_and_technical_reports/01_paper_map.md) | 论文全景地图与阅读顺序 |
| [02_transformer_inference_and_kv_cache_papers.md](docs/13_research_papers_and_technical_reports/02_transformer_inference_and_kv_cache_papers.md) | Transformer 推理与 KV cache 论文卡片 |
| [03_batching_serving_and_scheduler_papers.md](docs/13_research_papers_and_technical_reports/03_batching_serving_and_scheduler_papers.md) | batching、serving 与调度器论文 |
| [04_speculative_decoding_papers.md](docs/13_research_papers_and_technical_reports/04_speculative_decoding_papers.md) | 投机解码论文 |
| [05_quantization_and_compression_papers.md](docs/13_research_papers_and_technical_reports/05_quantization_and_compression_papers.md) | 量化与压缩论文 |
| [06_compiler_runtime_and_kernel_papers.md](docs/13_research_papers_and_technical_reports/06_compiler_runtime_and_kernel_papers.md) | 编译器、runtime 与 kernel 论文 |
| [07_distributed_and_moe_inference_papers.md](docs/13_research_papers_and_technical_reports/07_distributed_and_moe_inference_papers.md) | 分布式与 MoE 推理论文 |
| [08_hardware_and_architecture_papers.md](docs/13_research_papers_and_technical_reports/08_hardware_and_architecture_papers.md) | 硬件与体系结构论文 |
| [09_networking_and_datacenter_papers.md](docs/13_research_papers_and_technical_reports/09_networking_and_datacenter_papers.md) | 网络与数据中心论文 |
| [10_edge_inference_papers.md](docs/13_research_papers_and_technical_reports/10_edge_inference_papers.md) | 边缘推理论文 |
| [11_reliability_and_benchmarking_papers.md](docs/13_research_papers_and_technical_reports/11_reliability_and_benchmarking_papers.md) | 可靠性与基准测试论文 |
| [12_recent_reading_tracker.md](docs/13_research_papers_and_technical_reports/12_recent_reading_tracker.md) | 近期阅读追踪 |

### [14 — 公司与生态](docs/14_company_and_ecosystem_landscape/) `待开始`

| 文档 | 一句话说明 |
|---|---|
| `01_landscape_overview.md` | 推理产业生态全景 |
| `02_nvidia.md` … `22_broadcom_and_marvell.md` | 21 家重点公司/组织深度档案 |
| `23_cloud_neocloud_and_gpu_service_providers.md` | 云与 neocloud 供应商 |
| `24_inference_software_companies.md` | 推理软件公司 |
| `25_ecosystem_comparison.md` | 生态横向对比 |

> 完整公司清单见模块 README 与 [`data/companies.csv`](data/companies.csv)。

### [15 — 市场、经济学与战略](docs/15_market_economics_and_strategy/) `待开始`

| 文档 | 一句话说明 |
|---|---|
| `01_ai_inference_value_chain.md` | 推理价值链与价值捕获环节 |
| `02_inference_tam_and_workload_growth.md` | 推理 TAM 与工作负载增长 |
| `03_cloud_api_and_enterprise_pricing.md` | API 与企业定价结构 |
| `04_cost_per_token_and_tco.md` | cost/token 与 TCO |
| `05_gpu_asic_and_system_economics.md` | GPU/ASIC 与系统经济性 |
| `06_memory_networking_and_optics_value_capture.md` | 内存、网络与光学的价值捕获 |
| `07_hyperscaler_capex_and_custom_silicon.md` | 超大规模厂商 capex 与自研芯片 |
| `08_neocloud_and_gpu_as_a_service.md` | neocloud 与 GPUaaS |
| `09_open_vs_closed_models_and_margin_structure.md` | 开源与闭源模型的利润结构 |
| `10_company_financials_and_kpis.md` | 公司财务与 KPI |
| `11_mna_funding_and_partnerships.md` | 并购、融资与合作 |
| `12_geopolitics_export_controls_and_supply_chain.md` | 地缘政治、出口管制与供应链 |
| `13_investment_diligence_framework.md` | 投资尽调框架 |
| `14_bull_base_bear_scenarios.md` | 多空情景分析 |

### [16 — 未来路线](docs/16_research_frontiers/) `待开始`

| 文档 | 一句话说明 |
|---|---|
| `01_inference_roadmap_overview.md` | 推理技术路线全景 |
| `02_kv_cache_as_a_system_resource.md` | KV cache 作为一等系统资源 |
| `03_disaggregated_serving_and_memory_fabric.md` | 解耦式服务与内存 fabric |
| `04_next_generation_speculative_decoding.md` | 下一代投机解码 |
| `05_reasoning_test_time_compute_and_cost.md` | reasoning 与 test-time compute 经济学 |
| `06_inference_aware_model_architecture.md` | 面向推理的模型架构设计 |
| `07_moe_at_scale_and_expert_routing.md` | 大规模 MoE 与专家路由 |
| `08_optical_interconnect_and_photonic_compute.md` | 光互连与光子计算 |
| `09_processing_in_memory_and_memory_centric_compute.md` | 存内计算与内存中心架构 |
| `10_compiler_autotuning_and_ai_for_systems.md` | 编译器自动调优与 AI for systems |
| `11_edge_agents_and_private_inference.md` | 端侧 agent 与私有推理 |
| `12_open_questions_and_scenarios.md` | 开放问题与情景推演 |

### [17 — 面试准备](docs/17_interview_prep/) `已完成`

| 文档 | 一句话说明 |
|---|---|
| [01_inference_system_design.md](docs/17_interview_prep/01_inference_system_design.md) | 推理系统设计题与完整参考答案 |
| [02_kv_cache_and_transformer_questions.md](docs/17_interview_prep/02_kv_cache_and_transformer_questions.md) | Transformer 与 KV cache 题组 |
| [03_serving_scheduling_and_slo_questions.md](docs/17_interview_prep/03_serving_scheduling_and_slo_questions.md) | serving、调度与 SLO 题组 |
| [04_compiler_kernel_and_quantization_questions.md](docs/17_interview_prep/04_compiler_kernel_and_quantization_questions.md) | 编译器、kernel 与量化题组 |
| `05_distributed_moe_and_networking_questions.md` | 分布式、MoE 与网络题组 |
| `06_hardware_datacenter_and_edge_questions.md` | 硬件、数据中心与边缘题组 |
| `07_debugging_benchmarking_and_observability_questions.md` | 调试、基准与可观测性题组 |
| `08_company_strategy_and_paper_discussion.md` | 公司战略与论文讨论题组 |
| [09_mock_interview_cases.md](docs/17_interview_prep/09_mock_interview_cases.md) | 模拟面试案例 |
| [10_coding_exercises.md](docs/17_interview_prep/10_coding_exercises.md) | 编码练习 |
| [11_90_day_study_plan.md](docs/17_interview_prep/11_90_day_study_plan.md) | 90 天学习计划 |

> **面试题总数必须恰好 100 道**，分布约束见 [`data/schemas/interview_questions_schema.md`](data/schemas/interview_questions_schema.md)，由 `scripts/interview_coverage_report.py` 强制校验。

---

## 2. 按系统层检索

| 层 | 主要模块 |
|---|---|
| model | [02](docs/02_transformer_and_kv_cache/)、[05](docs/05_decoding_and_generation_algorithms/)、[16](docs/16_research_frontiers/) |
| serving | [03](docs/03_serving_engines_and_scheduling/)、[12](docs/12_open_source_deployment_and_reproduction/) |
| runtime | [04](docs/04_compilers_runtimes_and_kernels/)、[12](docs/12_open_source_deployment_and_reproduction/) |
| compiler | [04](docs/04_compilers_runtimes_and_kernels/) |
| kernel | [04](docs/04_compilers_runtimes_and_kernels/) |
| accelerator | [07](docs/07_hardware_and_server_architecture/) |
| memory | [02](docs/02_transformer_and_kv_cache/)、[07](docs/07_hardware_and_server_architecture/) |
| networking | [08](docs/08_networking_and_interconnect/)、[06](docs/06_distributed_and_moe_inference/) |
| datacenter | [09](docs/09_datacenter_power_thermal_and_operations/) |
| cloud | [12](docs/12_open_source_deployment_and_reproduction/)、[14](docs/14_company_and_ecosystem_landscape/)、[15](docs/15_market_economics_and_strategy/) |
| edge | [10](docs/10_edge_and_on_device_inference/) |
| market | [15](docs/15_market_economics_and_strategy/)、[14](docs/14_company_and_ecosystem_landscape/) |

## 3. 按 workload 检索

| Workload | 主要模块 |
|---|---|
| interactive chat | [01](docs/01_foundations_and_metrics/)、[03](docs/03_serving_engines_and_scheduling/) |
| long context | [02](docs/02_transformer_and_kv_cache/)、[06](docs/06_distributed_and_moe_inference/) |
| RAG | [02](docs/02_transformer_and_kv_cache/)、[03](docs/03_serving_engines_and_scheduling/)、[12](docs/12_open_source_deployment_and_reproduction/) |
| reasoning | [05](docs/05_decoding_and_generation_algorithms/)、[15](docs/15_market_economics_and_strategy/)、[16](docs/16_research_frontiers/) |
| code generation | [05](docs/05_decoding_and_generation_algorithms/)、[03](docs/03_serving_engines_and_scheduling/) |
| multimodal | [02](docs/02_transformer_and_kv_cache/) |
| batch inference | [01](docs/01_foundations_and_metrics/)、[03](docs/03_serving_engines_and_scheduling/) |
| agent | [05](docs/05_decoding_and_generation_algorithms/)、[16](docs/16_research_frontiers/) |
| edge | [10](docs/10_edge_and_on_device_inference/) |

## 4. 按指标检索

| 指标 | 主要模块 |
|---|---|
| TTFT | [01](docs/01_foundations_and_metrics/)、[03](docs/03_serving_engines_and_scheduling/)、[11](docs/11_benchmarking_reliability_and_observability/) |
| TPOT | [01](docs/01_foundations_and_metrics/)、[02](docs/02_transformer_and_kv_cache/)、[11](docs/11_benchmarking_reliability_and_observability/) |
| ITL | [11](docs/11_benchmarking_reliability_and_observability/) |
| throughput | [01](docs/01_foundations_and_metrics/)、[03](docs/03_serving_engines_and_scheduling/) |
| goodput | [11](docs/11_benchmarking_reliability_and_observability/) |
| cost/token | [01](docs/01_foundations_and_metrics/)、[15](docs/15_market_economics_and_strategy/) |
| J/token | [01](docs/01_foundations_and_metrics/)、[09](docs/09_datacenter_power_thermal_and_operations/) |
| availability | [11](docs/11_benchmarking_reliability_and_observability/)、[09](docs/09_datacenter_power_thermal_and_operations/) |
| utilization | [01](docs/01_foundations_and_metrics/)、[03](docs/03_serving_engines_and_scheduling/) |

## 5. 快速路径

| 我想…… | 阅读顺序 |
|---|---|
| 理解 KV Cache | [02](docs/02_transformer_and_kv_cache/) → [07](docs/07_hardware_and_server_architecture/) |
| 设计 LLM serving | [00](docs/00_start_here/) → [01](docs/01_foundations_and_metrics/) → [03](docs/03_serving_engines_and_scheduling/) → [12](docs/12_open_source_deployment_and_reproduction/) |
| 降低 TTFT | [02](docs/02_transformer_and_kv_cache/) → [03](docs/03_serving_engines_and_scheduling/) → [06](docs/06_distributed_and_moe_inference/) |
| 降低 TPOT | [02](docs/02_transformer_and_kv_cache/) → [04](docs/04_compilers_runtimes_and_kernels/) → [05](docs/05_decoding_and_generation_algorithms/) |
| 提高吞吐 | [03](docs/03_serving_engines_and_scheduling/) → [04](docs/04_compilers_runtimes_and_kernels/) |
| 做 MoE serving | [06](docs/06_distributed_and_moe_inference/) → [08](docs/08_networking_and_interconnect/) |
| 设计 prefill/decode 分离 | [06](docs/06_distributed_and_moe_inference/) → [08](docs/08_networking_and_interconnect/) |
| 选择 GPU / ASIC | [07](docs/07_hardware_and_server_architecture/) → [11](docs/11_benchmarking_reliability_and_observability/) → [15](docs/15_market_economics_and_strategy/) |
| 理解 AI 网络与光互连 | [08](docs/08_networking_and_interconnect/) → [09](docs/09_datacenter_power_thermal_and_operations/) |
| 面试 inference system 岗位 | [00](docs/00_start_here/) → [17](docs/17_interview_prep/) |
| 做 AI 基础设施技术尽调 | [14](docs/14_company_and_ecosystem_landscape/) → [15](docs/15_market_economics_and_strategy/) → [16](docs/16_research_frontiers/) |

---

## 6. 近 90 天待复核资料

> 由 `scripts/freshness_report.py` 生成。当前所有 seed 记录核验日期为 2026-07-29，尚无到期项。

| 条目 | 类型 | 最后核验 | 到期 | 优先级 |
|---|---|---|---|---|
| — | — | — | — | — |

---

## 7. 结构化数据入口

| 文件 | 内容 | Schema |
|---|---|---|
| [`data/papers.csv`](data/papers.csv) | 论文与技术报告 | [schema](data/schemas/papers_schema.md) |
| [`data/models.csv`](data/models.csv) | 模型记录 | [schema](data/schemas/models_schema.md) |
| [`data/inference_engines.csv`](data/inference_engines.csv) | 推理引擎 | [schema](data/schemas/inference_engines_schema.md) |
| [`data/accelerators.csv`](data/accelerators.csv) | 加速器 | [schema](data/schemas/accelerators_schema.md) |
| [`data/server_platforms.csv`](data/server_platforms.csv) | 服务器平台 | — |
| [`data/memory_technologies.csv`](data/memory_technologies.csv) | 内存技术 | — |
| [`data/networking_technologies.csv`](data/networking_technologies.csv) | 网络与互连 | — |
| [`data/benchmarks.csv`](data/benchmarks.csv) | benchmark 结果 | [schema](data/schemas/benchmarks_schema.md) |
| [`data/deployment_cases.csv`](data/deployment_cases.csv) | 部署案例 | [schema](data/schemas/deployment_cases_schema.md) |
| [`data/techniques.csv`](data/techniques.csv) | 技术卡片 | [schema](data/schemas/techniques_schema.md) |
| [`data/companies.csv`](data/companies.csv) | 公司与组织 | [schema](data/schemas/companies_schema.md) |
| [`data/company_events.csv`](data/company_events.csv) | 公司事件 | — |
| [`data/cloud_pricing.csv`](data/cloud_pricing.csv) | 云与 API 定价 | — |
| [`data/market_transactions.csv`](data/market_transactions.csv) | 并购与融资 | — |
| [`data/glossary.csv`](data/glossary.csv) | 术语表 | — |
| [`data/interview_questions.csv`](data/interview_questions.csv) | 面试题库 | [schema](data/schemas/interview_questions_schema.md) |
| [`data/references.bib`](data/references.bib) | BibTeX 引用 | — |
