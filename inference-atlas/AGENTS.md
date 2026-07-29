# AGENTS.md — InferenceAtlas 工作协议

本文件定义 InferenceAtlas 的唯一合法构建方式。任何在本仓库中工作的 Agent 或人类贡献者都必须遵守。

---

## 1. 执行模式：单一 Agent、串行、模块化

本项目**强制**采用单一 Agent 逐模块推进模式。

**明确禁止：**

| 禁止事项 | 原因 |
|---|---|
| Agent Swarm | 无法保证术语、口径与来源纪律的一致性 |
| 并行子 Agent | 交叉引用与 INDEX 状态会产生竞态 |
| 多 Agent 分工 | 责任边界模糊，QA 无法归因 |
| 并发 worktree | 破坏串行可恢复性 |
| 并行 branch | 本项目使用单一开发分支 |
| 同时处理多个大型模块 | 导致内容浅薄、来源核验不足 |
| 为形式创建大量空文件 | 违反"无空壳文件"原则 |
| 一次性生成整个数据库 | 必然产生虚构与低质量内容 |
| 未完成当前模块即跳到下一模块 | 破坏阶段验收 |

本项目被视为一个**长期、分阶段、可恢复**的工程项目，目标是在多次 session 中逐渐达成最终验收标准，而非在单次 session 内完成。

---

## 2. 每次 session 的工作上限

每次 session 只能：

- 完成 **1 个主模块**，或一个主模块中 **2–4 篇紧密相关的文档**；
- 不得同时进入多个大模块；
- 不得为尚未开始的模块生成正文；
- 可以创建未来模块的目录与**简短 README**，但不得提前填充大量空壳文档。

---

## 3. 标准工作流程（严格按序）

1. 检查仓库状态（`git status`、`git log`）；
2. 阅读 `README.md`、`INDEX.md`、`CHANGELOG.md`、`GLOSSARY.md` 及当前模块 README；
3. 确认本次**唯一**工作包；
4. 收集并核验本工作包所需的公开资料；
5. 编写/更新当前文档；
6. 更新当前模块的局部目录（模块 README）；
7. 更新必要的 CSV 记录；
8. 更新 `GLOSSARY.md` 中新出现的重要术语；
9. 添加 Mermaid 图或表格；
10. 运行相关 QA 脚本；
11. 修复明显问题；
12. 更新 `CHANGELOG.md`；
13. 提交一次清晰的 Git commit（英文 message）；
14. 输出本次工作报告；
15. **停止**，等待用户指令。

### 第 14 步工作报告必须包含

- 本次完成内容；
- 新增/修改文件清单；
- 新增字数；
- 新增表格数；
- 新增 Mermaid 图数；
- 新增数据记录数；
- **未核验事项**；
- 建议的下一个工作包。

未经用户许可，**不得**启动下一个大型模块。

---

## 4. 内容红线

### 严禁

- 创建空文件；
- 创建只有 TODO、标题、目录或占位符的文件；
- 虚构模型参数、芯片规格、HBM 容量、带宽、TOPS/FLOPS、吞吐、时延、功耗、能耗、集群规模、成本、收入、市场份额、客户关系、融资或合作；
- 将第三方估计、匿名爆料、媒体报道写成"官方确认"；
- 使用"最快""最低成本""最大""领先"等无来源的绝对化表达；
- 通过重复和无意义内容凑字数；
- 大段复制受版权保护的论文、博客或公司材料；
- 提交模型权重、大型数据集、二进制文件、API key、私密 token 或受限材料；
- 在无可靠来源时编造任何公司内部推理基础设施细节。

### 必须

- 每篇已完成文档都有真实正文、结构化表格、来源与交叉链接；
- 所有涉及性能、成本、规格、市场的陈述带**披露等级标签**；
- 所有高时效内容带**最后核验日期**；
- 所有公式解释变量、单位、直觉、假设与局限，并声明其为近似模型。

---

## 5. 来源优先级

1. 原始论文（arXiv、OpenReview、会议论文）；
2. MLSys、OSDI、SOSP、NSDI、EuroSys、USENIX ATC、ISCA、HPCA、SC、SIGCOMM、NeurIPS、ICLR、ICML、ACL、EMNLP；
3. 官方技术报告、产品文档、模型卡、system card、官方研究博客；
4. 官方 GitHub repo、release、benchmark recipe、性能文档；
5. 芯片与云厂商官方资料；
6. MLPerf Inference 官方结果；
7. OCP、UCIe、PCI-SIG、JEDEC、OIF、Ethernet Alliance、UEC、IBTA 等标准组织资料；
8. 年报、10-K、20-F、季报、投资者资料、正式新闻稿；
9. 可信第三方 benchmark 与行业研究（**必须标记性质**）。

**不能单独作为关键事实依据：** 社交媒体、Reddit/论坛、聚合网站、无原始链接的图表、匿名爆料、无法确认版本与测试条件的 benchmark。

---

## 6. 披露等级标签（枚举，唯一合法取值）

```text
官方披露
技术文档披露
开源代码/配置披露
独立可复现实验
可信第三方估计
未公开
待核实
```

不得将"可信第三方估计"写成"官方披露"。

---

## 7. 必须标注"最后核验日期"的内容

