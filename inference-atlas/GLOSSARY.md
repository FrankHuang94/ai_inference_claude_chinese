# GLOSSARY — InferenceAtlas 术语表

> 最后更新：2026-07-29 ｜ 版本：v0.1.0
>
> 本表收录阅读本数据库所必需的核心术语。**每完成一个模块，必须将该模块新出现的重要术语补入本表**（见 [AGENTS.md](AGENTS.md) 第 3 节第 8 步）。
>
> 机器可读镜像见 [`data/glossary.csv`](data/glossary.csv)。Phase 0 阶段 CSV 仅含 1 条 schema 演示记录，完整同步随模块推进进行。

**口径纪律**：同一术语在不同 benchmark、不同厂商文档中可能定义不同。本表给出**本数据库统一采用的定义**；引用外部数据时若其定义不同，必须在该处显式说明。

---

## 1. 推理阶段与流程

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 推理 | inference | 使用已训练模型对新输入产生输出的过程；与 training 相对 | — |
| 预填充 | prefill | 自回归生成前，对整个输入 prompt 做一次并行 forward，产生首个输出 token 并填充 KV cache | — |
| 解码 | decode | prefill 之后逐 token 自回归生成的阶段，每步仅处理 1 个新 token | — |
| 自回归 | autoregressive | 每个输出 token 依赖此前所有 token 的生成方式 | — |
| 分词 | tokenization | 将文本切分为模型词表单元的过程 | token |
| 流式返回 | streaming | 边生成边返回 token，而非等待完整响应 | — |

## 2. 时延与吞吐指标

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 首 token 时延 | TTFT (time to first token) | 从请求到达到**首个输出 token 返回给客户端**的时间；本库口径**包含**排队与 tokenization | ms |
| 每输出 token 时延 | TPOT (time per output token) | 首 token 之后，平均每个输出 token 的生成时间 | ms/token |
| token 间隔 | ITL (inter-token latency) | 相邻两个输出 token 返回时刻的间隔；与 TPOT 口径接近但为**逐次测量的分布**而非均值 | ms |
| 端到端时延 | end-to-end latency | 请求到达至完整响应结束 | ms |
| 吞吐 | throughput | 单位时间产出的 token 或请求数；必须注明是 output token 还是 total token | tokens/s、req/s |
| 有效吞吐 | goodput | **满足 SLO 的**请求所贡献的吞吐；必须给出所用 SLO 定义 | tokens/s、req/s |
| 并发 | concurrency | 系统中同时在处理（含排队）的请求数 | 个 |
| 排队时延 | queue delay | 请求到达至开始被服务的时间 | ms |
| 尾时延 | tail latency | 分布高分位处的时延，通常指 P95/P99/P99.9 | ms |

## 3. KV Cache 与注意力

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| KV 缓存 | KV cache | 缓存已计算 token 的 Key/Value 张量，避免 decode 每步重算全序列 attention | GB（须注明 GB 还是 GiB） |
| 分页注意力 | PagedAttention | 以固定大小 block 分页管理 KV 内存、消除碎片的机制 | — |
| 前缀缓存 | prefix caching | 复用多个请求共享前缀的 KV cache | 命中率 % |
| 多头注意力 | MHA (multi-head attention) | 每个 query head 拥有独立的 K/V head | — |
| 多查询注意力 | MQA (multi-query attention) | 所有 query head 共享单组 K/V，大幅压缩 KV 体积 | — |
| 分组查询注意力 | GQA (grouped-query attention) | 若干 query head 共享一组 K/V，介于 MHA 与 MQA 之间 | — |
| 多头潜在注意力 | MLA (multi-head latent attention) | 将 K/V 压缩到低维潜空间以减少 cache 体积的注意力变体 | — |
| 驱逐 | eviction | 显存不足时移除部分 KV cache 条目 | — |
| 卸载 | offload | 将 KV cache 或权重迁移到 CPU 内存、NVMe 或远端内存 | — |

## 4. 调度与服务

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 静态批处理 | static batching | 固定批大小，等齐后统一执行 | — |
| 动态批处理 | dynamic batching | 在时间窗口内动态聚合请求成批 | — |
| 连续批处理 | continuous batching | 在**迭代粒度**上进出请求，完成的请求立即离开、新请求立即加入 | — |
| 分块预填充 | chunked prefill | 将长 prompt 的 prefill 切分为多块，与 decode 交错执行以抑制干扰 | — |
| 准入控制 | admission control | 在过载时拒绝或延迟接纳请求以保护 SLO | — |
| 背压 | backpressure | 将下游拥塞信号回传上游以限制进入速率 | — |
| 队头阻塞 | head-of-line blocking | 队首长请求阻塞其后短请求 | — |
| 服务级目标 | SLO (service level objective) | 内部设定的性能/可用性目标（如 P99 TTFT < X ms） | — |
| 服务级协议 | SLA (service level agreement) | 对外承诺的、带违约后果的服务标准 | — |
| 错误预算 | error budget | `1 − SLO` 允许的失败额度 | % 或时间 |

