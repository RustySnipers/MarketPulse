import tkinter as tk
from tkinter import ttk
import re
import time
import threading
from trading import start_trading_bot, stop_trading_bot
from calendar_app import CalendarApp, load_events
from discord_webhook import send_discord_message
from dialogs import showinfo, showerror

class TradingFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Trading")
        self.parent = parent
        self.ticker_pattern = re.compile(r"^[A-Za-z0-9.-]{1,10}$")
        self.trading_active = False
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Enter Ticker:").grid(column=0, row=0, sticky="w")
        self.ticker_entry = ttk.Entry(self)
        self.ticker_entry.grid(column=1, row=0, sticky="ew")
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Watchlist (comma separated):").grid(column=0, row=1, sticky="w")
        self.watchlist_entry = ttk.Entry(self)
        self.watchlist_entry.grid(column=1, row=1, sticky="ew")
        self.set_watchlist_button = ttk.Button(self, text="Set Watchlist", command=self.set_watchlist)
        self.set_watchlist_button.grid(column=2, row=1, sticky="ew")
        self.columnconfigure(2, weight=0)

        self.start_button = ttk.Button(self, text="Start Trading", command=self.start_trading)
        self.start_button.grid(column=0, row=2, sticky="ew")
        self.stop_button = ttk.Button(self, text="Stop Trading", command=self.stop_trading, state="disabled")
        self.stop_button.grid(column=1, row=2, sticky="ew")
        self.calendar_button = ttk.Button(self, text="Open Calendar", command=self.open_calendar)
        self.calendar_button.grid(column=2, row=2, sticky="ew")

    def start_trading(self):
        if self.trading_active:
            showerror(self, "Error", "Trading is already active.")
            return

        ticker = self.ticker_entry.get().strip().upper()
        if not ticker or not self.ticker_pattern.match(ticker):
            showerror(self, "Error", "Please enter a ticker")
            return

        def trading():
            start_trading_bot(ticker)
            self.parent.after(0, self.stop_trading)

        self.trading_active = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        threading.Thread(target=trading, daemon=True).start()
        showinfo(self, "Info", "Trading started")
        send_discord_message(f"Trading started for {ticker}")

    def stop_trading(self):
        if not self.trading_active:
            return
        self.trading_active = False
        stop_trading_bot()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        showinfo(self, "Info", "Trading stopped")
        send_discord_message("Trading stopped")

    def open_calendar(self):
        top = tk.Toplevel(self.master)
        top.title("Market Calendar")
        events = load_events()
        CalendarApp(top, events)

    def set_watchlist(self):
        from watchlist import save_watchlist
        tickers = [t.strip().upper() for t in self.watchlist_entry.get().split(',') if t.strip()]
        if not tickers:
            showerror(self, "Error", "Please enter at least one ticker")
            return
        self.parent.watchlist = tickers
        save_watchlist(self.parent.watchlist)
        showinfo(self, "Watchlist", "Watchlist updated")
        send_discord_message(f"Watchlist updated: {', '.join(self.parent.watchlist)}")
