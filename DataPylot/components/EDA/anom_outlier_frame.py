import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys
from wsgiref import validate

from components.Patterns.generate_frame import GenerateCodeFrame
from CodeGenerators.EDA.gen_anom import OutlierGenerator

class OutlierFrame(GenerateCodeFrame):
    def __init__(self, parent):
        super().__init__(parent)

        if hasattr(sys, '_MEIPASS'):
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(__file__).resolve().parent.parent.parent
        
        about_path = base_dir / "edu" / "EDA" / "about_outlier.txt"

        self.winfo_toplevel().SessionData.setAboutStep(str(about_path))

        self.df_names = self.winfo_toplevel().SessionData.getDFNames()

        top_label = ttk.Label(
            self.content_frame, 
            text="Select DataFrame, Technique, and Parameter",
            font=("Arial", 14)
        )
        top_label.grid(row=0, column=0, padx=5, pady=(20,5), sticky="n")

        select_df_text = ttk.Label(
            self.content_frame,
            text="Select DataFrame:",
            font=("Arial", 12)
        )
        select_df_text.grid(row=1, column=0, padx=5, pady=(70,5), sticky="w")

        self.df_dropdown = ttk.Combobox(
            self.content_frame,
            state="readonly",
            values=self.df_names,
            width=30
        )
        self.df_dropdown.grid(row=1, column=0, padx=(250,5), pady=(70,5), sticky="w")
        self.df_dropdown.bind("<<ComboboxSelected>>", lambda e: self.validate_inputs())

        select_data_text = ttk.Label(
            self.content_frame,
            text="Select Data Type to Analyze:",
            font=("Arial", 10)
        )
        select_data_text.grid(row=2, column=0, padx=5, pady=(50,5), sticky="w")

        self.data_type_var = tk.StringVar(value="")
        self.numeric_radio = ttk.Radiobutton(
            self.content_frame,
            text="Numerical",
            variable=self.data_type_var,
            value="numerical",
            command=self.on_data_type_selected
        )
        self.numeric_radio.grid(row=2, column=0, padx=(225, 5), pady=(50,5), sticky="w")

        self.categorical_radio = ttk.Radiobutton(
            self.content_frame,
            text="Categorical",
            variable=self.data_type_var,
            value="categorical",
            command=self.on_data_type_selected
        )
        self.categorical_radio.grid(row=2, column=0, padx=(350, 5), pady=(50,5), sticky="w")

        

        self.tech_text = None
        self.tukey_radio = None
        self.zscore_radio = None

        self.parameter_label = None
        self.parameter_entry = None

        self.generate_btn.config(state="disabled")
        self.content_frame.grid_columnconfigure(0, weight=1)

    def on_data_type_selected(self):
        if self.parameter_label:
            self.parameter_label.destroy()
        if self.parameter_entry:
            self.parameter_entry.destroy()

        if self.data_type_var.get() == "numerical":
            self.tech_text = ttk.Label(
            self.content_frame,
                text="Select Technique:",
                font=("Arial", 10)
            )
            self.tech_text.grid(row=3, column=0, padx=5, pady=(50,5), sticky="w")

            self.technique_var = tk.StringVar(value="")
            self.tukey_radio = ttk.Radiobutton(
                self.content_frame, text="Tukey's Fence", variable=self.technique_var, value="Tukey",
                command=self.on_technique_selected
            )
            self.tukey_radio.grid(row=3, column=0, padx=(200, 5), pady=(50,5), sticky="w")
        
            self.zscore_radio = ttk.Radiobutton(
                self.content_frame, text="Z-Score Method", variable=self.technique_var, value="ZScore",
                command=self.on_technique_selected
            )
            self.zscore_radio.grid(row=3, column=0, padx=(325, 5), pady=(50,5), sticky="w")
       
        elif self.data_type_var.get() == "categorical":
            if self.tech_text:
               self.tech_text.destroy()
            if self.tukey_radio:
                self.tukey_radio.destroy()
            if self.zscore_radio:
                self.zscore_radio.destroy()

            self.parameter_label = ttk.Label(
                self.content_frame,
                text="Set Proportional Threshold:",
                font=("Arial", 10)    
            )
            self.parameter_label.grid(row=3, column=0, padx=5, pady=(50,5), sticky="w")

            self.parameter_entry = ttk.Entry(
                self.content_frame,
                width=10
            )
            self.parameter_entry.insert(0, "0.01")
            self.parameter_entry.grid(row=3, padx=(200, 5), pady=(50,5), sticky="w")

            self.param_err = ttk.Label(
                self.content_frame,
                text="",
                font=("Arial", 10)
            )
            self.param_err.grid(row=3, column=0, padx=(250,5), pady=(50,5), sticky="w")

            self.validate_inputs()
            
    def on_technique_selected(self):
        if self.parameter_label:
            self.parameter_label.destroy()
        if self.parameter_entry:
            self.parameter_entry.destroy()

        if self.technique_var.get() == "Tukey":
            self.parameter_label = ttk.Label(
                self.content_frame, 
                text="Enter Tukey Fence Multiplier:", 
                font=("Arial", 10)
            )
            default_param = "1.5"
        elif self.technique_var.get() == "ZScore":
            self.parameter_label = ttk.Label(
                self.content_frame, 
                text="Enter Z-Score Threshold:", 
                font=("Arial", 10)
            )
            default_param = "3.0"

        self.parameter_label.grid(row=4, column=0, padx=5, pady=(50,5), sticky="w")

        self.parameter_entry = ttk.Entry(
            self.content_frame, 
            width=10
        )
        self.parameter_entry.insert(0, default_param)
        self.parameter_entry.grid(row=4, column=0, padx=(200, 5), pady=(50,5), sticky="w")

        self.param_err = ttk.Label(
            self.content_frame,
            text="",
            font=("Arial", 10)
        )
        self.param_err.grid(row=4, column=0, padx=(250,5), pady=(50,5), sticky="w")

        self.validate_inputs()

    def validate_inputs(self):
        df_selected = self.df_dropdown.get().strip()
        param_valid = self.validate_param(self.parameter_entry.get().strip()) if self.parameter_entry else False
        technique_selected = self.technique_var.get() if self.data_type_var.get() == "numerical" else True

        if df_selected and param_valid and technique_selected:
            self.generate_btn.config(state="normal")
        else:
            self.generate_btn.config(state="disabled")

    def validate_param(self, param):
        try:
            param = float(param)
            if self.data_type_var.get() == "numerical":
                if self.technique_var.get() == "Tukey" and (param <= 0):
                    return False
                if self.technique_var.get() == "ZScore" and (param <= 0):
                    return False
            elif self.data_type_var.get() == "categorical":
                if param <= 0 or param > 1:
                    return False
            return True
        except ValueError:
            return False

    def generate_code(self):
        df_name = self.df_dropdown.get().strip()
        if self.data_type_var.get() == "numerical":
            technique = self.technique_var.get()
        else:
            technique = ""

        param = self.parameter_entry.get().strip()

        if not self.validate_param(param):
            self.param_err.config(
                text="Invalid Parameter value",
                foreground="red"
                )
            return
        else:
            self.param_err.config(text="")

        param = float(param)

        code, imports = OutlierGenerator.generate(
            df=df_name,
            technique=technique,
            param=param,
            withImport=self.include_import_var.get()
        )

        if code:
            self.winfo_toplevel().SessionData.addOutput(code)
        if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

        self.reset_inputs()

    def reset_inputs(self):
        self.df_dropdown.set("")
        self.data_type_var.set("")
        self.technique_var.set("")

        if self.tech_text:
            self.tech_text.destroy()
        if self.tukey_radio:
            self.tukey_radio.destroy()
        if self.zscore_radio:
            self.zscore_radio.destroy()
        if self.parameter_label:
            self.parameter_label.destroy()
        if self.parameter_entry:
            self.parameter_entry.destroy()

        self.generate_btn.config(state="disabled")




        


