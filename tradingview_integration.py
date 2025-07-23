import requests
import webview
from credential_store import delete_password, get_password, save_password
from utils.formatting import format_symbol_for_tradingview

SERVICE_USER = "tradingview_user"
SERVICE_PASS = "tradingview_pass"


class TradingViewSession:
    """Handle TradingView authentication and chart display."""

    def __init__(self):
        self.session = requests.Session()

    def login(self, username: str, password: str | None, save: bool = False) -> None:
        """Attempt to authenticate to TradingView."""
        if password is None:
            password = get_password(SERVICE_PASS, username)
            if password is None:
                raise ValueError("Password required for TradingView login")
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
        if save:
            save_password(SERVICE_USER, username, username)
            save_password(SERVICE_PASS, username, password)

    def open_chart(self, symbol: str, interval: str = "D") -> None:
        """Open a TradingView chart for the given symbol."""
        formatted_symbol = format_symbol_for_tradingview(symbol)
        url = f"https://www.tradingview.com/chart/?symbol={formatted_symbol}&interval={interval}"
        self.window = webview.create_window(f"TradingView Chart - {symbol.upper()}", url)
        webview.start()

    def change_symbol(self, symbol: str, interval: str = "D") -> None:
        """Change the symbol on the current TradingView chart."""
        if self.window:
            formatted_symbol = format_symbol_for_tradingview(symbol)
            url = f"https://www.tradingview.com/chart/?symbol={formatted_symbol}&interval={interval}"
            self.window.load_url(url)


def clear_saved_tradingview(username: str) -> None:
    """Remove stored TradingView credentials."""
    delete_password(SERVICE_USER, username)
    delete_password(SERVICE_PASS, username)

