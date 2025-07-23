import tkinter as tk
from tkinter import ttk

class StrategyFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Strategy")
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Select Indicator:").pack()
        self.indicator_var = tk.StringVar()
        self.indicator_combo = ttk.Combobox(self, textvariable=self.indicator_var,
                                              values=["RSI", "MACD", "Bollinger Bands"])
        self.indicator_combo.pack()

        self.settings_frame = ttk.Frame(self)
        self.settings_frame.pack()

        self.indicator_combo.bind("<<ComboboxSelected>>", self.update_settings)

    def update_settings(self, event=None):
        for widget in self.settings_frame.winfo_children():
            widget.destroy()

        indicator = self.indicator_var.get()
        if indicator == "RSI":
            ttk.Label(self.settings_frame, text="Period:").pack()
            ttk.Entry(self.settings_frame).pack()
        elif indicator == "MACD":
            ttk.Label(self.settings_frame, text="Fast Period:").pack()
            ttk.Entry(self.settings_frame).pack()
            ttk.Label(self.settings_frame, text="Slow Period:").pack()
            ttk.Entry(self.settings_frame).pack()
            ttk.Label(self.settings_frame, text="Signal Period:").pack()
            ttk.Entry(self.settings_frame).pack()
        elif indicator == "Bollinger Bands":
            ttk.Label(self.settings_frame, text="Period:").pack()
            ttk.Entry(self.settings_frame).pack()
            ttk.Label(self.settings_frame, text="StdDev:").pack()
            ttk.Entry(self.settings_frame).pack()
