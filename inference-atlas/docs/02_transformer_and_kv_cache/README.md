# 模块 02 — Transformer 推理与 KV Cache

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**已完成**
> 模块目标字数：**≥ 15,000 字**
> 最后更新：2026-07-29

## 模块定位

本模块是全库的技术核心。KV cache 是 LLM 推理与传统深度学习推理最本质的区别：它把一个无状态的前向计算变成了**有状态的、显存受限的、生命周期需要被管理的系统资源**。调度、内存管理、长上下文、MoE、disaggregation 等后续所有主题，都建立在本模块的公式与直觉之上。

## 前置阅读

[模块 00](../00_start_here/)、[模块 01](../01_foundations_and_metrics/)

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | [01_transformer_inference_from_first_principles.md](01_transformer_inference_from_first_principles.md) | 从 tensor shape 出发重建一次 forward pass | 已完成 |
| 02 | [02_prefill_vs_decode.md](02_prefill_vs_decode.md) | 两个阶段的计算特征、资源画像与调度含义 | 已完成 |
| 03 | [03_attention_complexity_during_inference.md](03_attention_complexity_during_inference.md) | 推理期 attention 的复杂度与长序列代价 | 已完成 |
| 04 | [04_kv_cache_fundamentals.md](04_kv_cache_fundamentals.md) | KV cache 的必要性、结构与生命周期 | 已完成 |
| 05 | [05_kv_cache_capacity_and_memory_models.md](05_kv_cache_capacity_and_memory_models.md) | KV 容量公式、教学案例与真实实现的偏差来源 | 已完成 |
| 06 | [06_gqa_mqa_mla_and_kv_reduction.md](06_gqa_mqa_mla_and_kv_reduction.md) | MHA/MQA/GQA/MLA 对 KV 体积与质量的影响 | 已完成 |
| 07 | [07_long_context_inference.md](07_long_context_inference.md) | 长上下文的时延、显存与质量三重压力 | 已完成 |
| 08 | [08_kv_cache_compression_quantization_and_eviction.md](08_kv_cache_compression_quantization_and_eviction.md) | KV 压缩、量化、驱逐与 offload 策略 | 已完成 |
| 09 | [09_multimodal_inference.md](09_multimodal_inference.md) | 图像/视频/语音输入对 prefill 与 cache 的影响 | 已完成 |
| 10 | [10_reasoning_workloads_and_test_time_compute.md](10_reasoning_workloads_and_test_time_compute.md) | reasoning 模型的长输出与 test-time compute 特征 | 已完成 |

## 写作要求

1. **Transformer inference**：token embedding、RMSNorm/LayerNorm、Q/K/V projection、attention、MLP/SwiGLU、residual、logits、sampling、autoregressive loop；forward pass 的 tensor shapes；prefill 与 decode 的计算差异；为什么 decode 更容易 memory-bound
2. **KV Cache**：必要性、K/V tensor shape、cache 大小与 layer/batch/sequence/KV heads/head dim/precision 的关系、fragmentation、eviction、prefix cache、prompt cache、reusable cache、paged/block-based memory、cache sharing、compression、quantization、CPU/NVMe/remote offload、remote KV transfer、multi-tenant isolation、privacy 与 security
3. **必须给出并解释**：$M_{KV} \approx 2 \times L \times B \times S \times H_{KV} \times D_h \times b$（$L$ 层数、$B$ 并发序列数、$S$ 缓存 token 数、$H_{KV}$ KV heads、$D_h$ head dimension、$b$ 每元素字节数、系数 2 对应 K 与 V）
4. **必须声明**该公式为教学近似：真实实现还受 page/block 粒度、alignment、padding、metadata、cache sharing、tensor parallel 分片与 runtime 策略影响
5. **必须比较**：MHA、MQA、GQA、MLA、sliding-window attention、long context、recurrent/memory 架构、RAG 与长上下文的关系、RoPE scaling 的推理影响
6. **必须包含**：KV cache 生命周期 Mermaid 图；prefill vs decode 资源对比表；MHA/MQA/GQA/MLA 对比表；KV 容量计算案例；cache hit/miss 对服务质量影响表；long context 设计决策树

## 完成标准

- [x] 全部规划文档已按 [`templates/chapter_template.md`](../../templates/chapter_template.md) 完成
- [x] 模块正文合计 ≥ 15,000 字
- [x] 上述"写作要求"逐条覆盖
- [x] 所有事实性数字带来源链接与披露标签
- [x] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md)
- [x] 相关 [`data/`](../../data/) CSV 已更新
- [x] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [x] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
