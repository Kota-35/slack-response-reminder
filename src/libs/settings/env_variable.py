"""Env variables."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    """Env settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        min_length=1,
    )

    google_application_credentials: str = Field(
        default="",
        validation_alias="GOOGLE_APPLICATION_CREDENTIALS",
        description="Google Application Credentials",
        min_length=1,
    )

    project_id: str = Field(
        default="",
        validation_alias="PROJECT_ID",
        description="Project ID",
        min_length=1,
    )

    location: str = Field(
        default="",
        validation_alias="LOCATION",
        description="Location",
        min_length=1,
    )

    queue_id: str = Field(
        default="",
        validation_alias="QUEUE_ID",
        description="Queue ID",
        min_length=1,
    )

    server_url: str = Field(
        default="",
        validation_alias="SERVER_URL",
        description="Server URL",
        min_length=1,
    )

    slack_team_id: str = Field(
        default="",
        validation_alias="SLACK_TEAM_ID",
        description="Slack Team ID",
        min_length=1,
    )

    slack_bot_token: str = Field(
        default="",
        validation_alias="SLACK_BOT_TOKEN",
        description="Slack Bot Token",
        min_length=1,
    )

    slack_log_channel_id: str = Field(
        default="",
        validation_alias="SLACK_LOG_CHANNEL_ID",
        description="Slack Log Channel ID",
        min_length=1,
    )

    notion_api_key: str = Field(
        default="",
        validation_alias="NOTION_API_KEY",
        description="Notion API Key",
        min_length=1,
    )

    notion_client_database_id: str = Field(
        default="",
        validation_alias="NOTION_CLIENT_DATABASE_ID",
        description="Notion Client Database ID",
        min_length=1,
    )

    notion_member_database_id: str = Field(
        default="",
        validation_alias="NOTION_MEMBER_DATABASE_ID",
        description="Notion Member Database ID",
        min_length=1,
    )
