<!--
文件：AKM.md
核心功能：作为“主动知识建模 / Active Knowledge Modeling (AKM)”的唯一母文件，固化定义、边界、对立面、派生关系与复用口径。
输入：用户对 AKM 的最新定义修正、既有 DaE 产品资产、既有 SSRN 研究资产。
输出：供 README、SKILL、SSRN 摘要、技术声明等派生文稿直接复用的权威口径。
-->

# AKM

## 一句话定义

**主动知识建模（Active Knowledge Modeling, AKM）是指由 AI 引导并挖掘出用户的目标、约束、偏好、背景与决策风格，将其显式结构化，并在任务开始前主动注入 AI 工作流，使系统先认识人，再处理事。**

## AKM 不是什么

AKM 不是某个单独产品。

AKM 不是一次性 prompt 润色。

AKM 不是靠长期行为数据慢慢猜用户。

AKM 不是只有资料检索、没有用户模型层的个性化。

## AKM 在切什么旧范式

AKM 明确切割三类旧路径：

1. 被动用户建模：依赖长期交互和行为数据，让模型事后慢慢猜人。
2. 一次性 Prompt 定制：只优化局部指令，不形成稳定、可复用的用户模型。
3. 检索式个性化：只有资料片段，没有任务开始前的显式用户模型层。

## AKM 为什么高一层

AKM 处理的不是“这次怎么回答更像样”，而是“系统在开工前是否已经获得了足够稳定的用户模型”。

它把用户信息采集，从零散聊天副产品，提升为任务前置层。

它把“认识用户”从隐含猜测，提升为显式结构。

它把单次会话素材，提升为可跨任务复用的上游配置资产。

## DaE 与 AKM 的关系

**DaE 是 AKM 在 Persona / 顾问协作场景下的首个完整实现，现在就可以独立使用。**

DaE 不是独立于 AKM 的平行概念。

DaE 也不是“基于 AKM”的外围应用。

DaE 本身就是 AKM 在一个高价值场景里的 1 号实例。

## SSRN 与研究仓的关系

SSRN 论文与研究仓不是权威母源，它们是 AKM 的研究派生资产与时间戳证据。

它们的作用是：

1. 提供方法论溯源与公开时间锚点。
2. 证明相关核心思想早已形成，不是事后贴标签。
3. 为未来引用、对外背书与概念争夺提供证据链。

## 当前派生地图

当前建议按以下结构理解：

- `AKM.md`：唯一权威母文件。
- DaE GitHub / README / SKILL：AKM 的产品化派生入口。
- SSRN 论文与研究仓：AKM 的研究派生资产与公开证据。
- 未来顾问 / 健身 / 穿搭 / 健康智能体：AKM 的场景化派生实现。

## 可直接复用的短句

**AKM is a proactive user-modeling method.**

**DaE is the first complete implementation of AKM in persona and advisory collaboration.**

**SSRN and the research repository are derived research assets, not the canonical source of AKM.**

**Build the user model first. Then let downstream agents work.**
