from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any, Dict, List

import httpx
import pandas as pd
import yfinance as yf

from ..core.config import settings

ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"


async def _run_in_thread(func, *args, **kwargs):
    return await asyncio.to_thread(func, *args, **kwargs)


async def get_company_profile(symbol: str) -> Dict[str, Any]:
    ticker = await _run_in_thread(yf.Ticker, symbol)
    info = await _run_in_thread(lambda: ticker.info)
    profile = {
        "symbol": symbol.upper(),
        "name": info.get("longName") or info.get("shortName") or symbol.upper(),
        "currency": info.get("currency"),
        "exchange": info.get("fullExchangeName") or info.get("exchange"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "marketCap": info.get("marketCap"),
        "website": info.get("website"),
        "country": info.get("country"),
        "description": info.get("longBusinessSummary"),
        "cik": info.get("cik"),
        "logo": info.get("logo_url"),
    }
    return profile


async def get_key_metrics(symbol: str) -> List[Dict[str, Any]]:
    ticker = await _run_in_thread(yf.Ticker, symbol)
    info = await _run_in_thread(lambda: ticker.info)

    def format_currency(value: Any) -> str:
        if value is None:
            return "-"
        if isinstance(value, (int, float)):
            if abs(value) >= 1_000_000_000:
                return f"${value/1_000_000_000:.2f}B"
            if abs(value) >= 1_000_000:
                return f"${value/1_000_000:.2f}M"
            return f"${value:,.2f}"
        return str(value)

    metrics = [
        {"label": "Market Cap", "value": format_currency(info.get("marketCap"))},
        {"label": "P/E", "value": f"{info.get('trailingPE', 0):.2f}" if info.get("trailingPE") else "-"},
        {"label": "EPS", "value": f"{info.get('trailingEps', 0):.2f}" if info.get("trailingEps") else "-"},
        {
            "label": "Revenue",
            "value": format_currency(info.get("totalRevenue")),
            "hint": "Trailing twelve months",
        },
        {
            "label": "Profit Margin",
            "value": f"{info.get('profitMargins', 0) * 100:.2f}%" if info.get("profitMargins") else "-",
        },
        {
            "label": "52W Range",
            "value": f"{info.get('fiftyTwoWeekLow', '-')}-{info.get('fiftyTwoWeekHigh', '-')}",
        },
    ]
    return metrics


async def _statement_to_payload(frame: pd.DataFrame) -> List[Dict[str, Any]]:
    if frame is None or frame.empty:
        return []
    frame = frame.fillna(0)
    payload: List[Dict[str, Any]] = []
    for column in frame.columns:
        period = column.strftime("%Y-%m-%d") if isinstance(column, (pd.Timestamp, datetime)) else str(column)
        payload.append({"period": period, "data": {k: float(v) for k, v in frame[column].items()}})
    return payload


async def get_financial_statements(symbol: str) -> Dict[str, List[Dict[str, Any]]]:
    ticker = await _run_in_thread(yf.Ticker, symbol)
    income = await _run_in_thread(lambda: getattr(ticker, "income_stmt", ticker.financials))
    balance = await _run_in_thread(lambda: getattr(ticker, "balance_sheet", ticker.balance_sheet))
    cashflow = await _run_in_thread(lambda: getattr(ticker, "cashflow", ticker.cashflow))

    return {
        "income": await _statement_to_payload(income),
        "balance": await _statement_to_payload(balance),
        "cashflow": await _statement_to_payload(cashflow),
    }


async def get_price_history(symbol: str, range_: str = "1y", interval: str = "1d") -> List[Dict[str, Any]]:
    ticker = await _run_in_thread(yf.Ticker, symbol)

    def _history() -> pd.DataFrame:
        return ticker.history(period=range_, interval=interval, actions=False)

    history = await _run_in_thread(_history)
    history = history.reset_index()
    records: List[Dict[str, Any]] = []
    for row in history.to_dict(orient="records"):
        records.append(
            {
                "timestamp": row["Date"].to_pydatetime() if isinstance(row["Date"], pd.Timestamp) else row["Date"],
                "open": float(row.get("Open", 0)),
                "high": float(row.get("High", 0)),
                "low": float(row.get("Low", 0)),
                "close": float(row.get("Close", 0)),
                "volume": float(row.get("Volume", 0)),
            }
        )
    return records


async def _alpha_vantage_request(params: Dict[str, Any]) -> Dict[str, Any]:
    api_key = settings.alpha_vantage_api_key or "demo"
    params_with_key = {**params, "apikey": api_key}
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(ALPHA_VANTAGE_BASE_URL, params=params_with_key)
        response.raise_for_status()
        return response.json()


async def get_macd(symbol: str) -> List[Dict[str, Any]]:
    try:
        data = await _alpha_vantage_request(
            {
                "function": "MACD",
                "symbol": symbol,
                "interval": "daily",
                "series_type": "close",
            }
        )
    except Exception:
        return []
    technicals = data.get("Technical Analysis: MACD", {})
    series: List[Dict[str, Any]] = []
    for timestamp, values in list(technicals.items())[:120]:
        series.append(
            {
                "timestamp": datetime.fromisoformat(timestamp),
                "macd": float(values.get("MACD", 0.0)),
                "signal": float(values.get("MACD_Signal", 0.0)),
                "hist": float(values.get("MACD_Hist", 0.0)),
            }
        )
    return series


async def get_rsi(symbol: str) -> List[Dict[str, Any]]:
    try:
        data = await _alpha_vantage_request(
            {
                "function": "RSI",
                "symbol": symbol,
                "interval": "daily",
                "time_period": 14,
                "series_type": "close",
            }
        )
    except Exception:
        return []
    technicals = data.get("Technical Analysis: RSI", {})
    series: List[Dict[str, Any]] = []
    for timestamp, values in list(technicals.items())[:120]:
        series.append(
            {
                "timestamp": datetime.fromisoformat(timestamp),
                "value": float(values.get("RSI", 0.0)),
            }
        )
    return series


async def get_bbands(symbol: str) -> List[Dict[str, Any]]:
    try:
        data = await _alpha_vantage_request(
            {
                "function": "BBANDS",
                "symbol": symbol,
                "interval": "daily",
                "time_period": 20,
                "series_type": "close",
            }
        )
    except Exception:
        return []
    technicals = data.get("Technical Analysis: BBANDS", {})
    series: List[Dict[str, Any]] = []
    for timestamp, values in list(technicals.items())[:120]:
        series.append(
            {
                "timestamp": datetime.fromisoformat(timestamp),
                "upper": float(values.get("Real Upper Band", 0.0)),
                "middle": float(values.get("Real Middle Band", 0.0)),
                "lower": float(values.get("Real Lower Band", 0.0)),
            }
        )
    return series


async def get_fx_pair(pair: str) -> Dict[str, Any]:
    data = await _alpha_vantage_request(
        {
            "function": "FX_DAILY",
            "from_symbol": pair[:3],
            "to_symbol": pair[3:],
        }
    )
    return data


async def get_crypto_series(symbol: str) -> Dict[str, Any]:
    data = await _alpha_vantage_request(
        {
            "function": "DIGITAL_CURRENCY_DAILY",
            "symbol": symbol,
            "market": "USD",
        }
    )
    return data


async def get_recent_filings(symbol: str, profile: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    if profile is None:
        profile = await get_company_profile(symbol)
    cik = profile.get("cik")
    if not cik:
        return []
    cik_normalized = str(cik).zfill(10)
    submissions_url = f"https://data.sec.gov/submissions/CIK{cik_normalized}.json"
    headers = {"User-Agent": settings.sec_user_agent}
    async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
        response = await client.get(submissions_url)
        response.raise_for_status()
        data = response.json()
    filings = []
    recent = data.get("filings", {}).get("recent", {})
    for idx, form in enumerate(recent.get("form", [])[:10]):
        if form not in {"10-K", "10-Q", "8-K"}:
            continue
        accession = recent.get("accessionNumber", [])[idx]
        filed_at = recent.get("filingDate", [])[idx]
        report_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession.replace('-', '')}/{accession}-index.html"
        filings.append(
            {
                "accessionNumber": accession,
                "formType": form,
                "filedAt": filed_at,
                "reportUrl": report_url,
            }
        )
    return filings


async def build_comparison(symbols: List[str]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for symbol in symbols:
        profile = await get_company_profile(symbol)
        metrics = await get_key_metrics(symbol)
        results.append({"symbol": symbol.upper(), "profile": profile, "metrics": metrics})
    return results


async def compute_correlations(symbols: List[str], range_: str = "6mo") -> Dict[str, float]:
    series: Dict[str, pd.Series] = {}
    for symbol in symbols:
        data = await get_price_history(symbol, range_, "1d")
        if not data:
            continue
        df = pd.DataFrame(data)
        df.set_index("timestamp", inplace=True)
        series[symbol.upper()] = df["close"].pct_change().dropna()
    if not series:
        return {}
    combined = pd.concat(series, axis=1).dropna()
    corr = combined.corr()
    correlations: Dict[str, float] = {}
    symbols_sorted = sorted(series.keys())
    for i, a in enumerate(symbols_sorted):
        for b in symbols_sorted[i + 1 :]:
            correlations[f"{a}-{b}"] = float(corr.loc[a, b])
    return correlations
