<!--
文件：SKILL.zh-CN.md
核心功能：作为 DaE skill 的正式中文说明页，定义其定位、核心资产、适用场景与边界。
输入：DaE 分支方法结构、PersonaProfile 字段设计、AKM 母港关系。
输出：供 GitHub 中文读者使用的 skill 文档。
-->

# DaE Skill

<p align="center">
  <a href="./SKILL.md">English</a> | <a href="./SKILL.zh-CN.md">简体中文</a>
</p>

**先建档，再协作。**

DaE 是 AKM 在 persona 感知顾问协作流程中的正式 skill 包。
它的作用是在下游规划、写作、咨询或多 agent 协作开始之前，先构建可复用的 `PersonaProfile`。

## 定位

- 母概念：`AKM`
- 分支：`DaE`
- 角色：`参考实现`

## 核心资产

这个 skill 的中心上游资产是 `PersonaProfile`。
它用于在多个下游任务之间复用结构化用户上下文。

常见字段包括：

- `Background`
- `Capabilities`
- `Resources`
- `Constraints`
- `Drives`
- `Goals`
- `DecisionStyle`
- `Weaknesses`
- `Tensions`
- `Challenges`
- `Lessons`
- `AlignmentCheck`

## 最适合的场景

当下游工作的质量依赖一层稳定、可复用的用户画像时，应使用这个 skill。
典型场景包括顾问协作、长期项目，以及原本会反复重建用户上下文的多 agent 工作流。

## 边界

- 不替代具体领域专家判断
- 不保证一次挖掘后画像永久有效
- 不把未经结构化和交叉校验的自我描述直接视为事实