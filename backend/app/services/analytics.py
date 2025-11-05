from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Any, Dict, Iterable, List, Tuple

import numpy as np

from .data_loader import load_financials, load_prices


@dataclass
class RatioResult:
    symbol: str
    valuation: Dict[str, float]
    profitability: Dict[str, float]
    liquidity: Dict[str, float]
    leverage: Dict[str, float]


@dataclass
class TechnicalIndicatorResult:
    macd: List[Dict[str, float]]
    rsi: List[Dict[str, float]]
    bollinger: List[Dict[str, float]]


def _closing_prices(symbol: str) -> List[float]:
    prices = load_prices().get(symbol, [])
    return [p["close"] for p in prices]


def compute_key_ratios(symbol: str) -> RatioResult:
    financials = load_financials().get(symbol, {})
    income = financials.get("incomeStatement", [])
    balance = financials.get("balanceSheet", {})
    trailing = income[-1] if income else {}
    valuation = {
        "eps": trailing.get("eps", 0.0),
        "revenue": trailing.get("revenue", 0.0),
    }
    profitability = {
        "netIncome": trailing.get("netIncome", 0.0),
        "netMargin": (trailing.get("netIncome", 0.0) / trailing.get("revenue", 1)) * 100,
    }
    liquidity = {
        "currentRatio": balance.get("currentRatio", 0.0),
        "quickRatio": balance.get("quickRatio", 0.0),
    }
    leverage = {
        "debtToEquity": balance.get("debtToEquity", 0.0),
        "returnOnEquity": balance.get("returnOnEquity", 0.0),
    }
    return RatioResult(
        symbol=symbol,
        valuation=valuation,
        profitability=profitability,
        liquidity=liquidity,
        leverage=leverage,
    )


def _ema(values: Iterable[float], period: int) -> np.ndarray:
    values = list(values)
    if not values:
        return np.array([])
    weights = np.exp(np.linspace(-1.0, 0.0, period))
    weights /= weights.sum()
    ema = np.convolve(values, weights, mode="full")[: len(values)]
    ema[:period] = ema[period]
    return ema


def compute_macd(prices: List[float]) -> List[Dict[str, float]]:
    if len(prices) < 26:
        return []
    ema12 = _ema(prices, 12)
    ema26 = _ema(prices, 26)
    macd_line = ema12 - ema26
    signal_line = _ema(macd_line, 9)
    histogram = macd_line - signal_line
    return [
        {"macd": float(m), "signal": float(s), "histogram": float(h)}
        for m, s, h in zip(macd_line[-len(signal_line):], signal_line, histogram[-len(signal_line):])
    ]


def compute_rsi(prices: List[float], period: int = 14) -> List[Dict[str, float]]:
    if len(prices) <= period:
        return []
    gains = []
    losses = []
    for prev, curr in zip(prices[:-1], prices[1:]):
        change = curr - prev
        gains.append(max(change, 0.0))
        losses.append(abs(min(change, 0.0)))
    avg_gain = mean(gains[:period]) if gains[:period] else 0.0
    avg_loss = mean(losses[:period]) if losses[:period] else 0.0
    rsi_values = []
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        rs = avg_gain / avg_loss if avg_loss else float("inf")
        rsi = 100 - (100 / (1 + rs))
        rsi_values.append({"rsi": rsi})
    return rsi_values


def compute_bollinger(prices: List[float], period: int = 20, std_dev: float = 2.0) -> List[Dict[str, float]]:
    if len(prices) < period:
        return []
    bollinger = []
    for i in range(period, len(prices) + 1):
        window = prices[i - period : i]
        avg = mean(window)
        deviation = pstdev(window)
        upper = avg + std_dev * deviation
        lower = avg - std_dev * deviation
        bollinger.append({"middle": avg, "upper": upper, "lower": lower})
    return bollinger


def technical_analysis(symbol: str) -> TechnicalIndicatorResult:
    prices = _closing_prices(symbol)
    return TechnicalIndicatorResult(
        macd=compute_macd(prices),
        rsi=compute_rsi(prices),
        bollinger=compute_bollinger(prices),
    )


def predictive_trend(symbol: str) -> Dict[str, Any]:
    prices = _closing_prices(symbol)
    if len(prices) < 4:
        return {"trend": "insufficient data", "confidence": 0.0}
    slope = np.polyfit(range(len(prices)), prices, 1)[0]
    direction = "uptrend" if slope > 0 else "downtrend"
    confidence = min(1.0, abs(slope) / max(prices))
    return {
        "trend": direction,
        "confidence": float(confidence),
        "projectedPrice": float(prices[-1] + slope * 5),
    }


def volatility_forecast(symbol: str) -> Dict[str, Any]:
    prices = _closing_prices(symbol)
    if len(prices) < 2:
        return {"volatility": 0.0}
    returns = np.diff(np.log(prices))
    volatility = float(np.std(returns) * np.sqrt(252))
    return {"volatility": volatility}


def anomaly_detection(symbol: str) -> Dict[str, Any]:
    prices = _closing_prices(symbol)
    if not prices:
        return {"anomalies": []}
    mean_price = np.mean(prices)
    std_price = np.std(prices)
    anomalies = [
        {"index": i, "price": price}
        for i, price in enumerate(prices)
        if abs(price - mean_price) > 2 * std_price
    ]
    return {"anomalies": anomalies}


def build_correlation_matrix(symbols: List[str]) -> Dict[str, Any]:
    price_data = load_prices()
    closes = [price_data.get(symbol, []) for symbol in symbols]
    aligned = []
    for series in closes:
        aligned.append([row["close"] for row in series])
    if not aligned or any(len(series) != len(aligned[0]) for series in aligned):
        return {"matrix": []}
    matrix = np.corrcoef(aligned).tolist()
    return {"matrix": matrix, "symbols": symbols}


def compare_symbols(symbols: List[str]) -> Dict[str, Any]:
    ratios = [compute_key_ratios(symbol) for symbol in symbols]
    return {
        "ratios": [ratio.__dict__ for ratio in ratios],
        "correlations": build_correlation_matrix(symbols),
    }
