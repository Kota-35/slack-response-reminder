"""Notion database query."""

from typing import Any, Self

from httpx import AsyncClient
from pydantic import BaseModel, Field

from src.libs.notion.types import (
    PeopleProperty,
    RichTextProperty,
    StatusProperty,
    TitleProperty,
)
from src.libs.settings import env


class ClientConfig(BaseModel):
    """Client config."""

    client: str
    outside_channel_id: str
    managers: list[str]
    status: bool

    @classmethod
    def from_notion_result(cls, result: dict[str, Any]) -> Self:
        """Validate managers."""
        properties: dict[str, Any] = result["properties"]
        client_property: TitleProperty = TitleProperty(
            **properties["クライアント名"],
        )
        outside_channel_id_property: RichTextProperty = RichTextProperty(
            **properties["社外チャンネルID"],
        )
        notion_managers: PeopleProperty = PeopleProperty(**properties["担当者"])
        status_property: StatusProperty = StatusProperty(
            **properties["ステータス"],
        )

        return cls(
            client=client_property.title[0].plain_text,
            outside_channel_id=outside_channel_id_property.rich_text[
                0
            ].plain_text,
            managers=[
                manager.id
                for manager in notion_managers.people
                if manager is not None
            ],
            status=True if status_property.status.name == "完了" else False,
        )


class MemberProp(BaseModel):
    """Member info."""

    name: str = Field(description="name")
    slack_id: str = Field(description="slack id")


class MemberInformation(BaseModel):
    """Member slack Information."""

    members: list[MemberProp] = Field(description="members")

    @classmethod
    def from_notion_result(cls, results: list[dict[str, Any]]) -> Self:
        """Validate slack ids."""
        members: list[MemberProp] = []
        for result in results:
            properties: dict[str, Any] = result["properties"]
            slack_id_property: RichTextProperty = RichTextProperty(
                **properties["slackId"],
            )
            name_property: TitleProperty = TitleProperty(
                **properties["name"],
            )
            members.append(
                MemberProp(
                    name=name_property.title[0].plain_text,
                    slack_id=slack_id_property.rich_text[0].plain_text,
                ),
            )

        return cls(members=members)


async def get_config_from_notion(
    client: AsyncClient,
    database_id: str,
    channel_id: str,
) -> ClientConfig:
    """Get config from notion."""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = await client.post(
        url=url,
        headers={
            "Authorization": f"Bearer {env.notion_api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        },
        json={
            "filter": {
                "property": "社外チャンネルID",
                "rich_text": {"contains": channel_id},
            },
        },
    )
    json_response = response.json()
    results = json_response["results"]
    if len(results) == 1:
        return ClientConfig.from_notion_result(results[0])
    msg = "Client config not found"
    raise ValueError(msg)


async def get_member_info(
    client: AsyncClient,
    database_id: str,
    user_ids: list[str],
) -> MemberInformation:
    """Get member info."""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = await client.post(
        url=url,
        headers={
            "Authorization": f"Bearer {env.notion_api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        },
        json={
            "filter": {
                "or": [
                    {"property": "user", "people": {"contains": user_id}}
                    for user_id in user_ids
                ],
            },
        },
    )
    json_response = response.json()
    member_information = MemberInformation.from_notion_result(
        json_response["results"],
    )
    return member_information


async def get_all_config(
    client: AsyncClient,
    database_id: str,
) -> list[ClientConfig]:
    """Get all config."""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = await client.post(
        url=url,
        headers={
            "Authorization": f"Bearer {env.notion_api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        },
    )
    json_response = response.json()
    results = json_response["results"]
    if len(results) == 0:
        msg = "Client config not found"
        raise ValueError(msg)

    return [ClientConfig.from_notion_result(result) for result in results]
