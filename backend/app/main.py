from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from .api.routes import router
from .core.config import settings


app = FastAPI(title="Aurora Terminal", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.on_event("startup")
async def on_startup() -> None:
    FastAPICache.init(InMemoryBackend(), prefix="aurora-cache")
    mount_frontend()


def mount_frontend() -> None:
    dist_path: Path = settings.frontend_dist
    if dist_path.exists() and any(dist_path.iterdir()):
        app.mount(
            "/",
            StaticFiles(directory=str(dist_path), html=True),
            name="frontend",
        )


@app.get("/healthz")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
