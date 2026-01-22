#!/usr/bin/env python3
"""
Minimal client for SiliconFlow Anthropic-style /v1/messages API.
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests

DEFAULT_TIMEOUT = 60
RETRY_STATUS = {429, 500, 502, 503, 504}


def _normalize_messages_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/messages"):
        return base
    if base.endswith("/v1"):
        return f"{base}/messages"
    return f"{base}/v1/messages"


def _extract_text_blocks(content: Iterable[Dict[str, Any]]) -> str:
    parts: List[str] = []
    for block in content or []:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "text" and isinstance(block.get("text"), str):
            parts.append(block["text"])
    return "".join(parts).strip()


def messages_create(
    *,
    api_key: Optional[str],
    base_url: str,
    model: str,
    system: Optional[str],
    messages: List[Dict[str, str]],
    max_tokens: int,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    top_k: Optional[int] = None,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = 2,
    return_raw: bool = False,
) -> Any:
    if not api_key:
        raise ValueError("Missing API key. Set ANTHROPIC_API_KEY.")

    url = _normalize_messages_url(base_url)
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
    }
    if system:
        payload["system"] = system
    if temperature is not None:
        payload["temperature"] = temperature
    if top_p is not None:
        payload["top_p"] = top_p
    if top_k is not None:
        payload["top_k"] = top_k

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    last_error: Optional[Exception] = None
    for attempt in range(retries + 1):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        except requests.RequestException as exc:
            last_error = exc
            if attempt >= retries:
                raise
            time.sleep(1.5 * (attempt + 1))
            continue

        if response.status_code in RETRY_STATUS and attempt < retries:
            time.sleep(1.5 * (attempt + 1))
            continue

        if not response.ok:
            raise RuntimeError(
                f"SiliconFlow API error {response.status_code}: {response.text}"
            )

        data = response.json()
        text = _extract_text_blocks(data.get("content", []))
        if not text:
            raise RuntimeError(
                f"SiliconFlow response has no text blocks: {json.dumps(data)[:800]}"
            )
        return (text, data) if return_raw else text

    if last_error:
        raise last_error
    raise RuntimeError("SiliconFlow request failed unexpectedly.")
