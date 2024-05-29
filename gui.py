import tkinter as tk
from tkinter import messagebox
import threading
from backtesting import run_backtest
from ml_training import run_ml_training
from trading import start_trading_bot, stop_trading_bot
import time

class TradingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Bot")
        self.create_widgets()
        self.data = None
        self.trading_active = False

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
            self
