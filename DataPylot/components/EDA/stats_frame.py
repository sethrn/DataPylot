import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys

from CodeGenerators.EDA.gen_stats import StatsGenerator
from components.Patterns.generate_frame import GenerateCodeFrame

class StatsFrame(GenerateCodeFrame):
    def __init__(self, parent):
        super().__init__(parent)

        if hasattr(sys, '_MEIPASS'):
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(__file__).resolve().parent.parent.parent
        
        about_path = base_dir / "edu" / "EDA" / "about_stats.txt"

        self.winfo_toplevel().SessionData.setAboutStep(str(about_path))
        
        self.df_names = self.winfo_toplevel().SessionData.getDFNames()

        top_label = ttk.Label(self.content_frame, text="Generate Summary Statistics", font=("Arial", 14))
        top_label.grid(row=0, column=0, columnspan=2, padx=5, pady=(20, 5), sticky="n")

        select_text = ttk.Label(
            self.content_frame,
            text="Select DataFrame:",
            font=("Arial", 12)
        )
        select_text.grid(row=1, column=0, padx=5, pady=(70,20), sticky="w")

        self.df_dropdown = ttk.Combobox(
            self.content_frame,
            state="readonly",
            values=self.df_names,
            width=30
        )
        self.df_dropdown.grid(row=1, column=0, padx=(250,5), pady=(70,20), sticky="w")
        self.df_dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_selected)

        self.shape_var = tk.BooleanVar(value=False)
        self.info_var = tk.BooleanVar(value=False)
        self.summary_var = tk.BooleanVar(value=False)
        self.vc_var = tk.BooleanVar(value=False)

        checkbox_texts = [
            ("Print Shape", self.shape_var),
            ("Print Feature Information", self.info_var),
            ("Print Summary Information", self.summary_var),
            ("Print Value Counts", self.vc_var)
        ]

        self.cb_refs = []

        for i, (text, var) in enumerate(checkbox_texts):
            checkbox = ttk.Checkbutton(
                self.content_frame,
                text=text,
                variable=var,
                state="disabled",
                command=self.update_generate_btn
            )
            self.cb_refs.append((checkbox, var))
            checkbox.grid(row=i+2, column=0, sticky="w", padx=(250,5), pady=5)

        self.content_frame.grid_columnconfigure(0, weight=1)  

        self.reset_inputs()

    def on_dropdown_selected(self, event):
        if self.df_dropdown.get():
            for checkbox, _ in self.cb_refs:
                checkbox.config(state="normal")
        self.update_generate_btn()

    def update_generate_btn(self):
        if any(var.get() for _, var in self.cb_refs):
            self.generate_btn.config(state="normal")
        else:
            self.generate_btn.config(state="disabled")

    def generate_code(self):
        df_name = self.df_dropdown.get()

        with_import = self.include_import_var.get()
        code, imports = StatsGenerator.generate(
            df_name,
            self.shape_var.get(), 
            self.info_var.get(),
            self.summary_var.get(), 
            self.info_var.get(), 
            with_import
        )

        if code:
            self.winfo_toplevel().SessionData.addOutput(code)
        if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

        self.reset_inputs()

    def reset_inputs(self):
        for _, var in self.cb_refs:
            var.set(False)
        if len(self.df_names) > 0:
            self.df_dropdown.current(0)
            for checkbox, _ in self.cb_refs:
                checkbox.config(state="normal")

        self.generate_btn.config(state="disabled")
