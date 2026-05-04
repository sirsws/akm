#!/usr/bin/env python3
"""
文件：generate_latex_tables.py
核心功能：从 results/v1/*.json 直接生成 4 篇论文需要的 LaTeX 表格行（pooled 表 + α 表），
        避免人脑/LLM 手抄数字导致的 reproducibility 不一致。
输入：scores_summary.json / agreement.json / subset_advisory.json / subset_fitness.json / subset_fashion.json
输出：4 段可直接粘贴到 main.tex 的 LaTeX 表格行（每段对应一篇论文）。
维护要求：每次重跑实验，都用本脚本重新生成表格行后再贴进论文，不允许人手改数字。
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results" / "v1"

scores = json.loads((RESULTS / "scores_summary.json").read_text(encoding="utf-8"))
agreement = json.loads((RESULTS / "agreement.json").read_text(encoding="utf-8"))
sub_adv = json.loads((RESULTS / "subset_advisory.json").read_text(encoding="utf-8"))
sub_fit = json.loads((RESULTS / "subset_fitness.json").read_text(encoding="utf-8"))
sub_fas = json.loads((RESULTS / "subset_fashion.json").read_text(encoding="utf-8"))

DIM_KEYS = ["constraint_adherence","risk_control","specificity","actionability","personal_fit","tradeoff_awareness"]

def fmt2(x): return f"{x:.2f}"
def fmt3(x): return f"{x:.3f}"

def pooled_row(label, condition, pooled, with_std=True):
    p = pooled[condition]
    cells = [label, fmt2(p["total_mean"])] + [fmt2(p["dimensions"][k]) for k in DIM_KEYS]
    if with_std:
        cells.append(fmt2(p["total_std"]))
    return " & ".join(cells) + r" \\"

def alpha_block(agreement_dict):
    a = agreement_dict
    out = [f"Krippendorff $\\alpha$ on totals (interval, 3 raters) & {fmt3(a['krippendorff_alpha_total'])} \\\\"]
    name_map = {"constraint_adherence":"constraint\\_adherence","risk_control":"risk\\_control",
                "specificity":"specificity","actionability":"actionability",
                "personal_fit":"personal\\_fit","tradeoff_awareness":"tradeoff\\_awareness"}
    for k in DIM_KEYS:
        out.append(f"$\\alpha$ {name_map[k]}         & {fmt3(a['krippendorff_alpha_per_dimension'][k])} \\\\")
    for pair, v in a.get("spearman_pairwise_condition_means", {}).items():
        nice = pair.replace("__vs__", " vs ").replace("_v4_pro","-V4-pro").replace("_3_flash","-3-Flash").replace("_4_3","-4.3").replace("deepseek","DeepSeek").replace("gemini","Gemini").replace("grok","Grok")
        out.append(f"Spearman $\\rho$ {nice} & {fmt2(v)} \\\\")
    return "\n".join(out)

print("="*70 + "\n母论文 Table 1 (pooled, n=150)\n" + "="*70)
for cond, label in [("no_profile","no\\_profile"),("unstructured_notes","unstructured\\_notes"),
                    ("akm_profile","akm\\_profile"),("akm_elicited","akm\\_elicited")]:
    print(pooled_row(f"{label}         ", cond, scores["pooled"], with_std=True))

print("\n" + "="*70 + "\n母论文 Table 2 (全量 agreement)\n" + "="*70)
print(alpha_block(agreement))

print("\n" + "="*70 + "\nDaE Table (advisory subset, n=90)\n" + "="*70)
for cond, label in [("no_profile","no\\_profile"),("unstructured_notes","unstructured\\_notes"),
                    ("akm_profile","akm\\_profile"),("akm_elicited","akm\\_elicited")]:
    print(pooled_row(f"{label}         ", cond, sub_adv["pooled"], with_std=True))

print("\n--- DaE Table 2 (advisory subset agreement) ---")
print(alpha_block(sub_adv["agreement"]))

print("\n" + "="*70 + "\nFitness Table (fitness subset, n=30)\n" + "="*70)
for cond, label in [("no_profile","no\\_profile"),("unstructured_notes","unstructured\\_notes"),
                    ("akm_profile","akm\\_profile"),("akm_elicited","akm\\_elicited")]:
    print(pooled_row(f"{label}         ", cond, sub_fit["pooled"], with_std=False))
print(f"\n--- Fitness agreement ---\nα_total = {sub_fit['agreement']['krippendorff_alpha_total']:.3f}")
for pair, v in sub_fit["agreement"]["spearman_pairwise_condition_means"].items():
    print(f"ρ {pair}: {v}")
b = sub_fit["best_answer_counts"]["pooled"]
print(f"best-answer pooled: {b} (parseable={sum(b.values())}/{sub_fit['n_personas']*3})")

print("\n" + "="*70 + "\nFashion Table (fashion subset, n=30)\n" + "="*70)
for cond, label in [("no_profile","no\\_profile"),("unstructured_notes","unstructured\\_notes"),
                    ("akm_profile","akm\\_profile"),("akm_elicited","akm\\_elicited")]:
    print(pooled_row(f"{label}         ", cond, sub_fas["pooled"], with_std=False))
print(f"\n--- Fashion agreement ---\nα_total = {sub_fas['agreement']['krippendorff_alpha_total']:.3f}")
for pair, v in sub_fas["agreement"]["spearman_pairwise_condition_means"].items():
    print(f"ρ {pair}: {v}")
b = sub_fas["best_answer_counts"]["pooled"]
print(f"best-answer pooled: {b} (parseable={sum(b.values())}/{sub_fas['n_personas']*3})")
