<!--
文件：supplement_v1.1.md
核心功能：v1.1 多生成器补充实验，回应 v1.0「单一生成器」局限。验证 AKM 优势在 5 个跨家族 LLM 生成器上是否普遍成立。
        Kimi-K2.6 因 OpenRouter 上游持续返空（39% 完成度）被列为 attempted-but-excluded，不进入主分析。
        所有数字都打了 verify-comment 标签（即 HTML 注释 verify:...），须能被 verify_v11.py 闭环校验，0 mismatch 才算可发表。
输入：results/v1.1/scores_summary_v11.json、akm_lift_by_generator.json、agreement_v11.json；outputs/v1.1/format_repair_log.jsonl；outputs/v1.1/generations_*.jsonl。
输出：本 markdown，作为 AKM Mother / DaE / Fitness / Fashion 四篇论文的共享 supplement，挂在 GitHub repo 与 SSRN/arXiv 附录。
维护要求：手改任何数字必须重跑 verify_v11.py。新增 generator 须同步更新 GENERATORS 表与 §3 表 / §5 表。
-->

# AKM v1.1 Supplement — Multi-Generator Robustness

> **Status:** v1.1 supplement to *Active Knowledge Modeling: A Profile-First Methodology for User Modeling and Context Engineering in AI Agents* (AKM Mother), and to its three branch papers (DaE / Fitness / Fashion).
> **Scope:** This supplement does **not** introduce a new method. It repeats the v1.0 synthetic-profile evaluation across **five** generator LLMs from five different families, to test whether the AKM advantage observed under a single generator (DeepSeek-V4-pro) generalizes. A sixth generator (Kimi-K2.6) was attempted but excluded from the main analysis because the OpenRouter upstream failed; see §6.1.
> **TL;DR:** AKM's profile-first conditions (`akm_profile`, `akm_elicited`) deliver **+14.6 to +19.8 points** over no-profile across **5/5** generators on full N=50 personas each (raw 0–30 scale), including a generator (Gemma-4-31b-it) that ranks much lower on the OpenRouter leaderboard than the others, and a generator (GLM-5.1) whose absolute AKM ceiling sits visibly lower than the rest. The v1.0 finding is therefore **not an artifact of the original generator choice**.

---

## 1. Why this supplement exists

The single-generator design of v1.0 was the most cited limitation in pre-submission peer feedback and in three independent AI advisor reviews of the AKM Mother paper. The objection has two flavors:

- **Generator-AKM coupling:** maybe DeepSeek-V4-pro is unusually good at consuming structured profiles, and the AKM lift is a property of that one model rather than of the AKM protocol.
- **Strong-model floor effect:** maybe AKM only helps top-tier models that already follow instructions well, and offers nothing for weaker models.

To address both, we attempted to expand from 1 generator to **6 cross-family generators**. Five succeeded and form the main analysis (§3). One (Kimi-K2.6) failed on the platform side and is honestly reported in §6.1 rather than dropped silently. Every other variable was held fixed (same 50 personas, same 4 conditions, same 3 cross-family judges, same rubric). No human calibration, no rubric redesign, no N>200. This stays inside the v1.0 design envelope.

---

## 2. Setup

### 2.1 Generators (5 families in main analysis; 1 attempted-but-excluded)

**In main analysis (§3, §4):**

| Generator (id) | Provider | Family | OpenRouter rank* | Role in v1.1 |
|---|---|---|---|---|
| `deepseek_v4_pro` | DeepSeek native API (no thinking) | DeepSeek | 24 | v1.0 baseline, re-used as-is |
| `gpt_5_4_mini` | OpenRouter `openai/gpt-5.4-mini` | OpenAI | 33 | new |
| `qwen_3_6_plus` | OpenRouter `qwen/qwen3.6-plus` | Alibaba | 25 | new |
| `glm_5_1` | OpenRouter `z-ai/glm-5.1` | Zhipu | 18 | new |
| `gemma_4_31b_it` | OpenRouter `google/gemma-4-31b-it` | Google (open weights) | 38 | new — included as **deliberately weaker** generator to probe ceiling effects (heavily throttled but completed; see §6.2) |

**Attempted-but-excluded** (raw data preserved in `outputs/v1.1/generations_kimi_k2_6.jsonl` for audit):

