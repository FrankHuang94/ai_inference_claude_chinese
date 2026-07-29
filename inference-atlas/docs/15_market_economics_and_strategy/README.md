# 模块 15 — 市场、经济学与战略

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**待开始**
> 模块目标字数：**≥ 16,000 字**
> 最后更新：2026-07-29

## 模块定位

本模块把技术栈翻译成价值链：每一层的成本结构、价值捕获能力与竞争壁垒。它服务于技术战略与投资尽调，但**不构成投资建议**。所有市场、财务、capex、估值、订单与客户采用率数字必须带来源和披露标签。

## 前置阅读

[模块 07](../07_hardware_and_server_architecture/)、[模块 14](../14_company_and_ecosystem_landscape/)

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | `01_ai_inference_value_chain.md` | 推理价值链与价值捕获环节 | 待开始 |
| 02 | `02_inference_tam_and_workload_growth.md` | 推理 TAM 与工作负载增长 | 待开始 |
| 03 | `03_cloud_api_and_enterprise_pricing.md` | API 与企业定价结构 | 待开始 |
| 04 | `04_cost_per_token_and_tco.md` | cost/token 与 TCO | 待开始 |
| 05 | `05_gpu_asic_and_system_economics.md` | GPU/ASIC 与系统经济性 | 待开始 |
| 06 | `06_memory_networking_and_optics_value_capture.md` | 内存、网络与光学的价值捕获 | 待开始 |
| 07 | `07_hyperscaler_capex_and_custom_silicon.md` | 超大规模厂商 capex 与自研芯片 | 待开始 |
| 08 | `08_neocloud_and_gpu_as_a_service.md` | neocloud 与 GPUaaS | 待开始 |
| 09 | `09_open_vs_closed_models_and_margin_structure.md` | 开源与闭源模型的利润结构 | 待开始 |
| 10 | `10_company_financials_and_kpis.md` | 公司财务与 KPI | 待开始 |
| 11 | `11_mna_funding_and_partnerships.md` | 并购、融资与合作 | 待开始 |
| 12 | `12_geopolitics_export_controls_and_supply_chain.md` | 地缘政治、出口管制与供应链 | 待开始 |
| 13 | `13_investment_diligence_framework.md` | 投资尽调框架 | 待开始 |
| 14 | `14_bull_base_bear_scenarios.md` | 多空情景分析 | 待开始 |

## 写作要求

1. **价值链**：API、serving software、GPU、ASIC、HBM、packaging、server、NIC、switch、optics、fiber、power、cooling、cloud、neocloud、enterprise、edge、developer platform
2. **必须讨论**：API pricing；token pricing；input/output economics；reasoning 的 test-time compute 成本；reserved capacity；on-demand；serverless；GPU-as-a-service；utilization；idle capacity；depreciation；energy；networking；software；support；gross margin；TCO；cloud vs on-prem；custom silicon vs merchant GPU；open vs closed model；edge displacement
3. **投资尽调框架必须包括**：技术、产品、benchmark、客户、供应链、单位经济性、竞争、技术壁垒、估值变量、bull/base/bear scenario、催化剂、风险、**反证指标**
4. **所有市场、财务、capex、估值、订单、客户采用率数字必须带来源和披露标签**
5. 每篇文档必须重申免责声明：不构成投资建议

## 完成标准

- [ ] 全部规划文档已按 [`templates/chapter_template.md`](../../templates/chapter_template.md) 完成
- [ ] 模块正文合计 ≥ 16,000 字
- [ ] 上述"写作要求"逐条覆盖
- [ ] 所有事实性数字带来源链接与披露标签
- [ ] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md)
- [ ] 相关 [`data/`](../../data/) CSV 已更新
- [ ] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [ ] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
