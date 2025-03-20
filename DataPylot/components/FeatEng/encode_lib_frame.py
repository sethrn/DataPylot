import tkinter as tk
from tkinter import ttk
import re

from components.Patterns.dnd_listbox import DragDropListbox
from components.Patterns.generate_frame import GenerateCodeFrame
from components.Patterns.popup_dialog import PopupDialog
from CodeGenerators.FeatEng.gen_exe_encodelib import EncodeLibExecutor

class EncodeLibFrame(GenerateCodeFrame):
    def __init__(self, parent, manager):
        super().__init__(parent)
        self.manager = manager
        self.tech = self.manager.params["technique"]
        self.df_name = self.manager.params["df"]
        self.feature = self.manager.params["feature"]

        self.save_df_var = tk.StringVar(value="")
        self.save_col_var = tk.StringVar(value="")
        self.drop_first_var = tk.BooleanVar(value=False)

        top_label = ttk.Label(
            self.content_frame, 
            text="Specify Encoding Operation and Save Changes", 
            font=("Arial", 14)
        )
        top_label.grid(row=0, column=0, padx=5, pady=(20, 5), sticky="n")

        save_df_text = ttk.Label(
            self.content_frame,
            text="Save Changes to:",
            font=("Arial", 12)
        )
        save_df_text.grid(row=1, column=0, padx=5, pady=(30,15), sticky="w")


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

        if self.tech == "ordinal":
            self.setup_ordinal_ui()
        elif self.tech == "onehot":
            self.setup_onehot_ui()

        self.err_label = ttk.Label(self.content_frame, text="", font=("Arial", 10), foreground="red")
        self.err_label.grid(row=5, column=0, padx=5, pady=(5, 10), sticky="n")

        self.generate_btn.config(state="disabled")
        self.content_frame.grid_columnconfigure(0, weight=1)

    def on_save_df_selected(self):
        if self.save_df_var.get() == "new":
            self.new_df_entry.config(state="normal")
        else:
            self.new_df_entry.config(state="disabled")
        if self.tech != "custom":
            self.generate_btn.config(state="normal")

    def setup_ordinal_ui(self):
        save_col_text = ttk.Label(
            self.content_frame,
            text="Save Column:",
            font=("Arial", 12)
        )
        save_col_text.grid(row=2, column=0, padx=5, pady=(30,15), sticky="w")

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

        order_label = ttk.Label(self.content_frame, text="Set Category Order:", font=("Arial", 12))
        order_label.grid(row=3, column=0, padx=5, pady=(15, 5), sticky="w")

        self.order_listbox = DragDropListbox(self.content_frame, height=8, width=30) 
        self.order_listbox.grid(row=3, column=0, padx=(250,5), pady=(15, 5), sticky="w")

        df = self.winfo_toplevel().SessionData.getDataFrame(self.df_name)
        if df is not None:
            unique_values = df[self.feature].dropna().unique()
            for value in unique_values:
                self.order_listbox.insert(tk.END, value)
        self.generate_btn.config(state="disabled")

    def on_save_col_selected(self):
        if self.save_col_var.get() == "new":
            self.new_col_entry.config(state="normal")
        else:
            self.new_col_entry.config(state="disabled")
        self.generate_btn.config(state="normal")

    def setup_onehot_ui(self):
        drop_first_label = ttk.Label(self.content_frame, text="Drop First Category?", font=("Arial", 12))
        drop_first_label.grid(row=2, column=0, padx=5, pady=(15, 5), sticky="w")

        self.drop_first_var = tk.StringVar(value="no")

        self.drop_first_yes = ttk.Radiobutton(
            self.content_frame,
            text="Yes",
            variable=self.drop_first_var,
            value="yes"
        )
        self.drop_first_yes.grid(row=2, column=0, padx=(250, 5), pady=(15, 5), sticky="w")

        self.drop_first_no = ttk.Radiobutton(
            self.content_frame,
            text="No",
            variable=self.drop_first_var,
            value="no"
        )
        self.drop_first_no.grid(row=2, column=0, padx=(310, 5), pady=(15, 5), sticky="w")

        prefix_label = ttk.Label(self.content_frame, text="Prefix for Encoded Columns:", font=("Arial", 12))
        prefix_label.grid(row=3, column=0, padx=5, pady=(15, 5), sticky="w")

        self.prefix_entry = ttk.Entry(self.content_frame, width=30)
        self.prefix_entry.insert(0, self.feature)
        self.prefix_entry.grid(row=3, column=0, padx=(250, 5), pady=(15, 5), sticky="w")


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
        if self.tech == "onehot" and not self.prefix_entry.get().strip():
            self.err_label.config(text="Invalid Prefix Name")
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

        ordinal_order = list(self.order_listbox.get(0, tk.END)) if self.tech == "ordinal" else None

        code, imports = EncodeLibExecutor.generate(
            df=self.df_name,
            feature=self.feature,
            technique=self.tech,
            new_name=self.new_df_entry.get().strip() if self.save_df_var.get() == "new" else None,
            new_col=self.new_col_entry.get().strip() if self.save_col_var.get() == "new" else None,
            ordinal_order=ordinal_order,
            drop_first=self.drop_first_var.get() if self.tech == "onehot" else None,
            prefix=self.prefix_entry.get().strip() if self.tech == "onehot" else None,
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
        self.drop_first_var.set(False)

        if self.tech == "ordinal":
            self.new_col_entry.delete(0, tk.END)
            self.new_col_entry.config(state="disabled")
        elif self.tech == "onehot":
            self.prefix_entry.delete(0, tk.END)
            self.prefix_entry.insert(0, "encoded")

        self.err_label.config(text="")
        self.generate_btn.config(state="disabled")
