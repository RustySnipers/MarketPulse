import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import Calendar
from datetime import datetime
import json
import os

EVENTS_FILE = "calendar_events.json"


class ToolTip:
    def __init__(self, widget, text=""):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 1
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw,
            text=self.text,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1,
            font=("tahoma", "8", "normal"),
        )
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class CalendarApp(tk.Frame):
    TYPE_COLORS = {
        "earnings": "lightblue",
        "dividend": "lightgreen",
        "economic": "lightyellow",
        "custom": "lightpink",
    }
    SEVERITY_SYMBOLS = {"low": "\u2022", "medium": "\u26a0", "high": "\u203c"}

    def __init__(self, master, events=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.events = events or []
        self.filtered_events = self.events
        self.descriptions = {}
        self.create_widgets()
        self.load_events()

    def create_widgets(self):
        left = tk.Frame(self)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right = tk.Frame(self, width=200)
        right.pack(side=tk.RIGHT, fill=tk.Y)

        self.cal = Calendar(left, selectmode="day", date_pattern="yyyy-mm-dd")
        self.cal.pack(fill=tk.BOTH, expand=True)
        self.cal.bind("<<CalendarSelected>>", self.show_day_events)
        self.cal.bind("<<CalendarEvent>>", self.show_event_details)

        self.day_event_box = tk.Listbox(left)
        self.day_event_box.pack(fill=tk.BOTH, expand=True)
        self.day_event_box.bind("<<ListboxSelect>>", self.on_event_select)
        self.day_event_box.bind("<Motion>", self.update_tooltip)
        self.day_event_tooltip = ToolTip(self.day_event_box, "")

        # Filter Section
        filter_frame = tk.LabelFrame(right, text="Filters")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        self.type_vars = {}
        for t in self.TYPE_COLORS:
            var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(
                filter_frame,
                text=t.capitalize(),
                variable=var,
                command=self.apply_filters,
            )
            cb.pack(anchor="w")
            self.type_vars[t] = var
        tk.Label(filter_frame, text="Company:").pack(anchor="w")
        self.company_var = tk.StringVar()
        self.company_box = ttk.Combobox(
            filter_frame, textvariable=self.company_var, state="readonly"
        )
        self.company_box.pack(fill=tk.X)
        self.company_box.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())

        # Key Section
        key_frame = tk.LabelFrame(right, text="Key")
        key_frame.pack(fill=tk.X, padx=5, pady=5)
        for t, color in self.TYPE_COLORS.items():
            f = tk.Frame(key_frame)
            f.pack(fill=tk.X, anchor="w")
            tk.Label(f, width=2, background=color).pack(side=tk.LEFT, padx=2, pady=1)
            tk.Label(f, text=t.capitalize()).pack(side=tk.LEFT)
        for sev, sym in self.SEVERITY_SYMBOLS.items():
            tk.Label(key_frame, text=f"{sym} = {sev.capitalize()} impact").pack(
                anchor="w"
            )

        ttk.Button(right, text="Add Event", command=self.add_event).pack(fill=tk.X, padx=5, pady=5)

    def load_events(self):
        self.cal.calevent_remove("all")
        companies = sorted(set(ev["company"] for ev in self.events))
        self.company_box["values"] = ["All"] + companies
        self.company_box.set("All")
        self.apply_filters()

    def apply_filters(self):
        selected_company = self.company_var.get()
        self.filtered_events = [
            ev
            for ev in self.events
            if self.type_vars[ev["type"]].get()
            and (selected_company == "All" or ev["company"] == selected_company)
        ]
        self.refresh_calendar()

    def refresh_calendar(self):
        self.cal.calevent_remove("all")
        self.day_event_box.delete(0, tk.END)
        self.descriptions.clear()
        for ev in self.filtered_events:
            date = ev["date"]
            severity_symbol = self.SEVERITY_SYMBOLS.get(ev["severity"], "")
            title = f"{severity_symbol} {ev['title']}".strip()
            self.cal.calevent_create(date, title, tags=ev["type"])
            self.cal.tag_config(
                ev["type"], background=self.TYPE_COLORS.get(ev["type"], "white")
            )
            self.cal.tag_bind(ev["type"], "<Button-1>", self.show_event_details)
            item = f"{date} - {title}"
            self.day_event_box.insert(tk.END, item)
            index = self.day_event_box.size() - 1
            self.day_event_box.itemconfig(
                index, {"bg": self.TYPE_COLORS.get(ev["type"], "white")}
            )
            self.descriptions[index] = ev.get("description", "")

    def show_day_events(self, event=None):
        date = self.cal.get_date()
        self.day_event_box.delete(0, tk.END)
        for ev in self.filtered_events:
            if ev["date"] == date:
                severity_symbol = self.SEVERITY_SYMBOLS.get(ev["severity"], "")
                title = f"{severity_symbol} {ev['title']}".strip()
                self.day_event_box.insert(tk.END, title)
                self.day_event_box.itemconfig(
                    tk.END, {"bg": self.TYPE_COLORS.get(ev["type"], "white")}
                )

    def on_event_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            date = self.cal.get_date()
            selected_title = event.widget.get(index)
            for ev in self.filtered_events:
                severity_symbol = self.SEVERITY_SYMBOLS.get(ev["severity"], "")
                title = f"{severity_symbol} {ev['title']}".strip()
                if ev["date"] == date and title == selected_title:
                    self.show_event_popup(ev)
                    break

    def update_tooltip(self, event):
        index = self.day_event_box.nearest(event.y)
        self.day_event_tooltip.text = self.descriptions.get(index, "")

    def show_event_details(self, event):
        if isinstance(event, tk.Event):
            widget = event.widget
            ids = widget.get_calevents(widget.identify_day(event.x, event.y))
            if not ids:
                return
            ev_id = ids[0]
            cal_event = self.cal.calevents[ev_id]
            title = cal_event["text"]
            for ev in self.filtered_events:
                severity_symbol = self.SEVERITY_SYMBOLS.get(ev["severity"], "")
                if f"{severity_symbol} {ev['title']}".strip() == title:
                    self.show_event_popup(ev)
                    break
        else:
            self.show_event_popup(event)

    def show_event_popup(self, ev):
        detail = f"{ev['date']}\n{ev['company']} - {ev['type'].capitalize()}\n{ev.get('description', '')}"
        messagebox.showinfo(ev["title"], detail)

    def add_event(self):
        date = simpledialog.askstring("Add Event", "Date (YYYY-MM-DD):")
        title = simpledialog.askstring("Add Event", "Title:")
        company = simpledialog.askstring("Add Event", "Company:")
        if not date or not title:
            return
        new_ev = {
            "date": date,
            "company": company or "",
            "title": title,
            "type": "custom",
            "severity": "low",
            "description": "",
        }
        self.events.append(new_ev)
        save_events(self.events)
        self.apply_filters()


def load_events():
    if os.path.exists(EVENTS_FILE):
        try:
            with open(EVENTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_events(events):
    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Market Events Calendar")
    events = load_events()
    app = CalendarApp(root, events)
    root.mainloop()
