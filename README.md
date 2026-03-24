<!--
文件：README.md
核心功能：作为 AKM 母港的英文主入口，提供适合 GitHub 框架仓展示的 banner、badges、语言切换、快速导航、分支地图、研究入口与生态仓导航。
输入：AKM 母定义、母论文入口、DaE/Fitness/Fashion 分支入口、生态仓链接与展示素材。
输出：供 GitHub 首页直接展示的英文 README。
-->

# AKM — Active Knowledge Modeling

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

**Build the user model first. Then let downstream agents work.**

AKM is an upstream method for AI collaboration.
It treats user modeling as infrastructure, not decoration.

Instead of letting agents work from vague prompts, AKM makes the system actively elicit and structure the user's goals, constraints, preferences, background, and decision style before the real task begins.

> Academic foundation: AKM parent paper in review at SSRN. Public landing page: [AKM Mother Paper](./papers/akm/README.md)

---

## What Is AKM?

`Active Knowledge Modeling (AKM)` means:

- AI actively elicits user information instead of waiting for perfect prompts
- that information is structured into reusable upstream assets
- those assets are injected into downstream workflows before planning, writing, advising, or execution begins

AKM exists because many AI systems fail at the same upstream layer:

- planning before goals are ranked
- advising before constraints are clarified
- recommending before current assets are known
- treating preferences and decision logic as if they were obvious by default

---

## Quick Start

If this is your first time here:

1. Read [AKM.md](./AKM.md)
2. Read the [AKM Mother Paper](./papers/akm/README.md)
3. Enter one branch based on the scene you care about:
   - [DaE](./branches/dae/README.md)
   - [Fitness](./branches/fitness/README.md)
   - [Fashion](./branches/fashion/README.md)

---

## Branches

| Branch | Scene | Core Upstream Asset | Status |
| --- | --- | --- | --- |
| [DaE](./branches/dae/README.md) | Persona / advisory collaboration | `PersonaProfile` | First complete reference implementation |
| [Fitness](./branches/fitness/README.md) | Training constraints, recovery, equipment, workout decisions | `FitnessProfile` | Public paper + skill + prompt package |
| [Fashion](./branches/fashion/README.md) | Body shape, scenes, wardrobe assets, outfit / purchase decisions | `FashionProfile` | Public paper + skill + prompt package |

### Why these branches matter

- **DaE** proves AKM in persona-aware collaboration.
- **Fitness** proves AKM under physical constraints, equipment reality, and recovery uncertainty.
- **Fashion** proves AKM under wardrobe limits, body context, scene requirements, and purchase decisions.

---

## Why This Repository Matters

Most agent projects optimize downstream output too early.
AKM focuses on the layer before that.

The goal is not to make agents sound smarter.
The goal is to make them work from stronger upstream context.

That is why this repository is organized around:

- a parent concept
- a parent paper
- reusable branch implementations
- public research and distribution repositories

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

AKM is the mother hub.
The public ecosystem currently includes:

- [AKM mother hub](https://github.com/sirsws/akm)
- [DaE skill repository](https://github.com/sirsws/dae-persona-context-injector)
- [DaE research repository](https://github.com/sirsws/DaE-Personal-Strategic-Asset)

The two DaE repositories now point back into this mother-hub structure.

---

## Current Status

- AKM definition: completed
- AKM parent paper: completed, SSRN URL pending
- DaE branch: unified as AKM's first complete reference implementation
- Fitness branch: public paper + skill + prompt package ready
- Fashion branch: public paper + skill + prompt package ready
- External model validation: one DeepSeek behavior-test round completed

---

## License

This repository is released under the [Apache License 2.0](./LICENSE).

---

## Principles

- model first, execute second
- allow refusal when critical inputs are missing
- do not package a prompt as a method
- do not package marketing copy as a system