<!--
文件：README.zh-CN.md
核心功能：作为 AKM 母港的中文入口页，提供与英文主页对应的定位语、双语切换、快速导航、分支地图、研究入口与生态仓链接，并明确 AKM 对主流平台上下文槽位的上游方法论定位。
输入：AKM 母定义、母论文入口、DaE/Fitness/Fashion 分支入口、旧 DaE 公共仓链接与状态信息。
输出：供 GitHub 中文读者理解 AKM 方法框架的中文 README。
-->

# AKM - 主动知识建模

<p align="center">
  <img src="./assets/akm-banner.svg" alt="AKM banner" width="100%" />
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-0969da" alt="License" /></a>
  <img src="https://img.shields.io/badge/status-active-2ea44f" alt="Status" />
  <img src="https://img.shields.io/badge/paper-SSRN_审核中-b31b1b" alt="Paper" />
  <img src="https://img.shields.io/badge/branches-3-6f42c1" alt="Branches" />
  <img src="https://img.shields.io/github/stars/sirsws/akm?style=flat" alt="GitHub stars" />
</p>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> |
  <a href="#什么是-akm">核心概念</a> |
  <a href="#分支地图">分支地图</a> |
  <a href="#研究入口">研究入口</a> |
  <a href="#生态仓">生态仓</a>
</p>

**OpenClaw、ChatGPT、Gemini 这类平台已经给了 `user/context` 槽位。AKM 要解决的，是这些槽位到底该怎么填。**

AKM 是一套面向 AI 协作的主动式、结构化用户建模框架。
它把画像构建视为基础设施，而不是对话修饰。

OpenClaw、ChatGPT、Gemini 这类平台都允许用户提供上下文。
真正缺失的，往往不是输入框，而是如何主动挖掘、结构化记录、再把这些信息稳定回灌到下游任务里的方法。
AKM 定义的，就是这一层上游方法。

> 学术入口：母论文已提交 SSRN，公开 URL 待补。当前入口见 [AKM Mother Paper](./papers/akm/README.md)

---

## 什么是 AKM？

`Active Knowledge Modeling (AKM)` 指的是：

- 系统主动挖掘用户信息，而不是等待用户一次性写出完美 prompt
- 把挖出的信息整理成可复用的上游资产
- 在规划、写作、顾问、编码、执行前，把这些资产注入工作流

AKM 之所以存在，是因为很多 AI 系统虽然有上下文槽位，却没有一套严肃的填法：

- 目标未排序就开始规划
- 约束未澄清就开始建议
- 现有资产未建模就开始推荐
- 偏好与决策逻辑被默认存在

---

## 快速开始

1. 先读 [AKM.md](./AKM.md)
2. 再读 [AKM Mother Paper](./papers/akm/README.md)
3. 然后按场景进入分支：
   - [DaE](./branches/dae/README.md)：Persona / 顾问协作
   - [Fitness](./branches/fitness/README.md)：真实约束下的训练决策
   - [Fashion](./branches/fashion/README.md)：真实约束下的衣橱与穿搭决策

---

## 分支地图

| 分支 | 场景 | 核心上游资产 | 状态 |
| --- | --- | --- | --- |
| [DaE](./branches/dae/README.md) | Persona / 顾问协作 | `PersonaProfile` | 首个完整 AKM 参考实现 |
| [Fitness](./branches/fitness/README.md) | 训练约束、恢复、器械与日级训练决策 | `FitnessProfile` | 分支论文 + 双语 skill 包 |
| [Fashion](./branches/fashion/README.md) | 体型、场景、衣橱资产与穿搭 / 采购决策 | `FashionProfile` | 分支论文 + 双语 skill 包 |

### 这些分支为什么重要

- **DaE** 证明了 AKM 在 persona 感知顾问协作中的完整实现。
- **Fitness** 展示了 AKM 如何处理身体限制、器械现实与恢复不确定性。
- **Fashion** 展示了 AKM 如何处理衣橱限制、体型语境、场景要求与采购取舍。

---

## 研究入口

### 母论文

- [AKM Mother Paper](./papers/akm/README.md)
- 仓内 PDF：[AKM-main.pdf](./papers/akm/AKM-main.pdf)
- SSRN 状态：已提交，公开 URL 待补

### 分支论文

- [DaE Paper Entry](./branches/dae/paper/README.md)
- [Fitness Paper Entry](./branches/fitness/paper/README.md)
- [Fashion Paper Entry](./branches/fashion/paper/README.md)

---

## 生态仓

- [AKM 母港](https://github.com/sirsws/akm)
- [DaE skill 仓](https://github.com/sirsws/dae-persona-context-injector)
- [DaE research 仓](https://github.com/sirsws/DaE-Personal-Strategic-Asset)

这两个 DaE 仓仍是公开历史入口，但现在都回链到 AKM 母港结构。

---

## 当前状态

- AKM 母定义：已完成
- AKM 母论文：已完成，SSRN URL 待补
- DaE 分支：已统一为 AKM 的首个完整参考实现
- Fitness 分支：分支论文 + 双语 skill 包正在统一修订
- Fashion 分支：分支论文 + 双语 skill 包正在统一修订
- 双语公开层：正在统一 README、paper、skill 与 prompt 文件

---

## 许可证

本仓库采用 [Apache License 2.0](./LICENSE)。



