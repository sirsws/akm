<!--
文件：akm-homepage-and-demo-plan-2026-05-02.md
核心功能：给出 AKM 母港首屏改写句、已完成的 DeepSeek synthetic-profile 测试结果、开源 benchmark 包装与投稿级 evaluation 扩展方案。
输入：AKM/DaE/Fitness/Fashion 现有资产、SSRN 拒稿反馈、第 10-13 轮顾问讨论、DeepSeek API 实测结果、用户对隐私与测试边界的约束。
输出：可直接执行的 GitHub 首屏文案、发布前 demo 说明、AKM-Benchmark-Toolkit v0.2 包装方案、akm_elicited 实测结果与投稿扩展触发条件。
-->

# AKM 首屏改写与案例测试方案

## 0. 当前定位校准

AKM 不是记忆工具。

AKM 要解决的是更早一层的问题：在智能体开始执行任务前，主动发掘用户的目标、约束、偏好、风险边界、资源条件与决策风格，并把这些信息整理成可注入的 profile。

因此外部表达必须避开“让 AI 不失忆”这种容易落入 memory / RAG / long-term storage 赛道的说法。可以借“Context Engineering 上游”解释，但主品类不应叫 memory，不应叫 RAG，也不应被描述成上下文压缩工具。

建议主品类：

**Agent Profile Elicitation**

中文：

**智能体用户画像诱导协议**

更完整的学术/论文表述：

**Pre-task Agent Profile Elicitation for User-Aligned AI Agents**

中文：

**面向用户对齐智能体的任务前用户画像诱导方法**

## 1. GitHub 首屏句子

### 1.1 英文首屏主句

建议替换 README 首屏当前的长句为：

```text
Your agent has profile slots. They are empty.
AKM is a structured protocol for filling them before the agent starts working, not after it gets things wrong.
```

### 1.2 英文扩展句

```text
Active Knowledge Modeling (AKM) is a pre-task profile elicitation method for user-aligned AI agents. It actively uncovers a user's goals, constraints, preferences, risks, assets, and decision style, then turns that knowledge into structured context for downstream agents.
```

### 1.3 中文首屏主句

```text
GPTs、Gems 和各类智能体已经有 instructions、memory、profile 等上下文承载面。
AKM 解决的是：智能体开始工作前，这些位置里到底该放什么，以及这些内容如何被主动发掘出来。
```

### 1.4 中文扩展句

```text
主动知识建模（AKM）是一套任务前用户画像诱导方法。它主动发掘用户目标、约束、偏好、风险边界、资产条件与决策风格，并把这些信息转化为可注入下游智能体的结构化上下文。
```

### 1.5 首屏警戒线

不要在首屏使用这些表述：

- “AKM makes agents remember you better”
- “AKM is a memory framework”
- “AKM is RAG for user profiles”
- “AKM is a prompt collection”
- “AKM is a new paradigm” 作为第一句

可以在第二屏或论文区解释 paradigm，但首屏必须先让开发者看到工程缺口。

## 2. 传播版案例：2 组 DeepSeek before/after demo

传播版 demo 的目标不是证明普遍有效，而是让读者快速看见 AKM 与普通 prompt 的差别。

当前已完成 10 个 synthetic profiles 的 DeepSeek 测试，三组条件为：

1. `no_profile`：只给任务；
2. `unstructured_notes`：给自然语言碎片；
3. `akm_profile`：给 AKM 结构化画像。

结果摘要：

| Condition | Total | Constraint | Risk | Specificity | Actionability | Fit | Trade-off |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| no_profile | 12.1 | 1.6 | 2.5 | 2.6 | 2.8 | 1.5 | 1.1 |
| unstructured_notes | 24.7 | 4.5 | 4.6 | 4.2 | 4.5 | 4.2 | 2.7 |
| akm_profile | 30.0 | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 |

证据计数：

