# CHANGELOG — InferenceAtlas

本文件记录数据库的阶段性变更。遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 风格，版本号采用语义化版本。

**当前阶段**：Phase 5 进行中（模块 04 完成 5/11 篇）｜ **阻塞**：七个 CSV 因网络出口策略无法录入，见 [AGENTS.md 第 11 节](AGENTS.md)

---

## [v0.6.0] — 2026-07-29

### Phase 5（进行中）：模块 04 — Compiler、Runtime、Kernel 与量化

**状态**：模块 04 `进行中`（5/11 篇，16,513 字）。全库正文 139,501 字。

#### 重要：网络核验能力受阻

按用户指示尝试开启一手来源核验（方案 A），探测结果为**组织级出口策略拒绝**：

| 来源 | 状态 |
|---|---|
| `arxiv.org`、`export.arxiv.org` | 拒绝（`connect_rejected`，gateway 403 to CONNECT） |
| `usenix.org`、`dl.acm.org`、`openreview.net`、`proceedings.mlr.press` | 拒绝 |
| `huggingface.co`（模型卡唯一权威源） | 拒绝 |
| `mlcommons.org`（MLPerf 官方结果） | 拒绝 |
| `pytorch.org`、`docs.nvidia.com`、`onnxruntime.ai`、`jedec.org` | 拒绝 |
| `github.com`、`raw.githubusercontent.com` | 可达 |
| `api.github.com` | 可达但仅限本 session 已授权仓库；`add_repo` 不支持跨 owner |

已验证 WebFetch 与 curl 走同一条策略代理，无第二路径。按
`/root/.ccr/README.md` 规定，此类拒绝属组织策略，已上报而未绕行。

**后果**：七个 CSV（`papers`、`models`、`accelerators`、`benchmarks`、
`networking_technologies`、`companies`、`cloud_pricing`）无法按 AGENTS.md 第 5 节
的来源纪律录入。约束已固化为 [AGENTS.md 第 11 节](AGENTS.md)，含探测方法、
实测结果、受阻时的允许/禁止行为清单，以及解除阻塞所需的白名单清单。

#### 新增文档（5 篇，16,513 字，63 表，5 图）

| 文档 | 要点 |
|---|---|
| `01_inference_software_stack.md` | 七层结构、**编译器价值的三个机制**、固定开销模型 $\eta=T_c/(T_c+T_o)$、层与症状映射表 |
| `02_graph_compilers_and_ir.md` | 多级 IR 的动机、**融合的四个边界条件**、动态形状三策略、**pass 顺序不可交换** |
| `03_tensorrt_llm.md` | 深度编译路线：**五维绑定关系与产物组合爆炸**、10 项选型核实清单、适用边界 |
| `04_torch_compile_inductor_and_triton.md` | 渐进式编译：**图中断**与**重编译**两大陷阱、按维度的动态/分桶策略、DSL 的价值与局限 |
| `05_xla_jax_and_tpu_runtime.md` | 编译器优先栈：复杂度从硬件转移到编译器、**执行确定性改善 P99/P50**、覆盖度是选型核心 |

**来源受限处理**：03–05 三篇涉及具体产品，官方文档站不可达，故只写
**可从架构原理推导的分析框架与选型判据**，不给版本号、配置项、特性矩阵或性能数字，
全部标注 `待核实`。章首均有明确的来源限制声明，提示读者勿当产品手册使用。

#### 待完成（模块 04 剩余 6 篇）

`06_onnx_runtime_openvino_and_portability.md`、`07_kernel_fusion_and_operator_optimization.md`、
`08_flashattention_and_memory_efficient_attention.md`、`09_quantization_kernels.md`、
`10_cuda_graphs_and_execution_overhead.md`、`11_compiler_debugging_and_profiling.md`

其中 07–11 以原理为主，不依赖受阻来源，可正常撰写。

#### QA 结果

13 个脚本全部通过：1,127 条内部链接无死链；39 篇适用章节模板的文档无缺章；
37 张 Mermaid 图语法正确且四要素解释齐备。

