<!--
文件：SKILL.zh-CN.md
核心功能：作为 AKM Fitness skill 的正式中文说明页，定义其定位、输入要求、工作流、输出契约与使用边界。
输入：Fitness 分支方法结构、提示词文件、记录模板与测试结论。
输出：供 GitHub 中文读者使用的 skill 文档。
-->

# AKM Fitness Skill

<p align="center">
  <a href="./SKILL.md">English</a> | <a href="./SKILL.zh-CN.md">简体中文</a>
</p>

**没有画像，就没有严肃训练方案。**

AKM Fitness 是面向真实约束条件的训练裁决 skill 包。
它适用于那些身体限制、器械现实、时间预算、恢复状态和目标层级都会实质影响训练决策的场景。

## 定位

AKM Fitness 不是通用健身问答工具。
它是一个 profile-first skill，用来把训练规划转化为受约束的决策过程。

## 必要输入

严肃使用至少需要：

- `training goals`
- `body limitations or injury constraints`
- `available equipment`
- `weekly frequency`
- `session time budget`
- `recovery context`

当关键输入缺失时，skill 应优先暴露 `MissingInputs`，而不是伪装确定性。

## 工作流

1. `ELICITATION_PROMPT.md`
2. `RECORD_TEMPLATE.md`
3. `EXECUTION_PROMPT.md`

## 输出契约

输出应包含：

- `StateJudgment`
- `PrimaryDecision`
- `DecisionConfidence`
- `Plan`
- `RiskNotes`
- `NonNegotiables`
- `MissingInputs`

## 最适合的场景

当训练决策会被伤病史、器械变化、时间上限、恢复波动或多目标冲突显著影响时，应使用这个 skill。

## 边界

- 不是医疗诊断工具
- 不替代康复建议
- 不是健美模板生成器
- 不用热血话术掩盖不确定性