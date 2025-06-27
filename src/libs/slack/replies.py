"""Slack Replies."""

from src.libs.slack.client import create_slack_client
from src.models.slack.events import SlackEvent
from src.models.slack.replies import SlackMessage


async def get_replies(slack_event: SlackEvent) -> list[SlackMessage]:
    """Get Replies."""
    client = create_slack_client()
    response = await client.conversations_replies(
        channel=slack_event.channel,
        ts=slack_event.thread_ts or slack_event.ts,
    )
    slack_messages = [
        SlackMessage(**message) for message in response["messages"]
    ]
    return slack_messages
