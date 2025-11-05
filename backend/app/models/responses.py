from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl


class SearchResult(BaseModel):
    symbol: str
    name: str
    exchange: Optional[str] = None
    assetType: Optional[str] = None


class MetricCard(BaseModel):
    label: str
    value: str
    delta: Optional[float] = None
    hint: Optional[str] = None


class CompanyProfile(BaseModel):
    symbol: str
    name: str
    currency: Optional[str] = None
    exchange: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    marketCap: Optional[float] = None
    website: Optional[HttpUrl] = None
    country: Optional[str] = None
    description: Optional[str] = None


class FinancialStatement(BaseModel):
    period: str
    data: Dict[str, float]


class Filing(BaseModel):
    accessionNumber: str
    formType: str
    filedAt: date
    reportUrl: Optional[HttpUrl] = None


class FinancialsResponse(BaseModel):
    symbol: str
    profile: CompanyProfile
    metrics: List[MetricCard]
    statements: Dict[str, List[FinancialStatement]]
    filings: List[Filing]


class PricePoint(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class IndicatorSeries(BaseModel):
    name: str
    data: List[Dict[str, Any]]


class ChartResponse(BaseModel):
    symbol: str
    range: str
    interval: str
    prices: List[PricePoint]
    indicators: Dict[str, IndicatorSeries]


class NewsItem(BaseModel):
    title: str
    url: HttpUrl
    source: Optional[str] = None
    publishedAt: datetime
    summary: Optional[str] = None
    thumbnail: Optional[HttpUrl] = None
    relatedTickers: List[str] = Field(default_factory=list)
    videoUrl: Optional[HttpUrl] = None


class NewsResponse(BaseModel):
    symbol: str
    items: List[NewsItem]


class VideoItem(BaseModel):
    id: str
    title: str
    url: HttpUrl
    videoUrl: HttpUrl
    channel: Optional[str] = None
    description: Optional[str] = None
    publishedAt: datetime
    thumbnail: Optional[HttpUrl] = None


class VideosResponse(BaseModel):
    query: str
    items: List[VideoItem]


class Insight(BaseModel):
    title: str
    body: str
    sentiment: Optional[str] = None


class InsightsResponse(BaseModel):
    symbol: str
    highlights: List[str]
    metrics: List[MetricCard]
    narrative: str
    relatedNews: List[NewsItem]
    technicalView: Dict[str, Any]


class ComparisonRequest(BaseModel):
    symbols: List[str]
    baseline: Optional[str] = None


class ComparisonEntry(BaseModel):
    symbol: str
    profile: CompanyProfile
    metrics: List[MetricCard]


class ComparisonResponse(BaseModel):
    entries: List[ComparisonEntry]
    correlations: Dict[str, float]


class AnalyzeRequest(BaseModel):
    symbol: str
    question: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class AnalyzeResponse(BaseModel):
    summary: str
    source: str
