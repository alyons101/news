from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, Query
from fastapi_cache.decorator import cache

from ..models.responses import (
    AnalyzeRequest,
    AnalyzeResponse,
    ChartResponse,
    ComparisonRequest,
    ComparisonResponse,
    FinancialStatement,
    FinancialsResponse,
    InsightsResponse,
    NewsResponse,
    PricePoint,
    SearchResult,
)
from ..services import analyzer, insights, market, news, search

router = APIRouter()


@router.get("/search", response_model=List[SearchResult])
@cache(expire=600)
async def search_symbols(query: str = Query(..., min_length=1)) -> List[SearchResult]:
    results = await search.search_symbols(query)
    return [SearchResult(**item) for item in results]


@router.get("/financials/{symbol}", response_model=FinancialsResponse)
@cache(expire=900)
async def get_financials(symbol: str) -> FinancialsResponse:
    try:
        profile_raw = await market.get_company_profile(symbol)
    except Exception as exc:  # pragma: no cover - network dependency
        raise HTTPException(status_code=404, detail=f"Unable to locate symbol {symbol}: {exc}") from exc

    statements_raw = await market.get_financial_statements(symbol)
    filings_raw = await market.get_recent_filings(symbol, profile=profile_raw)
    metrics = await market.get_key_metrics(symbol)

    statements = {
        key: [FinancialStatement(**item) for item in value]
        for key, value in statements_raw.items()
    }

    return FinancialsResponse(
        symbol=symbol.upper(),
        profile=profile_raw,
        metrics=metrics,
        statements=statements,
        filings=filings_raw,
    )


@router.get("/chart/{symbol}", response_model=ChartResponse)
@cache(expire=300)
async def get_chart(
    symbol: str,
    range_: str = Query("1y", alias="range"),
    interval: str = "1d",
) -> ChartResponse:
    prices_raw = await market.get_price_history(symbol, range_, interval)
    macd, rsi, bbands = await market.get_macd(symbol), await market.get_rsi(symbol), await market.get_bbands(symbol)
    prices = [PricePoint(**price) for price in prices_raw]
    indicators = {
        "macd": {"name": "MACD", "data": macd},
        "rsi": {"name": "RSI", "data": rsi},
        "bollinger": {"name": "Bollinger Bands", "data": bbands},
    }
    return ChartResponse(symbol=symbol.upper(), range=range_, interval=interval, prices=prices, indicators=indicators)


@router.get("/news/{symbol}", response_model=NewsResponse)
@cache(expire=300)
async def get_company_news(symbol: str) -> NewsResponse:
    items = await news.get_news(symbol)
    return NewsResponse(symbol=symbol.upper(), items=items)


@router.get("/insights/{symbol}", response_model=InsightsResponse)
async def get_insights(symbol: str) -> InsightsResponse:
    payload = await insights.build_insights(symbol)
    return InsightsResponse(
        symbol=payload["symbol"],
        highlights=payload["highlights"],
        metrics=payload["metrics"],
        narrative=payload["narrative"],
        relatedNews=payload["news"],
        technicalView=payload["technicalView"],
    )


@router.post("/compare", response_model=ComparisonResponse)
@cache(expire=600)
async def compare_symbols(request: ComparisonRequest) -> ComparisonResponse:
    if not request.symbols:
        raise HTTPException(status_code=400, detail="Provide at least one symbol to compare")
    entries_raw = await market.build_comparison(request.symbols)
    correlations = await market.compute_correlations(request.symbols)
    return ComparisonResponse(entries=entries_raw, correlations=correlations)


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_symbol(request: AnalyzeRequest) -> AnalyzeResponse:
    context = request.context or {}
    result = await analyzer.analyze(request.symbol, request.question, context)
    return AnalyzeResponse(**result)
