"""
文件：aggregate_v1.py
核心功能：聚合三 judge 的盲评结果，输出条件均分矩阵、best-answer 投票、判官一致性（Krippendorff α 与判官间 Spearman ρ）。
输入：outputs/v1/judgments_<judge>.jsonl（label_map 把匿名标签映射回 condition）。
输出：results/v1/scores_long.csv（profile × judge × condition × dimension 长表）、scores_summary.json、best_answers.csv、agreement.json。
"""

from __future__ import annotations

import csv
import itertools
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JUDGE_FILES = {
    "deepseek_v4_pro": "judgments_deepseek_v4_pro.jsonl",
    "gemini_3_flash": "judgments_gemini_3_flash.jsonl",
    "grok_4_3": "judgments_grok_4_3.jsonl",
}
DIMENSIONS = [
    "constraint_adherence",
    "risk_control",
    "specificity",
    "actionability",
    "personal_fit",
    "tradeoff_awareness",
]
CONDITIONS = ["no_profile", "unstructured_notes", "akm_profile", "akm_elicited"]


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _normalize_judgment(judgment) -> dict:
    """Normalize many judgment shapes into a flat dict keyed by 'answer_X'.
    Handles:
      a) {"answer_a": {...}, "answer_b": {...}}
      b) {"evaluations": [{"answer_label": "answer_a", ...}, ...]}
      c) [{"answer_a": {...}}, {"answer_b": {...}}, ...] (Gemini list of single-label dicts)
      d) [{"answer_label": "answer_a", "constraint_adherence": ...}, ...] (Gemini list of flat objects)
      e) {"answer_scores": {"answer_a": {...}, ...}} (Grok variant)
    Returns dict possibly augmented with carry-overs of best_answer_label.
    """
    if isinstance(judgment, dict):
        merged: dict = dict(judgment)
        if "evaluations" in merged:
            ev = merged["evaluations"]
            if isinstance(ev, list):
                for item in ev:
                    if isinstance(item, dict) and "answer_label" in item:
                        label = item["answer_label"]
                        inner = {k: v for k, v in item.items() if k != "answer_label"}
                        merged.setdefault(label, inner)
            elif isinstance(ev, dict):
                for label, inner in ev.items():
                    if isinstance(inner, dict):
                        merged.setdefault(label, inner)
        if "answer_scores" in merged and isinstance(merged["answer_scores"], dict):
            for label, inner in merged["answer_scores"].items():
                merged.setdefault(label, inner)
        if "scores" in merged and isinstance(merged["scores"], dict):
            for label, inner in merged["scores"].items():
                if isinstance(inner, dict):
                    merged.setdefault(label, inner)
        return merged
    if isinstance(judgment, list):
        merged = {}
        for item in judgment:
            if not isinstance(item, dict):
                continue
            label_keys = [k for k in item.keys() if k.startswith("answer_") and isinstance(item[k], dict)]
            if label_keys:
                for k in label_keys:
                    merged.setdefault(k, item[k])
            elif "answer_label" in item:
                label = item["answer_label"]
                inner = {k: v for k, v in item.items() if k != "answer_label"}
                merged.setdefault(label, inner)
            else:
                merged.update(item)
        return merged
    return {}


def extract_scores(judgment, label: str) -> dict | None:
    j = _normalize_judgment(judgment)
    if "scores" in j and isinstance(j["scores"], dict) and label in j["scores"]:
        return j["scores"][label]
    if label in j and isinstance(j[label], dict):
        return j[label]
    if "answers" in j and isinstance(j["answers"], dict) and label in j["answers"]:
        return j["answers"][label]
    return None


def extract_best_answer(judgment) -> str | None:
    j = _normalize_judgment(judgment)
    for k in ("best_answer_label", "best_answer", "best"):
        if k in j:
            v = j[k]
            if isinstance(v, str) and v.startswith("answer_"):
                return v
    # DeepSeek puts best_answer_label inside each answer block as boolean.
    for label in sorted(j.keys()):
        if label.startswith("answer_") and isinstance(j[label], dict):
            v = j[label].get("best_answer_label")
            if v is True:
                return label
    return None


def parse_score_value(node: dict, dim: str) -> float | None:
    if dim not in node:
        return None
    v = node[dim]
    if isinstance(v, dict):
        for k in ("score", "value", "rating"):
            if k in v:
                v = v[k]
                break
    try:
        f = float(v)
        if math.isnan(f):
            return None
        return f
    except (ValueError, TypeError):
        return None


