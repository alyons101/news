from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    alpha_vantage_api_key: str | None = None
    finnhub_api_key: str | None = None
    newsdata_api_key: str | None = None
    openai_api_key: str | None = None
    yahoo_region: str = "US"
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])
    frontend_dist: Path = Path(__file__).resolve().parents[2] / "frontend" / "dist"
    sec_user_agent: str = "AuroraTerminal/1.0 (contact@aurora.example)"
    default_market: str = "US"

    documentation_url: HttpUrl | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_origins(cls, value: List[str] | str) -> List[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
