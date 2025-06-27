"""水曜日定期実行Weekly check."""

import httpx
from fastapi import APIRouter, Response

from src.libs.notion.client import get_all_client_settings
from src.libs.settings import env

router = APIRouter()


@router.post("/weekly-check")
async def weekly_check() -> Response:
    """水曜日定期実行Weekly check."""
    all_client_settings = await get_all_client_settings()

    async with httpx.AsyncClient() as client:
        for member_info, config in all_client_settings:
            if config.status:
                await client.post(
                    url=f"{env.server_url}/api/v1/tasks/channel-check",
                    json={
                        "channel_id": config.outside_channel_id,
                        "member_info": member_info.model_dump(mode="json"),
                    },
                )

    return Response(status_code=200)
