import os
import requests


def send_discord_message(content: str, username: str = "MarketPulse", embeds=None):
    """Send a simple message to the configured Discord webhook."""
    url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not url:
        print("Discord webhook URL not configured")
        return False
    payload = {"content": content, "username": username}
    if embeds:
        payload["embeds"] = embeds
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as exc:
        print(f"Failed to send Discord message: {exc}")
        return False


if __name__ == "__main__":
    send_discord_message("Discord webhook test from MarketPulse")
