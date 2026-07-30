# -*- coding: utf-8 -*-
"""验证 doc 10 的全部参考实现。运行本文件应无断言失败。"""
import math
import heapq
import random
from bisect import insort
from collections import defaultdict

# ---------- E1: KV 容量与并发上界 ----------

def kv_bytes_per_token(n_layers, n_kv_heads, head_dim, bytes_per_elem):
    return 2 * n_layers * n_kv_heads * head_dim * bytes_per_elem


def max_concurrency(mem_avail, weight_bytes, act_bytes, m_tok, seq_len):
    free = mem_avail - weight_bytes - act_bytes
    if free <= 0:
        return 0
    return int(free // (m_tok * seq_len))


def test_e1():
    m = kv_bytes_per_token(80, 8, 128, 2)
    assert m == 2 * 80 * 8 * 128 * 2 == 327680
    GiB = 1024 ** 3
    c = max_concurrency(80 * GiB, 40 * GiB, 2 * GiB, m, 4096)
    assert c == int((38 * GiB) // (327680 * 4096))
    assert c == 30, c
    assert max_concurrency(10, 20, 0, 1, 1) == 0
    print("E1 ok: m_tok =", m, "bytes/token;并发上界 =", c)


# ---------- E2: 在线 softmax 的分块合并 ----------

def online_softmax_merge(blocks):
    """blocks: [(m_i, l_i, o_i)]，m 为块内最大值、l 为指数和、o 为加权和向量。
    返回合并后的 (m, l, o)。o 为 list[float]。"""
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


def block_stats(scores, values):
    """对一个块直接算 (m, l, o)。"""
    m = max(scores)
    exps = [math.exp(s - m) for s in scores]
    l = sum(exps)
    d = len(values[0])
    o = [sum(e * v[j] for e, v in zip(exps, values)) for j in range(d)]
    return m, l, o


def attention_reference(scores, values):
    m = max(scores)
    exps = [math.exp(s - m) for s in scores]
    l = sum(exps)
    d = len(values[0])
    return [sum(e * v[j] for e, v in zip(exps, values)) / l for j in range(d)]


def test_e2():
    random.seed(0)
    n, d = 17, 4
    scores = [random.uniform(-30, 30) for _ in range(n)]
    values = [[random.uniform(-1, 1) for _ in range(d)] for _ in range(n)]
    ref = attention_reference(scores, values)
    for bs in (1, 2, 5, 17):
        blocks = [block_stats(scores[i:i + bs], values[i:i + bs])
                  for i in range(0, n, bs)]
        m, l, o = online_softmax_merge(blocks)
        got = [x / l for x in o]
        for a, b in zip(ref, got):
            assert abs(a - b) < 1e-9, (bs, a, b)
    print("E2 ok: 分块大小 1/2/5/17 的合并结果与整体计算在 1e-9 内一致")


# ---------- E3: 采样（temperature / top-k / top-p / min-p） ----------

def softmax(logits):
    m = max(logits)
    e = [math.exp(x - m) for x in logits]
    s = sum(e)
    return [x / s for x in e]


def apply_sampling_filters(logits, temperature=1.0, top_k=None,
                           top_p=None, min_p=None):
    """返回过滤并归一化后的概率分布（未被选中的位置为 0.0）。
    顺序：temperature -> top_k -> top_p -> min_p。顺序不可交换。"""
    if temperature <= 0:
        out = [0.0] * len(logits)
        out[max(range(len(logits)), key=lambda i: logits[i])] = 1.0
        return out
    scaled = [x / temperature for x in logits]
    probs = softmax(scaled)
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
            if cum >= top_p:
                break
        keep &= chosen
    if min_p is not None:
        p_max = max(probs[i] for i in keep)
        keep = {i for i in keep if probs[i] >= min_p * p_max}
    total = sum(probs[i] for i in keep)
    return [probs[i] / total if i in keep else 0.0 for i in range(len(probs))]


def test_e3():
    logits = [2.0, 1.0, 0.5, 0.0, -1.0]
    p = apply_sampling_filters(logits, temperature=0.0)
    assert p == [1.0, 0, 0, 0, 0]
    p = apply_sampling_filters(logits, top_k=2)
    assert sum(1 for x in p if x > 0) == 2
    assert abs(sum(p) - 1.0) < 1e-12
    # top-p 的定义包含「跨过阈值的那一个」，所以 0.6 在此分布下留下 2 个
    a = apply_sampling_filters(logits, top_p=0.6)
    assert sum(1 for x in a if x > 0) == 2, a
    # 温度会改变 nucleus 的大小：这就是「顺序不可交换」的具体表现
    sharp = apply_sampling_filters(logits, temperature=0.5, top_p=0.9)
    flat = apply_sampling_filters(logits, temperature=2.0, top_p=0.9)
    assert sum(1 for x in sharp if x > 0) == 2, sharp
    assert sum(1 for x in flat if x > 0) == 4, flat
    # min_p 相对最大概率裁剪
    b = apply_sampling_filters(logits, min_p=0.5)
    base = softmax(logits)
    expect = {i for i, q in enumerate(base) if q >= 0.5 * max(base)}
    assert {i for i, x in enumerate(b) if x > 0} == expect
    # 温度升高使分布更平
    def entropy(q):
        return -sum(x * math.log(x) for x in q if x > 0)
    assert entropy(apply_sampling_filters(logits, temperature=2.0)) > \
           entropy(apply_sampling_filters(logits, temperature=0.5))
    print("E3 ok: 温度 0 退化为 argmax；top-k/top-p/min-p 语义与归一化正确")


# ---------- E4: 分页 KV 的页表与写时复制 ----------

class PagedKV:
    def __init__(self, n_pages, page_size):
        self.page_size = page_size
        self.free = list(range(n_pages))
        self.refcount = defaultdict(int)
        self.tables = {}   # seq_id -> [page_id, ...]
        self.lengths = {}  # seq_id -> token 数

    def _alloc(self):
        if not self.free:
            raise MemoryError("no free page")
        pid = self.free.pop()
        self.refcount[pid] = 1
        return pid

    def new_sequence(self, seq_id):
        self.tables[seq_id] = []
        self.lengths[seq_id] = 0

    def append(self, seq_id, n_tokens=1):
        for _ in range(n_tokens):
            L = self.lengths[seq_id]
            off = L % self.page_size
            if off == 0:
                self.tables[seq_id].append(self._alloc())
            else:
                # 写时复制：末页若被共享，先复制再写
                last = self.tables[seq_id][-1]
                if self.refcount[last] > 1:
                    new = self._alloc()
                    self.refcount[last] -= 1
                    self.tables[seq_id][-1] = new
            self.lengths[seq_id] = L + 1

    def fork(self, src, dst):
        """共享全部已满页与末页（末页写时复制）。"""
        self.tables[dst] = list(self.tables[src])
        self.lengths[dst] = self.lengths[src]
        for pid in self.tables[dst]:
            self.refcount[pid] += 1

    def free_sequence(self, seq_id):
        for pid in self.tables.pop(seq_id):
            self.refcount[pid] -= 1
            if self.refcount[pid] == 0:
                del self.refcount[pid]
                self.free.append(pid)
        self.lengths.pop(seq_id)

    def used_pages(self):
        return len(self.refcount)


def test_e4():
    kv = PagedKV(n_pages=8, page_size=4)
    kv.new_sequence("a")
    kv.append("a", 6)                 # 2 页：满页 + 半页
    assert len(kv.tables["a"]) == 2
    assert kv.used_pages() == 2
    kv.fork("a", "b")                 # 共享 2 页
    assert kv.used_pages() == 2, kv.used_pages()
    page_before = kv.tables["b"][-1]
    kv.append("b", 1)                 # 触发末页写时复制
    assert kv.tables["b"][-1] != page_before
    assert kv.tables["a"][-1] == page_before
    assert kv.used_pages() == 3
    # 满页仍然共享
    assert kv.tables["a"][0] == kv.tables["b"][0]
    assert kv.refcount[kv.tables["a"][0]] == 2
    kv.free_sequence("a")
    assert kv.refcount[kv.tables["b"][0]] == 1
    kv.free_sequence("b")
    assert kv.used_pages() == 0
    assert len(kv.free) == 8
    print("E4 ok: 共享、写时复制、引用计数与页回收均正确")


# ---------- E5: 前缀缓存的 trie 匹配 ----------

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

    def size(self):
        return 1 + sum(c.size() for c in self.children.values())


def test_e5():
    t = PrefixTrie()
    t.insert([1, 2, 3, 4])
    assert t.match([1, 2, 3, 4]) == 4
    assert t.match([1, 2, 9]) == 2
    assert t.match([9]) == 0
    t.insert([1, 2, 5])
    assert t.match([1, 2, 5, 6]) == 3
    # 节点数：root + 1,2,3,4 + 5
    assert t.size() == 6, t.size()
    # 共享前缀的节省：两条 4+3=7 token 的序列只用了 5 个非根节点
    print("E5 ok: 最长前缀匹配与共享节点计数正确")


# ---------- E6: 投机解码的接受-重采样 ----------

def speculative_accept(p, q, draft_token, u):
    """标准接受判据：以 min(1, p[t]/q[t]) 接受。u 为 [0,1) 的随机数。
    拒绝时从残差分布 max(p-q,0) 归一化后重采样（这里返回该分布）。"""
    ratio = 1.0 if q[draft_token] == 0 else min(1.0, p[draft_token] / q[draft_token])
    if u < ratio:
        return True, draft_token, None
    resid = [max(pi - qi, 0.0) for pi, qi in zip(p, q)]
    s = sum(resid)
    if s <= 0:                      # 退化情形：直接用 p
        resid, s = list(p), sum(p)
    return False, None, [x / s for x in resid]


def spec_output_distribution(p, q):
    """解析地算出「一轮投机」的输出分布，应当恰好等于 p。"""
    n = len(p)
    out = [0.0] * n
    for t in range(n):
        acc = min(1.0, p[t] / q[t]) if q[t] > 0 else 0.0
        out[t] += q[t] * acc                       # 草稿提议 t 且被接受
    rej = sum(q[t] * (1 - (min(1.0, p[t] / q[t]) if q[t] > 0 else 0.0))
              for t in range(n))
    resid = [max(pi - qi, 0.0) for pi, qi in zip(p, q)]
    s = sum(resid)
    if s > 0:
        for t in range(n):
            out[t] += rej * resid[t] / s
    return out


def test_e6():
    random.seed(1)
    for _ in range(200):
        n = random.randint(2, 6)
        p = [random.random() for _ in range(n)]
        q = [random.random() for _ in range(n)]
        p = [x / sum(p) for x in p]
        q = [x / sum(q) for x in q]
        out = spec_output_distribution(p, q)
        assert abs(sum(out) - 1.0) < 1e-9
        for a, b in zip(p, out):
            assert abs(a - b) < 1e-9, (a, b)
    # 接受率等于重叠系数 sum min(p,q)
    p = [0.5, 0.3, 0.2]
    q = [0.2, 0.3, 0.5]
    alpha = sum(q[t] * min(1.0, p[t] / q[t]) for t in range(3))
    assert abs(alpha - sum(min(a, b) for a, b in zip(p, q))) < 1e-12
    ok, tok, _ = speculative_accept(p, q, 1, 0.0)
    assert ok and tok == 1
    ok, tok, r = speculative_accept([0.0, 1.0], [1.0, 0.0], 0, 0.5)
    assert not ok and abs(sum(r) - 1.0) < 1e-12 and r[1] == 1.0
    print("E6 ok: 输出分布恒等于目标分布 p；接受率等于重叠系数")


# ---------- E7: 加速比与最优提议数 ----------

def spec_speedup(alpha, k, r):
    if alpha >= 1.0:
        return (k + 1) / (k * r + 1)
    return (1 - alpha ** (k + 1)) / ((1 - alpha) * (k * r + 1))


def best_k(alpha, r, kmax=64):
    return max(range(1, kmax + 1), key=lambda k: spec_speedup(alpha, k, r))


def test_e7():
    assert abs(spec_speedup(0.7, 4, 0.1) - 1.98) < 0.005
    assert abs(spec_speedup(0.7, 8, 0.3) - 0.94) < 0.005
    assert best_k(0.7, 0.1) == 4, best_k(0.7, 0.1)
    assert best_k(0.7, 0.3) == 2, best_k(0.7, 0.3)
    # r -> 0 且 k 大时趋于 1/(1-alpha)
    assert abs(spec_speedup(0.7, 200, 1e-9) - 1 / 0.3) < 1e-3
    # alpha 越高上界越高
    assert spec_speedup(0.9, best_k(0.9, 0.1), 0.1) > \
           spec_speedup(0.7, best_k(0.7, 0.1), 0.1)
    print("E7 ok: 加速比、最优 k 与上界 1/(1-α) 均符合")


# ---------- E8: 流式分位数（P50/P95/P99） ----------

class ReservoirQuantile:
    """定容蓄水池 + 排序，用于对无界流估计分位数。
    可复现（给定 seed），且报告样本量——这是本练习的考点。"""

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
                # 替换第 j 个（按当前排序位置替换会引入偏差，故按值定位）
                old = self.buf[j]
                self.buf.remove(old)
                insort(self.buf, x)

    def quantile(self, p):
        if not self.buf:
            return None
        idx = min(len(self.buf) - 1, int(math.ceil(p * len(self.buf))) - 1)
        return self.buf[max(idx, 0)]

    def report(self):
        return {"n": self.n, "sample": len(self.buf),
                "p50": self.quantile(0.50),
                "p95": self.quantile(0.95),
                "p99": self.quantile(0.99)}


def exact_quantile(xs, p):
    s = sorted(xs)
    idx = min(len(s) - 1, int(math.ceil(p * len(s))) - 1)
    return s[max(idx, 0)]


def test_e8():
    random.seed(7)
    data = [random.lognormvariate(0, 1) * 100 for _ in range(50000)]
    q = ReservoirQuantile(capacity=8192, seed=42)
    for x in data:
        q.add(x)
    rep = q.report()
    assert rep["n"] == 50000 and rep["sample"] == 8192
    for p in (0.50, 0.95, 0.99):
        exact = exact_quantile(data, p)
        est = rep[f"p{int(p*100)}"]
        rel = abs(est - exact) / exact
        assert rel < 0.15, (p, exact, est, rel)
    # 小样本时 P99 不可靠：样本量必须被报告
    small = ReservoirQuantile(capacity=50, seed=1)
    for x in data[:200]:
        small.add(x)
    assert small.report()["sample"] == 50
    print("E8 ok: 分位数估计相对误差 < 15%，且 report 始终带样本量 n")


# ---------- E9: 准入控制与抢占的资源模拟 ----------

class KVScheduler:
    """按 KV 页配额做准入；不足时按「已生成最少」抢占（重算代价最小）。"""

    def __init__(self, total_pages, page_size):
        self.total = total_pages
        self.page_size = page_size
        self.used = 0
        self.running = {}   # rid -> dict(prompt, gen, pages)
        self.waiting = []
        self.preempted = 0
        self.admitted = 0
        self.rejected = 0

    def _pages_for(self, n_tok):
        return math.ceil(n_tok / self.page_size)

    def submit(self, rid, prompt_len, expect_gen):
        need = self._pages_for(prompt_len + expect_gen)
        if need > self.total:
            self.rejected += 1
            return "rejected"
        if self.used + need <= self.total:
            self.used += need
            self.running[rid] = {"prompt": prompt_len, "gen": 0, "pages": need}
            self.admitted += 1
            return "admitted"
        self.waiting.append((rid, prompt_len, expect_gen))
        return "queued"

    def step(self):
        """所有在跑请求各生成一个 token；页不足时抢占。"""
        for rid, st in list(self.running.items()):
            st["gen"] += 1
            need = self._pages_for(st["prompt"] + st["gen"])
            if need > st["pages"]:
                if self.used + 1 > self.total:
                    self._preempt_one(exclude=rid)
                if self.used + 1 <= self.total:
                    self.used += 1
                    st["pages"] = need
                else:
                    self._preempt(rid)
        self._admit_from_queue()

    def _preempt_one(self, exclude):
        cands = [(st["gen"], rid) for rid, st in self.running.items()
                 if rid != exclude]
        if not cands:
            return
        _, victim = min(cands)
        self._preempt(victim)

    def _preempt(self, rid):
        st = self.running.pop(rid)
        self.used -= st["pages"]
        self.preempted += 1
        # 重算代价 = prompt + 已生成
        self.waiting.insert(0, (rid, st["prompt"] + st["gen"], 0))

    def _admit_from_queue(self):
        rest = []
        for rid, plen, egen in self.waiting:
            need = self._pages_for(plen + egen)
            if self.used + need <= self.total:
                self.used += need
                self.running[rid] = {"prompt": plen, "gen": 0, "pages": need}
                self.admitted += 1
            else:
                rest.append((rid, plen, egen))
        self.waiting = rest


def test_e9():
    # 需要 ceil(200/16)=13 页 > 总容量 10 页，应直接拒绝而不是排队
    s2 = KVScheduler(total_pages=10, page_size=16)
    assert s2.submit("r1", 100, 100) == "rejected"
    assert s2.rejected == 1

    s3 = KVScheduler(total_pages=10, page_size=16)
    assert s3.submit("a", 16, 16) == "admitted"       # 2 页
    assert s3.submit("b", 16, 16) == "admitted"       # 2 页
    assert s3.used == 4
    for _ in range(20):
        s3.step()
    assert s3.used <= s3.total
    # 填满后新请求排队
    s4 = KVScheduler(total_pages=4, page_size=16)
    assert s4.submit("a", 16, 16) == "admitted"
    assert s4.submit("b", 16, 16) == "admitted"
    assert s4.submit("c", 16, 16) == "queued"
    assert s4.used == 4 and len(s4.waiting) == 1
    print("E9 ok: 准入拒绝、排队、页增长与抢占均不超过总容量")


# ---------- E10: roofline 与临界批大小 ----------

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


def test_e10():
    flops, bw = 1e15, 2e12            # 题面假设值
    assert abs(ridge_point(flops, bw) - 500) < 1e-9
    assert abs(critical_batch(flops, bw, 2) - 500) < 1e-9
    assert bound_kind(8, flops, bw, 2) == "bandwidth"
    assert bound_kind(2048, flops, bw, 2) == "compute"
    assert bound_kind(500, flops, bw, 2) == "near-ridge"
    # 位宽减半使临界批减半：更小的批就进入算力受限
    assert abs(critical_batch(flops, bw, 1) - 250) < 1e-9
    t = sweep_time(140e9, 10e9, 2e12)
    assert abs(t - 0.075) < 1e-12
    print(f"E10 ok: I*={ridge_point(flops,bw):.0f} FLOP/B，B*={critical_batch(flops,bw,2):.0f}，"
          f"扫描时间={t*1000:.1f} ms")


if __name__ == "__main__":
    test_e1(); test_e2(); test_e3(); test_e4(); test_e5()
    test_e6(); test_e7(); test_e8(); test_e9(); test_e10()
    print("\n全部 10 题参考实现通过。")
