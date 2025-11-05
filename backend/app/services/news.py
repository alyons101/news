from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, List

import httpx
import yfinance as yf

from ..core.config import settings


async def fetch_finnhub_news(symbol: str) -> List[Dict[str, Any]]:
    if not settings.finnhub_api_key:
        return []
    params = {
        "symbol": symbol.upper(),
        "from": (datetime.utcnow() - timedelta(days=14)).strftime("%Y-%m-%d"),
        "to": datetime.utcnow().strftime("%Y-%m-%d"),
        "token": settings.finnhub_api_key,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get("https://finnhub.io/api/v1/company-news", params=params)
        response.raise_for_status()
        payload = response.json()
    news_items = []
    for item in payload:
        news_items.append(
            {
                "title": item.get("headline"),
                "url": item.get("url"),
                "source": item.get("source"),
                "summary": item.get("summary"),
                "publishedAt": datetime.utcfromtimestamp(item.get("datetime", 0)),
                "thumbnail": item.get("image"),
            }
        )
    return news_items


async def fetch_newsdata_news(symbol: str) -> List[Dict[str, Any]]:
    if not settings.newsdata_api_key:
        return []
    params = {
        "apikey": settings.newsdata_api_key,
        "q": symbol,
        "language": "en",
        "category": "business,top",
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get("https://newsdata.io/api/1/news", params=params)
        response.raise_for_status()
        payload = response.json()
    articles = payload.get("results", [])
    news_items: List[Dict[str, Any]] = []
    for article in articles:
        published_at = article.get("pubDate")
        parsed = datetime.fromisoformat(published_at.replace("Z", "+00:00")) if published_at else datetime.utcnow()
        video_url = None
        if article.get("video_url"):
            video_url = article["video_url"]
        news_items.append(
            {
                "title": article.get("title"),
                "url": article.get("link"),
                "source": article.get("source_id"),
                "summary": article.get("description"),
                "publishedAt": parsed,
                "thumbnail": article.get("image_url"),
                "videoUrl": video_url,
            }
        )
    return news_items


async def fetch_youtube_videos(query: str) -> List[Dict[str, Any]]:
    if not settings.youtube_api_key:
        return []
    params = {
        "part": "snippet",
        "q": f"{query} stock news",
        "type": "video",
        "maxResults": 8,
        "order": "date",
        "key": settings.youtube_api_key,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get("https://www.googleapis.com/youtube/v3/search", params=params)
        response.raise_for_status()
        payload = response.json()
    videos: List[Dict[str, Any]] = []
    for item in payload.get("items", []):
        video_id = item.get("id", {}).get("videoId")
        if not video_id:
            continue
        snippet = item.get("snippet", {})
        published_raw = snippet.get("publishedAt")
        published_at = (
            datetime.fromisoformat(published_raw.replace("Z", "+00:00"))
            if published_raw
            else datetime.utcnow()
        )
        url = f"https://www.youtube.com/watch?v={video_id}"
        thumbnail = (
            snippet.get("thumbnails", {}).get("high", {}).get("url")
            or snippet.get("thumbnails", {}).get("default", {}).get("url")
        )
        videos.append(
            {
                "id": video_id,
                "title": snippet.get("title"),
                "url": url,
                "videoUrl": url,
                "source": snippet.get("channelTitle"),
                "channel": snippet.get("channelTitle"),
                "summary": snippet.get("description"),
                "description": snippet.get("description"),
                "publishedAt": published_at,
                "thumbnail": thumbnail,
            }
        )
    return videos


async def fetch_yahoo_news(symbol: str) -> List[Dict[str, Any]]:
    ticker = await asyncio.to_thread(yf.Ticker, symbol)
    raw_news = await asyncio.to_thread(lambda: ticker.news)
    news_items: List[Dict[str, Any]] = []
    for item in raw_news[:20]:
        published_at = datetime.fromtimestamp(item.get("providerPublishTime", 0))
        related_video = item.get("relatedVideo")
        video_url = None
        if isinstance(related_video, str):
            video_url = related_video
        elif isinstance(related_video, dict):
            video_url = related_video.get("url")
        news_items.append(
            {
                "title": item.get("title"),
                "url": item.get("link"),
                "source": item.get("publisher"),
                "summary": item.get("summary"),
                "publishedAt": published_at,
                "thumbnail": item.get("thumbnailUrl"),
                "videoUrl": video_url,
            }
        )
    return news_items


async def get_news(symbol: str) -> List[Dict[str, Any]]:
    providers = [fetch_finnhub_news, fetch_newsdata_news, fetch_yahoo_news, fetch_youtube_videos]
    aggregated: List[Dict[str, Any]] = []
    for provider in providers:
        try:
            data = await provider(symbol)
            aggregated.extend(data)
        except Exception:
            continue
    aggregated.sort(key=lambda item: item.get("publishedAt"), reverse=True)
    return aggregated[:40]


async def get_videos(query: str) -> List[Dict[str, Any]]:
    videos = await fetch_youtube_videos(query)
    return videos
