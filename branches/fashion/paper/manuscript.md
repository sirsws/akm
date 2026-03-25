<!--
文件：manuscript.md
核心功能：作为 Fashion 分支 SSRN 风格论文草稿，说明 AKM 在穿搭与衣橱规划场景中的研究问题、方法结构、证据形式与边界。
输入：穿搭系统一手证据、外部时尚推荐与可解释推荐文献、外部模型行为测试结果。
输出：供人工审阅后再转 LaTeX 的英文 markdown 论文稿。
-->

# Asset-Aware Wardrobe Planning and Outfit Decisions: An AKM Branch Case

## Abstract

This paper examines how `Active Knowledge Modeling (AKM)` operates in wardrobe planning and outfit decision workflows. Instead of producing styling output immediately, the system first models body context, scene requirements, wardrobe assets, functional constraints, and style preferences, and only then produces outfit recommendations, gap analysis, and purchase priorities. The paper is framed as a **single-user long-term system-design case** rather than a broad validation claim. Its contribution is methodological: it shows how AKM can convert styling from generic taste language into scene-aware and asset-aware decision making. The argument is supported by a local evidence base derived from a long-running private styling system and by external literature on personalized fashion recommendation, outfit compatibility, explainable recommendation, and capsule-wardrobe optimization [1]-[7].

## 1. Introduction

Most AI styling output fails for a simple reason: it does not know enough about the operator or the wardrobe. Systems that can describe style fluently still produce weak decisions when they ignore which scenes matter, what the user already owns, what body context must be handled, and which functional constraints are non-negotiable.

The research literature on fashion recommendation confirms this point from different angles. Outfit recommendation is not only a problem of item matching but also of compatibility, personalization, and context [1]-[4]. Explainable recommendation research further shows that useful recommendation output depends on making user-specific signals legible rather than relying on generic language alone [5], [6]. In wardrobe planning, the problem is even stricter: the recommendation is constrained not just by preference but by existing assets. Work on capsule wardrobes makes this explicit by treating the wardrobe as a combinational asset system rather than a flat list of isolated products [7].

This paper argues that AKM provides a useful framework for this scene because it forces the system to model the operator and the wardrobe before it generates styling output.

## 2. Research Position

This paper is not a computer-vision benchmark paper and not a large-sample fashion-recommendation evaluation. It is written as a branch-level systems and method paper. The question is whether AKM can organize wardrobe planning as a constrained decision workflow rather than a style-commentary workflow.

The evidence model is `single-user long-term self-use`. The relevant issue is not whether the branch wins on a public benchmark, but whether profile-first modeling changes the structure and usability of fashion decisions in practice.

## 3. Problem Definition

When wardrobe-related upstream variables are absent, styling systems degrade in familiar ways:

- they speak in vague taste language
- they ignore scene hierarchy
- they recommend items as if the user had no existing wardrobe constraints
- they generate purchase advice detached from current assets
- they offer polished explanations while lacking real user-specific grounding

The literature helps explain why this happens. Personalized fashion recommendation remains difficult because user preference is sparse, outfit compatibility is combinational, and context is often incomplete [1], [3], [4]. Explainable recommendation systems try to connect generated explanation to user and item context [5], [6], but in ordinary use there is still a gap between explanation fluency and actual wardrobe decision quality.

## 4. Method: AKM in the Fashion Scene

In this scene, AKM models wardrobe feasibility rather than style mood alone. The relevant upstream structure includes:

- scene hierarchy
- body context
- style preferences and anti-patterns
- wardrobe assets already owned
- functional constraints
- purchase priorities

The branch is implemented as a three-layer workflow.

### 4.1 Elicitation

The system first clarifies scenes, body context, existing assets, style preferences, and hard constraints. This step addresses the same personalization problem highlighted in the recommendation literature: preference cannot be approximated well if the system begins with too little user-specific context [1], [3].

### 4.2 Structured Record

The elicited material is converted into a reusable profile that covers both the operator and the wardrobe. This aligns with the asset-oriented logic visible in capsule-wardrobe research, where the value of a wardrobe depends on combinations, versatility, and the relationship between items rather than on isolated product descriptions [7].

### 4.3 Execution Decision

Only after the profile is available does the system produce outfit recommendations, gap analysis, and purchase priorities. The output contract is designed to make missing context visible instead of hiding it behind aesthetic fluency.

## 5. Why This Is Not a Generic Styling Prompt

A styling persona prompt can imitate fashion language without producing constrained decisions. The defining feature of this branch is not tone. It is workflow position. Wardrobe assets, scene hierarchy, and anti-patterns are treated as upstream inputs rather than optional flavor.

This difference matters because contemporary fashion recommendation systems increasingly model outfit-level relations and user-specific preference embeddings [2]-[4]. AKM extends the same idea into a decision-support workflow: build the user-and-wardrobe model first, then decide.

