<!--
文件：README.zh-CN.md
核心功能：作为 AKM 母港的中文说明页，供 GitHub 读者从英文主页切换进入。
输入：AKM 母定义、母论文与分支结构。
输出：供 GitHub 使用的中文总览与分支导航。
-->

# AKM

**先把用户建模出来，再让下游 agent 开工。**

[English](./README.md)

`AKM` 是 `Active Knowledge Modeling` 的缩写。

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
- [Fitness](./branches/fitness/README.md)
- [Fashion](./branches/fashion/README.md)

## 当前状态

- AKM 母定义：已完成
- AKM 母论文：已完成，等待 SSRN 审核结果
- DaE：已确认为 AKM 的首个完整参考实现，并完成母港并入口径
- Fitness：已抽取为 `paper + skill + prompt package` 的公开版分支
- Fashion：已抽取为 `paper + skill + prompt package` 的公开版分支
- 外部模型测试：已完成一轮 DeepSeek 行为测试，用于验证方法边界而非疗效