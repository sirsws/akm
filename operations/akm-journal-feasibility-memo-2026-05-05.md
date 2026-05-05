<!--
文件：akm-journal-feasibility-memo-2026-05-05.md
核心功能：S3 期刊可行性 memo —— 在 v1.1 supplement 已落盘的前提下，评估 AKM 是否值得投中档 SCI 期刊；如投，应投哪一刊、工时上限、外部信号检查、撤稿熔断器。
        2026-05-05 红队修订 v2：响应 GPT/DS 联合 red-team——desk-reject 估值由 ~15% 上调到 25-35%；
        路径由「W2 立即启动 25h sprint」改为 Door A→D 阶梯（A 修硬伤 → B 等 arXiv → C 4h skeleton 过红队 → D 决定 25h sprint）；
        合稿工时上调至 28-30h（含 TMLR 双盲匿名化 3-5h）；α 表述区分 α_total 与 per-dim α；
        删除 Personalized RewardBench 的 ICLR 2026 错标。
输入：v1.1 supplement (5/5 generators, +14.56~+19.81 lift, α_total ∈ [0.894, 0.949])；3 候选刊 (TMLR / KBS / ESWA) 公开文档；近 12 个月 LLM personalization / synthetic-persona / LLM-as-judge 接收先例；19 轮共识 (S3 memo 立项 + 止损纪律)；20 轮 GPT/DS 红队批注。
输出：阶梯式投稿决策 + 投刊次序 + 硬熔断器。供顾问团在讨论板批注。
维护要求：本 memo 一旦决策「进 Door D」，SSRN/arXiv 公开 URL 出来当天必须重新跑一遍「外部信号检查」并更新；任一熔断器触发立即归档此 memo。
-->

# AKM 期刊可行性 memo（S3）

> **日期**：2026-05-05（v2，响应 20 轮 GPT/DS 红队修订）
> **作者**：Claude（顾问，主笔）
> **审稿对象**：邵先生（拍板）+ 战略顾问团（ChatGPT / Gemini / DeepSeek / Kimi / GLM / MiniMax）
> **决策性质**：**阶梯式**——Door A（必做）→ Door B（被动等）→ Door C（4h skeleton gate）→ Door D（25-30h sprint）。每道门都是独立的 go/no-go 决策点。

---

## TL;DR（30 秒读完版）

**结论**：**S2 完成后，期刊线从「不该投」翻转为「值得有条件投」。建议路径：投 TMLR，但要走 4 道门，不是一上来就 sprint。**

**核心依据**：
- v1.1 实测数据（5/5 generator AKM lift +14.56~+19.81，α_total ∈ [0.894, 0.949]，per-dim α 最低 0.697 = GPT actionability，0 mismatch）
- TMLR 明确接受 "claims supported by accurate evidence"，**不要求 novelty / SOTA**
- 当本 claim 限定在 synthetic-persona benchmark 范围内（不主张 real-user behavior），不触发真人评估必要性

**desk-reject 估值（v2 红队修正）**：
- TMLR：**~25-35%**（v1 写的 ~15% 被 GPT/DS 同时反驳为低估，已撤回）
- KBS：~30-40%
- ESWA：~55%（不投）

**硬熔断器**：
- TMLR 评审若索要真人 / N>200 / 重设 rubric / 新增 domain / 跨语言 → 撤稿不修
- 工时硬顶 30h（含 TMLR 双盲匿名化 3-5h），超 80% 仍未达 70% 完成度即叫停
- Door C 的 4h skeleton 若顾问团红队不通过 → 不进 Door D
- 若 SSRN/arXiv 30 天后无任何外部信号（star/issue/被引）→ T+30 一次性 gate 不达标，暂缓决策

---

## 1. v1.1 完成后的形势变化

19 轮辩论时，三人触发条件全部基于 **v1.0 单 generator 已知硬伤**。19 轮 Claude（我）的判断是「合稿 25-35h、desk-reject 高、不值得」。**S2 落地后，三个判断全部需要更新**：

