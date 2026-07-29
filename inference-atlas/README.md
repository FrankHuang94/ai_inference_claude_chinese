# InferenceAtlas

## AI 推理：模型服务、推理系统、芯片、网络、数据中心与产业战略数据库

> **内容版本**：v0.1.0（Phase 0 初始化）
> **信息截至**：2026-07-29
> **最后核验**：2026-07-29
> **构建模式**：单一 Agent、串行、模块化（详见 [AGENTS.md](AGENTS.md)）

---

## 1. 项目定位

InferenceAtlas 是一个**中文**的 AI 推理知识数据库，目标是在 GitHub 上提供一份**可检索、可引用、可更新、GitHub 原生可浏览**的端到端参考资料。

它覆盖从单个 token 的生成路径，一直到芯片、HBM、互连、光网络、机房电力散热与产业经济学的完整推理栈。

**它不是**：课程大纲、一篇泛泛综述、或一堆空目录模板。每个标记为"已完成"的模块都必须包含真实正文、结构化表格、可核验来源、交叉链接与必要图示。

---

## 2. 读者画像

目标读者是具备计算机科学、半导体、分布式系统、云计算、基础模型与数据中心基础的技术专业人士，希望：

1. 理解 LLM、VLM、生成式视频、语音、RAG 与 agent 的在线/离线推理；
2. 设计高吞吐、低时延、高可靠、低成本的模型推理系统；
3. 掌握 prefill、decode、KV cache、continuous batching、PagedAttention、speculative decoding、MoE inference、long context、disaggregated serving；
4. 理解模型图、编译器、runtime、kernel、GPU/ASIC、HBM、互连、光网络、数据中心与边缘设备的端到端推理栈；
5. 分析主要芯片、云、模型与网络厂商的**公开**技术与商业路线；
6. 准备 Inference Engineer、ML Systems Engineer、AI Infrastructure Engineer、Compiler Engineer、Performance Engineer、AI Hardware/ASIC、Datacenter Network、Edge AI、Technical Strategy 等岗位；
7. 用于 AI 基础设施、半导体、云、网络、光互连与数据中心的技术战略与投资尽调。

---

## 3. 端到端推理栈简介

一次用户请求穿过的层次大致如下（详细展开见模块 00）：

```text
客户端
  → API gateway / 认证 / 限流
  → 请求路由与分类
  → 队列与调度器
  → tokenizer
  → prefill worker
  → KV cache manager
  → decode worker
  → 流式响应
  → 日志 / tracing / 计费
  → autoscaler / 容量规划
```

其下承载的物理层依次是：加速器（GPU/ASIC/NPU）→ 片上与封装内互连 → 服务器节点 → 机架 → 集群网络（scale-up 与 scale-out）→ 光互连 → 数据中心电力与散热。

---

## 4. 核心问题

推理系统设计的本质，是在以下互相冲突的目标之间求解：

| 维度 | 典型指标 |
|---|---|
| 质量 | 任务准确率、指令遵循、幻觉率 |
| 首字时延 | TTFT（time to first token） |
| 逐字时延 | TPOT / ITL |
| 吞吐 | tokens/s、requests/s、goodput |
| 成本 | $/1M tokens、TCO、单位经济性 |
| 功耗 | W、J/token、PUE |
| 可靠性 | 可用性、P99、错误预算 |
| 安全 | 租户隔离、cache 隐私、滥用防护 |

**没有任何单一配置能同时最优化全部维度。** 本数据库的核心价值，是把这些 trade-off 拆解为可计算、可测量、可决策的框架。

---

## 5. 免责声明

- 本数据库仅供**学习、研究、技术战略分析与投资尽调框架**使用；
- **不构成投资建议**，不构成对任何证券的买卖推荐；
- 所有公司、产品、性能与市场信息均来自**公开渠道**，并标注披露等级；
- 第三方估计与官方披露被严格区分，不得混用；
- 高时效内容（定价、路线图、财报、benchmark）可能已过时，请核对"最后核验日期"；
- 本项目与文中提及的任何公司均无关联关系。

---

## 6. 内容统计

> 由 `scripts/word_count.py` 与 `scripts/mermaid_audit.py` 生成，每完成若干关键文档后更新。

