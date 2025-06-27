"""Slackのイベントを受け取るエンドポイントを定義する."""

from typing import Annotated

from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

from src.api.endpoint.slack.types import SlackEventHeaders, SlackEventRequest
from src.libs.cloud_tasks.tasks import create_tasks
from src.libs.notion.client import get_setting_only
from src.libs.settings import env

router = APIRouter()


@router.post("/events")
async def slack_events(
    body: SlackEventRequest,
    headers: Annotated[SlackEventHeaders, Header()],
) -> JSONResponse:
    """Slackのイベントを受け取るエンドポイント."""
    if headers.x_slack_retry_num:
        # FYI: リトライの場合は、リトライ回数を返す

        return JSONResponse(
            status_code=200,
            content={"ok": True, "retry_num": headers.x_slack_retry_num},
        )

    if body.type == "url_verification":
        # FYI: URL検証の場合は、challengeを返す
        return JSONResponse(
            status_code=200,
            content={"challenge": body.challenge},
        )

    await judge_event(body)

    return JSONResponse(
        status_code=200,
        content={"ok": True},
    )


async def judge_event(body: SlackEventRequest) -> None:
    """イベントからチームを判定し、タスクを作成するか削除するかを判定する."""
    if body.event.team == env.slack_team_id:
        # 社内メンバーのメッセージの場合
        pass
    else:
        # 社外メンバーのメッセージの場合
        # Cloud Tasksでタスクを作成する

        client_config = await get_setting_only(channel_id=body.event.channel)
        if client_config.status:
            await create_tasks(slack_event=body.event)
