"""Slack Channel."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.libs.slack.client import create_slack_client
from src.models.slack.replies import SlackMessage


class SlackConversationHistoryError(Exception):
    """Slack Conversation History Exception."""


async def is_message_posted_on_this_week(
    channel_id: str,
    user_ids: list[str],
) -> bool:
    """月火のリマインドメッセージが投稿されているかどうかをチェックする."""
    slack_client = create_slack_client()

    tz = ZoneInfo("Asia/Tokyo")
    now = datetime.now(tz=tz)

    # weekday(): 月曜=0, 日曜=6なので、今週の月曜の日付を計算
    monday_date = now.date() - timedelta(days=now.weekday())

    # 今週月曜の0:00 datetimeオブジェクトを作成
    monday_zero = datetime.combine(monday_date, datetime.min.time(), tzinfo=tz)

    oldest_timestamp = str(monday_zero.timestamp())

    response = await slack_client.conversations_history(
        channel=channel_id,
        oldest=oldest_timestamp,
    )

    if not response.get("ok", False):
        print(f"Failed to get conversations history: {response}")  # noqa: T201
        return True

    messages = [
        SlackMessage(**message) for message in response.get("messages", [])
    ]

    judge = len(messages) != 0 and any(
        message.user in user_ids for message in messages
    )

    # RH側からメッセージが一件もない場合は、Falseを返す メッセージがあるかつ、user_idsに含まれるユーザーがメッセージを投稿している場合は、Trueを返す
    return judge
