# 模块 14 — 公司与生态

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**待开始**
> 模块目标字数：**≥ 20,000 字**
> 最后更新：2026-07-29

## 模块定位

本模块基于**公开资料**梳理推理产业的参与者与竞争格局。最高优先级的纪律是：把事实、第三方估计与本库推论三者严格分开标注。在缺乏可靠来源时，任何关于公司内部基础设施、客户关系或财务细节的猜测都被禁止。

## 前置阅读

[模块 07](../07_hardware_and_server_architecture/)、[模块 08](../08_networking_and_interconnect/)、[模块 12](../12_open_source_deployment_and_reproduction/)

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | `01_landscape_overview.md` | 推理产业生态全景 | 待开始 |
| 02 | `02_nvidia.md` | NVIDIA 深度档案 | 待开始 |
| 03 | `03_amd.md` | AMD 深度档案 | 待开始 |
| 04 | `04_intel.md` | Intel 深度档案 | 待开始 |
| 05 | `05_google.md` | Google 深度档案 | 待开始 |
| 06 | `06_aws.md` | AWS 深度档案 | 待开始 |
| 07 | `07_microsoft_azure.md` | Microsoft Azure 深度档案 | 待开始 |
| 08 | `08_meta.md` | Meta 深度档案 | 待开始 |
| 09 | `09_openai.md` | OpenAI 深度档案 | 待开始 |
| 10 | `10_anthropic.md` | Anthropic 深度档案 | 待开始 |
| 11 | `11_xai.md` | xAI 深度档案 | 待开始 |
| 12 | `12_deepseek.md` | DeepSeek 深度档案 | 待开始 |
| 13 | `13_alibaba_qwen.md` | Alibaba / Qwen 深度档案 | 待开始 |
| 14 | `14_huawei.md` | Huawei 深度档案 | 待开始 |
| 15 | `15_qualcomm.md` | Qualcomm 深度档案 | 待开始 |
| 16 | `16_groq.md` | Groq 深度档案 | 待开始 |
| 17 | `17_cerebras.md` | Cerebras 深度档案 | 待开始 |
| 18 | `18_sambanova.md` | SambaNova 深度档案 | 待开始 |
| 19 | `19_dmatrix.md` | d-Matrix 深度档案 | 待开始 |
| 20 | `20_etched.md` | Etched 深度档案 | 待开始 |
| 21 | `21_tenstorrent.md` | Tenstorrent 深度档案 | 待开始 |
| 22 | `22_broadcom_and_marvell.md` | Broadcom 与 Marvell 深度档案 | 待开始 |
| 23 | `23_cloud_neocloud_and_gpu_service_providers.md` | 云与 neocloud 供应商 | 待开始 |
| 24 | `24_inference_software_companies.md` | 推理软件公司 | 待开始 |
| 25 | `25_ecosystem_comparison.md` | 生态横向对比 | 待开始 |

## 写作要求

1. **至少完成 30 家组织深度档案**，每份 1,200–2,000 中文字
2. **统一结构**：一句话定位 / 公司历史与组织定位 / 推理相关产品、服务和路线 / 模型、应用或客户工作负载 / 芯片、硬件、服务器或基础设施战略 / Runtime、compiler、software 与生态策略 / 网络、数据中心、云或边缘战略 / 公开性能主张与证据质量 / 商业模式与单位经济性 / 战略合作、供应链与客户 / 技术优势 / 风险、限制与竞争压力 / 应重点追踪的公开信号 / 同业对比 / 主要来源与更新记录（模板见 [`templates/company_profile_template.md`](../../templates/company_profile_template.md)）
3. **每 session 深度完成 1–2 家**，并同步更新 [`data/companies.csv`](../../data/companies.csv)
4. **必须把事实、估计和推论分开**；不得将媒体报道或匿名爆料写成官方确认；不得在无可靠来源时编造任何公司内部推理基础设施细节
5. 所有客户关系、融资、财务、市场份额陈述必须带官方或可核验来源链接与披露标签

## 完成标准

- [ ] 全部规划文档已按 [`templates/chapter_template.md`](../../templates/chapter_template.md) 完成
- [ ] 模块正文合计 ≥ 20,000 字
- [ ] 上述"写作要求"逐条覆盖
- [ ] 所有事实性数字带来源链接与披露标签
- [ ] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md)
- [ ] 相关 [`data/`](../../data/) CSV 已更新
- [ ] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [ ] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
