from __future__ import annotations

from typing import Dict, List

from .data_loader import load_news


def news_for_symbol(symbol: str) -> List[Dict[str, str]]:
    return load_news().get(symbol, [])


def aggregate_sentiment(symbol: str) -> Dict[str, float]:
    items = news_for_symbol(symbol)
    if not items:
        return {"sentiment": 0.0}
    score = sum(item.get("sentiment", 0.0) for item in items) / len(items)
    return {"sentiment": score}
