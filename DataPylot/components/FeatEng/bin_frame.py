import tkinter as tk
from tkinter import ttk

from pandas.api.types import is_numeric_dtype

from components.Patterns.sequential_frames import SequentialFrameManager
from components.FeatEng.bin_nbins_frame import NBinsFrame
from components.FeatEng.bin_range_frame import BinRangeFrame
from components.FeatEng.bin_custom_frame import BinCustomFrame

class BinFrame(SequentialFrameManager):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_frame(BinFeatureFrame, manager=self)

        self.show_frame(0)

        self.next_btn.config(state="disabled")

    def next_frame(self):
        if self.current_index != 0:
            if self.current_index < len(self.frames) - 1:
                self.show_frame(self.current_index + 1)
        else:
            if len(self.frames) > 1:
                self.frames = self.frames[:1]

            tech = self.params["technique"]
            if tech in ("distance", "frequency"):
                self.add_frame(NBinsFrame, manager=self)
            elif tech == "range":
                self.add_frame(BinRangeFrame, manager=self)
            elif tech == "custom":
                self.add_frame(BinCustomFrame, manager=self)

            self.show_frame(1)

class BinFeatureFrame(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager

        self.df_name = None
        self.feat = None
        self.tech = None

        self.df_names = self.winfo_toplevel().SessionData.getDFNames()

        top_label = ttk.Label(
            self, text="Select DataFrame, Feature, and Binning Method",
            font=("Arial", 14)
        )
        top_label.grid(row=0, column=0, padx=5, pady=(20, 5), sticky="n")

        # Select DataFrame
        select_df_text = ttk.Label(self, text="Select DataFrame:", font=("Arial", 12))
        select_df_text.grid(row=1, column=0, padx=5, pady=(20, 5), sticky="w")

        self.df_dropdown = ttk.Combobox(
            self, state="readonly", values=self.df_names, width=30
        )
        self.df_dropdown.grid(row=1, column=0, padx=(250, 5), pady=(20, 5), sticky="w")
        self.df_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_df_selected())

        # Select Feature
        select_feat_text = ttk.Label(self, text="Select Feature:", font=("Arial", 12))
        select_feat_text.grid(row=2, column=0, padx=5, pady=(15, 5), sticky="w")

        self.feat_dropdown = ttk.Combobox(self, state="disabled", width=30)
        self.feat_dropdown.grid(row=2, column=0, padx=(250, 5), pady=(15, 5), sticky="w")
        self.feat_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_feat_selected())

        # Select Technique
        select_tech_text = ttk.Label(self, text="Select Binning Technique:", font=("Arial", 12))
        select_tech_text.grid(row=3, column=0, padx=5, pady=(70, 5), sticky="w")

        self.tech_var = tk.StringVar(value="")
        self.distance_radio = ttk.Radiobutton(
            self, text="Bin by Equal Distance", variable=self.tech_var, value="distance",
            state="disabled", command=self.on_tech_selected
        )
        self.distance_radio.grid(row=3, column=0, padx=(225, 5), pady=(15,5), sticky="w")

        self.frequency_radio = ttk.Radiobutton(
            self, text="Bin by Equal Frequency", variable=self.tech_var, value="frequency",
            state="disabled", command=self.on_tech_selected
        )
        self.frequency_radio.grid(row=3, column=0, padx=(375,5), pady=(15,5), sticky="w")

        self.range_radio = ttk.Radiobutton(
            self, text="Bin By Custom Range", variable=self.tech_var, value="range",
            state="disabled", command=self.on_tech_selected
        )
        self.range_radio.grid(row=4, column=0, padx=(225, 5), pady=(15,5), sticky="w")

        self.custom_radio = ttk.Radiobutton(
            self, text="Bin By Distance", variable=self.tech_var, value="custom",
            state="disabled", command=self.on_tech_selected
        )
        self.custom_radio.grid(row=4, column=0, padx=(375, 5), pady=(15,5), sticky="w")

        self.grid_columnconfigure(0, weight=1)

    def on_df_selected(self):
        self.df_name = self.df_dropdown.get()
        df = self.winfo_toplevel().SessionData.getDataFrame(self.df_name)

        if df is not None:
            features = [feature for feature in df.columns if is_numeric_dtype(df[feature])]
            self.feat_dropdown.config(state="readonly", values=features)

        self.feat_dropdown.set("")
        self.tech_var.set("")

        self.distance_radio.config(state="disabled")
        self.frequency_radio.config(state="disabled")
        self.range_radio.config(state="disabled")
        self.custom_radio.config(state="disabled")

        self.manager.next_btn.config(state="disabled")

    def on_feat_selected(self):
        self.feat = self.feat_dropdown.get()
        if self.feat:
            self.distance_radio.config(state="normal")
            self.frequency_radio.config(state="normal")
            self.range_radio.config(state="normal")
            self.custom_radio.config(state="normal")

        self.tech_var.set("")
        self.manager.next_btn.config(state="disabled")

    def on_tech_selected(self):
        self.tech = self.tech_var.get()

        if self.df_name and self.feat and self.tech:
            self.manager.params["df"] = self.df_name
            self.manager.params["feature"] = self.feat
            self.manager.params["technique"] = self.tech

            self.manager.next_btn.config(state="normal") 