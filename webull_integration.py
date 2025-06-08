from webull import webull
from credential_store import delete_password, get_password, save_password

SERVICE = "webull"


def login_webull(
    username: str,
    password: str | None,
    mfa: str = "",
    device_name: str = "MarketPulse",
    save: bool = False,
) -> webull:
    """Login to Webull and return the authenticated instance."""
    if password is None:
        password = get_password(SERVICE, username)
        if password is None:
            raise ValueError("Password required for Webull login")
    wb = webull()
    wb.login(username=username, password=password, device_name=device_name, mfa=mfa)
    if save:
        save_password(SERVICE, username, password)
    return wb


def fetch_portfolio(wb):
    """Return (tickers, raw positions) from the account portfolio."""
    data = wb.get_positions()
    tickers = [p.get("ticker", "").upper() for p in data if p.get("ticker")]
    return tickers, data


def clear_saved_webull(username: str) -> None:
    """Remove saved Webull credentials."""
    delete_password(SERVICE, username)
