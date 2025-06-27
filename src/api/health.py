"""Health check."""

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, Any]:
    """Health check."""
    return {
        "status": "ok",
        "timestamp": datetime.now(tz=ZoneInfo("Asia/Tokyo")).isoformat(),
    }
