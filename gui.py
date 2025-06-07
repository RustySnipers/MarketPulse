import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import threading
from backtesting import run_backtest
from ml_training import run_ml_training
from trading import start_trading_bot, stop_trading_bot
from calendar_app import CalendarApp, load_example_events
from watchlist import load_watchlist, save_watchlist
from webull_integration import login_webull, fetch_portfolio
from discord_webhook import send_discord_message
from settings import load_settings, save_settings
import time

class TradingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Bot")
        self.watchlist = load_watchlist()
        self.settings = load_settings()
        self.create_widgets()
        self.data = None
        self.trading_active = False

    def create_widgets(self):
        # Backtesting Section
        self.backtest_button = tk.Button(self.root, text="Perform Backtesting", command=self.perform_backtest)
        self.backtest_button.pack()
        self.progress_label = tk.Label(self.root, text="")
        self.progress_label.pack()

        # Configuration/Review buttons
        self.settings_button = tk.Button(self.root, text="Settings", command=self.open_settings)
        self.settings_button.pack()
        self.review_button = tk.Button(self.root, text="Review Symbols", command=self.open_symbol_review)
        self.review_button.pack()

        # ML Training Section
        self.ml_training_button = tk.Button(self.root, text="Start ML Training", command=self.start_ml_training)
        self.ml_training_button.pack()

        # Ticker Input Section
        self.ticker_label = tk.Label(self.root, text="Enter Ticker:")
        self.ticker_label.pack()
        self.ticker_entry = tk.Entry(self.root)
        self.ticker_entry.pack()

        # Watchlist Section
        self.watchlist_label = tk.Label(self.root, text="Watchlist (comma separated):")
        self.watchlist_label.pack()
        self.watchlist_entry = tk.Entry(self.root)
        self.watchlist_entry.pack()
        self.set_watchlist_button = tk.Button(self.root, text="Set Watchlist", command=self.set_watchlist)
        self.set_watchlist_button.pack()

        # Webull Portfolio Section
        self.load_portfolio_button = tk.Button(self.root, text="Load Webull Portfolio", command=self.load_webull_portfolio)
        self.load_portfolio_button.pack()
        self.portfolio_box = tk.Listbox(self.root, height=6)
        self.portfolio_box.pack(fill=tk.BOTH, expand=False)
        
        # Control Bot Section
        self.start_button = tk.Button(self.root, text="Start Trading", command=self.start_trading)
        self.start_button.pack()
        self.stop_button = tk.Button(self.root, text="Stop Trading", command=self.stop_trading)
        self.stop_button.pack()

        # Calendar Section
        self.calendar_button = tk.Button(self.root, text="Open Calendar", command=self.open_calendar)
        self.calendar_button.pack()
        
        # Report Section
        self.report_label = tk.Label(self.root, text="")
        self.report_label.pack()
    
    def perform_backtest(self):
        def backtest():
            self.root.after(0, lambda: self.progress_label.config(text="Backtesting in progress..."))
            run_backtest()
            self.root.after(0, lambda: self.progress_label.config(text="Backtesting completed. Report generated in reports folder"))
            self.root.after(0, lambda: self.report_label.config(text="Backtesting completed. Report generated in reports folder"))

        threading.Thread(target=backtest, daemon=True).start()

    def start_ml_training(self):
        def training():
            self.root.after(0, lambda: self.progress_label.config(text="ML Training in progress..."))
            run_ml_training()
            self.root.after(0, lambda: self.progress_label.config(text="ML Training completed. Report generated in reports folder"))
            self.root.after(0, lambda: self.report_label.config(text="ML Training completed. Report generated in reports folder"))

        threading.Thread(target=training, daemon=True).start()

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
        threading.Thread(target=trading, daemon=True).start()
        messagebox.showinfo("Info", "Trading started")
        send_discord_message(f"Trading started for {ticker}")

    def stop_trading(self):
        self.trading_active = False
        stop_trading_bot()
        messagebox.showinfo("Info", "Trading stopped")
        send_discord_message("Trading stopped")

    def open_calendar(self):
        top = tk.Toplevel(self.root)
        top.title("Market Calendar")
        events = load_example_events()
        CalendarApp(top, events)

    def open_settings(self):
        top = tk.Toplevel(self.root)
        top.title("Settings")
        tk.Label(top, text="Data CSV File:").pack(anchor='w')
        path_var = tk.StringVar(value=self.settings.get('data_file', ''))
        path_entry = tk.Entry(top, textvariable=path_var, width=40)
        path_entry.pack(fill=tk.X)

        def save():
            self.settings['data_file'] = path_var.get()
            save_settings(self.settings)
            messagebox.showinfo("Settings", "Settings saved")

        tk.Button(top, text="Save", command=save).pack()

    def open_symbol_review(self):
        top = tk.Toplevel(self.root)
        top.title("Symbols")
        frame = ttk.Frame(top)
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="Watchlist:").pack(anchor='w')
        watch_box = tk.Listbox(frame)
        watch_box.pack(fill=tk.BOTH, expand=True)
        for t in self.watchlist:
            watch_box.insert(tk.END, t)

        tk.Label(frame, text="Portfolio:").pack(anchor='w')
        port_box = tk.Listbox(frame)
        port_box.pack(fill=tk.BOTH, expand=True)
        for i in range(self.portfolio_box.size()):
            port_box.insert(tk.END, self.portfolio_box.get(i))

    def set_watchlist(self):
        tickers = [t.strip().upper() for t in self.watchlist_entry.get().split(',') if t.strip()]
        if not tickers:
            messagebox.showerror("Error", "Please enter at least one ticker")
            return
        self.watchlist = tickers
        save_watchlist(self.watchlist)
        messagebox.showinfo("Watchlist", "Watchlist updated")
        send_discord_message(f"Watchlist updated: {', '.join(self.watchlist)}")

    def load_webull_portfolio(self):
        username = simpledialog.askstring("Webull Login", "Username or Email:")
        password = simpledialog.askstring("Webull Login", "Password:", show='*')
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return
        mfa = simpledialog.askstring("Webull Login", "MFA Code (if applicable):", show='*')
        try:
            wb = login_webull(username=username, password=password, mfa=mfa or "")
            tickers, positions = fetch_portfolio(wb)
            if tickers:
                self.watchlist = tickers
                save_watchlist(self.watchlist)
            self.portfolio_box.delete(0, tk.END)
            for p in positions:
                symbol = p.get('ticker', 'N/A')
                qty = p.get('position', p.get('positionStr', ''))
                self.portfolio_box.insert(tk.END, f"{symbol}: {qty}")
            messagebox.showinfo("Portfolio", "Portfolio loaded from Webull")
            send_discord_message(f"Loaded Webull portfolio with {len(positions)} positions")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load portfolio: {e}")
            send_discord_message(f"Failed to load Webull portfolio: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotApp(root)
    root.mainloop()

