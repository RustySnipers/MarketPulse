import os
import requests

WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def send_discord_message(message: str) -> None:
    """Send a message to a Discord channel via webhook."""
    if not WEBHOOK_URL:
        print("DISCORD_WEBHOOK_URL not set; skipping Discord notification.")
        return
    data = {"content": message}
    try:
        response = requests.post(WEBHOOK_URL, json=data, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Failed to send Discord notification: {exc}")

