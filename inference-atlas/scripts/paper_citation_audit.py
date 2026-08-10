#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""论文引用审计：papers.csv 完整性 + 与 references.bib 的双向一致性。

退出码：0 = 通过；1 = 存在问题。
"""
import csv
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

CATEGORIES = {
    "Transformer Inference", "KV Cache", "Attention Optimization", "Serving and Scheduling",
    "Batching", "Speculative Decoding", "Quantization", "Compression", "Compilers",
    "Runtime Systems", "Kernels", "Distributed Inference", "MoE Serving",
    "Hardware Architecture", "Memory Systems", "Networking", "Datacenter Systems",
    "Edge Inference", "Benchmarking", "Reliability", "Security", "Agents", "Reasoning",
    "Multimodal", "Economics",
}
SUBSTANTIVE = ["one_sentence_contribution", "technical_summary", "inference_relevance",
               "limitations"]
EMPTYISH = {"", "无", "n/a", "N/A", "TODO", "-"}


def main() -> int:
    p = DATA / "papers.csv"
    if not p.exists():
        print("[paper_citation_audit] papers.csv 不存在")
        return 1
    with p.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    issues, pending, seen_ids, seen_titles = [], [], set(), set()
    for r in rows:
        pid = r.get("paper_id", "?")
        if pid in seen_ids:
            issues.append((pid, "paper_id 重复"))
        seen_ids.add(pid)
        t = (r.get("title") or "").strip().lower()
        if t in seen_titles:
            issues.append((pid, f"标题重复：{r.get('title')}"))
        seen_titles.add(t)
        if not re.match(r"^P-\d{3}$", pid):
            issues.append((pid, "paper_id 格式应为 P-XXX"))
        cat = (r.get("category") or "").strip()
        if cat not in CATEGORIES:
            issues.append((pid, f"category 不在枚举内：{cat}"))
        for col in SUBSTANTIVE:
            if (r.get(col) or "").strip() in EMPTYISH:
                issues.append((pid, f"`{col}` 缺少实质内容"))
        status = (r.get("citation_status") or "").strip()
        if status not in {"已核验", "待核实"}:
            issues.append((pid, f"citation_status 不在枚举内：{status}"))
        elif status == "待核实":
            # 待核实 是 schema 的合法取值，不是格式错误。
            # 它记录的是「尚未打开一手来源」这一事实性欠账：单独计数并列出，
            # 但不阻断 QA 门禁——否则在出口策略封锁一手来源的环境下，
            # 唯一能让门禁变绿的做法就是谎报 已核验，这与 AGENTS.md 第 11 节直接冲突。
            pending.append((pid, r.get("title", "")))
        url = (r.get("arxiv_or_doi_url") or "").strip()
        if not url.startswith("https://"):
            issues.append((pid, f"arxiv_or_doi_url 非 https 一手链接：{url}"))
        d = (r.get("last_verified_date") or "").strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", d):
            issues.append((pid, f"last_verified_date 非 YYYY-MM-DD：{d}"))

    bib = DATA / "references.bib"
    bib_txt = bib.read_text(encoding="utf-8") if bib.exists() else ""
    bib_ids = set(re.findall(r"paper_id:\s*(P-\d{3})", bib_txt))
    bib_keys = re.findall(r"@\w+\{([^,]+),", bib_txt)
    for pid in seen_ids:
        if pid not in bib_ids:
            issues.append((pid, "references.bib 中缺少对应条目（note 需含 paper_id）"))
    for bid in bib_ids - seen_ids:
        issues.append((bid, "references.bib 中的条目在 papers.csv 中不存在"))
    if len(bib_keys) != len(set(bib_keys)):
        issues.append(("-", "references.bib 存在重复 citation key"))

    verified = len(rows) - len(pending)
    REPORTS.mkdir(exist_ok=True)
    L = ["# 论文引用审计", "", "> 生成于 `scripts/paper_citation_audit.py`", "",
         f"- papers.csv 记录：{len(rows)}（最终目标 ≥ 550 条已核验来源）",
         f"- references.bib 条目：{len(bib_keys)}",
         f"- `citation_status=已核验`：{verified}",
         f"- `citation_status=待核实`：{len(pending)}（**不阻断门禁**，见下）",
         f"- **阻断性问题：{len(issues)}**", ""]
    if issues:
        L += ["## 阻断性问题", "", "| 条目 | 问题 |", "|---|---|"] + \
             [f"| `{a}` | {b} |" for a, b in issues] + [""]
    else:
        L += ["## 阻断性问题", "", "无。", ""]
    L += ["## 待核实清单（书目元数据尚未在一手来源上确认）", ""]
    if pending:
        L += ["> `已核验` 的判定标准见 [`data/schemas/papers_schema.md`](../data/schemas/papers_schema.md)：",
              "> **必须实际打开原文**确认标题、作者、年份与 venue。",
              "> 当前环境的出口策略拒绝 arxiv、USENIX、ACL、ACM 等一手来源"
              "（见 [`AGENTS.md`](../AGENTS.md) 第 11 节），",
              "> 因此下列条目一律保持 `待核实`，**不得**为了让门禁变绿而改填 `已核验`。", "",
              "| 条目 | 标题 |", "|---|---|"] + \
             [f"| `{a}` | {b} |" for a, b in pending]
    else:
        L.append("无。")
    (REPORTS / "paper_citation_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"[paper_citation_audit] 论文 {len(rows)}（已核验 {verified} / 待核实 {len(pending)}），"
          f"bib 条目 {len(bib_keys)}，阻断性问题 {len(issues)}")
    for a, b in issues[:20]:
        print(f"  ✗ {a}: {b}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