| 指标 | 当前 | 最终目标 | 最低验收线 |
|---|---:|---:|---:|
| 中文正文字数 | **161,100** | 120,000 | 100,000 |
| 实质内容 Markdown 文档 | 49 | 120 | — |
| Markdown 表格 | 536 | 110 | — |
| Mermaid 图示 | 43 | 60 | — |
| 已核验来源条目 | 5 | 550 | — |
| 模型记录 | 0 | 120 | — |
| 推理引擎记录 | 2 | 40 | — |
| 芯片/加速器/服务器/平台记录 | 0 | 80 | — |
| 网络与互连技术记录 | 0 | 50 | — |
| benchmark 或部署案例 | 0 | 100 | — |
| 技术卡片 | 2 | 90 | — |
| 组织记录 | 0 | 60 | — |
| 组织深度档案 | 0 | 30 | — |
| 面试题 | 0 | **恰好 100** | — |

**当前阶段**：Phase 5 已完成（模块 00–04）。**注意：`papers`、`models`、`accelerators`、`benchmarks`、`networking_technologies`、`companies`、`cloud_pricing` 七个 CSV 因组织级网络出口策略无法按来源纪律录入，详见 [AGENTS.md 第 11 节](AGENTS.md)。****中文正文字数已达最终目标 120,000**（121,924，101.6%）。其余 14 个模块 `待开始`，其中面试题库、论文卡片与结构化数据仍是主要缺口。

---

## 7. 数据来源与披露等级

所有涉及模型、芯片、硬件、网络、性能、成本、市场、客户、融资、财务、部署规模的信息，必须携带以下标签之一：

| 标签 | 含义 |
|---|---|
| `官方披露` | 厂商/机构官方文档、财报、新闻稿、模型卡直接陈述 |
| `技术文档披露` | 官方技术手册、白皮书、架构文档中的规格 |
| `开源代码/配置披露` | 可在公开 repo 中直接验证的实现或默认配置 |
| `独立可复现实验` | 有完整环境说明、可被第三方复现的测试 |
| `可信第三方估计` | 有方法论说明的第三方研究或拆解，**非官方确认** |
| `未公开` | 该项信息厂商未公开，不得猜测 |
| `待核实` | 有线索但尚未找到可靠一手来源 |

来源优先级与不可单独采信的来源类型，详见 [AGENTS.md](AGENTS.md) 第 5 节。

---

## 8. 目录

完整可点击导航见 **[INDEX.md](INDEX.md)**。

| # | 模块 | 状态 |
|---|---|---|
| 00 | [入门与端到端总览](docs/00_start_here/) | **已完成** |
| 01 | [基础、指标、排队论与成本](docs/01_foundations_and_metrics/) | **已完成** |
| 02 | [Transformer 推理与 KV Cache](docs/02_transformer_and_kv_cache/) | **已完成** |
| 03 | [Serving Engines、调度与 QoS](docs/03_serving_engines_and_scheduling/) | **已完成** |
| 04 | [Compiler、Runtime、Kernel 与量化](docs/04_compilers_runtimes_and_kernels/) | **已完成** |
| 05 | [解码、Speculative 与 Reasoning 推理](docs/05_decoding_and_generation_algorithms/) | 待开始 |
| 06 | [分布式、MoE 与 Disaggregated Inference](docs/06_distributed_and_moe_inference/) | 待开始 |
| 07 | [硬件、HBM、封装与服务器](docs/07_hardware_and_server_architecture/) | 待开始 |
| 08 | [网络、互连与光学](docs/08_networking_and_interconnect/) | 待开始 |
| 09 | [数据中心、电力、散热与运维](docs/09_datacenter_power_thermal_and_operations/) | 待开始 |
| 10 | [Edge 与 On-Device Inference](docs/10_edge_and_on_device_inference/) | 待开始 |
| 11 | [Benchmark、可靠性、可观测性与安全](docs/11_benchmarking_reliability_and_observability/) | 待开始 |
| 12 | [开源部署、复现与参考架构](docs/12_open_source_deployment_and_reproduction/) | 待开始 |
| 13 | [论文与技术报告地图](docs/13_research_papers_and_technical_reports/) | 待开始 |
| 14 | [公司与生态](docs/14_company_and_ecosystem_landscape/) | 待开始 |
| 15 | [市场、经济学与战略](docs/15_market_economics_and_strategy/) | 待开始 |
| 16 | [未来路线](docs/16_research_frontiers/) | 待开始 |
| 17 | [面试准备](docs/17_interview_prep/) | 待开始 |

