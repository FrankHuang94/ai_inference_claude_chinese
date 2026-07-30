# 编码练习：十道推理系统的现场编码题

> 位置：[InferenceAtlas](../../INDEX.md) > [模块 17](README.md) > 当前文档
> 信息截至：2026-07-29 ｜ 最后核验：2026-07-29 ｜ 内容版本：v0.1
> 时效性等级：低
> 相关主题：[题库 Q001–Q100](README.md)｜[系统设计案例](09_mock_interview_cases.md)｜`11_90_day_study_plan.md`

## 本文档的定位

推理岗位的编码环节**不考通用算法题**，考的是
**「你能不能把推理系统里的一个具体机制写出来」**。
这类题的特点是：

1. **规模小**：多数题的核心逻辑在 30–60 行以内；
2. **考点明确**：每道题都对应一个具体的系统概念，
   **写不出来通常是因为不理解那个概念，而不是不会写代码**；
3. **有正确性判据**：多数题有一个可以当场验证的不变量
   （例如在线 softmax 的分块合并必须与整体计算一致），
   **主动写出这个验证是最有效的加分动作**。

**全部十道题的参考实现是可运行的**，位于
[`code/interview_exercises.py`](../../code/interview_exercises.py)，
包含每题的自测。运行方式：

```bash
python3 code/interview_exercises.py
```

**它只依赖 Python 标准库**，没有任何第三方依赖——
这是有意的：面试白板或共享编辑器里通常没有 NumPy 与 PyTorch，
**能用纯 Python 把逻辑写清楚是这类题的实际要求**。

## 怎么用这份文档

**不要先看参考实现**。正确的用法是：

1. 读题面与「考察点」，先自己写；
2. 写完后用「自测」一节的不变量检查自己的实现；
3. 再对照参考实现，重点看「关键设计决策」里你没想到的部分；
4. 最后看「常见错误」，确认自己没踩。

**每道题标注了预期时间**。超时不是问题，
**但如果某道题的「考察点」你读完仍然不理解，
应该先回去读对应的题库题目**——
编码题写不出来的根因通常在概念而不在代码。

## 十道题一览

| # | 题目 | 考察的概念 | 预期时间 | 对应题库 |
|---|---|---|---|---|
| E1 | KV 容量与并发上界 | KV 内存模型 | 10 分钟 | [Q014](02_kv_cache_and_transformer_questions.md) |
| E2 | 在线 softmax 的分块合并 | FlashAttention 的核心 | 25 分钟 | [Q047](04_compiler_kernel_and_quantization_questions.md) |
| E3 | temperature / top-k / top-p / min-p | 采样与顺序不可交换 | 25 分钟 | [Q002 组](01_inference_system_design.md) |
| E4 | 分页 KV 的页表与写时复制 | PagedAttention 的内存管理 | 35 分钟 | [Q020](02_kv_cache_and_transformer_questions.md) |
| E5 | 前缀缓存的 trie 匹配 | 前缀共享 | 20 分钟 | [Q024](02_kv_cache_and_transformer_questions.md) |
| E6 | 投机解码的接受-重采样 | 分布不变性 | 35 分钟 | [案例三](09_mock_interview_cases.md) |
| E7 | 加速比与最优提议数 | 投机解码的经济学 | 15 分钟 | [案例三](09_mock_interview_cases.md) |
| E8 | 流式分位数统计 | 指标口径与样本量 | 25 分钟 | [Q092](07_debug_benchmark_and_reliability_questions.md) |
| E9 | 准入控制与抢占模拟 | 调度与资源守恒 | 40 分钟 | [Q032](03_serving_scheduling_and_slo_questions.md)、[Q033](03_serving_scheduling_and_slo_questions.md) |
| E10 | roofline 与临界批大小 | 瓶颈判定 | 10 分钟 | [Q045](04_compiler_kernel_and_quantization_questions.md) |

---

## E1：KV 容量与并发上界

**题面**：写两个函数。第一个计算每个 token 的 KV 字节数，
第二个在给定可用显存、权重大小与序列长度的情况下算出并发上界。

