# GLOSSARY — InferenceAtlas 术语表

> 最后更新：2026-07-31 ｜ 版本：v0.1.0
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

## 11. 性能建模与设计方法

> 本节随 [模块 00](docs/00_start_here/) 完成新增。

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 硬件平衡点 | machine balance point | 峰值算力与显存带宽之比 $I^*=\text{Peak}/BW$；workload 算术强度低于此值即为 memory-bound | FLOP/byte |
| 可行边界 | feasible frontier | 显存约束下并发数与上下文长度的可行组合曲线 | — |
| 突发比 | burst ratio | 峰值负载与平均负载之比，容量规划的关键输入 | 无量纲 |
| 抢占重算 | preemption and recompute | KV 显存不足时驱逐序列并在恢复时重算其 cache | 次/s |
| 缓存颠簸 | cache thrashing | 并发超出 KV 容量后陷入反复驱逐与重算的退化状态 | — |
| 冷启动 | cold start | 新实例从调度到可服务所需时间，含权重加载与预热 | s |
| 降级模式 | degraded mode | 过载时主动降低服务等级（并发、上下文、模型档位）以维持可用性 | — |
| 端到端时延分解 | E2E latency decomposition | $T_{E2E}=T_{queue}+T_{tokenize}+T_{prefill}+T_{decode}+T_{network}+T_{post}$ | ms |
| 队头阻塞 | head-of-line blocking | 队首长请求阻塞其后短请求，tail latency 的常见来源 | — |
| 选择性配置 | selective configuration | benchmark 中只报告对自身最有利配置点的做法 | — |

## 12. 排队、容量与成本建模

> 本节随 [模块 01](docs/01_foundations_and_metrics/) 完成新增。

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 计算画像比 | prefill/decode ratio $R$ | $S_{in}/S_{out}$，判断系统偏 compute- 还是 memory-bound | 无量纲 |
| 变异系数 | coefficient of variation $C_S$ | $\sigma_S/E[S]$，服务时间相对离散度；通过 $(1+C_S^2)$ 放大排队时延 | 无量纲 |
| 脊点 | ridge point $I^*$ | $P/BW$，Roofline 上 memory/compute-bound 的分界，纯硬件属性 | FLOP/byte |
| 可达性能 | attainable performance | $\min(P, I\times BW)$，**上界而非预测值** | FLOP/s |
| 分层 Roofline | hierarchical roofline | 为每级内存（SRAM/L2/HBM）各画一条斜屋顶 | — |
| 权重字节数 | weight bytes $W_{bytes}$ | $P_{params}\times b_w$，decode 每步至少读一遍 | byte |
| 临界并发 | critical batch size $B^*$ | 权重与 KV 带宽消耗相等时的并发数；与上下文长度成反比 | 个 |
| 权重主导区 | weight-dominated regime | $B<B^*$，优化重点为批处理与权重量化 | — |
| KV 主导区 | KV-dominated regime | $B>B^*$，优化重点为 KV 量化、GQA/MLA、驱逐 | — |
| 带宽墙 | bandwidth wall | 算力增速持续快于带宽增速，使 $I^*$ 上升 | — |
| 有效利用率 | effective utilization $U$ | 实际交付量 ÷ 理论产能；直接进入成本分母 | % |
| 伪精确 | false precision | 输出有效位数超出输入精度所能支持的范围 | — |
| 运行时开销 | runtime overhead $M_{rt}$ | 激活、缓冲、碎片等显存占用，需实测标定 | GB |
| 余量因子 | headroom factors | 冗余×增长×区域，三者**相乘**而非相加 | 无量纲 |
| 测量边界 | measurement boundary | J/token 与功耗的四级口径：chip/node/rack/facility | — |
| 功率封顶 | power cap | 功耗达上限触发的频率限制；高负载时立即出现 | W |
| 热降频 | thermal throttling | 温度达阈值触发的频率下降；**运行一段时间后**逐渐出现 | — |
| 空载功耗 | idle power | 通电但无有效负载时的功耗；低利用率下占比高 | W |

## 13. Transformer 推理与 KV Cache

