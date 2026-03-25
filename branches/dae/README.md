<!--
文件：README.md
核心功能：作为 DaE 分支在 AKM 母港中的英文主入口，说明分支定位、核心资产、场景与入口导航。
输入：AKM 母定义、DaE 研究线、DaE skill 与旧公开仓关系。
输出：供 GitHub 读者理解 DaE 分支角色的英文 README。
-->

# DaE - AKM Reference Implementation

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

**DaE is the first complete AKM reference implementation for persona-aware advisory and collaboration workflows.**

## Scope

DaE operationalizes AKM in workflows where downstream quality depends on a reusable user profile.
Its primary scene is persona-aware collaboration across planning, advisory, writing, coding, and multi-agent work.

## Core Asset

The central upstream asset is `PersonaProfile`.
It captures structured user context for reuse across downstream tasks instead of forcing every session to rebuild context from scratch.

## Why This Branch Exists

Many platforms let users provide context, but they do not provide a disciplined way to build that context.
DaE supplies that missing operational layer for persona-aware collaboration.

## Entry Points

- [Paper](./paper/README.md)
- [Skill](./skill/README.md)
- [AKM Mother Hub](../../README.md)