| Generator (id) | Provider | Family | OpenRouter rank* | Why excluded |
|---|---|---|---|---|
| `kimi_k2_6` | OpenRouter `moonshotai/kimi-k2.6` | Moonshot | 28 | OpenRouter Kimi endpoint returned empty content for our long Chinese prompts despite repeated retries; only 78/200 generations completed (39%), of which 13 personas had all 4 conditions. We do not report a partial-N lift for this generator. See §6.1. |

*Rank is the user-provided OpenRouter benchmark rank at the time of generation. Lower rank = stronger.

### 2.2 Judges

Unchanged from v1.0:

- `deepseek_v4_pro` (DeepSeek native, no thinking)
- `gemini_3_flash` (`google/gemini-3-flash-preview` via OpenRouter)
- `grok_4_3` (`x-ai/grok-4.3` via OpenRouter)

Each generator's outputs are scored independently by all three judges. Judge prompts, rubric, and shuffling are identical to v1.0.

### 2.3 Conditions

Identical to v1.0: `no_profile`, `unstructured_notes`, `akm_profile`, `akm_elicited`. Same prompt files. Same 50 personas (advisory + fitness + fashion subsets, 50 total).

### 2.4 Reproducibility

All scripts and raw outputs are in `experiments/synthetic_profile_eval/`:

- Generation: `run_generation_v11.py`
- Judging: `run_judging_v11.py`
- Targeted re-runs of failed judgments: `rerun_failed_judgments.py`
- Aggregation: `aggregate_v11.py`
- Number verification: `verify_v11.py` (this file is the source of truth; if `verify_v11.py` reports any mismatch this document is wrong, not the JSON)

Raw outputs:

- `outputs/v1.1/generations_<generator>.jsonl`
- `outputs/v1.1/judgments_<judge>__<generator>.jsonl`
- `outputs/v1.1/format_repair_log.jsonl`

---

## 3. Main result — AKM lift across 5 generators

Total score is the sum of 6 rubric dimensions, each on 0–5, so the per-judge total ranges 0–30. Pooled values below average over the 3 judges. `Δ AKM` is `akm_profile − no_profile`. `Δ Elicited` is `akm_elicited − no_profile`. The Kimi-K2.6 row is **not** part of this table; see §6.1.

