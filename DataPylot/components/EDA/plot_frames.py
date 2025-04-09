import tkinter as tk
from tkinter import ttk
import pandas as pd

from components.EDA.dynamic_plot_frame import DynamicPlotFrame
from components.Patterns.sequential_frames import SequentialFrameManager
from config.plotting_config import BIVARIATE_CONFIG, MULTIVARIATE_CONFIG, UNIVARIATE_CONFIG

class PlotFrames(SequentialFrameManager):
    def __init__(self, parent):
        super().__init__(parent)

        self.enable_next_var = tk.IntVar(value=0)

        self.add_frame(PlotTypeFrame, manager=self)

        self.show_frame(0)

        self.next_btn.config(state="disabled")

    def next_frame(self):
        if self.current_index == 0:
            if len(self.frames) > 1:
                self.frames = self.frames[:1]
        
            self.add_frame(DynamicPlotFrame, manager=self)
            self.show_frame(1)
        else:
            if self.current_index < len(self.frames) - 1:
                self.show_frame(self.current_index + 1)

class PlotTypeFrame(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager
        self.manager.params["class"] = "uni"
        self.df_names = self.winfo_toplevel().SessionData.getDFNames()
        
        top_label = ttk.Label(self, text="Generate a Visualization", font=("Arial", 14))
        top_label.grid(row=0, column=0, columnspan=2, padx=5, pady=(20, 5), sticky="n")

        select_df_text = ttk.Label(
            self,
            text="Select DataFrame:",
            font=("Arial", 12)
        )
        select_df_text.grid(row=1, column=0, padx=5, pady=(70,15), sticky="w")

        self.df_dropdown = ttk.Combobox(
            self,
            state="readonly",
            values=self.df_names,
            width=30
        )

        self.df_dropdown.grid(row=1, column=0, padx=(250,5), pady=(70,15), sticky="w")
        self.df_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_df_dropdown_selected())

        select_analysis_text = ttk.Label(
            self,
            text="Select Analysis Type:",
            font=("Arial", 12),
        )
        select_analysis_text.grid(row=2, column=0, padx=5, pady=(15,15), sticky="w")

        self.analysis_dropdown = ttk.Combobox(
            self,
            state="disabled",
            width=30
        )
        self.analysis_dropdown.grid(row=2, column=0, padx=(250,5), pady=(15,15), sticky="w")
        self.analysis_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_analysis_dropdown_selected())

        select_plot_text = ttk.Label(
            self,
            text="Select Plot Type:",
            font=("Arial", 12),
        )
        select_plot_text.grid(row=3, column=0, padx=5, pady=(15,15), sticky="w")

        self.plot_dropdown = ttk.Combobox(
            self,
            state="disabled",
            width=30
        )
        self.plot_dropdown.grid(row=3, column=0, padx=(250,5), pady=(15,15), sticky="w")
        self.plot_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_plot_dropdown_selected())

        self.grid_columnconfigure(0, weight=1)

    def on_df_dropdown_selected(self):
        self.analysis_dropdown.set("")
        self.plot_dropdown.set("")
        self.plot_dropdown.config(state="disabled")
        self.current_df = self.winfo_toplevel().SessionData.getDataFrame(self.df_dropdown.get())

        if isinstance(self.current_df, pd.DataFrame):
            self.analysis_dropdown.config(
                state="readonly",
                values=["Univariate Visualization", "Bivariate Visualization", "Multivariate Visualization"])

            self.manager.params['df_name'] = self.df_dropdown.get()

    def on_analysis_dropdown_selected(self):
        self.plot_dropdown.set("")
        self.analysis = self.analysis_dropdown.get()
        if self.current_df is not None and self.analysis:
            if self.analysis == "Univariate Visualization":
                self.manager.params["class"] = "uni"
                self.config = UNIVARIATE_CONFIG
            elif self.analysis == "Bivariate Visualization":
                self.manager.params["class"] = "bi"
                self.config = BIVARIATE_CONFIG
            elif self.analysis == "Multivariate Visualization":
                self.manager.params["class"] = "multi"
                self.config = MULTIVARIATE_CONFIG

            self.plot_dropdown.config(
                    state="readonly",
                    values=list(self.config.keys())
            )

    def on_plot_dropdown_selected(self):
        selection = self.plot_dropdown.get()
        if self.current_df is not None and self.analysis and selection:
            self.manager.params["type"] = selection
            self.manager.next_btn.config(state="normal")