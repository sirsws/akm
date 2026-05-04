"""
文件：run_generation.py
核心功能：调用 DeepSeek-V4-pro（thinking disabled），为每个 synthetic persona 生成 no_profile、unstructured_notes、akm_profile、akm_elicited 四组回答，并记录 akm_elicited 的画像生成链路。
输入：profiles.jsonl、prompts/generate_*.md、prompts/elicit_akm_profile.md、DEEPSEEK_API_KEY 环境变量（或回退 G:\\对话集\\顾问团\\dsapi.txt）。
输出：outputs/v1/generations.jsonl，含完整原始输出、模型名、温度、prompt hash、条件标签，以及 akm_elicited 的生成画像和追问记录；按行增量写入，断点可续。
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-v4-pro"
TEMPERATURE = 0.2
MAX_TOKENS = 1500
PROFILE_MAX_TOKENS = 2200
RETRIES = 3
RETRY_BACKOFF = 5.0
CONDITIONS = ["no_profile", "unstructured_notes", "akm_profile", "akm_elicited"]


def load_deepseek_key() -> str:
    env = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if env:
        return env
    fallback = Path(r"G:\对话集\顾问团\dsapi.txt")
    if fallback.exists():
        text = fallback.read_text(encoding="utf-8").strip()
        if text:
            return text
    raise RuntimeError("DEEPSEEK_API_KEY not set and dsapi.txt not found / empty")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def read_profiles(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]


def _post(api_key: str, payload: dict) -> dict:
    last_err: Exception | None = None
    for attempt in range(1, RETRIES + 1):
        request = urllib.request.Request(
            API_URL,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                body = response.read().decode("utf-8")
            data = json.loads(body)
            if "error" in data:
                raise RuntimeError(f"DeepSeek error: {data['error']}")
            return data
        except (urllib.error.HTTPError, urllib.error.URLError, RuntimeError, json.JSONDecodeError) as exc:
            last_err = exc
            err_body = ""
            if isinstance(exc, urllib.error.HTTPError):
                try:
                    err_body = exc.read().decode("utf-8", errors="replace")[:400]
                except Exception:
                    err_body = "<unreadable>"
            print(f"  [WARN] DeepSeek attempt {attempt}/{RETRIES} failed: {exc}; body: {err_body}", file=sys.stderr)
            if attempt < RETRIES:
                time.sleep(RETRY_BACKOFF * attempt)
    raise RuntimeError(f"DeepSeek call failed after {RETRIES} retries: {last_err}")


def call_deepseek(api_key: str, prompt: str) -> str:
    payload = {
        "model": MODEL,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "thinking": {"type": "disabled"},
        "messages": [
            {"role": "system", "content": "你是一个严谨、简洁、可执行的中文 AI 助手。"},
            {"role": "user", "content": prompt},
        ],
    }
    data = _post(api_key, payload)
    content = data["choices"][0]["message"]["content"]
    if not content or not str(content).strip():
        raise RuntimeError("Empty content from DeepSeek")
    return str(content)


def call_deepseek_json(api_key: str, prompt: str) -> dict:
    payload = {
        "model": MODEL,
        "temperature": TEMPERATURE,
        "max_tokens": PROFILE_MAX_TOKENS,
        "thinking": {"type": "disabled"},
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "你是一个严格的 AKM 用户画像诱导器，只返回合法 JSON。"},
            {"role": "user", "content": prompt},
        ],
    }
    data = _post(api_key, payload)
    content = data["choices"][0]["message"]["content"]
    if not content or not str(content).strip():
        raise RuntimeError("Empty JSON content from DeepSeek")
    return json.loads(content)


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


def load_done_keys(output_path: Path) -> set[tuple[str, str]]:
    done: set[tuple[str, str]] = set()
    if not output_path.exists():
        return done
    for line in output_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        done.add((rec["profile_id"], rec["condition"]))
    return done


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    api_key = load_deepseek_key()
    profiles = read_profiles(ROOT / "profiles.jsonl")
    templates = {
        "no_profile": read_text(ROOT / "prompts" / "generate_no_profile.md"),
        "unstructured_notes": read_text(ROOT / "prompts" / "generate_user_notes.md"),
        "akm_profile": read_text(ROOT / "prompts" / "generate_akm_profile.md"),
        "akm_elicited": read_text(ROOT / "prompts" / "generate_akm_profile.md"),
    }
    elicitation_template = read_text(ROOT / "prompts" / "elicit_akm_profile.md")
    output_dir = ROOT / "outputs" / "v1"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "generations.jsonl"

    done = load_done_keys(output_path)
    print(f"Resuming: {len(done)} records already on disk; total target {len(profiles) * len(CONDITIONS)}")

    with output_path.open("a", encoding="utf-8") as fout:
        for idx, profile in enumerate(profiles, 1):
            elicited: dict | None = None
            elicitation_prompt_hash = ""
            for condition in CONDITIONS:
                key = (profile["profile_id"], condition)
                if key in done:
                    print(f"  [{idx}/{len(profiles)}] {profile['profile_id']} {condition}: SKIP (cached)")
                    continue
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
                fout.write(json.dumps(record, ensure_ascii=False) + "\n")
                fout.flush()
                done.add(key)
                print(f"  [{idx}/{len(profiles)}] {profile['profile_id']} {condition}: OK")


if __name__ == "__main__":
    main()
