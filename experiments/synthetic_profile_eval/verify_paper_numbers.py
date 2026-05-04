#!/usr/bin/env python3
"""
文件：verify_paper_numbers.py
核心功能：把 4 篇论文 LaTeX 表格中的所有数字与 results/v1/*.json 实测值闭环对比，
        穷尽每个 condition × 每个 dimension × 每个 statistic。输出不一致清单。
输入：4 篇 main.tex + 5 个 JSON（scores_summary / agreement / subset_advisory / subset_fitness / subset_fashion）
输出：stdout 打印每处差异（论文写的 vs JSON 真值），便于 reviewer-grade reproducibility 检查。
维护要求：每次修改任何论文表格或重跑实验，都必须重新跑一次本脚本，0 mismatch 才算通过。
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

mismatches = []

def check(paper_name, label, paper_value, true_value, tol=0.015):
    if abs(paper_value - true_value) > tol:
        mismatches.append((paper_name, label, paper_value, true_value, round(paper_value - true_value, 4)))

def expect_row(paper_name, condition_label, paper_total, paper_dims, paper_std, json_pooled):
    p = json_pooled[condition_label]
    check(paper_name, f"{condition_label}.total", paper_total, p["total_mean"])
    if paper_std is not None:
        check(paper_name, f"{condition_label}.std", paper_std, p["total_std"])
    dim_keys = ["constraint_adherence","risk_control","specificity","actionability","personal_fit","tradeoff_awareness"]
    for k, v in zip(dim_keys, paper_dims):
        check(paper_name, f"{condition_label}.{k}", v, p["dimensions"][k])

# 母论文 Table 1 (pooled, n=150) — 修改后
expect_row("AKM母论文", "no_profile",         10.57, [1.43,2.19,2.02,2.28,1.31,1.34], 3.96, scores["pooled"])
expect_row("AKM母论文", "unstructured_notes", 20.93, [3.71,4.06,3.47,3.83,3.39,2.51], 4.26, scores["pooled"])
expect_row("AKM母论文", "akm_profile",        29.34, [4.90,4.93,4.94,4.94,4.85,4.84], 1.44, scores["pooled"])
expect_row("AKM母论文", "akm_elicited",       29.11, [4.85,4.92,4.92,4.88,4.83,4.77], 1.41, scores["pooled"])

# DaE Table 1 (advisory, n=90) — 修改后
expect_row("DaE", "no_profile",         10.80, [1.43,2.44,1.94,2.26,1.33,1.40], 4.17, sub_adv["pooled"])
expect_row("DaE", "unstructured_notes", 21.06, [3.69,4.09,3.41,3.86,3.41,2.66], 3.98, sub_adv["pooled"])
expect_row("DaE", "akm_profile",        29.43, [4.94,4.96,4.96,4.94,4.90,4.84], 1.32, sub_adv["pooled"])
expect_row("DaE", "akm_elicited",       29.10, [4.88,4.93,4.89,4.84,4.86,4.81], 1.53, sub_adv["pooled"])

# Fitness Table (fitness subset, n=30) — 修改后
expect_row("Fitness", "no_profile",         10.20, [1.37,1.63,2.27,2.47,1.17,1.30], None, sub_fit["pooled"])
expect_row("Fitness", "unstructured_notes", 22.50, [3.90,4.27,3.90,4.23,3.57,2.63], None, sub_fit["pooled"])
expect_row("Fitness", "akm_profile",        29.23, [4.83,4.87,4.93,4.93,4.83,4.83], None, sub_fit["pooled"])
expect_row("Fitness", "akm_elicited",       28.83, [4.73,4.83,4.97,4.90,4.73,4.67], None, sub_fit["pooled"])

# Fashion Table (fashion subset, n=30) — 修改后
expect_row("Fashion", "no_profile",         10.23, [1.47,2.00,2.00,2.17,1.40,1.20], None, sub_fas["pooled"])
expect_row("Fashion", "unstructured_notes", 19.00, [3.60,3.77,3.20,3.33,3.17,1.93], None, sub_fas["pooled"])
expect_row("Fashion", "akm_profile",        29.17, [4.83,4.90,4.90,4.93,4.73,4.87], None, sub_fas["pooled"])
expect_row("Fashion", "akm_elicited",       29.43, [4.90,4.97,4.97,4.97,4.87,4.77], None, sub_fas["pooled"])

# 母论文全量 alpha
def check_alpha(paper_name, label, paper_value, true_value):
    check(paper_name, label, paper_value, true_value, tol=0.005)

check_alpha("AKM母论文", "alpha_total", 0.948, agreement["krippendorff_alpha_total"])
for k, paper_v in [("constraint_adherence",0.937),("risk_control",0.824),("specificity",0.884),
                   ("actionability",0.843),("personal_fit",0.942),("tradeoff_awareness",0.921)]:
    check_alpha("AKM母论文", f"alpha_{k}", paper_v, agreement["krippendorff_alpha_per_dimension"][k])

# DaE alpha 表 (advisory subset真值) — 修改后
check_alpha("DaE", "alpha_total", 0.950, sub_adv["agreement"]["krippendorff_alpha_total"])
for k, paper_v in [("constraint_adherence",0.942),("risk_control",0.779),("specificity",0.909),
                   ("actionability",0.856),("personal_fit",0.943),("tradeoff_awareness",0.922)]:
    check_alpha("DaE", f"alpha_{k}_subset", paper_v, sub_adv["agreement"]["krippendorff_alpha_per_dimension"][k])

print("="*70)
if not mismatches:
    print("✓ 所有数字闭环验证通过 (0 mismatch)")
else:
    print(f"✗ 发现 {len(mismatches)} 处不一致：\n")
    for paper, label, paper_v, true_v, diff in mismatches:
        print(f"  [{paper}] {label}: paper={paper_v}  json={true_v:.4f}  diff={diff:+.4f}")
