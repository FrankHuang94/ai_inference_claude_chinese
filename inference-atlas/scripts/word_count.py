#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统计 docs/ 中文正文字数。

排除：fenced code block、HTML 注释、文档头部导航块（> 引用）、URL、Markdown 链接目标。
输出 reports/word_count_report.md。

退出码：始终 0（字数不足为提示而非阻断，建库过程中字数天然未达标）。
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPORTS = ROOT / "reports"

# 模块目标字数（来自项目规格）
TARGETS = {
    "00_start_here": 8000, "01_foundations_and_metrics": 14000,
    "02_transformer_and_kv_cache": 15000, "03_serving_engines_and_scheduling": 17000,
    "04_compilers_runtimes_and_kernels": 15000, "05_decoding_and_generation_algorithms": 13000,
    "06_distributed_and_moe_inference": 17000, "07_hardware_and_server_architecture": 18000,
    "08_networking_and_interconnect": 15000, "09_datacenter_power_thermal_and_operations": 10000,
    "10_edge_and_on_device_inference": 10000,
    "11_benchmarking_reliability_and_observability": 12000,
    "12_open_source_deployment_and_reproduction": 12000,
    "13_research_papers_and_technical_reports": 12000,
    "14_company_and_ecosystem_landscape": 20000, "15_market_economics_and_strategy": 16000,
    "16_research_frontiers": 12000, "17_interview_prep": 12000,
}
TOTAL_TARGET = 120_000
TOTAL_FLOOR = 100_000
PER_DOC_FLOOR = 800  # 单篇实质内容下限

CJK = re.compile(r"[一-鿿㐀-䶿]")
LATIN_WORD = re.compile(r"[A-Za-z][A-Za-z0-9_\-]*")


def strip_noise(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)          # fenced code
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)          # HTML 注释
    text = re.sub(r"^\s{4,}\S.*$", " ", text, flags=re.M)        # 缩进代码
    text = re.sub(r"`[^`\n]*`", " ", text)                       # 行内代码
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)       # 链接保留文字
    text = re.sub(r"https?://\S+", " ", text)                    # 裸 URL
    return text


def strip_nav(text: str) -> str:
    """移除文档开头连续的 '>' 导航/元信息块。"""
    lines = text.split("\n")
    out, in_head = [], True
    for ln in lines:
        s = ln.strip()
        if in_head:
            if s.startswith(">") or s.startswith("#") or not s:
                if s.startswith(">"):
                    continue
                if s.startswith("#"):
                    in_head = False
                out.append(ln)
                continue
            in_head = False
        out.append(ln)
    return "\n".join(out)


def count(text: str) -> int:
    t = strip_noise(strip_nav(text))
    return len(CJK.findall(t)) + len(LATIN_WORD.findall(t))


def main() -> int:
    rows, module_totals, grand = [], {}, 0
    for mod in sorted(TARGETS):
        d = DOCS / mod
        sub, files = 0, []
        if d.is_dir():
            for f in sorted(d.glob("*.md")):
                if f.name == "README.md":
                    continue  # 模块 README 属导航层，不计入正文
                n = count(f.read_text(encoding="utf-8"))
                files.append((f.name, n))
                sub += n
        module_totals[mod] = sub
        grand += sub
        rows.append((mod, sub, TARGETS[mod], files))

    REPORTS.mkdir(exist_ok=True)
    L = ["# 字数统计报告", "", f"> 生成于 `scripts/word_count.py`", "",
         f"**全库正文合计**：{grand:,} 字 ／ 目标 {TOTAL_TARGET:,}（最低验收线 {TOTAL_FLOOR:,}）",
         f"**完成度**：{grand / TOTAL_TARGET * 100:.1f}%", "",
         "## 模块汇总", "", "| 模块 | 字数 | 目标 | 完成度 | 文档数 |", "|---|---:|---:|---:|---:|"]
    for mod, sub, tgt, files in rows:
        L.append(f"| {mod} | {sub:,} | {tgt:,} | {sub / tgt * 100:.1f}% | {len(files)} |")
    L += ["", "## 未达单篇下限的文档", "",
          f"（下限 {PER_DOC_FLOOR} 字；空壳与占位文档会在此暴露）", ""]
    short = [(m, n, c) for m, _, _, fs in rows for n, c in fs if c < PER_DOC_FLOOR]
    if short:
        L += ["| 模块 | 文档 | 字数 |", "|---|---|---:|"]
        L += [f"| {m} | {n} | {c:,} |" for m, n, c in short]
    else:
        L.append("无。")
    L += ["", "## 逐篇明细", ""]
    any_doc = False
    for mod, sub, tgt, files in rows:
        if not files:
            continue
        any_doc = True
        L += [f"### {mod}", "", "| 文档 | 字数 |", "|---|---:|"]
        L += [f"| {n} | {c:,} |" for n, c in files]
        L.append("")
    if not any_doc:
        L.append("尚无正文文档（Phase 0 仅建立基础设施）。")
    (REPORTS / "word_count_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"[word_count] 全库正文 {grand:,} 字 / 目标 {TOTAL_TARGET:,} "
          f"({grand / TOTAL_TARGET * 100:.1f}%)")
    if short:
        print(f"[word_count] 提示：{len(short)} 篇文档低于单篇下限 {PER_DOC_FLOOR} 字")
    print(f"[word_count] 报告 → reports/word_count_report.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
