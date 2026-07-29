#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 data/*.csv 的表头、必填、日期、URL 与枚举。

退出码：0 = 通过；1 = 存在违规（阻断级）。
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
BOOLISH = {"是", "否", "部分", "待核实", "未公开"}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^https://\S+$")

# csv 名 -> (必填列, 日期列, URL 列, {列: 允许值集合})
SPEC = {
    "papers": (["paper_id", "title", "authors", "year", "venue", "arxiv_or_doi_url",
                "category", "one_sentence_contribution", "limitations",
                "citation_status", "last_verified_date"],
               ["last_verified_date"], ["arxiv_or_doi_url"],
               {"citation_status": {"已核验", "待核实"}}),
    "models": (["model_id", "model_family", "organization", "open_or_closed",
                "parameter_count", "official_source_url", "disclosure_level",
                "last_verified_date"],
               ["last_verified_date"], ["official_source_url"],
               {"disclosure_level": DISCLOSURE,
                "open_or_closed": {"开放权重", "闭源", "部分开放", "未公开"},
                "dense_or_moe": {"dense", "MoE", "未公开"}}),
    "inference_engines": (["engine_id", "name", "license", "official_source_url",
                           "last_verified_date"],
                          ["last_verified_date"], ["official_source_url"],
                          {k: BOOLISH for k in
                           ["continuous_batching", "paged_kv_cache", "prefix_caching",
                            "speculative_decoding", "moe_support",
                            "distributed_inference_support", "quantization_support",
                            "observability_support"]}),
    "accelerators": (["accelerator_id", "vendor", "product_name", "market_segment",
                      "official_benchmark_or_source", "disclosure_level",
                      "last_verified_date"],
                     ["last_verified_date"], ["official_benchmark_or_source"],
                     {"disclosure_level": DISCLOSURE,
                      "market_segment": {"训练", "推理", "训推一体", "边缘", "PC", "未公开"}}),
    "server_platforms": (["platform_id", "vendor", "platform_name", "disclosure_level",
                          "last_verified_date"],
                         ["last_verified_date"], ["official_source_url"],
                         {"disclosure_level": DISCLOSURE}),
    "memory_technologies": (["memory_id", "technology_name", "disclosure_level",
                             "last_verified_date"],
                            ["last_verified_date"], ["official_source_url"],
                            {"disclosure_level": DISCLOSURE}),
    "networking_technologies": (["network_id", "technology_name", "layer",
                                 "disclosure_level", "last_verified_date"],
                                ["last_verified_date"], ["official_source_url"],
                                {"disclosure_level": DISCLOSURE,
                                 "scale_up_or_scale_out": {"scale-up", "scale-out", "两者", "不适用"}}),
    "benchmarks": (["benchmark_id", "benchmark_name", "organization", "date", "model",
                    "hardware", "software_stack", "source_type", "source_url",
                    "reproducibility_level", "caveats", "last_verified_date"],
                   ["date", "last_verified_date"], ["source_url"],
                   {"reproducibility_level": {"完整可复现", "部分可复现", "不可复现"},
                    "source_type": {"MLPerf 官方", "厂商官方", "第三方独立", "论文", "本库复现"}}),
    "deployment_cases": (["case_id", "organization", "application", "source_type",
                          "source_url", "disclosure_level", "last_verified_date"],
                         ["last_verified_date"], ["source_url"],
                         {"disclosure_level": DISCLOSURE}),
    "techniques": (["technique_id", "name", "category", "problem_solved", "core_idea",
                    "common_failures", "maturity", "last_verified_date"],
                   ["last_verified_date"], [],
                   {"maturity": {"研究阶段", "早期采用", "生产成熟", "事实标准"}}),
    "companies": (["organization", "type", "core_business", "inference_positioning",
                   "key_risks", "official_source_url", "last_verified_date"],
                  ["last_verified_date"], ["official_source_url"], {}),
    "company_events": (["event_id", "organization", "event_date", "event_type",
                        "source_url", "disclosure_level", "last_verified_date"],
                       ["event_date", "last_verified_date"], ["source_url"],
                       {"disclosure_level": DISCLOSURE}),
    "cloud_pricing": (["pricing_id", "provider", "sku_or_model", "unit", "price",
                       "currency", "official_source_url", "disclosure_level",
                       "last_verified_date"],
                      ["last_verified_date"], ["official_source_url"],
                      {"disclosure_level": DISCLOSURE}),
    "market_transactions": (["transaction_id", "transaction_type", "announce_date",
                             "source_url", "disclosure_level", "last_verified_date"],
                            ["announce_date", "last_verified_date"], ["source_url"],
                            {"disclosure_level": DISCLOSURE}),
    "glossary": (["term_id", "term_zh", "term_en", "definition", "last_verified_date"],
                 ["last_verified_date"], [], {}),
    "interview_questions": (["question_id", "topic", "difficulty", "question",
                             "reference_answer", "common_mistakes",
                             "follow_up_questions", "related_docs", "format",
                             "last_updated"],
                            ["last_updated"], [],
                            {"difficulty": {"中等", "高", "专家"},
                             "format": {"概念", "系统设计", "计算", "排查", "编码", "战略讨论"}}),
}