**考察点**：能不能正确写出 KV 的内存公式。
**最常见的错误是漏掉「K 和 V 各一份」的因子 2**。

**关键设计决策**：

1. **用 KV 头数而不是查询头数**。GQA 下两者不同，
   **用查询头数会高估 KV 占用**；
2. **可用显存要先扣除权重与激活**，
   而且**传入的应当是「可用」而非「标称」容量**——
   把这个区分放在参数命名里能避免调用方误用；
3. **返回整数并向下取整**，因为半个请求没有意义。

```python
def kv_bytes_per_token(n_layers, n_kv_heads, head_dim, bytes_per_elem):
    return 2 * n_layers * n_kv_heads * head_dim * bytes_per_elem


def max_concurrency(mem_avail, weight_bytes, act_bytes, m_tok, seq_len):
    free = mem_avail - weight_bytes - act_bytes
    if free <= 0:
        return 0
    return int(free // (m_tok * seq_len))
```

**自测**：80 层、8 个 KV 头、头维 128、fp16 时，
每 token 应为 $2 \times 80 \times 8 \times 128 \times 2 = 327680$ 字节（320 KiB）。
可用 80 GiB、权重 40 GiB、激活 2 GiB、序列 4096 时，并发上界为 30。

**常见错误**：

- 漏掉因子 2（K 和 V）；
- 用查询头数而不是 KV 头数；
- 忘记处理 `free <= 0` 的情形而返回负数；
- 用标称容量而非可用容量。

**可能的追问**：如果序列长度不同怎么办？
（答：应按批内序列长度之和而非「并发 × 平均长度」，
**后者在长度方差大时会低估峰值占用**。）

---

## E2：在线 softmax 的分块合并

**题面**：注意力被分成若干块分别计算，
每块产出 $(m_i, \ell_i, o_i)$——块内最大分数、指数和、加权值向量。
写一个函数把这些块合并成最终结果，**要求与不分块的计算完全一致**。

**考察点**：这是 FlashAttention 与序列并行的数学核心。
**能写对它说明你真正理解了「为什么分块注意力是精确而非近似的」**。

**关键设计决策**：

1. **合并时要同时缩放累加器与新块**，因为新的最大值可能来自任一侧；
2. **缩放因子是 $\exp(m_{\text{old}} - m_{\text{new}})$**，
   它恒 $\le 1$，**这正是数值稳定性的来源**；
3. **初始的 $m$ 取 $-\infty$**，
   要处理 `exp(-inf - m_new)` 的情形（应为 0）。

```python
import math

def online_softmax_merge(blocks):
    """blocks: [(m_i, l_i, o_i)]。返回合并后的 (m, l, o)。"""
    m_acc, l_acc, o_acc = -math.inf, 0.0, None
    for m_b, l_b, o_b in blocks:
        if o_acc is None:
            o_acc = [0.0] * len(o_b)
        m_new = max(m_acc, m_b)
        s_acc = math.exp(m_acc - m_new) if m_acc > -math.inf else 0.0
        s_b = math.exp(m_b - m_new)
        l_acc = l_acc * s_acc + l_b * s_b
        o_acc = [a * s_acc + b * s_b for a, b in zip(o_acc, o_b)]
        m_acc = m_new
    return m_acc, l_acc, o_acc
```

最终输出是 $o / \ell$。

**自测（这是本题最重要的部分）**：
构造一组随机分数与值，用块大小 1、2、5、以及「整块」分别合并，
**四者的结果应在浮点误差内完全一致**。
参考实现中这个测试用 17 个 token、块大小 {1,2,5,17}，
差异小于 $10^{-9}$。

**主动写出这个测试是本题最大的加分点**——
它证明你知道「精确性」是这个算法的关键性质。

**常见错误**：

- 只缩放累加器不缩放新块（当新块的最大值更小时出错）；
- 忘记处理初始的 $-\infty$；
- 把 $o$ 提前除以 $\ell$（应该最后除一次）；
- 认为这是近似算法。

**可能的追问**：合并操作满足结合律吗？
（答：满足，所以分块顺序不影响结果——
**这正是它能用于序列并行的环形通信的原因**，见 [Q064](05_distributed_and_moe_questions.md)。）

