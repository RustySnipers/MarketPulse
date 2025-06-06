import json
import os

WATCHLIST_FILE = "watchlist.json"


def load_watchlist():
    """Load watchlist tickers from file."""
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, "r") as f:
            return json.load(f)
    return []


def save_watchlist(tickers):
    """Save the list of tickers to file."""
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(sorted(set(tickers)), f, indent=2)
