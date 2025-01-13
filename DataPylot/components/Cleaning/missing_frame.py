import tkinter as tk
from tkinter import ttk
from pathlib import Path
import re
import sys
import pandas as pd
from pandas.api.types import is_numeric_dtype

from components.Patterns.generate_frame import GenerateCodeFrame
from components.Patterns.popup_dialog import PopupDialog
from CodeGenerators.Cleaning.gen_exe_miss import MissingValueExecutor


class MissingFrame(GenerateCodeFrame):
    def __init__(self, parent):
        super().__init__(parent)

        if hasattr(sys, '_MEIPASS'):
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(__file__).resolve().parent.parent.parent
        
        about_path = base_dir / "edu" / "Cleaning" / "about_miss.txt"

        self.winfo_toplevel().SessionData.setAboutStep(str(about_path))

        self.df_names = self.winfo_toplevel().SessionData.getDFNames()

        top_label = ttk.Label(
            self.content_frame,
            text="Select DataFrame and Customize Operation",
            font=("Arial",14)
        )
        top_label.grid(row=0, column=0, padx=5,pady=(20,5),sticky="n")

        remove_col_label = ttk.Label(
            self.content_frame,
            text="To remove a column with msising values, navigate to the 'Remove Column' Section.",
            font=("Arial", 8)
        )
        remove_col_label.grid(row=1, column=0, padx=5, pady=(15,5), sticky="n")

        select_df_text = ttk.Label(
            self.content_frame,
            text="Select DataFrame:",
            font=("Arial", 12)
        )
        select_df_text.grid(row=2, column=0, padx=5, pady=(25,5), sticky="w")

        self.df_dropdown = ttk.Combobox(
            self.content_frame,
            state="readonly",
            values=self.df_names,
            width=30
        )
        self.df_dropdown.grid(row=2, column=0, padx=(250,5), pady=(25,5), sticky="w")
        self.df_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_df_selected())

        select_op_text = ttk.Label(
            self.content_frame,
            text="Select Operation on Missing Values:",
            font=("Arial", 10)
        )
        select_op_text.grid(row=3, column=0, padx=5, pady=(25,5), sticky="w")

        self.op_var = tk.StringVar(value="")
        self.rem_radio = ttk.Radiobutton(
            self.content_frame,
            text="Remove Instances",
            variable=self.op_var,
            value="remove",
            command=self.on_op_selected
            )
        self.rem_radio.grid(row=3, column=0, padx=(225,5), pady=(25,5), sticky="w")

        self.imp_radio = ttk.Radiobutton(
            self.content_frame,
            text="Impute Values",
            variable=self.op_var,
            value="impute",
            command=self.on_op_selected
            )
        self.imp_radio.grid(row=3, column=0, padx=(350,5), pady=(25,5), sticky="w")

        self.select_operation_text = None
        self.type_var = tk.StringVar(value="")
        self.entire_radio = None
        self.feat_radio = None

        self.feat_text = None
        self.feat_dropdown = None

        self.tech_var = tk.StringVar(value="")
        self.numeric_text = None
        self.mode_radio = None
        self.mean_radio = None
        self.median_radio = None

        self.save_label = None
        self.save_var = tk.StringVar(value="")
        self.current_radio = None
        self.new_radio = None
        self.name_entry = None

        self.err_label = ttk.Label(
            self.content_frame,
            text="",
            font=("Arial", 8)
        )
        self.err_label.grid(row=8, column=0, padx=5, pady=(20,5), sticky="s")

        self.generate_btn.config(state="disabled")
        self.content_frame.grid_columnconfigure(0, weight=1)

    def on_df_selected(self):
        self.df = self.winfo_toplevel().SessionData.getDataFrame(self.df_dropdown.get())

    def on_op_selected(self):
        if self.select_operation_text:
            self.select_operation_text.destroy()
        if self.entire_radio:
            self.entire_radio.destroy()
        if self.feat_radio:
            self.feat_radio.destroy()
        self.type_var.set("")

        if self.feat_text:
            self.feat_text.destroy()
        if self.feat_dropdown:
            self.feat_dropdown.destroy()

        if self.numeric_text:
            self.numeric_text.destroy()
        if self.mode_radio:
            self.mode_radio.destroy()
        if self.mean_radio:
            self.mean_radio.destroy()
        if self.median_radio:
            self.median_radio.destroy()

        if self.save_label:
            self.save_label.destroy()
        if self.current_radio:
            self.current_radio.destroy()
        if self.new_radio:
            self.new_radio.destroy()
        if self.name_entry:
            self.name_entry.destroy()
        self.save_var.set("")

        self.generate_btn.config(state="disabled")


        if self.op_var.get() == 'remove':
            self.select_operation_text = ttk.Label(
                self.content_frame,
                text="Select How to Apply Operation:",
                font=("Arial", 10)
            )
            self.select_operation_text.grid(row=4, column=0, padx=5, pady=(25,5), sticky="w")

            self.entire_radio = ttk.Radiobutton(
                self.content_frame,
                text="All Features",
                variable=self.type_var,
                value="entire",
                command=self.on_type_selected
                )
            self.entire_radio.grid(row=4, column=0, padx=(225,5), pady=(25,5), sticky="w")

            self.feat_radio = ttk.Radiobutton(
                self.content_frame,
                text="Single Feature",
                variable=self.type_var,
                value="single",
                command=self.on_type_selected
                )
            self.feat_radio.grid(row=4, column=0, padx=(350,5), pady=(25,5), sticky="w")
        
        elif self.op_var.get() == 'impute':
            self.type_var.set(value='single')
            self.on_type_selected()

    def on_type_selected(self):
        if self.feat_text:
            self.feat_text.destroy()
        if self.feat_dropdown:
            self.feat_dropdown.destroy()

        if self.numeric_text:
            self.numeric_text.destroy()
        if self.mode_radio:
            self.mode_radio.destroy()
        if self.mean_radio:
            self.mean_radio.destroy()
        if self.median_radio:
            self.median_radio.destroy()

        if self.save_label:
            self.save_label.destroy()
        if self.current_radio:
            self.current_radio.destroy()
        if self.new_radio:
            self.new_radio.destroy()
        if self.name_entry:
            self.name_entry.destroy()
        self.save_var.set("")

        self.generate_btn.config(state="disabled")

        if self.df_dropdown.get() and self.op_var.get() and self.type_var.get():
            if self.type_var.get() == 'single':
                self.feat_text = ttk.Label(
                    self.content_frame,
                    text="Select Feature:",
                    font=("Arial", 12)
                    )
                self.feat_text.grid(row=5, column=0, padx=5, pady=(30,5), sticky="w")

                features = self.df.columns[self.df.isnull().any()].tolist()

                self.feat_dropdown = ttk.Combobox(
                    self.content_frame,
                    state="readonly",
                    values=features,
                    width=30
                    )
                self.feat_dropdown.grid(row=5, column=0, padx=(150,5), pady=(30,5), sticky="w")
                self.feat_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_feat_selected())
                
            
            if self.type_var.get() == 'entire':
                self.save_label = ttk.Label(self.content_frame, text="Select how to save changes:", font=("Arial", 10))
                self.save_label.grid(row=4, column=0, padx=5, pady=(20, 5), sticky="w")

                self.current_radio = ttk.Radiobutton(
                    self.content_frame,
                    text="Current DataFrame",
                    variable=self.save_var,
                    value="current",
                    command=self.on_name_selected
                )
                self.current_radio.grid(row=5, column=0, padx=(225, 5), pady=(20,5), sticky="w")
                self.new_radio = ttk.Radiobutton(
                    self.content_frame,
                    text="New DataFrame",
                    variable=self.save_var,
                    value="new",
                    command=self.on_name_selected
                )
                self.new_radio.grid(row=5, column=0, padx=(350, 5), pady=(20,5), sticky="w")

                self.name_entry = ttk.Entry(self.content_frame, state="disabled", width=30)
                self.name_entry.grid(row=5, column=0, padx=(470, 5), pady=(20,5), sticky="w")
                

    def on_feat_selected(self):
        if self.save_label:
            self.save_label.destroy()
        if self.current_radio:
            self.current_radio.destroy()
        if self.new_radio:
            self.new_radio.destroy()
        if self.name_entry:
            self.name_entry.destroy()
        self.save_var.set("")

        feature = self.feat_dropdown.get()
        self.generate_btn.config(state="disabled")

        if self.df_dropdown.get() and self.op_var.get() and self.type_var.get() and feature:
            if is_numeric_dtype(self.df[feature]) and self.op_var.get() == 'impute':
                self.tech_var.set("")

                self.numeric_text = ttk.Label(
                    self.content_frame,
                    text="Select Technique:",
                    font=("Arial", 10)
                    )
                self.numeric_text.grid(row=6, column=0, padx=5, pady=(25,5), sticky="w")

                self.mean_radio = ttk.Radiobutton(
                    self.content_frame,
                    text="Mean",
                    variable=self.tech_var,
                    value="mean",
                    command=self.on_tech_selected
                    )
                self.mean_radio.grid(row=6, column=0, padx=(150,5), pady=(25,5), sticky="w")

                self.mode_radio = ttk.Radiobutton(
                    self.content_frame,
                    text="Mode",
                    variable=self.tech_var,
                    value="mode",
                    command=self.on_tech_selected
                    )
                self.mode_radio.grid(row=6, column=0, padx=(225,5), pady=(25,5), sticky="w")

                self.median_radio = ttk.Radiobutton(
                    self.content_frame,
                    text="Median",
                    variable=self.tech_var,
                    value="median",
                    command=self.on_tech_selected
                    )
                self.median_radio.grid(row=6, column=0, padx=(300,5), pady=(25,5), sticky="w")
            else:
                self.tech_var.set("mode")
                if self.numeric_text:
                    self.numeric_text.destroy()
                if self.mode_radio:
                    self.mode_radio.destroy()
                if self.mean_radio:
                    self.mean_radio.destroy()
                if self.median_radio:
                    self.median_radio.destroy()

                self.save_label = ttk.Label(self.content_frame, text="Select how to save changes:", font=("Arial", 10))
                self.save_label.grid(row=6, column=0, padx=5, pady=(20, 5), sticky="w")

                self.current_radio = ttk.Radiobutton(
                    self.content_frame,
                    text="Current DataFrame",
                    variable=self.save_var,
                    value="current",
                    command=self.on_name_selected
                )
                self.current_radio.grid(row=6, column=0, padx=(225, 5), pady=(20,5), sticky="w")
                self.new_radio = ttk.Radiobutton(
                    self.content_frame,
                    text="New DataFrame",
                    variable=self.save_var,
                    value="new",
                    command=self.on_name_selected
                )
                self.new_radio.grid(row=6, column=0, padx=(350, 5), pady=(20,5), sticky="w")

                self.name_entry = ttk.Entry(self.content_frame, state="disabled", width=30)
                self.name_entry.grid(row=6, column=0, padx=(470, 5), pady=(20,5), sticky="w")


    def on_tech_selected(self):
        self.generate_btn.config(state="disabled")

        if self.df_dropdown.get() and self.op_var.get() and self.type_var.get() and self.feat_dropdown.get() and self.tech_var.get():
            self.save_label = ttk.Label(self.content_frame, text="Select how to save changes:", font=("Arial", 10))
            self.save_label.grid(row=7, column=0, padx=5, pady=(20, 5), sticky="w")

            self.current_radio = ttk.Radiobutton(
                self.content_frame,
                text="Current DataFrame",
                variable=self.save_var,
                value="current",
                command=self.on_name_selected
            )
            self.current_radio.grid(row=7, column=0, padx=(225, 5), pady=(20,5), sticky="w")
            self.new_radio = ttk.Radiobutton(
                self.content_frame,
                text="New DataFrame:",
                variable=self.save_var,
                value="new",
                command=self.on_name_selected
            )
            self.new_radio.grid(row=7, column=0, padx=(350, 5), pady=(20,5), sticky="w")

            self.name_entry = ttk.Entry(self.content_frame, state="disabled", width=30)
            self.name_entry.grid(row=7, column=0, padx=(470, 5), pady=(20,5), sticky="w")            
        else:
            self.generate_btn.config(state="disabled")

    def on_name_selected(self):
        if self.save_var.get() == 'current':
            self.name_entry.config(state="disabled")
            self.generate_btn.config(state="normal")
        if self.save_var.get() == 'new':
            self.name_entry.config(state="normal")
            self.generate_btn.config(state="normal")

    def validate_name(self, name):
        return re.match(r"^[A-Za-z]\w*$", name) is not None

    def generate_code(self):
        if self.save_var.get() == 'new':
            new_name = self.name_entry.get().strip()
            if not self.validate_name(new_name):
                self.err_label.config(text="Error: Invalid dataset name. Please use only letters, numbers, and underscores. The name must start with a letter.", foreground="red")
                return
                    
            existing_names = self.winfo_toplevel().SessionData.getDFNames()

            if new_name in set(existing_names):
                self.open_overwrite_popup(new_name)
                return
        else:
            new_name = None
        
        self.finalize_code_generation(new_name)

    def open_overwrite_popup(self, name):
        PopupDialog(
            self,
            title="Duplicate DataFrame Name",
            message=f"A DataFrame named '{name}' already exists.\nDo you want to overwrite it?",
            on_right=lambda: self.finalize_code_generation(name),
            on_left=lambda: self.err_label.config(text="Action cancelled.", foreground="red"),
            rightButton="Yes",
            leftButton="No"
        )

    def finalize_code_generation(self, new_name):
         df_name = self.df_dropdown.get()
         if self.type_var.get() == 'entire':
             feature = None
         else:
             feature = self.feat_dropdown.get()
         operation = self.op_var.get()
         if operation == 'impute':
             operation = self.tech_var.get()
         

         code, imports = MissingValueExecutor.generate(
             df=df_name,
             feature=feature,
             operation=operation,
             new_name=new_name,
             session=self.winfo_toplevel().SessionData,
             withImport=self.include_import_var.get()
         )

         if code:
            self.winfo_toplevel().SessionData.addOutput(code)
         if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

         self.reset_inputs()


    def reset_inputs(self):
        if self.select_operation_text:
            self.select_operation_text.destroy()
        if self.entire_radio:
            self.entire_radio.destroy()
        if self.feat_radio:
            self.feat_radio.destroy()

        if self.feat_text:
            self.feat_text.destroy()
        if self.feat_dropdown:
            self.feat_dropdown.destroy()

        if self.numeric_text:
            self.numeric_text.destroy()
        if self.mode_radio:
            self.mode_radio.destroy()
        if self.mean_radio:
            self.mean_radio.destroy()
        if self.median_radio:
            self.median_radio.destroy()

        if self.save_label:
            self.save_label.destroy()
        if self.current_radio:
            self.current_radio.destroy()
        if self.new_radio:
            self.new_radio.destroy()
        if self.name_entry:
            self.name_entry.destroy()
        
        self.err_label.config(text="")

        self.save_var.set("")
        self.op_var.set("")
        self.type_var.set("")
        self.tech_var.set("")

        self.df_dropdown.config(values=self.winfo_toplevel().SessionData.getDFNames())

        self.generate_btn.config(state="disabled")