---

## E3：temperature / top-k / top-p / min-p

**题面**：实现采样的过滤链，支持温度、top-k、top-p 与 min-p，
返回过滤并重新归一化后的概率分布。

**考察点**：**四个参数的顺序不可交换**。
这是本题的核心考点，也是最容易被忽略的一点。

**关键设计决策**：

1. **温度必须最先应用**，因为它改变概率分布，
   **从而改变 top-p 会选中哪些 token**；
2. **温度为 0 应退化为 argmax**，而不是除零；
3. **top-p 的定义包含「跨过阈值的那一个」**——
   累积到 $\ge p$ 时把当前 token 也保留；
4. **min-p 是相对于最大概率的**（$p_i \ge \text{min\_p} \cdot p_{\max}$），
   不是绝对阈值；
5. **最后必须重新归一化**。

```python
def apply_sampling_filters(logits, temperature=1.0, top_k=None,
                           top_p=None, min_p=None):
    """顺序：temperature -> top_k -> top_p -> min_p。顺序不可交换。"""
    if temperature <= 0:
        out = [0.0] * len(logits)
        out[max(range(len(logits)), key=lambda i: logits[i])] = 1.0
        return out
    probs = softmax([x / temperature for x in logits])
    idx = sorted(range(len(probs)), key=lambda i: probs[i], reverse=True)
    keep = set(idx)
    if top_k is not None:
        keep &= set(idx[:top_k])
    if top_p is not None:
        cum, chosen = 0.0, set()
        for i in idx:
            if i not in keep:
                continue
            chosen.add(i)
            cum += probs[i]
            if cum >= top_p:      # 包含跨过阈值的这一个
                break
        keep &= chosen
    if min_p is not None:
        p_max = max(probs[i] for i in keep)
        keep = {i for i in keep if probs[i] >= min_p * p_max}
    total = sum(probs[i] for i in keep)
    return [probs[i] / total if i in keep else 0.0 for i in range(len(probs))]
```

**自测**：用 `logits = [2.0, 1.0, 0.5, 0.0, -1.0]`，
在 `top_p = 0.9` 下：

| 温度 | 保留的 token 数 |
|---|---|
| 0.5（更尖） | 2 |
| 2.0（更平） | 4 |

**同一个 top-p 阈值在不同温度下保留的集合大小不同**——
这就是「顺序不可交换」的具体表现。
**在面试中现场演示这一点比口头说明有力得多**。

**常见错误**：

- 在温度之前应用 top-p（顺序错）；
- 温度为 0 时除零；
- top-p 排除掉跨过阈值的那一个（导致 $p$ 很小时可能一个都不留）；
- 把 min-p 当成绝对阈值；
- 忘记重新归一化。

**可能的追问**：为什么服务端要支持每个请求不同的采样参数？
怎么在批处理中高效实现？
（答：参数需要张量化为一个批维度的向量，
**而不是逐请求循环**——否则采样会成为一个显著的 CPU 开销。）

---

## E4：分页 KV 的页表与写时复制

**题面**：实现一个分页的 KV 管理器，支持分配、追加 token、
**从一个序列 fork 出另一个（共享前缀）**、以及释放。

**考察点**：这是 PagedAttention 内存管理的核心。
**难点在写时复制的时机**。

**关键设计决策**：

1. **只有末页需要写时复制**。已满的页不会再被写入，
   **所以它们可以被无限共享**——这是 fork 的收益来源；
2. **写时复制发生在「写入一个被共享的末页」时**，
   而不是 fork 时。fork 本身是 $O(\text{页数})$ 的引用计数递增；
3. **引用计数归零才回收页**；
4. **新页分配时不需要检查共享**（它一定是独占的）。

