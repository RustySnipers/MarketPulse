import tkinter as tk
from tkinter import ttk
from dialogs import CustomDialog, askstring

class IndicatorsDialog(CustomDialog):
    def __init__(self, parent, tv_session):
        self.tv_session = tv_session
        super().__init__(parent, title="Manage Indicators")

    def body(self, master):
        self.indicator_list = tk.Listbox(master)
        self.indicator_list.pack()
        self.populate_indicator_list()

        button_frame = ttk.Frame(master)
        button_frame.pack()

        add_button = ttk.Button(button_frame, text="Add", command=self.add_indicator)
        add_button.pack(side=tk.LEFT)

        remove_button = ttk.Button(button_frame, text="Remove", command=self.remove_indicator)
        remove_button.pack(side=tk.LEFT)

        configure_button = ttk.Button(button_frame, text="Configure", command=self.configure_indicator)
        configure_button.pack(side=tk.LEFT)

    def populate_indicator_list(self):
        self.indicator_list.delete(0, tk.END)
        indicators = self.tv_session.get_indicators()
        if indicators:
            for indicator in indicators:
                self.indicator_list.insert(tk.END, f"{indicator['name']} ({indicator['id']})")

    def add_indicator(self):
        indicator_name = askstring(self, "Add Indicator", "Enter indicator name (e.g., 'Moving Average'):")
        if indicator_name:
            self.tv_session.add_indicator(indicator_name)
            self.populate_indicator_list()

    def remove_indicator(self):
        selected_indicator = self.indicator_list.get(tk.ACTIVE)
        if selected_indicator:
            entity_id = selected_indicator.split('(')[-1].replace(')', '')
            self.tv_session.remove_indicator(entity_id)
            self.populate_indicator_list()

    def configure_indicator(self):
        selected_indicator = self.indicator_list.get(tk.ACTIVE)
        if selected_indicator:
            entity_id = selected_indicator.split('(')[-1].replace(')', '')
            self.tv_session.window.evaluate_js(f"tvWidget.activeChart().showPropertiesDialog('{entity_id}');")

def open_indicators_dialog(parent, tv_session):
    IndicatorsDialog(parent, tv_session)
