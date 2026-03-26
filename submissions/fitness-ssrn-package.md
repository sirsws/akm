<!--
文件：Fitness_SSRN提交包.md
核心功能：汇总 Fitness 分支论文对应的 SSRN 投稿外围材料，供页面提交与摘要页同步使用。
输入：Fitness 论文 LaTeX 定稿、paper 目录下的 abstract/keywords/manuscript 与 AKM 母框架口径。
输出：标题、摘要短版、关键词、作者口径、页面短句与上传指引。
-->

# Fitness SSRN 提交包

## 标题备选

1. **Profile-First Fitness Planning Under Real Constraints: Active Knowledge Modeling in Training Decision Systems**
2. **Active Knowledge Modeling in Fitness Planning: A Profile-First Method Under Real Constraints**
3. **Constraint-Aware Fitness Planning Through Active Knowledge Modeling**

推荐使用第 1 个。

## SSRN 摘要短版

Platforms such as OpenClaw, ChatGPT, and Gemini already provide persistent context surfaces for user and agent state, but they provide little guidance on how the state behind those surfaces should be elicited, structured, updated, and reused in real decision environments. OpenClaw makes this especially explicit through injected workspace files and system-prompt reconstruction. This paper presents the fitness branch of Active Knowledge Modeling (AKM) as a profile-first method for training decisions under real constraints. Instead of generating a workout plan first, the branch elicits and structures ranked goals, injury limits, equipment availability, time budget, recovery uncertainty, and execution risk before producing a recommendation. The contribution is methodological rather than outcome-validational. It shows how a fitness workflow can be redesigned so that upstream user modeling becomes a stable decision layer rather than an afterthought in prompting. Local design records and representative decision traces are used to make workflow behavior visible, not to claim broad efficacy.

## 关键词

- Active Knowledge Modeling
- Fitness Planning
- User Modeling
- Constraint-Aware Decision Systems
- Training Load Monitoring
- Autoregulation

## 作者口径

- Author: `Weishi Shao`
- Affiliation: `Independent Researcher`
- Date line: `March 2026`

## 页面说明短句

This paper presents the fitness branch of Active Knowledge Modeling (AKM) as a profile-first method for training decisions under real constraints. It should be read as a branch paper within the broader AKM framework rather than as a general outcome-validation study.

## 上传文件

- Main PDF: `AKM工作区/AKM母港/branches/fitness/paper/latex/main.pdf`
- Main LaTeX source: `AKM工作区/AKM母港/branches/fitness/paper/latex/main.tex`
- Reference metadata: `AKM工作区/AKM母港/branches/fitness/paper/latex/refs.bib`

## 提交备注

- 本文定位是方法论文，不是医学验证论文。
- `Design Record` 和代表性 JSON trace 用于展示工作流行为，不用于宣称疗效。
- 对外说明时保持与 AKM 母框架一致：平台已有上下文承载面，AKM 定义其填法，Fitness 是其中一个场景分支。


