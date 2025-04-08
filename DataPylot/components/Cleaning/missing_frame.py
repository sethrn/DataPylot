import tkinter as tk
from tkinter import ttk
import re
import pandas as pd
from pandas.api.types import is_numeric_dtype

from components.Patterns.generate_frame import GenerateCodeFrame
from components.Patterns.popup_dialog import PopupDialog
from CodeGenerators.Cleaning.gen_exe_miss import MissingValueExecutor

class MissingFrame(GenerateCodeFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.df_names = self.winfo_toplevel().SessionData.getDFNames()

        top_label = ttk.Label(
            self.content_frame,
            text="Select DataFrame and Customize Operation",
            font=("Arial",14)
        )
        top_label.grid(row=0, column=0, padx=5,pady=(20,5),sticky="n")

        remove_col_label = ttk.Label(
            self.content_frame,
            text="To remove a column with missing values, navigate to the 'Remove Column' Section.",
            font=("Arial", 8)
        )
        remove_col_label.grid(row=1, column=0, padx=5, pady=(10,5), sticky="n")

        select_df_text = ttk.Label(
            self.content_frame,
            text="Select DataFrame:",
            font=("Arial", 12)
        )
        select_df_text.grid(row=2, column=0, padx=5, pady=(20,5), sticky="w")

        self.df_dropdown = ttk.Combobox(
            self.content_frame,
            state="readonly",
            values=self.df_names,
            width=30
        )
        self.df_dropdown.grid(row=2, column=0, padx=(250,5), pady=(20,5), sticky="w")
        self.df_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_df_selected())

        select_op_text = ttk.Label(
            self.content_frame,
            text="Select Operation on Missing Values:",
            font=("Arial", 10)
        )
        select_op_text.grid(row=3, column=0, padx=5, pady=(20,5), sticky="w")

        self.op_var = tk.StringVar(value="")
        self.rem_radio = ttk.Radiobutton(
            self.content_frame,
            text="Remove Instances",
            variable=self.op_var,
            value="remove",
            command=self.on_op_selected,
            state="disabled"
            )
        self.rem_radio.grid(row=3, column=0, padx=(350,5), pady=(20,5), sticky="w")

        self.imp_radio = ttk.Radiobutton(
            self.content_frame,
            text="Impute Values",
            variable=self.op_var,
            value="impute",
            command=self.on_op_selected,
            state="disabled"
            )
        self.imp_radio.grid(row=3, column=0, padx=(225,5), pady=(20,5), sticky="w")

        self.select_operation_text = None
        self.type_var = tk.StringVar(value="")
        self.entire_radio = None
        self.feat_radio = None

        self.feat_text = None
        self.feat_dropdown = None

        self.tech_var = tk.StringVar(value="")
        self.save_row=7
        self.tech_text = None
        self.mode_radio = None
        self.mean_radio = None
        self.median_radio = None
        self.dummy_radio = None

        self.save_df_text = None
        self.save_df_var = tk.StringVar(value="")
        self.current_df_radio = None
        self.new_df_radio = None
        self.new_df_entry = None

        self.err_label = ttk.Label(
            self.content_frame,
            text="",
            font=("Arial", 8)
        )
        self.err_label.grid(row=9, column=0, padx=5, pady=(20,5), sticky="s")

        self.generate_btn.config(state="disabled")
        self.content_frame.grid_columnconfigure(0, weight=1)

    def on_df_selected(self):
        self.df = self.winfo_toplevel().SessionData.getDataFrame(self.df_dropdown.get())
        self.rem_radio.config(state="normal")
        self.imp_radio.config(state="normal")

        self.destroy_type()
        self.destroy_feat()
        self.destroy_tech()
        self.destroy_save()
        self.op_var.set("")
        self.generate_btn.config(state="disabled")

    def on_op_selected(self):
        self.destroy_type()
        self.destroy_feat()
        self.destroy_tech()
        self.destroy_save()
        self.generate_btn.config(state="disabled")

        if self.op_var.get() == 'remove':
            self.select_operation_text = ttk.Label(
                self.content_frame,
                text="Select How to Apply Operation:",
                font=("Arial", 10)
            )
            self.select_operation_text.grid(row=4, column=0, padx=5, pady=(20,5), sticky="w")

            self.entire_radio = ttk.Radiobutton(
                self.content_frame,
                text="All Features",
                variable=self.type_var,
                value="entire",
                command=self.on_type_selected
                )
            self.entire_radio.grid(row=4, column=0, padx=(225,5), pady=(20,5), sticky="w")

            self.feat_radio = ttk.Radiobutton(
                self.content_frame,
                text="Single Feature",
                variable=self.type_var,
                value="single",
                command=self.on_type_selected
                )
            self.feat_radio.grid(row=4, column=0, padx=(350,5), pady=(20,5), sticky="w")
        
        elif self.op_var.get() == 'impute':
            self.type_var.set(value='single')
            self.on_type_selected()

    def on_type_selected(self):
        self.destroy_feat()
        self.destroy_tech()
        self.destroy_save()
        self.generate_btn.config(state="disabled")

        if self.df_dropdown.get() and self.op_var.get() and self.type_var.get():
            if self.type_var.get() == 'single':
                self.feat_text = ttk.Label(
                    self.content_frame,
                    text="Select Feature:",
                    font=("Arial", 12)
                    )
                self.feat_text.grid(row=5, column=0, padx=5, pady=(20,5), sticky="w")

                features = self.df.columns[self.df.isnull().any()].tolist()

                self.feat_dropdown = ttk.Combobox(
                    self.content_frame,
                    state="readonly",
                    values=features,
                    width=30
                    )
                self.feat_dropdown.grid(row=5, column=0, padx=(250,5), pady=(20,5), sticky="w")
                self.feat_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_feat_selected())
                
            
            if self.type_var.get() == 'entire':
                self.save_df_text = ttk.Label(self.content_frame, text="Select how to save changes:", font=("Arial", 10))
                self.save_df_text.grid(row=5, column=0, padx=5, pady=(20, 5), sticky="w")

                self.current_df_radio = ttk.Radiobutton(
                    self.content_frame,
                    text="Current DataFrame",
                    variable=self.save_df_var,
                    value="current",
                    command=self.on_save_df_selected
                )
                self.current_df_radio.grid(row=5, column=0, padx=(225, 5), pady=(20,5), sticky="w")
                self.new_df_radio = ttk.Radiobutton(
                    self.content_frame,
                    text="New DataFrame",
                    variable=self.save_df_var,
                    value="new",
                    command=self.on_save_df_selected
                )
                self.new_df_radio.grid(row=5, column=0, padx=(350, 5), pady=(20,5), sticky="w")

                self.new_df_entry= ttk.Entry(self.content_frame, state="disabled", width=20)
                self.new_df_entry.grid(row=5, column=0, padx=(470, 5), pady=(20,5), sticky="w")

    def on_feat_selected(self):
        self.destroy_tech()
        self.destroy_save()
        self.generate_btn.config(state="disabled")

        feature = self.feat_dropdown.get()
        if self.df_dropdown.get() and self.op_var.get() and self.type_var.get() and feature:
            if self.op_var.get() == 'impute':
                if is_numeric_dtype(self.df[feature]):
                    self.tech_var.set("")

                    self.tech_text = ttk.Label(
                        self.content_frame,
                        text="Select Technique (Numeric):",
                        font=("Arial", 10)
                        )
                    self.tech_text.grid(row=6, column=0, padx=5, pady=(20,5), sticky="w")

                    self.mean_radio = ttk.Radiobutton(
                        self.content_frame,
                        text="Mean",
                        variable=self.tech_var,
                        value="mean",
                        command=self.on_tech_selected
                        )
                    self.mean_radio.grid(row=6, column=0, padx=(225,5), pady=(20,5), sticky="w")

                    self.mode_radio = ttk.Radiobutton(
                        self.content_frame,
                        text="Mode",
                        variable=self.tech_var,
                        value="mode",
                        command=self.on_tech_selected
                        )
                    self.mode_radio.grid(row=6, column=0, padx=(300,5), pady=(20,5), sticky="w")

                    self.median_radio = ttk.Radiobutton(
                        self.content_frame,
                        text="Median",
                        variable=self.tech_var,
                        value="median",
                        command=self.on_tech_selected
                        )
                    self.median_radio.grid(row=6, column=0, padx=(375,5), pady=(20,5), sticky="w")
                else:    
                    self.tech_var.set("")

                    self.tech_text = ttk.Label(
                        self.content_frame,
                        text="Select Technique (Categorical):",
                        font=("Arial", 10)
                    )
                    self.tech_text.grid(row=6, column=0, padx=5, pady=(20,5), sticky="w")

                    self.mode_radio = ttk.Radiobutton(
                        self.content_frame,
                        text="Impute with most frequent category (Mode)",
                        variable=self.tech_var,
                        value="mode",
                        command=self.on_tech_selected
                    )
                    self.mode_radio.grid(row=6, column=0, padx=(225,5), pady=(20,5), sticky="w")
                
                    if self.op_var.get() == "impute":
                        self.save_row=8

                        self.dummy_radio = ttk.Radiobutton(
                            self.content_frame,
                            text="Replace column with indicator: 1 = Present, 0 = Missing",
                            variable=self.tech_var,
                            value="dummy",
                            command=self.on_tech_selected
                        )
                        self.dummy_radio.grid(row=7, column=0, padx=(225,5), pady=(20,5), sticky="w")
            else:
                self.save_df_text = ttk.Label(self.content_frame, text="Select how to save changes:", font=("Arial", 10))
                self.save_df_text.grid(row=6, column=0, padx=5, pady=(20, 5), sticky="w")

                self.current_df_radio = ttk.Radiobutton(
                    self.content_frame,
                    text="Current DataFrame",
                    variable=self.save_df_var,
                    value="current",
                    command=self.on_save_df_selected
                )
                self.current_df_radio.grid(row=6, column=0, padx=(225, 5), pady=(20,5), sticky="w")
                self.new_df_radio = ttk.Radiobutton(
                    self.content_frame,
                    text="New DataFrame",
                    variable=self.save_df_var,
                    value="new",
                    command=self.on_save_df_selected
                )
                self.new_df_radio.grid(row=6, column=0, padx=(350, 5), pady=(20,5), sticky="w")

                self.new_df_entry= ttk.Entry(self.content_frame, state="disabled", width=20)
                self.new_df_entry.grid(row=6, column=0, padx=(470, 5), pady=(20,5), sticky="w")
                
    def on_tech_selected(self):
        self.destroy_save()
        self.generate_btn.config(state="disabled")

        if self.df_dropdown.get() and self.op_var.get() and self.type_var.get() and self.feat_dropdown.get() and self.tech_var.get():
            self.save_df_text = ttk.Label(self.content_frame, text="Select how to save changes:", font=("Arial", 10))
            self.save_df_text.grid(row=self.save_row, column=0, padx=5, pady=(20, 5), sticky="w")

            self.current_df_radio = ttk.Radiobutton(
                self.content_frame,
                text="Current DataFrame",
                variable=self.save_df_var,
                value="current",
                command=self.on_save_df_selected
            )
            self.current_df_radio.grid(row=self.save_row, column=0, padx=(225, 5), pady=(20,5), sticky="w")
            self.new_df_radio = ttk.Radiobutton(
                self.content_frame,
                text="New DataFrame",
                variable=self.save_df_var,
                value="new",
                command=self.on_save_df_selected
            )
            self.new_df_radio.grid(row=self.save_row, column=0, padx=(350, 5), pady=(20,5), sticky="w")

            self.new_df_entry= ttk.Entry(self.content_frame, state="disabled", width=20)
            self.new_df_entry.grid(row=self.save_row, column=0, padx=(470, 5), pady=(20,5), sticky="w")       
        else:
            self.generate_btn.config(state="disabled")

    def on_save_df_selected(self):
        if self.save_df_var.get() == "new":
            self.new_df_entry.config(state="normal")
        else:
            self.new_df_entry.config(state="disabled")
        self.generate_btn.config(state="normal")

    def validate_name(self, name):
        return re.match(r"^[A-Za-z]\w*$", name) is not None

    def validate_inputs(self):
        if self.save_df_var.get() == "new":
            name = self.new_df_entry.get().strip()
            if not self.validate_name(name):
                self.err_label.config(text="Invalid DataFrame Name")
                return False
            df_names = self.winfo_toplevel().SessionData.getDFNames()
            if name in set(df_names):
                if not self.open_overwrite_popup("DataFrame", name):
                    return False
        elif self.save_df_var.get() == "current":
            return True
        else:
            return False
        return True

    def open_overwrite_popup(self, item, name):
            self.popup_result = False
            dialog = PopupDialog(
                self,
                title=f"Duplicate {item}",
                message=f"A {item} named '{name}' already exists.\nDo you want to overwrite it?",
                on_right=lambda: self.set_popup_result(True),
                on_left=lambda: self.set_popup_result(False),
                rightButton="Yes",
                leftButton="No"
            )
            self.wait_window(dialog)
            return self.popup_result

    def set_popup_result(self, value):
        self.popup_result = value
        self.focus_set()
 
    def generate_code(self):
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
             new_name=self.new_df_entry.get().strip() if self.save_df_var.get() == "new" else None,
             session=self.winfo_toplevel().SessionData,
             withImport=self.include_import_var.get()
         )

         if code:
            self.winfo_toplevel().SessionData.addOutput(code)
         if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

         self.winfo_toplevel().main_stage.refresh_children()

    def destroy_type(self):
        if self.select_operation_text:
            self.select_operation_text.destroy()
        if self.entire_radio:
            self.entire_radio.destroy()
        if self.feat_radio:
            self.feat_radio.destroy()
        self.type_var.set("")

    def destroy_feat(self):
        if self.feat_text:
            self.feat_text.destroy()
        if self.feat_dropdown:
            self.feat_dropdown.destroy()

    def destroy_tech(self):
        if self.tech_text:
            self.tech_text.destroy()
        if self.mode_radio:
            self.mode_radio.destroy()
        if self.mean_radio:
            self.mean_radio.destroy()
        if self.median_radio:
            self.median_radio.destroy()
        if self.dummy_radio:
            self.dummy_radio.destroy()
        self.tech_var.set("")

    def destroy_save(self):
        if self.save_df_text:
            self.save_df_text.destroy()
        if self.current_df_radio:
            self.current_df_radio.destroy()
        if self.new_df_radio:
            self.new_df_radio.destroy()
        if self.new_df_entry:
            self.new_df_entry.destroy()
        self.save_df_var.set("")