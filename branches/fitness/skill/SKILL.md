---
name: "akm-fitness-planner"
description: "AKM implementation for training decision workflows. Models goals, body limits, equipment context, time budget, and recovery before outputting a workout decision."
---

<!--
文件：SKILL.md
核心功能：作为 AKM Fitness skill 的英文正式说明页，定义其定位、输入要求、工作流、输出契约、双语规则与边界。
输入：Fitness 分支方法结构、提示词文件、记录模板与公开 skill 设计。
输出：供 GitHub、技能市场或代理工具直接引用的英文 skill 文档。
-->

# AKM Fitness Skill

<p align="center">
  <a href="./SKILL.md">English</a> | <a href="./SKILL.zh-CN.md">简体中文</a>
</p>

**No profile, no serious plan.**

AKM Fitness is the operational skill package for training decision workflows under real constraints.
It is designed for situations where body limits, equipment reality, time budget, recovery state, and goal hierarchy all materially affect what training is appropriate.

## Position

AKM Fitness is not a generic workout Q&A tool.
It turns training planning into a profile-first decision process.

## Required Inputs

- `training goals`
- `body limitations or injury constraints`
- `available equipment`
- `weekly frequency`
- `session time budget`
- `recovery context`

When critical inputs are missing, the skill should expose `MissingInputs` rather than fabricate certainty.

## Install

```bash
npx skills add https://github.com/sirsws/akm --skill akm-fitness-planner --full-depth
``` 

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

## Language Rule

Public landing pages are English-first with a Chinese toggle.
Field keys stay in English for output stability.
Operational prompting is available in both English and Chinese.

## Boundaries

- not a medical diagnosis tool
- not a rehabilitation substitute
- not a bodybuilding template generator
- not a place to hide uncertainty behind motivational language