```python
from collections import defaultdict

class PagedKV:
    def __init__(self, n_pages, page_size):
        self.page_size = page_size
        self.free = list(range(n_pages))
        self.refcount = defaultdict(int)
        self.tables = {}    # seq_id -> [page_id, ...]
        self.lengths = {}   # seq_id -> token 数

    def _alloc(self):
        if not self.free:
            raise MemoryError("no free page")
        pid = self.free.pop()
        self.refcount[pid] = 1
        return pid

    def append(self, seq_id, n_tokens=1):
        for _ in range(n_tokens):
            L = self.lengths[seq_id]
            if L % self.page_size == 0:          # 需要新页
                self.tables[seq_id].append(self._alloc())
            else:                                # 写入末页：可能需要复制
                last = self.tables[seq_id][-1]
                if self.refcount[last] > 1:
                    self.refcount[last] -= 1
                    self.tables[seq_id][-1] = self._alloc()
            self.lengths[seq_id] = L + 1

    def fork(self, src, dst):
        self.tables[dst] = list(self.tables[src])
        self.lengths[dst] = self.lengths[src]
        for pid in self.tables[dst]:
            self.refcount[pid] += 1
```

（完整实现含 `new_sequence` 与 `free_sequence`，见
[`code/interview_exercises.py`](../../code/interview_exercises.py)。）

**自测**：

1. 序列 a 追加 6 个 token（页大小 4）→ 占 2 页；
2. fork 出 b → **仍然只占 2 页**（全部共享）；
3. b 再追加 1 个 token → **末页被复制，总共 3 页**，
   而**首页（已满）仍然被两者共享**；
4. 释放 a → 首页引用计数降为 1；
5. 释放 b → 全部页回到空闲列表。

**第 3 步是关键**：验证「只复制末页、已满页仍共享」。

**常见错误**：

- fork 时就复制全部页（失去了共享的意义）；
- 写时复制时忘记递减原页的引用计数（导致页永不回收）；
- 在新页分配路径上也做写时复制检查（多余但无害）或反过来漏掉末页检查（导致数据被污染，**这是真正的 bug**）；
- 释放时不检查引用计数就把页放回空闲列表。

**可能的追问**：多个序列共享的页被并发写入怎么办？
（答：写路径必须先检查引用计数——
**这正是 [Q095](07_debug_benchmark_and_reliability_questions.md) 里提到的跨租户泄漏风险的技术根源**。）

---

## E5：前缀缓存的 trie 匹配

**题面**：实现一个前缀树，支持插入 token 序列与查询「最长可命中前缀长度」。

**考察点**：前缀缓存的匹配逻辑，
以及**理解「只有完全相同的前缀才能复用」这个限制**。

**关键设计决策**：

1. **按 token 而非按字符建树**；
2. **匹配返回长度而不是布尔值**——
   因为部分命中也有价值（只需 prefill 剩余部分）；
3. **记录每个节点的命中次数**，用于后续的驱逐决策。

```python
class PrefixTrie:
    __slots__ = ("children", "hits", "depth")

    def __init__(self, depth=0):
        self.children = {}
        self.hits = 0
        self.depth = depth

    def insert(self, tokens):
        node = self
        for t in tokens:
            nxt = node.children.get(t)
            if nxt is None:
                nxt = PrefixTrie(node.depth + 1)
                node.children[t] = nxt
            node = nxt
            node.hits += 1
        return node

    def match(self, tokens):
        """返回可命中的最长前缀长度。"""
        node, n = self, 0
        for t in tokens:
            nxt = node.children.get(t)
            if nxt is None:
                break
            node = nxt
            n += 1
        return n
```

**自测**：插入 `[1,2,3,4]` 与 `[1,2,5]` 后，
`match([1,2,5,6])` 应为 3，`match([1,2,9])` 应为 2，`match([9])` 应为 0。
两条共 7 个 token 的序列只用了 5 个非根节点——**这就是共享的收益**。

**常见错误**：

- 只支持全匹配不支持前缀匹配；
- 用字符串拼接做键（内存与比较开销都大）；
- 没有考虑驱逐——**生产实现必须有容量上限**，
  否则 trie 会无限增长。

**可能的追问**：怎么加驱逐？
（答：按「最久未使用 + 节点深度」——
**深的节点代表更长的共享前缀，价值更高，应该更晚被驱逐**。
另外驱逐必须从叶子开始，否则会切断到更深节点的路径。）

