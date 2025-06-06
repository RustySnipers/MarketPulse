import tkinter as tk
from tkinter import messagebox
import threading
from backtesting import run_backtest
from ml_training import run_ml_training
from trading import start_trading_bot, stop_trading_bot
import time
import json
import os
from webull_integration import WebullIntegration

class TradingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Bot")
        self.create_widgets()
        self.data = None
        self.trading_active = False
        self.webull = WebullIntegration()

    def create_widgets(self):
        # Backtesting Section
        self.backtest_button = tk.Button(self.root, text="Perform Backtesting", command=self.perform_backtest)
        self.backtest_button.pack()
        self.progress_label = tk.Label(self.root, text="")
        self.progress_label.pack()

        # ML Training Section
        self.ml_training_button = tk.Button(self.root, text="Start ML Training", command=self.start_ml_training)
        self.ml_training_button.pack()

        # Ticker Input Section
        self.ticker_label = tk.Label(self.root, text="Enter Ticker:")
        self.ticker_label.pack()
        self.ticker_entry = tk.Entry(self.root)
        self.ticker_entry.pack()

        self.add_watchlist_button = tk.Button(self.root, text="Add to Watchlist", command=self.add_to_watchlist)
        self.add_watchlist_button.pack()

        self.view_watchlist_button = tk.Button(self.root, text="View Watchlist", command=self.show_watchlist)
        self.view_watchlist_button.pack()

        self.import_portfolio_button = tk.Button(self.root, text="Import Webull Portfolio", command=self.import_webull_portfolio)
        self.import_portfolio_button.pack()
        
        # Control Bot Section
        self.start_button = tk.Button(self.root, text="Start Trading", command=self.start_trading)
        self.start_button.pack()
        self.stop_button = tk.Button(self.root, text="Stop Trading", command=self.stop_trading)
        self.stop_button.pack()
        
        # Report Section
        self.report_label = tk.Label(self.root, text="")
        self.report_label.pack()
    
    def perform_backtest(self):
        def backtest():
            self.progress_label.config(text="Backtesting in progress...")
            run_backtest()
            self.progress_label.config(text="Backtesting completed. Report generated in reports folder")
            self.report_label.config(text="Backtesting completed. Report generated in reports folder")
        
        threading.Thread(target=backtest).start()

    def start_ml_training(self):
        def training():
            self.progress_label.config(text="ML Training in progress...")
            run_ml_training()
            self.progress_label.config(text="ML Training completed. Report generated in reports folder")
            self.report_label.config(text="ML Training completed. Report generated in reports folder")
        
        threading.Thread(target=training).start()

    def start_trading(self):
        ticker = self.ticker_entry.get()
        if not ticker:
            messagebox.showerror("Error", "Please enter a ticker")
            return

        def trading():
            start_trading_bot(ticker)
            while self.trading_active:
                time.sleep(1)
        
        self.trading_active = True
        threading.Thread(target=trading).start()
        messagebox.showinfo("Info", "Trading started")

    def stop_trading(self):
        self.trading_active = False
        stop_trading_bot()
        messagebox.showinfo("Info", "Trading stopped")

    def watchlist_file(self):
        return os.path.join(os.getcwd(), "watchlist.json")

    def load_watchlist(self):
        path = self.watchlist_file()
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return []

    def save_watchlist(self, tickers):
        path = self.watchlist_file()
        with open(path, "w") as f:
            json.dump(tickers, f, indent=2)

    def add_to_watchlist(self):
        ticker = self.ticker_entry.get()
        if not ticker:
            messagebox.showerror("Error", "Please enter a ticker")
            return
        watchlist = self.load_watchlist()
        if ticker not in watchlist:
            watchlist.append(ticker)
            self.save_watchlist(watchlist)
        messagebox.showinfo("Info", f"{ticker} added to watchlist")

    def show_watchlist(self):
        watchlist = self.load_watchlist()
        if not watchlist:
            msg = "Watchlist is empty"
        else:
            msg = "\n".join(watchlist)
        messagebox.showinfo("Watchlist", msg)

    def import_webull_portfolio(self):
        try:
            tickers = self.webull.get_portfolio_tickers()
            watchlist = self.load_watchlist()
            added = 0
            for t in tickers:
                if t not in watchlist:
                    watchlist.append(t)
                    added += 1
            self.save_watchlist(watchlist)
            messagebox.showinfo("Info", f"Imported {added} tickers from Webull")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotApp(root)
    root.mainloop()
