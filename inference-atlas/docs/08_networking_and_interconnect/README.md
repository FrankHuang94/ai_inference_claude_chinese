# 模块 08 — 网络、互连与光学

> 位置：[InferenceAtlas](../../INDEX.md) > 当前模块
> 状态：**待开始**
> 模块目标字数：**≥ 15,000 字**
> 最后更新：2026-07-29

## 模块定位

推理网络的需求与训练网络显著不同：训练关心大规模同步集合通信的带宽，推理关心**每个 token 关键路径上的小消息时延与抖动**。本模块覆盖从 die-to-die 到跨数据中心的完整互连层次，并要求明确回答"何时网络是瓶颈、何时不是"。

## 前置阅读

[模块 06](../06_distributed_and_moe_inference/)、[模块 07](../07_hardware_and_server_architecture/)

## 规划文档

> 尚未创建的文档以 `代码体` 列出，避免死链。完成后改为链接并更新状态。

| # | 文档 | 一句话说明 | 状态 |
|---:|---|---|---|
| 01 | `01_inference_networking_overview.md` | 从 die-to-die 到跨数据中心的互连层次 | 待开始 |
| 02 | `02_pcie_cxl_nvlink_nvswitch.md` | 节点内与 scale-up 互连 | 待开始 |
| 03 | `03_infiniband_for_ai_inference.md` | InfiniBand 在推理集群中的角色 | 待开始 |
| 04 | `04_ethernet_roce_and_ultra_ethernet.md` | 以太网、RoCE 与 Ultra Ethernet | 待开始 |
| 05 | `05_collectives_rdma_and_communication_libraries.md` | 集合通信、RDMA 与通信库 | 待开始 |
| 06 | `06_scale_up_vs_scale_out.md` | scale-up 与 scale-out 的决策框架 | 待开始 |
| 07 | `07_network_topologies_fat_tree_dragonfly_rail_optimized.md` | 拓扑设计与 rail 优化 | 待开始 |
| 08 | `08_optical_transceivers_aec_dac_and_cpo.md` | DAC/AEC/可插拔光模块与 CPO | 待开始 |
| 09 | `09_optical_switching_and_photonic_interconnect.md` | 光交换与光子互连 | 待开始 |
| 10 | `10_network_congestion_tail_latency_and_qos.md` | 拥塞控制、incast 与 tail latency | 待开始 |
| 11 | `11_network_observability_and_debugging.md` | 网络可观测性与排查 | 待开始 |
| 12 | `12_inference_network_case_studies.md` | 公开推理网络案例 | 待开始 |

## 写作要求

1. **层次**：on-package、die-to-die、chiplet、board、server、rack、cluster、datacenter、inter-datacenter
2. **技术**：PCIe、CXL、NVLink、NVSwitch、Infinity Fabric、UALink、InfiniBand、Ethernet、RoCE、RDMA、Ultra Ethernet、NIC、DPU、switch ASIC；congestion control、ECN、PFC、DCQCN；collective communication；rail-optimized、fat-tree、dragonfly、Clos；DAC、AEC、pluggable optics、co-packaged optics、optical circuit switching、silicon photonics
3. **推理特有网络需求**：TP、EP、KV transfer、prefill/decode disaggregation 的网络模式；推理与训练网络流量的区别；tail latency、microburst、incast、noisy neighbor、remote KV、multi-region routing；bandwidth/latency/jitter 的 trade-off；network observability；**何时网络不是瓶颈、何时成为瓶颈**
4. 所有链路速率必须区分 Gb/s 与 GB/s；所有标准引用须指向标准组织官方资料

## 完成标准

- [ ] 全部规划文档已按 [`templates/chapter_template.md`](../../templates/chapter_template.md) 完成
- [ ] 模块正文合计 ≥ 15,000 字
- [ ] 上述"写作要求"逐条覆盖
- [ ] 所有事实性数字带来源链接与披露标签
- [ ] 新术语已补入 [`GLOSSARY.md`](../../GLOSSARY.md)
- [ ] 相关 [`data/`](../../data/) CSV 已更新
- [ ] 本 README 的文档状态与 [`INDEX.md`](../../INDEX.md) 模块状态表已同步
- [ ] QA 门禁通过（见 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 第 2 节）

## 工作节奏

按 [AGENTS.md](../../AGENTS.md) 规定，本模块须分多次 session 完成，
**每次 session 只推进 2–4 篇紧密相关的文档**，完成后提交 commit 并停止。
