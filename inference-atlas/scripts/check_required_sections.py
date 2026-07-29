#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查核心文档是否具备必备章节（依据 templates/chapter_template.md）。

跳过：模块 README、模块 13/14/17（使用卡片式模板，另有专用审计）。
退出码：0 = 通过或尚无正文；1 = 存在缺章的正文文档。
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPORTS = ROOT / "reports"

# (显示名, 匹配该章节的正则)
REQUIRED = [
    ("本章导读", r"^##\s*本章导读"),
    ("学习目标", r"^##\s*学习目标"),
    ("核心结论", r"^##\s*核心结论"),
    ("问题定义", r"^##\s*1\..*问题定义"),
    ("原理/数学", r"^##\s*2\..*(原理|数学|性能模型)"),
    ("工程实现", r"^##\s*3\..*(实现|系统设计)"),
    ("性能/成本 trade-off", r"^##\s*4\..*(trade-off|权衡)"),
    ("benchmark/案例", r"^##\s*5\..*(benchmark|案例)"),
    ("决策框架", r"^##\s*6\..*决策框架"),
    ("失败模式", r"^##\s*7\..*(失败模式|排查)"),
    ("面试主题", r"^##\s*8\..*面试"),
    ("小结", r"^##\s*9\..*小结"),
    ("关键术语", r"^##\s*关键术语"),
    ("主要来源", r"^##\s*主要来源"),
    ("更新记录", r"^##\s*更新记录"),
]
# 卡片式模块，不套用章节模板
CARD_MODULES = {"13_research_papers_and_technical_reports",
                "14_company_and_ecosystem_landscape", "17_interview_prep"}


def main() -> int:
    results, bad = [], 0
    for mod in sorted(p for p in DOCS.iterdir() if p.is_dir()):
        if mod.name in CARD_MODULES:
            continue
        for f in sorted(mod.glob("*.md")):
            if f.name == "README.md":
                continue
            txt = f.read_text(encoding="utf-8")
            missing = [n for n, pat in REQUIRED
                       if not re.search(pat, txt, re.M | re.I)]
            results.append((f.relative_to(ROOT), missing))
            if missing:
                bad += 1

    REPORTS.mkdir(exist_ok=True)
    L = ["# 必备章节检查", "", "> 生成于 `scripts/check_required_sections.py`", "",
         f"- 检查文档：{len(results)}", f"- **缺章文档：{bad}**", ""]
    if not results:
        L.append("尚无正文文档（Phase 0 仅建立基础设施）。")
    elif bad:
        L += ["| 文档 | 缺失章节 |", "|---|---|"]
        L += [f"| `{p}` | {'、'.join(m)} |" for p, m in results if m]
    else:
        L.append("全部文档章节完整。")
    (REPORTS / "required_sections_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"[check_required_sections] 检查 {len(results)} 篇，缺章 {bad}")
    for p, m in results:
        if m:
            print(f"  ✗ {p}: 缺 {'、'.join(m)}")
    if not results:
        print("[check_required_sections] 尚无正文文档，跳过。")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
