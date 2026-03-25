<!--
文件：manuscript.md
核心功能：作为 Fashion 分支论文的英文 markdown 稿，说明 AKM 如何在衣橱与场景决策中把穿搭重写成画像优先的决策系统，并明确其对主流平台上下文槽位的上游方法论补位。
输入：穿搭私有系统、本地设计记录、衣橱资产信息与外部个性化推荐文献。
输出：供人工审阅后再转 LaTeX 的英文论文草稿。
-->

# Profile-First Wardrobe Planning Under Real Constraints: An AKM Branch Paper

## Abstract

This paper examines how `Active Knowledge Modeling (AKM)` operates in wardrobe planning and outfit decision workflows. Instead of producing styling output first, the system models body context, scene requirements, wardrobe assets, functional constraints, and style preferences before making an outfit or purchase decision. The contribution is methodological. The branch shows how AKM converts styling from generic taste language into profile-first decision design.

## 1. Introduction

Platforms such as OpenClaw, ChatGPT, and Gemini already expose user-context or system-prompt fields, but they rarely provide a rigorous method for constructing the state that should populate them. Styling systems expose the gap clearly. Generic outfit advice often assumes that body shape, wardrobe inventory, scene demands, and functional limits are already known or can be safely guessed.

The problem is upstream. If outfit quality depends on body context, scene logic, wardrobe reality, and functional tradeoffs, then the system should not begin with a suggestion. It should begin with a model of what the user actually owns, needs, rejects, and can plausibly wear.

## 2. Problem Definition

When upstream context is weak, generic styling prompts degrade in predictable ways:

- body shape becomes a vague aesthetic label instead of a decision variable
- scene requirements are flattened into broad style categories
- wardrobe assets are assumed rather than modeled
- functional constraints are treated as optional details
- purchase advice is detached from existing wardrobe structure

These failures align with a broader lesson from personalized recommendation research: recommendation quality depends on explicit user state, asset modeling, and explainable constraint handling rather than on loose taste language alone [1]-[7].

## 3. Method: AKM in the Fashion Scene

In the fashion scene, AKM models wardrobe feasibility rather than abstract identity. The relevant upstream state includes:

- body shape and posture notes
- primary scenes
- wardrobe assets already owned
- style preferences and anti-preferences
- functional constraints
- purchase tolerance and replacement logic

The branch is implemented as a three-layer workflow.

### 3.1 Elicitation

The system first asks what kind of outfit decision is even valid. It clarifies scenes, body context, preference structure, functional limits, and wardrobe inventory before recommending anything.

### 3.2 Structured Record

The elicited information is converted into persistent upstream state through wardrobe records, scene maps, preference notes, and purchase-priority records.

### 3.3 Execution Decision

Only after profile and current wardrobe state are available does the system produce a decision. The output contract includes:

- `SceneJudgment`
- `OutfitRecommendation`
- `WhyThisWorks`
- `GapAnalysis`
- `PurchasePriority`
- `MissingInputs`

## 4. Design Record

The local design record for this branch is listed in [local-evidence.md](./local-evidence.md). It includes:

- style rules and anti-rules
- wardrobe asset records
- scene notes
- outfit decision files
- purchase-priority records
- long-running revision notes

These records are not presented as a benchmark claim. They are used to make workflow behavior visible.
A representative decision trace is shown below.

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

This trace illustrates workflow behavior under partial information. It is not a proof of universal styling effectiveness.

## 5. Discussion

The main value of AKM in fashion is asset preservation. It reduces the tendency of an agent to answer as if styling were only a matter of taste labels and inspiration boards.

Real wardrobe decisions depend on existing clothes, scene expectations, body context, function, and tradeoffs. A system that ignores those variables may sound stylish, but it will produce friction. A system that models them upstream is narrower, but more actionable.

## 6. Boundaries

This paper is not an image-recognition paper, not a virtual try-on paper, and not a broad aesthetics theory paper.
Its claim is narrower: AKM can be implemented as a profile-first wardrobe decision system under real scene and asset constraints.

## 7. Conclusion

The fashion branch matters because it shows how AKM converts styling from generic taste output into a decision process grounded in wardrobe state, scene logic, and explicit tradeoffs. The contribution is methodological: better upstream modeling can matter more than more polished aesthetic language.

## References

[1] Lu, Z., Hu, Y., Jiang, Y., Chen, Y., & Zeng, B. (2019). *Learning Binary Code for Personalized Fashion Recommendation*. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2019.

[2] Kang, W.-C., Kim, E., Leskovec, J., Rosenberg, C., & McAuley, J. (2019). *Complete the Look: Scene-Based Complementary Product Recommendation*. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2019.

[3] Lu, Z., Jiang, Y., Hu, Y., Chen, Y., & Zeng, B. (2021). *Personalized Outfit Recommendation with Learnable Anchors*. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2021.

[4] Sarkar, R., Bodla, N., Vasileva, M., Lin, Y.-L., Beniwal, A., Lu, A., & Medioni, G. (2022). *OutfitTransformer: Outfit Representations for Fashion Recommendation*. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), 2022.

[5] Li, L., Zhang, Y., & Chen, L. (2021). *Personalized Transformer for Explainable Recommendation*. Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics (ACL), 2021.

[6] Cheng, H., Wang, S., Lu, W., Zhang, W., Zhou, M., Lu, K., & Liao, H. (2023). *Explainable Recommendation with Personalized Review Retrieval and Aspect Learning*. Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL), 2023.

[7] Hsiao, W.-L., & Grauman, K. (2018). *Creating Capsule Wardrobes from Fashion Images*. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2018.



