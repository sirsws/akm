<!--
文件：manuscript.md
核心功能：作为 Fashion 分支论文稿，说明 AKM 在穿搭与衣橱规划场景中的方法结构、证据形式与边界。
输入：穿搭智能体提示词、场景与衣橱建模逻辑、约束条件与外部行为测试结论。
输出：供后续整理为正式子论文的英文 markdown 稿件。
-->

# Asset-Aware Wardrobe Planning and Outfit Decisions: An AKM Branch Case

## Abstract

This paper examines how `Active Knowledge Modeling (AKM)` operates in wardrobe planning and outfit decision workflows. Instead of producing styling output immediately, the system first models body context, scene requirements, wardrobe assets, functional constraints, and style preferences, and only then produces outfit recommendations, gap analysis, and purchase priorities. The paper is framed as a **long-term single-user system design and method case** rather than a broad validation claim. Its contribution is methodological: it shows how AKM converts styling from generic taste language into asset-aware and scene-constrained decision-making.

## 1. Problem

Most styling systems fail because they ignore the structure of the operator. They do not know what the user owns, which scenes actually matter, what body context must be handled, or which functional constraints are non-negotiable.

When these upstream variables are absent, typical output degrades into:

- vague taste language
- scene-insensitive outfit suggestions
- recommendations that assume unlimited wardrobe replacement
- purchase advice detached from current assets

The issue is not that the system cannot describe style. The issue is that it lacks the upstream model required for real decisions.

## 2. AKM in the Fashion Scene

In this scene, AKM models a wardrobe decision structure rather than a mood or identity label. The relevant upstream structure includes:

- scene hierarchy
- body context
- style preferences and anti-patterns
- wardrobe assets already owned
- functional constraints
- purchase priorities

This shifts the task from generating styling commentary to making constrained decisions.

## 3. Method Structure

The branch is organized into three layers.

### 3.1 Elicitation

The system first clarifies scenes, body context, existing assets, style preferences, and hard constraints.

### 3.2 Structured Record

The elicited material is stored as a reusable profile covering the operator, the wardrobe, and current gaps.

### 3.3 Execution Decision

Only after the profile is available does the system produce outfit recommendations, gap analysis, and purchase priorities.

## 4. Why This Is Not a Generic Styling Prompt

A styling persona prompt can imitate taste language without producing constrained decisions. This branch differs because wardrobe assets and scene requirements are treated as upstream inputs rather than optional flavor.

The system is designed to expose what it does not know. If wardrobe or scene detail is incomplete, it should output missing inputs rather than pretending to know the user's closet.

## 5. Evidence Form

This branch is best interpreted as a long-term single-user system design and method case. The evidence base includes:

- stable scene logic
- explicit body and style constraints
- structured wardrobe assets
- repeatable output types
- external model behavior tests

This is not presented as image-recognition validation or large-sample aesthetic benchmarking. The contribution is methodological.

## 6. External Behavior Testing

External-model testing was used to check whether the method preserved constraint-aware reasoning under another model. The critical question was whether the workflow still avoided drifting into generic taste talk.

The tested behaviors included:

- eliciting scenes and wardrobe constraints before recommending outfits
- making single-scene or cross-scene decisions from explicit assets
- surfacing `MissingInputs` when wardrobe or context detail remained incomplete

These observations support the claim that AKM improves styling quality by strengthening upstream modeling rather than by increasing surface-level stylistic fluency.

## 7. Boundaries

This system does not replace a stylist, an image-recognition pipeline, or a virtual try-on product. It depends on user-provided information about wardrobe, body context, and scene requirements.

When those inputs are incomplete, the correct behavior is constrained output and gap exposure rather than artificial certainty.

## 8. Conclusion

The fashion branch matters because it shows how AKM can turn styling from generic commentary into asset-aware and scene-constrained decision-making. Its contribution is not that AI can discuss clothing. Its contribution is that upstream modeling changes what kind of styling decision becomes possible.