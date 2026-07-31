# 模块 10 — Edge 与 On-Device Inference

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**进行中（1/9 篇）**
> 模块目标字数：**≥ 10,000 字**
> 最后更新：2026-07-29

## 模块定位

端侧推理面对的是与数据中心完全不同的约束集合：内存以 GB 而非 TB 计，功耗以 W 而非 kW 计，且必须在热预算与电池之间做持续权衡。本模块要求给出**云、边、端混合架构的清晰决策边界**，而不是笼统地声称端侧会取代云。

## 前置阅读

[模块 04](../04_compilers_runtimes_and_kernels/)、[模块 07](../07_hardware_and_server_architecture/)

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | [01_edge_inference_overview.md](01_edge_inference_overview.md) | 边缘推理的约束条件与价值主张 | 已完成 |
| 02 | `02_mobile_npu_soc_and_memory_constraints.md` | 移动 SoC、NPU 与 LPDDR 约束 | 待开始 |
| 03 | `03_qualcomm_apple_mediatek_google_samsung_platforms.md` | 主要移动平台的端侧推理能力 | **受阻**（内容本体为需核验的厂商规格，出口策略下无法撰写） |
| 04 | `04_pc_ai_inference.md` | AI PC 的推理路径 | 待开始 |
| 05 | `05_automotive_robotics_and_embedded_inference.md` | 车载、机器人与嵌入式推理 | 待开始 |
| 06 | `06_small_language_models_and_on_device_agents.md` | 小模型与端侧 agent | 待开始 |
| 07 | `07_quantization_distillation_and_pruning_for_edge.md` | 面向端侧的模型压缩 | 待开始 |
| 08 | `08_private_hybrid_cloud_edge_architectures.md` | 云-边混合与隐私优先架构 | 待开始 |
| 09 | `09_edge_deployment_case_studies.md` | 端侧部署案例 | 待开始 |

## 写作要求

1. **覆盖**：edge inference；on-device LLM；mobile SoC；NPU；CPU/GPU/NPU 异构执行；unified memory；LPDDR；memory capacity；thermal envelope；battery；offline；privacy；cloud-edge hybrid；quantization；distillation；pruning；small language model；on-device RAG；multimodal；automotive；robotics；AI PC；deployment tooling；secure enclave；model protection
2. **必须比较**：cloud-only、edge-only、cloud-edge hybrid、local-first、privacy-sensitive、bandwidth-constrained、intermittent connectivity、low-latency control loops
3. 厂商 TOPS 宣称必须注明精度与测量条件，并标注披露等级

## 完成标准

- [ ] 全部规划文档已按 [`templates/chapter_template.md`](../../templates/chapter_template.md) 完成
- [ ] 模块正文合计 ≥ 10,000 字
- [ ] 上述"写作要求"逐条覆盖
- [ ] 所有事实性数字带来源链接与披露标签
- [ ] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md)
- [ ] 相关 [`data/`](../../data/) CSV 已更新
- [ ] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [ ] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
