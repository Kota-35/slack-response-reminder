"""Slack Replies."""

from typing import Literal

from pydantic import BaseModel, Field


class SlackMessage(BaseModel):
    """Slack Message."""

    user: str
    type: Literal["message"]
    ts: str
    text: str
    team: str
    user_team: str | None = Field(default=None)
    thread_ts: str | None = Field(default=None)
