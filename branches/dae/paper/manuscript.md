<!--
文件：manuscript.md
核心功能：作为 DaE 分支论文草稿，说明 AKM 在 persona 与顾问协作场景中的具体实现。
输入：AKM 母定义、DaE 既有研究口径、DaE 的 profile-first 工作流。
输出：供后续整理为正式子论文的分支稿件。
-->

# DaE as the First AKM Implementation

## Abstract

This paper presents Dialogue-as-Elicitation (DaE) as the first reference implementation of `Active Knowledge Modeling (AKM)` in persona-aware advisory and collaboration workflows. Rather than providing downstream advice directly, DaE first constructs a reusable user model through structured elicitation, outputs a `PersonaProfile`, and then uses that upstream asset to support planning, writing, research, and advisory tasks. The contribution of DaE is methodological: it shows how a profile-first workflow can function as reusable upstream infrastructure for downstream collaboration quality.

## 1. Problem

Many advisory and collaboration workflows fail at an upstream layer. The issue is not only model capability. The issue is that downstream systems often begin acting before they have a structured model of the user they are working for.

Typical failure patterns include:

- treating vague self-description as sufficient context
- rebuilding user context from scratch in every new session
- confusing personality labels with operational decision signals
- optimizing downstream output without stabilizing upstream user modeling

In these conditions, even strong downstream models tend to produce generic, weakly aligned work.

## 2. AKM in the DaE Scene

Within the AKM framework, DaE models the user as an upstream collaboration asset rather than as a loose conversational impression. The goal is to convert elicited user context into a reusable profile that can support multiple downstream tasks.

The central object is `PersonaProfile`, which may include:

- background
- capabilities
- resources
- constraints
- drives
- goals
- decision style
- weaknesses
- tensions
- challenges
- lessons
- alignment checks

This profile is not treated as biography for its own sake. It is treated as an operational context layer.

## 3. Method Structure

DaE follows a profile-first workflow.

### 3.1 Elicitation

The system uses structured dialogue to extract user information that is often missing from ordinary prompting. The emphasis is on decision-relevant context rather than on decorative self-description.

### 3.2 Structuring

The elicited material is normalized into a `PersonaProfile`. This step turns raw dialogue into a reusable upstream asset.

### 3.3 Injection

The resulting profile is injected into downstream workflows so that planning, analysis, or advisory work starts from a richer model of the operator.

## 4. Why DaE Is Not Just a Prompt Pattern

DaE is not defined by wording style. Its distinguishing property is workflow position.

It does not merely ask better questions in isolation. It creates an upstream artifact that can be reused across tasks and across time. That is the difference between a better prompt and a reusable AKM implementation.

A one-off prompt disappears after the session. A `PersonaProfile` persists as a reusable context asset.

## 5. Evidence Form

The DaE line is supported by several kinds of evidence:

- a complete profile-first workflow
- a reusable structured output format
- public release assets for the skill implementation
- a research line explaining the method and its rationale

The claim here is methodological, not universal. The evidence supports DaE as a coherent implementation pattern for persona-aware collaboration.

## 6. Boundaries

DaE does not replace task-specific expertise. It does not guarantee that one elicitation session is permanently sufficient. It also does not treat self-description as reliable fact without structure or internal consistency checks.

The system improves upstream modeling quality. It does not eliminate the need for downstream judgment.

## 7. Conclusion

DaE matters because it demonstrates the first complete AKM implementation in a concrete, reusable scene. It shows that user modeling can operate as upstream infrastructure for collaboration quality rather than as optional prompt decoration.