"""APIのエンドポイントを定義する."""

from fastapi import APIRouter

from src.api.endpoint import scheduler, slack, tasks

router = APIRouter()

router.include_router(slack.router)
router.include_router(tasks.router)
router.include_router(scheduler.router)
