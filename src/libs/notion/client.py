"""Notion client setting."""

import httpx
from httpx import AsyncClient

from src.libs.notion.database_query import (
    ClientConfig,
    MemberInformation,
    get_all_config,
    get_config_from_notion,
    get_member_info,
)
from src.libs.settings import env


async def get_setting_only(
    channel_id: str,
) -> ClientConfig:
    """Get client config only."""
    async with AsyncClient(timeout=httpx.Timeout(5.0, read=10.0)) as client:
        client_config = await get_config_from_notion(
            client,
            env.notion_client_database_id,
            channel_id,
        )

    return client_config


async def client_setting(
    channel_id: str,
) -> tuple[MemberInformation, ClientConfig]:
    """Get client setting and member information from Notion.

    Args:
        channel_id: Slack channel ID

    Returns:
        tuple[MemberInformation, ClientConfig]: Member information and client configuration
    """
    # FYI: ReadTimeoutErrorが出るためタイムアウトを設定.
    # ref: https://nikkie-ftnext.hatenablog.com/entry/grasp-httpx-client-timeout
    async with AsyncClient(timeout=httpx.Timeout(5.0, read=10.0)) as client:
        client_config = await get_config_from_notion(
            client,
            env.notion_client_database_id,
            channel_id,
        )

        member_information = await get_member_info(
            client,
            env.notion_member_database_id,
            client_config.managers,
        )
        return member_information, client_config


async def get_all_client_settings() -> list[
    tuple[MemberInformation, ClientConfig]
]:
    """Get all client config."""
    async with AsyncClient(timeout=httpx.Timeout(5.0, read=10.0)) as client:
        all_config = await get_all_config(
            client,
            env.notion_client_database_id,
        )

        all_member_info = [
            await get_member_info(
                client,
                database_id=env.notion_member_database_id,
                user_ids=config.managers,
            )
            for config in all_config
        ]

    return [
        (member_info, config)
        for member_info, config in zip(
            all_member_info,
            all_config,
            strict=False,
        )
    ]