**第二个追问**：多租户下这个 trie 怎么隔离？
（答：**根据租户分树，或把租户标识作为路径的第一个 token**。
见 [Q095](07_debug_benchmark_and_reliability_questions.md)。）

---

## E6：投机解码的接受-重采样

**题面**：给定目标分布 $p$、草稿分布 $q$ 与草稿采出的 token，
实现接受判据与拒绝时的重采样，
**并证明整个过程的输出分布恰好等于 $p$**。

**考察点**：这是投机解码的正确性核心。
**能写出「输出分布恒等于 $p$」的验证，是这道题的满分动作**。

**关键设计决策**：

1. **接受概率是 $\min(1, p_t/q_t)$**；
2. **拒绝时从残差分布 $\max(p-q, 0)$ 归一化后重采样**——
   **不是从 $p$ 重采样**，那样会破坏分布；
3. **残差和为 0 的退化情形要处理**（当 $q$ 处处 $\ge p$ 时不会发生拒绝，
   但数值上仍需防护）。

```python
def speculative_accept(p, q, draft_token, u):
    """u 为 [0,1) 的随机数。返回 (是否接受, token, 拒绝时的残差分布)。"""
    ratio = 1.0 if q[draft_token] == 0 else min(1.0, p[draft_token] / q[draft_token])
    if u < ratio:
        return True, draft_token, None
    resid = [max(pi - qi, 0.0) for pi, qi in zip(p, q)]
    s = sum(resid)
    if s <= 0:
        resid, s = list(p), sum(p)
    return False, None, [x / s for x in resid]
```

**自测（本题的核心）**：解析地算出一轮投机的输出分布：

$$
\Pr[\text{输出} = t] = \underbrace{q_t \cdot \min(1, p_t/q_t)}_{\text{提议 } t \text{ 且被接受}}
+ \underbrace{P_{\text{rej}} \cdot \frac{\max(p_t - q_t, 0)}{\sum_j \max(p_j - q_j, 0)}}_{\text{拒绝后重采样到 } t}
$$

**这个和应当恒等于 $p_t$**。
参考实现在 200 组随机的 $(p, q)$ 上验证，误差小于 $10^{-9}$。

**第二个可验证的性质**：接受率恰好等于重叠系数

$$
\alpha = \sum_t q_t \cdot \min(1, p_t/q_t) = \sum_t \min(p_t, q_t) = 1 - \text{TV}(p, q)
$$

**这个恒等式解释了「为什么草稿模型要与目标模型同源」**：
两个分布越接近，总变差距离越小，接受率越高。

**常见错误**：

- 拒绝后从 $p$ 重采样（**破坏分布，是一个静默的正确性 bug**）；
- 残差不做 `max(·, 0)`（会出现负概率）；
- 忘记归一化残差；
- 认为接受率是一个可以自由调的参数
  （它由两个分布决定，只能通过换草稿模型来改变）。

**可能的追问**：温度为 0 时这个算法应该有什么性质？
（答：**应产出与非投机完全一致的 token 序列**——
这是最强的正确性测试，见[案例三](09_mock_interview_cases.md)。）

---

## E7：加速比与最优提议数

**题面**：实现投机解码的加速比公式，并求给定 $(\alpha, r)$ 下的最优提议数 $k$。

**考察点**：能不能把一个经济性判断写成可计算的形式。
**这道题很短，但它决定了 E6 的工程价值**。

```python
def spec_speedup(alpha, k, r):
    if alpha >= 1.0:
        return (k + 1) / (k * r + 1)
    return (1 - alpha ** (k + 1)) / ((1 - alpha) * (k * r + 1))


def best_k(alpha, r, kmax=64):
    return max(range(1, kmax + 1), key=lambda k: spec_speedup(alpha, k, r))
```

**自测**：$\alpha = 0.7$ 时

| $r$ | 最优 $k$ | 该点加速比 |
|---|---|---|
| 0.1 | 4 | 1.98 |
| 0.3 | 2 | 1.37 |

且 $\alpha = 0.7$、$r = 0.3$、$k = 8$ 时加速比为 **0.94——即变慢了**。
另外令 $r \to 0$、$k$ 很大时，加速比趋于 $1/(1-\alpha) = 3.33$。