> 本节随 [模块 02](docs/02_transformer_and_kv_cache/) 完成新增。

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 单 token KV 占用 | per-token KV footprint $m_{tok}$ | $2LH_{KV}D_h b_{kv}$；只依赖模型结构与精度，是长上下文服务成本的代理指标 | byte/token |
| 可行边界 | feasible frontier | $B\times S\le$ KV 预算 $/m_{tok}$；并发与上下文长度是竞争关系 | — |
| KV 预算 | KV budget | 总显存 − 权重 − 运行时开销 | GB |
| 打分矩阵 | attention score matrix | $[B,H,T,S{+}T]$；长序列 prefill 的显存瓶颈 | — |
| 分组比 | group ratio | $H/H_{KV}$；决定 KV 压缩比与注意力算术强度 $2H/(H_{KV}b_{kv})$ | 无量纲 |
| 预留浪费 | reservation waste | 按最大可能长度预留而实际未用的显存 | GB |
| 写时复制 | copy-on-write | 共享 KV 块在被修改时才复制 | — |
| 共享作用域 | sharing scope | 前缀缓存的可见范围；**默认应限于租户内** | — |
| 混合精度 KV | mixed-precision KV | K 与 V 采用不同量化精度（K 经 softmax 对误差更敏感） | — |
| 针对性评测 | targeted evaluation | 专门包含依赖被牺牲信息样本的评测；通用评测检不出滑窗/驱逐的损失 | — |
| 标称上下文窗口 | nominal context window | 模型配置允许的最大 token 数 | token |
| 有效上下文能力 | effective context capability | 模型实际能可靠利用信息的长度范围；**未必等于标称窗口** | token |
| 视觉 token | visual token | 图像/视频经编码与投影后进入语言模型的 token | 个 |
| 特征缓存 | feature cache | 缓存多模态编码器输出以复用 | — |
| 思考预算 | thinking budget | 单请求允许消耗的推理 token 上限；兼作成本控制与过载降级旋钮 | token |
| 质量-成本曲线 | quality-cost curve | test-time compute 投入与结果质量的边际递减关系 | — |
| 三重压力 | triple pressure | 长上下文对时延、显存、质量的同时压力 | — |

## 14. Serving、调度与 QoS

> 本节随 [模块 03](docs/03_serving_engines_and_scheduling/) 完成新增。

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 控制面 / 数据面 | control plane / data plane | 秒级决策组件 / 毫秒级关键路径组件；职责错位是隐蔽的性能问题来源 | — |
| 有效批大小 | effective batch size | 实际贡献吞吐的平均并发序列数；静态批处理下可远低于名义批大小 | 个 |
| 吞吐峰值批大小 | throughput-peak batch size | 超过后因 cache thrashing 反而下降的批大小 | 个 |
| 抢占率 | preemption rate | 单位时间被抢占的请求数；cache thrashing 的先行信号 | 次/s |
| 块表 | block table | KV 逻辑块到物理块的映射 | — |
| 安全水位 | safety watermark | 触发拒绝或抢占的 KV 利用率阈值 | % |
| Token 预算 | token budget | 每次迭代处理的 token 总数上限 | token |
| Decode 份额上限 | max decode share | decode 最多占用的预算比例，防 prefill 饥饿 | % |
| Prefill 饥饿 | prefill starvation | decode 占满预算导致新请求无法开始 | — |
| 老化 | aging | 有效优先级随等待时间提升，防止饥饿 | — |
| 过载不可恢复 | non-self-recovering overload | 流量回落后系统仍停留在退化状态 | — |
| 多维配额 | multi-dimensional quota | 覆盖 req/s、tokens/s、并发、KV 占用的配额体系 | — |
| Token·秒 | token-seconds | 多租户统一资源计量，兼顾长度与占用时长 | token·s |
| 借用可回收 | reclaimable borrowing | 允许超用闲置配额但需要时回收 | — |
| 时序侧信道 | timing side channel | 通过 TTFT 差异推断他人是否发送过某前缀 | — |
| 升级率 | escalation rate $p$ | 级联中需升级到更高档位的请求比例；划算条件 $p<1-C_s/C_l$ | % |
| 保守偏置 | conservative bias | 路由不确定时上调档位，处理两类错误的非对称代价 | — |
| 命中比例 | hit ratio | $S_{hit}/S_{in}$，前缀缓存收益的一阶指标 | % |
| 缓存感知路由 | cache-aware routing | 依据实例缓存状态路由；缺失会使命中率稀释到约 $1/N$ | — |
| 路由稀释 | routing dilution | 多实例随机路由造成的命中率损失 | — |
| 思考时间 | think time $T_{think}$ | 用户读完回复到发下一条的间隔；决定 KV 驻留是否划算 | s |
| 机会主义缓存 | opportunistic caching | 不承诺保留但命中即受益 | — |
| 扩容滞后 | scaling lag $T_{lag}$ | 决策周期加冷启动时间；决定所需常备余量 | s |
| 滞后阈值 | hysteresis | 扩容与缩容用不同阈值以防抖动 | — |
| 成本交叉点 | cost crossover | $U=c_r/c_s$，serverless 与常驻成本相等的利用率 | % |
| 冷启动概率 | cold start probability $p_{cold}$ | 请求到达时无热实例的概率 | % |

