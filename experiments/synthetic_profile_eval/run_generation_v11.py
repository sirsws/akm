"""
文件：run_generation_v11.py
核心功能：v1.1 multi-generator supplement —— 把 v1.0 单生成器（DeepSeek-V4-pro）扩展到 5 家跨家族 generator。
        本脚本通过 --generator 参数选择 OpenRouter 模型（GPT-5.4-mini / Qwen3.6-Plus / Kimi-K2.6 / GLM-5.1）
        或 DS 原生 API；输出按 generator 分文件，断点续传。
        任何结构性损坏（空响应 / 截断）→ 调 DS-V4-pro 做 format_repair（只修格式不改语义），
        所有修复事件落 outputs/v1.1/format_repair_log.jsonl，supplement 中诚实声明。
输入：profiles.jsonl、prompts/generate_*.md、prompts/elicit_akm_profile.md、ora.txt（OpenRouter）、dsapi.txt（DS 原生 + format_repair）。
输出：outputs/v1.1/generations_<generator_slug>.jsonl（增量写入，断点可续）；
     outputs/v1.1/format_repair_log.jsonl（按事件追加）；
     outputs/v1.1/gen_<generator_slug>_log.txt（stdout 镜像，便于事后审计）。
维护要求：v1.1 supplement 不允许粉饰反例。任何 generator 上 AKM 优势消失/反向 → 必须诚实写入 supplement。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from openrouter_client import call_openrouter, load_openrouter_key


ROOT = Path(__file__).resolve().parent
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
TEMPERATURE = 0.2
MAX_TOKENS = 1500
PROFILE_MAX_TOKENS = 2200
RETRIES = 3
RETRY_BACKOFF = 5.0
CONDITIONS = ["no_profile", "unstructured_notes", "akm_profile", "akm_elicited"]

GENERATORS = {
    "gpt_5_4_mini": {
        "kind": "openrouter",
        "model": "openai/gpt-5.4-mini",
        "family": "OpenAI",
    },
    "qwen_3_6_plus": {
        "kind": "openrouter",
        "model": "qwen/qwen3.6-plus",
        "family": "Alibaba",
    },
    "kimi_k2_6": {
        "kind": "openrouter",
        "model": "moonshotai/kimi-k2.6",
        "family": "Moonshot",
    },
    "glm_5_1": {
        "kind": "openrouter",
        "model": "z-ai/glm-5.1",
        "family": "Zhipu",
    },
    "gemma_4_31b_it": {
        "kind": "openrouter",
        "model": "google/gemma-4-31b-it",
        "family": "Google",
    },
    "deepseek_v4_pro": {
        "kind": "deepseek",
        "model": "deepseek-v4-pro",
        "family": "DeepSeek",
    },
}


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


def _ds_post(api_key: str, payload: dict) -> dict:
    last_err: Exception | None = None
    for attempt in range(1, RETRIES + 1):
        request = urllib.request.Request(
            DEEPSEEK_URL,
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
                except OSError:
                    err_body = "<unreadable>"
            print(f"  [WARN] DeepSeek attempt {attempt}/{RETRIES} failed: {exc}; body: {err_body}", file=sys.stderr)
            if attempt < RETRIES:
                time.sleep(RETRY_BACKOFF * attempt)
    raise RuntimeError(f"DeepSeek call failed after {RETRIES} retries: {last_err}")


def call_deepseek_text(api_key: str, prompt: str, max_tokens: int = MAX_TOKENS) -> str:
    payload = {
        "model": "deepseek-v4-pro",
        "temperature": TEMPERATURE,
        "max_tokens": max_tokens,
        "thinking": {"type": "disabled"},
        "messages": [
            {"role": "system", "content": "你是一个严谨、简洁、可执行的中文 AI 助手。"},
            {"role": "user", "content": prompt},
        ],
    }
    data = _ds_post(api_key, payload)
    content = data["choices"][0]["message"]["content"]
    if not content or not str(content).strip():
        raise RuntimeError("Empty content from DeepSeek")
    return str(content)


def call_deepseek_json(api_key: str, prompt: str, max_tokens: int = PROFILE_MAX_TOKENS,
                       system: str = "你是一个严格的 AKM 用户画像诱导器，只返回合法 JSON。") -> dict:
    payload = {
        "model": "deepseek-v4-pro",
        "temperature": TEMPERATURE,
        "max_tokens": max_tokens,
        "thinking": {"type": "disabled"},
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    }
    data = _ds_post(api_key, payload)
    content = data["choices"][0]["message"]["content"]
    if not content or not str(content).strip():
        raise RuntimeError("Empty JSON content from DeepSeek")
    return json.loads(content)


def call_openrouter_text(model: str, prompt: str, openrouter_key: str, max_tokens: int = MAX_TOKENS) -> str:
    return call_openrouter(
        model,
        prompt,
        temperature=TEMPERATURE,
        max_tokens=max_tokens,
        api_key=openrouter_key,
        retries=RETRIES,
        retry_backoff=RETRY_BACKOFF,
    )


def call_openrouter_json(model: str, prompt: str, openrouter_key: str, max_tokens: int = PROFILE_MAX_TOKENS) -> dict:
    raw = call_openrouter(
        model,
        prompt,
        temperature=TEMPERATURE,
        max_tokens=max_tokens,
        response_format_json=True,
        api_key=openrouter_key,
        retries=RETRIES,
        retry_backoff=RETRY_BACKOFF,
    )
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
    return json.loads(cleaned)


def format_repair(ds_key: str, raw: str, expected: str, repair_log_fout) -> dict:
    """Use DS-V4-pro to repair structurally broken JSON. Returns parsed dict.
    expected: 'akm_profile_json' for elicit step.
    Logs every repair event for honest disclosure in supplement.
    """
    repair_prompt = (
        f"下面是一个本应是合法 JSON 的输出，但解析失败。请只修格式不改语义，"
        f"返回符合以下结构的合法 JSON：\n\n"
        f'期望结构：包含 "elicitation_trace"（数组，每项含 question 与 simulated_user_answer）'
        f'和 "akm_profile"（对象，含 goals/hard_constraints/soft_preferences/available_assets/risk_boundaries/decision_style）。\n\n'
        f"原始输出：\n```\n{raw[:4000]}\n```\n\n"
        f"只返回合法 JSON，不要 Markdown 包装。"
    )
    fixed = call_deepseek_json(
        ds_key,
        repair_prompt,
        max_tokens=2400,
        system="你是一个严格的 JSON 格式修复器，只修结构不改语义内容。",
    )
    repair_log_fout.write(json.dumps({
        "expected": expected,
        "raw_preview": raw[:500],
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }, ensure_ascii=False) + "\n")
    repair_log_fout.flush()
    return fixed


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


def elicit_for_generator(cfg: dict, template: str, profile: dict,
                         openrouter_key: str | None, ds_key: str,
                         repair_log_fout) -> tuple[dict, str, bool]:
    """Run elicitation for the chosen generator. Returns (parsed, prompt_hash, was_repaired)."""
    prompt = template.format(
        persona=json.dumps(profile["persona"], ensure_ascii=False, indent=2),
        task=profile["task"],
    )
    p_hash = prompt_hash(prompt)
    was_repaired = False
    if cfg["kind"] == "deepseek":
        parsed = call_deepseek_json(ds_key, prompt)
    else:
        try:
            parsed = call_openrouter_json(cfg["model"], prompt, openrouter_key)
        except (json.JSONDecodeError, RuntimeError) as exc:
            print(f"  [REPAIR] {cfg['model']} elicit returned broken JSON: {exc}; calling DS format_repair", file=sys.stderr)
            try:
                raw = call_openrouter_text(cfg["model"], prompt, openrouter_key, max_tokens=PROFILE_MAX_TOKENS)
            except RuntimeError as inner_exc:
                raise RuntimeError(f"elicit failed and raw fetch also failed: {inner_exc}") from inner_exc
            parsed = format_repair(ds_key, raw, "akm_profile_json", repair_log_fout)
            was_repaired = True
    if "akm_profile" not in parsed:
        raise RuntimeError(f"elicit response missing akm_profile key: {list(parsed.keys())}")
    return parsed, p_hash, was_repaired


def call_for_generator(cfg: dict, prompt: str, openrouter_key: str | None, ds_key: str) -> str:
    if cfg["kind"] == "deepseek":
        return call_deepseek_text(ds_key, prompt)
    return call_openrouter_text(cfg["model"], prompt, openrouter_key)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--generator", required=True, choices=list(GENERATORS.keys()),
                        help="Which generator to run for v1.1 supplement.")
    parser.add_argument("--limit", type=int, default=0,
                        help="Optional cap on # personas (0 = all).")
    args = parser.parse_args()

    gen_id = args.generator
    cfg = GENERATORS[gen_id]
    print(f"[v1.1] generator={gen_id} model={cfg['model']} family={cfg['family']}")

    profiles = read_profiles(ROOT / "profiles.jsonl")
    if args.limit:
        profiles = profiles[: args.limit]

    templates = {
        "no_profile": read_text(ROOT / "prompts" / "generate_no_profile.md"),
        "unstructured_notes": read_text(ROOT / "prompts" / "generate_user_notes.md"),
        "akm_profile": read_text(ROOT / "prompts" / "generate_akm_profile.md"),
        "akm_elicited": read_text(ROOT / "prompts" / "generate_akm_profile.md"),
    }
    elicitation_template = read_text(ROOT / "prompts" / "elicit_akm_profile.md")

    out_dir = ROOT / "outputs" / "v1.1"
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / f"generations_{gen_id}.jsonl"
    repair_log_path = out_dir / "format_repair_log.jsonl"

    ds_key = load_deepseek_key()
    openrouter_key = load_openrouter_key() if cfg["kind"] == "openrouter" else None

    done = load_done_keys(output_path)
    target = len(profiles) * len(CONDITIONS)
    print(f"Resuming: {len(done)}/{target} records already on disk")

    fail_count = 0
    with output_path.open("a", encoding="utf-8") as fout, repair_log_path.open("a", encoding="utf-8") as rlog:
        for idx, profile in enumerate(profiles, 1):
            elicited: dict | None = None
            elicit_p_hash = ""
            elicit_was_repaired = False
            for condition in CONDITIONS:
                key = (profile["profile_id"], condition)
                if key in done:
                    print(f"  [{idx}/{len(profiles)}] {profile['profile_id']} {condition}: SKIP (cached)")
                    continue
                working = dict(profile)
                if condition == "akm_elicited":
                    if elicited is None:
                        try:
                            elicited, elicit_p_hash, elicit_was_repaired = elicit_for_generator(
                                cfg, elicitation_template, profile, openrouter_key, ds_key, rlog
                            )
                        except (RuntimeError, json.JSONDecodeError, KeyError) as exc:
                            print(f"  [{idx}/{len(profiles)}] {profile['profile_id']} elicit FAIL: {exc}", file=sys.stderr)
                            fail_count += 1
                            continue
                    working["elicited_akm_profile"] = elicited["akm_profile"]
                prompt = render_prompt(templates[condition], working, condition)
                try:
                    content = call_for_generator(cfg, prompt, openrouter_key, ds_key)
                except RuntimeError as exc:
                    print(f"  [{idx}/{len(profiles)}] {profile['profile_id']} {condition} FAIL: {exc}", file=sys.stderr)
                    fail_count += 1
                    continue
                record = {
                    "profile_id": profile["profile_id"],
                    "domain": profile["domain"],
                    "condition": condition,
                    "generator_id": gen_id,
                    "generator_model": cfg["model"],
                    "generator_family": cfg["family"],
                    "temperature": TEMPERATURE,
                    "prompt_hash": prompt_hash(prompt),
                    "task": profile["task"],
                    "content": content,
                }
                if condition == "akm_elicited":
                    record["elicitation_prompt_hash"] = elicit_p_hash
                    record["elicitation_trace"] = elicited.get("elicitation_trace", [])
                    record["elicited_akm_profile"] = elicited["akm_profile"]
                    record["elicit_was_repaired"] = elicit_was_repaired
                fout.write(json.dumps(record, ensure_ascii=False) + "\n")
                fout.flush()
                done.add(key)
                print(f"  [{idx}/{len(profiles)}] {profile['profile_id']} {condition}: OK")

    print(f"[v1.1 {gen_id}] DONE. failures={fail_count}, total_target={target}, on_disk={len(done)}")


if __name__ == "__main__":
    main()
