---
name: "dae-persona-context-injector"
description: "AKM 在 Persona / 顾问协作场景下的首个完整参考实现。先建立 PersonaProfile，再让下游智能体开工。"
---

<!--
文件：SKILL.md
核心功能：作为 DaE skill 的正式发布入口，说明其在 AKM 体系中的定位、输入输出与使用边界。
输入：DaE 分支的方法结构、既有发布资产与 PersonaProfile 字段定义。
输出：供 GitHub、技能市场或代理工具直接引用的正式 skill 说明。
-->

# DaE Skill

**Profile first. Then collaborate.**

DaE 是 `AKM` 在 Persona / 顾问协作场景下的首个完整参考实现。
它不是“让 agent 更懂你”的口号，而是一套先构建 `PersonaProfile`，再把它用于后续协作的上游方法。

## 定位

用一句话概括：

**先把用户画像做成结构化资产，再让下游 agent 开始规划、写作、建议或协作。**

## 上游关系

- Parent concept: `AKM`
- Branch: `DaE`
- Role: `first complete reference implementation`

## 核心产物

DaE 的关键上游资产是 `PersonaProfile`。
它至少覆盖这些字段：

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

## 最适合的使用场景

- 顾问协作前置建模
- 多 agent 协作前的用户画像注入
- 长期项目中的用户上下文复用
- 需要减少 generic answer 的任务流

## 边界

- 不替代具体任务领域知识
- 不保证一次建模永远有效
- 不把用户自述直接当事实而不校验