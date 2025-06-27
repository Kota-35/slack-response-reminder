"""scheduler api."""

from fastapi import APIRouter

from src.api.endpoint.scheduler import weekly_check

router = APIRouter(prefix="/scheduler")

router.include_router(weekly_check.router)
