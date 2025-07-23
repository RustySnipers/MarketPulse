import tkinter as tk
from tkinter import ttk
from tradingview_integration import TradingViewSession, clear_saved_tradingview
from webull_integration import login_webull, fetch_portfolio, clear_saved_webull
from discord_webhook import send_discord_message
from settings import save_settings
from dialogs import askstring, askyesno, showinfo, showerror

class IntegrationsFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Integrations")
        self.parent = parent
        self.tv_session = TradingViewSession()
        self.create_widgets()

    def create_widgets(self):
        self.settings_button = ttk.Button(self, text="Settings", command=self.open_settings)
        self.settings_button.grid(column=0, row=0, sticky="ew")
        self.review_button = ttk.Button(self, text="Review Symbols", command=self.open_symbol_review)
        self.review_button.grid(column=1, row=0, sticky="ew")
        self.columnconfigure((0,1), weight=1)

        self.load_portfolio_button = ttk.Button(self, text="Load Webull Portfolio", command=self.load_webull_portfolio)
        self.load_portfolio_button.grid(column=0, row=1, sticky="ew")
        self.portfolio_box = tk.Listbox(self, height=6)
        self.portfolio_box.grid(column=0, row=2, columnspan=2, sticky="ew")

        self.tv_login_button = ttk.Button(self, text="Login TradingView", command=self.login_tradingview)
        self.tv_login_button.grid(column=1, row=1, sticky="ew")
        self.tv_chart_button = ttk.Button(self, text="Open TradingView Chart", command=self.open_tradingview_chart)
        self.tv_chart_button.grid(column=1, row=2, sticky="ew")

    def open_settings(self):
        top = tk.Toplevel(self.master)
        top.title("Settings")
        tk.Label(top, text="Data CSV File:").pack(anchor='w')
        path_var = tk.StringVar(value=self.parent.settings.get('data_file', ''))
        path_entry = tk.Entry(top, textvariable=path_var, width=40)
        path_entry.pack(fill=tk.X)

        tk.Label(top, text="Discord Webhook URL:").pack(anchor='w')
        webhook_var = tk.StringVar(value=self.parent.settings.get('discord_webhook', ''))
        webhook_entry = tk.Entry(top, textvariable=webhook_var, width=40)
        webhook_entry.pack(fill=tk.X)

        tk.Label(top, text="Theme:").pack(anchor='w')
        theme_var = tk.StringVar(value=self.parent.settings.get('theme', 'light'))
        ttk.Combobox(top, textvariable=theme_var, values=['light', 'dark'], state='readonly').pack(fill=tk.X)

        cred_frame = ttk.LabelFrame(top, text="Credentials")
        cred_frame.pack(fill=tk.X, pady=5)
        wb_label = ttk.Label(cred_frame, text=f"Webull: {self.parent.settings.get('webull_user') or 'None'}")
        wb_label.grid(column=0, row=0, sticky="w")
        ttk.Button(cred_frame, text="Clear", command=lambda:self.clear_credential('webull')).grid(column=1, row=0)
        tv_label = ttk.Label(cred_frame, text=f"TradingView: {self.parent.settings.get('tradingview_user') or 'None'}")
        tv_label.grid(column=0, row=1, sticky="w")
        ttk.Button(cred_frame, text="Clear", command=lambda:self.clear_credential('tradingview')).grid(column=1, row=1)

        def save():
            self.parent.settings['data_file'] = path_var.get()
            self.parent.settings['discord_webhook'] = webhook_var.get()
            self.parent.settings['theme'] = theme_var.get()
            save_settings(self.parent.settings)
            if self.parent.settings['theme'] == 'dark':
                self.parent.style.theme_use('clam')
            else:
                self.parent.style.theme_use('default')
            showinfo(self, "Settings", "Settings saved")

        tk.Button(top, text="Save", command=save).pack()

    def open_symbol_review(self):
        top = tk.Toplevel(self.master)
        top.title("Symbols")
        frame = ttk.Frame(top)
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="Watchlist:").pack(anchor='w')
        watch_box = tk.Listbox(frame)
        watch_box.pack(fill=tk.BOTH, expand=True)
        for t in self.parent.watchlist:
            watch_box.insert(tk.END, t)

        tk.Label(frame, text="Portfolio:").pack(anchor='w')
        port_box = tk.Listbox(frame)
        port_box.pack(fill=tk.BOTH, expand=True)
        for i in range(self.portfolio_box.size()):
            port_box.insert(tk.END, self.portfolio_box.get(i))

    def clear_credential(self, service: str):
        username = self.parent.settings.get(f'{service}_user')
        if not username:
            showinfo(self, "Info", f"No {service.capitalize()} credentials to clear.")
            return

        if service == 'webull':
            clear_saved_webull(username)
            self.parent.settings['webull_user'] = ''
        elif service == 'tradingview':
            clear_saved_tradingview(username)
            self.parent.settings['tradingview_user'] = ''

        save_settings(self.parent.settings)
        showinfo(self, "Credentials", f"{service.capitalize()} credentials cleared.")

    def login_tradingview(self):
        username = askstring(self, "TradingView Login", "Username:")
        if not username: return
        password = askstring(self, "TradingView Login", "Password:")
        if not password: return

        try:
            save = askyesno(self, "Save Credentials", "Save TradingView credentials?")
            self.tv_session.login(username, password, save=save)
            if save:
                self.parent.settings['tradingview_user'] = username
                save_settings(self.parent.settings)
            showinfo(self, "TradingView", "Login successful")
        except Exception as e:
            showerror(self, "Error", f"TradingView login failed: {e}")

    def open_tradingview_chart(self):
        ticker = self.parent.trading_frame.ticker_entry.get().strip().upper()
        interval = self.parent.trading_frame.time_period_var.get()
        if not ticker:
            showerror(self, "Error", "Please enter a ticker in the trading frame.")
            return
        try:
            self.tv_session.open_chart(ticker, interval)
        except Exception as e:
            showerror(self, "Error", f"Failed to open chart: {e}")

    def load_webull_portfolio(self):
        from watchlist import save_watchlist
        username = askstring(self, "Webull Login", "Username or Email:")
        if not username: return
        password = askstring(self, "Webull Login", "Password:")
        if not password: return
        mfa = askstring(self, "Webull Login", "MFA Code (if applicable):")

        try:
            save = askyesno(self, "Save Credentials", "Save Webull credentials?")
            wb = login_webull(username=username, password=password, mfa=mfa or "", save=save)
            if save:
                self.parent.settings['webull_user'] = username
                save_settings(self.parent.settings)
            tickers, positions = fetch_portfolio(wb)
            if tickers:
                self.parent.watchlist = tickers
                save_watchlist(self.parent.watchlist)
            self.portfolio_box.delete(0, tk.END)
            for p in positions:
                symbol = p.get('ticker', 'N/A')
                qty = p.get('position', p.get('positionStr', ''))
                self.portfolio_box.insert(tk.END, f"{symbol}: {qty}")
            showinfo(self, "Portfolio", "Portfolio loaded from Webull")
            send_discord_message(f"Loaded Webull portfolio with {len(positions)} positions")
        except Exception as e:
            showerror(self, "Error", f"Failed to load portfolio: {e}")
            send_discord_message(f"Failed to load Webull portfolio: {e}")
