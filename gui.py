import tkinter as tk
from tkinter import messagebox
import threading
from backtesting import run_backtest
from ml_training import run_ml_training
from trading import start_trading_bot, stop_trading_bot
from calendar_app import CalendarApp, load_example_events
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

        # Calendar Section
        self.calendar_button = tk.Button(self.root, text="Open Calendar", command=self.open_calendar)
        self.calendar_button.pack()
        
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

    def open_calendar(self):
        top = tk.Toplevel(self.root)
        top.title("Market Calendar")
        events = load_example_events()
        CalendarApp(top, events)

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotApp(root)
    root.mainloop()
