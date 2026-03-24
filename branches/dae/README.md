<!--
文件：README.md
核心功能：作为 DaE 分支在 AKM 母港中的英文主入口，明确其在 AKM 体系中的定位、论文入口、skill 入口与阅读路径。
输入：AKM 母定义、DaE 发布资产与研究资产。
输出：供 GitHub 分支页直接使用的英文总览页。
-->

# DaE

**DaE is the first complete reference implementation of AKM in persona and advisory collaboration.**

[中文说明](./README.zh-CN.md)

DaE is no longer presented as a concept parallel to AKM.

Its role is now explicit:

**if AKM solves "model the person first," DaE solves how to operationalize that idea in persona-aware advisory and collaboration workflows.**

## What this branch solves

Many collaborative agents do not fail because they cannot answer.
They fail because they start working before they understand the user.

DaE addresses that upstream failure by building a reusable `PersonaProfile` before downstream collaboration begins.

## Branch position

- parent concept: AKM
- scene: persona / advisory collaboration
- upstream asset: `PersonaProfile`
- role: first complete reference implementation

## Why it matters

DaE was the first AKM line to become a complete method package.
It demonstrates a core claim:

**user modeling is not conversational decoration; it is upstream infrastructure for downstream collaboration quality.**

## Entry points

- [Paper](./paper/README.md)
- [Skill](./skill/README.md)