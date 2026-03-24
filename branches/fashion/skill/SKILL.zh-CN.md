<!--
文件：SKILL.zh-CN.md
核心功能：作为 AKM Fashion skill 的正式中文说明页，定义其定位、输入要求、工作流、输出契约与使用边界。
输入：Fashion 分支方法结构、提示词文件、记录模板与测试结论。
输出：供 GitHub 中文读者使用的 skill 文档。
-->

# AKM Fashion Skill

<p align="center">
  <a href="./SKILL.md">English</a> | <a href="./SKILL.zh-CN.md">简体中文</a>
</p>

**没有衣橱模型，就没有严肃穿搭建议。**

AKM Fashion 是面向真实场景和资产约束的穿搭裁决 skill 包。
它适用于那些体型、现有衣橱、场景要求和功能约束都会实质影响穿搭决策的场景。

## 定位

AKM Fashion 不是 moodboard 生成器，也不是泛用 stylist 人设。
它是一个 profile-first skill，用来把穿搭问题转化为受约束的决策过程。

## 必要输入

严肃使用至少需要：

- `body shape or posture notes`
- `primary scenes`
- `style preferences`
- `wardrobe assets already owned`
- `functional constraints`

当关键输入缺失时，skill 应优先暴露 `MissingInputs`，而不是假装已经知道完整衣橱。

## 工作流

1. `ELICITATION_PROMPT.md`
2. `RECORD_TEMPLATE.md`
3. `EXECUTION_PROMPT.md`

## 输出契约

输出应包含：

- `SceneJudgment`
- `OutfitRecommendation`
- `WhyThisWorks`
- `GapAnalysis`
- `PurchasePriority`
- `MissingInputs`

## 最适合的场景

当穿搭决策依赖场景上下文、衣橱限制、体型条件、功能性要求和采购取舍时，应使用这个 skill。

## 边界

- 不是图像识别工具
- 不是虚拟试衣产品
- 不是泛用审美生成器
- 不用漂亮话掩盖缺失上下文