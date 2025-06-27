"""Slackのエンドポイントを定義する."""

from fastapi import APIRouter

from src.api.endpoint.slack import events

router = APIRouter(prefix="/slack")
router.include_router(events.router)
