import tkinter as tk
from pathlib import Path
import sys

from components import SideTabs, MainStage, CodeWindow, FeatureTabs
from session.session_data import SessionData

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DataPylot")

        if hasattr(sys, '_MEIPASS'):
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(__file__).resolve().parent
        try:
            self.iconbitmap(str(base_dir/"pylot.ico"))
        except Exception as e:
            print(f".ico file failure")

        self.geometry("850x800")

        self.main_pane = tk.PanedWindow(
            self, 
            orient="vertical", 
            sashrelief="flat", 
            sashwidth=5,
            bg="white"
        )
        self.main_pane.pack(fill="both", expand=True)

        self.top_pane = tk.PanedWindow(
            self.main_pane, 
            orient="horizontal",
            sashrelief="flat",
            sashwidth=5,
            bg="white"
        )

        self.bottom_pane = tk.PanedWindow(
            self.main_pane, 
            orient="horizontal", 
            sashrelief="flat", 
            sashwidth=5, 
            bg="white"
        )

        self.side_tabs = SideTabs(self.top_pane)
        self.main_stage = MainStage(self.top_pane)

        self.feature_tabs = FeatureTabs(self.bottom_pane)
        self.code_window = CodeWindow(self.bottom_pane)

        self.top_pane.add(self.side_tabs, minsize=150)
        self.top_pane.add(self.main_stage, minsize=400)

        self.bottom_pane.add(self.feature_tabs, minsize=150)
        self.bottom_pane.add(self.code_window, minsize=400)

        self.main_pane.add(self.top_pane, minsize=489)
        self.main_pane.add(self.bottom_pane, minsize=150)

        self.SessionData = SessionData(self)


def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
