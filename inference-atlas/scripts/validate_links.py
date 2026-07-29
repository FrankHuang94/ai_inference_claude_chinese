#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验仓库内所有 Markdown 的相对链接与同文件锚点。

剥离：fenced code、行内代码、HTML 注释、LaTeX 数学区（$...$ 与 $$...$$）。
这些区域中的 `E[S](1+x)` 等写法在语法上酷似 Markdown 链接，但并非链接。

排除目录：
  - templates/ —— 模板中的链接是**给复制到目标位置后使用**的占位路径
    （如 `../../INDEX.md` 相对 docs/<module>/ 才成立），在原位不可解析，属预期行为。
  - reports/   —— QA 生成物，不入库。

退出码：0 = 无死链；1 = 存在死链（阻断级）。
"""
import re
import sys
import pathlib
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
EXCLUDE_DIRS = {".git", "templates", "reports"}

LINK = re.compile(r"(?<!\!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.M)
FENCE = re.compile(r"```.*?```", re.S)
COMMENT = re.compile(r"<!--.*?-->", re.S)
# LaTeX 数学区：其中的 E[S](1+x) 等写法在语法上酷似 Markdown 链接，必须先剥离
MATH_BLOCK = re.compile(r"\$\$.*?\$\$", re.S)
MATH_INLINE = re.compile(r"(?<!\$)\$[^$\n]+\$(?!\$)")
# 行内代码：`E[S](1+x)` 同样酷似链接语法，且代码里的路径不应被当作真实链接校验
INLINE_CODE = re.compile(r"`[^`\n]*`")


def slugify(text: str) -> str:
    t = re.sub(r"`([^`]*)`", r"\1", text)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"[*_~]", "", t).strip().lower()
    t = re.sub(r"[^\w一-鿿\- ]", "", t)
    return t.replace(" ", "-")


def anchors_of(path: pathlib.Path) -> set:
    try:
        txt = FENCE.sub("", path.read_text(encoding="utf-8"))
        txt = MATH_INLINE.sub(" ", MATH_BLOCK.sub(" ", txt))
    except (OSError, UnicodeDecodeError):
        return set()
    return {slugify(m.group(2)) for m in HEADING.finditer(txt)}


def main() -> int:
    md_files = sorted(p for p in ROOT.rglob("*.md")
                      if not EXCLUDE_DIRS & set(p.relative_to(ROOT).parts))
    anchor_cache, dead, checked = {}, [], 0

    for md in md_files:
        raw = md.read_text(encoding="utf-8")
        body = COMMENT.sub("", FENCE.sub("", raw))
        body = MATH_INLINE.sub(" ", MATH_BLOCK.sub(" ", body))
        body = INLINE_CODE.sub(" ", body)
        for m in LINK.finditer(body):
            target = m.group(2).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                if target.startswith("#"):
                    checked += 1
                    frag = urllib.parse.unquote(target[1:]).lower()
                    if md not in anchor_cache:
                        anchor_cache[md] = anchors_of(md)
                        if frag and frag not in anchor_cache[md]:
                            dead.append((md, target, "锚点不存在"))
                continue
            checked += 1
            path_part, _, frag = target.partition("#")
            path_part = urllib.parse.unquote(path_part)
            if not path_part:
                continue
            resolved = (md.parent / path_part).resolve()
            if not resolved.exists():
                dead.append((md, target, "文件或目录不存在"))
                continue
            if frag and resolved.suffix == ".md":
                if resolved not in anchor_cache:
                    anchor_cache[resolved] = anchors_of(resolved)
                if urllib.parse.unquote(frag).lower() not in anchor_cache[resolved]:
                    dead.append((md, target, "锚点不存在"))

    REPORTS.mkdir(exist_ok=True)
    L = ["# 链接校验报告", "", "> 生成于 `scripts/validate_links.py`", "",
         f"> 排除目录：{'、'.join(sorted(EXCLUDE_DIRS))}"
         "（templates/ 中的链接是复制到目标位置后才成立的占位路径）", "",
         f"- 扫描 Markdown 文件：{len(md_files)}",
         f"- 校验相对链接与锚点：{checked}",
         f"- **死链：{len(dead)}**", ""]
    if dead:
        L += ["## 死链明细", "", "| 文件 | 链接目标 | 问题 |", "|---|---|---|"]
        L += [f"| `{p.relative_to(ROOT)}` | `{t}` | {r} |" for p, t, r in dead]
    else:
        L.append("未发现死链。")
    (REPORTS / "link_validation_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"[validate_links] 文件 {len(md_files)}，检查链接 {checked}，死链 {len(dead)}")
    for p, t, r in dead[:20]:
        print(f"  ✗ {p.relative_to(ROOT)} → {t} ({r})")
    print("[validate_links] 报告 → reports/link_validation_report.md")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