本次 QA 暴露并修正：模块内 17 处指向**尚未撰写文档**的前向引用被判为死链，
已按项目约定（只链接已存在文件）改为代码体，待对应文档写成后恢复为链接。

---

## [v0.5.0] — 2026-07-29

### Phase 4：模块 03 — Serving Engines、调度与 QoS

**状态**：模块 03 `已完成`。目标 17,000 字，实际 38,095 字（224%）。

> **里程碑**：全库中文正文达 **121,924 字**，超过最终目标 120,000（101.6%），
> 远超最低验收线 100,000。**但数据库整体尚未完成**——文档数、图示数、
> 结构化数据记录与面试题库仍有较大缺口，见下方"剩余缺口"。

#### 新增文档（12 篇，38,095 字，133 表，11 图）

| 文档 | 要点 |
|---|---|
| `01_serving_architecture_overview.md` | 16 组件清单、**控制面/数据面划分**、调度层是倍数级杠杆的定量依据、职责错配表 |
| `02_static_dynamic_and_continuous_batching.md` | **有效批大小推导**、收益饱和三条件、**tail latency 恶化的三个机制**、调度器伪代码 |
| `03_pagedattention_and_kv_memory_management.md` | 三类浪费分解、OS 类比表、块大小权衡、**分配器伪代码**、copy-on-write 场景 |
| `04_request_scheduling_and_admission_control.md` | **过载正反馈回路**、四判据准入控制器伪代码、五种调度策略、老化与背压 |
| `05_prefill_decode_scheduling.md` | **Token 预算模型**、chunk 大小下界（避免退化为 memory-bound）、prefill 饥饿失效模式 |
| `06_multi_tenant_isolation_and_qos.md` | **三类隔离**（性能/容量/信息）、多维配额、**token·秒计量**、前缀缓存的时序侧信道 |
| `07_model_routing_and_cascade_systems.md` | 级联划算条件 $p<1-C_s/C_l$、**级联抬高尾时延因而不适合交互式**、两类路由错误的非对称代价 |
| `08_prompt_caching_and_prefix_caching.md` | 收益计算、**路由稀释是命中率的首要杀手**、链式指纹伪代码、prompt 构造规范 |
| `09_session_memory_and_conversation_state.md` | **驻留经济学**（显存 × 思考时间）、机会主义缓存、KV 是派生数据而非会话状态 |
| `10_autoscaling_and_load_balancing.md` | **autoscaler 应对趋势、余量应对突发**、GPU 利用率为何不适合作指标、缩容更危险 |
| `11_serverless_and_burst_inference.md` | **成本交叉点 $U<c_r/c_s$**、冷启动对 P95 的影响、常驻+弹性混合架构 |
| `12_serving_incident_playbook.md` | 值班手册：一分钟分诊、9 类症状处置、**降级顺序表**、复盘模板、预防清单 |

#### 同步更新

- `INDEX.md`、模块 README、`README.md` 统计
- `GLOSSARY.md`：新增第 14 节共 26 条术语

#### QA 结果

13 个脚本全部通过：1,057 条内部链接无死链；34 篇适用章节模板的文档无缺章；
32 张 Mermaid 图语法正确且四要素解释齐备。

#### 剩余缺口（数据库**未**完成）

| 项目 | 当前 | 目标 | 缺口 |
|---|---:|---:|---|
| 中文正文字数 | 121,924 | 120,000 | **已达成** |
| 实质内容文档 | 38 | 120 | 82 |
| Markdown 表格 | 398 | 110 | **已达成** |
| Mermaid 图示 | 32 | 60 | 28 |
| 已核验来源 | 5 | 550 | 545 |
| 模型记录 | 0 | 120 | 120 |
| 推理引擎记录 | 2 | 40 | 38 |
| 加速器/平台记录 | 0 | 80 | 80 |
| 网络技术记录 | 0 | 50 | 50 |
| benchmark/部署案例 | 0 | 100 | 100 |
| 技术卡片 | 2 | 90 | 88 |
| 组织记录 / 深度档案 | 0 / 0 | 60 / 30 | 60 / 30 |
| 面试题 | 0 | **恰好 100** | 100 |
| 待完成模块 | — | 04–17 | 14 个 |