| 19 轮判断 | v1.1 落地后实测 | 调整方向 |
|---|---|---|
| 「单 generator」是 reviewer 第一刀 | 5/5 generator 全成立 + 1 attempted-but-excluded 诚实记录 | **第一刀 已挡** |
| 「合稿 25-35h」 | 已有 4 篇 LaTeX + supplement 完整，但 TMLR 双盲匿名化是硬约束（3-5h） | **维持 28-30h（v2 修正：v1 草稿写 12-18h 严重低估，已 deprecated；以 §3.2 完整 WBS 为准）** |
| 「中档 IF~3-9 可试」 | TMLR 明确不要求 novelty/SOTA + 同期 ICLR 2026 接收 synthetic-persona LLM-as-judge 论文 | **TMLR 比中档 IF 更适合** |

**两个意外发现**：
1. **TMLR 对此类工作的 fit 比 KBS/ESWA 都好**——审稿口径正面契合 v1.1 的「evidence-based」定位
2. **同期 ICLR 接收的 LLM-as-judge + synthetic personas 工作**（Doubly-Robust LLM-as-Judge ICLR 2026、RouteJudge ICLR 2026）证明这条研究路径**在顶会赛道是热的**。**v2 修正**：v1 同时把 Personalized RewardBench 列为 ICLR 2026，但其实它是 arXiv 2604.07343v1 而非 ICLR 接收稿——一查就穿，故移出 ICLR 列表，仍可作为同期 personalization benchmark 工作的旁证。

**v2 自我纠错**：v1 据此把 desk-reject 估值压到 ~15%，过于乐观。GPT 与 DS 的红队批注一致指出 TMLR 仍会因 scope mismatch（"像 protocol/product paper 不像 ML research paper"）desk-reject，正确估值是 **~25-35%**。本 memo 全文已更新此估值。

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

**对 AKM v1.1 的契合度**：★★★★☆（v2 由 5 星下调到 4.5 星：v1.1 仍是 protocol+benchmark paper 不是 ML research paper）
- v1.1 的核心主张是 evidence-based（5/5 generator + α_total ∈ [0.894, 0.949] + per-dim α 最低 0.697 已诚实披露 + 0 mismatch verify）→ 标准 1 大体满足
- TMLR audience 包括 LLM-as-judge、benchmark、personalization 研究者 → 标准 2 满足
- **明确不卷 SOTA、不卷 novelty** → 这一项确实是 AKM 的 friendly fit
- **关键限定**：TMLR 不要求真人，但若 claim 涉及 real-user behavior 仍会被要求真人或降 claim。**当本 claim 限定在 synthetic-persona benchmark 范围内（不主张 real-user behavior），不触发真人评估必要性**——本 memo 的所有 TMLR 路径都建立在这一限定之上。

**desk-reject 风险评估**：**~25-35%（v2 红队修正后）**
- 主因 1：scope mismatch——AKM 像 protocol+benchmark paper 而不像 ML research paper，editor 分配 reviewer pool 时可能分到不熟悉 elicitation methodology 的 ML reviewer
- 主因 2：technical depth——TMLR reviewer pool 对纯 protocol/benchmark 的技术深度评判口径不一
- 缓解：投稿 metadata 选 "evaluation methodology" + "language models" + "human-AI interaction" 三个标签
- 同期接收先例：Simula（synthetic data generation evaluation 框架）、多篇 LLM benchmark 论文

**送审后大修被卡风险**：**~25%**（v2 微调）
- 主要风险：reviewer 索要 cross-prompt-template robustness 实验、或新增 evaluation dimension
- 应对：诚实回复"out of scope of this submission, future work"，不补
- 若 reviewer 索要真人 / N>200 → **撤稿熔断**

**TMLR 双盲要求（v2 新增的硬约束）**：
- TMLR 双盲：submission 主文与 supplement 都不得指向带作者身份的 GitHub / SSRN / arXiv 链接
- 实际工作：准备 **匿名 PDF + 匿名 supplement zip + 匿名代码快照（Anonymous GitHub 或 Zenodo 匿名 DOI）**，并将正文里所有 `github.com/sirsws/akm` 等链接替换为占位
- 工时影响：约 **3-5h**，已计入 §3.2 的合稿 WBS（旧 25h → 新 28-30h）

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

### 2.4 综合对比（v2 红队修正）