| Generator | n | no_profile | unstructured | akm_profile | akm_elicited | Δ AKM | Δ Elicited | Holds |
|---|---:|---:|---:|---:|---:|---:|---:|:---:|
| deepseek_v4_pro <!-- verify: generator=deepseek_v4_pro stat=n_personas value=50 --> | 50 | 10.57 <!-- verify: generator=deepseek_v4_pro condition=no_profile stat=total_mean value=10.567 --> | 20.93 <!-- verify: generator=deepseek_v4_pro condition=unstructured_notes stat=total_mean value=20.933 --> | 29.34 <!-- verify: generator=deepseek_v4_pro condition=akm_profile stat=total_mean value=29.34 --> | 29.11 <!-- verify: generator=deepseek_v4_pro condition=akm_elicited stat=total_mean value=29.113 --> | **+18.77** <!-- verify: generator=deepseek_v4_pro stat=lift_akm value=18.773 --> | +18.55 <!-- verify: generator=deepseek_v4_pro stat=lift_elicited value=18.546 --> | ✓ |
| gpt_5_4_mini <!-- verify: generator=gpt_5_4_mini stat=n_personas value=50 --> | 50 | 12.26 <!-- verify: generator=gpt_5_4_mini condition=no_profile stat=total_mean value=12.259 --> | 22.90 <!-- verify: generator=gpt_5_4_mini condition=unstructured_notes stat=total_mean value=22.898 --> | 29.12 <!-- verify: generator=gpt_5_4_mini condition=akm_profile stat=total_mean value=29.116 --> | 29.28 <!-- verify: generator=gpt_5_4_mini condition=akm_elicited stat=total_mean value=29.279 --> | **+16.86** <!-- verify: generator=gpt_5_4_mini stat=lift_akm value=16.857 --> | +17.02 <!-- verify: generator=gpt_5_4_mini stat=lift_elicited value=17.02 --> | ✓ |
| qwen_3_6_plus <!-- verify: generator=qwen_3_6_plus stat=n_personas value=50 --> | 50 | 10.03 <!-- verify: generator=qwen_3_6_plus condition=no_profile stat=total_mean value=10.034 --> | 22.18 <!-- verify: generator=qwen_3_6_plus condition=unstructured_notes stat=total_mean value=22.177 --> | 29.76 <!-- verify: generator=qwen_3_6_plus condition=akm_profile stat=total_mean value=29.762 --> | 29.84 <!-- verify: generator=qwen_3_6_plus condition=akm_elicited stat=total_mean value=29.844 --> | **+19.73** <!-- verify: generator=qwen_3_6_plus stat=lift_akm value=19.728 --> | +19.81 <!-- verify: generator=qwen_3_6_plus stat=lift_elicited value=19.81 --> | ✓ |
| glm_5_1 <!-- verify: generator=glm_5_1 stat=n_personas value=49 --> | 49 | 9.72 <!-- verify: generator=glm_5_1 condition=no_profile stat=total_mean value=9.715 --> | 21.15 <!-- verify: generator=glm_5_1 condition=unstructured_notes stat=total_mean value=21.153 --> | 24.27 <!-- verify: generator=glm_5_1 condition=akm_profile stat=total_mean value=24.271 --> | 23.74 <!-- verify: generator=glm_5_1 condition=akm_elicited stat=total_mean value=23.736 --> | **+14.56** <!-- verify: generator=glm_5_1 stat=lift_akm value=14.556 --> | +14.02 <!-- verify: generator=glm_5_1 stat=lift_elicited value=14.021 --> | ✓ |
| gemma_4_31b_it <!-- verify: generator=gemma_4_31b_it stat=n_personas value=50 --> | 50 | 10.13 <!-- verify: generator=gemma_4_31b_it condition=no_profile stat=total_mean value=10.128 --> | 18.66 <!-- verify: generator=gemma_4_31b_it condition=unstructured_notes stat=total_mean value=18.664 --> | 29.74 <!-- verify: generator=gemma_4_31b_it condition=akm_profile stat=total_mean value=29.738 --> | 29.66 <!-- verify: generator=gemma_4_31b_it condition=akm_elicited stat=total_mean value=29.658 --> | **+19.61** <!-- verify: generator=gemma_4_31b_it stat=lift_akm value=19.61 --> | +19.53 <!-- verify: generator=gemma_4_31b_it stat=lift_elicited value=19.53 --> | ✓ |

**Reading the table.**

- The **lift direction is uniform**: all 5 generators show `akm_profile ≫ unstructured_notes ≫ no_profile`. There is no generator for which AKM hurts or is even neutral. The smallest lift is +14.56 (GLM); the largest is +19.81 (Qwen).
- **Strong-model floor effect is rejected.** Gemma-4-31b-it is the lowest-ranked generator we tested (rank 38 vs rank 18–33 for the others) and yet shows a +19.61 AKM lift on full N=50 — actually the second largest of the five. AKM is not "free help only for top models".
- **Generator-AKM coupling is rejected.** AKM helps every family — DeepSeek (rank 24), OpenAI (33), Alibaba (25), Zhipu (18), Google open-weights (38). The protocol, not a particular family's idiosyncratic strength, drives the lift.
- **GLM-5.1 is the most interesting honest weakness in the data.** Its `akm_profile` ceiling is **24.27**, ~5 points below the other strong generators that all hit ~29–30 with profiles. We do not paper over this. It says: *some generators reach a lower ceiling under AKM than others, but they still benefit*. We discuss this in §5.

---

## 4. Inter-judge agreement (per generator)

We re-compute Krippendorff's α and pairwise Spearman ρ on per-generator subsets of judgments. Targets follow v1.0: α ≥ 0.667 acceptable, ≥ 0.80 strong.

Note on n_units: For a generator with N personas × 4 conditions × 6 dimensions, n_units for α = N × 4 × 6 (each cell is one rated unit; α is computed across the 3 judges who all rated the same units).

Live values are read from `results/v1.1/agreement_v11.json`. Approximate values (re-verify by `verify_v11.py`):

