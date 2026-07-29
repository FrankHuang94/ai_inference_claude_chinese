# ai_inference_claude_chinese

本仓库承载 **InferenceAtlas** —— 一个中文的 AI 推理知识数据库，覆盖模型服务、推理系统、芯片、网络、数据中心与产业战略。

## 👉 从这里开始

| 入口 | 说明 |
|---|---|
| **[inference-atlas/INDEX.md](inference-atlas/INDEX.md)** | **全库唯一入口**：完整导航、按系统层/workload/指标检索、快速路径 |
| [inference-atlas/README.md](inference-atlas/README.md) | 项目定位、读者画像、内容统计、披露等级说明、QA 运行方法 |
| [inference-atlas/GLOSSARY.md](inference-atlas/GLOSSARY.md) | 术语表与单位书写规范 |
| [inference-atlas/AGENTS.md](inference-atlas/AGENTS.md) | **构建协议：单一 Agent、串行、模块化** |
| [inference-atlas/CONTRIBUTING.md](inference-atlas/CONTRIBUTING.md) | 贡献指南 |
| [inference-atlas/CHANGELOG.md](inference-atlas/CHANGELOG.md) | 变更历史与当前阶段 |

## 构建模式

本项目采用**单一 Agent、串行、模块化**的长期构建模式，分多次 session 逐模块推进。
仓库**禁止** agent swarm、并行子 Agent、多 Agent 分工、并发 worktree 与并行 branch。
完整规则见 [AGENTS.md](inference-atlas/AGENTS.md)。

## 当前状态

**Phase 0 已完成**（基础设施初始化）。18 个内容模块状态均为 `待开始`。

## 免责声明

本项目仅供学习、研究、技术战略分析与投资尽调框架使用，**不构成投资建议**。
所有信息来自公开渠道并标注披露等级，可能存在错误或已过时。

## License

文本内容 CC BY 4.0，脚本代码 MIT。详见 [LICENSE](inference-atlas/LICENSE)。