PLACEHOLDER_OK = {"未公开", "待核实", "不适用", "无", "待创建"}

# 枚举字段允许「枚举值（限定说明）」写法，例如：
#   是（tensor parallel、pipeline parallel）
# 校验时先剥离全角/半角括号内的限定说明，只比对前缀枚举值。
QUALIFIER = re.compile(r"[（(].*$")


def enum_key(value: str) -> str:
    return QUALIFIER.sub("", value).strip()


def main() -> int:
    issues, stats = [], []
    for name, (required, dates, urls, enums) in SPEC.items():
        path = DATA / f"{name}.csv"
        if not path.exists():
            issues.append((name, "-", "文件缺失", ""))
            continue
        with path.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
            header = rows[0].keys() if rows else None
        if header is None:
            with path.open(encoding="utf-8", newline="") as f:
                header = next(csv.reader(f), [])
        header = list(header)
        stats.append((name, len(header), len(rows)))

        for col in required:
            if col not in header:
                issues.append((name, "表头", f"缺少必填列 `{col}`", ""))

        for i, row in enumerate(rows, start=2):
            rid = row.get(list(header)[0], f"row{i}")
            for col in required:
                if col in row and not (row[col] or "").strip():
                    issues.append((name, rid, f"必填字段 `{col}` 为空", ""))
            for col in dates:
                v = (row.get(col) or "").strip()
                if v and v not in PLACEHOLDER_OK and not DATE_RE.match(v):
                    issues.append((name, rid, f"`{col}` 日期格式应为 YYYY-MM-DD", v))
            for col in urls:
                v = (row.get(col) or "").strip()
                if v and v not in PLACEHOLDER_OK and not URL_RE.match(v):
                    issues.append((name, rid, f"`{col}` 应为 https:// 开头的一手来源", v))
            for col, allowed in enums.items():
                v = (row.get(col) or "").strip()
                if v and enum_key(v) not in allowed:
                    issues.append((name, rid, f"`{col}` 取值不在枚举内", v))

    REPORTS.mkdir(exist_ok=True)
    L = ["# 数据质量报告", "", "> 生成于 `scripts/validate_csv_schema.py`", "",
         "## CSV 概览", "", "| 文件 | 列数 | 记录数 |", "|---|---:|---:|"]
    L += [f"| {n}.csv | {c} | {r} |" for n, c, r in stats]
    L += ["", f"**记录总数**：{sum(r for _, _, r in stats)}", "",
          f"## 违规项：{len(issues)}", ""]
    if issues:
        L += ["| 文件 | 记录 | 问题 | 值 |", "|---|---|---|---|"]
        L += [f"| {a}.csv | `{b}` | {c} | `{d}` |" for a, b, c, d in issues]
    else:
        L.append("全部通过。")
    (REPORTS / "data_quality_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"[validate_csv_schema] {len(stats)} 个 CSV，"
          f"{sum(r for _, _, r in stats)} 条记录，违规 {len(issues)}")
    for a, b, c, d in issues[:20]:
        print(f"  ✗ {a}.csv [{b}] {c} {d}")
    print("[validate_csv_schema] 报告 → reports/data_quality_report.md")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
