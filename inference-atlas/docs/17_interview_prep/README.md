# 模块 17 — 面试准备

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**待开始**
> 模块目标字数：**≥ 12,000 字**
> 最后更新：2026-07-29

## 模块定位

本模块是全库知识的**输出层**：把前 17 个模块的内容转化为可在 2–5 分钟内口头表达的结构化答案。题库规模被硬性约束为**恰好 100 道**，且每道题必须直接给出完整参考答案——只给提纲、不给答案的题目视为未完成。

## 前置阅读

全部模块

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | `01_inference_system_design.md` | 推理系统设计题与完整参考答案 | 待开始 |
| 02 | `02_kv_cache_and_transformer_questions.md` | Transformer 与 KV cache 题组 | 待开始 |
| 03 | `03_serving_scheduling_and_slo_questions.md` | serving、调度与 SLO 题组 | 待开始 |
| 04 | `04_compiler_kernel_and_quantization_questions.md` | 编译器、kernel 与量化题组 | 待开始 |
| 05 | `05_distributed_moe_and_networking_questions.md` | 分布式、MoE 与网络题组 | 待开始 |
| 06 | `06_hardware_datacenter_and_edge_questions.md` | 硬件、数据中心与边缘题组 | 待开始 |
| 07 | `07_debugging_benchmarking_and_observability_questions.md` | 调试、基准与可观测性题组 | 待开始 |
| 08 | `08_company_strategy_and_paper_discussion.md` | 公司战略与论文讨论题组 | 待开始 |
| 09 | `09_mock_interview_cases.md` | 模拟面试案例 | 待开始 |
| 10 | `10_coding_exercises.md` | 编码练习 | 待开始 |
| 11 | `11_90_day_study_plan.md` | 90 天学习计划 | 待开始 |

## 写作要求

1. **服务岗位**：Inference Engineer、ML Systems Engineer、AI Infrastructure Engineer、Compiler Engineer、GPU Performance Engineer、Serving Engineer、Distributed Systems Engineer、AI Hardware/ASIC Engineer、Datacenter Networking Engineer、Edge AI Engineer、Technical Product/Strategy、Research Engineer
2. **题目总数必须恰好 100 道**，分布见下表，由 `scripts/interview_coverage_report.py` 强制校验
3. **每道题必须**：直接包含完整参考答案；支持 2–5 分钟口头回答；包含明确结论；解释核心原理；给出设计、计算或排查路径；分析 trade-off；给出一个真实工程、论文或公开案例；写出局限或常见错误；链接至少一个数据库文档；涉及公司时只以公开资料为依据
4. **每 session 完成 10–15 道**，不得一次性生成全部 100 道
5. 格式模板见 [`templates/interview_question_template.md`](../../templates/interview_question_template.md)；同步录入 [`data/interview_questions.csv`](../../data/interview_questions.csv)

### 题目分布（硬性约束）

| 类别 | 题数 | 内容 |
|---|---:|---|
| 推理基础、指标、排队论、成本 | 12 | TTFT、TPOT、吞吐、goodput、queueing、TCO |
| Transformer、prefill/decode 与 KV Cache | 16 | KV 容量、GQA、MLA、long context、cache |
| Serving、batching、调度、QoS | 16 | continuous batching、routing、autoscaling、SLO |
| Compiler、kernel、量化与 runtime | 14 | TensorRT、Triton、FlashAttention、FP8/INT4 |
| 分布式、MoE、网络与 disaggregation | 18 | TP、EP、all-to-all、RDMA、KV transfer |
| 硬件、HBM、数据中心、edge | 12 | GPU/ASIC、memory wall、power、thermal、mobile |
| Debug、benchmark、可靠性、安全 | 7 | profiling、tail latency、incident、benchmark |
| 公司、论文与战略讨论 | 5 | 技术路线、商业模式、行业判断 |
| **合计** | **100** | 每题附完整答案 |

### 90 天计划周次骨架

| 周 | 主题 |
|---|---|
| 1–2 | 推理指标、Transformer inference、prefill/decode |
| 3–4 | KV cache、batching、serving engines |
| 5–6 | compiler、kernel、quantization、profiling |
| 7–8 | distributed inference、MoE、networking |
| 9 | hardware、HBM、server、datacenter |
| 10 | benchmark、reliability、incident response |
| 11 | 公司路线、市场、论文精读 |
| 12 | 模拟白板、系统设计、debug、项目讲解 |

### 必须包含并直接给出完整答案的 30 道系统设计题

1. 设计一个面向百万 DAU 的多模型 LLM chat service
2. 设计一个低 TTFT、高并发 LLM serving system
3. 如何为长上下文 RAG 设计 KV cache
4. 如何计算给定 context、batch 和精度下的 KV cache
5. 如何选择 static、dynamic 和 continuous batching
6. P99 很高但均值正常如何排查
7. TTFT 高、TPOT 正常如何排查
8. TPOT 高、TTFT 正常如何排查
9. 如何设计 prefill/decode disaggregation
10. 如何设计 MoE serving 集群
11. MoE all-to-all 拖慢推理如何优化
12. 如何设计 speculative decoding 并判断是否有真实收益
13. 如何在质量、吞吐、延迟、成本间选择 INT8/INT4/FP8/BF16
14. 如何为 inference workload 选择 GPU、ASIC 或 edge NPU
15. 如何做 TensorRT-LLM / vLLM / SGLang 选型
16. 如何设计 model routing 和 cascade
17. 如何设计 GPU/NIC/switch/rack 网络
18. 如何定义严谨的 inference benchmark
19. 如何判断厂商 benchmark 是否可比
20. 如何将 J/token 和 cost/token 纳入 capacity planning
21. cache thrashing 如何排查
22. 如何做 multi-tenant QoS
23. 如何 autoscale 并避免 cold start
24. 如何解决模型加载和权重分发瓶颈
25. 如何应对 region failure 或 capacity shortage
26. 如何设计 edge-cloud hybrid agent
27. 如何评估 CXL/remote memory 对 KV cache 的价值
28. 为什么推理网络需求和训练不同
29. 如何分析 reasoning model 的 test-time compute 经济学
30. 如何比较 NVIDIA、hyperscaler ASIC 和 inference startup 的公开路线

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
