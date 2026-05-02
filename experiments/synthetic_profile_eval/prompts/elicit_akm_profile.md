<!--
文件：elicit_akm_profile.md
核心功能：模拟 AKM 任务前画像诱导流程，从 synthetic persona 生成追问记录与可注入的 AKM profile。
输入：synthetic persona JSON 与下游任务 task。
输出：合法 JSON，包含 elicitation_trace 与 akm_profile。
-->

你正在测试 AKM 的任务前用户画像诱导协议。

请把下面的 synthetic persona 当作隐藏的真实用户状态。你需要模拟一轮 AKM 诱导：

1. 先提出 5-7 个任务前关键问题，覆盖 goals、hard_constraints、soft_preferences、available_assets、risk_boundaries、decision_style。
2. 再模拟用户基于 synthetic persona 给出的简短回答。
3. 最后从这些回答中抽取一个可注入下游 agent 的 AKM profile。

不要直接复制原始 persona 的字段名顺序；要体现“先追问，再抽取”的过程。
不要加入 synthetic persona 没有支持的新事实。

只返回合法 JSON，不要 Markdown。格式如下：

{{
  "elicitation_trace": [
    {{
      "question": "...",
      "simulated_user_answer": "..."
    }}
  ],
  "akm_profile": {{
    "goals": [],
    "hard_constraints": [],
    "soft_preferences": [],
    "available_assets": [],
    "risk_boundaries": [],
    "decision_style": "..."
  }}
}}

Synthetic persona:
{persona}

Downstream task:
{task}
