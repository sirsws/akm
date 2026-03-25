<!--
文件：manuscript.zh-CN.md
核心功能：作为 Fashion 分支论文的中文 markdown 稿，说明 AKM 如何在衣橱与场景决策中把穿搭重写成画像优先的决策系统，并明确其对主流平台上下文槽位的上游方法论补位。
输入：穿搭私有系统、本地设计记录、衣橱资产信息与外部个性化推荐文献。
输出：供人工审阅后再转 LaTeX 的中文论文草稿。
-->

# Profile-First Wardrobe Planning Under Real Constraints: An AKM Branch Paper

## 摘要

本文讨论 `Active Knowledge Modeling (AKM)` 如何在衣橱规划与穿搭决策中发挥作用。系统不是先输出穿搭建议，再去补限制条件；它会先建模体型语境、场景要求、衣橱资产、功能约束和风格偏好，然后才做穿搭或采购决策。本文的贡献是方法论层面的：它展示了 AKM 如何把穿搭从泛审美语言改写成画像优先的决策设计。

## 1. 引言

OpenClaw、ChatGPT、Gemini 这类平台已经暴露出 `user-context` 或 system-prompt 字段，但很少给出一套严肃的状态构建方法，告诉用户这些字段里到底该放什么。穿搭系统把这个缺口暴露得尤其明显：泛化建议常常默认体型、衣橱库存、场景要求和功能限制都已经清楚，或者可以安全猜测。

问题仍然出在上游。如果穿搭质量取决于体型、场景逻辑、现有衣橱和功能性权衡，那么系统就不该先给建议，而应先建立一个关于“用户到底拥有什么、需要什么、拒绝什么、能穿什么”的模型。

## 2. 问题定义

当上游上下文不足时，普通穿搭 prompting 会出现一组稳定失真：

- 体型被压平成模糊审美标签，而不是决策变量
- 场景要求被压平成宽泛风格分类
- 衣橱资产被默认存在，而不是被建模
- 功能约束被当成可选细节
- 采购建议与现有衣橱结构脱钩

这些失败与个性化推荐研究的共通结论一致：推荐质量取决于显式用户状态、资产建模和可解释约束处理，而不是单靠模糊的“审美语言” [1]-[7]。

## 3. 方法：Fashion 场景中的 AKM

在穿搭场景中，AKM 建模的不是抽象身份，而是衣橱可行性。关键上游状态包括：

- 体型与体态信息
- 核心场景
- 已有衣橱资产
- 风格偏好与反偏好
- 功能性约束
- 采购容忍度与替换逻辑

这个分支以三层工作流实现。

### 3.1 Elicitation

系统先问清楚“什么样的穿搭决策才合法”，而不是立刻给搭配。它会先澄清场景、体型语境、偏好结构、功能限制和衣橱库存。

### 3.2 Structured Record

挖出的信息会被转成持久的上游状态，包括衣橱记录、场景地图、偏好记录和采购优先级记录。

### 3.3 Execution Decision

只有在画像和当前衣橱状态都具备后，系统才产出决策。输出契约包括：

- `SceneJudgment`
- `OutfitRecommendation`
- `WhyThisWorks`
- `GapAnalysis`
- `PurchasePriority`
- `MissingInputs`

## 4. 设计记录

这个分支的本地设计记录列在 [local-evidence.md](./local-evidence.md) 中，主要包括：

- 风格规则与反规则
- 衣橱资产记录
- 场景记录
- 穿搭决策文件
- 采购优先级记录
- 长期修订记录

这些记录不是 benchmark 证明，而是为了让工作流行为可见。下面展示一个代表性决策样本。

```json
{
  "SceneJudgment": "Business-casual office scene with movement needs and no tie requirement.",
  "OutfitRecommendation": "Use a dark knit polo, lightweight tailored trousers, and clean leather sneakers.",
  "WhyThisWorks": [
    "The combination preserves structure without over-formality.",
    "The knit top reduces stiffness while keeping the upper body clean.",
    "The trouser-sneaker pairing keeps mobility and visual balance."
  ],
  "GapAnalysis": [
    "Current tops are stronger than current trousers for this scene.",
    "Outerwear coverage is still weak for mild-temperature transition days."
  ],
  "PurchasePriority": [
    "Add one darker lightweight trouser with cleaner drape.",
    "Add one transitional jacket that preserves line without bulk."
  ],
  "MissingInputs": [
    "Exact weather range",
    "Shoes currently available for the scene",
    "Whether the user expects client-facing formality"
  ]
}
```

这个样本展示的是“部分信息缺失时工作流如何表现”，不是普遍穿搭效果证明。

## 5. 讨论

AKM 在穿搭场景中的主要价值，是**资产保真**。它压制了 agent 把穿搭只当成情绪板和审美标签问题来答的冲动。

真实衣橱决策取决于已有衣物、场景要求、体型语境、功能需求和采购取舍。忽略这些变量的系统，看起来可能更时髦，但会制造更多摩擦。先把这些变量建模进去的系统，虽然答案更窄，却更可执行。

## 6. 边界

这不是图像识别论文，不是虚拟试衣论文，也不是广义审美理论论文。
它的主张更窄：AKM 可以被实现为一个真实场景与资产约束下的画像优先衣橱决策系统。

## 7. 结论

Fashion 分支的重要性在于，它展示了 AKM 如何把穿搭从泛审美输出改写成一个基于衣橱状态、场景逻辑与显式权衡的决策过程。它的贡献是方法论的：在这个场景里，更好的上游建模可能比更漂亮的审美语言更重要。

## 参考文献

[1] Tangseng, P., Okatani, T., & Yamaguchi, K. (2017). *Toward Explainable Fashion Recommendation*. arXiv:1711.04394.

[2] Han, X., Wu, Z., Jiang, Y.-G., & Davis, L. S. (2017). *Learning Fashion Compatibility with Bidirectional LSTMs*. ACM Multimedia 2017. DOI: 10.1145/3123266.3123315.

[3] Hsiao, W.-L., Grauman, K. (2018). *Creating Capsule Wardrobes from Fashion Images*. CVPR 2018. DOI: 10.1109/CVPR.2018.00760.

[4] Jagadeesh, V., Piramuthu, R., Bhardwaj, A., et al. (2014). *Large Scale Visual Recommendations from Street Fashion Images*. KDD 2014. DOI: 10.1145/2623330.2623358.

[5] McAuley, J., Targett, C., Shi, Q., & van den Hengel, A. (2015). *Image-based Recommendations on Styles and Substitutes*. SIGIR 2015. DOI: 10.1145/2766462.2767755.

[6] Yu, M., Liu, X., Song, Y., & Han, X. (2021). *Explainable Fashion Recommendation: A Semantic Attribute Region Guided Approach*. CIKM 2021. DOI: 10.1145/3459637.3482449.

[7] Hidayati, S. C., Chen, H., Yang, K., et al. (2018). *Personality in Fashion: Prediction and Styling*. ACM Multimedia 2018. DOI: 10.1145/3240508.3240634.


