"""Tasks API."""

from fastapi import APIRouter

from src.api.endpoint.tasks import channel_check, check

router = APIRouter(prefix="/tasks")

router.include_router(check.router)
router.include_router(channel_check.router)
