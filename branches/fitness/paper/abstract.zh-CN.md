<!--
文件：abstract.zh-CN.md
核心功能：作为 Fitness 分支论文的中文摘要提交件，供内部审稿与后续 LaTeX 转换直接复用。
输入：Fitness 分支论文正文、方法定位与本地设计记录。
输出：中文摘要定稿。
-->

# Fitness 摘要

OpenClaw、ChatGPT、Gemini 这类平台已经提供了用户与 agent 状态的上下文承载面，但在真实决策环境中，这些承载面背后的状态到底该如何被挖掘、结构化、更新和复用，平台几乎没有给出方法。其中 OpenClaw 通过 injected workspace files 和 system-prompt reconstruction 把这件事做得最显式。本文将 `Active Knowledge Modeling (AKM)` 的 Fitness 分支呈现为一种面向真实约束的画像优先训练决策方法。系统不是先生成训练计划，而是先挖掘并结构化记录目标排序、旧伤限制、器械可达性、时间预算、恢复不确定性和执行风险，然后才产出训练建议。本文的贡献是方法论层面的，而不是效果验证层面的。它展示了健身工作流如何被重写，使上游用户建模成为稳定的决策层，而不是 prompting 之后的补丁。本地设计记录与代表性决策样本仅用于让工作流行为可见，不用于宣称广义疗效。

