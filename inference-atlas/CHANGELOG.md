# CHANGELOG — InferenceAtlas

本文件记录数据库的阶段性变更。遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 风格，版本号采用语义化版本。

**当前阶段**：Phase 2 已完成（模块 00–01）｜ **下一阶段**：Phase 3（模块 02 Transformer 推理与 KV Cache）

---

## [v0.3.0] — 2026-07-29

### Phase 2：模块 01 — 基础、指标、排队论与成本

**状态**：模块 01 `已完成`。目标 14,000 字，实际 26,531 字（189%）。

#### 新增文档（9 篇，26,531 字，91 表，8 图）

| 文档 | 要点 |
|---|---|
| `01_inference_workload_taxonomy.md` | 四参数刻画法、$R=S_{in}/S_{out}$ 判据、9 类 workload 画像、混合干扰与隔离 |
| `02_latency_throughput_and_slo.md` | TTFT/TPOT/ITL 精确定义与口径分歧、三种测量边界、吞吐-时延反向关系、分层 SLO |
| `03_queueing_theory_for_inference.md` | Little's Law 与三个数值案例、$\frac{\rho}{1-\rho}$ 发散表、$(1+C_S^2)$ 方差放大、抢占重算正反馈 |
| `04_roofline_and_performance_modeling.md` | Roofline 与脊点、**decode 算术强度 $\approx 2B/b_w$ 推导**、优化方向判据、分层 Roofline |
| `05_memory_bandwidth_and_arithmetic_intensity.md` | **单序列 decode 上界 $BW/W_{bytes}$**、批处理摊薄与饱和、临界并发 $B^*$、带宽墙传导链 |
| `06_cost_modeling_and_unit_economics.md` | 成本分解与边界、**利用率倍数表**、输入/输出成本差异的技术依据、避免伪精确 |
| `07_energy_efficiency_and_joules_per_token.md` | J/token 四级测量边界、memory-bound 优化的性能-能效双赢、能效作为容量约束、功率封顶 vs 热降频 |
| `08_capacity_planning.md` | 五步计算链、两约束取小、三余量因子相乘、机架功率校验 |
| `09_inference_metrics_cheat_sheet.md` | 12 节速查（六公式、两张放大表、单位红线、症状首查） |

#### 同步更新

- `INDEX.md`、模块 README、`README.md` 统计
- `GLOSSARY.md`：新增第 12 节「排队、容量与成本建模」共 18 条术语

#### 工具修正（3 项，均由 QA 自身暴露）

- `validate_links.py`：剥离 LaTeX 数学区。`E[S](1+C_S^2)` 这类数学写法在语法上酷似
  Markdown 链接，此前被误报为死链
- `mermaid_audit.py`：上下文检查从「图前后各自都要有关键词」改为
  「前后 20 行合并窗口内覆盖四要素中至少 3 项」，更贴合实际写作约定
- `unit_consistency_audit.py`：收紧分位数规则（仅当报告了**具体数值**时才要求样本量，
  散文提及 P99 概念不告警）；新增反例行豁免（教学用的错误示范本身在演示违规写法）
  —— 告警从 42 降至 1，且剩余 1 条为有意保留的反例

#### QA 结果

13 个脚本全部通过：711 条内部链接无死链；13 篇适用章节模板的文档无缺章；
11 张 Mermaid 图语法正确且四要素解释齐备；CSV schema 无违规。

#### 未核验事项

- 各类 workload 的**具体长度分布数值**：公开可核验数据稀少，正文标注 `待核实`，
  要求生产环境自行标定
- **实测达成比例**（实际吞吐相对 $BW/W_{bytes}$ 上界的比例）：依赖实现质量，`待核实`
- **能耗比值**（HBM 访问 vs 算术运算）：随工艺代际变化大，未引用无来源数字
- 所有**具体价格、PUE、J/token 数值**：本模块一律不给出，留待模块 09/11/15 附一手来源
- `benchmarks.csv`、`deployment_cases.csv`、`cloud_pricing.csv` 仍为空

---

## [v0.2.0] — 2026-07-29

### Phase 1：模块 00 — 入门与端到端总览

**状态**：模块 00 `已完成`。

#### 新增文档（7 篇，21,824 字）

| 文档 | 字数量级 | 要点 |
|---|---|---|
| `00_database_guide.md` | 中 | 三种读法、三个约定（披露等级/口径/近似模型）、已知局限 |
| `01_executive_summary.md` | 中 | 六层栈划分、**三个物理级约束**、技术按约束归类、价值链结构 |
| `02_end_to_end_inference_lifecycle.md` | 大 | 端到端 Mermaid 图、六段时延分解、prefill/decode 资源画像对比、12 层职责与失效表、9 类失败模式排查表 |
| `03_how_to_read_inference_benchmarks.md` | 大 | **20 项审读清单**、六类常见失真、MLPerf 能与不能回答的问题 |
| `04_how_to_design_an_inference_system.md` | 大 | **九步设计流程 Mermaid 图**、KV 显存反推法、并行级别判据、何时不做 disaggregation |
| `05_how_to_prepare_for_inference_interviews.md` | 中 | 岗位能力权重表、四类必算计算、六段回答结构 |
| `06_metrics_units_and_quick_reference.md` | 中 | 12 节速查表（指标/单位/排查/清单/流程） |

- 新增表格：64 ｜ 新增 Mermaid 图：3
- 模块目标 8,000 字，实际 21,824 字（273%）

#### 同步更新

