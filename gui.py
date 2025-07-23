import tkinter as tk
from tkinter import ttk
from settings import load_settings
from watchlist import load_watchlist
from gui_data_analysis import DataAnalysisFrame
from gui_trading import TradingFrame
from gui_integrations import IntegrationsFrame
from gui_performance import PerformanceFrame
from gui_strategy import StrategyFrame

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

        notebook = ttk.Notebook(main)
        notebook.pack(expand=True, fill="both")

        self.data_analysis_frame = DataAnalysisFrame(notebook)
        notebook.add(self.data_analysis_frame, text="Data & Analysis")

        self.trading_frame = TradingFrame(notebook)
        notebook.add(self.trading_frame, text="Trading")

        self.integrations_frame = IntegrationsFrame(notebook)
        notebook.add(self.integrations_frame, text="Integrations")

        self.performance_frame = PerformanceFrame(notebook)
        notebook.add(self.performance_frame, text="Performance")

        self.strategy_frame = StrategyFrame(notebook)
        notebook.add(self.strategy_frame, text="Strategy")

        self.report_label = ttk.Label(main, text="")
        self.report_label.pack(side="bottom", fill="x")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotApp(root)
    root.mainloop()
