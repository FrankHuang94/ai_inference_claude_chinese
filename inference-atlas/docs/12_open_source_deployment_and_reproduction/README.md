# 模块 12 — 开源部署、复现与参考架构

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**进行中（9/12 篇）**
> 模块目标字数：**≥ 12,000 字**
> 最后更新：2026-08-10

## 模块定位

本模块把前面各模块的原理落到**可以真正跑起来的系统**上。每个项目都必须给出适用与不适用的 workload，而不是罗列特性。参考架构部分提供 10 个教学性蓝图，覆盖从单卡本地部署到 prefill/decode 分离的完整跨度。

## 前置阅读

[模块 03](../03_serving_engines_and_scheduling/)、[模块 04](../04_compilers_runtimes_and_kernels/)

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | [01_open_source_inference_ecosystem.md](01_open_source_inference_ecosystem.md) | 开源推理生态全景 | 已完成 |
| 02 | [02_vllm.md](02_vllm.md) | vLLM 架构、优化与适用边界 | 已完成 |
| 03 | [03_sglang.md](03_sglang.md) | SGLang 架构与结构化生成 | 已完成 |
| 04 | [04_tgi.md](04_tgi.md) | Hugging Face TGI | 已完成 |
| 05 | [05_tensorrt_llm_deployment.md](05_tensorrt_llm_deployment.md) | TensorRT-LLM 部署实践 | 已完成 |
| 06 | [06_deepspeed_fastgen.md](06_deepspeed_fastgen.md) | DeepSpeed-FastGen | 已完成 |
| 07 | [07_llama_cpp_mlx_ollama_and_local_serving.md](07_llama_cpp_mlx_ollama_and_local_serving.md) | 本地与端侧 serving | 已完成 |
| 08 | [08_ray_serve_kubernetes_kserve_and_triton.md](08_ray_serve_kubernetes_kserve_and_triton.md) | 编排层与推理服务器 | 已完成 |
| 09 | [09_litellm_gateways_and_model_routing.md](09_litellm_gateways_and_model_routing.md) | 网关与多模型路由 | 已完成 |
| 10 | `10_observability_stack.md` | Prometheus/Grafana/OpenTelemetry 观测栈 | 待开始 |
| 11 | `11_reference_architectures.md` | 10 个教学性参考架构 | 待开始 |
| 12 | `12_reproduction_playbooks.md` | 可复现实验手册 | 待开始 |

> **本模块的出口策略状态（2026-08-10 复核）**：
> 各项目的**官方文档站点不可达**（`docs.vllm.ai`、`huggingface.co` 等均返回 403），
> **但 GitHub 系可达**（`github.com`、`raw.githubusercontent.com`），
> 而这些项目的文档源文件、配置与代码**就在仓库里**。
> 因此本模块的一手来源是可核验的，**12 篇全部可撰写**，
> 披露标签统一为 `开源代码/配置披露`。
> 详见 [AGENTS.md 第 11 节](../../AGENTS.md) 的复测结果。

## 写作要求

1. **每个项目必须包括**：项目定位、架构、支持模型、支持硬件、核心优化、教学配置示例、适合 workload、**不适合 workload**、可观测性、扩展性、局限、竞品对比、官方文档来源、版本信息
2. **至少 10 个参考架构**：①单 GPU 本地 LLM ②单节点多 GPU serving ③Kubernetes 服务 ④多模型 routing gateway ⑤RAG serving ⑥长上下文服务 ⑦LoRA/multi-tenant adapter serving ⑧MoE serving ⑨prefill/decode 分离 ⑩edge-cloud hybrid service
3. 版本信息必须带最后核验日期；配置示例须标注对应版本，避免随上游演进而失效

## 完成标准

- [ ] 全部规划文档已按 [`templates/chapter_template.md`](../../templates/chapter_template.md) 完成
- [ ] 模块正文合计 ≥ 12,000 字
- [ ] 上述"写作要求"逐条覆盖
- [ ] 所有事实性数字带来源链接与披露标签
- [ ] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md)
- [ ] 相关 [`data/`](../../data/) CSV 已更新
- [ ] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [ ] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