## 15. 编译器、Runtime 与 Kernel

> 本节随 [模块 04](docs/04_compilers_runtimes_and_kernels/) 完成新增。

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 图捕获 | graph capture | 把动态执行转为静态计算图 | — |
| 优化 pass | optimization pass | 对 IR 施加的一次变换；**顺序不可交换** | — |
| Pass 顺序 | pass ordering | 融合须在布局变换之后、量化插入之前 | — |
| 分桶 | bucketing | 为若干离散形状分别编译，应对动态形状 | 桶数 |
| 填充浪费 | padding waste | $1-S/S_{bucket}$，补齐固定形状产生的无效工作 | % |
| 编译产物 | compiled artifact | 与硬件、模型、形状、量化、并行度**五维绑定**的二进制 | — |
| 图中断 | graph break | 编译器无法处理的构造使图被切成多段，跨段融合机会丢失 | 段数 |
| 重编译 | recompilation | 形状/类型不匹配缓存时重新编译；推理中因序列长度每步变化而高频触发 | 次 |
| 动态维度 | dynamic dimension | 不参与特化的张量维度；推荐序列长度设为动态、batch 分桶 | — |
| 覆盖度 | coverage | 编译器支持的算子与架构范围；编译器优先栈的选型核心 | — |
| 线程束 | warp | 一组同步执行的线程；束内分支发散会串行化 | — |
| 占用率 | occupancy | 活跃线程束数与硬件上限之比；**并非越高越好** | % |
| 访存合并 | memory coalescing | 束内线程访问连续地址；非合并的带宽损失是数量级的 | — |
| 分块 | tiling | 把问题切成可驻留片上的块以复用数据；**改常数不改复杂度阶** | — |
| 在线归约 | online reduction | 可增量更新的归约形式，避免全局同步，使分块成为可能 | — |
| 在线 softmax | online softmax | 用 $e^{m_{old}-m_{new}}$ 缩放修正已累积量；**数学精确等价** | — |
| 中间矩阵物化 | materialisation | 把注意力打分矩阵写入 HBM；朴素注意力的主要瓶颈 | — |
| 精确等价优化 | exact-equivalence optimisation | 代数恒等变换，无质量影响，**可无条件采用** | — |
| 仅权重量化 | weight-only quantisation | 只量化权重；在 memory-bound decode 中已取得主要收益 | — |
| 量化粒度 | quantisation granularity | 缩放因子共享范围（tensor / channel / group） | — |
| 缩放因子开销 | scale overhead | $2/(g\cdot b_w)$；group 过小会侵蚀量化收益 | % |
| 融合反量化 | fused dequantisation | 反量化在 kernel 内完成、不写回 HBM；**量化生效的前提** | — |
| 校准分布匹配 | calibration distribution match | 校准集须与生产流量分布一致，否则通用评测发现不了问题 | — |
| 固定开销 | fixed overhead $T_o$ | 与计算量无关的每次调用成本 | ms |
| 有效效率 | effective efficiency $\eta$ | $T_c/(T_c+T_o)$；消除开销的吞吐收益倍数为 $1/\eta$ | 无量纲 |
| Batch 扫描法 | batch sweep | 增大 batch 看每步时间是否不变，判断开销是否主导 | — |
| 验证证据 | verification evidence | 证明优化真的生效的可观测数字，而非配置项 | — |
| 静默失效 | silent failure | 配置正确、不报错，但优化实际未生效 | — |
| 支持的三个层次 | L1/L2/L3 support | 能跑通 / 性能可接受 / 接近最优；厂商矩阵通常只保证 L1 | — |
| 算子拆解 | operator decomposition | 用旧算子组合表达新算子；能跑但慢的隐蔽损失 | — |

