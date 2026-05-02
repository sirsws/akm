"""
文件：run_judging.py
核心功能：重新调用 DeepSeek API，对多组匿名回答进行盲评，不暴露 no_profile、unstructured_notes、akm_profile、akm_elicited 条件标签。
输入：profiles.jsonl、outputs/generations.jsonl、prompts/judge.md、DEEPSEEK_API_KEY 环境变量。
输出：outputs/judgments.jsonl，包含匿名标签映射、评分 JSON 与 judge 原始输出。
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
TEMPERATURE = 0.0
MAX_TOKENS = 2200


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]


def call_deepseek(api_key: str, prompt: str) -> str:
    payload = {
        "model": MODEL,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "messages": [
            {"role": "system", "content": "你是一个只返回合法 JSON 的严格评估器。"},
            {"role": "user", "content": prompt},
        ],
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        body = response.read().decode("utf-8")
    data = json.loads(body)
    return data["choices"][0]["message"]["content"]


def group_generations(records: list[dict]) -> dict[str, dict[str, dict]]:
    grouped: dict[str, dict[str, dict]] = {}
    for record in records:
        profile_id = record["profile_id"]
        condition = record["condition"]
        if profile_id not in grouped:
            grouped[profile_id] = {}
        grouped[profile_id][condition] = record
    return grouped


def main() -> None:
    api_key = os.environ["DEEPSEEK_API_KEY"].strip()
    profiles = {record["profile_id"]: record for record in read_jsonl(ROOT / "profiles.jsonl")}
    generations = group_generations(read_jsonl(ROOT / "outputs" / "generations.jsonl"))
    judge_template = read_text(ROOT / "prompts" / "judge.md")
    output_records: list[dict] = []

    for profile_id in sorted(generations):
        profile = profiles[profile_id]
        condition_items = list(generations[profile_id].items())
        rng = random.Random(f"akm-{profile_id}")
        rng.shuffle(condition_items)
        labels = [f"answer_{chr(97 + index)}" for index in range(len(condition_items))]
        label_map: dict[str, str] = {}
        anonymous_answers: dict[str, str] = {}
        for label, (condition, record) in zip(labels, condition_items):
            label_map[label] = condition
            anonymous_answers[label] = record["content"]

        prompt = judge_template.format(
            persona=json.dumps(profile["persona"], ensure_ascii=False, indent=2),
            task=profile["task"],
            anonymous_answers=json.dumps(anonymous_answers, ensure_ascii=False, indent=2),
        )
        raw_judgment = call_deepseek(api_key, prompt)
        parsed_judgment = json.loads(raw_judgment)
        output_records.append(
            {
                "profile_id": profile_id,
                "domain": profile["domain"],
                "model": MODEL,
                "temperature": TEMPERATURE,
                "prompt_hash": prompt_hash(prompt),
                "label_map": label_map,
                "judgment": parsed_judgment,
                "raw_judgment": raw_judgment,
            }
        )

    output_path = ROOT / "outputs" / "judgments.jsonl"
    output_path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in output_records) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
