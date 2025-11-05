from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class CompanySummary(BaseModel):
    symbol: str
    name: str
    sector: str
    industry: str
    marketCap: int
    description: str
    esgScore: int
    headquarters: str


class RatioBucket(BaseModel):
    valuation: Dict[str, float]
    profitability: Dict[str, float]
    liquidity: Dict[str, float]
    leverage: Dict[str, float]


class DashboardPayload(BaseModel):
    company: CompanySummary
    ratios: RatioBucket
    incomeStatement: List[Dict[str, Any]]
    technicals: Dict[str, Any]
    predictive: Dict[str, Any]
    volatility: Dict[str, Any]
    anomalies: Dict[str, Any]
    news: List[Dict[str, Any]]
    sentiment: Dict[str, Any]
    aiSummary: Dict[str, str]


class ComparisonRequest(BaseModel):
    symbols: List[str]


class ComparisonResponse(BaseModel):
    ratios: List[Dict[str, Any]]
    correlations: Dict[str, Any]
