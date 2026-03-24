<!--
文件：README.zh-CN.md
核心功能：作为 DaE skill 的中文入口页，说明用途、输入输出与文件导航。
输入：DaE skill 包、AKM 母港结构与分支定位。
输出：供 GitHub 中文读者使用的 README。
-->

# DaE Skill

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md">简体中文</a>
</p>

## 用途

DaE skill 是在下游任务开始前构建 `PersonaProfile` 的可执行入口。

## 输入

- 通过结构化追问获得的用户回答
- 画像约束与上下文证据

## 输出

- 可复用的 `PersonaProfile`
- 供下游顾问协作或多 agent 工作流使用的上游上下文

## 文件

- [SKILL.md](./SKILL.md)
- [references/](./references/)