| Condition | Satisfied constraints | Missed constraints | Risk violations | Profile details used |
| --- | ---: | ---: | ---: | ---: |
| no_profile | 0.8 | 3.2 | 1.1 | 2.1 |
| unstructured_notes | 3.7 | 0.3 | 0.0 | 4.9 |
| akm_profile | 4.0 | 0.0 | 0.0 | 6.2 |

盲评中，AKM 组在 10 个 profiles 中有 7 个被明确标为最佳答案；其余样本仍在分项总分上保持 AKM 最高。完整结果见：

- `experiments/synthetic_profile_eval/results/summary.md`
- `experiments/synthetic_profile_eval/results/summary.json`

### 2.1 Demo A：冷启动画像诱导

目的：证明 AKM 补的是“任务前主动发掘”，不是记忆。

场景：

一个合成用户第一次使用“职业/创业顾问智能体”。用户只说：“我想让 AI 帮我规划下一阶段工作重心。”

Baseline agent：

- 直接回答；
- 或只问一个泛泛的问题；
- 输出容易变成通用建议。

AKM agent：

- 先走一轮结构化 elicitation；
- 主动问目标、资源、约束、风险、偏好、不可做事项；
- 形成 `UserProfile`；
- 再基于 profile 给建议。

展示格式应以真实输出和对话流为主：

1. 先展示 `no_profile` 如何给出泛化建议；
2. 再展示 `unstructured_notes` 如何部分命中约束；
3. 最后展示 `akm_profile` 如何系统引用目标、硬约束、资源、风险边界和决策风格；
4. 表格只作为摘要，不替代原始输出。

### 2.2 Demo B：约束命中率对比

目的：证明 AKM 提升的是“约束命中与风险边界”，不是语气模仿。

场景：

一个合成健身用户，具有多重但不过度医学化的约束：

- 每周可训练时间：3 次，每次 35 分钟；
- 器械：哑铃、弹力带、跑步机；
- 目标：减脂、保持肌肉、改善体态；
- 旧伤：膝盖不适，避免高冲击跳跃；
- 偏好：讨厌复杂动作，不喜欢长时间有氧；
- 风险边界：不能推荐大重量深蹲、跳箱、极端节食。

任务：

```text
请给这个用户制定一周训练建议。
```

no_profile：

只给任务，不给 profile。

unstructured_notes：

给自然语言碎片，不提供结构化画像。

akm_profile：

给完整 `FitnessProfile` 后再生成建议。

评分表：

| 硬约束 | no_profile | unstructured_notes | akm_profile |
| --- | --- | --- | --- |
| 每周 3 次 | 部分偏离 | 命中 | 命中 |
| 每次 35 分钟 | 偏离 | 基本命中 | 命中 |
| 避免高冲击跳跃 | 违反 | 命中 | 命中 |
| 只使用现有器械 | 不确定 | 基本命中 | 命中 |
| 不推荐极端节食 | 基本命中 | 命中 | 命中 |
| 不推荐大重量深蹲/跳箱 | 违反或模糊 | 部分命中 | 命中 |

核心指标：

```text
constraint_hit_rate = 命中的硬约束数量 / 硬约束总数
risk_violation_count = 违反禁忌约束的次数
```

## 3. 后续实验：从结构化输入测试升级到协议价值测试

当前 10 组测试已经能支撑公众号传播，但还不能直接支撑“AKM elicitation 协议本身有效”的论文主张。

原因很简单：

- 当前 `akm_profile` 是预先写好的结构化 JSON；
- 下游任务直接注入这个 JSON；
- 因此当前实验主要证明的是“结构化用户画像比自然语言碎片更利于模型命中约束”；
- 这对工程传播有价值，但对论文审查还不够。

所以，下一步不是立刻扩到 30 组。

下一步应先补一个 `akm_elicited` 条件，用 10 个 profiles 验证协议链路是否成立。

### 3.1 研究问题

```text
Does AKM elicitation produce profile context that improves constraint adherence, risk control, and trade-off awareness in downstream AI advice?
```

中文：

```text
AKM 诱导协议产生的用户画像，是否能改善下游 AI 建议中的约束命中、风险控制和取舍意识？
```

