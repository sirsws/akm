"""
文件：openrouter_client.py
核心功能：统一封装 OpenRouter chat/completions 调用，供多模型 judge 流水线复用。
输入：模型 ID、prompt、可选采样参数、可选模型 fallback 列表；从环境变量 OPENROUTER_API_KEY 或 ../../../../ora.txt 读 key。
输出：模型返回的字符串内容；失败时抛出异常并记录上下文。
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_TIMEOUT = 120
DEFAULT_RETRIES = 3
DEFAULT_RETRY_BACKOFF = 4.0


def load_openrouter_key() -> str:
    env_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if env_key:
        return env_key
    candidates = [
        Path(__file__).resolve().parents[4] / "ora.txt",
        Path(r"G:\对话集\顾问团\ora.txt"),
    ]
    for path in candidates:
        if path.exists():
            text = path.read_text(encoding="utf-8").strip()
            if text:
                return text
    raise RuntimeError(
        "OPENROUTER_API_KEY not set and ora.txt not found / empty"
    )


def call_openrouter(
    model: str,
    prompt: str,
    *,
    temperature: float = 0.0,
    max_tokens: int = 6000,
    response_format_json: bool = False,
    api_key: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    retry_backoff: float = DEFAULT_RETRY_BACKOFF,
    extra_headers: dict | None = None,
) -> str:
    """Call OpenRouter chat completions and return the message content string.

    The single-prompt design matches the existing judge / generator scripts.
    Raises RuntimeError after all retries exhaust.
    """
    if api_key is None:
        api_key = load_openrouter_key()

    payload: dict = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if response_format_json:
        payload["response_format"] = {"type": "json_object"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/sirsws/akm",
        "X-Title": "AKM Benchmark v1.0",
    }
    if extra_headers:
        headers.update(extra_headers)

    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        request = urllib.request.Request(
            OPENROUTER_URL,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8")
            data = json.loads(body)
            if "error" in data:
                raise RuntimeError(f"OpenRouter API error: {data['error']}")
            content = data["choices"][0]["message"]["content"]
            if content is None or not str(content).strip():
                raise RuntimeError("Empty content returned")
            return str(content)
        except (urllib.error.HTTPError, urllib.error.URLError, RuntimeError, KeyError, json.JSONDecodeError) as exc:
            last_error = exc
            err_body = ""
            if isinstance(exc, urllib.error.HTTPError):
                try:
                    err_body = exc.read().decode("utf-8", errors="replace")[:500]
                except Exception:
                    err_body = "<could not read error body>"
            print(
                f"  [WARN] {model} attempt {attempt}/{retries} failed: {exc}; body: {err_body}",
                file=sys.stderr,
            )
            if attempt < retries:
                time.sleep(retry_backoff * attempt)

    raise RuntimeError(f"OpenRouter call to {model} failed after {retries} retries: {last_error}")


def smoke_test(model: str) -> tuple[bool, str]:
    """Quick connectivity test. Returns (ok, message)."""
    try:
        reply = call_openrouter(
            model,
            "Reply with the single word PONG and nothing else.",
            temperature=0.0,
            max_tokens=20,
            retries=2,
        )
        ok = "PONG" in reply.upper()
        return ok, reply.strip()[:80]
    except Exception as exc:
        return False, f"ERROR: {exc}"


if __name__ == "__main__":
    targets = [
        "google/gemini-3-flash-preview",
        "x-ai/grok-4.3",
    ]
    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    sys.stdout.reconfigure(encoding="utf-8")
    for model in targets:
        ok, msg = smoke_test(model)
        flag = "OK" if ok else "FAIL"
        print(f"[{flag}] {model}: {msg}")
