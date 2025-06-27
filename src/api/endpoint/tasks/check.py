"""Check Cloud Tasks."""

import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.libs.notion.client import client_setting
from src.libs.notion.database_query import (
    ClientConfig,
    MemberInformation,
)
from src.libs.settings import env
from src.libs.slack.direct_message import send_direct_message, send_log_message
from src.libs.slack.message_urls import create_slack_message_url
from src.libs.slack.replies import get_replies
from src.models.slack.events import SlackEvent

router = APIRouter()


@router.post("/check")
async def check(slack_event: SlackEvent) -> JSONResponse:
    """Check Cloud Tasks."""
    print("Get Cloud Tasks")  # noqa: T201
    print(json.dumps(slack_event.model_dump(), indent=4, ensure_ascii=False))  # noqa: T201

    member_information, client_config = await client_setting(
        slack_event.channel,
    )

    slack_messages = await get_replies(slack_event)

    # FYI: 該当メッセージのインデックスを取得
    for idx, message in enumerate(slack_messages):  # noqa: B007
        if message.ts == slack_event.ts:
            break

    # FYI: スレッドの中で該当メッセージ以降のメッセージを取得
    target_messages = slack_messages[idx:]
    print("target_messages", target_messages)  # noqa: T201

    # FYI: スレッドの中で該当メッセージ以降のメッセージの中に未返信のメッセージがあるかを判定
    has_reply = any(
        message.user_team is None and message.team == env.slack_team_id
        for message in target_messages
    )

    await post_message(
        member_information,
        client_config,
        slack_event,
        has_reply,
    )

    print("has_reply", has_reply)  # noqa: T201
    return JSONResponse(
        status_code=200,
        content=json.dumps(
            {
                "message": "success",
                "has_reply": has_reply,
            },
        ),
    )


async def post_message(
    member_information: MemberInformation,
    client_config: ClientConfig,
    slack_event: SlackEvent,
    has_reply: bool,  # noqa: FBT001
) -> None:
    """Post message."""
    if not has_reply:
        user_ids = [member.slack_id for member in member_information.members]
        event_message_url = create_slack_message_url(slack_event)
        mention = ",".join([f"<@{slack_id}>" for slack_id in user_ids])
        message = (
            f"{mention}\n"
            f"*<#{slack_event.channel}>で未返信のメッセージがあります*\n"
            f"<{event_message_url}|こちら>からご覧ください"
        )

        await send_direct_message(
            user_ids=user_ids,
            message=message,
        )

    await send_log_message(
        has_reply,
        slack_event,
        member_information,
        client_config,
    )
