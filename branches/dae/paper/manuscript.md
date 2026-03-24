<!--
文件：manuscript.md
核心功能：作为 DaE 分支论文草稿，说明 AKM 在 persona 与顾问协作场景中的具体实现。
输入：AKM 母定义、DaE 既有研究口径、DaE 的 profile-first 工作流。
输出：供后续整理为正式子论文的分支稿件。
-->

# DaE as the First AKM Implementation

## Abstract

This paper presents Dialogue-as-Elicitation (DaE) as the first reference implementation of `Active Knowledge Modeling (AKM)` in persona-aware advisory and collaboration workflows. Rather than providing downstream advice directly, DaE first constructs a reusable user model through structured elicitation, outputs a `PersonaProfile`, and then uses that upstream asset to support planning, writing, research, and advisory tasks. The contribution of DaE is methodological: it shows how a profile-first workflow can function as reusable upstream infrastructure for downstream collaboration quality.

## Core Logic

1. elicit before advising
2. validate before accepting self-description
3. construct an upstream profile before downstream execution begins