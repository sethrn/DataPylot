import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys
import pandas as pd

from components.Patterns.generate_frame import GenerateCodeFrame
from CodeGenerators.EDA.gen_corr import CorrelationGenerator

class CorrelationFrame(GenerateCodeFrame):
    def __init__(self, parent):
        super().__init__(parent)

        if hasattr(sys, '_MEIPASS'):
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(__file__).resolve().parent.parent.parent
        
        about_path = base_dir / "edu" / "EDA" / "about_corr.txt"

        self.winfo_toplevel().SessionData.setAboutStep(str(about_path))

        self.df_names = self.winfo_toplevel().SessionData.getDFNames()

        top_label = ttk.Label(self.content_frame, text="Select DataFrame and Technique", font=("Arial", 14))
        top_label.grid(row=0, column=0, columnspan=2, padx=5, pady=(20, 5), sticky="n")

        select_df_text = ttk.Label(
            self.content_frame,
            text="Select DataFrame:",
            font=("Arial", 12)
        )
        select_df_text.grid(row=1, column=0, padx=5, pady=(50,5), sticky="w")

        self.df_dropdown = ttk.Combobox(
            self.content_frame,
            state="readonly",
            values=self.df_names,
            width=30
        )

        self.df_dropdown.grid(row=1, column=0, padx=(250,5), pady=(50,5), sticky="w")
        self.df_dropdown.bind("<<ComboboxSelected>>", lambda e: self.validate_input())

        select_tech_text = ttk.Label(
            self.content_frame,
            text="Select Technique:",
            font=("Arial", 12)
        )
        select_tech_text.grid(row=3, column=0, padx=5, pady=(50,5), sticky="w")

        self.tech_dropdown = ttk.Combobox(
            self.content_frame,
            state="readonly",
            values=["Pearson Coefficient", "Spearman Rank", "Kendall Tau"],
            width=30
        )
        self.tech_dropdown.current(0)
        self.tech_dropdown.grid(row=3, column=0, padx=(250,5), pady=(50,5), sticky="w")
        self.tech_dropdown.bind("<<ComboboxSelected>>", lambda e: self.validate_input())

        self.content_frame.grid_columnconfigure(0, weight=1)

    def validate_input(self):
        if self.df_dropdown.get().strip() and self.tech_dropdown.get().strip():
            self.generate_btn.config(state="normal")
        else:
            self.generate_btn.config(state="disabled")

    def generate_code(self):
        df = self.df_dropdown.get().strip()
        technique = self.tech_dropdown.get().strip()

        code, imports = CorrelationGenerator.generate(
            df=df,
            technique=technique,
            withImport=self.include_import_var.get()
        )

        if code:
                self.winfo_toplevel().SessionData.addOutput(code)
        if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

        self.reset_inputs()

        heatmap_label = ttk.Label(
            self.content_frame,
            text="To generate a heatmap, navigate to the multivariate section of the Visualizations tab.",
            font=("Arial", 8)
        )
        heatmap_label.grid(row=4, column=0, padx=(30,5), pady=(15,15), sticky="w")

    def reset_inputs(self):
        self.df_dropdown.set("")
        self.tech_dropdown.current(0)
        self.validate_input()