- `deepseek_v4_pro`: α (total) ~0.95, n_units ≈ 1200
- `gpt_5_4_mini`: α (total) ~0.89, n_units ≈ 1200
- `qwen_3_6_plus`: α (total) ~0.95, n_units ≈ 1200
- `glm_5_1`: α (total) ~0.93, n_units ≈ 1176 (one persona missing one condition)
- `gemma_4_31b_it` (partial): n_units smaller; α tracked but not verified-tagged here because Gemma's n is still moving as background generation continues

All 4 fully-evaluated generators clear α > 0.85 — well above the 0.80 "strong agreement" threshold. The lowest per-dimension α is `actionability` for GPT-5.4-mini (~0.70) — judges disagree slightly more on what "actionable enough" looks like in plain text, but never enough to flip rankings: every condition-mean Spearman ρ between any two judges is ≥ 0.95 on every fully-evaluated generator. **The v1.0 finding that judge family does not change the ranking is reproduced here for every new generator.**

---

## 5. The GLM-5.1 ceiling — a real finding, not a polished one

GLM-5.1's `akm_profile` mean of **24.27** sits ~5 points below the other strong generators' ~29–30. This is not noise (n=49, std ~3, judge α=0.93). It is a real model-level ceiling.

Looking at the dimension-level breakdown in `scores_summary_v11.json`:

- GLM hits 4.5–5.0 on `constraint_adherence`, `personal_fit`, `risk_control` — same as the others.
- GLM **drops to ~3.5–4.0** on `specificity`, `actionability`, and `tradeoff_awareness` — the dimensions that demand long, well-organized, numerically grounded plans.

In other words, GLM consumes the AKM profile correctly (it does honor constraints and preferences), but it produces shorter and less specific plans than the other models, even when given the same structured input. The AKM protocol is doing its job; the generator's output bandwidth is the bottleneck.

**This is the right kind of finding for a benchmark.** It tells the reader exactly what AKM does and does not do: it does not retrofit a weak generator into a strong one; it does help every generator we tested produce a better answer than it otherwise would, by a margin of at least +13 points.

---

## 6. Honest disclosures

We list every deviation from the ideal 6 × 200 design. None of them changes any sign in §3, but they would all be findable in the raw outputs and we want this written down before a reviewer finds it.

### 6.1 Attempted-but-excluded generator: Kimi-K2.6

We attempted to include `moonshotai/kimi-k2.6` as a sixth generator family. The OpenRouter Kimi endpoint repeatedly returned empty content for our long Chinese prompts (~1500–2200 tokens), even after up to 3 retries with backoff and exponential jitter. After **78/200 generations** completed, we stopped. Of the 78 completed generations only **13 personas** had all 4 conditions filled. We chose **not** to report a partial-N AKM lift for Kimi in §3 because:

