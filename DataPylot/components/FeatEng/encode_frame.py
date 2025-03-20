import tkinter as tk
from tkinter import ttk
from components.Patterns.sequential_frames import SequentialFrameManager
from components.FeatEng.encode_custom_frame import EncodeCustomFrame
from components.FeatEng.encode_lib_frame import EncodeLibFrame

class EncodingFrames(SequentialFrameManager):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_frame(EncodeFeatureFrame, manager=self)

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
            if tech == "custom":
                self.add_frame(EncodeCustomFrame, manager=self)
            elif tech in ("ordinal", "onehot", "binary"):
                self.add_frame(EncodeLibFrame, manager=self)

            self.show_frame(self.current_index+1)
    
class EncodeFeatureFrame(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)
        self.manager = manager
        self.df_name = None
        self.feat = None
        self.tech = None

        self.df_names = self.winfo_toplevel().SessionData.getDFNames()

        top_label = ttk.Label(
            self, text="Select DataFrame, Feature, and Encoding Method",
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
        select_tech_text = ttk.Label(self, text="Select Encoding Technique:", font=("Arial", 12))
        select_tech_text.grid(row=3, column=0, padx=5, pady=(70, 5), sticky="w")

        self.tech_var = tk.StringVar(value="")
        self.ordinal_radio = ttk.Radiobutton(
            self, text="Ordinal", variable=self.tech_var, value="ordinal",
            state="disabled", command=self.on_tech_selected
        )
        self.ordinal_radio.grid(row=3, column=0, padx=(225, 5), pady=(15, 5), sticky="w")

        self.onehot_radio = ttk.Radiobutton(
            self, text="One-Hot", variable=self.tech_var, value="onehot",
            state="disabled", command=self.on_tech_selected
        )
        self.onehot_radio.grid(row=3, column=0, padx=(325, 5), pady=(15, 5), sticky="w")

        self.binary_radio = ttk.Radiobutton(
            self, text="Binary", variable=self.tech_var, value="binary",
            state="disabled", command=self.on_tech_selected
        )
        self.binary_radio.grid(row=3, column=0, padx=(425, 5), pady=(15, 5), sticky="w")

        self.custom_radio = ttk.Radiobutton(
            self, text="Custom Encoding", variable=self.tech_var, value="custom",
            state="disabled", command=self.on_tech_selected
        )
        self.custom_radio.grid(row=4, column=0, padx=(225, 5), pady=(5, 5), sticky="w")

        self.grid_columnconfigure(0, weight=1)

    def on_df_selected(self):
        self.df_name = self.df_dropdown.get()
        df = self.winfo_toplevel().SessionData.getDataFrame(self.df_name)

        if df is not None:
            self.feat_dropdown.config(state="readonly", values=list(df.columns))

        self.feat_dropdown.set("")
        self.tech_var.set("")

        self.ordinal_radio.config(state="disabled")
        self.onehot_radio.config(state="disabled")
        self.binary_radio.config(state="disabled")
        self.custom_radio.config(state="disabled")

        self.manager.next_btn.config(state="disabled")

    def on_feat_selected(self):
        self.feat = self.feat_dropdown.get()
        if self.feat:
            self.ordinal_radio.config(state="normal")
            self.onehot_radio.config(state="normal")
            self.binary_radio.config(state="normal")
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
