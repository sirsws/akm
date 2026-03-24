<!--
文件：README.md
核心功能：作为 AKM 母港的英文主入口，明确母概念、母论文与 DaE / Fitness / Fashion 三条成熟分支的关系与阅读路径。
输入：AKM 母定义、AKM 母论文、DaE 发布资产、健身工作流与穿搭工作流。
输出：供 GitHub 母港首页直接使用的英文总览文档与分支导航。
-->

# AKM

**Build the user model first. Then let downstream agents work.**

[中文说明](./README.zh-CN.md)

`AKM` stands for `Active Knowledge Modeling`.

It is not a single product and not the name of a single prompt.
It is an upstream method:

**model the user's goals, constraints, preferences, context, and decision style first, then let downstream agents plan, write, collaborate, advise, or execute from that stronger starting point.**

## One-line definition

Active Knowledge Modeling means that AI actively elicits and structures user information, turns that information into a reusable upstream asset, and injects it into the workflow before the actual task begins.

## Repository structure

### Parent layer

- [AKM definition](./AKM.md)
- [AKM parent paper](./papers/akm/README.md)

### Branch layer

- [DaE](./branches/dae/README.md)
  The first complete reference implementation of AKM in persona and advisory collaboration.
- [Fitness](./branches/fitness/README.md)
  AKM applied to training constraints, recovery limits, equipment reality, and workout decisions.
- [Fashion](./branches/fashion/README.md)
  AKM applied to body shape, scene requirements, wardrobe assets, and outfit / purchase decisions.

## Why this repository exists

Most AI systems fail not because the downstream model is too weak, but because upstream user modeling is too weak.

Common failure patterns include:

- planning before goals are ranked
- advising before constraints are clarified
- recommending before current assets are known
- treating style, decision logic, and execution risk as if they were obvious by default

AKM exists to fix that layer.

## Current status

- AKM definition: completed
- AKM parent paper: completed, waiting on SSRN review status
- DaE: confirmed as AKM's first complete reference implementation and merged into the mother-hub narrative
- Fitness: extracted into a public `paper + skill + prompt package` branch
- Fashion: extracted into a public `paper + skill + prompt package` branch
- External model testing: one DeepSeek behavior test round completed to validate method boundaries rather than outcome claims

## Suggested reading path

1. Start with [AKM.md](./AKM.md)
2. Then read [papers/akm/README.md](./papers/akm/README.md)
3. Then enter one branch:
   - [DaE](./branches/dae/README.md)
   - [Fitness](./branches/fitness/README.md)
   - [Fashion](./branches/fashion/README.md)

## Principles

- model first, execute second
- allow refusal when critical inputs are missing
- do not package a prompt as if it were a method
- do not package marketing copy as if it were a system