## 16. 端侧与 On-Device 推理

> 本节随 [模块 10](docs/10_edge_and_on_device_inference/) 完成新增。

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 统一内存 | unified memory | CPU 与加速器共享同一物理内存与带宽池；**容量与带宽同时被瓜分** | — |
| 共享折扣 | sharing derate | 实际可用带宽与标称带宽之比中的共享因子 | 无量纲 |
| 内存预算 | memory budget | 应用可安全使用的设备内存上限；**分母是驻留额度而非设备标称容量** | 字节 |
| 驻留额度 | resident allowance | 系统内存压力下应用可稳定保持的内存；随用户行为变化 | 字节 |
| 进程终止 | process termination | 系统在内存压力下杀死应用；端侧的主要失效形式之一 | 次/时段 |
| 只读映射 | read-only mapping | 权重以干净页映射，可被回收后重新缺页；把「被杀」变为「重新缺页」 | — |
| 有效位宽 | effective bit width | 含量化缩放因子开销的实际位宽 $b_w + b_s/g$ | 位 |
| 质量断点 | quality cliff | 低于某位宽后质量迅速劣化的点 | 位 |
| 稀释倍数 | dilution factor | 聚合指标掩盖局部退化的倍数，等于受影响 token 占比的倒数 $1/f$ | 无量纲 |
| 算子覆盖 | operator coverage | NPU 能原生执行的算子集合 | — |
| 回退 | fallback | 不被支持的算子改由 CPU/GPU 执行 | — |
| 切换开销 | switch overhead | 计算单元之间切换的同步与布局转换代价；带宽受限时为纯损失 | 秒/次 |
| 热稳态吞吐 | sustained throughput | 进入热平衡后的持续吞吐；**端侧验收应取此值而非峰值** | token/s |
| 能效拐点 | efficiency knee | 每操作能耗最低的频率-电压点；峰值 boost 点通常在其之外 | — |
| 能力档位 | capability tier | 按实测能力而非型号划分的配置档 | — |
| 能力探测 | capability probing | 运行时测出内存、带宽与算子支持 | — |
| 资源让渡 | resource yielding | 用户高负载时主动降低占用 | — |
| 硬实时 | hard real-time | 必须在截止时间内完成，否则系统失效 | — |
| 最坏执行时间 | worst-case execution time | 所有输入与状态下的时延上界；**自回归生成无法可信给出** | 秒 |
| 资源分区 | resource partitioning | 静态划分算力、内存、带宽 | — |
| 确定性降级 | deterministic degradation | 明确定义的退化行为而非「慢一点」 | — |
| 共存验证 | co-existence validation | 在非实时负载满负荷时验证实时任务；**分别测两者会错过干扰** | — |
| 任务白名单 | task allowlist | 由产品逻辑限定端侧模型的调用入口 | — |
| 适配参数 | adapter | 在共享基座上切换任务的小参数集 | — |
| 交叉输出长度 | crossover length | 端云时延相等时的输出长度；随 RTT 上升而扩大端侧优势区间 | token |
| 事后升级 | post-hoc escalation | 端侧结果不佳时转到云端；**代价是两条路径相加而非二选一** | — |
| 并行发起 | parallel dispatch | 端云同时开始，择优返回；用能耗与成本换时延 | — |
| 隐私优先架构 | privacy-first architecture | 敏感数据强制端侧且无升级路径 | — |

> **交叉输出长度的两种记法**：[第 8 章](docs/10_edge_and_on_device_inference/08_private_hybrid_cloud_edge_architectures.md) 把首 token 计入 TTFT（写作 $N^{*}$），
> [第 9 章](docs/10_edge_and_on_device_inference/09_edge_deployment_case_studies.md) 把全部 token 按速率计（写作 $n^{*}$），二者相差 1。
> **同一次分析内不可混用**。

## 17. 网络、互连与集合通信

