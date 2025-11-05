from __future__ import annotations

from typing import Any, Dict

from . import analytics, market, news, nlp


async def build_insights(symbol: str) -> Dict[str, Any]:
    metrics = await market.get_key_metrics(symbol)
    highlights = analytics.extract_highlights(metrics)
    macd, rsi = await market.get_macd(symbol), await market.get_rsi(symbol)
    technical_view = analytics.summarize_technical_view(macd, rsi)
    news_items = await news.get_news(symbol)
    top_headline = news_items[0]["title"] if news_items else None
    narrative = nlp.compose_narrative(symbol, highlights, top_headline, technical_view)
    return {
        "symbol": symbol.upper(),
        "highlights": highlights,
        "metrics": metrics,
        "technicalView": technical_view,
        "news": news_items[:5],
        "narrative": narrative,
    }
