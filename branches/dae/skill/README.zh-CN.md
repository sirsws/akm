<!--
文件：README.zh-CN.md
核心功能：作为 DaE skill 的中文入口页，说明用途、输入输出与文件导航。
输入：DaE skill 包、AKM 母港结构与 DaE 分支定位。
输出：供 GitHub 中文页或技能市场直接引用的中文 README。
-->

# DaE Skill

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md">简体中文</a>
</p>

## 作用

DaE skill 是在下游任务开始前先构建 `PersonaProfile` 的操作入口。

## 输入

- 通过结构化追问获得的用户回答
- 画像约束与上下文证据

## 输出

- 一个可复用的 `PersonaProfile`
- 供后续顾问或协作工作流直接使用的上游上下文

## 文件

- [SKILL.md](./SKILL.md)
- [SKILL.zh-CN.md](./SKILL.zh-CN.md)
- [references/](./references/)
