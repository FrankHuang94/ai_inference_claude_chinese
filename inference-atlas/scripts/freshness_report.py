#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""时效性复核报告：扫描 CSV 与文档头部的核验日期，标记逾期项。

复核周期（天）按内容类型区分；逾期项按优先级排序输出。
退出码：始终 0（逾期是待办提示，不阻断提交）。
"""
import csv
import datetime as dt
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"
REPORTS = ROOT / "reports"
TODAY = dt.date.today()

# csv 名 -> (复核周期天数, 日期列, 标识列)
PERIODS = {
    "models": (90, "last_verified_date", "model_id"),
    "cloud_pricing": (90, "last_verified_date", "pricing_id"),
    "inference_engines": (90, "last_verified_date", "engine_id"),
    "companies": (90, "last_verified_date", "organization"),
    "company_events": (90, "last_verified_date", "event_id"),
    "market_transactions": (90, "last_verified_date", "transaction_id"),
    "accelerators": (180, "last_verified_date", "accelerator_id"),
    "memory_technologies": (180, "last_verified_date", "memory_id"),
    "networking_technologies": (180, "last_verified_date", "network_id"),
    "server_platforms": (180, "last_verified_date", "platform_id"),
    "benchmarks": (180, "last_verified_date", "benchmark_id"),
    "deployment_cases": (180, "last_verified_date", "case_id"),
    "techniques": (365, "last_verified_date", "technique_id"),
    "papers": (365, "last_verified_date", "paper_id"),
    "glossary": (365, "last_verified_date", "term_id"),
}
DOC_PERIOD = {"高": 90, "中": 180, "低": 365}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse(s):
    s = (s or "").strip()
    return dt.date.fromisoformat(s) if DATE_RE.match(s) else None


def main() -> int:
    overdue, upcoming, total = [], [], 0

    for name, (period, col, idcol) in PERIODS.items():
        p = DATA / f"{name}.csv"
        if not p.exists():
            continue
        with p.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                d = parse(row.get(col))
                if not d:
                    continue
                total += 1
                age = (TODAY - d).days
                item = (f"{name}.csv", row.get(idcol, "?"), d.isoformat(), age, period)
                if age > period:
                    overdue.append(item)
                elif age > period - 30:
                    upcoming.append(item)

    for md in sorted(DOCS.rglob("*.md")):
        if md.name == "README.md":
            continue
        head = md.read_text(encoding="utf-8")[:1500]
        m = re.search(r"最后核验[：:]\s*(\d{4}-\d{2}-\d{2})", head)
        lv = re.search(r"时效性等级[：:]\s*([高中低])", head)
        if not m:
            continue
        total += 1
        d, period = dt.date.fromisoformat(m.group(1)), DOC_PERIOD.get(lv.group(1) if lv else "中", 180)
        age = (TODAY - d).days
        item = (str(md.relative_to(ROOT)), "-", d.isoformat(), age, period)
        if age > period:
            overdue.append(item)
        elif age > period - 30:
            upcoming.append(item)

    overdue.sort(key=lambda x: x[3] - x[4], reverse=True)
    REPORTS.mkdir(exist_ok=True)
    L = ["# 时效性复核报告", "", "> 生成于 `scripts/freshness_report.py`", "",
         f"- 基准日期：{TODAY.isoformat()}", f"- 带核验日期的条目：{total}",
         f"- **逾期：{len(overdue)}** ｜ 30 天内到期：{len(upcoming)}", "",
         "## 逾期（按超期天数排序，优先处理）", ""]
    if overdue:
        L += ["| 来源 | 条目 | 最后核验 | 已过天数 | 周期 | 超期 |",
              "|---|---|---|---:|---:|---:|"]
        L += [f"| {a} | `{b}` | {c} | {d} | {e} | {d - e} |" for a, b, c, d, e in overdue]
    else:
        L.append("无逾期条目。")
    L += ["", "## 30 天内到期", ""]
    if upcoming:
        L += ["| 来源 | 条目 | 最后核验 | 已过天数 | 周期 |", "|---|---|---|---:|---:|"]
        L += [f"| {a} | `{b}` | {c} | {d} | {e} |" for a, b, c, d, e in upcoming]
    else:
        L.append("无。")
    (REPORTS / "freshness_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"[freshness_report] 条目 {total}，逾期 {len(overdue)}，30 天内到期 {len(upcoming)}")
    print("[freshness_report] 报告 → reports/freshness_report.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