> 本节随 [模块 08](docs/08_networking_and_interconnect/) 推进新增。

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| $\alpha$-$\beta$ 模型 | alpha-beta model | $T(n)=\alpha+n/\beta$，把传输拆为固定开销与带宽项 | — |
| 半功率消息尺寸 | half-power message size | $n_{1/2}=\alpha\beta$；固定开销与传输时间相等的尺寸 | 字节 |
| 时延主导 | latency-bound | $n \ll n_{1/2}$；**应减少通信次数，压缩无用** | — |
| 带宽主导 | bandwidth-bound | $n \gg n_{1/2}$；**应减少通信字节，批合并无用** | — |
| 环状 all-reduce | ring all-reduce | $2(P-1)$ 步、只与邻居通信；带宽最优但时延项 $O(P)$ | — |
| 递归折半-倍增 | recursive halving-doubling | $2\log_2 P$ 步且字节数与 ring 相同；对拓扑映射敏感 | — |
| 二项树 | binomial tree | $2\log_2 P$ 步但每步传完整 $D$；适用区间窄 | — |
| 带宽下界 | bandwidth lower bound | all-reduce 每节点至少移动 $\frac{2(P-1)}{P}D$ 字节 | 字节 |
| 抖动放大 | jitter amplification | $1-(1-p)^{2L}$；单次异常率经每 token $2L$ 次通信的放大 | — |
| 内核旁路 | kernel bypass | 绕过内核协议栈直接与 NIC 交互；**消除的是 $\alpha$ 的软件部分** | — |
| 单边操作 | one-sided operation | 接收方不参与的远程读写；适合 KV 拉取 | — |
| 内存注册 | memory registration | 锁定页表并向 NIC 登记；一次性高成本，**不应在关键路径上** | — |
| 同步点 | synchronization point | 后续计算依赖其结果因而不可重叠的通信；TP 的两次 all-reduce 即是 | — |
| 一致域大小 | scale-up domain size $S$ | 以高带宽低时延互连成一致域的设备数；也是故障域 | 设备数 |
| 所需设备数 | required device count | $\lceil (N b_w + M_{KV})/(M_{dev}u) \rceil$ | 设备数 |
| 层等价量 | layer-equivalent | $L/(\text{TP}\cdot\text{PP})$；**只依赖乘积，故 TP 与 PP 对内存等价** | — |
| 一阶开销估计 | first-order overhead | 通信占比与气泡占比之和；**用于排序而非精确预测** | % |
| 线速 | line rate | 物理层标称速率，未扣除编码与协议开销 | Gb/s |
| 二分带宽 | bisection bandwidth | 把网络分成两半时跨越切面的总带宽 | GB/s |
| 直径 | diameter | 任意两主机间最长最短路径的跳数；**只加在 $\alpha$ 上，影响有限** | 跳 |
| 交换机基数 | switch radix | 单台交换机端口数 $k$；Clos 的交换机/主机比为 $5/k$ | 端口 |
| 超订比 | oversubscription ratio | 下行与上行带宽之比；**直接乘在需满二分带宽的操作上** | — |
| 争用因子 | contention factor | 空载 $\beta$ 与满载有效 $\beta$ 之比；**乘在 $\beta$ 上，影响远大于跳数** | 无量纲 |
| rail 优化 | rail-optimized | 各主机同序号端口连到同一交换机；**本质是流量隔离而非减少跳数** | — |
| 映射校验 | mapping validation | 确认并行组成员的物理放置与假设一致；**每次部署都可能变** | — |
| 排队放大 | queueing amplification | $\frac{\rho}{1-\rho}$；$\rho=0.85$ 时为 5.67 倍 | 无量纲 |
| incast | incast | 多发送方同时向同一接收方汇聚 | degree |
| incast degree | incast degree | 并发发送方数；**all-to-all 为 $P-1$，ring 恒为 1** | — |
| 端到端标记式 | end-to-end marking | 交换机打标记、发送方降速；**反应需一个往返，对 incast 来不及** | — |
| 逐跳暂停式 | hop-by-hop pause | 下游满时暂停上游；**不丢包但拥塞会逆流扩散** | — |
| 流控粒度 | flow-control granularity | 流控作用的单位；**须与 QoS 分类一致，否则分类失效** | — |
| 等待时长 | wait time $w_i$ | $\max_j(t_j)-t_i$；rank $i$ 到达同步点后等待其余各方的时间 | 秒 |
| 等待极差 | wait spread | $\max_i w_i-\min_i w_i$；**区分「网络慢」与「单点掉队」的判据** | 秒 |
| 掉队者 | straggler | 最后到达同步点者；**其等待时长为 0，即等待最短者** | — |
| 上游级联 | upstream cascade | 全体都晚但彼此齐整；**本同步点全部指标正常，须跨同步点对齐才能发现** | — |
| 触发式采样 | triggered sampling | 仅在超阈值时详细记录；针对尾部，开销可控 | — |

