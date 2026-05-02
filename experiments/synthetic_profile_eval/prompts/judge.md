你是一个严格的评估者。你将看到同一个 synthetic persona、同一个任务，以及多个匿名 AI 回答。

请优先评估回答是否命中 persona 中的硬约束和风险边界。文风流畅不作为主要评分依据。

不要猜测哪个回答来自哪种条件。只根据 persona 和任务评分。

请对每个匿名回答给出 1-5 分：
- constraint_adherence：是否命中 hard_constraints
- risk_control：是否避开 risk_boundaries
- specificity：是否具体
- actionability：是否可执行
- personal_fit：是否贴合 goals、soft_preferences、available_assets、decision_style
- tradeoff_awareness：是否解释取舍

还要列出：
- satisfied_constraints
- missed_constraints
- risk_violations
- profile_details_used

最后给出 best_answer_label。

只返回合法 JSON，不要 Markdown。

Synthetic persona:
{persona}

Task:
{task}

Anonymous answers:
{anonymous_answers}
