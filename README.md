# Aurora Financial Intelligence Terminal

Aurora is a concept-stage, browser-based financial intelligence terminal that demonstrates how a modern alternative to legacy trading desktops could be built. The repository contains a FastAPI backend that aggregates structured company data, analytics, and event streams, together with a React/Vite front-end that renders a modular dashboard with search, visualization, and news media experiences.

## Architecture Overview

```
.
├── backend            # FastAPI application with analytics and search services
│   ├── app
│   │   ├── api        # REST + WebSocket routes
│   │   ├── data       # Sample data seeds used to simulate external providers
│   │   ├── models     # Pydantic response models
│   │   └── services   # Data aggregation, analytics, NLP, and news helpers
│   └── requirements.txt
└── frontend           # React + Vite client for the terminal UI
    ├── src
    │   ├── components # Modular dashboard panels and search interface
    │   ├── hooks      # Data fetching hooks
    │   └── services   # API client wrappers
    └── package.json
```

### Backend Capabilities
- Ticker search with fuzzy matching and metadata.
- Dashboard endpoint combining financial statements, ratios, technical indicators, ML-style predictive signals, anomaly detection, and AI summaries.
- Symbol comparison endpoint with cached correlation matrices.
- Live event WebSocket that streams macro alerts.
- Extensible service layer separating data access, analytics, NLP, and news aggregation.

### Frontend Highlights
- Dark, Bloomberg-inspired layout built with Material UI.
- Floating global search bar with autocomplete and suggestion text.
- Multi-panel dashboard: overview, charting (fundamental vs. technical modes), financial statements grid, AI insights, media/video wall, comparative analytics, and event ticker.
- WebSocket client for streaming macro news alerts.
- Modular component architecture designed for expansion into collaborative features.

## Getting Started

### One-command local launch

The repository ships with a helper script that prepares the Python virtual environment, installs Node dependencies, and boots
both services with hot reloading.

```bash
./scripts/dev.sh
```

The backend will be available at <http://localhost:8000> and the frontend at <http://localhost:5173>. The Vite dev server
proxies `/api` requests to the FastAPI backend automatically, so you can interact with the Aurora terminal in your browser once
the script prints the startup URLs.

### Manual setup

If you prefer to run each service independently:

1. **Backend**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev -- --host 0.0.0.0 --port 5173
   ```

Visit <http://localhost:5173> after both commands are running. The development server forwards API requests to the backend
listening on `localhost:8000`.

## Next Steps

- Connect to live market data providers (Polygon, Finnhub, Alpha Vantage, etc.).
- Expand technical analysis coverage (Bollinger Bands overlays, Ichimoku clouds, options surfaces).
- Add collaborative workspaces, annotation layers, and saved layouts backed by PostgreSQL.
- Implement authentication and permissioning for institutional deployments.
- Integrate automated report generation and voice-command workflows.
