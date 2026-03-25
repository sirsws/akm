<!--
文件：manuscript.md
核心功能：作为 Fitness 分支论文的英文 markdown 稿，说明 AKM 如何在真实约束下把健身规划重写成画像优先的决策系统，并明确其对主流平台上下文槽位的上游方法论补位。
输入：健身工作区本地设计记录、训练日志、结构化状态记录与外部训练负荷/自适应训练文献。
输出：供人工审阅后再转 LaTeX 的英文论文草稿。
-->

# Profile-First Fitness Planning Under Real Constraints: An AKM Branch Paper

## Abstract

This paper examines how `Active Knowledge Modeling (AKM)` operates in fitness planning under real constraints. Instead of generating a workout plan first, the system models goals, body limitations, equipment reality, time budget, recovery uncertainty, and execution risk before making a training decision. The contribution is methodological. The branch shows how AKM converts fitness prompting into profile-first decision design.

## 1. Introduction

Platforms such as OpenClaw, ChatGPT, and Gemini already expose user-context or system-prompt fields, but they rarely provide a rigorous method for constructing the state that should populate them. Fitness advice makes the gap especially visible. Generic plans often assume stable goals, healthy movement capacity, reliable recovery, and interchangeable equipment. Real users do not live inside those assumptions.

The problem is therefore upstream. If training decisions depend on body condition, recovery state, time budget, and equipment access, then the system should not begin with a plan. It should begin with a model of what can actually be advanced under the current constraints.

## 2. Problem Definition

Generic fitness prompting degrades in predictable ways when upstream context is weak:

- injury or pain signals are flattened into normal programming assumptions
- equipment limitations are treated as details rather than determinants
- time budgets are treated as flexible when they are actually hard constraints
- recovery uncertainty is overwritten by split logic or template logic
- the system behaves as if confidence already exists even when key state variables are missing

These failure modes match a broader lesson from training-load monitoring, autoregulation, and adherence research: training quality depends on the interaction between workload, readiness, and context rather than on a fixed template alone [1]-[4].

## 3. Method: AKM in the Fitness Scene

In the fitness scene, AKM does not model abstract identity for its own sake. It models training feasibility.
The relevant upstream state includes:

- ranked goals
- injury history and movement restrictions
- available equipment
- weekly frequency
- session time budget
- recovery state
- execution risk and adherence risk

The branch is implemented as a three-layer workflow.

### 3.1 Elicitation

The system first asks what kind of training decision is even valid. It clarifies goal hierarchy, body limitations, equipment reality, weekly rhythm, and recovery-relevant information before recommending anything.

### 3.2 Structured Record

The elicited information is converted into persistent upstream state. In this branch, the state is maintained through structured records such as metrics snapshots, equipment records, append-only logs, and monthly summaries.

### 3.3 Execution Decision

Only after profile and recent state are available does the system produce a training decision. The output contract includes:

- `StateJudgment`
- `PrimaryDecision`
- `DecisionConfidence`
- `Plan`
- `RiskNotes`
- `NonNegotiables`
- `MissingInputs`

Missing information is treated as part of the decision rather than something to hide behind fluent language.

## 4. Design Record

The local design record for this branch is listed in [local-evidence.md](./local-evidence.md). It includes:

- hard system rules
- structured body metrics
- equipment context records
- day-level decision files
- append-only execution logs
- monthly retrospective records

These records are not presented as broad proof of effectiveness. They are used to make workflow behavior visible.
A representative decision trace is shown below.

```json
{
  "StateJudgment": "Recovery state partially unclear; lower-back risk remains a live constraint.",
  "PrimaryDecision": "Do not assign heavy compound lifting today. Use a lower-risk session or pause pending clarification.",
  "DecisionConfidence": "Low",
  "Plan": [
    "Confirm current lumbar discomfort level and sleep quality before loading decisions.",
    "If discomfort is elevated, switch to mobility, light accessories, and walking.",
    "If discomfort is low and recovery is acceptable, resume with conservative volume only."
  ],
  "RiskNotes": [
    "Generic split logic is not sufficient under unresolved recovery and injury uncertainty.",
    "The main failure mode is acting as if readiness were already known."
  ],
  "NonNegotiables": [
    "No heavy axial loading until state is clarified.",
    "Do not infer readiness from schedule alone."
  ],
  "MissingInputs": [
    "Current lumbar discomfort score (1-10)",
    "Previous session load and residual soreness",
    "Sleep and recovery status over the last 24 hours"
  ]
}
```

This trace illustrates workflow behavior under uncertainty. It is not a treatment outcome claim.

## 5. Discussion

The main value of AKM in fitness is constraint preservation. It reduces the tendency of an agent to behave as if all fitness decisions were generic programming problems.

That matters because real users live inside changing schedules, soreness, equipment limits, old injuries, and inconsistent recovery. A planning system that ignores these variables may look confident, but it creates downstream friction. A planning system that models them upstream is narrower, but more usable.

## 6. Boundaries

This paper is not a medical paper.
The branch does not replace physicians, rehabilitation specialists, or in-person coaching.
Its claim is narrower: AKM can be implemented as a profile-first planning system in a high-constraint training environment.

## 7. Conclusion

The fitness branch matters because it shows how AKM converts workout generation into a decision process grounded in user state, constraints, and explicit uncertainty. The contribution is methodological: better upstream modeling can matter more than better downstream phrasing.

## References

[1] Foster, C., Rodriguez-Marroyo, J. A., & de Koning, J. J. (2017). *Monitoring Training Loads: The Past, the Present, and the Future*. International Journal of Sports Physiology and Performance, 12(S2), S2-2-S2-8. DOI: 10.1123/ijspp.2016-0388.

[2] Shattock, K., & Tee, J. C. (2022). *Autoregulation in Resistance Training: A Comparison of Subjective Versus Objective Methods*. Journal of Strength and Conditioning Research, 36(3), 641-648. DOI: 10.1519/JSC.0000000000003530.

[3] Haddad, M., Stylianides, G., Djaoui, L., Dellal, A., & Chamari, K. (2017). *Session-RPE Method for Training Load Monitoring: Validity, Ecological Usefulness, and Influencing Factors*. Frontiers in Neuroscience, 11, 612. DOI: 10.3389/fnins.2017.00612.

[4] Fuente-Vidal, A., Guerra-Balic, M., Roda-Noguera, O., Jerez-Roig, J., & Montane, J. (2022). *Adherence to eHealth-Delivered Exercise in Adults with no Specific Health Conditions: A Scoping Review on a Conceptual Challenge*. International Journal of Environmental Research and Public Health, 19(16), 10214. DOI: 10.3390/ijerph191610214.


