# 模块 09 — 数据中心、电力、散热与运维

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**进行中（4/10 篇）**
> 模块目标字数：**≥ 10,000 字**
> 最后更新：2026-07-29

## 模块定位

AI 数据中心的机架功率密度已远超传统云机房，供电与散热从后台约束变成了**决定可交付 token 数的一线变量**。本模块要求把机房设计明确连接到业务指标：power cap 如何压制 tokens/s，thermal throttling 如何抬高 P99，机架密度如何决定扩容速度。

## 前置阅读

[模块 07](../07_hardware_and_server_architecture/)、[模块 08](../08_networking_and_interconnect/)

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | [01_ai_datacenter_overview.md](01_ai_datacenter_overview.md) | AI 数据中心与传统数据中心的差异 | 已完成 |
| 02 | [02_rack_power_and_density.md](02_rack_power_and_density.md) | 机架功率密度与扩容速度 | 已完成 |
| 03 | [03_power_delivery_48v_and_busbar.md](03_power_delivery_48v_and_busbar.md) | 配电链路：电压、母线与转换损耗 | 已完成 |
| 04 | [04_cooling_air_direct_liquid_and_immersion.md](04_cooling_air_direct_liquid_and_immersion.md) | 风冷、冷板液冷与浸没式散热 | 已完成 |
| 05 | `05_power_usage_effectiveness_and_energy_modeling.md` | PUE/WUE 与能耗建模 | 待开始 |
| 06 | `06_cluster_capacity_and_site_planning.md` | 集群容量与选址规划 | 待开始 |
| 07 | `07_reliability_redundancy_and_maintenance.md` | 冗余、可维护性与 RAS | 待开始 |
| 08 | `08_storage_logging_and_data_plane.md` | 存储、日志与数据面 | 待开始 |
| 09 | `09_security_compliance_and_data_residency.md` | 安全、合规与数据驻留 | 待开始 |
| 10 | `10_operations_case_studies.md` | 运维案例研究 | 待开始 |

## 写作要求

1. **覆盖**：AI 数据中心与传统数据中心差异；rack density；power delivery；48V；busbar；PSU；voltage regulation；UPS；generator；grid interconnection；air cooling；direct liquid cooling；cold plate；CDU；immersion；PUE；WUE；capacity planning；maintenance；spare；RAS；firmware；telemetry；security；compliance；data residency；multi-region disaster recovery
2. **必须把机房设计连接到推理业务指标**：power cap 对 tokens/s 的影响；thermal throttling 对 P99 的影响；rack density 对扩容速度的影响；maintainability 对 availability 的影响；power/cooling 对 cost/token 的影响
3. 功率单位必须注明边界（chip/rack/room/facility）；PUE 必须注明测量方法与季节性

## 完成标准

- [ ] 全部规划文档已按 [`templates/chapter_template.md`](../../templates/chapter_template.md) 完成
- [ ] 模块正文合计 ≥ 10,000 字
- [ ] 上述"写作要求"逐条覆盖
- [ ] 所有事实性数字带来源链接与披露标签
- [ ] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md)
- [ ] 相关 [`data/`](../../data/) CSV 已更新
- [ ] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [ ] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
