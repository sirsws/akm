<!--
文件：manuscript.md
核心功能：作为 DaE 分支论文的草稿，说明 AKM 在 Persona 与顾问协作场景中的具体实现。
输入：AKM 母定义、DaE 既有研究口径、DaE 的 profile-first 工作流。
输出：供后续整理为正式子论文的分支稿件。
-->

# DaE as the First AKM Implementation

## 摘要

DaE 是 `Active Knowledge Modeling (AKM)` 在 Persona / 顾问协作场景中的首个完整参考实现。它不直接提供建议，而是先通过结构化追问建立用户模型，生成可复用的 `PersonaProfile`，再让下游智能体基于该上游资产执行规划、写作、研究或顾问工作。

## 关键逻辑

1. 先追问，不先建议
2. 先验证，不先接受自我描述
3. 先生成上游画像，再把画像注入下游工作流