| 刊 | 核心匹配度 | desk-reject 估值 | 大修被真人/N 卡的风险 | 周期 | 推荐 |
|---|:---:|:---:|:---:|:---:|:---:|
| **TMLR** | ★★★★☆ | **~25-35%** | 低（标准明确不卷 novelty） | 8-16 周 | **首选**（但要走 4 道门，不是直接 sprint） |
| **KBS** | ★★★★ | ~30-40% | 中（reviewer 个人偏好） | 8-16 周 | TMLR desk-reject 后才考虑 |
| **ESWA** | ★★ | ~55% | 高（真人是隐性硬要求） | 12-20 周 | **不投** |

---

## 3. 建议执行路径（v2 重写：Door A → Door D 阶梯）

**核心变更**：v1 写的"W2 立即启动 25h sprint"被 GPT/DS 红队同时反对——直接进 sprint 是把 v1.1 的胜利立刻押进 8 周写作债，且未先消化 v1.1 文档硬伤。v2 改为四道门，每道门是独立的 go/no-go 决策点。

```
Door A (必做，~2.5h)         修 v1.1 supplement/memo 的 11 条文档硬伤 + verify 0 mismatch
       ↓
Door B (被动等)              SSRN under review → URL 公开；arXiv on hold → moderation 结果
       ↓
Door C (~4h, 主持人批准后)   写 TMLR skeleton（标题/abstract/contributions/匿名化方案/related-work spine）
                              过顾问团红队（GPT/DS/Gemini）
       ↓
Door D (~25-30h, 红队通过后) 完整合稿 sprint，投 TMLR
```

**Door A 是本次主持人接受 plan 后立即执行的，已与本 memo 同时落盘**。Door B 是被动等待，无工时。Door C/D 都是独立 go/no-go，主持人在每道门可以无成本撤回。

### 3.1 投稿次序

**先投 TMLR 单刊**（OpenReview 系不允许同时多投）。Door D 启动后才投。

如 TMLR desk-reject 或 reject → **触发熔断**：
- 若 reject 理由是"lack of novelty / not interesting enough" → KBS 改投（仅当 desk-reject 不是 scope 问题时）
- 若 reject 理由是"need real users / larger N / different rubric" → **不改投，归档**

如 TMLR accept → 不再投其他刊。

### 3.2 合稿工作量分解（硬顶 30h，v2 上调）

基于 v1.1 已落地的 4 篇 LaTeX + supplement，合稿成 **1 篇 TMLR-ready 的"AKM Master + 3 Domain Studies"**：

| 工作 | 估时（v2） | 说明 |
|---|---:|---|
| **Door C：TMLR skeleton** | **4h** | 标题 + abstract + contributions + anonymous artifact plan + claim boundary + related-work spine。**不写正文**。skeleton 要过顾问团红队才进 Door D |
| **Door D 起算** | | |
| Abstract / Intro 重写为 TMLR 风格 | 2h | 强调 evidence-based、不卷 novelty，明确 claim 限定在 synthetic |
| Methodology 章节统一 | 3h | 4 篇方法不一致处统一 |
| Results 章节嵌入 v1.1 supplement 数据 | 4h | 5/5 lift 表 + α 表（区分 α_total 与 per-dim） + Gemma ρ=0.8 honest disclosure + GLM ceiling 反例 |
| Limitations & Honest Disclosure 章节 | 2h | Kimi excluded、Gemma 高 α 低 ρ、format_repair per-generator 分布缺失、real-user absent 全写 |
| Related Work 章节（必须钉牢同期工作） | 4h | Doubly-Robust LLM-as-Judge ICLR 2026 / RouteJudge ICLR 2026 / Personalized RewardBench arXiv 2604.07343 / RecBench+ / Bespoke / Zheng 2023 |
| Reproducibility 章节 + 代码链接 | 1h | 已有 verify_v11.py + GitHub repo |
| LaTeX 排版 + 4 篇内容裁剪去重 | 4h | 当前 4 篇有 ~20% 重复 |
| **TMLR 双盲匿名化（v2 新增）** | **3-5h** | 匿名 PDF + 匿名 supplement zip + 匿名代码快照（Anonymous GitHub 或 Zenodo 匿名 DOI） + 替换 README/SSRN/arXiv 链接为占位 |
| OpenReview 投稿 + metadata | 1h | 标签、领域、关键词 |
| 自审 + verify 数字 + bib 检查 | 4h | 17 轮教训不重犯，verify_v11.py 必须 0 mismatch |
| **Door D 合计** | **28-30h** | **硬顶 30h** |
| **Door C + Door D 总合计** | **32-34h** | |