> **两条容易出错的口径**：
> ① **网络链路速率用比特（Gb/s、Tb/s），内存与互连带宽用字节（GB/s、TB/s），相差 8 倍**；
> ② **线速不是可用吞吐**，其间还有编码、协议与有效载荷比三层折扣。

## 18. 硬件、存储层次与低精度

> 本节随 [模块 07](docs/07_hardware_and_server_architecture/) 推进新增。

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 机器平衡 | machine balance | $\text{FLOPS}/\text{BW}$，硬件的算术强度分界 | FLOP/B |
| 分块算术强度 | tile arithmetic intensity | $I=2T/(3b)$，**随分块边长线性增长**；矩阵引擎与分块的存在理由 | FLOP/B |
| 算力效应 | compute effect | 低精度提高峰值算力；**只在计算受限（prefill）时兑现** | — |
| 访存效应 | memory effect | 低精度减少搬运字节；**只在带宽受限（decode）时兑现** | — |
| 仅权重量化 | weight-only quantisation | 只量化权重，读入后反量化再计算；**decode 接近位宽比，prefill 接近 1×** | — |
| 有效位宽 | effective bit width | $b_w+b_s/g$，含缩放因子开销 | 位 |
| 累加精度 | accumulation precision | 乘积求和所用格式；**误差随 $\sqrt{K}$～$K$ 增长，通常不该降** | — |
| 补齐浪费 | padding waste | 维度非分块倍数造成的无效计算；**decode 下通常无害** | % |
| 在途字节 | bytes in flight | $\text{BW}\times\text{延迟}$，打满带宽所需的并发访存量 | 字节 |
| 访存并发不足 | insufficient memory-level parallelism | 在途字节低于 $\text{BW}\times\text{延迟}$；**表现为「带宽低」但只需改 kernel** | — |
| 可达分块 | achievable tile size | $T_{\max}=\sqrt{M_{\text{片上}}/3b}$；**片上容量对强度的影响是 $\sqrt{\cdot}$** | — |
| 卸载带宽比 | offload bandwidth ratio | $\text{BW}_{\text{HBM}}/\text{BW}_{\text{卸载层}}$；权重卸载的代价倍数 | 无量纲 |
| 可选择性 | selectivity | 能否只访问所需的一部分；**KV 有而权重没有**，决定卸载可行性 | — |
| 饱和吞吐上限 | throughput ceiling | $\text{BW}/(Sk)$，批趋于无穷时的 decode 吞吐；**与权重无关** | token/s |
| 半饱和批 | half-saturation batch | $B_{\text{half}}=W/(Sk)$；**KV 流量等于权重流量的批** | — |
| 容量并发上限 | capacity concurrency limit | $C_{\max}=(M-W)/(Sk)$ | — |
| 显存权重比 | memory-to-weight ratio | $M_{\text{total}}/W$；**可达吞吐占饱和上限的比例为 $1-W/M$** | 无量纲 |
| 每 token 搬运地板 | per-token traffic floor | $Sk$，不可被批摊薄的那部分；长上下文下主导能耗 | 字节 |
| 主机瓶颈批 | host-bound batch $B^{*}$ | $t_{\text{dev}}/h$；超过它主机成为瓶颈。**设备越快门槛越低** | — |
| 冷启动时间 | cold start time | $W/\text{BW}_{\text{存储}}$ 加初始化；**与尖峰时长同量级时扩缩容失效** | 秒 |
| 预热池 | warm pool | 预先就绪的副本；以成本换就绪时间 | 副本数 |
| 节点级口径 | node-level accounting | 含主机、风扇、电源转换的功耗与成本口径；**加速器级口径会系统性低估** | W / $ |
| 故障粒度 | failure granularity | 一次故障带走的最小单位；TP 组横跨整节点时即为整节点 | — |
| SRAM 常驻 | SRAM-resident | 权重全部放进片上存储；**$M/W\approx1$，故结构上拿不到批处理收益** | — |
| 阵列效率 | array efficiency | $\min(1, B/T_{\text{array}})$；小批下极低但带宽受限时只影响能耗 | % |
| 专用化适应风险 | specialisation adaptation risk | 模型结构变化时专用架构的失效风险 | — |
| 可摊薄性 | amortisability | 成本能否随并发下降；由 $1-W/M$ 决定 | — |
| 扣除通信后的 SLO 上界 | communication-adjusted SLO bound | $((\text{TPOT}-T_{\text{comm}})\text{BW}-W)/(Sk)$；**不扣会随 $P$ 增大而越发高估** | — |
| 边际收益耗尽点 | marginal-return exhaustion point | 每设备吞吐增幅降至阈值以下的 $P$；**同时是脆弱性拐点** | — |

