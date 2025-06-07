import requests
import webview


class TradingViewSession:
    """Handle TradingView authentication and chart display."""

    def __init__(self):
        self.session = requests.Session()

    def login(self, username: str, password: str) -> None:
        """Attempt to authenticate to TradingView."""
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.tradingview.com/",
        }
        data = {"username": username, "password": password, "remember": "on"}
        resp = self.session.post(
            "https://www.tradingview.com/accounts/signin/",
            headers=headers,
            data=data,
        )
        if resp.status_code != 200 or "error" in resp.text:
            raise Exception("TradingView login failed")

    def open_chart(self, symbol: str) -> None:
        """Open a TradingView chart for the given symbol."""
        url = f"https://www.tradingview.com/chart/?symbol={symbol.upper()}"
        webview.create_window(f"TradingView Chart - {symbol.upper()}", url)
        webview.start()