def krippendorff_alpha_interval(matrix: list[list[float | None]]) -> float | None:
    """matrix[unit][rater]; values in same scale; missing = None.
    Implements interval Krippendorff alpha.
    """
    n_units = len(matrix)
    if n_units < 2:
        return None
    pairs: list[tuple[float, float]] = []
    for unit in matrix:
        present = [v for v in unit if v is not None]
        if len(present) < 2:
            continue
        for a, b in itertools.combinations(present, 2):
            pairs.extend([(a, b), (b, a)])
    if not pairs:
        return None
    Do = sum((a - b) ** 2 for a, b in pairs) / len(pairs)
    flat = [v for unit in matrix for v in unit if v is not None]
    if len(flat) < 2:
        return None
    De_pairs = []
    for a, b in itertools.combinations(flat, 2):
        De_pairs.extend([(a - b) ** 2, (b - a) ** 2])
    De = sum(De_pairs) / len(De_pairs)
    if De == 0:
        return 1.0 if Do == 0 else 0.0
    return 1 - Do / De


def spearman(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 2:
        return None

    def ranks(values: list[float]) -> list[float]:
        sorted_pairs = sorted(enumerate(values), key=lambda x: x[1])
        rank_map: list[float] = [0.0] * len(values)
        i = 0
        while i < len(sorted_pairs):
            j = i
            while j + 1 < len(sorted_pairs) and sorted_pairs[j + 1][1] == sorted_pairs[i][1]:
                j += 1
            avg_rank = (i + j) / 2 + 1
            for k in range(i, j + 1):
                rank_map[sorted_pairs[k][0]] = avg_rank
            i = j + 1
        return rank_map

    rx = ranks(xs)
    ry = ranks(ys)
    n = len(xs)
    mean_rx = sum(rx) / n
    mean_ry = sum(ry) / n
    num = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n))
    den_x = math.sqrt(sum((rx[i] - mean_rx) ** 2 for i in range(n)))
    den_y = math.sqrt(sum((ry[i] - mean_ry) ** 2 for i in range(n)))
    if den_x == 0 or den_y == 0:
        return None
    return num / (den_x * den_y)


