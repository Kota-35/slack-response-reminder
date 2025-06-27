"""APIのエンドポイントを定義する."""

from fastapi import APIRouter

from src.api import endpoint, health

router = APIRouter(prefix="/api/v1")
router.include_router(endpoint.router)
router.include_router(health.router)
