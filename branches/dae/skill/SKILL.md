---
name: "dae-persona-context-injector"
description: "First AKM reference implementation for persona-aware advisory and collaboration workflows. Builds a reusable PersonaProfile before downstream work begins."
---

<!--
文件：SKILL.md
核心功能：作为 DaE skill 的正式项目说明，定义其定位、输入输出、核心资产与使用边界。
输入：DaE 分支方法结构、PersonaProfile 字段定义与 AKM 母港关系。
输出：供 GitHub、技能市场或代理工具直接引用的正式 skill 文档。
-->

# DaE Skill

**Profile first. Then collaborate.**

DaE is the operational skill package for AKM in persona-aware advisory and collaboration workflows.
Its purpose is to construct a reusable `PersonaProfile` before downstream planning, writing, advising, or multi-agent collaboration begins.

## Position

- parent concept: `AKM`
- branch: `DaE`
- role: `reference implementation`

## Core Asset

The central upstream asset is `PersonaProfile`.
It captures structured user context for reuse across downstream tasks.

Expected profile fields include:

- `Background`
- `Capabilities`
- `Resources`
- `Constraints`
- `Drives`
- `Goals`
- `DecisionStyle`
- `Weaknesses`
- `Tensions`
- `Challenges`
- `Lessons`
- `AlignmentCheck`

## Best-Fit Scenarios

Use this skill when the quality of downstream work depends on a stable, reusable profile layer.
Typical cases include advisory collaboration, long-running projects, and multi-agent workflows that would otherwise rebuild user context from scratch.

## Boundaries

- does not replace domain-specific expertise
- does not guarantee permanent profile validity after one elicitation pass
- does not treat self-description as verified fact without structure or cross-checking