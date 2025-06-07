import json
import os

SETTINGS_FILE = "settings.json"
DEFAULTS = {
    "data_file": "data/SPY2324.csv",
    "discord_webhook": os.environ.get("DISCORD_WEBHOOK_URL", ""),
}


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            data = {}
    else:
        data = {}
    merged = DEFAULTS.copy()
    merged.update(data)
    return merged


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
