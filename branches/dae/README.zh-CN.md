<!--
文件：README.zh-CN.md
核心功能：作为 DaE 分支在 AKM 母港中的中文入口，说明分支定位、场景范围、核心资产与入口导航。
输入：AKM 母定义、DaE 发布资产与研究资产。
输出：供 GitHub 中文读者使用的 README。
-->

# DaE — AKM 参考实现

<p align="center">
  <img src="../../assets/akm-banner.svg" alt="AKM banner" width="100%" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/branch-DaE-F6B042" alt="DaE" />
  <img src="https://img.shields.io/badge/role-reference_implementation-2ea44f" alt="Role" />
  <img src="https://img.shields.io/badge/scene-persona_%2F_advisory_collaboration-6f42c1" alt="Scene" />
</p>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md">简体中文</a>
</p>

**DaE 是 AKM 在 persona 感知顾问协作场景下的参考实现。**

## 范围

DaE 处理的核心问题是：当下游规划、建议或协作质量依赖一份稳定可复用的用户画像时，如何把这层上游建模做成标准化工作流。

## 核心资产

这个分支的中心上游资产是 `PersonaProfile`。
它用于在多轮任务中复用用户背景、约束、驱动和决策风格，而不是让每个下游 agent 都从零重建上下文。

## 这个分支的价值

DaE 证明了一件事：用户建模可以作为上游基础设施存在，而不是可有可无的 prompt 修饰。

## 当前交付

- 分支总览
- DaE 研究论文入口
- DaE skill 入口
- 提示词与验收标准参考材料

## 入口

- [Paper](./paper/README.md)
- [Skill](./skill/README.md)
- [AKM 母港](../../README.md)