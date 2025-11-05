# Aurora Financial Intelligence Terminal

Aurora is a full-stack, browser-based finance platform inspired by institutional terminals. It combines a FastAPI backend with a React + Vite front-end, aggregates live market data from Yahoo Finance, Alpha Vantage, Financial Modeling Prep, and SEC EDGAR, surfaces real-time news via Finnhub/NewsData, injects market video briefings from YouTube, and layers in AI commentary through OpenAI or an offline summarizer. The result is a modular, data-dense workspace that delivers market intelligence, charting, filings, and media without leaving the browser.

## Feature Highlights

- **Search Intelligence** – Natural ticker/company search powered by Yahoo Finance with persistent recent history and watchlists stored locally.
- **Live Market Data** – Company profiles, fundamental statements, key ratios, SEC filings, and multi-range price history pulled dynamically via `yfinance`, Financial Modeling Prep, and Alpha Vantage technical indicators (MACD, RSI, Bollinger Bands, FX, crypto).
- **News & Media Hub** – Aggregated real-time articles plus embedded video playback from Finnhub, NewsData.io, Yahoo Finance feeds, and curated YouTube finance channels.
- **Quant & AI Insights** – Automated highlights, technical outlooks, peer correlations, and an “AI Market Analyst” panel that can call OpenAI (if configured) for narrative summaries.
- **Interactive Visualization** – Tailwind/ShadCN-styled dashboard with Recharts-based price and indicator visualizations, financial statement tables, and comparison analytics.
- **Production-ready Infrastructure** – FastAPI caching via `fastapi-cache2`, optional OpenAI integration, static asset serving, Docker build, and environment-variable driven configuration.

## Repository Structure

```
.
├── backend
│   ├── app
│   │   ├── api            # FastAPI routers and response models
│   │   ├── core           # Application configuration
│   │   ├── services       # Market data, news, insights, analyzer modules
│   │   └── main.py        # FastAPI application entrypoint
│   └── requirements.txt
├── frontend
│   ├── index.html
│   ├── package.json
│   └── src                # React + Vite client (Tailwind, ShadCN utilities, Recharts)
├── scripts
│   └── dev.sh             # Combined frontend + backend development script
└── .env.example           # Environment variable template
```

## Getting Started

### 1. Prerequisites

- Python 3.10+
- Node.js 18+
- (Optional) Docker 24+

### 2. Configure Environment Variables

Copy the example file and fill in API keys (demo values work for initial exploration):

```bash
cp .env.example .env
```

| Variable | Description |
| --- | --- |
| `ALPHA_VANTAGE_API_KEY` | Required for technical indicators, FX, and crypto data (`demo` key has strict limits). |
| `FMP_API_KEY` | Required for live financial statements, company profiles, and ratios (use `demo` for limited access). |
| `FINNHUB_API_KEY` / `NEWSDATA_API_KEY` | Optional real-time company news feeds (fallback to Yahoo Finance if omitted). |
| `YOUTUBE_API_KEY` | Optional. Powers the market video briefings and `/api/videos` endpoint. |
| `OPENAI_API_KEY` | Optional. Enables the `/api/analyze` endpoint for GPT-powered commentary. |
| `CORS_ORIGINS` | Comma-separated list of allowed origins for the API. |
| `SEC_USER_AGENT` | Contact email for SEC EDGAR requests. |

### 3. One-command Local Launch

Use the bundled script to install dependencies, export environment variables, and start both services with hot reload:

```bash
./scripts/dev.sh
```

- Backend: <http://localhost:8000>
- Frontend: <http://localhost:5173>
- The Vite dev server proxies `/api` -> FastAPI automatically.

### 4. Manual Setup

**Backend**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

## Building & Deployment

### Production Build

Bundle the React client and serve it via FastAPI’s static mount:

```bash
cd frontend
npm run build
cd ../backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

When `frontend/dist` exists, FastAPI serves the built UI at `/` while keeping all API routes under `/api`.

### Docker Image

A multi-stage Dockerfile is provided to compile the frontend and run the FastAPI server with Uvicorn.

```bash
docker build -t aurora-terminal .
docker run --env-file .env -p 8000:8000 aurora-terminal
```

### Deploying to Render / Vercel / DigitalOcean

- **Render / DigitalOcean App Platform**: Build the Docker image or run the backend service with `uvicorn app.main:app`. Ensure environment variables are set and the frontend is prebuilt (`npm run build`).
- **Vercel**: Deploy the frontend separately using the `frontend` directory while pointing API routes to a hosted FastAPI service (Render, Railway, etc.).
- **Static Hosting**: Optionally upload `frontend/dist` to a CDN and update `CORS_ORIGINS` so the hosted React app can talk to the FastAPI API.

## API Overview

| Route | Description |
| --- | --- |
| `GET /api/search?query=AAPL` | Autocomplete for companies and tickers via Yahoo Finance. |
| `GET /api/financials/{symbol}` | Company profile, key metrics, financial statements, SEC filings. |
| `GET /api/chart/{symbol}?range=1y` | Price history with MACD/RSI/Bollinger indicators. |
| `GET /api/news/{symbol}` | Aggregated news headlines and media. |
| `GET /api/videos/{query}` | Latest finance-focused YouTube clips for the requested symbol or keyword. |
| `GET /api/insights/{symbol}` | Generated highlights, narratives, and technical outlook. |
| `POST /api/compare` | Peer comparison metrics and correlations. |
| `POST /api/analyze` | AI-generated narrative (OpenAI or offline fallback). |

All GET routes are cached in-memory with configurable TTLs for snappy repeated lookups.

## Frontend Architecture

- **Stack**: React 18, Vite, TailwindCSS, ShadCN-inspired utility components, Recharts, Framer Motion, React Query.
- **Layout**: Bloomberg-style dark theme with global search, watchlist sidebar, overview/financial/news/insights grid, and AI assistant.
- **State Management**: React Query handles API caching; watchlists and recents persist via `localStorage`.
- **Media**: Embedded HTML5 video player (React Player) to watch CNBC/Bloomberg/YouTube content in context.

## Extending the Platform

- Integrate authentication/JWT and persistent dashboards with PostgreSQL.
- Expand analytics (options surfaces, volatility cones, strategy backtesting).
- Hook in macro data (CPI, GDP) and ESG datasets for a multi-asset lens.
- Add collaborative workspaces, annotations, and webhook integrations.
- Productionize caching with Redis and background workers for scheduled refreshes.

Aurora now operates as a true web-based terminal that merges quantitative computation, AI-driven commentary, real-time visualization, and contextual media.
