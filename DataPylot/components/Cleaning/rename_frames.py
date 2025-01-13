import tkinter as tk
from tkinter import ttk
import pandas as pd

from components.Cleaning.save_rename_frame import SaveRenameFrame
from components.Patterns.sequential_frames import SequentialFrameManager
from CodeGenerators.Cleaning.gen_exe_rename import RenameExecutor

class RenameFrames(SequentialFrameManager):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_frame(RenameValueFrame, manager=self)

        self.show_frame(0)

        self.next_btn.config(state="disabled")

class RenameValueFrame(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager

        self.df_names = self.winfo_toplevel().SessionData.getDFNames()
        self.df = None

        top_label = ttk.Label(
            self,
            text="Select DataFrame, Feature, and Values to Rename",
            font=("Arial", 14)
        )
        top_label.grid(row=0, column=0, padx=5, pady=(20, 5), sticky="n")

        select_df_text = ttk.Label(
            self,
            text="Select DataFrame:",
            font=("Arial", 12)
        )
        select_df_text.grid(row=1, column=0, padx=5, pady=(20, 5), sticky="w")

        self.df_dropdown = ttk.Combobox(
            self,
            state="readonly",
            values=self.df_names,
            width=30
        )
        self.df_dropdown.grid(row=1, column=0, padx=(250, 5), pady=(20, 5), sticky="w")
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

        select_values_text = ttk.Label(
            self,
            text="Select Values to Rename:",
            font=("Arial", 12)
        )
        select_values_text.grid(row=3, column=0, padx=5, pady=(15, 5), sticky="w")

        self.values_listbox = tk.Listbox(
            self,
            selectmode="extended",
            height=8,
            width=30
        )
        self.values_listbox.grid(row=3, column=0, padx=(250,5), pady=(15, 5), sticky="w")
        self.values_listbox.bind("<<ListboxSelect>>", lambda e: self.on_value_selected())

        instruction_label = ttk.Label(
            self,
            text="Hold Ctrl key to select multiple values or Shift key to select a range of values.",
            font=("Arial", 8)
        )
        instruction_label.grid(row=4, column=0, padx=5, pady=(5, 10), sticky="n")

        rename_to_text = ttk.Label(
            self,
            text="Rename Selected Values to:",
            font=("Arial", 12)
        )
        rename_to_text.grid(row=5, column=0, padx=5, pady=(30, 5), sticky="w")

        self.rename_to_entry = ttk.Entry(self, state="disabled", width=30)
        self.rename_to_entry.grid(row=5, column=0, padx=(250,5), pady=(30, 5), sticky="w")
        self.rename_to_entry.bind("<KeyRelease>", lambda e: self.validate_value())

        self.rename_err = ttk.Label(
            self,
            text="",
            font=("Arial", 8),
            foreground="red"
        )
        self.rename_err.grid(row=6, column=0, padx=5, pady=(5, 10), sticky="n")

        self.grid_columnconfigure(0, weight=1)


    def on_df_selected(self):
        self.df_name = self.df_dropdown.get()
        self.df = self.winfo_toplevel().SessionData.getDataFrame(self.df_name)
        if isinstance(self.df, pd.DataFrame):
            self.feat_dropdown.config(state="readonly", values=list(self.df.columns))
        else:
            self.feat_dropdown.config(state="disabled")

    def on_feat_selected(self):
        self.selected_feature = self.feat_dropdown.get()
        if self.selected_feature and self.selected_feature in self.df.columns:
            unique_values = sorted(self.df[self.selected_feature].dropna().unique())
            self.values_listbox.delete(0, tk.END)
            for value in unique_values:
                self.values_listbox.insert(tk.END, value)
            self.rename_to_entry.config(state="disabled")

    def on_value_selected(self):
        self.rename_to_entry.config(state="normal")

    def validate_value(self):
        if self.rename_to_entry.get().strip():
            self.rename_err.config(text="")
            selected_indices = self.values_listbox.curselection()
            self.selected_values = [self.values_listbox.get(i) for i in selected_indices]
            if self.df_dropdown.get() and self.feat_dropdown.get() and self.selected_values:
                self.capture_state()
                self.manager.delete_frame_by_index(1)
                self.manager.add_frame(SaveRenameFrame, manager=self.manager)
                self.manager.show_frame(0)
        else:
            self.rename_err.config(text="Enter a valid new name for the value(s).")

    def capture_state(self):
        self.manager.params['df_name'] = self.df_name
        self.manager.params['feature'] = self.selected_feature
        self.manager.params['values'] = self.selected_values
        self.manager.params['rename'] = self.rename_to_entry.get().strip()


