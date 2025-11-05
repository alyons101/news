from __future__ import annotations

from typing import Dict, List

from .data_loader import load_news


SUMMARY_TEMPLATE = (
    "{symbol} highlights: Revenue ${revenue}B, EPS ${eps}. "
    "Sentiment leaning {sentiment}. Latest headline: {headline}."
)


SENTIMENT_BUCKETS = {
    "bullish": 0.25,
    "neutral": -0.15,
    "bearish": -1.0,
}


def bucket_sentiment(score: float) -> str:
    for label, threshold in SENTIMENT_BUCKETS.items():
        if score >= threshold:
            return label
    return "bearish"


def summarize_symbol(symbol: str, revenue: float, eps: float) -> Dict[str, str]:
    news_items: List[Dict[str, str]] = load_news().get(symbol, [])
    if news_items:
        top_story = max(news_items, key=lambda item: item.get("sentiment", 0.0))
        headline = top_story.get("title", "No headline")
        sentiment = bucket_sentiment(top_story.get("sentiment", 0.0))
    else:
        headline = "No current coverage"
        sentiment = "neutral"
    summary = SUMMARY_TEMPLATE.format(
        symbol=symbol,
        revenue=round(revenue / 1000, 1),
        eps=round(eps, 2),
        sentiment=sentiment,
        headline=headline,
    )
    return {"symbol": symbol, "summary": summary}
