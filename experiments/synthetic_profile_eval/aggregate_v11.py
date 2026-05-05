"""
文件：aggregate_v11.py
核心功能：v1.1 multi-generator supplement —— 聚合 4 家新 generator (GPT-5.4-mini / Qwen3.6-Plus / GLM-5.1 / Gemma-4-31b-it) +
        v1.0 已有 DS-V4-pro 的所有 (generator, condition) 单元，按 generator 维度切片。
        每个 generator 独立计算：6 维 mean/std + total + 三 judge Krippendorff α。
        最后产出"AKM 优势 generator-wise"对比表，显式标注任何 generator 上 AKM 优势消失或反向的反例。
        Kimi-K2.6 在 OpenRouter 上对长中文 prompt 持续返空，39% 完成度后被判定为 attempted-but-excluded，
        其原始数据保留在 outputs/v1.1/ 供审计，但不进入 lift 表 / agreement 主结论。
输入：outputs/v1.1/judgments_<judge>__<generator>.jsonl × 多文件 + outputs/v1/judgments_<judge>.jsonl × 3 个 (DS 视为 v1.0 generator)
输出：results/v1.1/scores_long.csv (含 generator 列)、scores_summary_v11.json (含 by_generator)、
     agreement_v11.json (per-generator α)、akm_lift_by_generator.json (核心 supplement 表)。
维护要求：每次 v1.1 数据有更新都必须重跑本脚本；任何 reviewer 质疑的数字都应该能从输出 JSON 直接核对。
"""

from __future__ import annotations

import csv
import itertools
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

# 复用 v1.0 的归一化与统计函数
from aggregate_v1 import (
    DIMENSIONS,
    _normalize_judgment,
    extract_best_answer,
    extract_scores,
    krippendorff_alpha_interval,
    parse_score_value,
    spearman,
)


ROOT = Path(__file__).resolve().parent
CONDITIONS = ["no_profile", "unstructured_notes", "akm_profile", "akm_elicited"]
# Kimi-K2.6 was attempted but excluded from main analysis (OpenRouter upstream
# returned empty content persistently; 39% completion). Its raw data is kept in
# outputs/v1.1/ for audit but the aggregator treats it as "attempted_excluded".
ATTEMPTED_EXCLUDED = ["kimi_k2_6"]
NEW_GENERATORS = ["gpt_5_4_mini", "qwen_3_6_plus", "glm_5_1", "gemma_4_31b_it"]
ALL_GENERATORS = ["deepseek_v4_pro"] + NEW_GENERATORS
# When walking output directories we still see the excluded generator's files;
# load_all_judgments() filters them out so they don't enter the main aggregates.
JUDGES = ["deepseek_v4_pro", "gemini_3_flash", "grok_4_3"]


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_all_judgments() -> list[dict]:
    """Load every judgment record, attaching generator_id.
    For v1.0 (DS as generator), read outputs/v1/judgments_*.jsonl and tag generator='deepseek_v4_pro'.
    For v1.1 (4 new generators), read outputs/v1.1/judgments_<judge>__<generator>.jsonl.
    """
    rows: list[dict] = []
    # v1.0 (deepseek_v4_pro generator)
    for jid in JUDGES:
        path = ROOT / "outputs" / "v1" / f"judgments_{jid}.jsonl"
        for rec in read_jsonl(path):
            rec["generator_id"] = "deepseek_v4_pro"
            rows.append(rec)
    # v1.1 (4 new generators)
    for gen in NEW_GENERATORS:
        for jid in JUDGES:
            path = ROOT / "outputs" / "v1.1" / f"judgments_{jid}__{gen}.jsonl"
            for rec in read_jsonl(path):
                rec.setdefault("generator_id", gen)  # already set by run_judging_v11
                rows.append(rec)
    return rows


def fmt(x, nd=3):
    if x is None:
        return None
    return round(float(x), nd)


