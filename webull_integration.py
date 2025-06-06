import os
from webull import webull

class WebullIntegration:
    def __init__(self):
        self.wb = webull()
        self.logged_in = False

    def login(self):
        if self.logged_in:
            return
        username = os.environ.get("WEBULL_USERNAME")
        password = os.environ.get("WEBULL_PASSWORD")
        if not username or not password:
            raise ValueError("Webull credentials not provided. Set WEBULL_USERNAME and WEBULL_PASSWORD environment variables.")
        self.wb.login(username=username, password=password)
        self.logged_in = True

    def get_positions(self):
        self.login()
        return self.wb.get_positions()

    def get_portfolio_tickers(self):
        positions = self.get_positions()
        tickers = []
        for pos in positions:
            symbol = pos.get('ticker') or pos.get('symbol')
            if symbol:
                tickers.append(symbol)
        return tickers
