<!--
文件：manuscript.md
核心功能：作为 Fitness 分支 SSRN 风格论文草稿，说明 AKM 在健身规划场景中的研究问题、方法结构、证据形式与边界。
输入：健身工作区一手证据、外部训练与依从性文献、外部模型行为测试结果。
输出：供人工审阅后再转 LaTeX 的英文 markdown 论文稿。
-->

# Profile-First Fitness Planning Under Real Constraints: An AKM Branch Case

## Abstract

This paper examines how `Active Knowledge Modeling (AKM)` operates in fitness planning under real-world constraints. Instead of generating a workout plan directly, the system first models the user's training goals, body limitations, equipment context, time budget, recovery state, and execution risks, and only then produces a day-level or stage-level training decision. The paper is framed as an **n=1 longitudinal self-use system case** rather than a broad effectiveness claim. Its contribution is methodological: it shows how AKM can transform fitness planning from generic programming into profile-first, state-dependent decision making under real constraints. The argument is supported by a local evidence base composed of rules, metrics, logs, and monthly records, together with external literature on training-load monitoring, autoregulation, and adherence [1]-[5].

## 1. Introduction

A recurring weakness of AI fitness advice is that it speaks as if the decision environment were simple. Generic plans often assume stable goals, healthy movement capacity, reliable recovery, and interchangeable equipment. In real use, these assumptions break quickly. A user may be managing injury constraints, uneven recovery, changing equipment access, and conflicting goals at the same time. Under these conditions, readable advice is easy to produce, but executable advice is much harder.

This paper starts from a simple claim: in constrained training environments, the main problem is often upstream modeling rather than downstream workout generation. Training-load research and monitoring literature already show that prescription quality depends on the interaction between workload, readiness, and context rather than on a fixed template alone [1], [3]. Research on autoregulation further supports the idea that training variables should respond to individual state rather than remain rigidly preassigned [2]. If that is true, then a fitness-planning agent should not begin with a plan. It should begin with a model of what can actually be advanced under current conditions.

## 2. Research Position

This paper does not claim that AKM is a medically validated coaching system or that its outputs have been benchmarked across a broad population. The paper makes a narrower claim. It presents a branch-level implementation case in which AKM is used to organize fitness planning as a constrained decision workflow.

The evidence model is `n=1 longitudinal self-use`. That choice matters. The relevant question is not whether a broad average user improves under a generic protocol. The relevant question is whether profile-first planning produces more realistic, lower-friction decisions in a high-constraint environment than ordinary prompt-first advice.

## 3. Problem Definition

Most generic fitness prompting degrades in predictable ways when the user context is underspecified:

- injury or pain signals are flattened into normal programming assumptions
- equipment limitations are treated as details rather than determinants
- time budgets are treated as adjustable even when they are real hard constraints
- recovery state is overwritten by split logic or template logic
- the system behaves as if confidence were available even when key state variables are missing

These failure patterns are consistent with a broader observation from adherence and intervention research: sustained exercise behavior depends not only on the nominal quality of the plan, but on whether the plan is matched to the user’s condition, context, and ability to comply over time [4], [5].

## 4. Method: AKM in the Fitness Scene

In the fitness scene, AKM does not model abstract identity for its own sake. It models training feasibility. The relevant upstream state includes:

- ranked goals
- injury history and movement restrictions
- available equipment
- weekly frequency
- session time budget
- recovery state
- execution risk and adherence risk

The branch is implemented as a three-layer workflow.

### 4.1 Elicitation

The system first clarifies the operator before it recommends anything. It asks for or retrieves the goal hierarchy, current body limitations, equipment reality, weekly rhythm, and recovery-relevant information. This step serves the same logic that motivates individualized training and autoregulation in the literature: prescription should respond to current capacity rather than ignore it [2], [3].

### 4.2 Structured Record

The elicited information is converted into persistent upstream state. In this branch, that state is maintained through structured records such as metrics snapshots, equipment records, append-only logs, and monthly stage summaries. The role of this layer is the same role that training-load monitoring plays in sport settings: it preserves the context required for a decision to remain grounded over time [1], [3].

### 4.3 Execution Decision

Only after the profile and recent state are available does the system produce a training decision. The output contract is not just a plan. It includes:

