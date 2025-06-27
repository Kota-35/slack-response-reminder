"""Slackの型定義."""

from typing import Literal

from pydantic import BaseModel

from src.models.slack.events import SlackEvent


class SlackUrlVerificationResponse(BaseModel):
    """Slack event url verification response."""

    token: str
    type: Literal["url_verification"]
    challenge: str


class SlackEventCallbackResponse(BaseModel):
    """Slack event callback response."""

    token: str
    team_id: str
    context_team_id: str | None = None
    context_enterprise_id: str | None = None
    type: Literal["event_callback"]
    event: SlackEvent


SlackEventRequest = SlackUrlVerificationResponse | SlackEventCallbackResponse


class SlackEventHeaders(BaseModel):
    """Slack event request headers."""

    host: str
    user_agent: str
    content_type: str
    x_slack_retry_num: int | None = None
    x_slack_retry_reason: str | None = None
