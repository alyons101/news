from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any, Dict, List

import httpx
import pandas as pd
import yfinance as yf

from ..core.config import settings

ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"


async def _run_in_thread(func, *args, **kwargs):
    return await asyncio.to_thread(func, *args, **kwargs)


async def get_company_profile(symbol: str) -> Dict[str, Any]:
    profile: Dict[str, Any] | None = None
    try:
        fmp_profile = await _fmp_request(f"profile/{symbol}")
        if fmp_profile:
            entry = fmp_profile[0]
            profile = {
                "symbol": symbol.upper(),
                "name": entry.get("companyName") or entry.get("symbol", symbol.upper()),
                "currency": entry.get("currency"),
                "exchange": entry.get("exchangeShortName") or entry.get("exchange"),
                "sector": entry.get("sector"),
                "industry": entry.get("industry"),
                "marketCap": entry.get("mktCap"),
                "website": entry.get("website"),
                "country": entry.get("country"),
                "description": entry.get("description"),
                "cik": entry.get("cik"),
                "logo": entry.get("image"),
            }
    except Exception:
        profile = None

    if profile is not None:
        return profile

    ticker = await _run_in_thread(yf.Ticker, symbol)
    info = await _run_in_thread(lambda: ticker.info)
    return {
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


async def get_key_metrics(symbol: str) -> List[Dict[str, Any]]:
    def format_currency(value: Any) -> str:
        if value in (None, ""):
            return "-"
        if isinstance(value, (int, float)):
            if abs(value) >= 1_000_000_000:
                return f"${value/1_000_000_000:.2f}B"
            if abs(value) >= 1_000_000:
                return f"${value/1_000_000:.2f}M"
            return f"${value:,.2f}"
        return str(value)

    def format_number(value: Any, decimals: int = 2, suffix: str = "") -> str:
        if value in (None, ""):
            return "-"
        try:
            return f"{float(value):.{decimals}f}{suffix}"
        except (TypeError, ValueError):
            return "-"

    def format_percent(value: Any) -> str:
        if value in (None, ""):
            return "-"
        try:
            return f"{float(value) * 100:.2f}%"
        except (TypeError, ValueError):
            return "-"

    metrics: List[Dict[str, Any]] = []
    key_metrics: Dict[str, Any] | None = None
    ratios: Dict[str, Any] | None = None

    try:
        key_metrics_payload = await _fmp_request(f"key-metrics-ttm/{symbol}")
        if key_metrics_payload:
            key_metrics = key_metrics_payload[0]
    except Exception:
        key_metrics = None

    try:
        ratios_payload = await _fmp_request(f"ratios-ttm/{symbol}")
        if ratios_payload:
            ratios = ratios_payload[0]
    except Exception:
        ratios = None

    if key_metrics:
        metrics.append({"label": "Market Cap", "value": format_currency(key_metrics.get("marketCapTTM"))})
        metrics.append({"label": "Enterprise Value", "value": format_currency(key_metrics.get("enterpriseValueTTM"))})
        metrics.append({"label": "P/E", "value": format_number(key_metrics.get("peRatioTTM"))})
        metrics.append({"label": "EPS (TTM)", "value": format_number(key_metrics.get("epsTTM"))})
        metrics.append({"label": "Free Cash Flow", "value": format_currency(key_metrics.get("freeCashFlowTTM"))})

    if ratios:
        metrics.append({"label": "Revenue Growth (TTM)", "value": format_percent(ratios.get("revenueGrowthTTM"))})
        metrics.append({"label": "Net Profit Margin", "value": format_percent(ratios.get("netProfitMarginTTM"))})
        metrics.append({"label": "Return on Equity", "value": format_percent(ratios.get("roeTTM"))})
        metrics.append({"label": "Debt to Equity", "value": format_number(ratios.get("debtEquityRatioTTM"))})

    if not metrics:
        ticker = await _run_in_thread(yf.Ticker, symbol)
        info = await _run_in_thread(lambda: ticker.info)
        metrics = [
            {"label": "Market Cap", "value": format_currency(info.get("marketCap"))},
            {"label": "P/E", "value": format_number(info.get("trailingPE"))},
            {"label": "EPS", "value": format_number(info.get("trailingEps"))},
            {
                "label": "Revenue",
                "value": format_currency(info.get("totalRevenue")),
                "hint": "Trailing twelve months",
            },
            {"label": "Profit Margin", "value": format_percent(info.get("profitMargins"))},
        ]
    else:
        try:
            ticker = await _run_in_thread(yf.Ticker, symbol)
            info = await _run_in_thread(lambda: ticker.info)
            low = format_number(info.get("fiftyTwoWeekLow"))
            high = format_number(info.get("fiftyTwoWeekHigh"))
            if low != "-" or high != "-":
                metrics.append({"label": "52W Range", "value": f"{low}-{high}"})
        except Exception:
            pass

    return metrics


async def _fmp_request(path: str, params: Dict[str, Any] | None = None) -> Any:
    params_with_key = {**(params or {}), "apikey": settings.fmp_api_key or "demo"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{FMP_BASE_URL}/{path.lstrip('/')}", params=params_with_key)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and any(key in data for key in ("error", "Error Message")):
            raise ValueError(data.get("error") or data.get("Error Message"))
        return data


async def _statement_to_payload(frame: pd.DataFrame | None) -> List[Dict[str, Any]]:
    if frame is None or frame.empty:
        return []
    frame = frame.fillna(0)
    payload: List[Dict[str, Any]] = []
    for column in frame.columns:
        period = column.strftime("%Y-%m-%d") if isinstance(column, (pd.Timestamp, datetime)) else str(column)
        payload.append({"period": period, "data": {k: float(v) for k, v in frame[column].items()}})
    return payload


def _fmp_statement_payload(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    payload: List[Dict[str, Any]] = []
    for record in records:
        period = record.get("date") or record.get("calendarYear")
        data: Dict[str, float] = {}
        for key, value in record.items():
            if key in {
                "date",
                "symbol",
                "reportedCurrency",
                "cik",
                "fillingDate",
                "acceptedDate",
                "calendarYear",
                "period",
                "link",
                "finalLink",
            }:
                continue
            if isinstance(value, (int, float)):
                data[key] = float(value)
        payload.append({"period": str(period), "data": data})
    return payload


async def get_financial_statements(symbol: str) -> Dict[str, List[Dict[str, Any]]]:
    try:
        income = await _fmp_request(f"income-statement/{symbol}", {"limit": 6})
        balance = await _fmp_request(f"balance-sheet-statement/{symbol}", {"limit": 6})
        cashflow = await _fmp_request(f"cash-flow-statement/{symbol}", {"limit": 6})
        return {
            "income": _fmp_statement_payload(income),
            "balance": _fmp_statement_payload(balance),
            "cashflow": _fmp_statement_payload(cashflow),
        }
    except Exception:
        ticker = await _run_in_thread(yf.Ticker, symbol)
        income_frame = await _run_in_thread(lambda: getattr(ticker, "income_stmt", ticker.financials))
        balance_frame = await _run_in_thread(lambda: getattr(ticker, "balance_sheet", ticker.balance_sheet))
        cashflow_frame = await _run_in_thread(lambda: getattr(ticker, "cashflow", ticker.cashflow))
        return {
            "income": await _statement_to_payload(income_frame),
            "balance": await _statement_to_payload(balance_frame),
            "cashflow": await _statement_to_payload(cashflow_frame),
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
