<!--
文件：README.md
核心功能：说明 AKM-Benchmark-Toolkit v1.0 的实验目标、数据规模、跨家族 LLM-as-judge 协议、复现命令、输出文件结构与边界声明。
输入：profiles.jsonl（50 personas）、prompts/*.md、run_generation.py、run_judging_multi.py、aggregate_v1.py、DEEPSEEK_API_KEY、OPENROUTER_API_KEY（或 ora.txt）。
输出：outputs/v1/generations.jsonl、outputs/v1/judgments_<judge>.jsonl、results/v1/scores_long.csv、scores_summary.json、best_answers.csv、agreement.json。
-->

# AKM Benchmark Toolkit v1.0

A reproducible synthetic-profile evaluation for **Active Knowledge Modeling (AKM)**.
v1.0 expands on v0.2 with 50 personas, three cross-family LLM judges, and inter-judge agreement statistics.

## What v1.0 measures

We compare downstream advice quality under **four pre-task user-context conditions**, holding the generator model and prompt template constant:

1. `no_profile` — task only, no user context.
2. `unstructured_notes` — task plus a 80–160 character first-person natural-language self-description.
3. `akm_profile` — task plus a hand-curated structured AKM profile (`goals / hard_constraints / soft_preferences / available_assets / risk_boundaries / decision_style`).
4. `akm_elicited` — task plus an AKM profile **generated automatically** from a simulated AKM elicitation dialogue (5–7 follow-up questions, simulated user answers, then profile extraction).

Conditions 3 and 4 isolate two separate claims:
- (3) *If* a structured AKM profile already exists, does it help downstream tasks?
- (4) Can the AKM elicitation protocol *itself* produce a good-enough profile from a cold start?

## Data

- **50 synthetic personas** across 7 domains (advisory-heavy):

| Domain | n | Sub-scenario coverage |
| --- | ---: | --- |
| career | 6 | mid-life pivot, side project, project-acceptance, energy reallocation |
| learning | 6 | 3-month plan, certification ROI, year-long uplift, work-study integration |
| investment | 6 | 12-mo allocation, in/out timing, education fund, housing, passive income |
| health_lifestyle | 6 | improvement plan, work-day routine, weekend recovery, top-risk, exam decision |
| relationship | 6 | family repair, parental boundary, intimate communication, kids, workplace, friends |
| fitness | 10 | 8-week plan, home setup, injury return, plateau, cut, mid-life, volume audit, travel |
| fashion | 10 | seasonal budget, capsule, occasion, declutter, body-change, low-budget, identity, travel |

- Each persona has a `persona` (ground-truth state), an `unstructured_notes` first-person fragment, a hand-aligned `akm_profile`, and a `task`.
- Total generated answers: **50 × 4 = 200**.
- Total judgments: **200 × 3 = 600** (three judges score the same anonymized 4-answer set per profile).

## Models

| Role | Model | Provider | Why |
| --- | --- | --- | --- |
| Generator | `deepseek-v4-pro` (thinking disabled) | DeepSeek | Single high-capability generator to isolate the *condition* effect; cheap and recent (2026-04). |
| Judge 1 | `deepseek-v4-pro` (thinking disabled) | DeepSeek | Same family as generator (self-judging baseline). |
| Judge 2 | `google/gemini-3-flash-preview` | OpenRouter | Cross-family check (Google). |
| Judge 3 | `x-ai/grok-4.3` | OpenRouter | Cross-family check (xAI). |

Each judge receives the **same anonymized 4-answer set** per persona (deterministic shuffle seeded by `profile_id`) and rates each anonymous answer on six 1–5 dimensions plus picks a `best_answer_label`.

## Headline results

```text
Pooled across 3 judges, 50 personas (n=150 per condition):

  no_profile          mean=10.57   std=4.4
  unstructured_notes  mean=20.93   std=4.7
  akm_profile         mean=29.34   std=1.7
  akm_elicited        mean=29.11   std=1.4

Krippendorff alpha (interval, 3 raters): 0.948
Per-dimension alpha:
  constraint_adherence  0.937
  risk_control          0.824
  specificity           0.884
  actionability         0.843
  personal_fit          0.942
  tradeoff_awareness    0.921

Pairwise Spearman rho on condition rankings:
  deepseek_v4_pro vs gemini_3_flash : 1.00
  deepseek_v4_pro vs grok_4_3       : 1.00
  gemini_3_flash  vs grok_4_3       : 1.00

Best-answer votes (150 total):
  no_profile           0
  unstructured_notes   1
  akm_profile         70
  akm_elicited        47
  (the remaining 32 votes were not parseable as a single answer label
   in one judge's structured output and are excluded from the count;
   they do not affect the dimension means above.)
```

## Reproduce

Requirements:
- Python 3.11+ (no third-party packages required for the core pipeline).
- DeepSeek API key in env var `DEEPSEEK_API_KEY` or in `<workspace_root>/dsapi.txt`.
- OpenRouter API key in env var `OPENROUTER_API_KEY` or in `<workspace_root>/ora.txt`.

```powershell
cd experiments\synthetic_profile_eval

# Step A: regenerate all 200 answers (skips records already in outputs\v1\generations.jsonl).
python run_generation.py

# Step B: run the three judges (each writes its own jsonl, fully resumable).
python run_judging_multi.py --judge deepseek_v4_pro
python run_judging_multi.py --judge gemini_3_flash
python run_judging_multi.py --judge grok_4_3

# Step C: aggregate.
python aggregate_v1.py
```

To regenerate the personas themselves:

```powershell
python generate_profiles.py
```

## Output layout

```text
outputs/
  v1/
    generations.jsonl                # 200 lines, one per (profile_id, condition)
    judgments_deepseek_v4_pro.jsonl  # 50 lines
    judgments_gemini_3_flash.jsonl   # 50 lines
    judgments_grok_4_3.jsonl         # 50 lines
    profiles_generation_log.jsonl    # provenance for each newly synthesized persona
results/
  v1/
    scores_long.csv      # profile x judge x condition x dimension long table
    scores_summary.json  # by_judge / pooled / by_domain means and stds
    best_answers.csv     # best-answer counts per judge and pooled
    agreement.json       # Krippendorff alpha (total + per-dim) and pairwise Spearman
```

## Boundary

This is a synthetic evaluation. It supports a narrow but defensible claim:
**under controlled synthetic profiles and three independent cross-family LLM judges in near-perfect agreement, both a hand-curated AKM profile and an AKM-elicited profile substantially outperform an unstructured first-person note (and trivially outperform no profile at all) on six downstream advisory-quality dimensions.**

It does **not** claim:
- that real users will provide enough information through AKM elicitation in production,
- clinical efficacy or behavioral change,
- universal personalization performance across cultures or task types,
- transfer to high-stakes decisions where calibration of *advice itself* matters more than constraint adherence.

The judge models share at least one obvious failure mode: they all rated the *structured* condition near the ceiling (≈4.95/5 on every dimension), suggesting the rubric saturates quickly. Future work should add ceiling-resistant rubrics (e.g. forced ranking, per-constraint pass/fail counts) before scaling.

## akm_elicited flow

```text
synthetic persona
  -> simulated user answers AKM elicitation questions (DeepSeek-V4-pro)
  -> profile extraction (DeepSeek-V4-pro JSON mode)
  -> downstream task answer (DeepSeek-V4-pro)
  -> blind 3-judge LLM-as-judge evaluation
```
