#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""单位一致性审计：扫描 docs/ 中易混淆的单位写法。

规则为启发式，输出为**告警**，需人工确认。
退出码：始终 0（避免误报阻断写作）。
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPORTS = ROOT / "reports"
FENCE = re.compile(r"```.*?```", re.S)
COUNTEREXAMPLE = re.compile(r"(错误写法|错误示范|错误[:：]|反例|不要写|第一反应|应该是怀疑|属伪精确|禁止)")
COMMENT = re.compile(r"<!--.*?-->", re.S)

# (规则名, 正则, 说明)
RULES = [
    ("带宽单位大小写", re.compile(r"\d+\s*(?:TBps|GBps|Tbps|Gbps)\b"),
     "建议写作 TB/s（字节）或 Tb/s（比特），避免 Tbps/TBps 混写"),
    ("内存带宽误用比特", re.compile(r"(?:内存带宽|显存带宽|HBM\s*带宽)[^\n。]{0,20}?\d+\s*(?:Tb/s|Gb/s)"),
     "内存带宽应使用字节单位 TB/s，比特单位用于网络链路速率"),
    ("网络速率误用字节", re.compile(r"(?:链路速率|端口速率|网络带宽)[^\n。]{0,20}?\d+\s*(?:TB/s|GB/s)"),
     "网络链路速率通常以 Gb/s、Tb/s 表述，若确为字节需显式说明"),
    ("FLOPS/TOPS 未标精度", re.compile(r"\d+(?:\.\d+)?\s*(?:P|T|G)(?:FLOPS|OPS)\b(?![^\n]{0,40}"
                                       r"(?:FP4|FP8|FP16|FP32|BF16|TF32|INT4|INT8|稀疏|sparse|dense))"),
     "算力必须注明精度（如 BF16 TFLOPS）与是否含稀疏加速"),
    ("功耗未标层级", re.compile(r"\d+(?:\.\d+)?\s*(?:W|kW|MW)\b(?![^\n]{0,40}"
                                r"(?:chip|die|board|module|card|server|node|rack|整机|单卡|板卡|机架|系统|设施))"),
     "功耗必须注明测量层级（chip/board/server/rack/facility）"),
    ("GB/GiB 未区分", re.compile(r"(?:容量|显存|内存)[^\n。]{0,12}?\d+(?:\.\d+)?\s*GB\b"),
     "确认是十进制 GB 还是二进制 GiB，必要时显式说明"),
    ("成本口径混用", re.compile(r"\$\s*\d+(?:\.\d+)?\s*/\s*(?:token|tok)\b"),
     "单 token 成本建议统一写作 $/1M tokens，避免极小数字的伪精确"),
    # 仅当分位数后面跟着**具体测量值**时才要求样本量。两类不告警：
    #   1) 散文中提及 P99 概念（无具体数值）；
    #   2) SLO / 目标 / 阈值语境——阈值是被设定的，不是被测量的，不需要样本量。
    ("分位数缺样本量",
     re.compile(r"\bP(?:50|95|99|99\.9)\b(?![^\n]{0,12}?(?:≤|<=|≥|>=|目标|阈值|SLO|上限|下限))"
                r"[^\n]{0,20}?\d+(?:\.\d+)?\s*(?:ms|s|秒|毫秒)"
                r"(?![^\n]{0,80}(?:样本|n\s*=|请求数|次|窗口))"),
     "报告了具体分位数值但未给出样本量或观测窗口"),
    ("伪精确成本", re.compile(r"\$\s*\d+\.\d{5,}"),
     "成本数字位数超出输入精度，属伪精确"),
]


def main() -> int:
    findings = []
    files = sorted(p for p in DOCS.rglob("*.md") if p.name != "README.md")
    for md in files:
        text = COMMENT.sub("", FENCE.sub("", md.read_text(encoding="utf-8")))
        for i, line in enumerate(text.split("\n"), 1):
            if line.lstrip().startswith(">"):
                continue
            # 教学用的反例/错误示范行本身就是在演示违规写法，不告警
            if COUNTEREXAMPLE.search(line):
                continue
            for name, rx, hint in RULES:
                m = rx.search(line)
                if m:
                    findings.append((md.relative_to(ROOT), i, name, m.group(0).strip(), hint))

    REPORTS.mkdir(exist_ok=True)
    L = ["# 单位一致性审计", "", "> 生成于 `scripts/unit_consistency_audit.py`", "",
         "> 本报告为**启发式告警**，需人工确认；不阻断提交。", "",
         f"- 扫描文档：{len(files)}", f"- 告警：{len(findings)}", "",
         "## 检查规则", "", "| 规则 | 说明 |", "|---|---|"]
    L += [f"| {n} | {h} |" for n, _, h in RULES]
    L += ["", "## 告警明细", ""]
    if not files:
        L.append("尚无正文文档（Phase 0）。")
    elif findings:
        L += ["| 文件 | 行 | 规则 | 片段 |", "|---|---:|---|---|"]
        L += [f"| `{a}` | {b} | {c} | `{d}` |" for a, b, c, d, _ in findings]
    else:
        L.append("未发现问题。")
    (REPORTS / "unit_consistency_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"[unit_consistency_audit] 扫描 {len(files)} 篇，告警 {len(findings)}")
    for a, b, c, d, _ in findings[:20]:
        print(f"  ! {a}:{b} [{c}] {d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
