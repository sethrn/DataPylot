import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys
import pandas as pd

from components.Patterns.sequential_frames import SequentialFrameManager
from components.EDA.uni_plot_frame import UniPlotFrame

class UnivariateFrames(SequentialFrameManager):
    def __init__(self, parent):
        super().__init__(parent)

        self.enable_next_var = tk.IntVar(value=0)

        self.add_frame(UnivariateStep1, manager=self)

        self.show_frame(0)

        self.next_btn.config(state="disabled")

class UnivariateStep1(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager

        if hasattr(sys, '_MEIPASS'):
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(__file__).resolve().parent.parent.parent
        
        about_path = base_dir / "edu" / "EDA" / "about_uni.txt"

        self.winfo_toplevel().SessionData.setAboutStep(str(about_path))
        
        self.df_names = self.winfo_toplevel().SessionData.getDFNames()

        top_label = ttk.Label(self, text="Select DataFrame, Feature, and Plot Type", font=("Arial", 14))
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
        self.df_dropdown.bind("<<ComboboxSelected>>", self.on_df_dropdown_selected)

        select_feat_text = ttk.Label(
            self,
            text="Select Feature:",
            font=("Arial", 12)
        )
        select_feat_text.grid(row=2, column=0, padx=5, pady=(15,15), sticky="w")

        self.feat_dropdown = ttk.Combobox(
            self,
            state="disabled",
            width=30
        )
        self.feat_dropdown.grid(row=2, column=0, padx=(250,5), pady=(15,15), sticky="w")
        self.feat_dropdown.bind("<<ComboboxSelected>>", self.on_feat_dropdown_selected)

        select_plot_text = ttk.Label(
            self,
            text="Select Plot Type:",
            font=("Arial", 12)
        )
        select_plot_text.grid(row=3, column=0, padx=5, pady=(15,15), sticky="w")

        self.plot_dropdown = ttk.Combobox(
            self,
            state="disabled",
            width=30
        )
        self.plot_dropdown.grid(row=3, column=0, padx=(250,5), pady=(15,15), sticky="w")
        self.plot_dropdown.bind("<<ComboboxSelected>>", self.on_plot_dropdown_selected)

        self.grid_columnconfigure(0, weight=1)

    def on_df_dropdown_selected(self, event):
        self.current_df = self.winfo_toplevel().SessionData.getDataFrame(self.df_dropdown.get())

        if isinstance(self.current_df, pd.DataFrame):
            self.feat_dropdown.config(
                state="readonly",
                values=list(self.current_df.columns)
            )

            self.manager.params['df'] = self.df_dropdown.get()
    
    def on_feat_dropdown_selected(self ,event):
        self.feature = self.feat_dropdown.get()
        self.plot_dropdown.config(
            state="readonly",
            values=['Countplot', 'Pie Chart', 'Boxplot', 'Histogram', 'Kernel Density Estimate']
        )

        self.manager.params['feature'] = self.feat_dropdown.get()

    def on_plot_dropdown_selected(self, event):
        selection = self.plot_dropdown.get()
        prev_selection = self.manager.params.get('type')
        if not prev_selection:
            self.manager.params['type'] = selection
            self.manager.add_frame(UniPlotFrame, manager=self.manager)
        elif prev_selection != selection:
            self.manager.params['type'] = selection
            self.manager.delete_frame_by_index(1)
            self.manager.add_frame(UniPlotFrame, manager=self.manager)
        
        self.manager.show_frame(0)