## 5. 并行与分布式

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 张量并行 | TP (tensor parallel) | 将单层权重沿维度切分到多个加速器，每层需要集合通信 | — |
| 流水线并行 | PP (pipeline parallel) | 将模型按层切分到多个加速器，形成流水线 | — |
| 上下文并行 | CP (context parallel) | 沿序列维度切分以支持超长上下文 | — |
| 专家并行 | EP (expert parallel) | 将 MoE 的专家分布到多个加速器 | — |
| 混合专家 | MoE (mixture of experts) | 每 token 仅激活部分专家的稀疏架构 | — |
| 全互换 | all-to-all | MoE dispatch/combine 阶段的集合通信原语 | — |
| 解耦式服务 | disaggregated serving | 将 prefill 与 decode 分配到独立资源池 | — |
| 纵向扩展 | scale-up | 在单一高带宽域内增加加速器（如 NVLink 域） | — |
| 横向扩展 | scale-out | 通过集群网络连接更多节点 | — |

## 6. 硬件与内存

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 高带宽内存 | HBM (high bandwidth memory) | 通过 2.5D/3D 封装堆叠、提供高带宽的 DRAM | 容量 GB；带宽 TB/s |
| 内存墙 | memory wall | 算力增速快于内存带宽增速导致的瓶颈 | — |
| 算术强度 | arithmetic intensity | 每字节内存访问对应的浮点运算数 | FLOP/byte |
| Roofline | roofline model | 由峰值算力与带宽共同界定可达性能的性能模型 | — |
| 计算受限 | compute-bound | 性能受峰值算力限制 | — |
| 内存受限 | memory-bound | 性能受内存带宽限制；LLM decode 阶段通常属此类 | — |
| 峰值算力 | peak compute | 理论最大算力，**非**实测性能 | TFLOPS / TOPS（须注明精度） |
| 热设计功耗 | TDP | 散热设计功耗；须区分 chip / board / server / rack 级 | W / kW |

## 7. 精度与量化

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 量化 | quantization | 用低位宽数值表示权重和/或激活以降低显存与带宽需求 | bit |
| 仅权重量化 | weight-only quantization | 只量化权重，激活保持较高精度 | — |
| 逐张量/逐通道/逐组 | per-tensor / per-channel / per-group | 量化缩放因子的粒度 | — |
| 校准 | calibration | 用样本数据确定量化参数的过程 | — |
| 离群值 | outlier | 激活中数值远大于主体分布的元素，是量化质量损失的主因之一 | — |

## 8. 解码算法

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 贪心解码 | greedy decoding | 每步取概率最大 token | — |
| 温度 | temperature | 调节采样分布平滑度的参数 | 无量纲 |
| 核采样 | top-p / nucleus sampling | 在累积概率达 p 的最小候选集中采样 | 无量纲 |
| 投机解码 | speculative decoding | 用小 draft 模型批量提议、大 target 模型并行验证，以减少 target 前向次数 | — |
| 接受率 | acceptance rate | draft 提议被 target 接受的比例，决定投机解码实际收益 | % |
| 约束解码 | constrained decoding | 用语法/schema 限制输出空间（如 JSON mode） | — |
| 测试时计算 | test-time compute | 推理阶段额外投入的计算（更长思考、多次采样、搜索、验证） | token 或 FLOP |

## 9. 成本与能耗

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 单 token 成本 | cost per token | 交付每个 token 的摊销成本；须声明包含与不包含的成本项 | $/1M tokens |
| 总拥有成本 | TCO (total cost of ownership) | 含硬件、电力、网络、软件、运维、折旧的综合成本 | $ |
| 每 token 焦耳 | J/token | 生成单个 token 消耗的能量；须注明测量边界（chip/node/rack/facility） | J |
| 电能使用效率 | PUE (power usage effectiveness) | 设施总耗电 / IT 设备耗电 | 无量纲，≥1 |
| 利用率 | utilization | 资源被有效使用的比例；须注明是加速器占用率还是有效算力利用率 | % |

## 10. 数据质量与披露

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 披露等级 | disclosure level | 本库对信息来源可信度的分级标签（7 档，见 [README](README.md) 第 7 节） | 枚举 |
| 官方披露 | official disclosure | 厂商/机构官方渠道直接陈述的信息 | — |
| 可信第三方估计 | credible third-party estimate | 有方法论说明的第三方研究，**不等于**官方确认 | — |
| 未公开 | not disclosed | 厂商未公开该项信息；**不得猜测填充** | — |
| 可复现性等级 | reproducibility level | benchmark 是否提供足以复现的完整配置 | 枚举 |

---

## 单位书写规范（强制）

| 规范 | 说明 |
|---|---|
| GB vs GiB | 明确区分 10⁹ 与 2³⁰；显存容量通常厂商标称 GB，实际可用需说明 |
| TB/s vs Tb/s | 大写 B 为字节，小写 b 为比特；内存带宽用 TB/s，网络链路速率用 Gb/s 或 Tb/s |
| TFLOPS vs TOPS | 浮点用 FLOPS 并注明精度（如 BF16 TFLOPS）；整数用 TOPS 并注明位宽（如 INT8 TOPS） |
| W vs kW | chip/board 级用 W，rack/facility 级用 kW 或 MW，须注明边界 |
| $/hour vs $/token vs $/1M tokens | 三者不可混用；换算须给出利用率与吞吐假设 |
| P50/P95/P99 | 分位数必须与样本量、观测窗口一同给出 |

违反上述规范由 `scripts/unit_consistency_audit.py` 检出。
