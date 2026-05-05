<!--
文件：akm-journal-feasibility-memo-2026-05-05.md
核心功能：S3 期刊可行性 memo —— 在 v1.1 supplement 已落盘的前提下，评估 AKM 是否值得投中档 SCI 期刊；如投，应投哪一刊、工时上限、外部信号检查、撤稿熔断器。
        本 memo 的输出是一个二选一决策：投 / 不投，附依据。不是「再讨论一轮」。
输入：v1.1 supplement (5/5 generators, +14.56~+19.81 lift, α≥0.85)；3 候选刊 (KBS / ESWA / TMLR) 公开文档；近 12 个月 LLM personalization / synthetic-persona / LLM-as-judge 接收先例；19 轮共识 (S3 memo 立项 + 止损纪律)。
输出：一句话结论 + 投刊次序 + 硬熔断器。供 Gemini/DS/GPT/Kimi/GLM/MiniMax 在讨论板批注。
维护要求：本 memo 一旦决策「投」，SSRN/arXiv 公开 URL 出来当天必须重新跑一遍「外部信号检查」并更新；任一熔断器触发立即归档此 memo。
-->

# AKM 期刊可行性 memo（S3）

> **日期**：2026-05-05
> **作者**：Claude（顾问，主笔）
> **审稿对象**：邵先生（拍板）+ 战略顾问团（ChatGPT / Gemini / DeepSeek / Kimi / GLM / MiniMax）
> **决策性质**：**二选一**——投 / 不投。不是「再讨论一轮」。

---

## TL;DR（30 秒读完版）

**结论**：**S2 完成后，期刊线从「不该投」翻转为「值得有条件投」。建议优先投 TMLR（首选），KBS 备选，ESWA 不投。**

**核心依据**：v1.1 实测数据（5/5 generator AKM lift +14.56~+19.81，α≥0.85，0 mismatch）+ TMLR 明确接受 "claims supported by accurate evidence"，**不要求 novelty / SOTA / 真人**。

**硬熔断器**：
- TMLR 评审若索要真人 / N>200 / 重设 rubric → 撤稿不修
- 工时硬顶 25h，超即归档
- 若 6 周内未送审 → 归档，转维护模式
- 若 SSRN/arXiv 30 天后无任何外部信号（star/issue/被引）→ memo 失效，重评

---

## 1. v1.1 完成后的形势变化

19 轮辩论时，三人触发条件全部基于 **v1.0 单 generator 已知硬伤**。19 轮 Claude（我）的判断是「合稿 25-35h、desk-reject 高、不值得」。**S2 落地后，三个判断全部需要更新**：

| 19 轮判断 | v1.1 落地后实测 | 调整方向 |
|---|---|---|
| 「单 generator」是 reviewer 第一刀 | 5/5 generator 全成立 + 1 attempted-but-excluded 诚实记录 | **第一刀 已挡** |
| 「合稿 25-35h」 | 已有 4 篇 LaTeX + supplement 完整，合稿主要工作是 abstract/intro 重写 | **降到 12-18h** |
| 「中档 IF~3-9 可试」 | TMLR 明确不要求 novelty/SOTA + 同期 ICLR 2026 接收 synthetic-persona LLM-as-judge 论文 | **TMLR 比中档 IF 更适合** |

**两个意外发现**：
1. **TMLR 对此类工作的 fit 比 KBS/ESWA 都好**——审稿口径正面契合 v1.1 的「evidence-based」定位
2. **同期 ICLR/NeurIPS 接收的 LLM-as-judge + synthetic personas 工作**（Doubly-Robust LLM-as-Judge ICLR 2026、RouteJudge ICLR 2026、Personalized RewardBench）证明这条研究路径**在顶会都被认可**，AKM 投中档刊的 desk-reject 风险被高估了

---

## 2. 候选刊三选一深度对比

### 2.1 TMLR（Transactions on Machine Learning Research）

