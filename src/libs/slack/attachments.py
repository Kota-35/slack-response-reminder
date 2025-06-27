"""Slack attachments."""

import json
from typing import Any

from src.libs.notion.database_query import ClientConfig, MemberInformation
from src.libs.slack.message_urls import create_slack_message_url
from src.models.slack.events import SlackEvent


def create_reminded_attachment(
    slack_event: SlackEvent,
    member_information: MemberInformation,
    client_config: ClientConfig,
) -> tuple[str, list[dict[str, Any]]]:
    """Create success attachment."""
    event_message_url = create_slack_message_url(slack_event)
    text = f"*リマインドしました*\n<{event_message_url}|こちら>からご覧ください"
    attachment = [
        {
            "color": "#008000",
            "text": f"```{json.dumps(client_config.model_dump(mode='json'), indent=4, ensure_ascii=False)}\n"
            f"{json.dumps(member_information.model_dump(mode='json'), indent=4, ensure_ascii=False)}\n"
            f"{json.dumps(slack_event.model_dump(mode='json'), indent=4, ensure_ascii=False)}```",
        },
    ]

    return text, attachment


def create_not_reminded_attachment(
    slack_event: SlackEvent,
    member_information: MemberInformation,
    client_config: ClientConfig,
) -> tuple[str, list[dict[str, Any]]]:
    """Create success attachment."""
    event_message_url = create_slack_message_url(slack_event)
    text = f"*リマインドしませんでした*\n<{event_message_url}|こちら>からご覧ください"
    attachment = [
        {
            "color": "#6495ed",
            "text": f"```{json.dumps(client_config.model_dump(mode='json'), indent=4, ensure_ascii=False)}\n"
            f"{json.dumps(member_information.model_dump(mode='json'), indent=4, ensure_ascii=False)}\n"
            f"{json.dumps(slack_event.model_dump(mode='json'), indent=4, ensure_ascii=False)}```",
        },
    ]

    return text, attachment
