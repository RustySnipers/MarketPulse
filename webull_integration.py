from webull import webull


def login_webull(username: str, password: str, mfa: str = "", device_name: str = "MarketPulse"):
    """Login to Webull and return the authenticated instance."""
    wb = webull()
    wb.login(username=username, password=password, device_name=device_name, mfa=mfa)
    return wb


def fetch_portfolio(wb):
    """Return (tickers, raw positions) from the account portfolio."""
    data = wb.get_positions()
    tickers = [p.get("ticker", "").upper() for p in data if p.get("ticker")]
    return tickers, data