def main() -> None:
    out_dir = ROOT / "results" / "v1"
    out_dir.mkdir(parents=True, exist_ok=True)

    long_rows: list[dict] = []
    judgments: dict[str, list[dict]] = {
        jid: read_jsonl(ROOT / "outputs" / "v1" / fname) for jid, fname in JUDGE_FILES.items()
    }

    print("Records per judge:")
    for jid, recs in judgments.items():
        print(f"  {jid}: {len(recs)}")

    score_index: dict[tuple, float] = {}
    total_index: dict[tuple, float] = {}
    best_index: dict[tuple, str] = {}

    for jid, recs in judgments.items():
        for rec in recs:
            profile_id = rec["profile_id"]
            domain = rec["domain"]
            label_map: dict[str, str] = rec["label_map"]
            judgment = rec["judgment"]
            for label, condition in label_map.items():
                node = extract_scores(judgment, label)
                if node is None:
                    continue
                dim_scores = {}
                for dim in DIMENSIONS:
                    val = parse_score_value(node, dim)
                    if val is None:
                        continue
                    dim_scores[dim] = val
                    score_index[(profile_id, jid, condition, dim)] = val
                    long_rows.append({
                        "profile_id": profile_id,
                        "domain": domain,
                        "judge_id": jid,
                        "condition": condition,
                        "dimension": dim,
                        "score": val,
                    })
                if dim_scores:
                    total_index[(profile_id, jid, condition)] = sum(dim_scores.values())
            best_label = extract_best_answer(judgment)
            if best_label and best_label in label_map:
                best_index[(profile_id, jid)] = label_map[best_label]

    # Write long CSV
    long_csv = out_dir / "scores_long.csv"
    with long_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["profile_id", "domain", "judge_id", "condition", "dimension", "score"])
        w.writeheader()
        w.writerows(long_rows)
    print(f"Wrote {long_csv} ({len(long_rows)} rows)")

    # Summary: mean score per (judge, condition, dimension) and total
    summary: dict = {"by_judge": {}, "pooled": {}, "by_domain": {}}
    judges = list(JUDGE_FILES.keys())

    for jid in judges:
        per_cond = {}
        for cond in CONDITIONS:
            dim_means = {}
            for dim in DIMENSIONS:
                vals = [s for (pid, j, c, d), s in score_index.items() if j == jid and c == cond and d == dim]
                if vals:
                    dim_means[dim] = round(statistics.mean(vals), 3)
            totals = [s for (pid, j, c), s in total_index.items() if j == jid and c == cond]
            per_cond[cond] = {
                "n": len(totals),
                "total_mean": round(statistics.mean(totals), 3) if totals else None,
                "total_std": round(statistics.pstdev(totals), 3) if len(totals) > 1 else None,
                "dimensions": dim_means,
            }
        summary["by_judge"][jid] = per_cond

    pooled = {}
    for cond in CONDITIONS:
        dim_means = {}
        for dim in DIMENSIONS:
            vals = [s for (pid, j, c, d), s in score_index.items() if c == cond and d == dim]
            if vals:
                dim_means[dim] = round(statistics.mean(vals), 3)
        totals = [s for (pid, j, c), s in total_index.items() if c == cond]
        pooled[cond] = {
            "n": len(totals),
            "total_mean": round(statistics.mean(totals), 3) if totals else None,
            "total_std": round(statistics.pstdev(totals), 3) if len(totals) > 1 else None,
            "dimensions": dim_means,
        }
    summary["pooled"] = pooled

    # By domain (pooled across judges)
    domains = sorted({rec["domain"] for recs in judgments.values() for rec in recs})
    for domain in domains:
        dom_block = {}
        for cond in CONDITIONS:
            totals = [
                s for (pid, j, c), s in total_index.items()
                if c == cond and any(
                    rec["profile_id"] == pid and rec["domain"] == domain
                    for recs in judgments.values() for rec in recs
                )
            ]
            dom_block[cond] = {
                "n": len(totals),
                "total_mean": round(statistics.mean(totals), 3) if totals else None,
            }
        summary["by_domain"][domain] = dom_block

    (out_dir / "scores_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_dir / 'scores_summary.json'}")

    # Best answer counts per judge and pooled
    best_csv = out_dir / "best_answers.csv"
    best_counts: dict = {jid: {c: 0 for c in CONDITIONS} for jid in judges}
    pooled_best: dict = {c: 0 for c in CONDITIONS}
    for (pid, jid), cond in best_index.items():
        best_counts[jid][cond] += 1
        pooled_best[cond] += 1
    with best_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["judge"] + CONDITIONS)
        for jid in judges:
            w.writerow([jid] + [best_counts[jid][c] for c in CONDITIONS])
        w.writerow(["pooled"] + [pooled_best[c] for c in CONDITIONS])
    print(f"Wrote {best_csv}")

    # Agreement: Krippendorff alpha on per-(profile, condition) total scores; raters = judges
    profile_ids = sorted({rec["profile_id"] for recs in judgments.values() for rec in recs})
    matrix: list[list[float | None]] = []
    for pid in profile_ids:
        for cond in CONDITIONS:
            row = [total_index.get((pid, jid, cond)) for jid in judges]
            matrix.append(row)
    alpha_total = krippendorff_alpha_interval(matrix)

    # Per-dimension alpha
    alpha_per_dim: dict = {}
    for dim in DIMENSIONS:
        m = []
        for pid in profile_ids:
            for cond in CONDITIONS:
                row = [score_index.get((pid, jid, cond, dim)) for jid in judges]
                m.append(row)
        alpha_per_dim[dim] = krippendorff_alpha_interval(m)

    # Spearman per pair on condition mean ranking (4 conditions per judge)
    judge_cond_means = {
        jid: [summary["by_judge"][jid][c]["total_mean"] for c in CONDITIONS]
        for jid in judges
    }
    pairwise_spearman = {}
    for j1, j2 in itertools.combinations(judges, 2):
        if all(v is not None for v in judge_cond_means[j1]) and all(v is not None for v in judge_cond_means[j2]):
            pairwise_spearman[f"{j1}__vs__{j2}"] = round(
                spearman(judge_cond_means[j1], judge_cond_means[j2]) or 0.0, 4
            )

    agreement = {
        "n_profiles_with_any_judge": len(profile_ids),
        "krippendorff_alpha_total": round(alpha_total, 4) if alpha_total is not None else None,
        "krippendorff_alpha_per_dimension": {k: (round(v, 4) if v is not None else None) for k, v in alpha_per_dim.items()},
        "spearman_pairwise_condition_means": pairwise_spearman,
        "judge_condition_total_means": {
            jid: dict(zip(CONDITIONS, judge_cond_means[jid])) for jid in judges
        },
    }
    (out_dir / "agreement.json").write_text(json.dumps(agreement, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_dir / 'agreement.json'}")

    # Console summary
    print("\n=== Pooled means ===")
    for cond in CONDITIONS:
        print(f"  {cond}: total={pooled[cond]['total_mean']} (n={pooled[cond]['n']})")
    print("\n=== Krippendorff alpha (interval) ===")
    print(f"  total: {agreement['krippendorff_alpha_total']}")
    for dim, a in agreement["krippendorff_alpha_per_dimension"].items():
        print(f"  {dim}: {a}")
    print("\n=== Best-answer pooled ===")
    for c in CONDITIONS:
        print(f"  {c}: {pooled_best[c]}")


if __name__ == "__main__":
    main()