模型版本、API 定价、云实例价格、推理引擎版本、GPU/ASIC 路线图、HBM 与网络规格、MLPerf 成绩、公司财报/融资/并购、新产品发布、政策与出口管制。

---

## 8. Git 规则

- 使用**单一开发分支**，不创建多 Agent branch，不创建并行 worktree；
- 每次 session 至少一个清晰 commit；
- commit message 使用**英文**；
- 不将未完成草稿当作完成内容提交；
- 提交前确保不破坏 INDEX、内部链接或 CSV schema；
- 每完成一个模块，更新 `CHANGELOG.md` 与 `INDEX.md` 中的模块状态（`待开始` / `进行中` / `已完成`）；
- 每完成若干关键文档，更新 `README.md` 的内容统计。

---

## 9. QA 门禁

提交前至少运行：

```bash
python3 scripts/validate_csv_schema.py
python3 scripts/validate_links.py
python3 scripts/word_count.py
```

涉及对应内容时追加运行：`check_required_sections.py`、`benchmark_audit.py`、`hardware_spec_audit.py`、`unit_consistency_audit.py`、`company_disclosure_audit.py`、`mermaid_audit.py`、`interview_coverage_report.py`、`freshness_report.py`、`paper_citation_audit.py`。

---

## 10. 当前阶段

见 `CHANGELOG.md` 顶部与 `INDEX.md` 的模块状态表。

---

## 11. 网络核验能力约束（环境相关，必读）

本项目的数据录入纪律要求**打开一手来源确认**（第 5 节）。但构建环境可能施加**出口白名单**，
使一手来源不可达。启动任何数据录入工作前，**必须先探测实际可达性**，不得假设。

### 探测方法

```bash
for h in arxiv.org export.arxiv.org www.usenix.org openreview.net proceedings.mlr.press \
         dl.acm.org huggingface.co mlcommons.org api.github.com raw.githubusercontent.com; do
  printf "%-32s %s\n" "$h" "$(curl -sS --max-time 12 -o /dev/null -w '%{http_code}' https://$h/ 2>/dev/null)"
done
```

`000` 或代理返回 `Host not in allowlist` 表示该域被组织级出口策略拒绝。

### 2026-07-29 实测结果（本仓库当前环境）

| 来源类型 | 代表域名 | 状态 | 影响的 CSV |
|---|---|---|---|
| 论文预印本 | `arxiv.org`、`export.arxiv.org` | **拒绝** | `papers.csv` |
| 会议论文 | `www.usenix.org`、`dl.acm.org`、`proceedings.mlr.press`、`openreview.net` | **拒绝** | `papers.csv` |
| 模型卡 | `huggingface.co` | **拒绝** | `models.csv` |
| 基准官方 | `mlcommons.org` | **拒绝** | `benchmarks.csv` |
| 芯片厂商 | `www.nvidia.com` 等 | **拒绝** | `accelerators.csv`、`server_platforms.csv` |
| 学术索引 | `semanticscholar.org` | **拒绝** | `papers.csv` |
| GitHub 网页/raw | `github.com`、`raw.githubusercontent.com` | 可达 | — |
| GitHub API | `api.github.com` | 可达但**仅限本 session 已授权仓库**；`add_repo` 不支持跨 owner 添加 | `inference_engines.csv` |

**结论**：在此环境下，`papers`、`models`、`accelerators`、`benchmarks`、
`networking_technologies`、`companies`、`cloud_pricing` 七个 CSV **无法按第 5 节纪律录入**。

### 受阻时的强制行为

**允许**：

1. 继续撰写以**可推导内容**为主的模块正文（原理、公式、框架、判据、失败模式）；
2. 在正文中把需要一手来源的具体数值标注为 `待核实`，并说明所需来源类型；
3. 使用 WebSearch 建立**方向性认识**，用于组织内容结构。

**禁止**：

1. **禁止**用搜索结果摘要、Medium/Wikipedia/ResearchGate/课程站镜像等二级来源，
   作为 `papers.csv` 等 CSV 的录入依据；
2. **禁止**在未打开一手来源的情况下把 `citation_status` 填为 `已核验`；
3. **禁止**凭记忆填写芯片规格、模型参数、benchmark 数字、公司财务或客户关系；
4. **禁止**为绕过出口策略而更换 UA、改用镜像站或其他规避手段
   （见 `/root/.ccr/README.md`：403/407 属组织策略拒绝，应上报而非绕行）。

### 解除阻塞的条件

需要环境所有者把以下域加入出口白名单，之后方可开展数据录入：

```text
arxiv.org, export.arxiv.org        # 论文元数据（API 形式最稳定）
www.usenix.org, dl.acm.org         # OSDI/SOSP/NSDI/ATC 会议论文
openreview.net, proceedings.mlr.press  # ICLR / ICML
huggingface.co                     # 模型卡（models.csv 的唯一权威来源）
mlcommons.org                      # MLPerf Inference 官方结果
各芯片与云厂商官网 + 投资者关系页    # accelerators / companies / cloud_pricing
JEDEC / OIF / UEC / PCI-SIG / OCP  # networking_technologies
```

在此之前，`INDEX.md` 与 `README.md` 的内容统计表中，上述 CSV 的目标值应视为**受阻**而非未开始。
