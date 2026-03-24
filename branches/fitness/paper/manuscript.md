<!--
文件：manuscript.md
核心功能：作为 Fitness 分支论文稿，说明 AKM 在健身与体能规划场景中的方法结构、证据形式与边界。
输入：健身智能体的规则、训练日志、体征记录、约束条件与外部行为测试结论。
输出：供后续整理为正式子论文的英文 markdown 稿件。
-->

# Profile-First Fitness Planning Under Real Constraints: An AKM Branch Case

## Abstract

This paper examines how `Active Knowledge Modeling (AKM)` operates in fitness planning under real-world constraints. Instead of generating a workout plan directly, the system first models the user's training goals, body limitations, equipment context, time budget, recovery state, and execution risks, and only then produces a stage-level or day-level training decision. The paper is framed as an **n=1 longitudinal self-use system case** rather than a broad effectiveness claim. Its contribution is methodological: it shows how AKM converts a high-feedback, high-constraint training environment from generalized advice into state-dependent decision-making.

## 1. Problem

Most fitness systems assume too much. They often assume a clear single goal, stable equipment access, normal recovery, and a body that can tolerate standard programming. These assumptions fail quickly in real training environments.

When they fail, output quality degrades in predictable ways:

- plans ignore actual physical limitations
- exercise selection mismatches available equipment
- time budgets are treated as soft rather than real constraints
- recovery uncertainty is overwritten by generic programming logic

The result is often readable but weakly executable training advice.

## 2. AKM in the Fitness Scene

In this scene, AKM models training feasibility rather than abstract identity. The relevant upstream structure includes:

- goal hierarchy
- body constraints
- equipment context
- weekly frequency and session time budget
- recovery state
- execution risks

This shifts the core question. The system does not begin with "what workout should I do?" It begins with "what can be responsibly advanced under current constraints?"

## 3. Method Structure

The system is organized into three layers.

### 3.1 Elicitation

The system first clarifies the operator:

- ranked goals
- injury history and movement restrictions
- equipment conditions
- time budget
- recovery and adherence risks

### 3.2 Structured Record

The elicited information is maintained as reusable upstream state, including metrics, baselines, logs, and stage priorities.

### 3.3 Execution Decision

Only after the profile and recent state are available does the system produce a training decision. The output includes not only a plan, but also confidence, risk boundaries, and missing inputs.

## 4. Why This Is Not a Generic Workout Prompt

A stronger coaching prompt is still just a prompt if it lacks persistent upstream structure. The defining feature here is not tone. The defining feature is that the decision layer depends on an explicit profile and recent state evidence.

This means the system can refuse to behave as if it knows more than it knows. Missing information is part of the decision process rather than something hidden behind generic confidence.

## 5. Evidence Form

This branch is documented as an `n=1` longitudinal self-use system. The evidence base includes:

- append-only training logs
- body metrics snapshots
- equipment context records
- hard constraint rules
- external model behavior tests

This evidence does not support broad outcome claims. It does support the methodological claim that AKM can be implemented as a profile-first planning system in a high-constraint training scene.

## 6. External Behavior Testing

External-model testing was used here as a method-boundary check, not as outcome validation. The question was whether the workflow preserved AKM discipline under another model.

The most important behaviors were:

- elicitation before prescription
- explicit exposure of missing inputs
- reduced confidence when recovery and ordering information are insufficient
- refusal to hide uncertainty behind standard split logic

These tests support the view that AKM improves not by making models "guess better," but by making them guess less.

## 7. Boundaries

This paper is not a medical paper. The system does not replace physicians, rehabilitation specialists, or in-person coaching. Its competence depends on real user-provided constraints and state information.

When critical variables are missing, the correct behavior is constrained output or refusal, not complete-looking programming.

## 8. Conclusion

The fitness branch matters because it shows how AKM can transform training from generalized advice into constrained decision-making. Its main contribution is not market relevance. Its main contribution is methodological coherence under real-world constraints.