> **本节最值得记住的一条**：decode 的两个上界相除后，序列长度与 KV 配置**完全约掉**——
> $C_{\max}/B_{\text{half}} = M_{\text{total}}/W - 1$，
> 而可达吞吐占饱和上限的比例是 $1-W/M_{\text{total}}$，即**显存中未被权重占据的比例**。
> $M/W < 2$ 时连半饱和吞吐都达不到。

## 19. 开源部署、复现与参考架构

> 本节随 [模块 12](docs/12_open_source_deployment_and_reproduction/) 完成新增。

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 机制对齐 | mechanism alignment | 把各项目术语映射到统一概念，**而非按 README 词面比较** | — |
| 命名分歧 | naming divergence | 同一机制在各项目的不同名称（prefix caching / RadixAttention / KV Cache Reuse） | — |
| 参数同名不同义 | parameter semantic divergence | 名字相近但**分母或包含项不同**的参数；跨引擎不可直接搬运 | — |
| 分化点 | differentiator | 不写进特性表却决定实际行为的设计选择（默认值、调度、预留、失败行为、可观测面） | — |
| 有效容量比 | effective capacity ratio $u$ | 实际可分配给 KV 的容量占标称的比例；**推荐的首选横向指标** | % |
| 重算式抢占 | `RECOMPUTE` preemption | KV 不足时丢弃并重算；代价是重复 prefill，打在 TTFT 上 | — |
| retract | retract | 部分项目对「抢占」的用词；**按 preemption 检索会漏掉** | — |
| 分层 KV 缓存 | hierarchical KV cache | L1(GPU)/L2(主机)/L3(分布式)；**L3 可集群共享** | — |
| 预取阈值 | prefetch threshold | 触发从远端预取所需的最小命中长度；**过低则短命中的往返变纯开销** | token |
| 优先级 LRU | prioritized LRU | 先清空最低优先级再按 LRU；**驱逐可为降级而非失效** | — |
| 取小规则 | min-rule allocation | 同时设容量比例与绝对上限时，实际分配取两者下界 | — |
| 规模一致性 | forward-size consistency | 各次前向的 token 数接近相等；**直接压缩时延方差** | — |
| 驻留比例 | resident fraction $\varphi$ | 本地推理中驻留显存的权重比例；**接近 1 与否几乎决定全部性能** | 无量纲 |
| 可行性参数 | feasibility parameter | 决定「能否跑」而非「跑多快」的参数；本地场景的位宽即是 | — |
| 弹性上界 | elasticity ceiling | 由冷启动时间决定的扩缩容有效性上界；**编排层无法突破** | — |
| 组调度 | gang scheduling | 并行组要么整组就位、要么不启动 | — |
| 前缀感知路由 | prefix-aware routing | 把共享前缀的请求聚集到同一实例；**与负载均衡目标冲突** | — |
| 串联尾部放大 | serial tail amplification | $1-(1-p)^n$，$n$ 为串联层数；与每 token $2L$ 次通信同式 | — |
| GenAI 语义约定 | GenAI semantic conventions | OTel 的标准指标命名；**在名字里区分 server/client 与 token/chunk** | — |
| 分位数不可平均 | percentiles are not averageable | 须先聚合直方图桶计数再求分位数 | — |
| 决定性约束 | binding constraint | 某架构最先撞上的那个上界 | — |
| 纸上否决 | paper rejection | 实施前用判据排除不可行架构 | — |
| 口径问题 | measurement-artifact | 测到的是测量方式而非系统性质 | — |
| 可复核结论 | reproducible conclusion | 含版本 tag、口径、样本量与复现命令；**缺任一项等同未核验** | — |