**基本信息**：
- 出版商：JMLR（机器学习领域权威）
- 性质：纯 online、open-review、双盲
- 评审周期：2-4 周一轮，可多轮
- IF：未参与 IF 排名（**JMLR 系刻意不卷 IF**），但社区认可度等同 NeurIPS/ICML 期刊版

**接收标准**（官方原文）：
> 1. Are claims supported by accurate, convincing, and clear evidence?
> 2. Would some TMLR audience members be interested in the findings?
>
> **Work is not rejected solely for lacking novelty or failing to achieve state-of-the-art benchmarks.**

**对 AKM v1.1 的契合度**：★★★★★
- v1.1 的核心主张是 evidence-based（5/5 generator + α≥0.85 + 0 mismatch verify）→ 标准 1 满足
- TMLR audience 包括 LLM-as-judge、benchmark、personalization 研究者 → 标准 2 满足
- **明确不卷 SOTA、不卷 novelty** → 我们最大的潜在风险点 (single-domain method) 被 TMLR 标准排除在 reject 理由之外

**desk-reject 风险评估**：**~15%**
- 主要风险：editor 觉得 scope 偏 application 不够 ML core
- 缓解：投稿 metadata 选 "evaluation methodology" + "language models" 两个标签
- 同期接收先例：Simula（synthetic data generation evaluation 框架）、多篇 LLM benchmark 论文

**送审后大修被卡风险**：**~20%**
- 主要风险：reviewer 索要 cross-prompt-template robustness 实验
- 应对：诚实回复"out of scope of this submission, future work"，不补
- 若 reviewer 索要真人 / N>200 → **撤稿熔断**

**预计周期**：投稿到 first decision 4-8 周，全程 8-16 周

### 2.2 KBS（Knowledge-Based Systems, Elsevier）

**基本信息**：
- IF: 7.2-7.6（2025）
- CiteScore: 15.0
- 接收率: 25%（desk-reject 30%）
- Q1 in CS-AI

**Scope 匹配点**：
- "Recommender systems and personalization" ✓（直击 AKM）
- "Intelligent decision support systems" ✓（DaE/Fitness/Fashion 都是 decision support）
- "Knowledge presentation and engineering" ✓（AKM profile 本身是 knowledge engineering）

**Scope 不匹配点**：
- KBS 偏 method + dataset + benchmark experiment，AKM 是 protocol + benchmark
- 同期接收的 LLM 论文偏 augmentation/classification，AKM 偏 elicitation methodology

**desk-reject 风险评估**：**~30%**
- 主要风险：editor 觉得 protocol-level work 不够 method novelty
- 缓解：标题强化 "A Reproducible Cross-Family LLM-as-Judge Benchmark"（已是当前标题）

**预计周期**：投稿到 first decision 8-16 周

### 2.3 ESWA（Expert Systems with Applications, Elsevier）

**基本信息**：
- IF: 7+（2024）
- 高吞吐量
- 强调 **applied AI + real-world domain application**

**Scope 匹配点**：
- 三分支（DaE/Fitness/Fashion）正好是三个 domain application
- 应用导向契合

**Scope 不匹配点**：
- ESWA 强调 **real-world application with real-world data**
- v1.1 全 synthetic personas，0 真人 → **这是 ESWA 的硬伤**

**desk-reject 风险评估**：**~55%**
- 主要风险：synthetic-only 直接被 editor 判 "not real-world enough"
- 不缓解（缓解就要做真人，违反主持人红线）

**结论**：**ESWA 不投**。

### 2.4 综合对比

| 刊 | 核心匹配度 | desk-reject 估值 | 大修被真人/N 卡的风险 | 周期 | 推荐 |
|---|:---:|:---:|:---:|:---:|:---:|
| **TMLR** | ★★★★★ | ~15% | 低（标准明确不卷 novelty） | 8-16 周 | **首选** |
| **KBS** | ★★★★ | ~30% | 中（reviewer 个人偏好） | 8-16 周 | **备选** |
| **ESWA** | ★★ | ~55% | 高（真人是隐性硬要求） | 12-20 周 | **不投** |

