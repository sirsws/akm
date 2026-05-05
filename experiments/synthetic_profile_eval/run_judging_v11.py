"""
文件：run_judging_v11.py
核心功能：v1.1 supplement —— 用 v1.0 同款 3 跨族 judge（DeepSeek-V4-pro / Gemini 3 Flash / Grok 4.3）
        盲评 v1.1 新生成的 800 generations（4 generator × 50 personas × 4 conditions）。
        每条 generation 过 3 judges = 2400 新 judgments。
        与 v1.0 一致：同一 (generator, profile_id) 三个 judge 看到的匿名标签顺序一致。
输入：profiles.jsonl、outputs/v1.1/generations_<gen_id>.jsonl（来自 run_generation_v11.py）、
     prompts/judge.md、DEEPSEEK_API_KEY、OpenRouter key（ora.txt）。
输出：outputs/v1.1/judgments_<judge_id>__<generator_id>.jsonl（按行增量，断点可续），
     含 profile_id、generator_id、judge_id、label_map、judgment JSON、prompt_hash 与 raw_judgment。
维护要求：仅在 v1.1 generations 上跑；不要触碰 v1.0 outputs/v1/。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from openrouter_client import call_openrouter, load_openrouter_key


ROOT = Path(__file__).resolve().parent
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
TEMPERATURE = 0.0
MAX_TOKENS = 2400
RETRIES = 3
RETRY_BACKOFF = 5.0


JUDGES = {
    "deepseek_v4_pro": {
        "kind": "deepseek",
        "model": "deepseek-v4-pro",
    },
    "gemini_3_flash": {
        "kind": "openrouter",
        "model": "google/gemini-3-flash-preview",
    },
    "grok_4_3": {
        "kind": "openrouter",
        "model": "x-ai/grok-4.3",
    },
}

GENERATORS = ["gpt_5_4_mini", "qwen_3_6_plus", "kimi_k2_6", "glm_5_1", "gemma_4_31b_it", "deepseek_v4_pro"]


def load_deepseek_key() -> str:
    env = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if env:
        return env
    fallback = Path(r"G:\对话集\顾问团\dsapi.txt")
    if fallback.exists():
        text = fallback.read_text(encoding="utf-8").strip()
        if text:
            return text
    raise RuntimeError("DEEPSEEK_API_KEY missing")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]


def call_deepseek_judge(api_key: str, model: str, prompt: str) -> str:
    payload = {
        "model": model,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "thinking": {"type": "disabled"},
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "你是一个只返回合法 JSON 的严格评估器。"},
            {"role": "user", "content": prompt},
        ],
    }
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
                raise RuntimeError(str(data["error"]))
            content = data["choices"][0]["message"]["content"]
            if not content or not str(content).strip():
                raise RuntimeError("Empty content")
            return str(content)
        except (urllib.error.HTTPError, urllib.error.URLError, RuntimeError, json.JSONDecodeError) as exc:
            last_err = exc
            err_body = ""
            if isinstance(exc, urllib.error.HTTPError):
                try:
                    err_body = exc.read().decode("utf-8", errors="replace")[:300]
                except OSError:
                    err_body = "<unreadable>"
            print(f"  [WARN] {model} attempt {attempt}/{RETRIES} failed: {exc}; body: {err_body}", file=sys.stderr)
            if attempt < RETRIES:
                time.sleep(RETRY_BACKOFF * attempt)
    raise RuntimeError(f"DeepSeek judge {model} failed after retries: {last_err}")


def group_generations(records: list[dict]) -> dict[str, dict[str, dict]]:
    grouped: dict[str, dict[str, dict]] = {}
    for record in records:
        grouped.setdefault(record["profile_id"], {})[record["condition"]] = record
    return grouped


def deterministic_label_map(generator_id: str, profile_id: str, conditions: list[str]) -> tuple[list[str], dict[str, str]]:
    """Return (labels, label_to_condition) with deterministic shuffle per (generator, profile_id).
    Same (gen, profile) gets same anonymous order across all 3 judges, but different generators
    can have different orders for the same profile.
    """
    sorted_conditions = sorted(conditions)
    rng = random.Random(f"akm-v1.1-{generator_id}-{profile_id}")
    shuffled = sorted_conditions[:]
    rng.shuffle(shuffled)
    labels = [f"answer_{chr(97 + idx)}" for idx in range(len(shuffled))]
    return labels, dict(zip(labels, shuffled))


def loaded_profile_ids(output_path: Path) -> set[str]:
    if not output_path.exists():
        return set()
    return {
        json.loads(line)["profile_id"]
        for line in output_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def run_for_judge_generator(judge_id: str, judge_cfg: dict, generator_id: str,
                            profiles: dict, generations: dict, judge_template: str,
                            deepseek_key: str | None, openrouter_key: str | None) -> tuple[int, int]:
    output_path = ROOT / "outputs" / "v1.1" / f"judgments_{judge_id}__{generator_id}.jsonl"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    done = loaded_profile_ids(output_path)
    targets = sorted(generations.keys())
    print(f"[{judge_id}|{generator_id}] Resume: {len(done)}/{len(targets)} done")
    fails: list[tuple[str, str]] = []
    ok_count = 0
    with output_path.open("a", encoding="utf-8") as fout:
        for i, profile_id in enumerate(targets, 1):
            if profile_id in done:
                continue
            profile = profiles[profile_id]
            cond_records = generations[profile_id]
            if len(cond_records) < 4:
                print(f"  [{judge_id}|{generator_id}] {profile_id}: incomplete ({list(cond_records)}), skip")
                fails.append((profile_id, "incomplete_generations"))
                continue
            labels, label_map = deterministic_label_map(generator_id, profile_id, list(cond_records.keys()))
            anonymous_answers = {label: cond_records[label_map[label]]["content"] for label in labels}
            prompt = judge_template.format(
                persona=json.dumps(profile["persona"], ensure_ascii=False, indent=2),
                task=profile["task"],
                anonymous_answers=json.dumps(anonymous_answers, ensure_ascii=False, indent=2),
            )
            try:
                if judge_cfg["kind"] == "deepseek":
                    raw = call_deepseek_judge(deepseek_key, judge_cfg["model"], prompt)
                else:
                    raw = call_openrouter(
                        judge_cfg["model"],
                        prompt,
                        temperature=TEMPERATURE,
                        max_tokens=MAX_TOKENS,
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
                parsed = json.loads(cleaned)
            except (urllib.error.HTTPError, urllib.error.URLError, RuntimeError, json.JSONDecodeError, KeyError) as exc:
                print(f"  [{judge_id}|{generator_id}] {profile_id}: ERROR {exc}", file=sys.stderr)
                fails.append((profile_id, str(exc)[:200]))
                continue

            record = {
                "profile_id": profile_id,
                "domain": profile["domain"],
                "generator_id": generator_id,
                "judge_id": judge_id,
                "judge_model": judge_cfg["model"],
                "temperature": TEMPERATURE,
                "prompt_hash": prompt_hash(prompt),
                "label_map": label_map,
                "judgment": parsed,
                "raw_judgment": raw,
            }
            fout.write(json.dumps(record, ensure_ascii=False) + "\n")
            fout.flush()
            ok_count += 1
            print(f"  [{judge_id}|{generator_id}] [{i}/{len(targets)}] {profile_id}: OK")
    if fails:
        print(f"[{judge_id}|{generator_id}] FAILED: {len(fails)}")
        for pid, why in fails:
            print(f"    {pid}: {why}")
    return ok_count, len(fails)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--judge", choices=list(JUDGES) + ["all"], default="all")
    parser.add_argument("--generator", choices=GENERATORS + ["all"], default="all",
                        help="Which v1.1 generator's outputs to judge.")
    args = parser.parse_args()

    profiles = {r["profile_id"]: r for r in read_jsonl(ROOT / "profiles.jsonl")}
    judge_template = read_text(ROOT / "prompts" / "judge.md")

    deepseek_key = load_deepseek_key()
    openrouter_key = load_openrouter_key()

    target_judges = list(JUDGES.keys()) if args.judge == "all" else [args.judge]
    target_generators = GENERATORS if args.generator == "all" else [args.generator]

    summary: list[tuple[str, str, int, int]] = []
    for gen_id in target_generators:
        if gen_id == "deepseek_v4_pro":
            gen_path = ROOT / "outputs" / "v1" / "generations.jsonl"
        else:
            gen_path = ROOT / "outputs" / "v1.1" / f"generations_{gen_id}.jsonl"
        if not gen_path.exists():
            print(f"[skip] {gen_id} generations file missing: {gen_path}")
            continue
        generations = group_generations(read_jsonl(gen_path))
        for jid in target_judges:
            ok, fail = run_for_judge_generator(
                jid, JUDGES[jid], gen_id, profiles, generations, judge_template,
                deepseek_key, openrouter_key,
            )
            summary.append((jid, gen_id, ok, fail))

    print("\n=== v1.1 judging summary ===")
    for jid, gid, ok, fail in summary:
        print(f"  {jid:18} x {gid:18} ok={ok:3} fail={fail:3}")


if __name__ == "__main__":
    main()
