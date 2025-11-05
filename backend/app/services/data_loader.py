from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _load_json(name: str) -> Any:
    path = DATA_DIR / name
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=None)
def load_companies() -> List[Dict[str, Any]]:
    return _load_json("sample_companies.json")


@lru_cache(maxsize=None)
def load_financials() -> Dict[str, Any]:
    return _load_json("sample_financials.json")


@lru_cache(maxsize=None)
def load_prices() -> Dict[str, Any]:
    return _load_json("sample_prices.json")


@lru_cache(maxsize=None)
def load_news() -> Dict[str, Any]:
    return _load_json("sample_news.json")
