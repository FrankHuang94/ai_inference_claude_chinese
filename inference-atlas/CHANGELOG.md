# CHANGELOG — InferenceAtlas

本文件记录数据库的阶段性变更。遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 风格，版本号采用语义化版本。

**当前阶段**：Phase 0 已完成 ｜ **下一阶段**：Phase 1（模块 00 正文，需用户确认后启动）

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
