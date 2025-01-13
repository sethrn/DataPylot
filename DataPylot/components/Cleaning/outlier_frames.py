import tkinter as tk
from tkinter import ttk
from pathlib import Path
import re
import sys
import pandas as pd
from pandas.api.types import is_numeric_dtype

from components.Patterns.sequential_frames import SequentialFrameManager
from components.Cleaning.save_out_frame import SaveOutlierFrame

class OutlierFrames(SequentialFrameManager):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_frame(OutlierOperationFrame, manager=self)

        self.show_frame(0)

        self.next_btn.config(state="disabled")

class OutlierOperationFrame(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager

        if hasattr(sys, '_MEIPASS'):
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(__file__).resolve().parent.parent.parent
        
        about_path = base_dir / "edu" / "Cleaning" / "about_outlier.txt"

        self.winfo_toplevel().SessionData.setAboutStep(str(about_path))


        self.df_names = self.winfo_toplevel().SessionData.getDFNames()

        top_label = ttk.Label(self, text="Select DataFrame and Customize Operation", font=("Arial", 14))
        top_label.grid(row=0, column=0, padx=5, pady=(20, 5), sticky="n")

        remove_col_label = ttk.Label(
            self,
            text="To remove a column with msising values, navigate to the 'Remove Column' Section.",
            font=("Arial", 8)
        )
        remove_col_label.grid(row=1, column=0, padx=5, pady=(15,5), sticky="n")

        select_df_text = ttk.Label(
            self,
            text="Select DataFrame:",
            font=("Arial", 12)
        )
        select_df_text.grid(row=2, column=0, padx=5, pady=(25,5), sticky="w")

        self.df_dropdown = ttk.Combobox(
            self,
            state="readonly",
            values=self.df_names,
            width=30
        )

        self.df_dropdown.grid(row=2, column=0, padx=(250,5), pady=(25,5), sticky="w")
        self.df_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_df_selected())


        select_op_text = ttk.Label(
            self,
            text="Select Operation on Outliers:",
            font=("Arial", 10)
        )
        select_op_text.grid(row=3, column=0, padx=5, pady=(25,5), sticky="w")

        self.op_var = tk.StringVar(value="")
        self.rem_radio = ttk.Radiobutton(
            self,
            text="Remove Instances",
            variable=self.op_var,
            value="remove",
            command=self.on_op_selected
            )
        self.rem_radio.grid(row=3, column=0, padx=(225,5), pady=(25,5), sticky="w")

        self.cap_radio = ttk.Radiobutton(
            self,
            text="Winsorization (Cap Values)",
            variable=self.op_var,
            value="cap",
            command=self.on_op_selected
            )
        self.cap_radio.grid(row=3, column=0, padx=(350,5), pady=(25,5), sticky="w")

        self.grid_columnconfigure(0, weight=1)
        # selecting entire dataset or single feature (remove only)
        self.type_text = None
        self.type_var = tk.StringVar(value="")
        self.single_radio = None
        self.entire_radio = None
        # selecting feature (numeric features)
        self.feat_text = None
        self.feat_dropdown = None
        #selecting bound
        self.select_bound_text = None
        self.bound_var = tk.StringVar(value="")
        self.upper_radio = None
        self.lower_radio = None
        self.both_radio = None
        # selectng technique to detect outlier
        self.tech_text = None
        self.tech_var = tk.StringVar(value="")
        self.tukey_radio = None
        self.zscore_radio = None
        self.custom_radio = None
        # select parameter for technique (tukey, zscore, custom)
        self.parameter_text = None
        self.parameter_entry = None
        self.parameter2_entry = None
        self.param_err = None

    def on_df_selected(self):
        self.destroy_type()
        self.destroy_feat()
        self.destroy_bound()
        self.destroy_tech()
        self.destroy_param()

        self.df = self.winfo_toplevel().SessionData.getDataFrame(self.df_dropdown.get())

    def on_op_selected(self):
        self.destroy_type()
        self.destroy_feat()
        self.destroy_bound()
        self.destroy_tech()
        self.destroy_param()

        if self.df_dropdown.get() and self.op_var.get():
            if self.op_var.get() == "remove":
                self.type_text = ttk.Label(
                    self,
                    text="Select How to Apply Operation",
                    font=("Arial", 10)
                )
                self.type_text.grid(row=4, column=0, padx=5, pady=(25,5), sticky="w")

                self.single_radio = ttk.Radiobutton(
                    self,
                    text="Single Feature",
                    variable=self.type_var,
                    value="single",
                    command=self.on_type_selected
                )
                self.single_radio.grid(row=4, column=0, padx=(225,5), pady=(25,5), sticky="w")

                self.entire_radio = ttk.Radiobutton(
                    self,
                    text="Entire Dataset",
                    variable=self.type_var,
                    value="entire",
                    command=self.on_type_selected
                )
                self.entire_radio.grid(row=4, column=0, padx=(350,5), pady=(25,5), sticky="w")
            elif self.op_var.get() == "cap":
                features = [feature for feature in self.df.columns if is_numeric_dtype(self.df[feature])]

                self.feat_text = ttk.Label(
                        self,
                        text="Select Feature",
                        font=("Arial", 10)
                )
                self.feat_text.grid(row=4, column=0, padx=5, pady=(25,5), sticky="w")

                self.feat_dropdown = ttk.Combobox(
                    self,
                    state="readonly",
                    values=features,
                    width=30
                )
                self.feat_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_feat_selected())
                self.feat_dropdown.grid(row=4, column=0, padx=(250,5), pady=(25,5), sticky="w")
   
    def on_type_selected(self):
        self.destroy_feat()
        self.destroy_bound()
        self.destroy_tech()
        self.destroy_param()

        if self.df_dropdown.get() and self.op_var.get() and self.type_var.get():
            if self.type_var.get() == "entire":
                self.select_bound_text = ttk.Label(
                    self,
                    text="Select Bound(s) to Apply Operation:",
                    font=("Arial", 10)
                )
                self.select_bound_text.grid(row=5, column=0, padx=5, pady=(25,5), sticky="w")

                self.upper_radio = ttk.Radiobutton(
                    self,
                    text="Upper Bound",
                    variable=self.bound_var,
                    value="upper",
                    command=lambda: self.on_bound_selected(6)
                )
                self.upper_radio.grid(row=5, column=0, padx=(225,5), pady=(25,5), sticky="w")

                self.lower_radio = ttk.Radiobutton(
                    self,
                    text="Lower Bound",
                    variable=self.bound_var,
                    value="lower",
                    command=lambda: self.on_bound_selected(6)
                )
                self.lower_radio.grid(row=5, column=0, padx=(350,5), pady=(25,5), sticky="w")

                self.both_radio = ttk.Radiobutton(
                    self,
                    text="Both",
                    variable=self.bound_var,
                    value="both",
                    command=lambda: self.on_bound_selected(6)
                )
                self.both_radio.grid(row=5, column=0, padx=(475,5), pady=(25,5), sticky="w")
            
            elif self.type_var.get() == "single":
                features = [feature for feature in self.df.columns if is_numeric_dtype(self.df[feature])]

                self.feat_text = ttk.Label(
                        self,
                        text="Select Feature",
                        font=("Arial", 10)
                )
                self.feat_text.grid(row=5, column=0, padx=5, pady=(25,5), sticky="w")

                self.feat_dropdown = ttk.Combobox(
                    self,
                    state="readonly",
                    values=features,
                    width=30
                )
                self.feat_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_feat_selected())
                self.feat_dropdown.grid(row=5, column=0, padx=(250,5), pady=(25,5), sticky="w")
                
    def on_feat_selected(self):
        self.destroy_bound()
        self.destroy_tech()
        self.destroy_param()

        if self.df_dropdown.get() and self.op_var.get() and self.feat_dropdown.get():
            self.select_bound_text = ttk.Label(
                self,
                text="Select Bound(s) to Apply Operation:",
                font=("Arial", 10)
            )
            self.select_bound_text.grid(row=6, column=0, padx=5, pady=(25,5), sticky="w")

            self.upper_radio = ttk.Radiobutton(
                self,
                text="Upper Bound",
                variable=self.bound_var,
                value="upper",
                command=lambda: self.on_bound_selected(7)
            )
            self.upper_radio.grid(row=6, column=0, padx=(225,5), pady=(25,5), sticky="w")

            self.lower_radio = ttk.Radiobutton(
                self,
                text="Lower Bound",
                variable=self.bound_var,
                value="lower",
                command=lambda: self.on_bound_selected(7)
            )
            self.lower_radio.grid(row=6, column=0, padx=(350,5), pady=(25,5), sticky="w")

            self.both_radio = ttk.Radiobutton(
                self,
                text="Both",
                variable=self.bound_var,
                value="both",
                command=lambda: self.on_bound_selected(7)
            )
            self.both_radio.grid(row=6, column=0, padx=(475,5), pady=(25,5), sticky="w")

    def on_bound_selected(self, row):
        self.destroy_tech()
        self.destroy_param()

        if self.df_dropdown.get() and self.op_var.get() and (self.type_var.get() or self.feat_dropdown.get()):
            self.tech_text = ttk.Label(
                self,
                text="Select Technique to Detect Outliers:",
                font=("Arial", 10)
            )
            self.tech_text.grid(row=row, column=0, padx=5, pady=(25,5), sticky="w")

            self.tukey_radio = ttk.Radiobutton(
                self,
                text="Tukey's Fence",
                variable=self.tech_var,
                value="tukey",
                command=lambda: self.on_tech_selected(row+1)
            )
            self.tukey_radio.grid(row=row, column=0, padx=(225,5), pady=(25,5), sticky="w")

            self.zscore_radio = ttk.Radiobutton(
                self,
                text="Z-Score Method",
                variable=self.tech_var,
                value="zscore",
                command=lambda: self.on_tech_selected(row+1)
            )
            self.zscore_radio.grid(row=row, column=0, padx=(350,5), pady=(25,5), sticky="w")

            if self.type_var.get() != "entire":
                self.custom_radio = ttk.Radiobutton(
                    self,
                    text="Custom Value",
                    variable=self.tech_var,
                    value="custom",
                    command=lambda: self.on_tech_selected(row+1)
                )
                self.custom_radio.grid(row=row, column=0, padx=(475,5), pady=(25,5), sticky="w")

    
    def on_tech_selected(self, row):
        self.destroy_param()

        if self.df_dropdown.get() and self.op_var.get() and (self.type_var.get() or self.feat_dropdown.get()) and self.tech_var.get():
            if self.tech_var.get() == "tukey":
                self.parameter_text= ttk.Label(
                    self, 
                    text="Enter Tukey Fence Multiplier:", 
                    font=("Arial", 10)
                )
                default_param = "1.5"
                xpad_param = 200
                xpad_err = 250

               
            elif self.tech_var.get() == "zscore":
                self.parameter_text = ttk.Label(
                    self, 
                    text="Enter Z-Score Threshold:", 
                    font=("Arial", 10)
                )
                default_param = "3.0"
                xpad_param = 200
                xpad_err = 250
                
            elif self.tech_var.get() == "custom":
                if self.bound_var.get() == "both":
                    self.parameter_text = ttk.Label(
                        self,
                        text="Enter Custom Values:\tLower:\t\t   Upper:",
                        font=("Arial", 10)
                    )
                    self.parameter2_entry = ttk.Entry(self, width=8)
                    self.parameter2_entry.bind("<KeyRelease>", lambda e: self.validate_param())
                    self.parameter2_entry.grid(row=row, column=0, padx=(350, 5), pady=(25,5), sticky="w")
                else:
                    self.parameter_text = ttk.Label(
                    self, 
                    text="Enter Custom Value:",
                    font=("Arial", 10)
                )   
                default_param = ""
                xpad_param = 225
                xpad_err = 425

            self.parameter_text.grid(row=row, column=0, padx=5, pady=(25,5), sticky="w")

            self.parameter_entry = ttk.Entry(
                self, 
                width=8
            )
            self.parameter_entry.insert(0, default_param)
            self.parameter_entry.bind("<KeyRelease>", lambda e: self.validate_param())
            self.parameter_entry.grid(row=row, column=0, padx=(xpad_param, 5), pady=(25,5), sticky="w")

            self.param_err = ttk.Label(
                self,
                text="",
                font=("Arial", 10)
            )
            self.param_err.grid(row=row, column=0, padx=(xpad_err,5), pady=(25,5), sticky="w")

            if self.tech_var.get() != "custom":
                self.capture_state()

                self.manager.delete_frame_by_index(1)
                self.manager.add_frame(SaveOutlierFrame, manager=self.manager)
                self.manager.show_frame(0)
               

    def validate_param(self):
        param = self.parameter_entry.get().strip()
        try:
            param = float(param)
            if self.tech_var.get() == "tukey" and param <= 0:
                self.param_err.config(text="Value must be > 0", foreground="red")
                self.manager.next_btn.config(state="disabled")
                return False
            elif self.tech_var.get() == "zscore" and param <= 0:
                self.param_err.config(text="Value must be > 0", foreground="red")
                self.manager.next_btn.config(state="disabled")
                return False
            elif self.tech_var.get() == "custom" and self.bound_var.get() == "both":
                lower_param = self.parameter_entry.get().strip()
                upper_param = self.parameter2_entry.get().strip()
                if not lower_param or not upper_param or float(lower_param) >= float(upper_param):
                    self.param_err.config(text="Lower bound must be less than upper bound", foreground="red")
                    self.manager.next_btn.config(state="disabled")
                    return False
            self.param_err.config(text="", foreground="black")
            self.capture_state()
            self.manager.delete_frame_by_index(1)
            self.manager.add_frame(SaveOutlierFrame, manager=self.manager)
            self.manager.show_frame(0)
            return True
        except ValueError:
            self.param_err.config(text="Invalid numeric value", foreground="red")
            self.manager.next_btn.config(state="disabled")
            return False

    def capture_state(self):
        self.manager.params['df'] = self.df_dropdown.get()
        self.manager.params['op'] = self.op_var.get()
        self.manager.params['type'] = self.type_var.get() if self.type_var else 'single'
        self.manager.params['feature'] = self.feat_dropdown.get() if self.feat_dropdown else 'all'
        self.manager.params['bound'] = self.bound_var.get()
        self.manager.params['technique'] = self.tech_var.get()
        self.manager.params['param'] = self.parameter_entry.get().strip()
        self.manager.params['param2'] = (
            self.parameter2_entry.get().strip() if self.parameter2_entry and self.bound_var.get() == "both" else None
        )

    def reset_inputs(self):
        self.destroy_type()
        self.destroy_feat()
        self.destroy_bound()
        self.destroy_tech()
        self.destroy_param()

        self.df = None

    def destroy_type(self):
        if self.type_text:
            self.type_text.destroy()
        if self.single_radio:
            self.single_radio.destroy()
        if self.entire_radio:
            self.entire_radio.destroy()
        self.type_var.set("")

    def destroy_feat(self):
        if self.feat_text:
            self.feat_text.destroy()
        if self.feat_dropdown:
            self.feat_dropdown.destroy()

    def destroy_bound(self):
        if self.select_bound_text:
            self.select_bound_text.destroy()
        if self.upper_radio:
            self.upper_radio.destroy()
        if self.lower_radio:
            self.lower_radio.destroy()
        if self.both_radio:
            self.both_radio.destroy()
        self.bound_var.set("")
       
    def destroy_tech(self):
        if self.tech_text:
            self.tech_text.destroy()
        if self.tukey_radio:
            self.tukey_radio.destroy()
        if self.zscore_radio:
            self.zscore_radio.destroy()
        if self.custom_radio:
            self.custom_radio.destroy()
        self.tech_var.set("")

    def destroy_param(self):
        if self.parameter_text:
            self.parameter_text.destroy()
            self.parameter_text = None
        if self.parameter_entry:
            self.parameter_entry.destroy()
            self.parameter_entry = None
        if self.parameter2_entry:
            self.parameter2_entry.destroy()
            self.parameter2_entry = None
        if self.param_err:
            self.param_err.destroy()
            self.param_err = None
