---
name: "akm-fitness-planner"
description: "AKM implementation for training decision workflows. Models goals, body limits, equipment context, time budget, and recovery before outputting a workout decision."
---

<!--
文件：SKILL.md
核心功能：作为 AKM Fitness skill 的正式项目说明，定义其定位、输入要求、工作流、输出契约与使用边界。
输入：Fitness 分支方法结构、提示词文件、记录模板与测试结论。
输出：供 GitHub、技能市场或代理工具直接引用的正式 skill 文档。
-->

# AKM Fitness Skill

**No profile, no serious plan.**

AKM Fitness is the operational skill package for training decision workflows under real constraints.
It is designed for situations where body limits, equipment reality, time budget, recovery state, and goal hierarchy all materially affect what training is appropriate.

## Position

AKM Fitness is not a generic workout Q&A tool.
It is a profile-first skill that turns training planning into a constrained decision process.

## Required Inputs

Serious use requires at least the following:

- `training goals`
- `body limitations or injury constraints`
- `available equipment`
- `weekly frequency`
- `session time budget`
- `recovery context`

When critical inputs are missing, the skill should expose `MissingInputs` rather than fabricate certainty.

## Workflow

1. `ELICITATION_PROMPT.md`
2. `RECORD_TEMPLATE.md`
3. `EXECUTION_PROMPT.md`

## Output Contract

Outputs should include:

- `StateJudgment`
- `PrimaryDecision`
- `DecisionConfidence`
- `Plan`
- `RiskNotes`
- `NonNegotiables`
- `MissingInputs`

## Best-Fit Scenarios

Use this skill when workout decisions are materially constrained by injury history, equipment changes, time limits, recovery instability, or conflicting goals.

## Boundaries

- not a medical diagnosis tool
- not a rehabilitation substitute
- not a bodybuilding template generator
- not a place to hide uncertainty behind motivational language