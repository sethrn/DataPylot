from tkinter import ttk
from pathlib import Path
import sys

from components.Patterns.generate_frame import GenerateCodeFrame
from CodeGenerators.EDA.gen_anom import MissingValGenerator

class MissingFrame(GenerateCodeFrame):
    def __init__(self, parent):
        super().__init__(parent)

        if hasattr(sys, '_MEIPASS'):
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(__file__).resolve().parent.parent.parent
        
        about_path = base_dir / "edu" / "EDA" / "about_outlier.txt"

        self.winfo_toplevel().SessionData.setAboutStep(str(about_path))

        top_label = ttk.Label(
            self.content_frame, 
            text="Select DataFrame to Analyze Missing Values", 
            font=("Arial", 14)
        )
        top_label.grid(row=0, column=0, padx=5, pady=(20,5), sticky="n")

        self.df_dropdown = ttk.Combobox(
            self.content_frame,
            state="readonly",
            values=self.winfo_toplevel().SessionData.getDFNames(),
            width=30
        )
        self.df_dropdown.grid(row=1, column=0, padx=(250,5), pady=(70,5), sticky="w")
        self.df_dropdown.bind("<<ComboboxSelected>>", lambda e: self.validate_input())

        self.content_frame.grid_columnconfigure(0, weight=1)

    def validate_input(self):
        if self.df_dropdown.get().strip():
            self.generate_btn.config(state="normal")
        else:
            self.generate_btn.config(state="disabled")
    
    def generate_code(self):
        df = self.df_dropdown.get().strip()
        code, imports = MissingValGenerator.generate(
            df=df, 
            withImport=self.include_import_var.get()
        )

        if code:
            self.winfo_toplevel().SessionData.addOutput(code)
        if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

        self.reset_inputs()

    def reset_inputs(self):
        self.df_dropdown.set("")
        self.validate_input()