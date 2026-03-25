---
name: "dae-persona-context-injector"
description: "AKM 在 Persona 感知顾问与协作场景中的首个参考实现，在下游任务开始前先构建可复用的 PersonaProfile。"
---

<!--
文件：SKILL.zh-CN.md
核心功能：作为 DaE skill 的中文正式说明页，定义其定位、核心资产、适用场景、双语规则与边界。
输入：DaE 分支方法结构、PersonaProfile 字段设计与 AKM 母港关系。
输出：供 GitHub 中文页、技能市场或代理工具直接引用的中文 skill 文档。
-->

# DaE Skill

<p align="center">
  <a href="./SKILL.md">English</a> | <a href="./SKILL.zh-CN.md">简体中文</a>
</p>

**先建画像，再做协作。**

DaE 是 AKM 在 Persona 感知顾问与协作场景中的操作型 skill 包。
它的任务是在规划、写作、顾问、编码或多智能体协作开始前，先建立一个可复用的 `PersonaProfile`。

## 定位

- 母概念：`AKM`
- 分支：`DaE`
- 角色：`reference implementation`

## 核心资产

核心上游资产是 `PersonaProfile`。
典型字段包括：

- `Background`
- `Capabilities`
- `Resources`
- `Constraints`
- `Goals`
- `DecisionStyle`
- `Weaknesses`
- `Challenges`
- `Lessons`
- `AlignmentCheck`

## 双语规则

公开落地页采用英文主页 + 中文切换。
字段 key 保持英文，以保证路由与复用稳定。
实际提示词和执行过程可以使用英文或中文。

## 适用场景

当下游工作反复失败的原因是系统缺少一个稳定、可复用的“操作者模型”时，应该使用 DaE。

## 边界

- 不替代各领域的专业知识
- 不把单次挖掘结果视为永久有效画像
- 不把未经交叉校验的自述直接当成事实
