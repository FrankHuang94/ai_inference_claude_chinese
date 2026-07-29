# 指标、单位与速查参考

> 位置：[InferenceAtlas](../../INDEX.md) > [模块 00](README.md) > 当前文档
> 信息截至：2026-07-29 ｜ 最后核验：2026-07-29 ｜ 内容版本：v0.1
> 时效性等级：低
> 相关主题：[指标与排队论](../01_foundations_and_metrics/)｜[术语表](../../GLOSSARY.md)｜[如何读 benchmark](03_how_to_read_inference_benchmarks.md)

> **本文档定位**：速查表，非教学章节。所有条目的推导与讨论见对应模块。适合打印或在面试前快速过一遍。

---

## 1. 时延指标

| 指标 | 定义 | 单位 | 本库口径 | 最常见的口径分歧 |
|---|---|---|---|---|
| **TTFT** | 请求到达 → 首个 token 返回客户端 | ms | **含**排队与 tokenization | 部分来源从「开始 prefill」计时，不含排队 |
| **TPOT** | 首 token 后平均每 token 生成时间 | ms/token | $(T_{E2E} - \text{TTFT}) / (N_{out}-1)$ | 分母用 $N_{out}$ 还是 $N_{out}-1$ |
| **ITL** | 相邻两 token 返回时刻的间隔 | ms | 逐次测量的**分布**，非均值 | 常被与 TPOT 混用 |
| **端到端时延** | 请求到达 → 完整响应结束 | ms | 含全部六段 | 是否含客户端网络 |
| **排队时延** | 请求到达 → 开始被服务 | ms | — | 是否含准入控制耗时 |

**时延分解**：

$$
T_{E2E} = T_{queue} + T_{tokenize} + T_{prefill} + T_{decode} + T_{network} + T_{post}
$$

**报告纪律**：任何时延数字必须附**分位数 + 样本量 + 观测窗口**。只给均值等于没给。

---

## 2. 吞吐与容量指标

| 指标 | 定义 | 单位 | 陷阱 |
|---|---|---|---|
| **吞吐** | 单位时间产出 token 数 | tokens/s | **必须注明是 output token 还是 total token**，二者可差约 2 倍 |
| **请求吞吐** | 单位时间完成的请求数 | req/s | 受输出长度分布影响极大 |
| **Goodput** | 满足 SLO 的请求所贡献的吞吐 | tokens/s | **必须同时给出 SLO 定义**，否则不可比 |
| **并发** | 系统中同时处理（含排队）的请求数 | 个 | 与 batch size 不同 |
| **Batch size** | 单次迭代实际同时计算的序列数 | 个 | continuous batching 下随迭代变化 |

**关系**（Little's Law）：

$$
L = \lambda W
$$

$L$ = 系统内平均请求数，$\lambda$ = 到达率（req/s），$W$ = 平均逗留时间（s）。

---

## 3. 资源指标

| 指标 | 单位 | 口径要点 |
|---|---|---|
| 加速器利用率 | % | **注意区分**「有 kernel 在跑」与「算力被有效利用」，前者常虚高 |
| 显存占用 | GB / GiB | 明确进制；区分权重 / KV / 运行时开销 |
| 显存带宽利用率 | % | decode 阶段的关键指标，比算力利用率更能说明问题 |
| KV cache 占用率 | % | 接近 100% 时会触发抢占与重算 |
| 前缀命中率 | % | 直接影响 TTFT，必须与 cache 状态一起报告 |
| 队列深度 | 个 | tail latency 的先行指标 |
| 抢占/重算次数 | 次/s | cache thrashing 的直接证据 |

---

## 4. 成本与能耗指标

| 指标 | 单位 | 口径要点 |
|---|---|---|
| 单 token 成本 | **$/1M tokens** | 不要用 $/token（易伪精确）；须声明含哪些成本项 |
| 单请求成本 | $ | 受输出长度分布影响 |
| TCO | $ | 含硬件、电力、网络、软件、运维、折旧 |
| 每 token 能耗 | J/token | **必须注明测量边界**：chip / node / rack / facility |
| 功率 | W / kW / MW | 同上，注明层级 |
| PUE | 无量纲，≥1 | 设施总耗电 ÷ IT 设备耗电；注明测量方法与季节 |

**成本模型**：

$$
\text{Cost per Token} = \frac{C_{accel} + C_{power} + C_{network} + C_{software} + C_{ops}}{\text{Delivered Tokens}}
$$

**关键**：分母是**实际交付**的 token，因此利用率直接进入成本。利用率 30% 时单位成本约为满载的 3 倍。

---

## 5. 硬件与性能模型

**Roofline**：

$$
\text{Attainable} = \min(\text{Peak Compute},\ I \times BW)
$$

$I$ = 算术强度（FLOP/byte），$BW$ = 显存带宽（byte/s）。

**硬件平衡点**：$I^* = \text{Peak Compute} / BW$。当 $I < I^*$ 时为 memory-bound。

| 阶段 | 算术强度 | 通常瓶颈 | 决定指标 |
|---|---|---|---|
| Prefill | 高 | 峰值算力 | TTFT |
| **Decode** | **低** | **显存带宽** | TPOT |

---

## 6. KV Cache 速查

$$
M_{KV} \approx 2 \times L \times B \times S \times H_{KV} \times D_h \times b
$$

| 符号 | 含义 | 典型影响 |
|---|---|---|
| $L$ | 层数 | 线性 |
| $B$ | 并发序列数 | 线性 |
| $S$ | 缓存 token 数 | 线性 |
| $H_{KV}$ | KV head 数 | 线性；**GQA/MQA 在此处压缩** |
| $D_h$ | head 维度 | 线性 |
| $b$ | 每元素字节数 | 线性；**KV 量化在此处压缩** |
| 系数 2 | K 与 V | — |