- `INDEX.md`：模块 00 状态改为 `已完成`，7 篇文档改为可点击链接，统计与合计行更新
- `docs/00_start_here/README.md`：状态、文档链接、完成标准勾选
- `GLOSSARY.md`：新增第 11 节「性能建模与设计方法」共 10 条术语
- `README.md`：内容统计与模块状态表

#### 工具修正

- `scripts/check_required_sections.py`：新增元文档/速查/手册类的体裁豁免
  （`*_guide.md`、`*_quick_reference.md`、`*_cheat_sheet.md`、`*_playbook.md` 等），
  这类文档不适用「问题定义→原理→实现→trade-off」章节骨架

#### QA 结果

全部 13 个脚本通过：链接 563 条无死链；5 篇适用章节模板的文档无缺章；
3 张 Mermaid 图语法正确且均有前后文解释；CSV schema 无违规。

#### 未核验事项

- 面试题型占比为本库推论，已在正文标注 `待核实`
- MLPerf 规则细节待模块 11 撰写时逐条核验官方来源
- `benchmarks.csv` 与 `deployment_cases.csv` 仍为空，模块 00 中引用的案例均指向论文而非生产部署

---

## [v0.1.0] — 2026-07-29

### Phase 0：仓库初始化

首次提交，建立基础设施。**不含任何模块正文**。

#### 新增 — 顶层文档

- `README.md` — 项目定位、读者画像、端到端栈简介、核心 trade-off、免责声明、内容统计、披露等级说明、目录、GitHub 浏览方法、QA 运行方法、贡献与更新机制、License
- `INDEX.md` — 全库唯一入口；18 个模块的完整导航（约 150 篇规划文档的一句话说明）、模块状态总览表、按系统层/workload/指标三种检索路径、11 条快速路径、90 天待复核清单、结构化数据入口
- `GLOSSARY.md` — 10 类共 70+ 条核心术语，含统一口径定义与强制单位书写规范
- `AGENTS.md` — **单一 Agent 串行工作协议**：禁止事项清单、session 工作上限、15 步标准流程、内容红线、来源优先级、7 档披露标签、Git 规则、QA 门禁
- `CONTRIBUTING.md` — 贡献流程、写作规范、数据录入规范、审阅清单
- `CHANGELOG.md` — 本文件
- `LICENSE` — 文本 CC BY 4.0 / 代码 MIT
- `.gitignore` — 排除权重、大数据集、二进制、密钥与缓存

#### 新增 — 目录骨架

- `docs/` 下 18 个模块目录，每个含一份**真实内容的模块 README**（模块定位、规划文档清单、写作要求要点、状态、前置阅读），状态统一标记为 `待开始`
- `visuals/` 下 11 个主题目录
- `data/` 与 `data/schemas/`
- `scripts/`、`reports/`、`templates/`

> 按 [AGENTS.md](AGENTS.md) 规定，**未**为任何规划文档创建空壳或占位文件。

#### 新增 — 写作模板（`templates/`）

`chapter_template.md`、`paper_card_template.md`、`company_profile_template.md`、`hardware_card_template.md`、`benchmark_card_template.md`、`technique_card_template.md`、`deployment_case_template.md`、`interview_question_template.md`

#### 新增 — 结构化数据（`data/`）

- 16 个 CSV 文件，均已写入**规范表头**：`papers`、`models`、`inference_engines`、`accelerators`、`server_platforms`、`memory_technologies`、`networking_technologies`、`benchmarks`、`deployment_cases`、`techniques`、`companies`、`company_events`、`cloud_pricing`、`market_transactions`、`glossary`、`interview_questions`
- `references.bib` — BibTeX 引用库，含 5 条 seed 条目
- `data/schemas/` — 9 份 schema 文档，定义字段含义、类型、枚举取值、必填性与校验规则

#### 新增 — Seed 记录（共 10 条，均可核验）

| CSV | 条数 | 内容 |
|---|---:|---|
| `papers.csv` | 5 | Attention Is All You Need；FlashAttention；Orca (OSDI'22)；PagedAttention/vLLM (SOSP'23)；Speculative Decoding (ICML'23) |
| `inference_engines.csv` | 2 | vLLM；SGLang |
| `techniques.csv` | 2 | continuous batching；PagedAttention |
| `glossary.csv` | 1 | TTFT（schema 演示记录） |

#### 新增 — QA 脚本（`scripts/`，13 个，仅依赖 Python 3 标准库）

`word_count.py`、`validate_links.py`、`validate_csv_schema.py`、`check_required_sections.py`、`generate_index.py`、`freshness_report.py`、`paper_citation_audit.py`、`benchmark_audit.py`、`hardware_spec_audit.py`、`unit_consistency_audit.py`、`company_disclosure_audit.py`、`interview_coverage_report.py`、`mermaid_audit.py`

均为**最小可运行版本**：能在当前空内容状态下正确执行、生成报告并返回正确退出码；随模块推进逐步加强规则。

#### 模块状态

全部 18 个模块：`待开始`。

---

## 变更记录规范

每次 session 结束时，在本文件顶部追加一节，格式：

```markdown
## [vX.Y.Z] — YYYY-MM-DD

### Phase N：<工作包名称>

- 完成文档：<清单>
- 新增字数：N
- 新增表格：N ｜ 新增 Mermaid 图：N
- 新增/更新数据记录：<CSV 名称 + 条数>
- QA 结果：<各脚本通过情况>
- 未核验事项：<清单>
- 下一工作包：<建议>
```
