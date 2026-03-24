---
name: "akm-fitness-planner"
description: "AKM 在健身场景下的实现。先建模目标、身体约束、器械环境、时间预算与恢复状态，再输出训练裁决。"
---

<!--
文件：SKILL.md
核心功能：作为 AKM Fitness skill 的正式发布入口，说明其定位、输入要求、工作流、输出契约与使用边界。
输入：Fitness 分支的方法结构、提示词文件、记录模板与测试结论。
输出：供 GitHub、技能市场或代理工具直接引用的正式 skill 说明。
-->

# AKM Fitness Skill

**No profile, no serious plan.**

AKM Fitness 不是通用健身问答，也不是一键生成训练单的 prompt。
它是一个先建模、后裁决的训练规划 skill，用来处理那些“约束比热情更重要”的真实训练场景。

## 定位

用一句话概括：

**先建立训练画像，再决定今天或这个阶段到底该怎么练。**

它优先处理的是：

- 目标冲突
- 身体限制
- 器械差异
- 时间预算
- 恢复状态
- 执行风险

## 输入要求

严肃使用前，至少要有这些输入：

- `training goals`
- `body limitations or injury constraints`
- `available equipment`
- `weekly frequency`
- `session time budget`
- `recovery context`

如果这些输入缺得太多，skill 应优先暴露 `MissingInputs`，而不是硬给完整处方。

## 工作流

1. 运行 `ELICITATION_PROMPT.md`
   追问主线目标、身体禁区、器械条件、时间预算、恢复与执行风险。
2. 使用 `RECORD_TEMPLATE.md`
   整理为结构化 `FitnessProfile`。
3. 运行 `EXECUTION_PROMPT.md`
   在读取画像后输出训练裁决、风险边界、置信度与待补信息。

## 输出契约

输出至少应包含：

- `StateJudgment`
- `PrimaryDecision`
- `DecisionConfidence`
- `Plan`
- `RiskNotes`
- `NonNegotiables`
- `MissingInputs`

## 最适合的使用场景

在这些情况下，这个 skill 最有价值：

- 用户有真实伤病或动作禁区
- 器械环境会显著改变方案
- 用户时间预算很硬
- 用户不缺热情，缺的是可执行裁决
- 用户长期被泛健身建议误导

## 不适合的使用场景

- 用户只想聊通用健身知识
- 任务本质上是医学诊断
- 已经有稳定且可信的 `FitnessProfile`，只需要执行，不需要重新挖掘

## 文件入口

正式使用前应先读：

- `ELICITATION_PROMPT.md`
- `RECORD_TEMPLATE.md`
- `EXECUTION_PROMPT.md`
- `INPUT_TEMPLATE.md`

## 上游关系

- 母概念：上游 `AKM.md`
- 分支入口：`../README.md`
- 分支论文：`../paper/manuscript.md`
- 当前方法文件：本目录