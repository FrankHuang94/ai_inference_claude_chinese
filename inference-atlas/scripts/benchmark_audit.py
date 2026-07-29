#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""benchmark 方法论审计：检查 benchmarks.csv 是否具备可比性所需的最低充分条件。

退出码：0 = 通过或暂无记录；1 = 存在缺项。
"""
import csv
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

# 必须明确（可填 `未公开`，但不得留空）
MUST_STATE = ["model_version", "hardware", "software_stack", "quantization",
              "input_tokens", "output_tokens", "batch_or_concurrency",
              "goodput_definition", "power_w", "source_url", "reproducibility_level",
              "caveats"]
# 不得为占位符——必须有实质内容
MUST_BE_REAL = ["source_url", "reproducibility_level", "caveats"]
EMPTYISH = {"", "无", "n/a", "N/A", "TODO", "-"}
LAT_COLS = ["ttft_ms", "tpot_ms", "itl_ms", "end_to_end_latency_ms"]


def main() -> int:
    p = DATA / "benchmarks.csv"
    if not p.exists():
        print("[benchmark_audit] benchmarks.csv 不存在")
        return 1
    with p.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    issues = []
    for r in rows:
        bid = r.get("benchmark_id", "?")
        for col in MUST_STATE:
            if (r.get(col) or "").strip() == "":
                issues.append((bid, f"`{col}` 留空（未公开请显式填 `未公开`）"))
        for col in MUST_BE_REAL:
            if (r.get(col) or "").strip() in EMPTYISH:
                issues.append((bid, f"`{col}` 必须有实质内容，不得为占位符"))
        if all((r.get(c) or "").strip() in ("", "未公开") for c in LAT_COLS) and \
           (r.get("throughput_tokens_per_sec") or "").strip() in ("", "未公开"):
            issues.append((bid, "时延与吞吐全部未公开，该记录无可比信息"))
        if (r.get("source_type") or "").strip() == "厂商官方" and \
           (r.get("reproducibility_level") or "").strip() == "完整可复现":
            issues.append((bid, "厂商官方结果标为完整可复现，需确认是否提供了完整复现配方"))

    REPORTS.mkdir(exist_ok=True)
    L = ["# Benchmark 方法论审计", "", "> 生成于 `scripts/benchmark_audit.py`", "",
         f"- benchmarks.csv 记录：{len(rows)}（最终目标 ≥ 100 条 benchmark 或部署案例）",
         f"- **问题：{len(issues)}**", "",
         "## 最低充分条件", "",
         "以下任一项缺失，该 benchmark **不可跨来源比较**：", "",
         "模型版本、硬件、软件栈版本、量化方案、输入长度、输出长度、batch/concurrency、"
         "warmup 方式、latency 定义、throughput 定义、功耗测量边界、来源 URL、可复现性、caveat。", ""]
    if not rows:
        L.append("暂无 benchmark 记录（Phase 0）。")
    elif issues:
        L += ["## 问题明细", "", "| benchmark | 问题 |", "|---|---|"]
        L += [f"| `{a}` | {b} |" for a, b in issues]
    else:
        L.append("全部通过。")
    (REPORTS / "benchmark_audit_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"[benchmark_audit] 记录 {len(rows)}，问题 {len(issues)}")
    for a, b in issues[:20]:
        print(f"  ✗ {a}: {b}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