---

## 3. 建议执行路径

### 3.1 投稿次序

**先投 TMLR 单刊**（OpenReview 系不允许同时多投）。

如 TMLR desk-reject 或 reject → **触发熔断**：
- 若 reject 理由是"lack of novelty / not interesting enough" → KBS 改投
- 若 reject 理由是"need real users / larger N / different rubric" → **不改投，归档**

如 TMLR accept → 不再投其他刊。

### 3.2 合稿工作量分解（硬顶 25h）

基于 v1.1 已落地的 4 篇 LaTeX + supplement，合稿成 **1 篇 TMLR-ready 的"AKM Master + 3 Domain Studies"**：

| 工作 | 估时 | 说明 |
|---|---:|---|
| Abstract / Intro 重写为 TMLR 风格 | 2h | 强调 evidence-based、不卷 novelty |
| Methodology 章节统一 | 3h | 4 篇方法不一致处统一 |
| Results 章节嵌入 v1.1 supplement 数据 | 4h | 5/5 lift 表 + α 表 + GLM 反例分析 |
| Limitations & Honest Disclosure 章节 | 2h | Kimi excluded、Gemma throttled、real-user absent 全写 |
| Related Work 章节（必须钉牢同期工作） | 4h | Doubly-Robust LLM-as-Judge / RouteJudge / Personalized RewardBench / RecBench+ / Bespoke / Zheng 2023 |
| Reproducibility 章节 + 代码链接 | 1h | 已有 verify_v11.py + GitHub repo |
| LaTeX 排版 + 4 篇内容裁剪去重 | 4h | 当前 4 篇有 ~20% 重复 |
| OpenReview 投稿 + metadata | 1h | 标签、领域、关键词 |
| 自审 + verify 数字 + bib 检查 | 4h | 17 轮教训不重犯 |
| **合计** | **25h** | **硬顶** |

**这 25h 在 8 周内分摊 = 平均 3.1h/周**。在 19 轮共识的「≤2h/周」基础上略超，但 8 周一次性 sprint 后回归 1h/周维护。

### 3.3 时间线

| 时点 | 动作 | 触发 |
|---|---|---|
| **2026-05-05~05-08（W0）** | SSRN 4 篇 + arXiv 1 篇等审 / moderation | 同步 |
| **2026-05-08~05-15（W1）** | 等 SSRN/arXiv URL 到位；URL 到 → 立即更新 README + 邵看人生短讯 | URL 到位 |
| **2026-05-15~06-30（W2-W7）** | 25h 合稿 sprint（每周 4h，6 周完成） | 硬顶 |
| **2026-07-01（W8）** | 投 TMLR | 投稿 |
| **2026-07-01~08-31（W8-W16）** | TMLR 评审 | 等 |
| **第 30 天**（约 2026-06-04） | **第一次外部信号检查**（GitHub star/issue/被引） | 见 §3.4 |
| **第 60 天**（约 2026-07-04） | **第二次外部信号检查** + 投稿状态复盘 | 见 §3.4 |

### 3.4 外部信号检查清单

**目的**：避免「无人关注却继续投学术」的多巴胺陷阱。

**检查时点**：T+30 天、T+60 天（T = arXiv 公开日）。

**检查项**：
| 信号 | 阈值（T+30） | 阈值（T+60） | 不达标动作 |
|---|---:|---:|---|
| GitHub star（akm 主仓） | ≥10 | ≥30 | 不达标 1 项可继续；2 项以上不达标 → 暂缓 TMLR 投稿决策 |
| GitHub issue（外部用户） | ≥1 | ≥3 | 同上 |
| Google Scholar 显示被引 | ≥0 | ≥1 | 同上 |
| arXiv abs 页 access count | ≥50 | ≥150 | 同上 |
| 邵看人生公号文章被外部转引 | ≥1 次 | ≥2 次 | 同上 |

