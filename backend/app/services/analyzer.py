from __future__ import annotations

from typing import Any, Dict

from fastapi.concurrency import run_in_threadpool

from ..core.config import settings
from . import nlp

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - optional dependency fallback
    OpenAI = None  # type: ignore


async def analyze(symbol: str, prompt: str | None, context: Dict[str, Any]) -> Dict[str, str]:
    if settings.openai_api_key and OpenAI is not None:
        client = OpenAI(api_key=settings.openai_api_key)
        question = prompt or "Provide a market update."
        messages = [
            {
                "role": "system",
                "content": "You are Aurora, an institutional market strategist focused on factual financial analysis.",
            },
            {
                "role": "user",
                "content": f"Symbol: {symbol}. Context: {context}. Question: {question}",
            },
        ]

        def _call_openai() -> str:
            completion = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
            return completion.choices[0].message.content or "No response received."

        summary = await run_in_threadpool(_call_openai)
        return {"summary": summary, "source": "openai"}

    highlights = context.get("highlights") or []
    technical = context.get("technical", {})
    headline = context.get("headline")
    summary = nlp.compose_narrative(symbol, highlights, headline, technical)
    if prompt:
        summary = f"{summary} Additional question: {prompt}.".strip()
    return {"summary": summary, "source": "aurora-offline"}
