from __future__ import annotations

from typing import Dict, List

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from ..models.responses import ComparisonRequest, ComparisonResponse, DashboardPayload
from ..services import analytics, data_loader, news, nlp, search
from ..utils.cache import cache

router = APIRouter()


@router.get("/search")
def search_symbols(query: str) -> List[Dict[str, str]]:
    if not query:
        return []
    return search.search_service.search(query)


@router.get("/companies/{symbol}")
def company_dashboard(symbol: str) -> DashboardPayload:
    companies = {item["symbol"]: item for item in data_loader.load_companies()}
    company = companies.get(symbol.upper())
    if not company:
        raise HTTPException(status_code=404, detail="Symbol not found")

    financials = data_loader.load_financials().get(symbol.upper(), {})
    ratios = analytics.compute_key_ratios(symbol.upper())
    technicals = analytics.technical_analysis(symbol.upper())
    predictive = analytics.predictive_trend(symbol.upper())
    volatility = analytics.volatility_forecast(symbol.upper())
    anomalies = analytics.anomaly_detection(symbol.upper())
    news_items = news.news_for_symbol(symbol.upper())
    sentiment = news.aggregate_sentiment(symbol.upper())
    summary = nlp.summarize_symbol(
        symbol.upper(),
        revenue=ratios.valuation.get("revenue", 0.0),
        eps=ratios.valuation.get("eps", 0.0),
    )

    payload = DashboardPayload(
        company=company,
        ratios=ratios.__dict__,
        incomeStatement=financials.get("incomeStatement", []),
        technicals={
            "macd": technicals.macd,
            "rsi": technicals.rsi,
            "bollinger": technicals.bollinger,
        },
        predictive=predictive,
        volatility=volatility,
        anomalies=anomalies,
        news=news_items,
        sentiment=sentiment,
        aiSummary=summary,
    )
    return payload


@router.post("/compare")
def compare(request: ComparisonRequest) -> ComparisonResponse:
    if not request.symbols:
        raise HTTPException(status_code=400, detail="No symbols provided")
    cached = cache.get_or_set(
        key=f"compare:{','.join(sorted(request.symbols))}",
        factory=lambda: analytics.compare_symbols(request.symbols),
        ttl=60,
    )
    return ComparisonResponse(**cached)


_active_connections: List[WebSocket] = []


@router.websocket("/ws/events")
async def events_websocket(ws: WebSocket) -> None:
    await ws.accept()
    _active_connections.append(ws)
    try:
        await ws.send_json({"type": "welcome", "message": "Streaming macro updates"})
        await ws.send_json(
            {
                "type": "event",
                "category": "macro",
                "payload": {
                    "title": "Fed Chair commentary",
                    "detail": "Markets expect one more rate hike this cycle.",
                    "severity": "medium",
                },
            }
        )
    except WebSocketDisconnect:
        pass
    finally:
        if ws in _active_connections:
            _active_connections.remove(ws)
