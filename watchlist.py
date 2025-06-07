import json
import os

WATCHLIST_FILE = "watchlist.json"


def load_watchlist():
    """Load watchlist tickers from file."""
    if os.path.exists(WATCHLIST_FILE):
        try:
            with open(WATCHLIST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return []
    return []


def save_watchlist(tickers):
    """Save the list of tickers to file."""
    with open(WATCHLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(set(tickers)), f, indent=2)
