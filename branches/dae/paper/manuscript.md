<!--
文件：manuscript.md
核心功能：作为 DaE 分支论文的英文 markdown 稿，保留原始 DaE 论文线的研究主轴，同时说明它与 AKM 母框架的关系。
输入：DaE 原始 SSRN / arXiv 论文线、AKM 母港结构与旧研究仓链接。
输出：供 GitHub 阅读和后续论文整理使用的英文稿。
-->

# Reducing Alignment Debt in AI Advisory: The Dialogue-as-Elicitation Approach

*This markdown manuscript stays close to the original DaE paper line. A parallel arXiv-style draft also exists under the title **Dialogue as Elicitation: Building High-Fidelity Personas for Personalized AI Advisors with LLMs**.*

## Abstract

In AI advisory, the main bottleneck is often not raw model capability but alignment transfer. Users carry tacit goals, constraints, values, and strategic tradeoffs that are expensive to communicate through ad-hoc prompting. This creates alignment debt: repeated correction effort, avoidable friction, and weak personalization in early interactions.

Dialogue-as-Elicitation (DaE) addresses this problem by treating persona construction as an explicit elicitation mechanism rather than hidden pre-work. The method builds a reusable `PersonaProfile` as a personal strategic asset. Instead of paying alignment cost repeatedly in downstream sessions, the user invests in an upstream asset that can be reused across advisory tasks.

## 1. Introduction

Many AI platforms already provide persistent context surfaces for user and agent state. OpenClaw makes this especially explicit through injected workspace files and context reconstruction, while ChatGPT and Gemini expose their own forms of reusable context entry. What these platforms rarely provide is a disciplined method for eliciting, structuring, updating, and reusing the state that should populate those surfaces. In advisory settings, the result is familiar: users restate background, goals, and constraints in every new session, while the system repeatedly falls back to generic advice.

This recurring cost can be understood as **alignment debt**: the cumulative time, cognitive load, and friction required to make an AI system work in accordance with a specific user rather than an abstract average user.

DaE starts from a different premise. In high-level advisory work, dialogue itself can be designed as an active elicitation process whose product is not merely an answer, but a reusable user asset.

## 2. Theoretical Framework

### 2.1 The Principal-Agent Problem in AI Advisory

AI advisory contains a principal-agent problem. The principal is the user. The agent is the model or advisory system. The failure is often not malicious divergence but information asymmetry. The agent lacks access to the user's real utility function, hidden constraints, and tradeoff logic, so it defaults to generic or weakly aligned advice.

### 2.2 Bounded Rationality and Sticky Information

Users do not hold a complete, ready-to-export specification of themselves. Their rationality is bounded, and much of their need-relevant information is sticky. It is expensive to compress into a single prompt, especially when the information includes conflict, ambivalence, and long-horizon preference structure.

DaE treats this not as a user failure but as a mechanism-design problem. The system should scaffold the externalization of sticky information rather than demand perfect self-serialization in one shot.

### 2.3 From Prompt Flow to Asset Stock

Under ad-hoc prompting, user effort behaves like a flow variable. Context is spent and then disappears with session turnover. Under DaE, the goal is to convert that effort into a stock variable: a `PersonaProfile` that accumulates value over time and can be reused across agents and tasks.

## 3. The DaE Mechanism Design

### 3.1 Core Asset: PersonaProfile

DaE produces a structured `PersonaProfile` rather than an unstructured conversational impression. Typical fields include:

- `Background`
- `Capabilities`
- `Resources`
- `Constraints`
- `Goals`
- `DecisionStyle`
- `Weaknesses`
- `Challenges`
- `Lessons`
- `AlignmentCheck`

The point of the profile is operational reuse. It is meant to be handed to downstream advisors, planners, writers, or agents as a stable context layer.

### 3.2 Dual-Agent Logic

DaE conceptually separates two roles:

- an **Elicitation Agent**, responsible for collection, contradiction surfacing, and refinement
- an **Application Agent**, responsible for downstream advice using the completed profile

This separation matters because learning the user and serving the user are related but distinct tasks.

### 3.3 Four-Stage Pipeline

1. **Asset Collection**
2. **Dialectical Audit**
3. **Asset Refinement**
4. **Strategic Pathfinding**

The sequence converts noisy autobiographical material into a reusable advisory substrate.

## 4. Comparative Analysis

Compared with ordinary ad-hoc prompting, DaE changes four things:

- **information structure:** it enforces schema and clarification instead of session-local ambiguity
- **cognitive load allocation:** it shifts more alignment burden from the user to the elicitation workflow
- **asset nature:** it produces cumulative profile capital rather than disposable context
- **alignment mode:** it emphasizes ex-ante elicitation instead of endless ex-post correction

## 5. Practical Significance

The DaE contribution is not just a better interview prompt. It is a mechanism for turning scattered, high-noise user context into a structured, durable, and transferable alignment asset.

That matters because long-term advisory quality depends less on any single answer than on whether downstream agents start from an adequate model of the principal they serve.

## 6. Relationship to AKM

Within the current repository structure, AKM serves as the parent framework and DaE is its first complete reference implementation in persona-aware advisory work.

That repository relationship should not erase the original identity of the DaE paper line. Historically and intellectually, DaE developed as a standalone research line with its own titles, framing, and evidence claims. AKM now provides the broader umbrella under which that line is organized.

## 7. Conclusion

DaE reframes alignment in AI advisory as an upstream elicitation and asset-construction problem. Instead of repeatedly repairing weak prompts and generic outputs, the user builds a structured alignment asset that can travel across advisors and over time.

That is why DaE remains more substantial than a prompt pattern. It is an operational method for reducing alignment debt by improving the information supply chain between human principals and AI agents.

