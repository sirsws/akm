<!--
文件：README.md
核心功能：作为 AKM 母港的英文主入口页，提供适合 GitHub 项目首页展示的定位语、双语切换、快速导航、分支地图、研究入口与生态仓链接，并明确 AKM 对主流平台上下文承载面的上游方法论定位。
输入：AKM 母定义、母论文入口、DaE/Fitness/Fashion 分支入口、旧 DaE 公共仓链接与状态信息。
输出：供 GitHub 外部读者直接进入 AKM 方法框架的英文 README。
-->

# AKM - Active Knowledge Modeling

<p align="center">
  <img src="./assets/akm-banner.svg" alt="AKM banner" width="100%" />
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-0969da" alt="License" /></a>
  <img src="https://img.shields.io/badge/status-active-2ea44f" alt="Status" />
  <img src="https://img.shields.io/badge/paper-SSRN_in_review-b31b1b" alt="Paper" />
  <img src="https://img.shields.io/badge/branches-3-6f42c1" alt="Branches" />
  <img src="https://img.shields.io/github/stars/sirsws/akm?style=flat" alt="GitHub stars" />
</p>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> |
  <a href="#what-is-akm">Core Idea</a> |
  <a href="#branches">Branches</a> |
  <a href="#research">Research</a> |
  <a href="#ecosystem">Ecosystem</a>
</p>

**Platforms such as OpenClaw, ChatGPT, and Gemini already provide persistent context surfaces for user and agent state. AKM defines how that state should be elicited, structured, updated, and reused before downstream agents begin to work.**

AKM is a framework for active, structured user modeling in AI collaboration.
It treats profile construction as infrastructure rather than prompt decoration.

Platforms such as OpenClaw, ChatGPT, and Gemini already let users supply context.
OpenClaw makes this especially explicit through injected workspace files and system-prompt reconstruction across files such as `USER.md`, `IDENTITY.md`, `AGENTS.md`, and `MEMORY.md`. What these platforms usually lack is a repeatable method for eliciting, structuring, updating, and reusing the state that should populate those context endpoints.
AKM defines that missing upstream layer.

Official OpenClaw anchors: [Context](https://docs.openclaw.ai/context/), [System Prompt](https://docs.openclaw.ai/concepts/system-prompt), [USER Template](https://docs.openclaw.ai/templates/USER), [IDENTITY Template](https://docs.openclaw.ai/reference/templates/IDENTITY), [AGENTS Template](https://docs.openclaw.ai/reference/templates/AGENTS), [Memory](https://docs.openclaw.ai/concepts/memory)

> Academic foundation: parent paper in review at SSRN. Public landing page: [AKM Mother Paper](./papers/akm/README.md)

---

## What Is AKM?

`Active Knowledge Modeling (AKM)` means:

- the system actively elicits user information instead of waiting for a perfect prompt
- the elicited information is structured into reusable upstream assets
- those assets are injected before planning, writing, advising, coding, or execution begins

AKM exists because many AI systems already provide context endpoints without giving users a rigorous way to populate them:

- goals are not ranked before planning begins
- constraints are not clarified before advice is generated
- current assets are not modeled before recommendations appear
- preferences and decision rules are treated as if they were already obvious

---

## Quick Start

1. Read [AKM.md](./AKM.md)
2. Read the [AKM Mother Paper](./papers/akm/README.md)
3. Enter the branch that matches your scene:
   - [DaE](./branches/dae/README.md): persona and advisory collaboration
   - [Fitness](./branches/fitness/README.md): training decisions under real constraints
   - [Fashion](./branches/fashion/README.md): wardrobe and outfit decisions under real constraints

---

## Branches

| Branch | Scene | Core Upstream Asset | Status |
| --- | --- | --- | --- |
| [DaE](./branches/dae/README.md) | Persona / advisory collaboration | `PersonaProfile` | First complete AKM reference implementation |
| [Fitness](./branches/fitness/README.md) | Training constraints, recovery, equipment, workout decisions | `FitnessProfile` | Branch paper + bilingual skill package |
| [Fashion](./branches/fashion/README.md) | Body shape, scenes, wardrobe assets, outfit / purchase decisions | `FashionProfile` | Branch paper + bilingual skill package |

### Why these branches matter

- **DaE** is the first full reference implementation in persona-aware collaboration.
- **Fitness** shows how AKM handles physical constraints, equipment reality, and recovery uncertainty.
- **Fashion** shows how AKM handles wardrobe limits, body context, scene requirements, and purchase tradeoffs.

---

## Research

### Parent Paper

- [AKM Mother Paper](./papers/akm/README.md)
- PDF included in this repository: [AKM-main.pdf](./papers/akm/AKM-main.pdf)
- SSRN status: in review, public URL pending

### Branch Papers

- [DaE Paper Entry](./branches/dae/paper/README.md)
- [Fitness Paper Entry](./branches/fitness/paper/README.md)
- [Fashion Paper Entry](./branches/fashion/paper/README.md)

---

## Ecosystem

- [AKM mother hub](https://github.com/sirsws/akm)
- [DaE skill repository](https://github.com/sirsws/dae-persona-context-injector)
- [DaE research repository](https://github.com/sirsws/DaE-Personal-Strategic-Asset)

The two DaE repositories remain public historical entry points, but they now point back into this mother-hub structure.

---

## Current Status

- AKM definition: completed
- AKM parent paper: completed, SSRN URL pending
- DaE branch: unified as AKM's first complete reference implementation
- Fitness branch: branch paper + bilingual skill package available
- Fashion branch: branch paper + bilingual skill package available
- Bilingual public layer: standardized across README, paper, skill, and prompt files

---

## License

This repository is released under the [Apache License 2.0](./LICENSE).












