"""Slack events."""

from typing import Literal

from pydantic import BaseModel


class SlackEventMessage(BaseModel):
    """Slack Event Message."""

    user: str
    type: Literal["message"]
    ts: str
    text: str
    team: str
    channel: str
    event_ts: str
    channel_type: Literal["group", "channel"]
    thread_ts: str | None = None


class SlackEventMessageEdited(BaseModel):
    """Slack Event Message Edited."""

    type: Literal["message"]
    subtype: Literal["message_changed"]
    message: SlackEventMessage
    previous_message: SlackEventMessage
    channel: str
    hidden: bool
    ts: str
    channel_type: Literal["group", "channel"]


SlackEvent = SlackEventMessage