def compute_per_generator_summary(records: list[dict]) -> dict:
    """For each generator: by_judge x condition + pooled across judges, total + 6 dimensions + std + n."""
    score_index: dict[tuple, float] = {}
    total_index: dict[tuple, float] = {}
    best_index: dict[tuple, str] = {}
    domain_index: dict[str, str] = {}

    for rec in records:
        pid = rec["profile_id"]
        gid = rec["generator_id"]
        jid = rec["judge_id"]
        domain_index[pid] = rec.get("domain", "")
        for label, condition in rec["label_map"].items():
            node = extract_scores(rec["judgment"], label)
            if node is None:
                continue
            dim_scores: dict[str, float] = {}
            for dim in DIMENSIONS:
                v = parse_score_value(node, dim)
                if v is None:
                    continue
                dim_scores[dim] = v
                score_index[(gid, jid, pid, condition, dim)] = v
            if dim_scores:
                total_index[(gid, jid, pid, condition)] = sum(dim_scores.values())
        best = extract_best_answer(rec["judgment"])
        if best and best in rec["label_map"]:
            best_index[(gid, jid, pid)] = rec["label_map"][best]

    summary: dict = {"by_generator": {}}
    for gid in ALL_GENERATORS:
        by_judge: dict = {}
        for jid in JUDGES:
            per_cond = {}
            for cond in CONDITIONS:
                dim_means = {}
                for dim in DIMENSIONS:
                    vals = [s for (g, j, p, c, d), s in score_index.items()
                            if g == gid and j == jid and c == cond and d == dim]
                    if vals:
                        dim_means[dim] = fmt(statistics.mean(vals))
                totals = [s for (g, j, p, c), s in total_index.items()
                          if g == gid and j == jid and c == cond]
                per_cond[cond] = {
                    "n": len(totals),
                    "total_mean": fmt(statistics.mean(totals)) if totals else None,
                    "total_std": fmt(statistics.pstdev(totals)) if len(totals) > 1 else None,
                    "dimensions": dim_means,
                }
            by_judge[jid] = per_cond

        pooled = {}
        for cond in CONDITIONS:
            dim_means = {}
            for dim in DIMENSIONS:
                vals = [s for (g, j, p, c, d), s in score_index.items()
                        if g == gid and c == cond and d == dim]
                if vals:
                    dim_means[dim] = fmt(statistics.mean(vals))
            totals = [s for (g, j, p, c), s in total_index.items()
                      if g == gid and c == cond]
            pooled[cond] = {
                "n": len(totals),
                "total_mean": fmt(statistics.mean(totals)) if totals else None,
                "total_std": fmt(statistics.pstdev(totals)) if len(totals) > 1 else None,
                "dimensions": dim_means,
            }

        # n_personas judged for this generator (with ≥1 dim score)
        personas = {p for (g, j, p, c, d) in score_index if g == gid}

        summary["by_generator"][gid] = {
            "n_personas_with_scores": len(personas),
            "by_judge": by_judge,
            "pooled": pooled,
        }

    # Best-answer counts per generator
    for gid in ALL_GENERATORS:
        per_judge_counts: dict = {}
        for jid in JUDGES:
            counts = {c: 0 for c in CONDITIONS}
            for (g, j, p), cond in best_index.items():
                if g == gid and j == jid:
                    counts[cond] = counts.get(cond, 0) + 1
            per_judge_counts[jid] = counts
        pooled_counts = {c: 0 for c in CONDITIONS}
        for (g, j, p), cond in best_index.items():
            if g == gid:
                pooled_counts[cond] = pooled_counts.get(cond, 0) + 1
        summary["by_generator"][gid]["best_answer_counts"] = {
            "by_judge": per_judge_counts,
            "pooled": pooled_counts,
        }

    return summary, score_index, total_index, best_index, domain_index


def compute_per_generator_agreement(score_index: dict, total_index: dict) -> dict:
    """For each generator: alpha on totals + per-dim, plus pairwise spearman on condition means across judges."""
    agreement: dict = {"by_generator": {}}
    for gid in ALL_GENERATORS:
        # personas judged by all 3 judges (intersection) — use union actually OK because alpha handles missing
        all_personas = sorted({p for (g, j, p, c) in total_index if g == gid})
        # alpha on totals: matrix[unit][rater]; unit = (persona, condition); rater = judge
        units_totals: list[list[float | None]] = []
        for pid in all_personas:
            for cond in CONDITIONS:
                row = [total_index.get((gid, jid, pid, cond)) for jid in JUDGES]
                if any(v is not None for v in row):
                    units_totals.append(row)
        alpha_total = krippendorff_alpha_interval(units_totals) if units_totals else None

        per_dim_alpha: dict = {}
        for dim in DIMENSIONS:
            units_dim: list[list[float | None]] = []
            for pid in all_personas:
                for cond in CONDITIONS:
                    row = [score_index.get((gid, jid, pid, cond, dim)) for jid in JUDGES]
                    if any(v is not None for v in row):
                        units_dim.append(row)
            per_dim_alpha[dim] = fmt(krippendorff_alpha_interval(units_dim) if units_dim else None)

        # Pairwise spearman on condition means (one mean per condition per judge)
        cond_means_by_judge: dict[str, list[float]] = {}
        for jid in JUDGES:
            means = []
            for cond in CONDITIONS:
                vals = [s for (g, j, p, c), s in total_index.items()
                        if g == gid and j == jid and c == cond]
                means.append(statistics.mean(vals) if vals else float("nan"))
            cond_means_by_judge[jid] = means

        pairwise: dict = {}
        for ja, jb in itertools.combinations(JUDGES, 2):
            xs = cond_means_by_judge[ja]
            ys = cond_means_by_judge[jb]
            xs2 = [v for v in xs if not math.isnan(v)]
            ys2 = [v for v in ys if not math.isnan(v)]
            if len(xs2) == len(ys2) == len(CONDITIONS):
                pairwise[f"{ja}__vs__{jb}"] = fmt(spearman(xs, ys), 4)
            else:
                pairwise[f"{ja}__vs__{jb}"] = None

        agreement["by_generator"][gid] = {
            "krippendorff_alpha_total": fmt(alpha_total),
            "krippendorff_alpha_per_dimension": per_dim_alpha,
            "spearman_pairwise_condition_means": pairwise,
            "n_units_for_alpha": len(units_totals),
        }
    return agreement


