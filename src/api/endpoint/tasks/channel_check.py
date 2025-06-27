"""月火のリマインドChannel check."""

from fastapi import APIRouter, Response
from pydantic import BaseModel
from slack_sdk.errors import SlackClientError

from src.libs.notion.database_query import MemberInformation
from src.libs.slack.channel import is_message_posted_on_this_week
from src.libs.slack.direct_message import send_direct_message

router = APIRouter()


class ChannelCheckRequest(BaseModel):
    """Channel check request."""

    channel_id: str
    member_info: MemberInformation


@router.post("/channel-check")
async def channel_check(
    body: ChannelCheckRequest,
) -> Response:
    """月火のリマインドChannel check."""
    user_ids = [member.slack_id for member in body.member_info.members]
    check_result = await is_message_posted_on_this_week(
        channel_id=body.channel_id,
        user_ids=user_ids,
    )

    if not check_result:
        # 日付と曜日を含むメッセージを作成
        message = f"*<#{body.channel_id}>で今週の月曜日から火曜日にRH側からメッセージがありません。*\n"

        try:
            await send_direct_message(
                user_ids=user_ids,
                message=message,
            )
        except SlackClientError as e:
            print(f"Failed to send direct message: {e}")  # noqa: T201

    return Response(status_code=200)
