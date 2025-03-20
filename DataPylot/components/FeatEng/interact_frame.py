import tkinter as tk
from tkinter import ttk
import pandas as pd
import re
from pandas.api.types import is_numeric_dtype


from components.Patterns.generate_frame import GenerateCodeFrame
from components.Patterns.popup_dialog import PopupDialog
from CodeGenerators.FeatEng.gen_exe_interaction import InteractionExecutor

class InteractionFrame(GenerateCodeFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.save_df_var = tk.StringVar(value="")
        self.df_names = self.winfo_toplevel().SessionData.getDFNames()

        top_label = ttk.Label(self.content_frame, text="Select DataFrame, Interaction Terms, and Saving Options", font=("Arial", 14))
        top_label.grid(row=0, column=0, padx=5, pady=(20,5), sticky="n")

        select_df_text = ttk.Label(self.content_frame, text="Select DataFrame:", font=("Arial", 12))
        select_df_text.grid(row=1, column=0, padx=5, pady=(20, 5), sticky="w")

        self.df_dropdown = ttk.Combobox(
            self.content_frame, state="readonly", values=self.df_names, width=30
        )
        self.df_dropdown.grid(row=1, column=0, padx=(250, 5), pady=(20, 5), sticky="w")
        self.df_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_df_selected())


        select_feat_text = ttk.Label(self.content_frame, text="Create Interaction:", font=("Arial", 12))
        select_feat_text.grid(row=2, column=0, padx=5, pady=(20, 5), sticky="w")

        self.feat1_dropdown = ttk.Combobox(self.content_frame, state="disabled", width=25)
        self.feat1_dropdown.grid(row=2, column=0, padx=(150, 5), pady=(20, 5), sticky="w")

        x_label = ttk.Label(self.content_frame, text="X", font=("Arial", 14))
        x_label.grid(row=2, column=0, padx=(335,5), pady=(20,5), sticky="w")
        
        self.feat2_dropdown = ttk.Combobox(self.content_frame, state="disabled", width=25)
        self.feat2_dropdown.grid(row=2, column=0, padx=(375, 5), pady=(20, 5), sticky="w")

        self.feat1_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_feat_selected())
        self.feat2_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_feat_selected())

        feature_label = ttk.Label(self.content_frame, text="Feature Name:", font=("Arial", 12))
        feature_label.grid(row=3, column=0, padx=5, pady=(20,5), sticky="w")

        self.feature_entry = ttk.Entry(self.content_frame, width=20, state="readonly")
        self.feature_entry.grid(row=3, column=0, padx=5, pady=(20,5), sticky="n")


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

        self.content_frame.grid_columnconfigure(0, weight=1)

        self.generate_btn.config(state="disabled")       

 
    def on_df_selected(self):
        self.df = self.winfo_toplevel().SessionData.getDataFrame(self.df_dropdown.get())
        
        if not isinstance(self.df, pd.DataFrame):
            return

        features = [feature for feature in self.df.columns if is_numeric_dtype(self.df[feature])]

        self.feat1_dropdown.config(
            state="readonly",
            values=features
        )
        self.feat1_dropdown.set("")

        self.feat2_dropdown.config(
            state="readonly",
            values=features
        )
        self.feat2_dropdown.set("")

        self.feature_entry.delete(0, tk.END)
        self.feature_entry.config(state="readonly")

        self.current_df_radio.config(state="disabled")
        self.new_df_radio.config(state="disabled")
        self.new_df_entry.config(state="disabled")
        self.save_df_var.set("")

        self.generate_btn.config(state="disabled")

    def on_feat_selected(self):
        if self.df_dropdown.get() and self.feat1_dropdown.get() and self.feat2_dropdown.get():
            self.feature_entry.config(state="normal")
            self.feature_entry.delete(0, tk.END)
            self.feature_entry.insert(0, f"{self.feat1_dropdown.get()}_X_{self.feat2_dropdown.get()}")
            
            self.current_df_radio.config(state="normal")
            self.new_df_radio.config(state="normal")
            self.save_df_var.set("")
        else:
            self.feature_entry.delete(0, tk.END)
            self.feature_entry.config(state="readonly")

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
        feature_name = self.feature_entry.get().strip()
        if not feature_name:
            self.err_label.config(text="Error: Feature name cannot be empty.")
            return False
    
        df_features = set(self.winfo_toplevel().SessionData.getDataFrame(self.df_dropdown.get()).columns)
        if feature_name in df_features:
            if not self.open_overwrite_popup(f"column within DataFrame {self.df_dropdown.get()}", feature_name):
                return False
    
        if self.save_df_var.get() == "new":
            new_df_name = self.new_df_entry.get().strip()
            if not self.validate_name(new_df_name):
                self.err_label.config(text="Error: Invalid DataFrame name.")
                return False
        
            df_names = self.winfo_toplevel().SessionData.getDFNames()
            if new_df_name in df_names:
                if not self.open_overwrite_popup("DataFrame", new_df_name):
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

        code, imports = InteractionExecutor.generate(
            df=self.df_dropdown.get(),
            feature1=self.feat1_dropdown.get(),
            feature2=self.feat2_dropdown.get(),
            new_col=self.feature_entry.get().strip(),
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
        self.feat1_dropdown.set("")
        self.feat2_dropdown.set("")
    
        self.feat1_dropdown.config(state="disabled")
        self.feat2_dropdown.config(state="disabled")

        self.feature_entry.delete(0, tk.END)
        self.feature_entry.config(state="readonly")

        self.save_df_var.set("")
        self.new_df_entry.delete(0, tk.END)
        self.new_df_entry.config(state="disabled")

        self.current_df_radio.config(state="disabled")
        self.new_df_radio.config(state="disabled")

        self.generate_btn.config(state="disabled")

        self.err_label.config(text="")
