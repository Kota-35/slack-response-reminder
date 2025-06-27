"""Slackのクライアント."""

from slack_sdk.web.async_client import AsyncWebClient

from src.libs.settings import env


def create_slack_client() -> AsyncWebClient:
    """Slackのクライアントを作成する."""
    return AsyncWebClient(token=env.slack_bot_token)
