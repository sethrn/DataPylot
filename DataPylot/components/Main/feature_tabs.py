from asyncio.windows_events import NULL
import tkinter as tk
from tkinter import ttk

from components.Patterns.popup_dialog import PopupDialog

class FeatureTabs(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = self.winfo_toplevel()

        self.import_stmt = ""
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "FeatureTab.TButton",
            font=("Verdana", 10),
            background="white",
            foreground="black",
            padding=(1,30),
            relief="groove",
            borderwidth=1,
        )
        style.configure(
            "Selected.FeatureTab.TButton",
            font=("Verdana", 10),
            background="darkgray",
            foreground="white",
            padding=(1,30),
            relief="sunken",
            borderwidth=1
        )

        side_buttons = [
            ("About This Step", self.about_step),
            ("View All Imports", self.collect_imports)
        ]
        self.btn_refs = []

        for text, command in side_buttons:
            btn = ttk.Button(
                self,
                text=text,
                style="FeatureTab.TButton",
                command=command
            )
            btn.pack(fill="x")
            self.btn_refs.append(btn)

    def about_step(self):
        self.btn_refs[0].configure(
            style="Selected.FeatureTab.TButton"
        )
        about_filepath = self.app.SessionData.getAboutStep()
        try:
            with open(about_filepath, "r") as file:
                content = file.read()
        except FileNotFoundError:
            content = "Information not available for this step."

        PopupDialog(
            self.app.main_stage,
            title="About This Step",
            message=content,
            on_right=lambda: self.btn_refs[0].configure(style="FeatureTab.TButton"),
            on_left=lambda: self.btn_refs[0].configure(style="FeatureTab.TButton"),
            rightButton="Close",
            leftButton=None,
            modal=False
        )

    def collect_imports(self):
        self.btn_refs[1].configure(
            style="Selected.FeatureTab.TButton"
        )
        self.import_stmt = ""
        imports = self.app.SessionData.getImports()
        for stmt in imports:
            self.import_stmt += stmt + "\n"

        PopupDialog(
            self.app.main_stage,
            title="All Import Statements",
            message=self.import_stmt,
            on_right=lambda: self.copy_imports(),
            on_left=lambda: self.btn_refs[1].configure(style="FeatureTab.TButton"),
            rightButton="Copy",
            leftButton="Close"
        )

    def copy_imports(self):
        self.clipboard_clear()
        self.clipboard_append(self.import_stmt)