> **本节最值得记住的一条**：三家引擎的显存比例参数**分母各不相同**——
> vLLM `gpu_memory_utilization`（总显存）、SGLang `--mem-fraction-static`（总显存**含权重**）、
> TensorRT-LLM `free_gpu_memory_fraction`（**空闲显存**，默认 0.9）。
> **同样填 0.9 会得到不同的 KV 容量，进而按 $C_{\max}=M_{\text{KV}}/(Sk)$ 得到不同的并发上限**。

---

## 20. 文献工作与证据分级

> 本节随 [模块 13](docs/13_research_papers_and_technical_reports/) 第一批文档新增。

| 中文术语 | 英文 | 定义 | 单位/口径 |
|---|---|---|---|
| 降级书写 | degraded authoring | 一手来源不可达时，只书写可独立论证的部分，并对其余部分**显式标注欠账**而非省略 | — |
| 证据类别 | evidence class | 字段来源的四级划分：A 仓库 BibTeX / B 搜索书目 / C 实现代码 / D 论文正文 | — |
| 结构性论断 | structural claim | 可由机制形状推出、不依赖实验数据的结论（如收益归零条件、能否叠加） | — |
| 测量性论断 | measured claim | 必须由实验给出、跨条件不可外推的结论（如加速比） | — |
| 瓶颈导向地图 | bottleneck-oriented map | 按论文攻击的性能方程分项、而非按时间或会议组织文献 | — |
| 可见欠账 | visible debt | 审计中单独计数并逐条列出、但不阻断门禁的未完成项；对立面是「为了让门禁变绿而谎报」 | 条 |
| 精确注意力 | exact attention | 与标准注意力逐位相等的实现，区别于稀疏/低秩等近似方法 | — |
| 注意力泄压点 | attention sink | 序列最开头承接多余注意力质量的少数 token；被驱逐会导致窗口注意力突然崩坏 | 个 |
| 续训 | uptraining | 由已有检查点经结构变换与短期继续训练得到新结构（如 MHA → GQA） | — |
| 生成停顿 | generation stall | 批内出现长 prefill 导致同批 decode 请求的 ITL 被同步拉长 | s |
| 无停顿调度 | stall-free scheduling | 固定每迭代 token 预算，使迭代耗时方差趋近于零 | — |
| 统计复用 | statistical multiplexing | 合并 $n$ 条独立突发流使相对波动按 $1/\sqrt{n}$ 量级下降 | — |
| 分布不变性 | distribution preservation | 投机解码的接受/重采样规则使输出与直接从目标模型采样同分布 | — |
| 自投机 | self-speculation | draft 与 target 共享主干计算，不引入第二个模型 | — |
| token 树 | token tree | 多条候选序列组成的树，可由一次前向并行验证 | — |
| 雅可比解码 | Jacobi decoding | 把自回归约束视为非线性方程组并行迭代求解 | — |
| 用算力换时延 | compute-for-latency trade | 增加总计算量以减少串行步数；能耗随之上升 | J/token |
| 名义位宽 | nominal bit width | 量化格式声明的位宽，不含定标参数开销 | bit |
| 有效位宽 | effective bit width | 计入定标开销后的平均位宽 $b_w + b_s/g$；报压缩比必须用它 | bit |
| 仅权重量化 | weight-only quantization | 只量化权重，计算时反量化回高精度；**省带宽不省算力** | — |
| 权重激活联合量化 | W+A quantization | 权重与激活同时量化，矩阵乘可落到低精度算力单元 | — |
| 等价缩放变换 | equivalent scaling transform | 插入一对互逆对角缩放，在激活与权重之间**再分配**量化难度 | — |
| 稠密-稀疏分解 | dense-and-sparse decomposition | 少数权重以稀疏高精度保留、其余低位宽稠密存储 | — |

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