**三个应当被验证的性质**：

1. **存在最优 $k$**，超过后下降；
2. **上界是 $1/(1-\alpha)$**，只在 $r \to 0$ 时可达；
3. **$\alpha$ 越高，最优点的加速比越高**。

**常见错误**：

- 认为 $k$ 越大越好；
- 忘记 $\alpha = 1$ 的边界（会除零）；
- 把加速比与接受率混为一谈。

**可能的追问**：实际系统里 $\alpha$ 怎么测？
（答：测每轮实际接受的 token 数期望 $E[\ell]$，再反推 $\alpha$——
**因为 $\alpha$ 本身不可直接观测**。）

---

## E8：流式分位数统计

**题面**：实现一个可以处理无界数据流的分位数估计器，
支持 P50 / P95 / P99，**并且报告必须包含样本量**。

**考察点**：**「分位数必须带样本量」这个纪律**。
这道题表面考数据结构，实际考指标口径的严谨性。

**关键设计决策**：

1. **定容采样**，否则内存无界；
2. **必须报告 $n$（总观测数）与实际样本数**——
   **这是本题的考点，不是附加要求**。
   小样本下的 P99 波动可能大于你想检测的改进；
3. **可复现**：给定种子应产出相同结果，否则无法用于回归测试。

```python
import math, random
from bisect import insort

class ReservoirQuantile:
    def __init__(self, capacity=4096, seed=0):
        self.capacity = capacity
        self.rng = random.Random(seed)
        self.buf = []
        self.n = 0

    def add(self, x):
        self.n += 1
        if len(self.buf) < self.capacity:
            insort(self.buf, x)
        else:
            j = self.rng.randrange(self.n)
            if j < self.capacity:
                self.buf.remove(self.buf[j])
                insort(self.buf, x)

    def quantile(self, p):
        if not self.buf:
            return None
        idx = min(len(self.buf) - 1, int(math.ceil(p * len(self.buf))) - 1)
        return self.buf[max(idx, 0)]

    def report(self):
        return {"n": self.n, "sample": len(self.buf),
                "p50": self.quantile(0.50), "p95": self.quantile(0.95),
                "p99": self.quantile(0.99)}
```

**自测**：在 50000 个对数正态分布的样本上（模拟重尾的时延分布），
容量 8192 的估计器对 P50 / P95 / P99 的相对误差均小于 15%。
**并且 `report()` 始终返回 $n$ 与实际样本数**。

**常见错误**：

- **只返回分位数不返回样本量**——这是本题最重要的失分点；
- 无界地保存全部数据；
- 用不可复现的随机源（无法用于回归测试）；
- **跨窗口平均分位数**（「过去一天的平均 P99」没有统计意义）。

**可能的追问**：为什么不用固定分桶的直方图？
（答：可以，且它更省内存与更容易合并；
**代价是精度受分桶粒度限制，而时延的量级跨度很大，
需要对数分桶才合适**。
两种方案的选择取决于「要不要跨实例合并」——
**直方图可合并，蓄水池不可**。）

---

## E9：准入控制与抢占模拟

**题面**：实现一个按 KV 页做准入控制的调度器：
请求提交时判断是否有足够的页，不足则排队；
运行中页不够时抢占某个请求。

**考察点**：调度的**资源守恒**——
在任何时刻已用页数不得超过总页数。
**这是最容易写出 bug 的一类代码**。

**关键设计决策**：

1. **准入必须在资源被消耗之前判断**（[Q032](03_serving_scheduling_and_slo_questions.md)）；
2. **需求超过总容量的请求应直接拒绝而不是排队**——
   否则它会永远排在队列里；
3. **抢占的受害者选择要考虑重算代价**。
   参考实现选「已生成最少」的请求，
   因为**重算代价是 $\text{prefill}(S_{\text{prompt}} + L_g)$，随 $L_g$ 增长**；
4. **被抢占的请求重新入队时，它的 prompt 变成「原 prompt + 已生成」**——
   **这个细节体现了你理解抢占的真实代价**。