- `StateJudgment`
- `PrimaryDecision`
- `DecisionConfidence`
- `Plan`
- `RiskNotes`
- `NonNegotiables`
- `MissingInputs`

This is important because missing information is treated as part of the decision rather than something to hide behind fluent language.

## 5. Why This Is Not a Generic Workout Prompt

A stronger prompt is still just a prompt if it lacks stable upstream structure. The defining property of this branch is not tone, style, or motivational language. The defining property is workflow position. The decision layer depends on explicit state and can degrade its confidence when that state is incomplete.

This is where the branch connects most clearly with the literature on autoregulation and monitoring. Autoregulation methods adjust training according to current feedback rather than requiring blind adherence to a fixed plan [2]. Training-load monitoring frameworks also treat context and adjustment as central rather than incidental [1], [3]. The AKM branch extends the same logic into agent behavior: model first, decide second.

## 6. Evidence Base

The local evidence base for this paper is listed in [local-evidence.md](./local-evidence.md). At a high level, it includes:

- hard system rules
- structured body metrics
- equipment context records
- day-level decision files
- append-only execution logs
- monthly retrospective records

This does not create broad causal proof. It does provide a traceable basis for a longitudinal systems case. In addition, external-model testing was used as a behavioral boundary check. The question was not whether another model would outperform the original setup, but whether the workflow still enforced AKM discipline under another model.

The critical behaviors were:

- elicitation before prescription
- explicit exposure of missing inputs
- reduced confidence under insufficient recovery or sequencing information
- refusal to default to standard split logic when state evidence was incomplete

## 7. Discussion

The branch suggests that the main value of AKM in fitness is not informational richness for its own sake. Its value is constraint preservation. It reduces the tendency of an agent to speak as if all fitness decisions were generic programming problems.

This matters practically because real users do not live inside stable training abstractions. They live inside changing schedules, soreness, equipment limitations, old injuries, and inconsistent recovery. A planning system that ignores these variables may look sophisticated but will generate friction downstream. A planning system that models them upstream may produce narrower answers, but those answers are more likely to remain usable.

## 8. Boundaries

This paper is not a medical paper. The branch does not replace physicians, rehabilitation specialists, or in-person coaching. It also does not show broad-sample effectiveness. The correct claim is narrower: AKM can be implemented as a profile-first planning system in a high-constraint training environment.

When critical variables are missing, the correct behavior is constrained output or refusal, not complete-looking programming.

## 9. Conclusion

The fitness branch matters because it shows how AKM can convert workout generation into a decision process grounded in user state, constraints, and evolving evidence. The contribution is methodological. It demonstrates that, in a constrained planning scene, better upstream modeling can be more important than better downstream phrasing.

## References

[1] Foster, C., Rodriguez-Marroyo, J. A., & de Koning, J. J. (2017). *Monitoring Training Loads: The Past, the Present, and the Future*. International Journal of Sports Physiology and Performance, 12(S2), S2-2-S2-8. DOI: 10.1123/ijspp.2016-0388.

[2] Shattock, K., & Tee, J. C. (2022). *Autoregulation in Resistance Training: A Comparison of Subjective Versus Objective Methods*. Journal of Strength and Conditioning Research, 36(3), 641-648. DOI: 10.1519/JSC.0000000000003530.

[3] Haddad, M., Stylianides, G., Djaoui, L., Dellal, A., & Chamari, K. (2017). *Session-RPE Method for Training Load Monitoring: Validity, Ecological Usefulness, and Influencing Factors*. Frontiers in Neuroscience, 11, 612. DOI: 10.3389/fnins.2017.00612.

[4] Fuente-Vidal, A., Guerra-Balic, M., Roda-Noguera, O., Jerez-Roig, J., & Montane, J. (2022). *Adherence to eHealth-Delivered Exercise in Adults with no Specific Health Conditions: A Scoping Review on a Conceptual Challenge*. International Journal of Environmental Research and Public Health, 19(16), 10214. DOI: 10.3390/ijerph191610214.

[5] Lee, J., Kim, D. I., & Jeon, J. Y. (2025). *Personalized exercise programs improve health-related quality of life in individuals with spinal cord injuries: an exploratory randomized clinical trial*. Physical Activity and Nutrition, 29(2), 11-18. DOI: 10.20463/pan.2025.0009.