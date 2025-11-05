from __future__ import annotations

from statistics import mean
from typing import Any, Dict, List


def extract_highlights(metrics: List[Dict[str, Any]]) -> List[str]:
    highlights: List[str] = []
    for metric in metrics:
        label = metric.get("label")
        value = metric.get("value")
        if not value or value == "-":
            continue
        if label == "Market Cap":
            highlights.append(f"Market cap stands at {value}.")
        elif label == "Revenue":
            highlights.append(f"Trailing revenue came in at {value}.")
        elif label == "Profit Margin":
            highlights.append(f"Profit margins are holding near {value}.")
        elif label == "P/E":
            highlights.append(f"Shares trade at a P/E of {value}.")
    if not highlights:
        highlights.append("No headline financial metrics available.")
    return highlights[:4]


def summarize_technical_view(macd: List[Dict[str, Any]], rsi: List[Dict[str, Any]]) -> Dict[str, Any]:
    view: Dict[str, Any] = {}
    if macd:
        latest = macd[0]
        trend = "bullish" if latest.get("macd", 0) > latest.get("signal", 0) else "bearish"
        view["macd"] = {
            "latest": latest,
            "trend": trend,
            "narrative": f"MACD histogram is {trend} with reading {latest.get('hist', 0):.2f}.",
        }
    if rsi:
        latest_rsi = rsi[0].get("value", 50)
        if latest_rsi >= 70:
            regime = "overbought"
        elif latest_rsi <= 30:
            regime = "oversold"
        else:
            regime = "neutral"
        view["rsi"] = {
            "latest": latest_rsi,
            "regime": regime,
            "narrative": f"RSI sits at {latest_rsi:.2f}, indicating {regime} conditions.",
        }
    return view


def average_indicator(series: List[Dict[str, Any]], key: str) -> float:
    if not series:
        return 0.0
    values = [item.get(key, 0.0) for item in series if item.get(key) is not None]
    return mean(values) if values else 0.0