## 6. Evidence Base

The local evidence base for this paper is listed in [local-evidence.md](./local-evidence.md). At a high level, it includes:

- a long-running private styling system prompt
- a derived public elicitation prompt
- a structured wardrobe record template
- an execution prompt for outfit recommendation and gap analysis

To make that basis visible, a representative decision trace is shown below. The example is anonymized and slightly compressed, but it preserves the real structure of the workflow.

```json
{
  "SceneJudgment": "Primary need is smart-casual weekday wear with low-friction reuse across repeated office and city scenes.",
  "OutfitRecommendation": {
    "Top": "dark knit polo or clean long-sleeve shirt",
    "Bottom": "mid-to-dark tailored trousers",
    "OuterLayer": "light structured jacket if temperature or formality rises",
    "Shoes": "minimal leather sneakers or simple loafers"
  },
  "WhyThisWorks": [
    "The combination is anchored to repeat-use scenes rather than one-off styling theater.",
    "Silhouette stays clean without requiring a full wardrobe reset.",
    "The recommendation reuses likely core assets before suggesting purchases."
  ],
  "GapAnalysis": [
    "Wardrobe baseline suggests a shortage of versatile mid-formality outerwear.",
    "Footwear options may be too casual for cross-scene reuse."
  ],
  "PurchasePriority": [
    "1. Lightweight structured jacket in a versatile neutral tone",
    "2. One pair of cleaner leather footwear for smart-casual scenes"
  ],
  "MissingInputs": [
    "Current full wardrobe inventory",
    "Seasonal climate split",
    "Non-negotiable fit dislikes"
  ]
}
```

This trace is not presented as proof of benchmark superiority. It is presented as proof of system behavior: the workflow makes scene, asset, and wardrobe gaps explicit before it escalates to recommendation or purchasing advice.

External-model testing was used as a method-boundary check. The key question was whether another model would still preserve the upstream discipline of the workflow.

The critical behaviors were:

- eliciting scenes and wardrobe constraints before recommendations
- producing asset-aware outfit decisions instead of generic taste talk
- surfacing `MissingInputs` when wardrobe or context detail remained incomplete
- keeping purchase advice tied to gaps in the current wardrobe rather than to abstract aspiration

## 7. Discussion

The branch suggests that the practical value of AKM in fashion is not that it makes recommendations more fashionable in the abstract. Its value is that it changes the unit of reasoning. The system stops reasoning only over desired style and starts reasoning over scenes, constraints, and assets.

This is exactly where wardrobe planning differs from ordinary product recommendation. A wardrobe is an evolving asset system. Recommendations should therefore be evaluated not only by whether an item looks good in isolation, but by whether it fits the user’s scenes, body context, existing inventory, and purchase priorities. That is why the asset-aware framing is central rather than decorative.

## 8. Boundaries

This branch does not replace a stylist, an image-recognition pipeline, or a virtual try-on product. It also does not claim benchmark leadership. Its claim is narrower: AKM can be implemented as a profile-first wardrobe-decision system whose outputs stay closer to the user’s actual wardrobe reality.

When inputs are incomplete, the correct behavior is constrained output and gap exposure rather than artificial certainty.

## 9. Conclusion

The fashion branch matters because it shows how AKM can convert styling from generic commentary into asset-aware and scene-constrained decision making. The contribution is methodological. It demonstrates that better upstream modeling changes not only what the system says, but what kind of recommendation becomes possible.

## References

[1] Lu, Z., Hu, Y., Jiang, Y., Chen, Y., & Zeng, B. (2019). *Learning Binary Code for Personalized Fashion Recommendation*. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2019.

[2] Kang, W.-C., Kim, E., Leskovec, J., Rosenberg, C., & McAuley, J. (2019). *Complete the Look: Scene-Based Complementary Product Recommendation*. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2019.

[3] Lu, Z., Jiang, Y., Hu, Y., Chen, Y., & Zeng, B. (2021). *Personalized Outfit Recommendation with Learnable Anchors*. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2021.

[4] Sarkar, R., Bodla, N., Vasileva, M., Lin, Y.-L., Beniwal, A., Lu, A., & Medioni, G. (2022). *OutfitTransformer: Outfit Representations for Fashion Recommendation*. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), 2022.

[5] Li, L., Zhang, Y., & Chen, L. (2021). *Personalized Transformer for Explainable Recommendation*. Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics (ACL), 2021.

[6] Cheng, H., Wang, S., Lu, W., Zhang, W., Zhou, M., Lu, K., & Liao, H. (2023). *Explainable Recommendation with Personalized Review Retrieval and Aspect Learning*. Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL), 2023.

[7] Hsiao, W.-L., & Grauman, K. (2018). *Creating Capsule Wardrobes from Fashion Images*. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2018.