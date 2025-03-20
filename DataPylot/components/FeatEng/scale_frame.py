import re
import tkinter as tk
from tkinter import ttk

import pandas as pd
from pandas.api.types import is_numeric_dtype

from CodeGenerators.FeatEng.gen_exe_scale import ScaleExecutor
from components.Patterns.generate_frame import GenerateCodeFrame
from components.Patterns.sequential_frames import SequentialFrameManager
from components.Patterns.popup_dialog import PopupDialog

class ScaleFrames(SequentialFrameManager):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_frame(ScaleOperationFrame, manager=self)

        self.show_frame(0)

        self.next_btn.config(state="disabled")

class ScaleOperationFrame(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager
        self.df_names = self.winfo_toplevel().SessionData.getDFNames()

        top_label = ttk.Label(
            self,
            text="Select DataFrame and Scaling Method",
            font=("Arial",14)
        )
        top_label.grid(row=0, column=0, padx=5,pady=(20,5),sticky="n")

        select_df_text = ttk.Label(
            self,
            text="Select DataFrame:",
            font=("Arial", 12)
        )
        select_df_text.grid(row=1, column=0, padx=5, pady=(20,5), sticky="w")

        self.df_dropdown = ttk.Combobox(
            self,
            state="readonly",
            values=self.df_names,
            width=30
        )
        self.df_dropdown.grid(row=1, column=0, padx=(250,5), pady=(20,5), sticky="w")
        self.df_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_df_selected())

        select_feat_text = ttk.Label(
            self,
            text="Select Feature:",
            font=("Arial", 12)
        )
        select_feat_text.grid(row=2, column=0, padx=5, pady=(15, 5), sticky="w")

        self.feat_dropdown = ttk.Combobox(
            self,
            state="disabled",
            width=30
        )
        self.feat_dropdown.grid(row=2, column=0, padx=(250,5), pady=(15, 5), sticky="w")
        self.feat_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_feat_selected())

        self.tech_text = ttk.Label(
            self,
            text="Select Technique:",
            font=("Arial", 12)
         )
        self.tech_text.grid(row=3, column=0, padx=5, pady=(15, 5), sticky="w")

        self.tech_var = tk.StringVar(value="")

        self.zscore_radio = ttk.Radiobutton(
            self,
            state="disabled",
            text="Standardization (Z-score)",
            variable=self.tech_var,
            value="stand",
            command=lambda: self.on_tech_selected()
        )
        self.zscore_radio.grid(row=3, column=0, padx=(175,5), pady=(15, 5), sticky="w")

        self.log_radio = ttk.Radiobutton(
            self,
            state="disabled",
            text="Log Transformation",
            variable=self.tech_var,
            value="log",
             command=lambda: self.on_tech_selected()
        )
        self.log_radio.grid(row=3, column=0, padx=(340, 5), pady=(15, 5), sticky="w")

        self.sqrt_radio = ttk.Radiobutton(
            self,
            state="disabled",
            text="Square Root Transformation",
            variable=self.tech_var,
            value="sqrt",
             command=lambda: self.on_tech_selected()
        )
        self.sqrt_radio.grid(row=3, column=0, padx=(475, 5), pady=(15, 5), sticky="w")

        self.out_label = ttk.Label(
            self,
            text="Feature scaling should generally be done after handling outliers to avoid extreme values dominating transformations.",
            font=("Arial", 8)
        )
        self.out_label.grid(row=4, column=0, padx=5, pady=(150, 5), sticky="s")

        self.grid_columnconfigure(0, weight=1)

    def on_df_selected(self):
        self.df = self.winfo_toplevel().SessionData.getDataFrame(self.df_dropdown.get())
        
        if not isinstance(self.df, pd.DataFrame):
            return

        features = [feature for feature in self.df.columns if is_numeric_dtype(self.df[feature])]

        self.feat_dropdown.config(
            state="readonly",
            values=features
        )
        self.feat_dropdown.set("")
        self.tech_var.set("")

        self.zscore_radio.config(state="disabled")
        self.log_radio.config(state="disabled")
        self.sqrt_radio.config(state="disabled")

        self.manager.next_btn.config(state="disabled")

    def on_feat_selected(self):
        if self.df_dropdown.get() and self.feat_dropdown.get():
            self.zscore_radio.config(state="normal")
            self.log_radio.config(state="normal")
            self.sqrt_radio.config(state="normal")

        self.manager.next_btn.config(state="disabled")

    def on_tech_selected(self):
        if self.df_dropdown.get() and self.feat_dropdown.get() and self.tech_var.get():
            self.capture_state()

            if self.manager.frame_count() != 1:
                self.manager.delete_frame_by_index(1)

            self.manager.add_frame(SaveScaleFrame, manager=self.manager)
            self.manager.show_frame(0)

    def capture_state(self):
        self.manager.params['df'] = self.df_dropdown.get()
        self.manager.params['feature'] = self.feat_dropdown.get()
        self.manager.params['technique'] = self.tech_var.get()

    
