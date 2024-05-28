import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import pandas as pd
from backtesting import run_backtest
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
        # Upload Data Section
        self.upload_label = tk.Label(self.root, text="Upload Data for Backtesting:")
        self.upload_label.pack()
        self.upload_button = tk.Button(self.root, text="Upload CSV", command=self.upload_data)
        self.upload_button.pack()
        
        # Backtesting Section
        self.backtest_button = tk.Button(self.root, text="Perform Backtesting", command=self.perform_backtest)
        self.backtest_button.pack()
        self.progress_label = tk.Label(self.root, text="")
        self.progress_label.pack()
        
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
    
    def upload_data(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.data = pd.read_csv(file_path, parse_dates=True, index_col='date')
            messagebox.showinfo("Success", "Data uploaded successfully")
        else:
            messagebox.showerror("Error", "Failed to upload data")

    def perform_backtest(self):
        if self.data is None:
            messagebox.showerror("Error", "Please upload data first")
            return

        def backtest():
            self.progress_label.config(text="Backtesting in progress...")
            run_backtest()
            self.progress_label.config(text="Backtesting completed. Report generated in reports/backtesting_report.txt")
            self.report_label.config(text="Backtesting completed. Report generated in reports/backtesting_report.txt")
        
        threading.Thread(target=backtest).start()

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

