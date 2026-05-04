"""
文件：generate_profiles.py
核心功能：调用 DeepSeek-V4-pro 批量合成 synthetic personas，扩充 profiles.jsonl 至目标 50 条；保留既有条目，仅追加新 id。
输入：现有 profiles.jsonl、内置场景配置（domain, sub_scenario, task 模板, count）、DEEPSEEK_API_KEY。
输出：扩展后的 profiles.jsonl（schema 与既有条目一致：profile_id/domain/task/persona/unstructured_notes/akm_profile）；同时落盘 profiles_generation_log.jsonl 记录每条来源 prompt hash。
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

from run_generation import call_deepseek_json, load_deepseek_key


ROOT = Path(__file__).resolve().parent
PROFILES_PATH = ROOT / "profiles.jsonl"
LOG_PATH = ROOT / "outputs" / "v1" / "profiles_generation_log.jsonl"


SCENARIOS = [
    {
        "domain": "career",
        "id_prefix": "career",
        "start_index": 3,
        "count": 4,
        "task_templates": [
            "请为这位用户规划未来三个月的工作重心。",
            "请为这位用户设计一个低风险的职业转型试验计划。",
            "请帮这位用户决定是否接受当前手上的新项目机会。",
            "请帮这位用户重新设计当前工作的精力分配。",
        ],
        "persona_seed": "面向 35-50 岁专业人士的真实职业困境（含主业压力、副业探索、转型纠结、晋升博弈、跨界尝试、行业下行、女性职业天花板、技术更替焦虑等多样情境）",
    },
    {
        "domain": "learning",
        "id_prefix": "learning",
        "start_index": 3,
        "count": 4,
        "task_templates": [
            "请为这位用户设计一个三个月的学习方案。",
            "请帮这位用户决定是否值得报名当前正在考虑的课程或证书。",
            "请帮这位用户规划下一年的能力跃迁路径。",
            "请帮这位用户搭建一个工作-学习一体化的最小可行体系。",
        ],
        "persona_seed": "面向不同年龄、行业、家庭情况的真实终身学习者：含中年转码、跨界考证、家庭主妇副业自学、研究生毕业进入行业、高管自我升级等多样情境",
    },
    {
        "domain": "investment",
        "id_prefix": "investment",
        "start_index": 2,
        "count": 5,
        "task_templates": [
            "请为这位用户设计一份 12 个月的家庭资产配置方案。",
            "请帮这位用户判断当前是否应该减仓或加仓。",
            "请帮这位用户设计一个针对孩子未来教育金的长期投资计划。",
            "请帮这位用户评估当前是否应该买房 / 卖房 / 换房。",
            "请帮这位用户设计一个低社交负载的被动收入构建路径。",
        ],
        "persona_seed": "面向中国大陆家庭的真实理财决策者：含工薪夹心层、个体工商户、自由职业者、单身高净值、临退休夫妇、投资亏损后重启者等情境，必须涉及现实约束（房贷/教育/养老）",
    },
    {
        "domain": "health_lifestyle",
        "id_prefix": "health",
        "start_index": 2,
        "count": 5,
        "task_templates": [
            "请为这位用户设计一个三个月内可坚持的健康改善方案。",
            "请帮这位用户重新规划工作日的作息和精力管理。",
            "请帮这位用户设计一份兼顾家庭和自我修复的周末安排。",
            "请帮这位用户处理目前最严重的一项健康风险。",
            "请帮这位用户重新评估当前是否需要做体检 / 看医生 / 调整药物。",
        ],
        "persona_seed": "面向 30-55 岁中国都市人群的真实健康与生活方式困境：含久坐颈椎、慢病管理、亚健康、产后恢复、照护失能父母、心理倦怠、轮班工作者等情境",
    },
    {
        "domain": "relationship",
        "id_prefix": "relationship",
        "start_index": 1,
        "count": 6,
        "task_templates": [
            "请帮这位用户规划接下来一个月的家庭关系修复路径。",
            "请帮这位用户处理与父母的边界冲突。",
            "请帮这位用户优化当前的亲密关系沟通模式。",
            "请帮这位用户重新设计与孩子的相处节奏。",
            "请帮这位用户处理当前最紧张的一段职场人际关系。",
            "请帮这位用户设计一个低社交负载的朋友圈维护策略。",
        ],
        "persona_seed": "面向真实成年人的关系议题：含夫妻冷淡、隔代育儿冲突、独居社交断层、职场人际消耗、亲密关系不安全感、单身/离异/再婚等多样情境，避免狗血戏剧化",
    },
    {
        "domain": "fitness",
        "id_prefix": "fitness",
        "start_index": 3,
        "count": 8,
        "task_templates": [
            "请为这位用户制定一个 8 周的训练计划。",
            "请为这位用户设计一份家庭场景的最小训练方案。",
            "请帮这位用户在伤病恢复期重建训练节奏。",
            "请帮这位用户解决目前最影响进步的训练瓶颈。",
            "请帮这位用户重新设计减脂期的训练与饮食配比。",
            "请帮这位用户设计一份中年体能维护方案。",
            "请帮这位用户判断当前训练强度是否过量并给出调整建议。",
            "请帮这位用户在出差/旅行场景下保持训练连续性。",
        ],
        "persona_seed": "面向不同水平、性别、伤病背景、训练目标（增肌/减脂/体能/康复/竞技）的真实健身用户，必须包含明确的硬约束如伤病、时间、设备限制",
    },
    {
        "domain": "fashion",
        "id_prefix": "fashion",
        "start_index": 3,
        "count": 8,
        "task_templates": [
            "请为这位用户设计一份未来一季的穿搭预算分配方案。",
            "请帮这位用户搭建一个最小可工作的胶囊衣橱。",
            "请帮这位用户为某个特定场景（如重要会议/相亲/年会）规划穿搭。",
            "请帮这位用户重新整理现有衣橱并指出最值得淘汰的部分。",
            "请帮这位用户解决体型变化后的过渡期穿搭问题。",
            "请帮这位用户在低预算下提升整体职业形象。",
            "请帮这位用户评估当前衣橱是否匹配现阶段的职业身份。",
            "请帮这位用户为旅行 / 出差打包出一套兼顾功能与体面的穿搭。",
        ],
        "persona_seed": "面向不同性别、年龄、体型、身份（学生/职场/创业者/全职主妇/退休）的真实穿搭决策者，必须包含明确的硬约束（预算、体型、场合、宗教/职业要求等）",
    },
]


PROFILE_GEN_PROMPT_TEMPLATE = """你正在为 AKM（Active Knowledge Modeling）基准测试合成一份高质量、贴近真实中国语境的 synthetic persona 数据。

