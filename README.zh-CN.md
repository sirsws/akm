<!--
文件：README.zh-CN.md
核心功能：作为 AKM 母港的中文说明页，提供与英文主页对应的 banner、徽章、语言切换、导航、分支地图、研究入口与生态仓说明。
输入：AKM 母定义、母论文入口、DaE/Fitness/Fashion 分支入口、生态仓链接与展示素材。
输出：供 GitHub 中文读者使用的 README。
-->

# AKM — 主动知识建模

<p align="center">
  <img src="./assets/akm-banner.svg" alt="AKM banner" width="100%" />
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-0969da" alt="License" /></a>
  <img src="https://img.shields.io/badge/status-active-2ea44f" alt="Status" />
  <img src="https://img.shields.io/badge/paper-SSRN审核中-b31b1b" alt="Paper" />
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

**先把用户建模出来，再让下游 agent 开工。**

AKM 是一套更上游的 AI 协作方法。
它把用户建模视为基础设施，而不是对话修饰。

AKM 不接受“让 agent 在模糊 prompt 上直接开工”这套默认前提。
它要求系统先主动挖掘并结构化用户的目标、约束、偏好、背景和决策风格，再进入真正的规划、写作、建议或执行。

> 学术基础：AKM 母论文已提交 SSRN，公开 URL 待补。当前入口见 [AKM Mother Paper](./papers/akm/README.md)

---

## 什么是 AKM？

`Active Knowledge Modeling (AKM)` 指的是：

- 由 AI 主动追问并挖掘用户信息，而不是等用户写出完美 prompt
- 把这些信息结构化为可复用的上游资产
- 在任务开始前把这些资产注入工作流

AKM 之所以存在，是因为很多 AI 系统都死在同一层上游失真：

- 目标没排序就开始规划
- 约束没澄清就开始建议
- 现有资产没盘清就开始推荐
- 偏好和决策方式被默认处理

---

## 快速开始

第一次进入 AKM，建议按这个顺序：

1. 先读 [AKM.md](./AKM.md)
2. 再读 [AKM Mother Paper](./papers/akm/README.md)
3. 然后根据场景进入一个分支：
   - [DaE](./branches/dae/README.md)
   - [Fitness](./branches/fitness/README.md)
   - [Fashion](./branches/fashion/README.md)

---

## 分支地图

| 分支 | 场景 | 核心上游资产 | 当前状态 |
| --- | --- | --- | --- |
| [DaE](./branches/dae/README.md) | Persona / 顾问协作 | `PersonaProfile` | 首个完整参考实现 |
| [Fitness](./branches/fitness/README.md) | 训练约束、恢复限制、器械现实、训练裁决 | `FitnessProfile` | 已有公开版 paper + skill + prompt package |
| [Fashion](./branches/fashion/README.md) | 体型、场景、衣橱资产、穿搭 / 采购裁决 | `FashionProfile` | 已有公开版 paper + skill + prompt package |

### 这些分支为什么重要

- **DaE** 证明 AKM 在 persona 感知协作中的有效落地。
- **Fitness** 证明 AKM 可以在身体限制、器械现实和恢复不确定性下做训练裁决。
- **Fashion** 证明 AKM 可以在衣橱资产、体型和场景约束下做穿搭与采购裁决。

---

## 为什么这个仓库重要

很多 agent 项目太早优化下游输出。
AKM 处理的是更上游的一层。

它的目标不是让 agent “说得更像懂你”。
它的目标是让 agent **真的在更强的上游上下文里工作**。

这也是为什么这个仓库被组织为：

- 一个母概念
- 一篇母论文
- 多个可复用的分支实现
- 对应的研究仓与分发仓

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

AKM 是母港。
当前公开生态包括：

- [AKM 母港](https://github.com/sirsws/akm)
- [DaE skill 仓](https://github.com/sirsws/dae-persona-context-injector)
- [DaE research 仓](https://github.com/sirsws/DaE-Personal-Strategic-Asset)

这两个 DaE 仓现在都已经回链到 AKM 母港结构。

---

## 当前状态

- AKM 母定义：已完成
- AKM 母论文：已完成，SSRN URL 待补
- DaE：已统一为 AKM 的首个完整参考实现
- Fitness：公开版 paper + skill + prompt package 已就绪
- Fashion：公开版 paper + skill + prompt package 已就绪
- 外部模型验证：已完成一轮 DeepSeek 行为测试

---

## 许可证

本仓库采用 [Apache License 2.0](./LICENSE)。

---

## 原则

- 先建模，再执行
- 缺关键输入时，允许拒绝完整结论
- 不把 prompt 包装成方法
- 不把营销文案包装成系统