#### 未核验事项（本阶段刻意留白）

- **chunked prefill 的原始学术工作**（Sarathi 系列等）：留待模块 13 核验
- **模型路由与级联的实证节省比例**（FrugalGPT 等）：同上
- **各引擎的 chunked prefill / 前缀缓存配置项名称与默认值**：随版本变化，留待模块 12
- **各云厂商 serverless 推理的定价、冷启动时长、是否支持实例内批处理**：留待模块 15
- **冷启动时长、块大小最优值、各类阈值参数**：依赖部署，正文均要求实测标定
- 前缀缓存时序侧信道分析基于**机制推理**，未引用具体漏洞报告

---

## [v0.4.0] — 2026-07-29

### Phase 3：模块 02 — Transformer 推理与 KV Cache

**状态**：模块 02 `已完成`。目标 15,000 字，实际 30,961 字（206%）。全库累计 79,316 字（66%）。

#### 新增文档（10 篇，30,961 字，110 表，10 图）

| 文档 | 要点 |
|---|---|
| `01_transformer_inference_from_first_principles.md` | 逐层张量形状表、计算量分解、**算术强度统一形式 $I\approx 2\times(\text{同时处理 token 数})/b_w$**、自回归为何必然导出 KV cache |
| `02_prefill_vs_decode.md` | 13 维资源画像对比表、$I_{prefill}/I_{decode}\approx S_{in}$、批处理收益不对称的成因、三种共存方案对比 |
| `03_attention_complexity_during_inference.md` | prefill 平方 / decode 线性、**decode 注意力算术强度 $2H/(H_{KV}b_{kv})$ 与 $S$、$B$ 无关**、$B\times S$ 乘积判据 |
| `04_kv_cache_fundamentals.md` | 生命周期状态机、五个管理维度、碎片三来源、**共享作用域应默认限于租户内** |
| `05_kv_cache_capacity_and_memory_models.md` | 容量公式与 $m_{tok}$、**反解可行边界**、四方案对比表、七项偏差来源 |
| `06_gqa_mqa_mla_and_kv_reduction.md` | 四结构对比、压缩比与算术强度、**为何必须预训练时决定**、MQA 与大 TP 度的整除性冲突 |
| `07_long_context_inference.md` | 三重压力、TTFT 增长 2–4 倍、并发反比、**标称窗口≠有效能力**、RAG 与长上下文的互补关系 |
| `08_kv_cache_compression_quantization_and_eviction.md` | 三类手段的代价性质、K/V 敏感度不对称、**offload 判据是带宽非容量**、针对性评测设计 |
| `09_multimodal_inference.md` | 多模态是 prefill 主导、编码器作为额外流水线级、特征缓存的适用条件 |
| `10_reasoning_workloads_and_test_time_compute.md` | 输出长度由模型决定、$C_S$ 放大排队、**思考预算兼作成本控制与过载降级旋钮** |

#### 同步更新

- `INDEX.md`、模块 README、`README.md` 统计
- `GLOSSARY.md`：新增第 13 节共 17 条术语

#### QA 结果

13 个脚本全部通过：871 条内部链接无死链；23 篇适用章节模板的文档无缺章；
21 张 Mermaid 图语法正确且四要素解释齐备；单位一致性告警 1 条（有意保留的教学反例）。

#### 未核验事项（本阶段刻意留白，不猜测）

- **MQA / GQA / MLA 的原始论文编号、作者与实验数字**：留待模块 13 逐篇打开原文核验后录入 `papers.csv`
- **各模型的 $L$、$H_{KV}$、$D_h$、上下文窗口实际值**：须引用官方模型卡，`models.csv` 仍为空
- **KV 量化的质量损失幅度、驱逐策略效果、长上下文质量评测**：依赖模型与任务，要求实测
- **多模态模型的每图像/每秒视频 token 数**：须引用官方模型卡
- **test-time compute 的质量-成本曲线形状与拐点**：留待模块 05/13 核验
- 第 5 章数值案例使用**演示用假设参数**（$L=32$、$H_{KV}=8$、$D_h=128$、40 GiB），已在文中声明不对应任何真实产品

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
