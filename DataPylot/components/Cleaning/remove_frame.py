import tkinter as tk
from tkinter import ttk
import re
import pandas as pd

from components.Patterns.generate_frame import GenerateCodeFrame
from components.Patterns.popup_dialog import PopupDialog
from CodeGenerators.Cleaning.gen_exe_remove import RemoveExecutor

class RemoveFeatureFrame(GenerateCodeFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.df_names = self.winfo_toplevel().SessionData.getDFNames()
        self.df = None

        top_label = ttk.Label(
            self.content_frame,
            text="Select DataFrame and Features to Remove",
            font=("Arial", 14)
        )
        top_label.grid(row=0, column=0, padx=5, pady=(20,5), sticky="n")

        select_df_text = ttk.Label(
            self.content_frame,
            text="Select DataFrame:",
            font=("Arial", 12)
        )
        select_df_text.grid(row=1, column=0, padx=5, pady=(20, 5), sticky="w")

        self.df_dropdown = ttk.Combobox(
            self.content_frame,
            state="readonly",
            values=self.df_names,
            width=30
        )
        self.df_dropdown.grid(row=1, column=0, padx=(250, 5), pady=(20, 5), sticky="w")
        self.df_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_df_selected())

        select_feat_text = ttk.Label(
            self.content_frame,
            text="Select Features to Remove:",
            font=("Arial", 12)
        )
        select_feat_text.grid(row=2, column=0, padx=5, pady=(15, 5), sticky="w")

        self.feat_listbox = tk.Listbox(
            self.content_frame,
            selectmode="extended",
            height=8,
            width=30
        )
        self.feat_listbox.grid(row=2, column=0, padx=(250,5), pady=(15, 5), sticky="w")
        self.feat_listbox.bind("<<ListboxSelect>>", lambda e: self.on_feat_selected())

        instruction_label = ttk.Label(
            self.content_frame,
            text="Hold Ctrl key to select multiple features or Shift key to select a range of features.",
            font=("Arial", 8)
        )
        instruction_label.grid(row=3, column=0, padx=5, pady=(5, 10), sticky="n")

        save_df_text = ttk.Label(
            self.content_frame,
            text="Save Changes to:",
            font=("Arial", 12)
        )
        save_df_text.grid(row=4, column=0, padx=5, pady=(30,15), sticky="w")

        self.save_df_var = tk.StringVar(value="")

        self.current_df_radio = ttk.Radiobutton(
            self.content_frame,
            text="Current DataFrame",
            variable=self.save_df_var,
            value="current",
            command=self.on_save_df_selected,
            state="disabled"
        )
        self.current_df_radio.grid(row=4, column=0, padx=(150,5), pady=(30,15), sticky="w")

        self.new_df_radio = ttk.Radiobutton(
            self.content_frame,
            text="New DataFrame:",
            variable=self.save_df_var,
            value="new",
            command=self.on_save_df_selected,
            state="disabled"
        )
        self.new_df_radio.grid(row=4, column=0, padx=(275, 5), pady=(30,15), sticky="w")

        self.new_df_entry = ttk.Entry(
            self.content_frame,
            state="disabled",
            width=15
        )
        self.new_df_entry.grid(row=4, column=0, padx=(400, 5), pady=(30,15), sticky="w")

        self.err_label = ttk.Label(
            self.content_frame,
            text="",
            font=("Arial", 10),
            foreground="red"
        )
        self.err_label.grid(row=5, column=0, columnspan=2, padx=5, pady=(25,5), sticky="n")

        self.generate_btn.config(state="disabled")
        self.content_frame.grid_columnconfigure(0, weight=1)

    def on_df_selected(self):
        self.df_name = self.df_dropdown.get()
        self.df = self.winfo_toplevel().SessionData.getDataFrame(self.df_name)
        if isinstance(self.df, pd.DataFrame):
            features = list(self.df.columns)
            self.feat_listbox.delete(0, tk.END)
            for value in features:
                self.feat_listbox.insert(tk.END, value)

    def on_feat_selected(self):
        self.current_df_radio.config(state="normal")
        self.new_df_radio.config(state="normal")

    def on_save_df_selected(self):
        if self.save_df_var.get() == "new":
            self.new_df_entry.config(state="normal")
        else:
            self.new_df_entry.config(state="disabled")

        selected_indices = self.feat_listbox.curselection()
            
        if self.df_dropdown.get() and selected_indices:
            self.selected_features = [self.feat_listbox.get(i) for i in selected_indices]
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
        if not self.validate_inputs():
            return

        code, imports = RemoveExecutor.generate(
            df=self.df_dropdown.get(),
            features=self.selected_features,
            new_name=self.new_df_entry.get().strip() if self.save_df_var.get() == "new" else None,
            session=self.winfo_toplevel().SessionData,
            withImport=self.include_import_var.get()
        )

        if code:
            self.winfo_toplevel().SessionData.addOutput(code)
        if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

        self.reset_inputs()

    def reset_inputs(self):
        self.df_dropdown.set("")
        self.feat_listbox.delete(0, tk.END)      
        self.save_df_var.set("")
        self.current_df_radio.config(state="disabled")
        self.new_df_radio.config(state="disabled")
        self.new_df_entry.delete(0, tk.END)
        self.generate_btn.config(state="disabled")
