"""
文件：aggregate_results.py
核心功能：聚合 DeepSeek 盲评结果，生成 summary.json 与 summary.md，供讨论板、公众号文章和 akm_elicited 后续复盘引用。
输入：profiles.jsonl、outputs/generations.jsonl、outputs/judgments.jsonl。
输出：results/summary.json、results/summary.md。
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONDITIONS = ["no_profile", "unstructured_notes", "akm_profile", "akm_elicited"]
SCORE_KEYS = [
    "constraint_adherence",
    "risk_control",
    "specificity",
    "actionability",
    "personal_fit",
    "tradeoff_awareness",
]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def find_answer_scores(judgment: dict) -> dict[str, dict]:
    if "answers" in judgment:
        return judgment["answers"]
    if "evaluations" in judgment:
        return judgment["evaluations"]
    return {key: value for key, value in judgment.items() if key.startswith("answer_")}


def numeric_score(answer_data: dict, score_key: str) -> float:
    value = answer_data[score_key]
    return float(value)


def count_items(answer_data: dict, key: str) -> int:
    value = answer_data.get(key, [])
    if isinstance(value, list):
        return len(value)
    return 0


def normalize_best_label(label: str) -> str:
    normalized = str(label).strip().lower()
    if normalized in {"a", "b", "c"}:
        return f"answer_{normalized}"
    return normalized


def find_best_label(judgment: dict, answer_scores: dict[str, dict]) -> str:
    if "best_answer_label" in judgment:
        return normalize_best_label(judgment["best_answer_label"])
    for answer_data in answer_scores.values():
        if isinstance(answer_data, dict) and "best_answer_label" in answer_data:
            return normalize_best_label(answer_data["best_answer_label"])
    return ""


def main() -> None:
    profiles = {record["profile_id"]: record for record in read_jsonl(ROOT / "profiles.jsonl")}
    generations = read_jsonl(ROOT / "outputs" / "generations.jsonl")
    judgments = read_jsonl(ROOT / "outputs" / "judgments.jsonl")

    scores: dict[str, dict[str, list[float]]] = {condition: {key: [] for key in SCORE_KEYS} for condition in CONDITIONS}
    item_counts: dict[str, dict[str, list[int]]] = {
        condition: {
            "satisfied_constraints": [],
            "missed_constraints": [],
            "risk_violations": [],
            "profile_details_used": [],
        }
        for condition in CONDITIONS
    }
    best_counts: dict[str, int] = {condition: 0 for condition in CONDITIONS}
    examples: dict[str, dict[str, str]] = defaultdict(dict)

    for generation in generations:
        profile_id = generation["profile_id"]
        condition = generation["condition"]
        if profile_id not in examples:
            examples[profile_id] = {}
        examples[profile_id][condition] = generation["content"]

    for record in judgments:
        answer_scores = find_answer_scores(record["judgment"])
        label_map = record["label_map"]
        for label, condition in label_map.items():
            answer_data = answer_scores[label]
            for score_key in SCORE_KEYS:
                scores[condition][score_key].append(numeric_score(answer_data, score_key))
            for count_key in item_counts[condition]:
                item_counts[condition][count_key].append(count_items(answer_data, count_key))
        best_label = find_best_label(record["judgment"], answer_scores)
        if best_label in label_map:
            best_counts[label_map[best_label]] += 1

    score_means = {
        condition: {
            score_key: round(sum(values) / len(values), 3)
            for score_key, values in score_map.items()
        }
        for condition, score_map in scores.items()
    }
    count_means = {
        condition: {
            count_key: round(sum(values) / len(values), 3)
            for count_key, values in count_map.items()
        }
        for condition, count_map in item_counts.items()
    }
    total_score = {
        condition: round(sum(score_means[condition].values()), 3)
        for condition in CONDITIONS
    }
    summary = {
        "num_profiles": len(profiles),
        "conditions": CONDITIONS,
        "score_means": score_means,
        "count_means": count_means,
        "total_score": total_score,
        "best_counts": best_counts,
    }

    results_dir = ROOT / "results"
    (results_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    lines: list[str] = []
    lines.append("# AKM Synthetic Profile Evaluation Summary")
    lines.append("")
    lines.append(f"- Profiles: {len(profiles)}")
    lines.append(f"- Conditions: {', '.join(CONDITIONS)}")
    lines.append("")
    lines.append("## Mean Scores")
    lines.append("")
    lines.append("| Condition | Total | Constraint | Risk | Specificity | Actionability | Fit | Trade-off |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for condition in CONDITIONS:
        row = score_means[condition]
        lines.append(
            f"| {condition} | {total_score[condition]} | {row['constraint_adherence']} | {row['risk_control']} | {row['specificity']} | {row['actionability']} | {row['personal_fit']} | {row['tradeoff_awareness']} |"
        )
    lines.append("")
    lines.append("## Mean Evidence Counts")
    lines.append("")
    lines.append("| Condition | Satisfied constraints | Missed constraints | Risk violations | Profile details used |")
    lines.append("| --- | ---: | ---: | ---: | ---: |")
    for condition in CONDITIONS:
        row = count_means[condition]
        lines.append(
            f"| {condition} | {row['satisfied_constraints']} | {row['missed_constraints']} | {row['risk_violations']} | {row['profile_details_used']} |"
        )
    lines.append("")
    lines.append("## Best Answer Counts")
    lines.append("")
    for condition in CONDITIONS:
        lines.append(f"- {condition}: {best_counts[condition]}")
    lines.append("")
    lines.append("## Representative Example: fitness_001")
    lines.append("")
    if "fitness_001" in examples:
        for condition in CONDITIONS:
            snippet = examples["fitness_001"][condition].strip().replace("\r\n", "\n")
            lines.append(f"### {condition}")
            lines.append("")
            lines.append("```text")
            lines.append(snippet[:1600])
            lines.append("```")
            lines.append("")
    elicited_gap = round(total_score["akm_elicited"] - total_score["unstructured_notes"], 3)
    ideal_gap = round(total_score["akm_profile"] - total_score["akm_elicited"], 3)
    lines.append("## akm_elicited Check")
    lines.append("")
    lines.append(f"- akm_elicited minus unstructured_notes: {elicited_gap}")
    lines.append(f"- akm_profile minus akm_elicited: {ideal_gap}")
    lines.append("")
    if total_score["akm_elicited"] > total_score["unstructured_notes"]:
        lines.append("The elicited AKM profile condition outperformed unstructured notes in total judge score.")
    else:
        lines.append("The elicited AKM profile condition did not outperform unstructured notes in total judge score. Do not expand to a larger paper experiment before protocol review.")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    if total_score["akm_profile"] > total_score["unstructured_notes"] > total_score["no_profile"]:
        lines.append("AKM structured profiles outperformed unstructured notes and no-profile answers in total judge score.")
    elif total_score["akm_profile"] > total_score["unstructured_notes"]:
        lines.append("AKM structured profiles outperformed unstructured notes, but the ordering against no-profile answers needs manual review.")
    else:
        lines.append("AKM structured profiles did not clearly outperform unstructured notes in total judge score. Do not expand the experiment before manual review.")
    lines.append("")
    lines.append("Boundary: this is a synthetic LLM-as-judge evaluation. It does not establish real-user satisfaction or clinical/behavioral efficacy.")

    (results_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
