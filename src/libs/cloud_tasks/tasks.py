"""Cloud Tasks Task."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from google.protobuf import timestamp_pb2

from src.libs.cloud_tasks.client import create_cloud_tasks_client
from src.libs.settings import env
from src.models.slack.events import SlackEvent


class CreateCloudTasksError(Exception):
    """Create Cloud Tasks Error."""


class DeleteCloudTasksError(Exception):
    """Delete Cloud Tasks Error."""


async def create_tasks(slack_event: SlackEvent) -> None:
    """Create Cloud Tasks Task.

    Returns:
        str: 作成されたタスクの名前
    """
    client = create_cloud_tasks_client()
    parent = client.queue_path(
        project=env.project_id,
        location=env.location,
        queue=env.queue_id,
    )

    timestamp = timestamp_pb2.Timestamp()  # ty: ignore[unresolved-attribute]
    feature_time = datetime.now(ZoneInfo("Asia/Tokyo")) + timedelta(hours=3)
    timestamp.FromDatetime(feature_time)

    task = {
        "name": f"{parent}/tasks/{slack_event.channel}-{slack_event.user}-{slack_event.ts.replace('.', '_')}",
        "http_request": {
            "url": f"{env.server_url}/api/v1/tasks/check",
            "headers": {"Content-Type": "application/json"},
            "body": slack_event.model_dump_json().encode(),
        },
        "schedule_time": timestamp,
    }

    # Cloud Tasks へタスクを追加
    try:
        await client.create_task(parent=parent, task=task)
    except Exception as e:
        raise CreateCloudTasksError(e) from e
