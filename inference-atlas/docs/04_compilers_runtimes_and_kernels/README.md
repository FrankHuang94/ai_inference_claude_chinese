# 模块 04 — Compiler、Runtime、Kernel 与量化

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**待开始**
> 模块目标字数：**≥ 15,000 字**
> 最后更新：2026-07-29

## 模块定位

本模块解释**从模型图到 GPU 指令之间发生了什么**。上层调度决定了做多少工作，本层决定每一份工作的单价。算子融合、kernel 选择、launch overhead 与数值精度，共同决定了同一硬件上可实现性能与理论峰值之间的差距。

## 前置阅读

[模块 02](../02_transformer_and_kv_cache/)

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | `01_inference_software_stack.md` | framework → IR → compiler → runtime → kernel → driver 全栈 | 待开始 |
| 02 | `02_graph_compilers_and_ir.md` | 图捕获、IR 设计与图优化 | 待开始 |
| 03 | `03_tensorrt_llm.md` | TensorRT-LLM 的架构、优化与适用边界 | 待开始 |
| 04 | `04_torch_compile_inductor_and_triton.md` | TorchDynamo/Inductor/Triton 的推理路径 | 待开始 |
| 05 | `05_xla_jax_and_tpu_runtime.md` | XLA/JAX 与 TPU runtime | 待开始 |
| 06 | `06_onnx_runtime_openvino_and_portability.md` | 跨硬件可移植性与代价 | 待开始 |
| 07 | `07_kernel_fusion_and_operator_optimization.md` | 算子融合与 kernel 优化基本功 | 待开始 |
| 08 | `08_flashattention_and_memory_efficient_attention.md` | IO-aware attention 与显存/带宽优化 | 待开始 |
| 09 | `09_quantization_kernels.md` | 量化 GEMM 与低精度 kernel 实现 | 待开始 |
| 10 | `10_cuda_graphs_and_execution_overhead.md` | launch overhead 与 CUDA Graphs | 待开始 |
| 11 | `11_compiler_debugging_and_profiling.md` | 编译与 kernel 层的调试与 profiling | 待开始 |

## 写作要求

1. **栈**：framework、graph capture、IR、compiler、runtime、kernel、driver、profiler、deployment orchestration；TorchDynamo、TorchInductor、Triton、TensorRT、TensorRT-LLM、XLA、JAX、ONNX Runtime、OpenVINO、TVM、MLIR；graph optimization、operator fusion、autotuning、memory planning、CUDA Graphs
2. **kernel 概念**：GEMM、GEMV、tensor core、warp、block、shared memory、register pressure、occupancy、memory coalescing、launch overhead、fused RMSNorm、fused RoPE、fused attention、fused MLP、sampling kernel、top-k/top-p、quantized GEMM
3. **量化**：FP32、TF32、BF16、FP16、FP8、FP4、INT8、INT4；weight-only、activation quantization、KV cache quantization；per-tensor、per-channel、per-group；calibration、outlier；SmoothQuant、GPTQ、AWQ；quality regression、mixed precision、hardware support
4. **必须明确区分**：training precision vs inference precision；理论峰值 vs 实测性能；显存降低 vs 质量退化

## 完成标准

- [ ] 全部规划文档已按 [`templates/chapter_template.md`](../../templates/chapter_template.md) 完成
- [ ] 模块正文合计 ≥ 15,000 字
- [ ] 上述"写作要求"逐条覆盖
- [ ] 所有事实性数字带来源链接与披露标签
- [ ] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md)
- [ ] 相关 [`data/`](../../data/) CSV 已更新
- [ ] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [ ] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
