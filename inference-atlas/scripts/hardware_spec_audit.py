#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""硬件规格审计：来源、峰值/实测混淆、训练/推理混淆、功耗层级、精度与单位。

退出码：0 = 通过或暂无记录；1 = 存在问题。
"""
import csv
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

DISCLOSURE = {"官方披露", "技术文档披露", "开源代码/配置披露", "独立可复现实验",
              "可信第三方估计", "未公开", "待核实"}
PRECISION = re.compile(r"(FP4|FP6|FP8|FP16|FP32|FP64|BF16|TF32|INT4|INT8|INT16|"
                       r"MXFP\d|NVFP\d|稀疏|sparse|dense)", re.I)
POWER_SCOPE = re.compile(r"(chip|die|board|module|card|server|node|rack|整机|单卡|板卡|机架|系统)", re.I)
BYTE_BW = re.compile(r"\b(TB/s|GB/s|MB/s)\b")
BIT_BW = re.compile(r"\b(Tb/s|Gb/s|Mb/s)\b")
CAP_UNIT = re.compile(r"\b(GB|GiB|TB|TiB|MB|MiB)\b")
MEASURED = re.compile(r"(实测|measured|benchmark|MLPerf|吞吐|throughput|tokens/s)", re.I)
TRAINING = re.compile(r"(训练|training|pretrain)", re.I)
PLACEHOLDER = {"未公开", "待核实", "不适用"}


def main() -> int:
    p = DATA / "accelerators.csv"
    if not p.exists():
        print("[hardware_spec_audit] accelerators.csv 不存在")
        return 1
    with p.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    issues = []
    for r in rows:
        aid = r.get("accelerator_id", "?")
        src = (r.get("official_benchmark_or_source") or "").strip()
        if not src.startswith("https://") and src not in PLACEHOLDER:
            issues.append((aid, "规格缺少可点击的一手来源链接", src))
        if (r.get("disclosure_level") or "").strip() not in DISCLOSURE:
            issues.append((aid, "披露等级非法或缺失", r.get("disclosure_level", "")))

        peak = (r.get("peak_compute_claim") or "").strip()
        if peak and peak not in PLACEHOLDER:
            if not PRECISION.search(peak):
                issues.append((aid, "peak_compute_claim 未注明精度（及是否含稀疏加速）", peak))
            if MEASURED.search(peak):
                issues.append((aid, "peak_compute_claim 混入了实测/benchmark 数据，"
                                    "实测结果应录入 benchmarks.csv", peak))
            if TRAINING.search(peak):
                issues.append((aid, "peak_compute_claim 混入训练性能表述，需与推理性能分列", peak))

        pw = (r.get("tdp_or_power") or "").strip()
        if pw and pw not in PLACEHOLDER and not POWER_SCOPE.search(pw):
            issues.append((aid, "tdp_or_power 未注明层级（chip/board/server/rack）", pw))

        cap = (r.get("memory_capacity") or "").strip()
        if cap and cap not in PLACEHOLDER and not CAP_UNIT.search(cap):
            issues.append((aid, "memory_capacity 缺少明确单位（GB vs GiB）", cap))

        bw = (r.get("memory_bandwidth") or "").strip()
        if bw and bw not in PLACEHOLDER:
            if BIT_BW.search(bw) and not BYTE_BW.search(bw):
                issues.append((aid, "memory_bandwidth 使用了比特单位，内存带宽应为字节单位（TB/s）", bw))
            elif not BYTE_BW.search(bw):
                issues.append((aid, "memory_bandwidth 缺少明确单位（TB/s）", bw))

        ic = (r.get("interconnect") or "").strip()
        if ic and ic not in PLACEHOLDER and not (BYTE_BW.search(ic) or BIT_BW.search(ic)):
            issues.append((aid, "interconnect 缺少速率单位（须区分 GB/s 与 Gb/s）", ic))

    REPORTS.mkdir(exist_ok=True)
    L = ["# 硬件规格审计", "", "> 生成于 `scripts/hardware_spec_audit.py`", "",
         f"- accelerators.csv 记录：{len(rows)}（最终目标 ≥ 80 条硬件/平台记录）",
         f"- **问题：{len(issues)}**", "",
         "## 强制区分项", "",
         "| 必须区分 | 检查方式 |", "|---|---|",
         "| 理论峰值 vs 实测 | `peak_compute_claim` 中出现实测/benchmark 关键词即告警 |",
         "| 训练 vs 推理性能 | `peak_compute_claim` 中出现训练关键词即告警 |",
         "| 官方宣称 vs 第三方 | `disclosure_level` 枚举校验 |",
         "| chip/board/server/rack 功耗 | `tdp_or_power` 必须含层级关键词 |",
         "| GB vs GiB、TB/s vs Tb/s | 容量与带宽单位正则校验 |", ""]
    if not rows:
        L.append("暂无加速器记录（Phase 0）。")
    elif issues:
        L += ["## 问题明细", "", "| 记录 | 问题 | 值 |", "|---|---|---|"]
        L += [f"| `{a}` | {b} | `{c}` |" for a, b, c in issues]
    else:
        L.append("全部通过。")
    (REPORTS / "hardware_spec_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"[hardware_spec_audit] 记录 {len(rows)}，问题 {len(issues)}")
    for a, b, c in issues[:20]:
        print(f"  ✗ {a}: {b} — {c}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