### 3.2 当前最小测试结果

当前已完成 10 个 synthetic profiles 的最小测试。它是传播级 proof-of-concept，不是最终论文证据。结论：

- `akm_profile` 总分 30.0；
- `unstructured_notes` 总分 24.7；
- `no_profile` 总分 12.1；
- `akm_profile` 在约束命中、风险控制、具体性、可执行性、个人贴合和取舍意识上均为最高。

边界：

- 不在公开文章里强调“满分”；
- 不把 10 组结果包装成最终证明；
- 不声称真人满意度、健身效果或普遍个性化能力；
- 不直接拿当前结果重投 SSRN/arXiv。

真正有信息量的差距是：

```text
unstructured_notes 的 trade-off awareness = 2.7
akm_profile 的 trade-off awareness = 5.0
```

这说明自然语言碎片能告诉 AI “用户想要什么”，但对“用户愿意放弃什么、不能碰什么、如何取舍”的表达不足。AKM 的 `risk_boundaries` 与 `decision_style` 字段正好补这个缺口。

### 3.3 新增条件：akm_elicited

新增一个条件：

```text
akm_elicited
```

含义：

1. LLM 扮演 synthetic user；
2. 另一个 LLM 按 AKM elicitation 问题序列进行一轮对话；
3. 从对话中抽取 `UserProfile`；
4. 用这个 profile 跑同一个下游任务；
5. 与 `akm_profile` 直接注入预写 JSON 的结果对比。

它回答的问题不是“结构化输入是否更好”。

它回答的是：

```text
AKM 的对话发掘过程，是否能产生足够完整、足够可用的 profile？
```

如果 `akm_elicited` 接近 `akm_profile`：

- 说明 AKM 协议能把用户碎片稳定转成 agent-ready profile；
- 论文叙事可以写成“AKM 作为任务前画像生成协议有效”。

如果 `akm_elicited` 明显弱于 `akm_profile`：

- 说明协议问题序列还要改；
- 暂停投稿扩展，先修 protocol。

如果 `akm_elicited` 与 `unstructured_notes` 差不多：

- 说明当前 AKM 的核心价值还停留在“结构化整理示范”；
- 不应急着重投论文。

### 3.4 推荐四种生成条件

最终投稿级实验建议使用四组：

1. `no_profile`：只给任务；
2. `unstructured_notes`：给自然语言碎片；
3. `akm_profile`：给预写结构化 AKM profile；
4. `akm_elicited`：经 AKM 对话协议自动生成 profile 后再回答。

第 3 组是理想上限。

第 4 组才是 AKM 协议本身的关键证据。

### 3.5 扩展样本规模

扩展顺序：

- 先在 10 个 profiles 上补 `akm_elicited`；
- 如果方向成立，再扩到 30 个 synthetic profiles；
- 60 个 profiles 只在准备更严肃投稿时考虑；
- 100 个 profiles 当前没有必要。

### 3.6 场景分布

建议 6 类场景，每类 5-10 个 synthetic profiles：

1. 职业/创业决策
2. 健身训练
3. 穿搭/形象决策
4. 学习规划
5. 投资/估值辅助
6. 健康生活方式管理（不做医学疗效声明）

### 3.7 每个 profile 的结构

```json
{
  "profile_id": "fitness_001",
  "domain": "fitness",
  "goals": ["fat loss", "maintain muscle"],
  "hard_constraints": [
    "train 3 times per week",
    "35 minutes per session",
    "avoid high-impact jumping"
  ],
  "soft_preferences": [
    "simple movements",
    "dislikes long cardio"
  ],
  "available_assets": [
    "dumbbells",
    "resistance bands",
    "treadmill"
  ],
  "risk_boundaries": [
    "no extreme dieting",
    "no heavy barbell squats"
  ],
  "decision_style": "pragmatic, low-friction, consistency-first",
  "task": "Create a weekly training plan."
}
```

### 3.8 三种已完成生成条件

no_profile：

```text
You are a helpful AI assistant. Answer the user's task.
Task: {task}
```

