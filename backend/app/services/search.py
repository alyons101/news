from __future__ import annotations

from typing import List

import httpx

from ..core.config import settings


async def search_symbols(query: str, limit: int = 8) -> List[dict]:
    if not query:
        return []
    params = {
        "q": query,
        "quotesCount": limit,
        "newsCount": 0,
        "enableFuzzyQuery": "true",
        "lang": "en-US",
        "region": settings.yahoo_region,
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get("https://query2.finance.yahoo.com/v1/finance/search", params=params)
        response.raise_for_status()
        payload = response.json()
    quotes = payload.get("quotes", [])
    results = []
    for item in quotes[:limit]:
        results.append(
            {
                "symbol": item.get("symbol"),
                "name": item.get("longname") or item.get("shortname") or item.get("symbol"),
                "exchange": item.get("exchange"),
                "assetType": item.get("quoteType"),
            }
        )
    return results
