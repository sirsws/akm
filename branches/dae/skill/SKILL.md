---
name: "dae-persona-context-injector"
description: "First AKM reference implementation for persona-aware advisory and collaboration workflows. Builds a reusable PersonaProfile before downstream work begins."
---

<!--
文件：SKILL.md
核心功能：作为 DaE skill 的英文正式说明页，定义其定位、核心资产、适用场景、双语规则与边界。
输入：DaE 分支方法结构、PersonaProfile 字段设计与 AKM 母港关系。
输出：供 GitHub、技能市场或代理工具直接引用的英文 skill 文档。
-->

# DaE Skill

<p align="center">
  <a href="./SKILL.md">English</a> | <a href="./SKILL.zh-CN.md">简体中文</a>
</p>

**Profile first. Then collaborate.**

DaE is the operational skill package for AKM in persona-aware advisory and collaboration workflows.
Its purpose is to construct a reusable `PersonaProfile` before downstream planning, writing, advising, coding, or multi-agent collaboration begins.

## Position

- parent concept: `AKM`
- branch: `DaE`
- role: `reference implementation`

## Core Asset

The central upstream asset is `PersonaProfile`.
Expected profile fields include:

- `Background`
- `Capabilities`
- `Resources`
- `Constraints`
- `Goals`
- `DecisionStyle`
- `Weaknesses`
- `Challenges`
- `Lessons`
- `AlignmentCheck`

## Language Rule

Public landing pages are English-first with a Chinese toggle.
Field keys stay in English for routing and reuse stability.
Prompting and operational use may run in either English or Chinese.

## Best-Fit Scenarios

Use this skill when downstream work keeps failing because the system lacks a stable model of the operator it is supposed to serve.

## Boundaries

- does not replace domain-specific expertise
- does not guarantee permanent profile validity after one elicitation pass
- does not treat self-description as verified fact without structure or cross-checking
