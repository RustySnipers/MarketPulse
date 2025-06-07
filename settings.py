import json
import os

SETTINGS_FILE = "settings.json"
DEFAULTS = {
    "data_file": "data/SPY2324.csv",
    "discord_webhook": os.environ.get("DISCORD_WEBHOOK_URL", "")
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}
    merged = DEFAULTS.copy()
    merged.update(data)
    return merged


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)