```python
def submit(self, rid, prompt_len, expect_gen):
    need = self._pages_for(prompt_len + expect_gen)
    if need > self.total:
        self.rejected += 1
        return "rejected"                 # 永远装不下，直接拒绝
    if self.used + need <= self.total:
        self.used += need
        self.running[rid] = {"prompt": prompt_len, "gen": 0, "pages": need}
        return "admitted"
    self.waiting.append((rid, prompt_len, expect_gen))
    return "queued"

def _preempt(self, rid):
    st = self.running.pop(rid)
    self.used -= st["pages"]
    self.preempted += 1
    # 重新入队时 prompt 变长了——这就是抢占的正反馈来源
    self.waiting.insert(0, (rid, st["prompt"] + st["gen"], 0))
```

（完整实现含 `step`、受害者选择与队列回填，见
[`code/interview_exercises.py`](../../code/interview_exercises.py)。）

**自测**：

1. 需求超过总容量 → `rejected`，且不进队列；
2. 容量填满后新请求 → `queued`；
3. 连续 `step()` 20 次后，**`used <= total` 必须始终成立**。

**第 3 条是这道题的核心不变量**，应该写成断言。

**常见错误**：

- **先分配再检查**（会短暂超出容量，在真实系统里就是 OOM）；
- 把「装不下」的请求放进队列导致队头阻塞；
- 抢占时忘记归还页数；
- 重新入队时用原始 prompt 长度
  （**低估了重算代价，也就看不到抢占的正反馈**）；
- 抢占自己（要排除当前正在处理的请求）。

**可能的追问**：抢占率持续很高说明什么？
（答：**说明准入太松，应该往上游调准入而不是优化抢占实现**——
见 [Q034](03_serving_scheduling_and_slo_questions.md)。）

---

## E10：roofline 与临界批大小

**题面**：给定设备算力与带宽，写函数判断某个批大小下是算力受限还是带宽受限，
并计算权重扫描时间。

**考察点**：把 roofline 从概念变成可计算的判据。

```python
def ridge_point(flops, bw):
    return flops / bw


def critical_batch(flops, bw, bytes_per_weight):
    return ridge_point(flops, bw) * bytes_per_weight / 2


def bound_kind(batch, flops, bw, bytes_per_weight):
    b_star = critical_batch(flops, bw, bytes_per_weight)
    if batch < 0.9 * b_star:
        return "bandwidth"
    if batch > 1.1 * b_star:
        return "compute"
    return "near-ridge"


def sweep_time(weight_bytes, kv_read_bytes, bw):
    return (weight_bytes + kv_read_bytes) / bw
```

**自测**（用题面假设值：算力 $10^{15}$ FLOP/s、带宽 $2 \times 10^{12}$ B/s）：

- 临界算术强度 $I^{*} = 500$ FLOP/Byte；
- fp16 权重（2 字节）下临界批大小 $B^{*} = 500$；
- 批 8 → `bandwidth`，批 2048 → `compute`；
- **权重量化到 1 字节时 $B^{*}$ 降到 250**——
  **即量化之后更小的批就进入算力受限区**；
- 权重 140 GB、KV 读取 10 GB 时，扫描时间为 75 ms
  （**这就是 TPOT 的物理下界**）。

**注意 `bound_kind` 保留了一个 `near-ridge` 区间**。
**这是有意的**：临界点附近两种资源都接近饱和，
**给出一个明确的判断是误导性的**。

**常见错误**：

- 忘记 $B^{*}$ 与权重位宽成正比；
- 在临界点附近给出二元判断；
- 扫描时间只算权重不算 KV
  （**长上下文下 KV 读取可能占大头**）。

**可能的追问**：如果实测的单步时间远大于 `sweep_time`，说明什么？
（答：说明没有跑在带宽上限——
可能是延迟受限（kernel 启动开销）、并行度不足、或访存模式差。
**见 [Q055](04_compiler_kernel_and_quantization_questions.md) 的三分诊断**。）

---

## 编码环节的通用建议

**五条，按重要性排序**：

