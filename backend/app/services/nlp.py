from __future__ import annotations

from typing import Any, Dict, List, Optional


def compose_narrative(symbol: str, highlights: List[str], news_headline: Optional[str], technical: Dict[str, Any]) -> str:
    sections = [f"Snapshot for {symbol.upper()}."]
    if highlights:
        sections.append(" ".join(highlights))
    if technical:
        macd = technical.get("macd")
        rsi = technical.get("rsi")
        if macd:
            sections.append(macd.get("narrative", ""))
        if rsi:
            sections.append(rsi.get("narrative", ""))
    if news_headline:
        sections.append(f"Latest headline: {news_headline}.")
    return " ".join(section for section in sections if section)