结构化数据见 [`data/`](data/)，schema 见 [`data/schemas/`](data/schemas/)，写作模板见 [`templates/`](templates/)。

---

## 9. GitHub 浏览方法

- **从 [INDEX.md](INDEX.md) 进入**：它是全库唯一入口，提供按系统层、按 workload、按指标三种检索路径与"快速路径"专题。
- **Mermaid 图**：GitHub 原生渲染 ` ```mermaid ` 代码块，无需额外工具。
- **LaTeX 公式**：GitHub 支持 `$...$` 与 `$$...$$` 渲染。
- **CSV**：GitHub 会将 `data/*.csv` 渲染为可排序表格，并支持按列筛选。
- **术语**：不确定的缩写先查 [GLOSSARY.md](GLOSSARY.md)。
- **变更历史**：见 [CHANGELOG.md](CHANGELOG.md)。

---

## 10. 如何运行 QA 脚本

所有脚本仅依赖 Python 3 标准库，无需安装第三方包。

```bash
cd inference-atlas

# 单独运行
python3 scripts/word_count.py              # 字数统计 → reports/word_count_report.md
python3 scripts/validate_links.py          # 内部链接检查 → reports/link_validation_report.md
python3 scripts/validate_csv_schema.py     # CSV schema 校验 → reports/data_quality_report.md
python3 scripts/check_required_sections.py # 文档必备章节检查
python3 scripts/freshness_report.py        # 时效性复核（>180 天告警）
python3 scripts/paper_citation_audit.py    # 论文引用完整性
python3 scripts/benchmark_audit.py         # benchmark 方法论完整性
python3 scripts/hardware_spec_audit.py     # 硬件规格来源与口径
python3 scripts/unit_consistency_audit.py  # 单位一致性（GB/GiB、TB/s vs Tb/s 等）
python3 scripts/company_disclosure_audit.py# 公司信息披露标签
python3 scripts/interview_coverage_report.py # 面试题数量/分布/答案完整性
python3 scripts/mermaid_audit.py           # Mermaid 图统计与语法
python3 scripts/generate_index.py --check  # INDEX 与实际文件一致性

# 提交前最小门禁
python3 scripts/validate_csv_schema.py && \
python3 scripts/validate_links.py && \
python3 scripts/word_count.py
```

脚本以非零退出码表示存在**阻断级**问题。所有报告输出到 [`reports/`](reports/)。

---

## 11. 如何贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。核心要求：

1. **单一 Agent、串行推进**——本仓库**禁止** agent swarm、并行子 Agent、多 Agent 分工、并发 worktree 与并行 branch（完整禁止清单见 [AGENTS.md](AGENTS.md) 第 1 节）；
2. 一次 PR/session 只推进**一个明确工作包**（1 个模块，或 2–4 篇紧密相关文档）；
3. 不创建空文件或纯占位符文件；
4. 所有事实性陈述附来源链接与披露等级；
5. 提交前通过最小 QA 门禁。

---

## 12. 更新机制

| 内容类型 | 复核周期 | 触发条件 |
|---|---|---|
| API/云定价 | 90 天 | 厂商调价 |
| 模型版本与能力 | 90 天 | 新模型发布 |
| 推理引擎版本与特性 | 90 天 | 主要 release |
| GPU/ASIC 路线图 | 180 天 | 官方发布会、财报 |
| HBM 与网络规格 | 180 天 | JEDEC/OIF/UEC 标准更新 |
| MLPerf 成绩 | 每轮提交 | 官方结果发布 |
| 公司财报与并购 | 90 天 | 季报、正式公告 |
| 出口管制与政策 | 90 天 | 法规更新 |
| 论文卡片 | 365 天 | 重要后续工作出现 |

`scripts/freshness_report.py` 会扫描 CSV 与文档头部的 `最后核验` 字段，对超过 180 天未复核的高时效内容生成更新优先级列表。

---

## 13. License

本仓库文本内容采用 **CC BY 4.0**，脚本代码采用 **MIT**。详见 [LICENSE](LICENSE)。

引用的论文、官方文档与公司材料版权归原作者所有；本项目仅做**摘要、结构化与链接**，不做大段复制。