**这 30h 在 8 周内分摊 = 平均 3.75h/周**（v1 写的 3.1h/周低估了）。在 19 轮共识的「≤2h/周」基础上明显超出，主持人在 Door C 的 skeleton 红队后必须显式批准才进入 Door D。

### 3.3 时间线（v2 更新）

| 时点 | 动作 | 门 |
|---|---|---|
| **2026-05-05（今天）** | Door A：修 v1.1 supplement/memo 11 条硬伤 + push | A |
| **2026-05-05~05-15** | SSRN under review URL 已公开（4 篇）；arXiv on hold 等 moderation | B（被动） |
| **arXiv URL 到位之日** | 立即更新 README + 邵看人生短讯 | B |
| **arXiv 过审后 + 主持人批准** | Door C：4h TMLR skeleton + 顾问团红队 | C |
| **Skeleton 过红队 + 主持人批准** | Door D：28-30h 合稿 sprint | D |
| **Sprint 完成后** | 投 TMLR | D |
| **第 30 天**（约 2026-06-04） | **一次性外部信号检查 gate**（GitHub star/issue/被引） | 见 §3.4 |

### 3.4 外部信号检查清单（v2：T+30 一次性 gate）

**目的**：避免「无人关注却继续投学术」的多巴胺陷阱。

**v2 修订**：v1 设了 T+30 + T+60 双检查。GPT 红队反驳 Gemini 时指出"双检查没问题，但要避免每天盯 star 的日常巡逻"。Gemini 的反对核心是"监控本身是内耗"。最稳妥折中：**改为 T+30 一次性 gate**，到点看一次（约 10 分钟）记录一次，不日常巡逻。如 T+30 全部 0，T+60 不再单独检查（因为 Door D 已结束）。

**检查时点**：T+30 天（T = arXiv 公开日）。一次。

**检查项**：
| 信号 | 阈值（T+30） | 不达标动作 |
|---|---:|---|
| GitHub star（akm 主仓） | ≥10 | 不达标 1 项可继续；3 项以上不达标 → 暂缓投稿决策 |
| GitHub issue（外部用户） | ≥1 | 同上 |
| Google Scholar 显示被引 | ≥0 | 同上（≥0 = 只要 Scholar 索引到了就算达标） |
| arXiv abs 页 access count | ≥50 | 同上 |
| 邵看人生公号文章被外部转引 | ≥1 次 | 同上 |

**特别说明**：以上阈值**不是要求 viral**，是要求「**能被搜索引擎/学术爬虫看见**」的最低存在感。如全部 0，说明定位/关键词出了问题，硬投也是浪费工时。

### 3.5 撤稿熔断器（Hard Cutoff，v2 微调）

**触发任一条件 → 立即撤稿，不修不投，归档此 memo**：

1. ✋ Reviewer 要求 **真人评估 / 真人校准**（rubric 或 ground truth）
2. ✋ Reviewer 要求 **N > 200 personas**
3. ✋ Reviewer 要求 **重新设计 rubric**（包括加 dimensions、改 scale）
4. ✋ Reviewer 要求 **加入新的 domain application**（即不再是 DaE/Fitness/Fashion 三个）
5. ✋ Reviewer 要求 **跨语言验证**（再加英语 personas）
6. ⏰ Door D 合稿工时触及 **30h 上限的 80%（即 24h）** 但完成度 < 70% → 主动叫停
7. ⏰ 投稿后 **6 个月** 仍未给出 first decision（TMLR 异常）→ 撤稿
8. 📉 **T+30 一次性 gate** 5 项全部不达标 → 暂缓 Door D（如 Door D 已启动则做完不撤）
9. 🛑 **Door C skeleton 顾问团红队不通过** → 不进 Door D，归档

---

## 4. 不投的反方案（如果决策是「不投」）

如果主持人最终决定不投：

1. **v1.1 supplement 已上 GitHub** → 留作搜索引擎 evidence
2. **arXiv 一旦通过 moderation** → 自动获得永久 DOI 等价物
3. **SSRN 4 篇通过审批后** → 各自有 working paper URL
4. **不写合稿、不投任何刊** → 工时省 25h，回归量化主轴