**（一）先说清楚你要写什么，再动手**。
一句话说明你的方案与数据结构选择，
**这能让面试官在你写错方向时及时打断**——
对双方都是节省。

**（二）主动写不变量与自测**。
E2 的「分块与整体一致」、E6 的「输出分布等于 $p$」、
E9 的「已用不超过总量」——
**这些不变量本身就是你理解概念的证据**。
**很多面试者写完就停，而写自测的人明显更少**。

**（三）边界条件要主动提，不一定要实现**。
「这里如果容量为 0 会出问题，我先假设不发生，
最后如果有时间再补」——
**这比默默忽略或者花时间写完整的防御代码都好**。

**（四）复杂度要能说出来**。
E5 的匹配是 $O(L)$、E4 的 fork 是 $O(\text{页数})$、
E8 的插入是 $O(\log C)$（二分）加 $O(C)$（列表插入）。
**能说出来说明你知道自己写的东西的代价**。

**（五）代码写不完不是致命的，思路错了才是**。
这类题的时间通常紧张，
**面试官关心的是你的方案与你写出的部分是否正确**，
而不是有没有写完。
**所以宁可写对一半，不要为了写完而跳过关键的正确性处理**。

## 关键术语

| 中文术语 | 英文 | 定义 | 单位/口径 | 关联文档 |
|---|---|---|---|---|
| 在线 softmax | online softmax | 分块累积并按最大值修正的精确 softmax | — | [Q047](04_compiler_kernel_and_quantization_questions.md) |
| 写时复制 | copy-on-write | 写入被共享的页时先复制再写 | — | [Q020](02_kv_cache_and_transformer_questions.md) |
| 残差分布 | residual distribution | 投机解码拒绝后重采样用的 $\max(p-q,0)$ 归一化分布 | — | [案例三](09_mock_interview_cases.md) |
| 重叠系数 | overlap coefficient | $\sum_t \min(p_t,q_t)$，等于接受率 | 无量纲 | [案例三](09_mock_interview_cases.md) |
| 定容采样 | reservoir sampling | 用固定内存对无界流做无偏采样 | 样本数 | [Q092](07_debug_benchmark_and_reliability_questions.md) |
| 临界批大小 | critical batch size | 使算术强度达到临界值的批大小 | token 数 | [Q045](04_compiler_kernel_and_quantization_questions.md) |
| 权重扫描时间 | weight sweep time | 把权重与需读 KV 读一遍的时间，TPOT 的物理下界 | 秒 | [Q078](06_hardware_and_datacenter_questions.md) |

## 延伸阅读

- [可运行的参考实现与自测](../../code/interview_exercises.py)
- [系统设计案例走查](09_mock_interview_cases.md)
- [题库总览](README.md)
- [模块 02：Transformer 与 KV cache](../02_transformer_and_kv_cache/)
- [模块 03：serving 引擎与调度](../03_serving_engines_and_scheduling/)
- [模块 05：解码与生成算法](../05_decoding_and_generation_algorithms/)

## 主要来源

十道题的参考实现均为本库原创，
基于模块 02–06 与题库 Q001–Q100 的机制描述实现，
**全部通过 [`code/interview_exercises.py`](../../code/interview_exercises.py) 中的自测**
（运行 `python3 code/interview_exercises.py` 可复现）。

**不含任何需要外部核验的产品实现细节**。
本文档的实现是**教学用的最小可运行版本**，
不对应任何具体推理框架的实际代码——
受当前环境的网络出口策略限制，本库无法访问任何推理框架的源码
（详见 [AGENTS.md 第 11 节](../../AGENTS.md)），
**因此不声称这些实现与任何框架的做法一致**。

| 类别 | 说明 | 披露标签 |
|---|---|---|
| 十道题的参考实现与自测 | 本库原创，可复现 | `独立可复现实验` |
| 题面中的硬件假设值 | 为演示推导而设定 | — |
| 具体框架的实际实现方式 | **本文档未声称** | `待核实` |

## 更新记录

| 日期 | 版本 | 变更 | 核验人 |
|---|---|---|---|
| 2026-07-29 | v0.1 | 初稿：十道编码题与可运行的参考实现，全部自测通过 | — |
