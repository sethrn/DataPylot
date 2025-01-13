import tkinter as tk
from tkinter import CURRENT, ttk

import pandas as pd
from pandas.api.types import is_numeric_dtype, is_object_dtype

from components.Patterns.generate_frame import GenerateCodeFrame
from CodeGenerators.EDA.gen_multi import MultivariatePlotGenerator

class MultiPlotFrame(GenerateCodeFrame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager
        self.df_name = self.manager.params.get("df")
        self.plot_type = self.manager.params.get('type')

        self.current_df = self.winfo_toplevel().SessionData.getDataFrame(self.df_name)

        if not isinstance(self.current_df, pd.DataFrame):
            return
       
        top_label = ttk.Label(
            self.content_frame,
            text=f"Customize {self.plot_type} for DataFrame {self.df_name}", 
            font=("Arial", 12)
        )
        top_label.grid(row=0, column=0, padx=5, pady=5, sticky="n")

        if self.plot_type in ['Heatmap']:
            self.generate_btn.config(state="enabled")
            current_row=1
        else:
            self.generate_btn.config(state="disabled")

            xvals = []
            yvals = []
            hues = list(self.current_df.columns)
       
            if self.plot_type in ['Violin Plot', 'Swarm Plot']:
                xvals = list(self.current_df.columns)
                yvals = [col for col in self.current_df.columns if is_numeric_dtype(self.current_df[col])]
            elif self.plot_type in ['Scatter Plot', 'Line Plot']:
                xvals = [col for col in self.current_df.columns if is_numeric_dtype(self.current_df[col])]
                yvals = [col for col in self.current_df.columns if is_numeric_dtype(self.current_df[col])]

            if self.plot_type != 'Pair Plot':
                xaxis_col_label = ttk.Label(
                    self.content_frame, 
                    text="Select X Axis Feature:",
                    font=("Arial", 10)
                )
                xaxis_col_label.grid(row=1, column=0, padx=5, pady=(25,5), sticky="w")

                self.xaxis_col_entry = ttk.Combobox(
                    self.content_frame,
                    state="readonly",
                    values=xvals,
                    width=30
                )
                self.xaxis_col_entry.grid(row=1, column=0, padx=(250,5), pady=(25,5), sticky="w")
                self.xaxis_col_entry.bind("<<ComboboxSelected>>", lambda e: self.validate_inputs())


                yaxis_col_label = ttk.Label(
                    self.content_frame,
                    text="Select Y Axis Feature:",
                    font=("Arial", 10)
                )
                yaxis_col_label.grid(row=2, column=0, padx=5, pady=(25,5), sticky="w")

                self.yaxis_col_entry = ttk.Combobox(
                    self.content_frame,
                    state="readonly",
                    values=yvals,
                    width=30
                )
                self.yaxis_col_entry.grid(row=2, column=0, padx=(250,5), pady=(25,5), sticky="w")
                self.yaxis_col_entry.bind("<<ComboboxSelected>>", lambda e: self.validate_inputs())
                
                current_row = 4
            else:
                current_row = 2

            hue_label = ttk.Label(
                self.content_frame,
                text="Select Hue:",
                font=("Arial", 10)
            )
            hue_label.grid(row=current_row-1, column=0, padx=5, pady=(25,5), sticky="w")

            self.hue_entry = ttk.Combobox(
                self.content_frame,
                state="readonly",
                values=hues,
                width=30
            )
            self.hue_entry.grid(row=current_row-1, column=0, padx=(250,5), pady=(25,5), sticky="w")
            self.hue_entry.bind("<<ComboboxSelected>>", lambda e: self.validate_inputs())


        self.title_var = tk.StringVar()
        title_label = ttk.Label(
            self.content_frame, 
            text="Set Plot Title",
            font=("Arial", 10)
        )
        title_label.grid(row=current_row, column=0, padx=5, pady=(25,5), sticky="w")

        self.title_entry = ttk.Entry(
            self.content_frame,
            textvariable=self.title_var,
            width=30
        )
        self.title_entry.grid(row=current_row, column=0, padx=(250,5), pady=(25,5), sticky="w")

        xaxis_label = ttk.Label(
            self.content_frame, 
            text="Set X Axis Tick Rotation", 
            font=("Arial", 10)
        )
        xaxis_label.grid(row=current_row+1, column=0, padx=5, pady=(25,5), sticky="w")

        self.xaxis_value = tk.StringVar(value="0")
        self.xaxis_entry = ttk.Entry(
            self.content_frame,
            textvariable=self.xaxis_value,
            width=5
        )
        self.xaxis_entry.grid(row=current_row+1, column=0, padx=(250,5), pady=(25,5), sticky="w")

        self.xaxis_err = ttk.Label(
            self.content_frame,
            text="",
            font=("Arial", 10)
        )
        self.xaxis_err.grid(row=current_row+2, column=0, padx=(300,5), pady=(25,5), sticky="w")

        color_label = ttk.Label(
            self.content_frame,
            text="Select Color Pallette:",
            font=("Arial", 10)
        )
        color_label.grid(row=current_row+2, column=0, padx=5, pady=(25,5), sticky="w")

        colors = ["tab10", "viridis", "cividis", "pastel", "RdBu"]

        self.color_entry = ttk.Combobox(
            self.content_frame,
            state="readonly",
            values=colors,
            width=30
        )
        self.color_entry.grid(row=current_row+2, column=0, padx=(250,5), pady=(25,5), sticky="w")
        self.content_frame.grid_columnconfigure(0, weight=1)

    def validate_inputs(self):
        if self.plot_type not in ['Heatmap', 'Pair Plot']:
            x_selected = self.xaxis_col_entry.get().strip()
            y_selected = self.yaxis_col_entry.get().strip()
        else:
            x_selected = True
            y_selected = True
        if self.plot_type != 'Heatmap':
            hue_selected = self.hue_entry.get().strip()
        else:
            hue_selected = True

        if x_selected and y_selected and hue_selected:
            self.generate_btn.config(state="normal")
        else:
            self.generate_btn.config(state="disabled")

    def validate_rotation(self, rotation):
        try:
            rotation = int(rotation)
            return rotation >= 0
        except ValueError:
            return False

    def generate_code(self):
        if self.plot_type not in ['Heatmap', 'Pair Plot']:
            x = self.xaxis_col_entry.get().strip()
            y = self.yaxis_col_entry.get().strip()
        else: 
            x = ""
            y = ""

        if self.plot_type != 'Heatmap':
            hue = self.hue_entry.get().strip()
        else:
            hue = ""

        title = self.title_var.get().strip()
        rotation = self.xaxis_value.get().strip()
        color = self.color_entry.get().strip()

        if not self.validate_rotation(rotation):
            self.xaxis_err.config(
                text="Invalid rotation value",
                foreground="red"
            )
            return
        else:
            self.xaxis_err.config(text="")

        rotation = int(rotation)

        code, imports = MultivariatePlotGenerator.generate(
            df=self.df_name,
            plot=self.plot_type,
            x=x,
            y=y,
            hue=hue,
            title=title,
            rotation=rotation,
            color=color,
            withImport=self.include_import_var.get()
        )

        if code:
                self.winfo_toplevel().SessionData.addOutput(code)
        if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

        self.reset_inputs()

    def reset_inputs(self):
        self.title_var.set("")
        self.xaxis_value.set("0")
        self.color_entry.set("")
        if self.plot_type not in ['Heatmap', 'Pair Plot']:
            self.xaxis_col_entry.set("")
            self.yaxis_col_entry.set("")
            self.hue_entry.set("")
            self.validate_inputs()
