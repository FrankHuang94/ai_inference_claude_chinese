#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""面试题库覆盖审计：总数、类别配额、答案完整性、必填字段、重复检测。

用法：
  python3 scripts/interview_coverage_report.py           # 建库过程中（未满 100 题不阻断）
  python3 scripts/interview_coverage_report.py --final   # 最终验收（强制恰好 100 题且配额吻合）

退出码：0 = 通过；1 = 存在阻断问题。
"""
import csv
import difflib
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

QUOTA = {
    "推理基础、指标、排队论、成本": 12,
    "Transformer、prefill/decode 与 KV Cache": 16,
    "Serving、batching、调度、QoS": 16,
    "Compiler、kernel、量化与 runtime": 14,
    "分布式、MoE、网络与 disaggregation": 18,
    "硬件、HBM、数据中心、edge": 12,
    "Debug、benchmark、可靠性、安全": 7,
    "公司、论文与战略讨论": 5,
}
TOTAL = 100
assert sum(QUOTA.values()) == TOTAL

REQUIRED = ["question_id", "topic", "difficulty", "question", "reference_answer",
            "common_mistakes", "follow_up_questions", "related_docs", "format"]
MIN_ANSWER_CHARS = 300     # 完整参考答案的下限；提纲式答案会被拦下
SIMILARITY = 0.85


def main() -> int:
    final = "--final" in sys.argv
    p = DATA / "interview_questions.csv"
    if not p.exists():
        print("[interview_coverage] interview_questions.csv 不存在")
        return 1
    with p.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    blocking, warnings = [], []
    counts = {k: 0 for k in QUOTA}
    unknown_topics = {}
    for r in rows:
        t = (r.get("topic") or "").strip()
        if t in counts:
            counts[t] += 1
        else:
            unknown_topics[t] = unknown_topics.get(t, 0) + 1

    for t, n in unknown_topics.items():
        blocking.append(f"topic 不在配额表内：`{t}`（{n} 条）")

    n = len(rows)
    if n > TOTAL:
        blocking.append(f"题目总数 {n} 超过硬性上限 {TOTAL}")
    elif n < TOTAL:
        (blocking if final else warnings).append(
            f"题目总数 {n}，尚未达到 {TOTAL}（缺 {TOTAL - n} 题）")

    for topic, quota in QUOTA.items():
        c = counts[topic]
        if c > quota:
            blocking.append(f"类别「{topic}」{c} 题，超出配额 {quota}")
        elif c < quota and final:
            blocking.append(f"类别「{topic}」{c} 题，未达配额 {quota}")

    ids = set()
    for r in rows:
        qid = (r.get("question_id") or "?").strip()
        if qid in ids:
            blocking.append(f"question_id 重复：`{qid}`")
        ids.add(qid)
        for col in REQUIRED:
            if not (r.get(col) or "").strip():
                blocking.append(f"`{qid}` 必填字段 `{col}` 为空")
        ans = (r.get("reference_answer") or "").strip()
        if ans and len(ans) < MIN_ANSWER_CHARS:
            blocking.append(f"`{qid}` reference_answer 仅 {len(ans)} 字，"
                            f"疑为提纲而非完整答案（下限 {MIN_ANSWER_CHARS}）")
        if not (r.get("related_docs") or "").strip():
            blocking.append(f"`{qid}` 未链接任何数据库文档")

    qs = [((r.get("question_id") or "?"), (r.get("question") or "")) for r in rows]
    for i in range(len(qs)):
        for j in range(i + 1, len(qs)):
            ratio = difflib.SequenceMatcher(None, qs[i][1], qs[j][1]).ratio()
            if ratio >= SIMILARITY:
                warnings.append(f"题目疑似重复（相似度 {ratio:.2f}）：`{qs[i][0]}` 与 `{qs[j][0]}`")

    REPORTS.mkdir(exist_ok=True)
    L = ["# 面试题库覆盖报告", "", "> 生成于 `scripts/interview_coverage_report.py`", "",
         f"- 模式：{'最终验收（--final）' if final else '建库过程'}",
         f"- **题目总数：{n} / {TOTAL}**", "",
         "## 类别配额", "", "| 类别 | 当前 | 配额 | 缺口 |", "|---|---:|---:|---:|"]
    for topic, quota in QUOTA.items():
        L.append(f"| {topic} | {counts[topic]} | {quota} | {quota - counts[topic]} |")
    L += [f"| **合计** | **{n}** | **{TOTAL}** | **{TOTAL - n}** |", "",
          f"## 阻断问题：{len(blocking)}", ""]
    L += [f"- {x}" for x in blocking] if blocking else ["无。"]
    L += ["", f"## 告警：{len(warnings)}", ""]
    L += [f"- {x}" for x in warnings] if warnings else ["无。"]
    (REPORTS / "interview_coverage_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"[interview_coverage] 题目 {n}/{TOTAL}，阻断 {len(blocking)}，告警 {len(warnings)}")
    for x in blocking[:20]:
        print(f"  ✗ {x}")
    for x in warnings[:10]:
        print(f"  ! {x}")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