unstructured_notes：

```text
You are a helpful AI assistant. Use the user's natural-language notes if relevant.
User notes:
{unstructured_notes}
Task:
{task}
```

akm_profile：

```text
You are a user-aligned AI assistant. Before answering, use the provided structured user profile as binding context.
User profile:
{profile_json}
Task:
{task}
```

注意：`unstructured_notes` 不是“用户自写 profile”。它是从同一个 synthetic persona 派生出的自然语言碎片，用于测试“碎片化用户表达”与“AKM 结构化画像”的差异。

### 3.9 akm_elicited 生成流程

```text
Synthetic persona
  -> simulated user answers AKM elicitation questions
  -> extracted UserProfile
  -> downstream task answer
  -> blind judge evaluation
```

该流程需要新增三类 prompt：

```text
prompts/
  elicitation_questions.md
  simulate_user_answers.md
  extract_akm_profile.md
```

输出建议：

```text
outputs/elicitation_dialogues.jsonl
outputs/elicited_profiles.jsonl
outputs/generations.jsonl
outputs/judgments.jsonl
```

### 3.10 生成模型

建议：

- Generator：DeepSeek
- Judge 1：DeepSeek
- Judge 2：另一个模型（如果可用，GPT/Gemini/Claude 任一）

如果只用 DeepSeek，也可以做，但论文里必须写 limitation：

```text
The same model family was used for generation and judging in part of the evaluation, which may introduce model-specific bias.
```

### 3.11 盲评方式

Judge 不知道哪个输出来自 AKM。

每条记录随机打乱 A/B/C 顺序：

```json
{
  "profile_id": "fitness_001",
  "task": "...",
  "profile": {...},
  "answer_a": "...",
  "answer_b": "...",
  "judge_prompt": "Evaluate answer_a and answer_b without knowing their condition."
}
```

### 3.12 评分维度

每项 1-5 分：

1. Constraint adherence：是否命中硬约束；
2. Risk control：是否避开禁忌；
3. Specificity：是否具体；
4. Actionability：是否可执行；
5. Personal fit：是否贴合 profile；
6. Trade-off awareness：是否说明取舍。

另外加入可计算指标：

```text
hard_constraint_hit_rate
risk_violation_count
profile_reference_count
```

### 3.13 Judge prompt

```text
You are evaluating two AI-generated answers for the same user task.

Use the provided user profile only as evaluation context.
Do not assume which answer used the profile.
Score each answer from 1 to 5 on:
1. Constraint adherence
2. Risk control
3. Specificity
4. Actionability
5. Personal fit
6. Trade-off awareness

Also identify:
- hard constraints satisfied
- hard constraints missed
- risk boundaries violated
- profile details explicitly used

Return JSON only.
```

### 3.14 最小统计输出

论文里至少给：

- 平均分对比；
- 每个维度的差值；
- constraint hit rate；
- risk violation count；
- win rate：AKM 输出在多少比例样本中优于 baseline；
- `akm_elicited` 与 `akm_profile` 的差距；
- elicited profile 的字段完整度；
- judge agreement：两个 judge 是否方向一致。

### 3.15 可投论文标题

更适合 SSRN/arXiv 的标题：

```text
From User Notes to Agent-Ready Profiles: A Synthetic Evaluation of Active Knowledge Modeling
```

备选：

```text
Structured Profile Elicitation Improves Constraint Adherence: A Synthetic-Profile Evaluation Using LLM-as-Judge
```

不建议：

```text
Active Knowledge Modeling: A Proactive Paradigm...
```

这个标题仍容易被 SSRN 归入 framework。

### 3.16 论文边界声明

必须写：

```text
This study uses synthetic user profiles and LLM-as-judge evaluation. It does not claim real-user satisfaction, clinical efficacy, behavioral change, or universal personalization performance. The goal is narrower: to test whether pre-task profile elicitation improves observable constraint adherence and profile fit in generated AI advice under controlled synthetic conditions.
```

中文理解：