请生成 1 条用户画像，严格遵循以下要求：

【场景】
- domain: {domain}
- 该批 persona 的素材池: {persona_seed}
- 必须使用以下下游任务作为 task: "{task}"
- 这是该 domain 下的第 {seq} 条 persona。请确保与你之前可能见过的同一 domain 模板存在明显差异（不同性别、年龄、身份、约束组合）。
- 多样性提示: {diversity_hint}

【schema 严格要求】
只返回合法 JSON，不要 Markdown，不要 ```json 包裹，结构必须是：

{{
  "profile_id": "{profile_id}",
  "domain": "{domain}",
  "task": "{task}",
  "persona": {{
    "goals": ["3-4 条具体目标"],
    "hard_constraints": ["4-6 条强约束，必须可被违反的具体事实，禁止空泛"],
    "soft_preferences": ["3-5 条偏好"],
    "available_assets": ["3-5 条已有资源（时间/技能/工具/人脉/资金）"],
    "risk_boundaries": ["3-4 条不可触碰的红线"],
    "decision_style": "1 句话描述决策风格"
  }},
  "unstructured_notes": "用第一人称、口语化、像微信对朋友吐槽那样写一段 80-160 字的自述，包含上面 persona 中的核心信息但不要直接照搬字段，故意保留一些模糊和省略",
  "akm_profile": {{
    "goals": ["与 persona.goals 等价的精炼版本"],
    "hard_constraints": ["与 persona.hard_constraints 等价"],
    "soft_preferences": ["与 persona.soft_preferences 等价"],
    "available_assets": ["与 persona.available_assets 等价"],
    "risk_boundaries": ["与 persona.risk_boundaries 等价"],
    "decision_style": "与 persona.decision_style 等价"
  }}
}}

【硬性内容要求】
- persona 必须真实可信、避免狗血或刻板印象。
- hard_constraints 必须包含至少 1 条时间/金钱/身体/家庭层面的具体数字或具体限制。
- akm_profile 是 persona 的结构化精炼版本，措辞可以重排但不得引入 persona 中不存在的新事实。
- 全部使用简体中文。
"""


DIVERSITY_HINTS = [
    "请刻画女性视角，年龄段 30-40。",
    "请刻画男性视角，年龄段 40-55。",
    "请刻画自由职业者或创业者。",
    "请刻画体制内或国企工作者。",
    "请刻画带年幼孩子的父母。",
    "请刻画上有老下有小的夹心层。",
    "请刻画近期遭遇重大变化（失业/搬迁/疾病）的用户。",
    "请刻画一线城市以外的二三线城市用户。",
]


def prompt_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def existing_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {
        json.loads(line)["profile_id"]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    api_key = load_deepseek_key()
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    existing = existing_ids(PROFILES_PATH)
    print(f"Existing profiles: {len(existing)}")

    success: list[str] = []
    failed: list[tuple[str, str]] = []

    fout = PROFILES_PATH.open("a", encoding="utf-8")
    flog = LOG_PATH.open("a", encoding="utf-8")
    try:
        for scenario in SCENARIOS:
            domain = scenario["domain"]
            prefix = scenario["id_prefix"]
            templates = scenario["task_templates"]
            for i in range(scenario["count"]):
                seq_index = scenario["start_index"] + i
                profile_id = f"{prefix}_{seq_index:03d}"
                if profile_id in existing:
                    print(f"  SKIP {profile_id}: already exists")
                    continue
                task = templates[i % len(templates)]
                diversity_hint = DIVERSITY_HINTS[(seq_index + hash(domain)) % len(DIVERSITY_HINTS)]
                attempt_ok = False
                for attempt in range(1, 4):
                    prompt = PROFILE_GEN_PROMPT_TEMPLATE.format(
                        domain=domain,
                        persona_seed=scenario["persona_seed"],
                        task=task,
                        seq=seq_index,
                        profile_id=profile_id,
                        diversity_hint=diversity_hint,
                    )
                    print(f"  Generating {profile_id} (attempt {attempt}) ...")
                    data = call_deepseek_json(api_key, prompt)
                    data["profile_id"] = profile_id
                    data["domain"] = domain
                    data["task"] = task
                    schema_problem = _validate_schema(data)
                    if schema_problem:
                        print(f"    Schema problem: {schema_problem}; retrying")
                        time.sleep(1.5)
                        continue
                    fout.write(json.dumps(data, ensure_ascii=False) + "\n")
                    fout.flush()
                    flog.write(json.dumps({
                        "profile_id": profile_id,
                        "domain": domain,
                        "task": task,
                        "prompt_hash": prompt_hash(prompt),
                        "diversity_hint": diversity_hint,
                        "model": "deepseek-v4-pro",
                        "attempt": attempt,
                    }, ensure_ascii=False) + "\n")
                    flog.flush()
                    success.append(profile_id)
                    existing.add(profile_id)
                    attempt_ok = True
                    time.sleep(0.4)
                    break
                if not attempt_ok:
                    failed.append((profile_id, "schema_validation_failed_after_retries"))
    finally:
        fout.close()
        flog.close()

    print(f"\n== summary == success: {len(success)}, failed: {len(failed)}")
    for pid, why in failed:
        print(f"  FAIL {pid}: {why}")


def _validate_schema(data: dict) -> str | None:
    if not all(k in data for k in ("persona", "akm_profile", "unstructured_notes")):
        return "missing top-level fields"
    for field in ("goals", "hard_constraints", "soft_preferences", "available_assets", "risk_boundaries", "decision_style"):
        if field not in data["persona"]:
            return f"persona.{field} missing"
        if field not in data["akm_profile"]:
            return f"akm_profile.{field} missing"
    if not isinstance(data["unstructured_notes"], str) or len(data["unstructured_notes"]) < 30:
        return "unstructured_notes too short or wrong type"
    return None


if __name__ == "__main__":
    main()
