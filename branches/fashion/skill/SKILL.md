---
name: "akm-fashion-strategist"
description: "AKM 在穿搭场景下的实现。先建模体型、场景、衣橱资产与功能约束，再输出穿搭与采购裁决。"
---

<!--
文件：SKILL.md
核心功能：作为 AKM Fashion skill 的正式发布入口，说明其定位、输入要求、工作流、输出契约与使用边界。
输入：Fashion 分支的方法结构、提示词文件、记录模板与测试结论。
输出：供 GitHub、技能市场或代理工具直接引用的正式 skill 说明。
-->

# AKM Fashion Skill

**No wardrobe model, no serious styling advice.**

AKM Fashion 不是风格 moodboard，也不是“随手推荐几件单品”的 stylist prompt。
它是一个先建模、后裁决的穿搭与衣橱规划 skill，用来处理那些“真实场景和现有资产比审美口号更重要”的穿搭问题。

## 定位

用一句话概括：

**先建立形象画像，再决定今天怎么穿、接下来该补什么。**

它优先处理的是：

- 场景排序
- 体型与体态
- 风格偏好与禁区
- 现有衣橱资产
- 功能性约束
- 采购优先级

## 输入要求

严肃使用前，至少要有这些输入：

- `body shape or posture notes`
- `primary scenes`
- `style preferences`
- `wardrobe assets already owned`
- `functional constraints`

如果这些输入缺得太多，skill 应优先暴露 `MissingInputs`，而不是假装自己知道用户衣橱全貌。

## 工作流

1. 运行 `ELICITATION_PROMPT.md`
   追问场景、体型、衣橱、风格偏好与功能约束。
2. 使用 `RECORD_TEMPLATE.md`
   整理为结构化 `FashionProfile`。
3. 运行 `EXECUTION_PROMPT.md`
   在读取画像后输出穿搭裁决、短板分析、采购优先级与待补信息。

## 输出契约

输出至少应包含：

- `SceneJudgment`
- `OutfitRecommendation`
- `WhyThisWorks`
- `GapAnalysis`
- `PurchasePriority`
- `MissingInputs`

## 最适合的使用场景

在这些情况下，这个 skill 最有价值：

- 用户需要场景化穿搭决策
- 用户现有衣橱会实质限制建议空间
- 功能性与舒适性和审美同等重要
- 用户真正想要的是采购优先级，而不是风格口号

## 不适合的使用场景

- 用户只想要模糊的风格灵感
- 任务本质上是图像识别、量体或虚拟试衣
- 已经有稳定且可信的 `FashionProfile`，只需要执行，不需要重新挖掘

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