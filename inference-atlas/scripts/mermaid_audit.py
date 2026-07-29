#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mermaid 图审计：统计数量、基础语法检查、标记缺少上下文解释的图。

约定：每张图前后必须回答四个问题——图展示什么、核心瓶颈、trade-off、面试如何引用。
本脚本以「图前 15 行内 + 图后 15 行内是否存在解释性文字」作为启发式判据。

退出码：0 = 无语法错误；1 = 存在语法错误（阻断级，因 GitHub 将无法渲染）。
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPORTS = ROOT / "reports"
TARGET = 60

BLOCK = re.compile(r"^([ \t]*)```mermaid[ \t]*$(.*?)^\1```[ \t]*$", re.M | re.S)
VALID_HEAD = re.compile(
    r"^\s*(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram(?:-v2)?|erDiagram|"
    r"journey|gantt|pie|gitGraph|mindmap|timeline|quadrantChart|C4Context|block-beta|"
    r"sankey-beta|xychart-beta|requirementDiagram)\b")
CONTEXT_HINT = re.compile(r"(瓶颈|trade-?off|权衡|本图|上图|下图|该图|图中|面试)", re.I)


def main() -> int:
    files = sorted(DOCS.rglob("*.md"))
    total, errors, missing_ctx, per_module = 0, [], [], {}

    for md in files:
        text = md.read_text(encoding="utf-8")
        lines = text.split("\n")
        for m in BLOCK.finditer(text):
            total += 1
            mod = md.relative_to(DOCS).parts[0]
            per_module[mod] = per_module.get(mod, 0) + 1
            body = m.group(2)
            rel = md.relative_to(ROOT)
            start_line = text[:m.start()].count("\n") + 1

            content = [ln for ln in body.split("\n") if ln.strip()]
            if not content:
                errors.append((rel, start_line, "空的 mermaid 代码块"))
                continue
            if not VALID_HEAD.match(content[0]):
                errors.append((rel, start_line,
                               f"首行缺少合法图类型声明：`{content[0].strip()[:40]}`"))
            for br in "()[]{}":
                pass
            joined = "\n".join(content)
            for op, cl in (("[", "]"), ("(", ")"), ("{", "}")):
                if joined.count(op) != joined.count(cl):
                    errors.append((rel, start_line,
                                   f"括号不配对：`{op}` {joined.count(op)} 个 / "
                                   f"`{cl}` {joined.count(cl)} 个"))
            end_line = text[:m.end()].count("\n") + 1
            before = "\n".join(lines[max(0, start_line - 16):start_line - 1])
            after = "\n".join(lines[end_line:end_line + 15])
            if not (CONTEXT_HINT.search(before) and CONTEXT_HINT.search(after)):
                missing_ctx.append((rel, start_line))

    REPORTS.mkdir(exist_ok=True)
    L = ["# Mermaid 图审计", "", "> 生成于 `scripts/mermaid_audit.py`", "",
         f"- **图示总数：{total} / 目标 {TARGET}**（完成度 {total / TARGET * 100:.1f}%）",
         f"- 语法错误：{len(errors)}",
         f"- 缺少前后文解释：{len(missing_ctx)}", "",
         "## 按模块分布", ""]
    if per_module:
        L += ["| 模块 | 图数 |", "|---|---:|"]
        L += [f"| {k} | {v} |" for k, v in sorted(per_module.items())]
    else:
        L.append("尚无 Mermaid 图（Phase 0）。")
    L += ["", f"## 语法错误：{len(errors)}", ""]
    if errors:
        L += ["| 文件 | 行 | 问题 |", "|---|---:|---|"]
        L += [f"| `{a}` | {b} | {c} |" for a, b, c in errors]
    else:
        L.append("无。")
    L += ["", f"## 缺少前后文解释：{len(missing_ctx)}", "",
          "> 约定：每张图前后须说明「图展示什么 / 核心瓶颈 / trade-off / 面试如何引用」。", ""]
    if missing_ctx:
        L += ["| 文件 | 行 |", "|---|---:|"] + [f"| `{a}` | {b} |" for a, b in missing_ctx]
    else:
        L.append("无。")
    (REPORTS / "mermaid_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"[mermaid_audit] 图 {total}/{TARGET}，语法错误 {len(errors)}，缺解释 {len(missing_ctx)}")
    for a, b, c in errors[:20]:
        print(f"  ✗ {a}:{b} {c}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
