"""
文件：run_generation.py
核心功能：调用 DeepSeek API，为每个 synthetic persona 生成 no_profile、unstructured_notes、akm_profile、akm_elicited 四组回答，并记录 akm_elicited 的画像生成链路。
输入：profiles.jsonl、prompts/generate_*.md、prompts/elicit_akm_profile.md、DEEPSEEK_API_KEY 环境变量。
输出：outputs/generations.jsonl，包含完整原始输出、模型名、温度、prompt hash、条件标签，以及 akm_elicited 的生成画像和追问记录。
"""

from __future__ import annotations

import hashlib
import json
import os
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
TEMPERATURE = 0.2
MAX_TOKENS = 1200
PROFILE_MAX_TOKENS = 1800
CONDITIONS = ["no_profile", "unstructured_notes", "akm_profile", "akm_elicited"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def read_profiles(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]


def call_deepseek(api_key: str, prompt: str) -> str:
    payload = {
        "model": MODEL,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "messages": [
            {"role": "system", "content": "你是一个严谨、简洁、可执行的中文 AI 助手。"},
            {"role": "user", "content": prompt},
        ],
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


def call_deepseek_json(api_key: str, prompt: str) -> dict:
    payload = {
        "model": MODEL,
        "temperature": TEMPERATURE,
        "max_tokens": PROFILE_MAX_TOKENS,
        "messages": [
            {"role": "system", "content": "你是一个严格的 AKM 用户画像诱导器，只返回合法 JSON。"},
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
    return json.loads(data["choices"][0]["message"]["content"])


def elicit_akm_profile(api_key: str, template: str, profile: dict) -> tuple[dict, str]:
    prompt = template.format(
        persona=json.dumps(profile["persona"], ensure_ascii=False, indent=2),
        task=profile["task"],
    )
    response = call_deepseek_json(api_key, prompt)
    return response, prompt_hash(prompt)


def render_prompt(template: str, profile: dict, condition: str) -> str:
    if condition == "no_profile":
        return template.format(task=profile["task"])
    if condition == "unstructured_notes":
        return template.format(unstructured_notes=profile["unstructured_notes"], task=profile["task"])
    if condition == "akm_profile":
        return template.format(
            akm_profile=json.dumps(profile["akm_profile"], ensure_ascii=False, indent=2),
            task=profile["task"],
        )
    if condition == "akm_elicited":
        return template.format(
            akm_profile=json.dumps(profile["elicited_akm_profile"], ensure_ascii=False, indent=2),
            task=profile["task"],
        )
    raise ValueError(f"Unknown condition: {condition}")


def main() -> None:
    api_key = os.environ["DEEPSEEK_API_KEY"].strip()
    profiles = read_profiles(ROOT / "profiles.jsonl")
    templates = {
        "no_profile": read_text(ROOT / "prompts" / "generate_no_profile.md"),
        "unstructured_notes": read_text(ROOT / "prompts" / "generate_user_notes.md"),
        "akm_profile": read_text(ROOT / "prompts" / "generate_akm_profile.md"),
        "akm_elicited": read_text(ROOT / "prompts" / "generate_akm_profile.md"),
    }
    elicitation_template = read_text(ROOT / "prompts" / "elicit_akm_profile.md")
    output_path = ROOT / "outputs" / "generations.jsonl"
    records: list[dict] = []

    for profile in profiles:
        elicited: dict | None = None
        elicitation_prompt_hash = ""
        for condition in CONDITIONS:
            working_profile = dict(profile)
            if condition == "akm_elicited":
                elicited, elicitation_prompt_hash = elicit_akm_profile(api_key, elicitation_template, profile)
                working_profile["elicited_akm_profile"] = elicited["akm_profile"]
            prompt = render_prompt(templates[condition], working_profile, condition)
            content = call_deepseek(api_key, prompt)
            record = {
                "profile_id": profile["profile_id"],
                "domain": profile["domain"],
                "condition": condition,
                "model": MODEL,
                "temperature": TEMPERATURE,
                "prompt_hash": prompt_hash(prompt),
                "task": profile["task"],
                "content": content,
            }
            if condition == "akm_elicited":
                record["elicitation_prompt_hash"] = elicitation_prompt_hash
                record["elicitation_trace"] = elicited.get("elicitation_trace", [])
                record["elicited_akm_profile"] = elicited["akm_profile"]
            records.append(record)

    output_path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
