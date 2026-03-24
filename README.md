<!--
文件：README.md
核心功能：作为 AKM 母港的统一入口，明确母概念、母论文与 DaE / Fitness / Fashion 三条成熟分支的关系与阅读路径。
输入：AKM 母定义、AKM 母论文、DaE 发布资产、健身工作流与穿搭工作流。
输出：供 GitHub 母港首页直接使用的正式总览文档与分支导航。
-->

# AKM

**Build the user model first. Then let downstream agents work.**

`AKM` 是 `Active Knowledge Modeling` 的统一母港。

它不是某一个单独产品，也不是某一个 prompt 的名字。
它是一套更上游的方法：

**先把用户的目标、约束、偏好、背景和决策风格建模出来，再让下游 agent 去规划、写作、协作、建议或执行。**

## 一句话定义

主动知识建模，是指由 AI 主动追问并结构化用户信息，把这些上游信息沉淀为可复用资产，再在任务开始前注入工作流，使系统先认识人，再处理事。

## 仓库结构

### 母层

- [AKM 定义](./AKM.md)
- [AKM 母论文](./papers/akm/README.md)

### 分支层

- [DaE](./branches/dae/README.md)
  AKM 在 Persona / 顾问协作场景下的首个完整参考实现。
- [Fitness](./branches/fitness/README.md)
  AKM 在训练约束、恢复限制、器械现实与训练裁决中的应用。
- [Fashion](./branches/fashion/README.md)
  AKM 在体型、场景、衣橱资产与穿搭/采购裁决中的应用。

## 为什么这个仓库存在

大多数 AI 系统出问题，不是因为下游模型不够强，而是因为上游用户建模太弱。

常见失真包括：

- 目标没排序就开始规划
- 约束没澄清就开始建议
- 现有资产没盘清就开始推荐
- 风格偏好、决策方式、执行风险都被默认处理

AKM 的价值就在这里：

- 把“用户是谁”从模糊背景，提升成显式输入
- 把一次性聊天内容，提升成可复用资产
- 把下游 agent 的工作，从泛化回答拉回约束内决策

## 当前状态

- AKM 母定义：已完成
- AKM 母论文：已完成，等待 SSRN 审核结果
- DaE：已确认为 AKM 的首个完整参考实现，并完成母港并入口径
- Fitness：已抽取为 `paper + skill + prompt package` 的公开版分支
- Fashion：已抽取为 `paper + skill + prompt package` 的公开版分支
- 外部模型测试：已完成一轮 DeepSeek 行为测试，用于验证方法边界而非疗效

## 阅读顺序

如果你第一次进入 AKM，建议按这个顺序：

1. 先读 [AKM.md](./AKM.md)
2. 再看 [papers/akm/README.md](./papers/akm/README.md)
3. 然后选一个分支进入：
   - [DaE](./branches/dae/README.md)
   - [Fitness](./branches/fitness/README.md)
   - [Fashion](./branches/fashion/README.md)

## 原则

- 先建模，再执行
- 缺关键输入时，允许拒绝完整结论
- 不把 prompt 包装成方法
- 不把营销文案包装成系统