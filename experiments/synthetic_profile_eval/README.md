<!--
文件：README.md
核心功能：说明 AKM-Benchmark-Toolkit v0.2 的实验目标、输入输出、运行方式、环境变量配置、当前边界与 akm_elicited 条件。
输入：profiles.jsonl、prompts/*.md、run_generation.py、run_judging.py、aggregate_results.py、DEEPSEEK_API_KEY 环境变量。
输出：outputs/generations.jsonl、outputs/judgments.jsonl、results/summary.json、results/summary.md。
-->

# AKM-Benchmark-Toolkit v0.2

This toolkit reproduces a synthetic profile evaluation for Active Knowledge Modeling (AKM).

It compares downstream AI advice under four conditions:

1. no user profile,
2. unstructured natural-language user notes,
3. structured AKM-style user profiles,
4. AKM-elicited profiles generated through a simulated pre-task elicitation chain.

The current v0.2 result is still a proof-of-concept benchmark. It is suitable for reproducing the published demo, inspecting raw outputs, and checking whether the elicitation chain narrows the gap between unstructured notes and ideal structured profiles.

It does not test real-user satisfaction. It uses synthetic personas, DeepSeek generation, and DeepSeek LLM-as-judge evaluation.

## Conditions

- `no_profile`: the model receives only the task.
- `unstructured_notes`: the model receives natural-language user notes.
- `akm_profile`: the model receives a structured AKM profile.
- `akm_elicited`: the model receives a structured AKM profile generated from a simulated AKM elicitation trace.

## Main Question

Does a structured AKM profile improve constraint adherence, risk control, specificity, actionability, personal fit, and trade-off awareness? Does the `akm_elicited` chain preserve enough of that advantage to justify larger-scale paper evaluation?

## Current Result

The included 10-profile run produced this aggregate pattern:

| Condition | Total | Constraint | Risk | Specificity | Actionability | Fit | Trade-off |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `no_profile` | 12.6 | 1.7 | 2.7 | 2.6 | 2.7 | 1.7 | 1.2 |
| `unstructured_notes` | 22.4 | 4.1 | 4.3 | 3.8 | 4.1 | 3.8 | 2.3 |
| `akm_profile` | 29.1 | 4.9 | 4.9 | 4.9 | 4.9 | 4.9 | 4.6 |
| `akm_elicited` | 29.7 | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 4.7 |

Best-answer counts:

- `no_profile`: 0
- `unstructured_notes`: 0
- `akm_profile`: 4
- `akm_elicited`: 6

Do not treat a high score as a real-world "perfect proof". The useful signal is narrower: structured and elicited profiles can be compared against unstructured notes in a controlled synthetic setting.

## Run

```powershell
python experiments\synthetic_profile_eval\run_generation.py
python experiments\synthetic_profile_eval\run_judging.py
python experiments\synthetic_profile_eval\aggregate_results.py
```

The scripts read the DeepSeek API key from the `DEEPSEEK_API_KEY` environment variable. The key is not written to output files.

## Output

- `outputs/generations.jsonl`: raw generated answers under all four conditions, including elicitation traces for `akm_elicited`.
- `outputs/judgments.jsonl`: blind judge scores with randomized answer labels.
- `results/summary.json`: aggregated metrics.
- `results/summary.md`: human-readable summary for review and article revision.

## What v0.2 Does Not Prove

The `akm_profile` condition injects a pre-written structured profile. The `akm_elicited` condition adds a simulated elicitation chain, but it still uses synthetic personas and LLM-simulated user answers. Therefore v0.2 mainly tests these claims:

```text
Structured user context improves downstream constraint adherence compared with no profile or unstructured notes.
AKM-style elicitation can generate a usable profile in this synthetic setting.
```

It does not yet prove this stronger real-world claim:

```text
Real users will provide enough information through AKM elicitation to outperform other profile-generation methods in production.
```

## akm_elicited Flow

```text
synthetic persona
  -> simulated user answers AKM elicitation questions
  -> profile extraction
  -> downstream task generation
  -> downstream task generation
  -> blind LLM-as-judge evaluation
```

Implemented files:

```text
prompts/elicit_akm_profile.md
outputs/generations.jsonl
outputs/judgments.jsonl
```

Run `akm_elicited` on the existing 10 profiles before expanding to 30 or more profiles.

## Boundary

This is a synthetic evaluation. It supports a narrow claim: under controlled synthetic profiles, structured pre-task profile elicitation can improve observable constraint adherence and profile fit. It does not claim clinical efficacy, behavioral change, real-user satisfaction, or universal personalization performance.
