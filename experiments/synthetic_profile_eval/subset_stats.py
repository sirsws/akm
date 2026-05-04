"""
文件：subset_stats.py
核心功能：从 v1.0 三 judge 数据中按 domain 子集统计均分、维度均分、Krippendorff α、Spearman ρ 与 best-answer 投票，便于 DaE/fitness/fashion 三篇分支论文嵌入数据。
输入：profiles.jsonl、outputs/v1/judgments_<judge>.jsonl、命令行参数 --domains（默认 advisory）。
输出：results/v1/subset_<tag>.json + 控制台表格。
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

from aggregate_v1 import (
    JUDGE_FILES,
    DIMENSIONS,
    CONDITIONS,
    read_jsonl,
    extract_scores,
    extract_best_answer,
    parse_score_value,
    krippendorff_alpha_interval,
    spearman,
)


ROOT = Path(__file__).resolve().parent

PRESETS = {
    "advisory": ["career", "learning", "investment", "health_lifestyle", "relationship"],
    "fitness": ["fitness"],
    "fashion": ["fashion"],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", required=True, choices=list(PRESETS) + ["custom"])
    parser.add_argument("--domains", nargs="+", default=None)
    args = parser.parse_args()

    if args.tag == "custom":
        if not args.domains:
            raise SystemExit("--domains required when --tag custom")
        target_domains = args.domains
    else:
        target_domains = PRESETS[args.tag]

    out_dir = ROOT / "results" / "v1"
    out_dir.mkdir(parents=True, exist_ok=True)

    profiles = {r["profile_id"]: r for r in read_jsonl(ROOT / "profiles.jsonl")}
    target_pids = {pid for pid, p in profiles.items() if p["domain"] in target_domains}
    print(f"Subset tag={args.tag} domains={target_domains} -> {len(target_pids)} personas")

    judges = list(JUDGE_FILES.keys())
    judgments = {jid: read_jsonl(ROOT / "outputs" / "v1" / fname) for jid, fname in JUDGE_FILES.items()}

    score_index: dict = {}
    total_index: dict = {}
    best_index: dict = {}

    for jid, recs in judgments.items():
        for rec in recs:
            if rec["profile_id"] not in target_pids:
                continue
            label_map = rec["label_map"]
            for label, condition in label_map.items():
                node = extract_scores(rec["judgment"], label)
                if node is None:
                    continue
                dim_scores = {}
                for dim in DIMENSIONS:
                    val = parse_score_value(node, dim)
                    if val is None:
                        continue
                    dim_scores[dim] = val
                    score_index[(rec["profile_id"], jid, condition, dim)] = val
                if dim_scores:
                    total_index[(rec["profile_id"], jid, condition)] = sum(dim_scores.values())
            best = extract_best_answer(rec["judgment"])
            if best and best in label_map:
                best_index[(rec["profile_id"], jid)] = label_map[best]

    summary = {"by_judge": {}, "pooled": {}, "n_personas": len(target_pids)}
    for jid in judges:
        per_cond = {}
        for cond in CONDITIONS:
            totals = [s for (pid, j, c), s in total_index.items() if j == jid and c == cond]
            dim_means = {}
            for dim in DIMENSIONS:
                vals = [s for (pid, j, c, d), s in score_index.items() if j == jid and c == cond and d == dim]
                if vals:
                    dim_means[dim] = round(statistics.mean(vals), 3)
            per_cond[cond] = {
                "n": len(totals),
                "total_mean": round(statistics.mean(totals), 3) if totals else None,
                "total_std": round(statistics.pstdev(totals), 3) if len(totals) > 1 else None,
                "dimensions": dim_means,
            }
        summary["by_judge"][jid] = per_cond

    pooled = {}
    for cond in CONDITIONS:
        totals = [s for (pid, j, c), s in total_index.items() if c == cond]
        dim_means = {}
        for dim in DIMENSIONS:
            vals = [s for (pid, j, c, d), s in score_index.items() if c == cond and d == dim]
            if vals:
                dim_means[dim] = round(statistics.mean(vals), 3)
        pooled[cond] = {
            "n": len(totals),
            "total_mean": round(statistics.mean(totals), 3) if totals else None,
            "total_std": round(statistics.pstdev(totals), 3) if len(totals) > 1 else None,
            "dimensions": dim_means,
        }
    summary["pooled"] = pooled

    matrix = []
    for pid in sorted(target_pids):
        for cond in CONDITIONS:
            matrix.append([total_index.get((pid, jid, cond)) for jid in judges])
    alpha_total = krippendorff_alpha_interval(matrix)
    alpha_per_dim = {}
    for dim in DIMENSIONS:
        m = []
        for pid in sorted(target_pids):
            for cond in CONDITIONS:
                m.append([score_index.get((pid, jid, cond, dim)) for jid in judges])
        alpha_per_dim[dim] = krippendorff_alpha_interval(m)

    judge_cond_means = {jid: [summary["by_judge"][jid][c]["total_mean"] for c in CONDITIONS] for jid in judges}
    pairwise_spearman = {}
    import itertools
    for j1, j2 in itertools.combinations(judges, 2):
        if all(v is not None for v in judge_cond_means[j1]) and all(v is not None for v in judge_cond_means[j2]):
            pairwise_spearman[f"{j1}__vs__{j2}"] = round(spearman(judge_cond_means[j1], judge_cond_means[j2]) or 0.0, 4)

    best_counts = {jid: {c: 0 for c in CONDITIONS} for jid in judges}
    pooled_best = {c: 0 for c in CONDITIONS}
    for (pid, jid), cond in best_index.items():
        best_counts[jid][cond] += 1
        pooled_best[cond] += 1

    summary["agreement"] = {
        "krippendorff_alpha_total": round(alpha_total, 4) if alpha_total is not None else None,
        "krippendorff_alpha_per_dimension": {k: (round(v, 4) if v is not None else None) for k, v in alpha_per_dim.items()},
        "spearman_pairwise_condition_means": pairwise_spearman,
    }
    summary["best_answer_counts"] = {"by_judge": best_counts, "pooled": pooled_best}
    summary["domains"] = target_domains

    out_path = out_dir / f"subset_{args.tag}.json"
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")

    print("\n=== pooled ===")
    for c in CONDITIONS:
        p = pooled[c]
        print(f"  {c}: total_mean={p['total_mean']} (n={p['n']}, sd={p['total_std']})")
    print("\nKrippendorff alpha total:", summary["agreement"]["krippendorff_alpha_total"])
    print("Best-answer pooled:", pooled_best)


if __name__ == "__main__":
    main()
