import tkinter as tk
from tkinter import ttk
import pandas as pd

class PerformanceFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Performance")
        self.parent = parent
        self.create_widgets()
        self.load_performance_data()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("Metric", "Value"), show="headings")
        self.tree.heading("Metric", text="Metric")
        self.tree.heading("Value", text="Value")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_performance_data(self):
        # This is a placeholder. In a real application, you would load
        # the trading history from a file or database.
        data = {
            "Metric": ["Total Trades", "Winning Trades", "Losing Trades", "Win Rate", "Average Gain", "Average Loss"],
            "Value": [0, 0, 0, "0%", "$0.00", "$0.00"]
        }
        df = pd.DataFrame(data)

        for i in self.tree.get_children():
            self.tree.delete(i)

        for index, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))
