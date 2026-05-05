"""
文件：verify_v11.py
核心功能：把 supplement_v1.1.md 中所有写入的数字与 results/v1.1/*.json 真值闭环对比，0 mismatch 才算通过。
        v1.0 的 verify_paper_numbers.py 是面向 LaTeX 论文表的；本脚本面向 supplement.md（多 generator 维度）。
        会扫 supplement.md 的所有"GENERATOR_NUMBER:value"声明（特殊注释格式），与 JSON 比较。
输入：supplement_v1.1.md（含 verify-tag 注释）、results/v1.1/scores_summary_v11.json、akm_lift_by_generator.json、agreement_v11.json
输出：stdout 打印 verify 结果。0 mismatch = OK；任一 mismatch 须在 supplement 中改正后再跑。
维护要求：每次手改 supplement.md 数字都必须重跑本脚本。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results" / "v1.1"

NEW_GENERATORS = ["gpt_5_4_mini", "qwen_3_6_plus", "kimi_k2_6", "glm_5_1", "gemma_4_31b_it"]
ALL_GENERATORS = ["deepseek_v4_pro"] + NEW_GENERATORS
DIMENSIONS = [
    "constraint_adherence", "risk_control", "specificity",
    "actionability", "personal_fit", "tradeoff_awareness",
]
CONDITIONS = ["no_profile", "unstructured_notes", "akm_profile", "akm_elicited"]


def load_summary() -> dict:
    return json.loads((RESULTS / "scores_summary_v11.json").read_text(encoding="utf-8"))


def load_lift() -> list[dict]:
    return json.loads((RESULTS / "akm_lift_by_generator.json").read_text(encoding="utf-8"))


def load_agreement() -> dict:
    return json.loads((RESULTS / "agreement_v11.json").read_text(encoding="utf-8"))


def verify_supplement_numbers(supplement_path: Path) -> tuple[int, int]:
    """Scan supplement.md for HTML comments of the form
    <!-- verify: generator=X condition=Y stat=Z value=N -->
    and check each against the JSON ground truth.
    Returns (n_checked, n_mismatch).
    """
    if not supplement_path.exists():
        print(f"[skip] supplement not found at {supplement_path}")
        return (0, 0)

    text = supplement_path.read_text(encoding="utf-8")
    summary = load_summary()
    lift = {row["generator"]: row for row in load_lift()}
    agreement = load_agreement()

    pattern = re.compile(r"<!--\s*verify:\s*(.+?)\s*-->", re.DOTALL)
    n_checked = 0
    n_mismatch = 0
    mismatches: list[str] = []

    for match in pattern.finditer(text):
        body = match.group(1)
        kv = dict(p.split("=", 1) for p in body.split() if "=" in p)
        n_checked += 1
        try:
            stat = kv["stat"]
            paper_value = float(kv["value"])
            tol = float(kv.get("tol", "0.01"))
        except (KeyError, ValueError) as exc:
            mismatches.append(f"  [malformed verify tag] body_repr={body!r} ({len(body)} chars): missing {exc}")
            n_mismatch += 1
            continue

        # Resolve true value
        true_value = None
        if stat == "alpha_total":
            gid = kv["generator"]
            true_value = agreement["by_generator"][gid]["krippendorff_alpha_total"]
        elif stat == "alpha_dim":
            gid = kv["generator"]
            dim = kv["dim"]
            true_value = agreement["by_generator"][gid]["krippendorff_alpha_per_dimension"][dim]
        elif stat == "total_mean":
            gid = kv["generator"]; cond = kv["condition"]
            true_value = summary["by_generator"][gid]["pooled"][cond]["total_mean"]
        elif stat == "total_std":
            gid = kv["generator"]; cond = kv["condition"]
            true_value = summary["by_generator"][gid]["pooled"][cond]["total_std"]
        elif stat == "dim_mean":
            gid = kv["generator"]; cond = kv["condition"]; dim = kv["dim"]
            true_value = summary["by_generator"][gid]["pooled"][cond]["dimensions"].get(dim)
        elif stat == "lift_akm":
            gid = kv["generator"]
            true_value = lift[gid]["delta_akm_vs_no"]
        elif stat == "lift_elicited":
            gid = kv["generator"]
            true_value = lift[gid]["delta_elicited_vs_no"]
        elif stat == "n_personas":
            gid = kv["generator"]
            true_value = lift[gid]["n_personas"]
        else:
            mismatches.append(f"  [unknown stat] {body}")
            n_mismatch += 1
            continue

        if true_value is None:
            mismatches.append(f"  [no JSON data] {body}: paper={paper_value}, json=None")
            n_mismatch += 1
            continue
        if abs(float(true_value) - paper_value) > tol:
            mismatches.append(
                f"  [MISMATCH] {body}: paper={paper_value}, json={true_value:.4f}, "
                f"diff={paper_value - float(true_value):+.4f}"
            )
            n_mismatch += 1

    return n_checked, n_mismatch, mismatches


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    supplement = ROOT / "supplement_v1.1.md"
    n, mm, msgs = verify_supplement_numbers(supplement)
    print(f"verify_v11: {n} numbers checked, {mm} mismatches")
    if mm:
        print("\n".join(msgs))
        sys.exit(1)
    print("OK: 0 mismatch")


if __name__ == "__main__":
    main()
