<!--
文件：Fashion_SSRN提交包.md
核心功能：汇总 Fashion 分支论文对应的 SSRN 投稿外围材料，供页面提交与摘要页同步使用。
输入：Fashion 论文 LaTeX 定稿、paper 目录下的 abstract/keywords/manuscript 与 AKM 母框架口径。
输出：标题、摘要短版、关键词、作者口径、页面短句与上传指引。
-->

# Fashion SSRN 提交包

## 标题备选

1. **Profile-First Wardrobe Planning Under Real Constraints: Active Knowledge Modeling in Styling Decision Systems**
2. **Active Knowledge Modeling in Wardrobe Planning: A Profile-First Method for Scene and Asset Constraints**
3. **Constraint-Aware Styling Through Active Knowledge Modeling**

推荐使用第 1 个。

## SSRN 摘要短版

Platforms such as OpenClaw, ChatGPT, and Gemini already expose user-context or system-prompt fields, but they provide little guidance on how those fields should be populated in real wardrobe and outfit decisions. This paper presents the fashion branch of Active Knowledge Modeling (AKM) as a profile-first method for wardrobe planning under scene, asset, and functional constraints. Instead of generating styling output first, the branch elicits and structures body context, scene requirements, wardrobe assets, anti-preferences, purchase tolerance, and practical limits before producing an outfit or purchase recommendation. The contribution is methodological rather than benchmark-driven. It shows how styling workflows can be redesigned so that upstream user modeling becomes a stable decision layer. Local design records and representative decision traces are used to make workflow behavior visible, not to claim universal fashion performance.

## 关键词

- Active Knowledge Modeling
- Wardrobe Planning
- User Modeling
- Outfit Recommendation
- Explainable Recommendation
- Capsule Wardrobe

## 作者口径

- Author: `Weishi Shao`
- Affiliation: `Independent Researcher`
- Date line: `March 2026`

## 页面说明短句

This paper presents the fashion branch of Active Knowledge Modeling (AKM) as a profile-first method for wardrobe planning under scene, asset, and functional constraints. It should be read as a branch paper within the broader AKM framework rather than as an image-recognition or benchmark paper.

## 上传文件

- Main PDF: `AKM工作区/AKM母港/branches/fashion/paper/latex/main.pdf`
- Main LaTeX source: `AKM工作区/AKM母港/branches/fashion/paper/latex/main.tex`
- Reference metadata: `AKM工作区/AKM母港/branches/fashion/paper/latex/refs.bib`

## 提交备注

- 本文定位是方法论文，不是图像识别论文，也不是虚拟试衣论文。
- `Design Record` 和代表性 JSON trace 用于展示工作流行为，不用于宣称普遍穿搭效果。
- 对外说明时保持与 AKM 母框架一致：平台已有上下文槽位，AKM 定义其填法，Fashion 是其中一个场景分支。
