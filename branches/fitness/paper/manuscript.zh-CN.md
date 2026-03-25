<!--
文件：manuscript.zh-CN.md
核心功能：作为 Fitness 分支论文的中文 markdown 稿，说明 AKM 如何在真实约束下把健身规划重写成画像优先的决策系统，并明确其对主流平台上下文槽位的上游方法论补位。
输入：健身工作区本地设计记录、训练日志、结构化状态记录与外部训练负荷/自适应训练文献。
输出：供人工审阅后再转 LaTeX 的中文论文草稿。
-->

# Profile-First Fitness Planning Under Real Constraints: An AKM Branch Paper

## 摘要

本文讨论 `Active Knowledge Modeling (AKM)` 如何在真实健身约束下发挥作用。系统不是先生成训练计划，再去补限制条件；它会先建模目标排序、身体限制、器械现实、时间预算、恢复不确定性和执行风险，然后才给出训练决策。本文的贡献是方法论层面的：它展示了 AKM 如何把“健身 prompt”改写成“画像优先的决策设计”。

## 1. 引言

OpenClaw、ChatGPT、Gemini 这类平台已经暴露出 `user-context` 或 system-prompt 字段，但很少给出一套严肃的状态构建方法，告诉用户这些字段里到底该放什么。健身建议把这个缺口暴露得尤其明显：泛化计划往往默认目标稳定、动作能力健康、恢复可靠、器械可替换，但真实用户并不生活在这些假设里。

因此，问题首先出在上游。如果训练决策取决于身体状态、恢复情况、时间预算和器械可达性，那么系统就不该先给计划，而应先建立一个关于“当前到底能推进什么”的模型。

## 2. 问题定义

当上游上下文不足时，普通健身 prompting 会出现一组稳定失真：

- 旧伤或疼痛信号被压平成普通训练前提
- 器械限制被当成细节而不是决定因素
- 时间预算被当成可调变量，哪怕它其实是硬约束
- 恢复不确定性被训练分化模板直接覆盖
- 关键状态变量缺失时，系统仍假装自己有信心

这些失真与训练负荷监测、自适应训练、依从性研究的共通结论一致：训练质量取决于负荷、准备状态与场景条件之间的互动，而不是单靠一个固定模板 [1]-[4]。

## 3. 方法：Fitness 场景中的 AKM

在健身场景中，AKM 建模的不是抽象身份，而是训练可行性。
关键上游状态包括：

- 目标排序
- 旧伤与动作限制
- 可用器械
- 每周训练频率
- 单次时长预算
- 恢复状态
- 执行风险与依从性风险

这个分支以三层工作流实现。

### 3.1 Elicitation

系统先问清楚“什么样的训练决策才合法”，而不是立刻给训练单。它会先澄清目标层级、身体限制、器械现实、周节奏和恢复相关信息。

### 3.2 Structured Record

挖出的信息会被转成持久的上游状态。在这个分支里，这层状态通过指标快照、器械记录、追加式日志和月度总结来维护。

### 3.3 Execution Decision

只有在画像和近期状态都具备后，系统才产出训练决策。输出契约包括：

- `StateJudgment`
- `PrimaryDecision`
- `DecisionConfidence`
- `Plan`
- `RiskNotes`
- `NonNegotiables`
- `MissingInputs`

缺失信息本身会进入输出，而不是被流畅语言遮蔽掉。

## 4. 设计记录

这个分支的本地设计记录列在 [local-evidence.md](./local-evidence.md) 中，主要包括：

- 硬规则
- 身体指标记录
- 器械语境记录
- 日级决策文件
- 追加式执行日志
- 月度复盘记录

这些记录不是被拿来宣称广义疗效，而是用来让工作流行为变得可见。下面展示一个代表性决策样本。

```json
{
  "StateJudgment": "Recovery state partially unclear; lower-back risk remains a live constraint.",
  "PrimaryDecision": "Do not assign heavy compound lifting today. Use a lower-risk session or pause pending clarification.",
  "DecisionConfidence": "Low",
  "Plan": [
    "Confirm current lumbar discomfort level and sleep quality before loading decisions.",
    "If discomfort is elevated, switch to mobility, light accessories, and walking.",
    "If discomfort is low and recovery is acceptable, resume with conservative volume only."
  ],
  "RiskNotes": [
    "Generic split logic is not sufficient under unresolved recovery and injury uncertainty.",
    "The main failure mode is acting as if readiness were already known."
  ],
  "NonNegotiables": [
    "No heavy axial loading until state is clarified.",
    "Do not infer readiness from schedule alone."
  ],
  "MissingInputs": [
    "Current lumbar discomfort score (1-10)",
    "Previous session load and residual soreness",
    "Sleep and recovery status over the last 24 hours"
  ]
}
```

这个样本展示的是“不确定条件下工作流如何表现”，不是治疗结果证明。

## 5. 讨论

AKM 在健身场景中的主要价值，是**约束保真**。它压制了 agent 把所有健身问题都当成泛化编程题来答的冲动。

这很重要，因为真实用户的生活由时间波动、酸痛、器械限制、旧伤和恢复不稳定组成。忽略这些变量的系统，看起来可能更自信，但会制造更多下游摩擦。先把这些变量建模进去的系统，虽然答案更窄，却更可执行。

## 6. 边界

这不是医学论文。
这个分支不替代医生、康复师或线下教练。
它的主张更窄：AKM 可以被实现为一个高约束训练环境中的画像优先规划系统。

## 7. 结论

Fitness 分支的重要性在于，它展示了 AKM 如何把“生成训练单”改写为“基于用户状态、约束和显式不确定性的决策过程”。它的贡献是方法论的：在高约束场景里，更好的上游建模可能比更漂亮的下游措辞更重要。

## 参考文献

[1] Foster, C., Rodriguez-Marroyo, J. A., & de Koning, J. J. (2017). *Monitoring Training Loads: The Past, the Present, and the Future*. International Journal of Sports Physiology and Performance, 12(S2), S2-2-S2-8. DOI: 10.1123/ijspp.2016-0388.

[2] Shattock, K., & Tee, J. C. (2022). *Autoregulation in Resistance Training: A Comparison of Subjective Versus Objective Methods*. Journal of Strength and Conditioning Research, 36(3), 641-648. DOI: 10.1519/JSC.0000000000003530.

[3] Haddad, M., Stylianides, G., Djaoui, L., Dellal, A., & Chamari, K. (2017). *Session-RPE Method for Training Load Monitoring: Validity, Ecological Usefulness, and Influencing Factors*. Frontiers in Neuroscience, 11, 612. DOI: 10.3389/fnins.2017.00612.

[4] Fuente-Vidal, A., Guerra-Balic, M., Roda-Noguera, O., Jerez-Roig, J., & Montane, J. (2022). *Adherence to eHealth-Delivered Exercise in Adults with no Specific Health Conditions: A Scoping Review on a Conceptual Challenge*. International Journal of Environmental Research and Public Health, 19(16), 10214. DOI: 10.3390/ijerph191610214.


