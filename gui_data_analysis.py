import tkinter as tk
from tkinter import ttk
import threading
from backtesting import run_backtest
from ml_training import run_ml_training
from trading import self_improve_model
from settings import load_settings
from utils.ml_utils import load_data

class DataAnalysisFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Data & Analysis")
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.backtest_button = ttk.Button(self, text="Perform Backtesting", command=self.perform_backtest)
        self.backtest_button.grid(column=0, row=0, sticky="ew")
        self.ml_training_button = ttk.Button(self, text="Start ML Training", command=self.start_ml_training)
        self.ml_training_button.grid(column=1, row=0, sticky="ew")
        self.improve_model_button = ttk.Button(self, text="Improve Model", command=self.improve_model)
        self.improve_model_button.grid(column=2, row=0, sticky="ew")
        self.columnconfigure((0,1,2), weight=1)
        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.grid(column=0, row=1, columnspan=3, sticky="ew")
        self.progress_label = ttk.Label(self, text="")
        self.progress_label.grid(column=0, row=2, columnspan=3, sticky="ew")

    def perform_backtest(self):
        def backtest():
            self.parent.after(0, self.progress.start)
            self.parent.after(0, lambda: self.progress_label.config(text="Backtesting in progress..."))
            run_backtest()
            self.parent.after(0, self.progress.stop)
            self.parent.after(0, lambda: self.progress_label.config(text="Backtesting completed. Report generated in reports folder"))
            self.parent.after(0, lambda: self.parent.report_label.config(text="Backtesting completed. Report generated in reports folder"))
            self.parent.after(0, lambda: self.backtest_button.config(state="normal"))

        self.backtest_button.config(state="disabled")
        threading.Thread(target=backtest, daemon=True).start()

    def start_ml_training(self):
        def training():
            self.parent.after(0, self.progress.start)
            self.parent.after(0, lambda: self.progress_label.config(text="ML Training in progress..."))
            run_ml_training()
            self.parent.after(0, self.progress.stop)
            self.parent.after(0, lambda: self.progress_label.config(text="ML Training completed. Report generated in reports folder"))
            self.parent.after(0, lambda: self.parent.report_label.config(text="ML Training completed. Report generated in reports folder"))
            self.parent.after(0, lambda: self.ml_training_button.config(state="normal"))

        self.ml_training_button.config(state="disabled")
        threading.Thread(target=training, daemon=True).start()

    def improve_model(self):
        def improve():
            self.parent.after(0, self.progress.start)
            self.parent.after(0, lambda: self.progress_label.config(text="Improving model..."))

            settings = load_settings()
            file_path = settings.get("data_file", "data/SPY2324.csv")
            new_data = load_data(file_path)

            self_improve_model(new_data)

            self.parent.after(0, self.progress.stop)
            self.parent.after(0, lambda: self.progress_label.config(text="Model improvement complete."))
            self.parent.after(0, lambda: self.improve_model_button.config(state="normal"))

        self.improve_model_button.config(state="disabled")
        threading.Thread(target=improve, daemon=True).start()
