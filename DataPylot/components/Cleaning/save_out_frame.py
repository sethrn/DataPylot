import tkinter as tk
from tkinter import ttk
import re

from components.Patterns.generate_frame import GenerateCodeFrame
from components.Patterns.popup_dialog import PopupDialog
from CodeGenerators.Cleaning.gen_exe_outlier import OutlierExecutor

class SaveOutlierFrame(GenerateCodeFrame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager
        self.params = manager.params
        self.current_df = self.params['df']
        self.remove_op = self.params['op'] == "remove"
       
        top_label = ttk.Label(
            self.content_frame,
            text="Select How to Save Changes",
            font=("Arial", 14)
        )
        top_label.grid(row=0, column=0, columnspan=2, padx=5, pady=(20,5), sticky="n")

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

        if not self.remove_op:
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
        self.content_frame.grid_columnconfigure(1, weight=1)

        self.generate_btn.config(state="disabled")
        
    def on_save_df_selected(self):
        if self.save_df_var.get() == "new":
            self.new_df_entry.config(state="normal")
        else:
            self.new_df_entry.config(state="disabled")
        if self.remove_op:
            self.generate_btn.config(state="normal")

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
        if not self.remove_op and self.save_col_var.get() == "new":
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

        code, imports = OutlierExecutor.generate(
            df=self.params["df"],
            operation=self.params["op"], #remove/cap
            feature=self.params["feature"], # feature or 'all'
            bound=self.params["bound"], # uppler/lower/both
            technique=self.params["technique"], #tueky/zscore/custom
            param=self.params["param"], #tukey/zscore/lower custom
            param2=self.params["param2"] if self.params.get("param2") else None, #upper custom
            new_name=self.new_df_entry.get().strip() if self.save_df_var.get() == "new" else None, # new df name
            new_col=self.new_col_entry.get().strip() if not self.remove_op and self.save_col_var.get() == "new" else None, # new col name
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


