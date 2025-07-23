import tkinter as tk
from tkinter import ttk
from settings import load_settings
from watchlist import load_watchlist
from gui_data_analysis import DataAnalysisFrame
from gui_trading import TradingFrame
from gui_integrations import IntegrationsFrame

class TradingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Bot")
        self.watchlist = load_watchlist()
        self.settings = load_settings()
        self.style = ttk.Style()
        if self.settings.get('theme') == 'dark':
            self.style.theme_use('clam')
        self.create_widgets()
        self.data = None

    def create_widgets(self):
        main = ttk.Frame(self.root)
        main.grid(column=0, row=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.data_analysis_frame = DataAnalysisFrame(main)
        self.data_analysis_frame.grid(column=0, row=0, padx=5, pady=5, sticky="ew")

        self.trading_frame = TradingFrame(main)
        self.trading_frame.grid(column=0, row=1, padx=5, pady=5, sticky="ew")

        self.integrations_frame = IntegrationsFrame(main)
        self.integrations_frame.grid(column=0, row=2, padx=5, pady=5, sticky="ew")

        self.report_label = ttk.Label(main, text="")
        self.report_label.grid(column=0, row=3, sticky="ew")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotApp(root)
    root.mainloop()