**特别说明**：以上阈值**不是要求 viral**，是要求「**能被搜索引擎/学术爬虫看见**」的最低存在感。如全部 0，说明定位/关键词出了问题，硬投也是浪费工时。

### 3.5 撤稿熔断器（Hard Cutoff）

**触发任一条件 → 立即撤稿，不修不投，归档此 memo**：

1. ✋ Reviewer 要求 **真人评估 / 真人校准**（rubric 或 ground truth）
2. ✋ Reviewer 要求 **N > 200 personas**
3. ✋ Reviewer 要求 **重新设计 rubric**（包括加 dimensions、改 scale）
4. ✋ Reviewer 要求 **加入新的 domain application**（即不再是 DaE/Fitness/Fashion 三个）
5. ✋ Reviewer 要求 **跨语言验证**（再加英语 personas）
6. ⏰ 合稿工时实际触及 **25h 上限的 80%（即 20h）** 但完成度 < 70% → 主动叫停
7. ⏰ 投稿后 **6 个月** 仍未给出 first decision（TMLR 异常）→ 撤稿
8. 📉 **外部信号检查 T+60 天** 全部 0 → 暂缓投稿决策（不撤稿但不进新阶段）

---

## 4. 不投的反方案（如果决策是「不投」）

如果主持人最终决定不投：

1. **v1.1 supplement 已上 GitHub** → 留作搜索引擎 evidence
2. **arXiv 一旦通过 moderation** → 自动获得永久 DOI 等价物
3. **SSRN 4 篇通过审批后** → 各自有 working paper URL
4. **不写合稿、不投任何刊** → 工时省 25h，回归量化主轴

**这条路的风险**：3-5 年后可能后悔——AKM 协议被同期工作（如 Doubly-Robust LLM-as-Judge 系）覆盖、被引为 baseline、自己反而失去 first-mover 学术发明权。但**这个风险无法用 25h 工时完全消除**——投了也可能被 reject 或被同期工作覆盖。

---

## 5. 我（Claude）的最终建议

**投 TMLR，硬顶 25h，外部信号检查门槛严格执行。**

依据：
1. **v1.1 让 desk-reject 风险从 19 轮的「中-高」降到 ~15%**（TMLR 标准明确）
2. **同期 ICLR/NeurIPS 接收类似工作**——这条赛道在主流学术界是热的，不是冷的
3. **不投的机会成本无法量化**（first-mover 学术发明权），但**投的成本可量化**（25h，可硬顶）
4. **6 个熔断器 + 5 个外部信号阈值**确保「不死磕大修黑洞」

**关键反方观点（须主持人裁决）**：

- **Gemini 19 轮立场**：心智带宽 + 沉没成本，「**不合稿、不投新刊**」。我现在判断 Gemini 这个立场**部分仍成立**——25h sprint 在 8 周内执行，对量化主轴的挤占必须由主持人评估
- **DeepSeek 19 轮立场**：投 KBS/ESWA。我现在判断 DS **应改投 TMLR 而非 KBS/ESWA**——TMLR 标准对 AKM 类工作更友好
- **GPT 19 轮立场**：S3 memo + 止损。本 memo 即是 GPT 路径的具体执行

---

## 6. 主持人需要拍板的 3 件事

1. ☐ **是否投**？（TMLR / 不投）
2. ☐ **如投，是否同意 25h 工时硬顶 + 5 个外部信号阈值 + 6 个熔断器**？
3. ☐ **W2 sprint 启动时间**——SSRN/arXiv URL 到位后立即启动，还是等外部信号检查 T+30 天数据后再启动？

---

*memo 完成：2026-05-05 13:45 Beijing*
*下次复盘：T+30 天（外部信号第一次检查）*