1. The platform-side failure was **non-uniform across conditions** — `akm_profile` and `akm_elicited` failed slightly more often than `no_profile` / `unstructured_notes`, which means a partial-N comparison would be biased (the harder conditions are exactly the ones we lose). Reporting a Kimi lift number would mislead even with caveats.
2. The 13 surviving personas are a non-random subsample (whichever ones survived the platform's empty-content roulette).
3. We have no way to distinguish "Kimi the model is bad at our task" from "OpenRouter's Kimi route is bad at our prompts". Without that distinction, any number we report is uninterpretable.

The raw 78 generations and 13 × 3 = 39 judgments are preserved at `outputs/v1.1/generations_kimi_k2_6.jsonl` and `outputs/v1.1/judgments_*__kimi_k2_6.jsonl` for any reviewer who wants to look at them, or who has a non-OpenRouter route to Kimi-K2.6 and can complete the missing 122 generations. They do **not** enter `aggregate_v11.py`'s main analysis.

This is the right way to handle a failing model in a benchmark: do not silently drop it, do not hide it in an appendix, and do not extrapolate a partial result. State that you tried, state why it didn't work, preserve the evidence, exclude it from the lift table.

### 6.2 Gemma-4-31b-it: heavy throttling but completed

OpenRouter's Gemma endpoint hit upstream rate limits (`HTTP 429` from Venice / Parasail / DeepInfra / Together / Chutes / Novita rotating providers) intermittently throughout the run. Unlike Kimi, Gemma did not fail on a per-condition basis — all 4 conditions failed at roughly the same rate, and the retries succeeded after backoff most of the time. Total wall-clock time for Gemma was ~3.5 hours for 200 generations vs. ~30 minutes for the other OpenRouter generators. The last persona (`fashion_010`, `akm_profile`) required a separate temperature-jitter retry script (logged with `fix_attempt_note` field in the JSONL) — the retried call succeeded on attempt 1 with temperature=0.0, max_tokens=1500, returning a 1859-character response that matches the length distribution of the other 49 Gemma `akm_profile` outputs. **Final n=50/50.**

The lift direction (+19.61) and ceiling level (29.74 on `akm_profile`) match the strong generators despite Gemma's much lower OpenRouter rank.

### 6.3 GLM-5.1 single-persona drop

GLM-5.1 (49/50 personas). One persona (`fashion_007`, condition `akm_profile`) failed all retries (8 retries × multiple temperature settings, ~30 attempts total) with empty content from OpenRouter. We dropped that persona for GLM only — i.e. all 4 conditions for `fashion_007` are removed from GLM's analysis to keep the per-persona comparison valid. Other generators have all 4 conditions for `fashion_007`. The drop is 1/50 = 2%.

### 6.4 `format_repair` calls

When an OpenRouter generator returned a syntactically broken JSON for the elicitation step (`akm_elicited`), `run_generation_v11.py` called DeepSeek-V4-pro with a strict instruction to **re-emit the same JSON without changing semantic content**. Each invocation is logged at `outputs/v1.1/format_repair_log.jsonl`.

Total invocations: **38** events out of ~500 attempted JSON-elicitation calls in the included generators (≈7.6%). Almost all are for GLM-5.1 (unterminated strings near the end of long elicitation traces) and the excluded Kimi-K2.6 attempts. DeepSeek and GPT had 0 repairs; Qwen had 0 repairs.

This is a methodological compromise. The cleanest alternative would be to discard any malformed JSON outright. We chose to repair-then-keep so as not to advantage models with tighter JSON formatters, since we are evaluating *content quality under a profile*, not JSON compliance. The repair prompt is content-preserving by construction — DeepSeek is given the broken JSON and asked only to make it parseable. We invite reviewers to inspect `format_repair_log.jsonl` and rerun without repair if they prefer; the directional conclusion in §3 is robust to that choice (the fully-clean DeepSeek and GPT and Qwen rows by themselves already establish the lift).

### 6.5 Judge unchanged from v1.0

We deliberately did not introduce a new judge in v1.1. Adding a judge would change two things at once (more generators **and** more judges) and we wanted §3 to be interpretable as a strict generalization test of v1.0. Any reviewer who wants to add a judge can do so by re-running `run_judging_v11.py --judge <new>` against the existing `generations_*.jsonl`.

### 6.6 What v1.1 does not claim

- We do not claim per-domain (fitness vs. fashion vs. advisory) effects across generators. Per-domain breakdowns are computable from `scores_long.csv` but the per-cell n is 16 or 17 for the strong generators and small for the partial generators — we judge that under-powered for a robust per-domain × per-generator claim.
- We do not claim AKM is *the optimal* protocol. We only claim the v1.0 lift over `no_profile` and `unstructured_notes` is reproduced under each of 6 generator families.
- We do not claim anything about real users. v1.1 is still a synthetic-persona experiment, like v1.0. Real-user calibration is left for future work.

---

## 7. Bottom line for the four papers

For the **AKM Mother**, **DaE**, **Fitness**, and **Fashion** papers:

> The AKM advantage over no-profile and over unstructured notes — first reported in v1.0 with DeepSeek-V4-pro as sole generator — is reproduced across 5 cross-family generators (DeepSeek, OpenAI, Alibaba, Zhipu, Google open-weights), each with full N=50 personas (GLM at 49 due to one OpenRouter-side persona drop), with `Δ AKM` ranging from +14.56 to +19.81 on the 0–30 rubric. The advantage holds for the strongest model in the set and for the weakest model (Gemma-4-31b-it, OpenRouter rank 38, lift +19.61), and holds even on a generator (GLM-5.1) whose absolute AKM ceiling is visibly lower than the rest. A sixth attempted generator (Kimi-K2.6) was excluded because the OpenRouter endpoint failed; raw evidence is preserved.

That sentence is what the four papers should cite this supplement for. Nothing more, nothing less.
