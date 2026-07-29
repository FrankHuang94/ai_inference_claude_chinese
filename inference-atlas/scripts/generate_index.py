#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""INDEX.md 与实际文件系统的一致性检查 / 目录片段生成。

用法：
  python3 scripts/generate_index.py --check    # 校验（CI 用）
  python3 scripts/generate_index.py            # 打印可粘贴的目录片段

退出码：--check 下，0 = 一致；1 = 不一致。
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
INDEX = ROOT / "INDEX.md"
STATUS = ("已完成", "进行中", "待开始")


def modules():
    return sorted(p for p in DOCS.iterdir() if p.is_dir())


def check() -> int:
    txt = INDEX.read_text(encoding="utf-8")
    problems = []

    for m in modules():
        if f"docs/{m.name}/" not in txt:
            problems.append(f"INDEX.md 未引用模块目录 `docs/{m.name}/`")
        if not (m / "README.md").exists():
            problems.append(f"模块 `{m.name}` 缺少 README.md")

    for ref in sorted(set(re.findall(r"docs/(\d\d_[a-z0-9_]+)/", txt))):
        if not (DOCS / ref).is_dir():
            problems.append(f"INDEX.md 引用了不存在的模块目录 `docs/{ref}/`")

    # 模块状态总览表必须为每个模块给出合法状态
    for m in modules():
        row = re.search(rf"\|\s*\d+\s*\|\s*\[[^\]]+\]\(docs/{re.escape(m.name)}/\)\s*\|\s*([^|]+)\|",
                        txt)
        if not row:
            problems.append(f"模块状态总览表缺少 `{m.name}` 行")
        elif row.group(1).strip() not in STATUS:
            problems.append(f"模块 `{m.name}` 状态非法：`{row.group(1).strip()}`"
                            f"（应为 {'/'.join(STATUS)}）")

    # 已存在的正文文档应已在 INDEX 中列出
    for m in modules():
        for f in sorted(m.glob("*.md")):
            if f.name == "README.md":
                continue
            if f.name not in txt:
                problems.append(f"INDEX.md 未列出已存在的文档 `{m.name}/{f.name}`")

    if problems:
        print(f"[generate_index] 不一致 {len(problems)} 处：")
        for p in problems:
            print(f"  ✗ {p}")
        return 1
    print(f"[generate_index] INDEX.md 与 {len(modules())} 个模块目录一致。")
    return 0


def emit():
    print("<!-- 可粘贴至 INDEX.md 的模块状态总览表 -->")
    print("| # | 模块 | 状态 | 文档数 |")
    print("|---|---|---|---:|")
    for m in modules():
        n = len([f for f in m.glob("*.md") if f.name != "README.md"])
        print(f"| {m.name[:2]} | [{m.name}](docs/{m.name}/) | "
              f"{'待开始' if n == 0 else '进行中'} | {n} |")


if __name__ == "__main__":
    sys.exit(check() if "--check" in sys.argv else (emit() or 0))