**注意**：教学近似。真实占用还受 block 粒度、对齐、padding、元数据、共享与 TP 分片影响。

**KV 压缩手段对照**：

| 手段 | 作用于 | 质量影响 |
|---|---|---|
| MQA | $H_{KV} \to 1$ | 需在预训练时选择 |
| GQA | $H_{KV}$ 减小为组数 | 需在预训练时选择 |
| MLA | 低维潜表示 | 需在预训练时选择 |
| KV 量化 | $b$ 减小 | 可能有质量损失，需评测 |
| 驱逐/滑窗 | $S$ 减小 | 丢失远端上下文 |
| 前缀共享 | 有效 $B$ 减小 | 无（相同前缀） |

---

## 7. 单位书写规范（强制）

| 易混对 | 区分 |
|---|---|
| **GB vs GiB** | $10^9$ vs $2^{30}$；差约 7.4% |
| **TB/s vs Tb/s** | 大写 B = 字节，小写 b = 比特；**内存带宽用 TB/s，网络链路用 Gb/s 或 Tb/s** |
| **TFLOPS vs TOPS** | 浮点用 FLOPS 并注明精度；整数用 TOPS 并注明位宽 |
| **峰值 vs 实测** | 峰值属规格，实测属 benchmark，不可混列 |
| **训练 vs 推理性能** | 不可互相论证 |
| **W vs kW vs MW** | 注明 chip / board / server / rack / facility 层级 |
| **$/hour vs $/1M tokens** | 换算须给出利用率与吞吐假设 |
| **P50/P95/P99** | 必须附样本量与观测窗口 |

由 [`scripts/unit_consistency_audit.py`](../../scripts/unit_consistency_audit.py) 检查。

---

## 8. 症状 → 排查层 速查

| 症状 | 首查 | 次查 | 常见根因 |
|---|---|---|---|
| TTFT 高、TPOT 正常 | 队列深度 | prefill 耗时、输入长度分布 | 排队积压；长 prompt 未分块 |
| TPOT 高、TTFT 正常 | 显存带宽利用率 | batch 大小、量化配置 | decode 批太小；kernel 慢路径 |
| 均值正常、P99 差 | ITL 分布 | 抢占/重算次数 | 批内长短干扰；KV 显存不足 |
| 吞吐随并发上升后骤降 | KV 占用率 | 抢占率 | cache thrashing |
| 吞吐低且利用率也低 | 调度器组批 | 到达模式 | 静态批处理；组批窗口不当 |
| 时延周期性尖峰 | autoscaler 事件 | 模型加载耗时 | 冷启动；权重分发慢 |
| 多租户互相影响 | 优先级与配额 | 批内混合 | 缺隔离与准入控制 |
| 分布式下 TPOT 异常 | 集合通信耗时 | 网络 incast、拓扑映射 | TP 通信在关键路径 |
| 长时间运行后变慢 | 温度与功耗 | 频率曲线 | thermal throttling / power cap |

---

## 9. Benchmark 审读清单（20 项）

模型名称 · 模型版本/checkpoint · 模型参数化 · **量化方案** · 硬件型号 · **加速器数量** · 网络配置 · **软件栈版本** · **输入长度** · **输出长度** · **batch/并发** · warmup 方式 · **cache 状态** · tokenizer · 是否流式 · **时延指标定义** · **吞吐定义** · **分位数与样本量** · 功耗测量边界 · 成本口径与利用率假设

**判据**：任一项缺失 → 不可跨来源比较。详见 [03 如何读 benchmark](03_how_to_read_inference_benchmarks.md)。

---

## 10. 披露等级速查

| 标签 | 可用于 |
|---|---|
| `官方披露` | 决策依据（注意选择性披露） |
| `技术文档披露` | 决策依据 |
| `开源代码/配置披露` | 可核实性最高 |
| `独立可复现实验` | 跨厂商比较的最佳依据 |
| `可信第三方估计` | **仅建立量级感，非事实** |
| `未公开` | 提醒：此处空白是真实的，不要用常识补 |
| `待核实` | 待办，不可引用 |

---

## 11. 设计九步速查

1. workload 画像（分布，非均值） → 2. SLO（分位数） → 3. **KV 显存反推硬件** → 4. 并行策略（"装不下"驱动） → 5. 调度策略 → 6. 精度 → 7. 是否分离 prefill/decode → 8. 可观测性 → 9. **降级路径**

详见 [04 如何设计一个推理系统](04_how_to_design_an_inference_system.md)。

---

## 12. 回答结构速查（面试）

结论（15s） → 原理（45s） → 路径（90s） → trade-off（45s） → 案例（30s） → **局限（30s）**

详见 [05 如何准备推理岗位面试](05_how_to_prepare_for_inference_interviews.md)。

---

## 主要来源

本速查表汇总本库其他文档的定义与结论，其外部来源见对应章节：

| 内容 | 来源文档 |
|---|---|
| 时延分解、prefill/decode 画像、排查表 | [02 端到端生命周期](02_end_to_end_inference_lifecycle.md) |
| Benchmark 审读清单、Roofline 讨论 | [03 如何读 benchmark](03_how_to_read_inference_benchmarks.md) |
| 设计九步 | [04 系统设计方法论](04_how_to_design_an_inference_system.md) |
| 回答结构 | [05 面试准备](05_how_to_prepare_for_inference_interviews.md) |
| 单位规范、术语定义 | [GLOSSARY](../../GLOSSARY.md) |

## 更新记录

| 日期 | 版本 | 变更 | 核验人 |
|---|---|---|---|
| 2026-07-29 | v0.1 | 初稿 | — |