**这条路的风险**：3-5 年后可能后悔——AKM 协议被同期工作（如 Doubly-Robust LLM-as-Judge 系）覆盖、被引为 baseline、自己反而失去 first-mover 学术发明权。但**这个风险无法用 25h 工时完全消除**——投了也可能被 reject 或被同期工作覆盖。

---

## 5. 我（Claude）的最终建议（v2 红队后）

**走 Door A → Door D 阶梯，每道门主持人独立批准。当前先批准 Door A（已落盘）。Door C/D 等 arXiv URL 后再决策。**

依据：
1. **v1.1 让 desk-reject 风险从 19 轮的「中-高」降到 ~25-35%**（v1 写的 ~15% 已被 GPT/DS 红队修正，v2 接受）
2. **同期 ICLR 接收类似工作**——Doubly-Robust LLM-as-Judge / RouteJudge 是真实先例（v1 把 Personalized RewardBench 错列为 ICLR 已修正）
3. **不投的机会成本无法量化**（first-mover 学术发明权），但**投的成本可量化**（28-30h，可硬顶）
4. **9 个熔断器 + T+30 一次性 gate + Door C skeleton 红队**确保「不死磕大修黑洞」
5. **Door C 是关键 gate**：4h skeleton 由顾问团红队评估，如不通过则不进 Door D，机会成本仅 4h 而非 30h

**v2 立场调整公开声明**：

| v1 (原 Claude 立场) | v2 (红队后) | 调整原因 |
|---|---|---|
| W2 立即启动 25h sprint | Door A→D 阶梯，Door C 4h skeleton 先过红队 | GPT+DS 共同反对"立即"，理由是 v1.1 文档硬伤未消化 |
| desk-reject ~15% | desk-reject ~25-35% | scope mismatch 风险被低估 |
| 合稿 25h | 合稿 28-30h（含双盲匿名化 3-5h） | TMLR 双盲是硬约束，必须匿名化 GitHub/SSRN/arXiv 链接 |
| α≥0.85 全称 | α_total ∈ [0.894, 0.949]，per-dim α 最低 0.697 | 区分 α_total 与 per-dim α，不混用 |
| Personalized RewardBench (ICLR 2026) | (arXiv 2604.07343) | 错列为 ICLR，已修正 |
| T+30 + T+60 双检查 | T+30 一次性 gate | Gemini 内耗担忧 + GPT 折中方案 |

**对 19/20 轮三人立场的最终回应**：

- **Gemini 立场（彻底冻结）**：v2 部分接纳——T+30 一次性 gate 替代日常巡逻；Door C skeleton 是低成本红队 gate，不是直接 sprint。但**冻结整个 S3/S4 我仍不接受**——v1.1 用 5/5 generator 数据真实推进了 benchmark 硬度，不进 Door C 等于放弃外部学术坐标
- **DeepSeek 立场（投 KBS/ESWA）**：v2 不接受改投——TMLR 仍是首选（标准更友好），但接受 DS 的 desk-reject 25-35% 修正与 11 条硬伤批注，11 条已在 Door A 修完
- **GPT 立场（修硬伤 + 4h skeleton + 等 arXiv）**：v2 全盘接纳——Door A→D 阶梯就是 GPT 方案的具体执行

---

## 6. 主持人需要拍板的 3 件事（v2 阶梯版）

1. ☐ **是否同意 Door A→D 阶梯路径**？（即 GPT+DS 共识方案：先修硬伤 → 等 arXiv → 4h skeleton 过红队 → 决定 Door D）
2. ☐ **是否同意 Door D 工时硬顶 30h（含双盲匿名化）+ T+30 一次性 gate + 9 个熔断器**？
3. ☐ **Door C 启动时间**——arXiv 过审后立即启动（确认 4h 工时），还是先等 T+30 外部信号 gate 数据后再决定 Door C？

如果选项 1 是"否"（即采纳 Gemini 立场），Door A 的 11 条硬伤修复仍然有价值（保护 SSRN/arXiv 公开版本的诚信），但 memo 全文改为"维护模式"，Door C/D 永久搁置。

---

*memo v1 完成：2026-05-05 13:45 Beijing*
*memo v2 红队修订完成：2026-05-05 14:50 Beijing（响应 20 轮 GPT/DS 联合 red-team）*
*下次复盘：T+30 天（外部信号一次性 gate）或 arXiv 过审之日（Door C 启动决策）*
