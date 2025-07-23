import tkinter as tk
from tkinter import ttk

class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title=None, message=None):
        super().__init__(parent)
        self.transient(parent)
        if title:
            self.title(title)

        self.message = message
        self.result = None

        body = ttk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry(f"+{parent.winfo_rootx()+50}+{parent.winfo_rooty()+50}")
        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        # create dialog body. return widget that should have initial focus
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the standard buttons
        pass

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        return 1 # override

    def apply(self):
        pass # override

class AskStringDialog(CustomDialog):
    def body(self, master):
        ttk.Label(master, text=self.message).grid(row=0)
        self.entry = ttk.Entry(master)
        self.entry.grid(row=1)
        return self.entry

    def buttonbox(self):
        box = ttk.Frame(self)
        w = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def apply(self):
        self.result = self.entry.get()

class AskYesNoDialog(CustomDialog):
    def body(self, master):
        ttk.Label(master, text=self.message).pack()

    def buttonbox(self):
        box = ttk.Frame(self)
        w = ttk.Button(box, text="Yes", width=10, command=self.yes)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = ttk.Button(box, text="No", width=10, command=self.no)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.yes)
        self.bind("<Escape>", self.no)
        box.pack()

    def yes(self, event=None):
        self.result = True
        self.ok()

    def no(self, event=None):
        self.result = False
        self.ok()

class MessageDialog(CustomDialog):
    def body(self, master):
        ttk.Label(master, text=self.message).pack()

    def buttonbox(self):
        box = ttk.Frame(self)
        w = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.ok)
        box.pack()

def askstring(parent, title, message):
    return AskStringDialog(parent, title, message).result

def askyesno(parent, title, message):
    return AskYesNoDialog(parent, title, message).result

def showinfo(parent, title, message):
    MessageDialog(parent, title, message)

def showerror(parent, title, message):
    MessageDialog(parent, title, message)
