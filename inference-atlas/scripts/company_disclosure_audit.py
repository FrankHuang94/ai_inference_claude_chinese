#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公司信息披露审计：官方链接、披露等级、客户关系、事件时效、预测写成事实。

退出码：0 = 通过或暂无记录；1 = 存在问题。
"""
import csv
import datetime as dt
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs" / "14_company_and_ecosystem_landscape"
REPORTS = ROOT / "reports"
TODAY = dt.date.today()

DISCLOSURE = {"官方披露", "技术文档披露", "开源代码/配置披露", "独立可复现实验",
              "可信第三方估计", "未公开", "待核实"}
PLACEHOLDER = {"未公开", "待核实", "不适用"}
# 预测/传闻语气——不得与已披露事实混写
SPECULATIVE = re.compile(r"(据悉|知情人士|传闻|预计将|有望|或将|业内人士|据报道|坊间|听说)")
ABSOLUTE = re.compile(r"(最快|最强|最低成本|最大的|全球领先|行业第一|遥遥领先|无可匹敌)")
STALE_EVENT_DAYS = 365


def main() -> int:
    issues = []
    cpath = DATA / "companies.csv"
    rows = []
    if cpath.exists():
        with cpath.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))

    for r in rows:
        org = r.get("organization", "?")
        url = (r.get("official_source_url") or "").strip()
        if not url.startswith("https://"):
            issues.append((org, "缺少官方一手来源链接", url))
        if (r.get("key_risks") or "").strip() in ("", "无"):
            issues.append((org, "key_risks 必填且不得为空", ""))
        cust = (r.get("key_customers_or_partners") or "").strip()
        if cust and cust not in PLACEHOLDER and SPECULATIVE.search(cust):
            issues.append((org, "客户/伙伴字段含传闻语气，未确认关系应填 `未公开`", cust[:60]))
        for col in ("public_performance_claims", "key_strengths", "inference_positioning"):
            v = (r.get(col) or "").strip()
            if ABSOLUTE.search(v):
                issues.append((org, f"`{col}` 含无来源绝对化表达", v[:60]))
        d = (r.get("last_verified_date") or "").strip()
        if re.match(r"^\d{4}-\d{2}-\d{2}$", d):
            age = (TODAY - dt.date.fromisoformat(d)).days
            if age > 90:
                issues.append((org, f"公司信息已 {age} 天未复核（周期 90 天）", d))

    epath = DATA / "company_events.csv"
    events = []
    if epath.exists():
        with epath.open(encoding="utf-8", newline="") as f:
            events = list(csv.DictReader(f))
    for e in events:
        eid = e.get("event_id", "?")
        if (e.get("disclosure_level") or "").strip() not in DISCLOSURE:
            issues.append((eid, "事件披露等级非法或缺失", e.get("disclosure_level", "")))
        st = (e.get("source_type") or "").strip()
        dl = (e.get("disclosure_level") or "").strip()
        if st == "第三方报道" and dl == "官方披露":
            issues.append((eid, "第三方报道不得标记为官方披露", f"{st}/{dl}"))
        ed = (e.get("event_date") or "").strip()
        if re.match(r"^\d{4}-\d{2}-\d{2}$", ed):
            if (TODAY - dt.date.fromisoformat(ed)).days > STALE_EVENT_DAYS:
                issues.append((eid, "事件已超过一年，确认是否仍为 latest_material_event", ed))

    doc_findings = []
    if DOCS.is_dir():
        for md in sorted(DOCS.glob("*.md")):
            if md.name == "README.md":
                continue
            for i, line in enumerate(md.read_text(encoding="utf-8").split("\n"), 1):
                if ABSOLUTE.search(line):
                    doc_findings.append((md.name, i, "绝对化表达", line.strip()[:70]))
                elif SPECULATIVE.search(line) and "待核实" not in line and "可信第三方估计" not in line:
                    doc_findings.append((md.name, i, "传闻语气未标披露等级", line.strip()[:70]))

    REPORTS.mkdir(exist_ok=True)
    L = ["# 公司披露审计", "", "> 生成于 `scripts/company_disclosure_audit.py`", "",
         f"- companies.csv 记录：{len(rows)}（最终目标 ≥ 60 条，其中 ≥ 30 份深度档案）",
         f"- company_events.csv 记录：{len(events)}",
         f"- **CSV 问题：{len(issues)}** ｜ 文档告警：{len(doc_findings)}", ""]
    if not rows and not events:
        L.append("暂无公司记录（Phase 0）。")
    if issues:
        L += ["## CSV 问题", "", "| 条目 | 问题 | 值 |", "|---|---|---|"]
        L += [f"| `{a}` | {b} | `{c}` |" for a, b, c in issues]
    if doc_findings:
        L += ["", "## 文档告警", "", "| 文件 | 行 | 类型 | 片段 |", "|---|---:|---|---|"]
        L += [f"| {a} | {b} | {c} | `{d}` |" for a, b, c, d in doc_findings]
    if not issues and not doc_findings and (rows or events):
        L.append("全部通过。")
    (REPORTS / "company_disclosure_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"[company_disclosure_audit] 公司 {len(rows)}，事件 {len(events)}，"
          f"CSV 问题 {len(issues)}，文档告警 {len(doc_findings)}")
    for a, b, c in issues[:20]:
        print(f"  ✗ {a}: {b} — {c}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