本文不声称真人满意度，不声称医疗/行为疗效，不声称普遍个性化性能。只检验在合成画像条件下，任务前画像诱导是否改善可观察的约束命中与画像贴合。

## 4. AKM-Benchmark-Toolkit v0.2 包装建议

当前实验目录已经可以作为 `AKM-Benchmark-Toolkit v0.2` 发布，`akm_elicited` 条件已完成 10 组实测。

但 v0.2 的定位必须诚实：

```text
This toolkit reproduces a synthetic profile evaluation comparing no profile, unstructured notes, and structured AKM profiles. It is a proof-of-concept benchmark, not a final validation of the AKM elicitation protocol.
```

现有结构：

```text
experiments/synthetic_profile_eval/
  profiles.jsonl
  prompts/
    generator_baseline.md
    generator_akm.md
    judge.md
  run_generation.py
  run_judging.py
  aggregate_results.py
  outputs/
  results/
```

v0.2 发布内容：

- `profiles.jsonl`
- `prompts/*.md`
- `run_generation.py`
- `run_judging.py`
- `aggregate_results.py`
- `outputs/generations.jsonl`
- `outputs/judgments.jsonl`
- `results/summary.md`
- `results/summary.json`

README 必须写清：

- 这是 synthetic benchmark；
- 当前四组条件已包含 `akm_elicited`；
- 当前结果适合传播和复现，不足以单独支撑学术投稿；
- 后续若重投论文，再扩展到 30 组以上并增加更严格的 judge 一致性检查。

代码约束继续保留：

- 不捕获通用异常；
- API key 从环境变量读取；
- 每次调用记录 model、temperature、prompt_hash、profile_id；
- 输出原文完整保存，不能只保存评分。

## 5. 公众号文章与论文的关系

公众号文章只需要展示 2 组传播版 demo。

论文重投不是直接扩样本；先补 10 组 `akm_elicited`，结果成立后再考虑 30-60 组 synthetic profiles。

不要把公众号文章写成论文摘要；也不要把论文写成公众号故事。

分工：

| 载体 | 目的 | 样本量 | 语言 |
| --- | --- | --- | --- |
| GitHub 首屏 | 让开发者秒懂缺口 | 无 | 英文为主 |
| 公众号 | 让非专业读者看见 before/after | 2 组 | 中文 |
| SSRN/arXiv 重投 | 可复现研究 | 先 10 组 `akm_elicited`，成立后再扩 30-60 组 | 英文 |
| Issue 寄生投放 | 精准触达构建者 | 针对具体问题 | 中英按场景 |

## 6. 最小执行顺序

1. 修改 GitHub README 首屏句。
2. 公众号文章补 Demo A 对话流和 fitness_001 原始输出。
3. 发布 `AKM-Benchmark-Toolkit v0.2`，附带当前代码、四组条件和结果。
4. 根据 `akm_elicited` 结果决定是否扩到 30 组。
6. 若扩展结果显著，再改写论文并重投。

## 7. 投稿判断

只补几组 demo，不足以重新冲 SSRN/arXiv。

`akm_elicited` 先跑出差距，再扩展 synthetic profiles + 盲评 + 评分表 + 可复现数据，才有机会把稿件从 framework 拉到 study。

但前提是先完成 `akm_elicited` 条件。

没有 `akm_elicited`，论文只能主张“结构化用户画像有益”；有 `akm_elicited`，才有机会主张“AKM 协议能产生可用画像”。

但仍有风险：

- SSRN 当前明确通常不收 framework，且对 AI 内容审查收紧；
- arXiv 对 AI 相关文章也可能卡在“是否为 refereeable scientific contribution”；
- LLM-as-judge 会被质疑主观性；
- synthetic profiles 会被质疑外部效度。

所以重投策略应是：

先发布 v0.2 开源实验包。当前 `akm_elicited` 相对 `unstructured_notes` 已出现明显提升，可进入 30 组扩展评估；是否重投仍取决于扩展后结果、judge 一致性与论文叙事收束。
