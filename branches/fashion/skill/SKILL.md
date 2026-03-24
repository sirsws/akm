---
name: "akm-fashion-strategist"
description: "AKM implementation for wardrobe and outfit decision workflows. Models body context, scenes, wardrobe assets, and functional constraints before outputting styling decisions."
---

<!--
文件：SKILL.md
核心功能：作为 AKM Fashion skill 的正式英文说明页，定义其定位、输入要求、工作流、输出契约与使用边界。
输入：Fashion 分支方法结构、提示词文件、记录模板与测试结论。
输出：供 GitHub、技能市场或代理工具直接引用的英文 skill 文档。
-->

# AKM Fashion Skill

<p align="center">
  <a href="./SKILL.md">English</a> | <a href="./SKILL.zh-CN.md">简体中文</a>
</p>

**No wardrobe model, no serious styling advice.**

AKM Fashion is the operational skill package for wardrobe and outfit decision workflows under real scene and asset constraints.
It is designed for situations where body context, existing wardrobe, scene requirements, and functional constraints all materially affect what styling decision is appropriate.

## Position

AKM Fashion is not a moodboard generator and not a generic styling persona.
It is a profile-first skill that turns styling into a constrained decision process.

## Required Inputs

Serious use requires at least the following:

- `body shape or posture notes`
- `primary scenes`
- `style preferences`
- `wardrobe assets already owned`
- `functional constraints`

When critical inputs are missing, the skill should expose `MissingInputs` rather than pretend the wardrobe is already known.

## Workflow

1. `ELICITATION_PROMPT.md`
2. `RECORD_TEMPLATE.md`
3. `EXECUTION_PROMPT.md`

## Output Contract

Outputs should include:

- `SceneJudgment`
- `OutfitRecommendation`
- `WhyThisWorks`
- `GapAnalysis`
- `PurchasePriority`
- `MissingInputs`

## Best-Fit Scenarios

Use this skill when outfit choices depend on scene context, wardrobe limits, body shape, functionality, and purchase tradeoffs rather than loose style labels.

## Boundaries

- not an image-recognition tool
- not a virtual try-on product
- not a generic taste generator
- not a place to hide missing context behind aesthetic language