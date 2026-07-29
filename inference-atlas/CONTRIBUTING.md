# CONTRIBUTING — InferenceAtlas 贡献指南

在提交任何变更前，请先完整阅读 [AGENTS.md](AGENTS.md)。本文件是其面向贡献者的操作化补充。

---

## 1. 第一原则：单一 Agent、串行推进

本仓库**禁止**并行化构建。具体禁止事项见 [AGENTS.md](AGENTS.md) 第 1 节，包括但不限于 agent swarm、并行子 Agent、多 Agent 分工、并发 worktree、并行 branch、同时处理多个大型模块。

**一次贡献 = 一个明确工作包**：1 个模块，或一个模块中 2–4 篇紧密相关的文档。

---

## 2. 工作流程

```bash
# 1. 确认当前状态
git status && git log --oneline -5
cat CHANGELOG.md | head -30      # 上次做到哪
grep -n "待开始\|进行中" INDEX.md  # 下一个工作包

# 2. 阅读上下文
#    README.md → INDEX.md → 目标模块 README.md → GLOSSARY.md

# 3. 写作（见第 3 节规范）

# 4. 同步更新
#    - 模块 README 的文档清单与状态
#    - INDEX.md 的模块状态表（字数/表格/图示/最后更新）
#    - GLOSSARY.md 新术语
#    - 相关 data/*.csv
#    - CHANGELOG.md

# 5. QA
python3 scripts/validate_csv_schema.py && \
python3 scripts/validate_links.py && \
python3 scripts/word_count.py

# 6. 提交（英文 message）
git add -A && git commit -m "docs: <what you added>"
```

---

## 3. 写作规范

### 3.1 结构

核心文档必须使用 [`templates/chapter_template.md`](templates/chapter_template.md) 的骨架，包含全部必备章节：本章导读、学习目标、核心结论、问题定义、原理与性能模型、实现机制、trade-off、benchmark/案例、决策框架、失败模式、关联面试主题、小结、关键术语、延伸阅读、主要来源、更新记录。

由 `scripts/check_required_sections.py` 强制校验。

### 3.2 事实纪律

| 要求 | 说明 |
|---|---|
| 每个规格/性能/成本/市场数字都有来源 | 附可点击链接 |
| 每条此类陈述都有披露标签 | 7 档枚举，见 [README](README.md) 第 7 节 |
| 严格区分事实、估计与推论 | 推论必须显式写成"推论"并给出依据 |
| 严格区分理论峰值与实测 | 以及训练性能 vs 推理性能 |
| 严格区分 chip / board / server / rack 级功耗 | 不得跨级比较 |
| 不使用无来源绝对化表达 | "最快""最低成本""领先"等 |
| 未公开的信息写 `未公开` | **不得猜测填充** |
| 不大段复制受版权材料 | 做摘要、结构化与链接 |

### 3.3 数学

- 使用 LaTeX（GitHub 支持 `$...$` 与 `$$...$$`）；
- 每个公式必须解释：变量含义、单位、直觉、假设、局限；
- 成本与性能模型必须显式声明为**近似模型**，禁止产生伪精确结论（例如不要给出 `$0.0037421/1K tokens` 这类超出输入精度的结果）。

### 3.4 表格与图示

- 只创建有**实际比较价值**的表，不生成重复表；
- 每张 Mermaid 图前后必须说明：图展示什么、核心瓶颈是什么、图中的 trade-off、面试如何引用该图；
- Mermaid 使用 ` ```mermaid ` 代码块以便 GitHub 原生渲染。

### 3.5 链接

- 内部链接使用**相对路径**；
- 只链接**已存在**的文件；尚未创建的文档在导航中以 `代码体` 呈现文件名，避免死链；
- 由 `scripts/validate_links.py` 校验。

---

## 4. 数据录入规范

1. 先读对应的 [`data/schemas/*_schema.md`](data/schemas/)；
2. 必填字段不得留空；无信息时填 `未公开` 或 `待核实`；
3. 日期统一 `YYYY-MM-DD`；
4. URL 必须是 `https://` 开头的**一手来源**；
5. 枚举字段只能取 schema 中列出的值；
6. 含逗号的字段用双引号包裹；含分号分隔的多值字段使用 `;`；
7. 每条记录必须有 `last_verified_date`；
8. 新增论文同时补充 [`data/references.bib`](data/references.bib)。

由 `scripts/validate_csv_schema.py` 校验。

---

## 5. 提交前审阅清单

- [ ] 本次只推进了**一个**工作包
- [ ] 没有创建空文件或纯占位符文件
- [ ] 所有事实性数字有来源链接
- [ ] 所有相关陈述有披露标签
- [ ] 高时效内容有"最后核验"日期
- [ ] 公式解释了变量、单位、假设与局限
- [ ] 每张 Mermaid 图有前后文解释
- [ ] 新术语已进入 `GLOSSARY.md`
- [ ] 模块 README 与 `INDEX.md` 状态已更新
- [ ] `CHANGELOG.md` 已追加本次记录
- [ ] QA 最小门禁全部通过
- [ ] commit message 为英文且描述准确
- [ ] 未提交权重、数据集、二进制、密钥

---

## 6. Commit message 约定

```text
chore: <基础设施/工具链变更>
docs:  <文档内容变更>
data:  <结构化数据变更>
fix:   <修正错误事实、死链、schema 违规>
```

示例：

```text
chore: initialize InferenceAtlas single-agent research workflow
docs: add inference foundations and performance metrics
data: add validated accelerator and inference engine records
fix: correct KV cache capacity formula units in module 02
```

---

## 7. 报告问题

发现事实错误、失效链接、过时数据或口径不一致，请提交 issue 并附：所在文件与行号、你认为正确的内容、**一手来源链接**。事实性纠错优先于新增内容。
