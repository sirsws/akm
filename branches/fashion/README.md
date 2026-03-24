<!--
文件：README.md
核心功能：作为 Fashion 分支在 AKM 母港中的英文主入口，说明该分支的定位、方法结构、证据形态、论文与 skill 入口，以及适用边界。
输入：穿搭规则、衣橱资产、场景偏好与 AKM 方法结构。
输出：供 GitHub 分支页直接使用的英文总览页。
-->

# AKM Fashion

**AKM Fashion = build the wardrobe and scene model first, then make outfit and purchase decisions.**

[中文说明](./README.zh-CN.md)

This is not a generic styling assistant.
It is built for the more realistic question: when body shape, scene requirements, wardrobe limits, and functional constraints all matter, what should the user actually wear, and what should be added next?

## What it solves

Typical styling AI systems assume too much:

- body shape barely matters
- wardrobe assets are unlimited
- scene ambiguity is acceptable
- style labels can replace execution

AKM Fashion reverses that logic.
It models the operator and the wardrobe first, then allows execution.

## Method structure

1. `Elicitation`
   Clarify scenes, body context, wardrobe assets, style preferences, and functional constraints.
2. `Record`
   Store profile, core items, gaps, and anti-patterns as reusable upstream assets.
3. `Execution`
   Read the profile and output outfit decisions, gap analysis, and purchase priorities.

## Evidence form

This branch is best framed as:

**a long-term single-user AKM system design and method case.**

Its evidence includes stable wardrobe logic, explicit constraints, structured assets, and external model behavior tests.

## Entry points

- [Paper](./paper/README.md)
- [Skill](./skill/README.md)