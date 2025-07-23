import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import threading
import re
from backtesting import run_backtest
from ml_training import run_ml_training
from trading import start_trading_bot, stop_trading_bot
from calendar_app import CalendarApp, load_events
from tradingview_integration import TradingViewSession, clear_saved_tradingview
from watchlist import load_watchlist, save_watchlist
from webull_integration import login_webull, fetch_portfolio, clear_saved_webull
from discord_webhook import send_discord_message
from settings import load_settings, save_settings
import time

class TradingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Bot")
        self.watchlist = load_watchlist()
        self.settings = load_settings()
        self.tv_session = TradingViewSession()
        self.ticker_pattern = re.compile(r"^[A-Za-z0-9.-]{1,10}$")
        self.style = ttk.Style()
        if self.settings.get('theme') == 'dark':
            self.style.theme_use('clam')
        self.create_widgets()
        self.data = None
        self.trading_active = False

    def create_widgets(self):

        main = ttk.Frame(self.root)
        main.grid(column=0, row=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        data_frame = ttk.LabelFrame(main, text="Data & Analysis")
        data_frame.grid(column=0, row=0, padx=5, pady=5, sticky="ew")

        trade_frame = ttk.LabelFrame(main, text="Trading")
        trade_frame.grid(column=0, row=1, padx=5, pady=5, sticky="ew")

        integ_frame = ttk.LabelFrame(main, text="Integrations")
        integ_frame.grid(column=0, row=2, padx=5, pady=5, sticky="ew")

        # Backtesting Section
        self.backtest_button = ttk.Button(data_frame, text="Perform Backtesting", command=self.perform_backtest)
        self.backtest_button.grid(column=0, row=0, sticky="ew")
        self.ml_training_button = ttk.Button(data_frame, text="Start ML Training", command=self.start_ml_training)
        self.ml_training_button.grid(column=1, row=0, sticky="ew")
        data_frame.columnconfigure((0,1), weight=1)
        self.progress = ttk.Progressbar(data_frame, mode="indeterminate")
        self.progress.grid(column=0, row=1, columnspan=2, sticky="ew")
        self.progress_label = ttk.Label(data_frame, text="")
        self.progress_label.grid(column=0, row=2, columnspan=2, sticky="ew")

        # Ticker Input
        ttk.Label(trade_frame, text="Enter Ticker:").grid(column=0, row=0, sticky="w")
        self.ticker_entry = ttk.Entry(trade_frame)
        self.ticker_entry.grid(column=1, row=0, sticky="ew")
        trade_frame.columnconfigure(1, weight=1)

        # Configuration/Review buttons
        self.settings_button = ttk.Button(integ_frame, text="Settings", command=self.open_settings)
        self.settings_button.grid(column=0, row=0, sticky="ew")
        self.review_button = ttk.Button(integ_frame, text="Review Symbols", command=self.open_symbol_review)
        self.review_button.grid(column=1, row=0, sticky="ew")
        integ_frame.columnconfigure((0,1), weight=1)

        # Watchlist Section
        ttk.Label(trade_frame, text="Watchlist (comma separated):").grid(column=0, row=1, sticky="w")
        self.watchlist_entry = ttk.Entry(trade_frame)
        self.watchlist_entry.grid(column=1, row=1, sticky="ew")
        self.set_watchlist_button = ttk.Button(trade_frame, text="Set Watchlist", command=self.set_watchlist)
        self.set_watchlist_button.grid(column=2, row=1, sticky="ew")
        trade_frame.columnconfigure(2, weight=0)

        # Webull Portfolio Section
        self.load_portfolio_button = ttk.Button(integ_frame, text="Load Webull Portfolio", command=self.load_webull_portfolio)
        self.load_portfolio_button.grid(column=0, row=1, sticky="ew")
        self.portfolio_box = tk.Listbox(integ_frame, height=6)
        self.portfolio_box.grid(column=0, row=2, columnspan=2, sticky="ew")

        # TradingView Section
        self.tv_login_button = ttk.Button(integ_frame, text="Login TradingView", command=self.login_tradingview)
        self.tv_login_button.grid(column=1, row=1, sticky="ew")
        self.tv_chart_button = ttk.Button(integ_frame, text="Open TradingView Chart", command=self.open_tradingview_chart)
        self.tv_chart_button.grid(column=1, row=2, sticky="ew")

        # Control Bot Section
        self.start_button = ttk.Button(trade_frame, text="Start Trading", command=self.start_trading)
        self.start_button.grid(column=0, row=2, sticky="ew")
        self.stop_button = ttk.Button(trade_frame, text="Stop Trading", command=self.stop_trading)
        self.stop_button.grid(column=1, row=2, sticky="ew")
        self.calendar_button = ttk.Button(trade_frame, text="Open Calendar", command=self.open_calendar)
        self.calendar_button.grid(column=2, row=2, sticky="ew")

        # Report Section
        self.report_label = ttk.Label(main, text="")
        self.report_label.grid(column=0, row=3, sticky="ew")
    
    def perform_backtest(self):
        def backtest():
            self.root.after(0, self.progress.start)
            self.root.after(0, lambda: self.progress_label.config(text="Backtesting in progress..."))
            run_backtest()
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.progress_label.config(text="Backtesting completed. Report generated in reports folder"))
            self.root.after(0, lambda: self.report_label.config(text="Backtesting completed. Report generated in reports folder"))
            self.root.after(0, lambda: self.backtest_button.config(state="normal"))

        self.backtest_button.config(state="disabled")
        threading.Thread(target=backtest, daemon=True).start()

    def start_ml_training(self):
        def training():
            self.root.after(0, self.progress.start)
            self.root.after(0, lambda: self.progress_label.config(text="ML Training in progress..."))
            run_ml_training()
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.progress_label.config(text="ML Training completed. Report generated in reports folder"))
            self.root.after(0, lambda: self.report_label.config(text="ML Training completed. Report generated in reports folder"))
            self.root.after(0, lambda: self.ml_training_button.config(state="normal"))

        self.ml_training_button.config(state="disabled")
        threading.Thread(target=training, daemon=True).start()

    def start_trading(self):
        ticker = self.ticker_entry.get().strip().upper()
        if not ticker or not self.ticker_pattern.match(ticker):
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
        events = load_events()
        CalendarApp(top, events)

    def login_tradingview(self):
        username = simpledialog.askstring("TradingView Login", "Username:")
        password = simpledialog.askstring("TradingView Login", "Password:", show='*')
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return
        try:
            save = messagebox.askyesno("Save Credentials", "Save TradingView credentials?")
            self.tv_session.login(username, password, save=save)
            if save:
                self.settings['tradingview_user'] = username
                save_settings(self.settings)
            messagebox.showinfo("TradingView", "Login successful")
        except Exception as e:
            messagebox.showerror("Error", f"TradingView login failed: {e}")

    def open_tradingview_chart(self):
        ticker = self.ticker_entry.get().strip().upper()
        if not ticker or not self.ticker_pattern.match(ticker):
            messagebox.showerror("Error", "Please enter a ticker")
            return
        try:
            self.tv_session.open_chart(ticker)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open chart: {e}")

    def open_settings(self):
        top = tk.Toplevel(self.root)
        top.title("Settings")
        tk.Label(top, text="Data CSV File:").pack(anchor='w')
        path_var = tk.StringVar(value=self.settings.get('data_file', ''))
        path_entry = tk.Entry(top, textvariable=path_var, width=40)
        path_entry.pack(fill=tk.X)

        tk.Label(top, text="Discord Webhook URL:").pack(anchor='w')
        webhook_var = tk.StringVar(value=self.settings.get('discord_webhook', ''))
        webhook_entry = tk.Entry(top, textvariable=webhook_var, width=40)
        webhook_entry.pack(fill=tk.X)

        tk.Label(top, text="Theme:").pack(anchor='w')
        theme_var = tk.StringVar(value=self.settings.get('theme', 'light'))
        ttk.Combobox(top, textvariable=theme_var, values=['light', 'dark'], state='readonly').pack(fill=tk.X)

        cred_frame = ttk.LabelFrame(top, text="Credentials")
        cred_frame.pack(fill=tk.X, pady=5)
        wb_label = ttk.Label(cred_frame, text=f"Webull: {self.settings.get('webull_user') or 'None'}")
        wb_label.grid(column=0, row=0, sticky="w")
        ttk.Button(cred_frame, text="Clear", command=lambda:self.clear_credential('webull')).grid(column=1, row=0)
        tv_label = ttk.Label(cred_frame, text=f"TradingView: {self.settings.get('tradingview_user') or 'None'}")
        tv_label.grid(column=0, row=1, sticky="w")
        ttk.Button(cred_frame, text="Clear", command=lambda:self.clear_credential('tradingview')).grid(column=1, row=1)

        def save():
            self.settings['data_file'] = path_var.get()
            self.settings['discord_webhook'] = webhook_var.get()
            self.settings['theme'] = theme_var.get()
            save_settings(self.settings)
            if self.settings['theme'] == 'dark':
                self.style.theme_use('clam')
            else:
                self.style.theme_use('default')
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

    def clear_credential(self, service: str):
        username = self.settings.get(f'{service}_user')
        if not username:
            messagebox.showinfo("Info", f"No {service.capitalize()} credentials to clear.")
            return

        if service == 'webull':
            clear_saved_webull(username)
            self.settings['webull_user'] = ''
        elif service == 'tradingview':
            clear_saved_tradingview(username)
            self.settings['tradingview_user'] = ''

        save_settings(self.settings)
        messagebox.showinfo("Credentials", f"{service.capitalize()} credentials cleared.")


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
            save = messagebox.askyesno("Save Credentials", "Save Webull credentials?")
            wb = login_webull(username=username, password=password, mfa=mfa or "", save=save)
            if save:
                self.settings['webull_user'] = username
                save_settings(self.settings)
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

