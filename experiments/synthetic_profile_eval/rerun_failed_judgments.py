"""
文件：rerun_failed_judgments.py
核心功能：扫描某 (judge, generator) 已写 judgments_*.jsonl，找出缺失的 profile_id，重新调一次模型补齐。
        支持指定 max_retry 和 max_tokens 加大；若仍失败则降级到只取数值字段、丢弃 raw 末尾乱码。
        失败的 JSON 可由 DS 做 format_repair 二次抢救。
输入：--judge / --generator / --max-tokens / --max-retry
输出：追加到 outputs/v1.1/judgments_<judge>__<generator>.jsonl
维护要求：仅用于"个别失败补齐"场景；不要替代主 run_judging_v11.py。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

from openrouter_client import call_openrouter, load_openrouter_key
from run_judging_v11 import (
    JUDGES,
    GENERATORS,
    call_deepseek_judge,
    deterministic_label_map,
    group_generations,
    load_deepseek_key,
    read_jsonl,
    read_text,
)


ROOT = Path(__file__).resolve().parent
TEMPERATURE = 0.0


def repair_with_ds(ds_key: str, raw: str, max_tokens: int = 3000) -> dict:
    """Use DS to repair structurally broken judge JSON. Returns parsed dict."""
    repair_prompt = (
        "下面是一个本应是合法 JSON 的 judge 评分输出，但解析失败（可能是 truncate / 多余数据 / 字符串未闭合）。"
        "请只修结构不改语义内容，返回唯一一个合法 JSON 对象（不要 Markdown 包装，不要拼接多个 JSON）。"
        "保留所有 answer_a/b/c/d 的评分字段（constraint_adherence、risk_control、specificity、actionability、"
        "personal_fit、tradeoff_awareness）以及 satisfied_constraints / missed_constraints / risk_violations / "
        "profile_details_used / best_answer_label。\n\n"
        f"原始输出：\n```\n{raw[:6000]}\n```\n\n只返回合法 JSON。"
    )
    payload = {
        "model": "deepseek-v4-pro",
        "temperature": 0.0,
        "max_tokens": max_tokens,
        "thinking": {"type": "disabled"},
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "你是一个严格的 JSON 修复器。"},
            {"role": "user", "content": repair_prompt},
        ],
    }
    import urllib.request, urllib.error
    request = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {ds_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        body = response.read().decode("utf-8")
    data = json.loads(body)
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def parse_with_repair(raw: str, ds_key: str) -> tuple[dict, bool]:
    """Try to parse JSON; if fails, ask DS to repair. Returns (parsed, was_repaired)."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
    try:
        return json.loads(cleaned), False
    except json.JSONDecodeError:
        pass
    # Try truncating to last balanced } (for "Extra data" errors)
    last_brace = cleaned.rfind("}")
    if last_brace > 0:
        try:
            return json.loads(cleaned[: last_brace + 1]), True
        except json.JSONDecodeError:
            pass
    # Last resort: DS repair
    return repair_with_ds(ds_key, raw), True


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--judge", required=True, choices=list(JUDGES))
    parser.add_argument("--generator", required=True, choices=GENERATORS)
    parser.add_argument("--max-tokens", type=int, default=4500, help="Larger token budget for retry.")
    parser.add_argument("--max-retry", type=int, default=3)
    args = parser.parse_args()

    profiles = {r["profile_id"]: r for r in read_jsonl(ROOT / "profiles.jsonl")}
    judge_template = read_text(ROOT / "prompts" / "judge.md")
    judge_cfg = JUDGES[args.judge]

    if args.generator == "deepseek_v4_pro":
        gen_path = ROOT / "outputs" / "v1" / "generations.jsonl"
    else:
        gen_path = ROOT / "outputs" / "v1.1" / f"generations_{args.generator}.jsonl"
    gens = group_generations(read_jsonl(gen_path))

    out_path = ROOT / "outputs" / "v1.1" / f"judgments_{args.judge}__{args.generator}.jsonl"
    done = set()
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["profile_id"])

    targets = sorted(set(gens.keys()) - done)
    if not targets:
        print(f"[{args.judge}|{args.generator}] no missing profiles; nothing to do")
        return

    print(f"[{args.judge}|{args.generator}] missing {len(targets)}: {targets}")

    ds_key = load_deepseek_key()
    openrouter_key = load_openrouter_key() if judge_cfg["kind"] == "openrouter" else None

    repaired_count = 0
    fail_count = 0
    with out_path.open("a", encoding="utf-8") as fout:
        for pid in targets:
            cond_records = gens[pid]
            if len(cond_records) < 4:
                print(f"  {pid}: incomplete generations, skip")
                fail_count += 1
                continue
            labels, label_map = deterministic_label_map(args.generator, pid, list(cond_records.keys()))
            anonymous_answers = {label: cond_records[label_map[label]]["content"] for label in labels}
            prompt = judge_template.format(
                persona=json.dumps(profiles[pid]["persona"], ensure_ascii=False, indent=2),
                task=profiles[pid]["task"],
                anonymous_answers=json.dumps(anonymous_answers, ensure_ascii=False, indent=2),
            )
            success = False
            for attempt in range(1, args.max_retry + 1):
                try:
                    if judge_cfg["kind"] == "deepseek":
                        raw = call_deepseek_judge(ds_key, judge_cfg["model"], prompt)
                    else:
                        raw = call_openrouter(
                            judge_cfg["model"], prompt,
                            temperature=TEMPERATURE, max_tokens=args.max_tokens,
                            response_format_json=True, api_key=openrouter_key,
                            retries=2, retry_backoff=4.0,
                        )
                    parsed, was_repaired = parse_with_repair(raw, ds_key)
                    if was_repaired:
                        repaired_count += 1
                    rec = {
                        "profile_id": pid,
                        "domain": profiles[pid]["domain"],
                        "generator_id": args.generator,
                        "judge_id": args.judge,
                        "judge_model": judge_cfg["model"],
                        "temperature": TEMPERATURE,
                        "prompt_hash": hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16],
                        "label_map": label_map,
                        "judgment": parsed,
                        "raw_judgment": raw,
                        "rerun_attempt": attempt,
                        "repaired": was_repaired,
                    }
                    fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    fout.flush()
                    print(f"  {pid}: OK (attempt {attempt}, repaired={was_repaired})")
                    success = True
                    break
                except (json.JSONDecodeError, RuntimeError) as exc:
                    print(f"  {pid}: attempt {attempt}/{args.max_retry} failed: {type(exc).__name__}: {str(exc)[:200]}", file=sys.stderr)
                    if attempt < args.max_retry:
                        time.sleep(5 * attempt)
            if not success:
                fail_count += 1
                print(f"  {pid}: GIVE UP after {args.max_retry} attempts", file=sys.stderr)

    print(f"\n[{args.judge}|{args.generator}] done. repaired={repaired_count}, fail={fail_count}")


if __name__ == "__main__":
    main()