class SaveScaleFrame(GenerateCodeFrame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager
        self.params = manager.params
        
        top_label = ttk.Label(
            self.content_frame,
            text="Select How to Save Changes",
            font=("Arial", 14)
        )
        top_label.grid(row=0, column=0, padx=5, pady=(20,5), sticky="n")

        save_df_text = ttk.Label(
            self.content_frame,
            text="Save Changes to:",
            font=("Arial", 12)
        )
        save_df_text.grid(row=1, column=0, padx=5, pady=(30,15), sticky="w")

        self.save_df_var = tk.StringVar(value="")

        self.current_df_radio = ttk.Radiobutton(
            self.content_frame,
            text="Current DataFrame",
            variable=self.save_df_var,
            value="current",
            command=self.on_save_df_selected
        )
        self.current_df_radio.grid(row=1, column=0, padx=(150,5), pady=(30,15), sticky="w")

        self.new_df_radio = ttk.Radiobutton(
            self.content_frame,
            text="New DataFrame:",
            variable=self.save_df_var,
            value="new",
            command=self.on_save_df_selected
        )
        self.new_df_radio.grid(row=1, column=0, padx=(275, 5), pady=(30,15), sticky="w")


        self.new_df_entry = ttk.Entry(
            self.content_frame,
            state="disabled",
            width=15
        )
        self.new_df_entry.grid(row=1, column=0, padx=(400, 5), pady=(30,15), sticky="w")

        save_col_text = ttk.Label(
        self.content_frame,
        text="Save Column:",
        font=("Arial", 12)
        )
        save_col_text.grid(row=2, column=0, padx=5, pady=(30,15), sticky="w")

        self.save_col_var = tk.StringVar(value="")
        self.current_col_radio = ttk.Radiobutton(
            self.content_frame,
            text="Current Column",
            variable=self.save_col_var,
            value="current",
            command=self.on_save_col_selected
        )
        self.current_col_radio.grid(row=2, column=0, padx=(150, 5), pady=(30,15), sticky="w")

        self.new_col_radio = ttk.Radiobutton(
            self.content_frame,
            text="New Column:",
            variable=self.save_col_var,
            value="new",
            command=self.on_save_col_selected
        )
        self.new_col_radio.grid(row=2, column=0, padx=(275, 5), pady=(30,15), sticky="w")

        self.new_col_entry = ttk.Entry(
            self.content_frame,
            state="disabled",
            width=15
        )
        self.new_col_entry.grid(row=2, column=0, padx=(400, 5), pady=(30,15), sticky="w")

        self.err_label = ttk.Label(
            self.content_frame,
            text="",
            font=("Arial", 10),
            foreground="red"
        )
        self.err_label.grid(row=3, column=0, columnspan=2, padx=5, pady=(25,5), sticky="n")

        self.content_frame.grid_columnconfigure(0, weight=1)

        self.generate_btn.config(state="disabled")
            
    def on_save_df_selected(self):
        if self.save_df_var.get() == "new":
            self.new_df_entry.config(state="normal")
        else:
            self.new_df_entry.config(state="disabled")

    def on_save_col_selected(self):
        if self.save_col_var.get() == "new":
            self.new_col_entry.config(state="normal")
        else:
            self.new_col_entry.config(state="disabled")
        self.generate_btn.config(state="normal")

    def validate_name(self, name):
        return re.match(r"^[A-Za-z]\w*$", name) is not None

    def validate_inputs(self):
        if self.save_df_var.get() == "new":
            name = self.new_df_entry.get()
            if not self.validate_name(name):
                self.err_label.config(text="Invalid DataFrame Name")
                return False
            df_names = self.winfo_toplevel().SessionData.getDFNames()
            if name in set(df_names):
                if not self.open_overwrite_popup("DataFrame", name):
                    return False
        if self.save_col_var.get() == "new":
            col = self.new_col_entry.get().strip()
            if not col:
                self.err_label.config(text="Invalid Column Name")
                return False
            if col in set(self.winfo_toplevel().SessionData.getDataFrame(self.current_df).columns):
                if not self.open_overwrite_popup(f"column within DataFrame {self.current_df}", col):
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
        if not self.validate_inputs():
            return

        code, imports = ScaleExecutor.generate(
            df=self.params["df"],
            feature=self.params["feature"],
            technique=self.params["technique"],
            new_name=self.new_df_entry.get().strip() if self.save_df_var.get() == "new" else None, # new df name
            new_col=self.new_col_entry.get().strip() if self.save_col_var.get() == "new" else None, # new col name
            session=self.winfo_toplevel().SessionData,
            withImport=self.include_import_var.get()
        )

        if code:
            self.winfo_toplevel().SessionData.addOutput(code)
        if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

        self.reset_inputs()

    def reset_inputs(self):
        self.save_df_var.set("")
        self.new_df_entry.delete(0, tk.END)
        self.new_df_entry.config(state="disabled")

        self.save_col_var.set("")
        self.new_col_entry.delete(0, tk.END)
        self.new_col_entry.config(state="disabled")

        self.err_label.config(text="")
        self.generate_btn.config(state="disabled")