def compute_akm_lift_table(per_gen_summary: dict) -> list[dict]:
    """Core supplement table: AKM lift per generator.
    Δ_akm = akm_profile.total - no_profile.total
    Δ_elicited = akm_elicited.total - no_profile.total
    Flag any generator where Δ ≤ 0 (AKM disadvantage = honest counterexample).
    """
    rows = []
    for gid, block in per_gen_summary["by_generator"].items():
        p = block["pooled"]
        no_p = p["no_profile"]["total_mean"]
        unstr = p["unstructured_notes"]["total_mean"]
        akm = p["akm_profile"]["total_mean"]
        elic = p["akm_elicited"]["total_mean"]
        n = block["n_personas_with_scores"]
        if no_p is None or akm is None:
            rows.append({
                "generator": gid,
                "n_personas": n,
                "no_profile": no_p,
                "unstructured": unstr,
                "akm_profile": akm,
                "akm_elicited": elic,
                "delta_akm_vs_no": None,
                "delta_elicited_vs_no": None,
                "akm_advantage_holds": None,
                "note": "incomplete data",
            })
            continue
        dA = round(akm - no_p, 3)
        dE = round(elic - no_p, 3) if elic is not None else None
        akm_holds = dA > 0 and (dE is None or dE > 0)
        rows.append({
            "generator": gid,
            "n_personas": n,
            "no_profile": no_p,
            "unstructured": unstr,
            "akm_profile": akm,
            "akm_elicited": elic,
            "delta_akm_vs_no": dA,
            "delta_elicited_vs_no": dE,
            "akm_advantage_holds": akm_holds,
            "note": "OK" if akm_holds else "WARNING: AKM advantage absent or reversed",
        })
    return rows


def main() -> None:
    out_dir = ROOT / "results" / "v1.1"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Loading all judgments (v1.0 DS + v1.1 4 new generators)...")
    records = load_all_judgments()
    print(f"Total judgment records: {len(records)}")

    # Per-generator counts
    by_gen_counts: dict = defaultdict(lambda: defaultdict(int))
    for rec in records:
        by_gen_counts[rec["generator_id"]][rec["judge_id"]] += 1
    for gid in ALL_GENERATORS:
        cnts = by_gen_counts.get(gid, {})
        print(f"  {gid}: " + ", ".join(f"{j}={cnts.get(j,0)}" for j in JUDGES))

    print("\nComputing per-generator summary...")
    per_gen_summary, score_index, total_index, best_index, _ = compute_per_generator_summary(records)

    print("Computing per-generator agreement (alpha + spearman)...")
    agreement = compute_per_generator_agreement(score_index, total_index)

    print("Computing AKM lift table...")
    lift_table = compute_akm_lift_table(per_gen_summary)
    for row in lift_table:
        flag = "OK " if row.get("akm_advantage_holds") else "WARN"
        print(f"  [{flag}] {row['generator']:18} n={row['n_personas']:3}  "
              f"no={row['no_profile']}  unstr={row['unstructured']}  "
              f"akm={row['akm_profile']}  elic={row['akm_elicited']}  "
              f"dA={row['delta_akm_vs_no']}  dE={row['delta_elicited_vs_no']}")

    # Write outputs
    (out_dir / "scores_summary_v11.json").write_text(
        json.dumps(per_gen_summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "agreement_v11.json").write_text(
        json.dumps(agreement, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "akm_lift_by_generator.json").write_text(
        json.dumps(lift_table, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Long CSV with generator
    long_path = out_dir / "scores_long.csv"
    with long_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["profile_id", "generator_id", "judge_id", "condition", "dimension", "score"])
        w.writeheader()
        for (gid, jid, pid, cond, dim), s in score_index.items():
            w.writerow({"profile_id": pid, "generator_id": gid, "judge_id": jid,
                        "condition": cond, "dimension": dim, "score": s})

    print(f"\nOutputs written to {out_dir}/")
    print(f"  scores_summary_v11.json")
    print(f"  agreement_v11.json")
    print(f"  akm_lift_by_generator.json  <-- core supplement table")
    print(f"  scores_long.csv  ({len(score_index)} rows)")


if __name__ == "__main__":
    main()
