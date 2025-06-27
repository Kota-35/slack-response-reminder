"""Cloud Tasks Client."""

from google.cloud import tasks_v2


def create_cloud_tasks_client() -> tasks_v2.CloudTasksAsyncClient:
    """Create Cloud Tasks Client."""
    try:
        cloud_tasks_client = tasks_v2.CloudTasksAsyncClient()
        return cloud_tasks_client  # noqa: TRY300
    except Exception as e:
        print(f"Error creating Cloud Tasks client: {e}")
        raise e  # noqa: TRY201
