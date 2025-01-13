import tkinter as tk
from tkinter import ttk

class SideTabs(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.selected_tab = None

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "SideTab.TButton",
            font=("Verdana", 10),
            background="white",
            foreground="black",
            padding=(1,30),
            relief="groove",
            borderwidth=1,
        )
        style.configure(
            "Selected.SideTab.TButton",
            font=("Verdana", 10),
            background="darkgray",
            foreground="white",
            padding=(1,30),
            relief="sunken",
            borderwidth=1
        )

        self.tab_texts = [
            "Import Dataset", "EDA", "Data Cleaning", 
            "Feature Engineering", "Model Training", 
            "Model Evaulation"
        ]
        self.tabs = {}

        for tab_txt in self.tab_texts:
            tab = ttk.Button(
                self, 
                text=tab_txt, 
                style="SideTab.TButton",
                command=lambda t=tab_txt: self.select_tab(t)
            )
            tab.pack(fill="x")
            self.tabs[tab_txt] = tab

    def select_tab(self, tab_txt):
        if self.selected_tab:
            self.tabs[self.selected_tab].configure(
                style="SideTab.TButton"    
            )

        self.selected_tab = tab_txt
        self.tabs[self.selected_tab].configure(
            style="Selected.SideTab.TButton"
        )

        self.winfo_toplevel().main_stage.load_frame(tab_txt)