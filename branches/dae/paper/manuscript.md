<!--
文件：manuscript.md
核心功能：作为 DaE 分支论文的英文 markdown 稿，尽量贴近原始 DaE 论文线而不是仅作 AKM 摘要。
输入：DaE 的 SSRN 版本、arXiv 风格稿、AKM 与 DaE 的当前仓库关系。
输出：供 GitHub 阅读的 DaE 论文 markdown 版，保留原论文问题意识、理论框架与机制设计结构。
-->

# Reducing Alignment Debt in AI Advisory: The Dialogue-as-Elicitation Approach

*This markdown manuscript aligns with the original DaE paper line. Two public variants exist in parallel: the arXiv-style draft, **Dialogue as Elicitation: Building High-Fidelity Personas for Personalized AI Advisors with LLMs**, and the SSRN version under the title above.*

## Abstract

In AI advisory, the main bottleneck is often not raw model capability but alignment transfer. Users typically carry tacit preferences, constraints, goals, and strategic tradeoffs that are expensive to communicate through ad-hoc prompting. This creates alignment debt: repeated correction effort, avoidable friction, and weak personalization in early interactions.

Dialogue-as-Elicitation (DaE) addresses this problem by treating persona construction as an explicit elicitation mechanism rather than as hidden pre-work. The method uses a dual-agent logic and a four-stage pipeline to build a reusable `PersonaProfile` as a personal strategic asset. Instead of paying alignment cost repeatedly in downstream sessions, the user invests in an upstream asset that can be reused across advisory tasks.

The DaE contribution is therefore not just a prompt pattern. It is a mechanism for turning scattered, high-noise user context into a structured, durable, and transferable alignment asset.

## 1. Introduction: The Economics of Alignment

Large language models have lowered the cost of prediction, drafting, and synthesis. They have not eliminated the cost of alignment. In advisory settings, users still spend substantial effort restating context, correcting weak assumptions, and repairing generic outputs.

This recurring cost can be understood as **alignment debt**: the cumulative time, cognitive load, and friction required to make an AI system work in accordance with a specific user rather than an abstract average user.

The root problem is usually upstream. The AI does not begin with a sufficiently rich model of the principal it is supposed to serve. Many users cannot fully articulate their own values, constraints, and priorities in one pass. Much of the relevant information is sticky, tacit, and distributed across memory, habit, contradiction, and unfinished reflection.

DaE starts from a different premise: for high-level advisory work, dialogue itself can be designed as an active elicitation process whose product is not merely an answer, but a reusable user asset.

## 2. Theoretical Framework

### 2.1 The Principal-Agent Problem in AI Advisory

AI advisory contains a principal-agent problem. The principal is the user. The agent is the model or advisory system. The failure is often not malicious divergence but information asymmetry. The agent lacks access to the user’s real utility function, hidden constraints, and tradeoff logic, so it defaults to generic or misaligned advice.

### 2.2 Bounded Rationality and Sticky Information

Users do not hold a complete, ready-to-export specification of themselves. Their rationality is bounded, and much of their need-relevant information is sticky. It is expensive to compress into a single prompt, especially when the information includes conflict, ambivalence, and long-horizon preference structure.

DaE treats this not as a user failure but as a mechanism-design problem. The system should scaffold the externalization of sticky information rather than demand that the user perform perfect self-serialization in one shot.

### 2.3 From Prompt Flow to Asset Stock

Under ad-hoc prompting, user effort behaves like a flow variable. Context is spent and then disappears with session turnover. Under DaE, the goal is to convert that effort into a stock variable: a `PersonaProfile` that accumulates value over time and can be reused across agents and tasks.

This shift matters because long-term advisory quality depends less on any single answer than on the continuity of aligned context.

## 3. The DaE Mechanism Design

### 3.1 Core Asset: PersonaProfile

DaE produces a structured `PersonaProfile` rather than an unstructured conversational impression. Typical fields include:

- `Background`
- `Capabilities`
- `Resources`
- `Values / Drives`
- `Constraints`
- `Goals`
- `Weaknesses and Patterns`
- `Challenges and Uncertainties`
- `Strategic Paths`

The point of the profile is operational reuse. It is meant to be handed to downstream advisors, planners, writers, or agents as a stable context layer.

### 3.2 Dual-Agent Logic

DaE conceptually separates two roles:

- an **Elicitation Agent**, responsible for collection, contradiction surfacing, and refinement
- an **Application Agent**, responsible for downstream advice using the completed profile

This separation matters because learning the user and serving the user are related but distinct tasks. DaE treats user modeling as a specialized upstream phase rather than a side effect of later advisory work.

### 3.3 Four-Stage Pipeline

DaE follows a four-stage process.

1. **Asset Collection**
   The user provides an initial self-portrait covering background, skills, resources, constraints, goals, values, weaknesses, and current uncertainty.

2. **Dialectical Audit**
   The system identifies vague abstractions, hidden contradictions, and unstable priorities, often through Socratic questioning.

3. **Asset Refinement**
   Raw user language is rewritten into clearer, reusable profile statements.

4. **Strategic Pathfinding**
   The profile is used to generate initial strategic paths, not only to provide advice but also to test whether the asset is decision-relevant.

This sequence converts noisy autobiographical material into a sharper advisory substrate.

## 4. Comparative Framework Analysis

DaE is best understood in contrast with ordinary ad-hoc prompting.

### 4.1 Information Structure

Ad-hoc prompting starts from high-noise, session-local context. DaE enforces structure through an explicit schema and iterative clarification.

### 4.2 Cognitive Load Allocation

Ad-hoc prompting keeps most alignment burden on the user. DaE shifts more of that burden to the elicitation procedure by scaffolding recall, contradiction detection, and refinement.

### 4.3 Asset Nature

Ad-hoc prompting produces disposable session context. DaE aims to build cumulative personal capital.

### 4.4 Alignment Mode

Ad-hoc prompting relies on ex-post correction. DaE emphasizes ex-ante elicitation. The goal is to prevent low-quality alignment before downstream recommendations are generated.

## 5. Preliminary Evidence and Practical Usefulness

The original DaE paper line includes preliminary evaluation and practical framing.
The arXiv-style draft presents a small user study in which participants compared DaE-generated personas with baseline self-written profiles for initializing a long-term advisor. The reported direction of the results was favorable to DaE on perceived coverage, accuracy, and preference for downstream use.

The SSRN version sharpens the argument in economic and mechanism-design terms. Its central claim is that DaE lowers the transaction cost of human-AI collaboration by turning repeated corrective effort into an up-front alignment asset.

The evidence should be read as early-stage but real: DaE is not yet a universal evaluation benchmark, but it is more than a rhetorical prompt idea. It has a coherent mechanism, an explicit asset model, public release artifacts, and real-world reuse logic.

## 6. Position Within AKM

Within the current repository structure, AKM serves as the mother-hub framework and DaE is the first complete reference implementation in the persona-aware advisory scene.

That relationship should not erase the original identity of the DaE paper line. Historically and intellectually, DaE developed as a standalone research line with its own titles, framing, and evidence claims. AKM now provides the broader umbrella under which that line is organized.

## 7. Conclusion

DaE matters because it reframes alignment in AI advisory as an upstream elicitation and asset-construction problem.
Instead of repeatedly repairing weak prompts and generic outputs, the user builds a structured, reusable alignment asset that can travel across advisors and over time.

That is why the DaE contribution is more substantial than a better interview prompt. It is a mechanism for reducing alignment debt by improving the information supply chain between human principals and AI agents.