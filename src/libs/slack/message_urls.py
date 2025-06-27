"""Message urls."""

from src.models.slack.events import SlackEvent


def create_slack_message_url(slack_event: SlackEvent) -> str:
    """Create slack message url."""
    if slack_event.thread_ts:
        url = (
            f"https://rehatchhq.slack.com/archives/{slack_event.channel}/p"
            f"{(slack_event.ts).replace('.', '')}/"
            f"?thread_ts={(slack_event.thread_ts)}"
            f"&cid={slack_event.channel.upper()}"
        )
        return url

    url = (
        f"https://rehatchhq.slack.com/archives/{slack_event.channel}/p"
        f"{(slack_event.ts).replace('.', '')}"
        f"?cid={slack_event.channel.upper()}"
    )

    return url
