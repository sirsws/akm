<!--
文件：README.zh-CN.md
核心功能：作为 DaE 分支在 AKM 母港中的中文主入口，说明分支定位、核心资产、场景与入口导航。
输入：AKM 母定义、DaE 研究线、DaE skill 与旧公开仓关系。
输出：供 GitHub 中文读者理解 DaE 分支角色的中文 README。
-->

# DaE - AKM 参考实现

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

**DaE 是 AKM 在 Persona 感知顾问协作场景里的首个完整参考实现。**

## 范围

DaE 把 AKM 落地到这样一类工作流：下游质量取决于是否先建立一个可复用的用户画像层。
它的核心场景是 Persona 感知的规划、顾问、写作、编码与多智能体协作。

## 核心资产

上游核心资产是 `PersonaProfile`。
它把用户上下文整理成可复用结构，而不是每次对话都从零重建。

## 为什么这个分支存在

很多平台都允许用户提供上下文，但没有给出一套严肃、可复用的填法。
DaE 提供的，就是 Persona 感知协作里的那层操作方法。

## 入口

- [Paper](./paper/README.md)
- [Skill](./skill/README.md)
- [AKM Mother Hub](../../README.md)
