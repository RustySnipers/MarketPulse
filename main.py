import tkinter as tk
from gui import TradingBotApp

print("Starting application...")

if __name__ == "__main__":
    print("Creating root window...")
    root = tk.Tk()
    print("Initializing TradingBotApp...")
    app = TradingBotApp(root)
    print("Running main loop...")
    root.mainloop()
    print("Application finished.")


