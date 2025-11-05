from __future__ import annotations

import difflib
from typing import Dict, List

from .data_loader import load_companies


class SearchService:
    def __init__(self) -> None:
        self._companies = load_companies()

    def search(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        query = query.upper()
        matches = difflib.get_close_matches(query, [c["symbol"] for c in self._companies], n=limit)
        ranked = []
        for company in self._companies:
            if query in company["symbol"] or query in company["name"].upper():
                ranked.append(company)
            elif company["symbol"] in matches:
                ranked.append(company)
        return ranked[:limit]


search_service = SearchService()
