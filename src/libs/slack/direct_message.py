"""SlackのDMを送信する."""

from slack_sdk.errors import SlackClientError

from src.libs.notion.database_query import ClientConfig, MemberInformation
from src.libs.settings import env
from src.libs.slack.attachments import (
    create_not_reminded_attachment,
    create_reminded_attachment,
)
from src.libs.slack.client import create_slack_client
from src.models.slack.events import SlackEvent


async def send_direct_message(user_ids: list[str], message: str) -> None:
    """SlackのDMを送信する."""
    client = create_slack_client()
    try:
        # DMを開く
        response = await client.conversations_open(users=user_ids)
        dm_id = response["channel"]["id"]

        # DMにメッセージを送信
        await client.chat_postMessage(
            channel=dm_id,
            text=message,
            unfurl_links=True,
            unfurl_media=True,
        )
    except SlackClientError as e:
        print(f"Failed to send direct message: {e}")  # noqa: T201


async def send_log_message(
    has_reply: bool,  # noqa: FBT001
    slack_event: SlackEvent,
    member_info: MemberInformation,
    client_config: ClientConfig,
) -> None:
    """Send log message."""
    client = create_slack_client()

    if not has_reply:
        text, attachments = create_reminded_attachment(
            slack_event,
            member_info,
            client_config,
        )
    else:
        text, attachments = create_not_reminded_attachment(
            slack_event,
            member_info,
            client_config,
        )

    try:
        await client.chat_postMessage(
            channel=env.slack_log_channel_id,
            text=text,
            attachments=attachments,
            unfurl_links=True,
            unfurl_media=True,
        )

    except Exception:  # noqa: TRY203
        raise
