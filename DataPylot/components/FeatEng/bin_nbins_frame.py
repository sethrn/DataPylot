import re
import tkinter as tk
from tkinter import ttk

from CodeGenerators.FeatEng.gen_exe_kbins import KBinsExecutor
from components.Patterns.generate_frame import GenerateCodeFrame
from components.Patterns.popup_dialog import PopupDialog

class NBinsFrame(GenerateCodeFrame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager
        self.tech = self.manager.params["technique"]
        self.df_name = self.manager.params["df"]
        self.feature = self.manager.params["feature"]

        self.save_df_var = tk.StringVar(value="")
        self.save_col_var = tk.StringVar(value="")
        self.encoding_var = tk.StringVar(value="ordinal")

        self.nbins_entry = None
        self.prefix_entry = None


        top_label = ttk.Label(
            self.content_frame,
            text="Specify Binning Operation and Save Changes",
            font=("Arial", 14)
        )
        top_label.grid(row=0, column=0, padx=5, pady=(20,5), sticky="n")

        nbins_label = ttk.Label(
            self.content_frame,
            text="Specify Number of Bins:",
            font=("Arial", 10)
        )
        nbins_label.grid(row=1, column=0, padx=5, pady=(30,5), sticky="w")

        self.nbins_entry = ttk.Entry(
            self.content_frame,
            state="normal",
            width=15
        )
        self.nbins_entry.grid(row=1, column=0, padx=(150,5), pady=(30,5), sticky="w")


        self.encoding_label = ttk.Label(
            self.content_frame,
            text="Specify How to Store Bins",
            font=("Arial", 10)
        )
        self.encoding_label.grid(row=2, column=0, padx=5, pady=(30,5), sticky="w")

        self.ordinal_radio = ttk.Radiobutton(
            self.content_frame,
            text="Ordinal Encoding (One Column)",
            variable=self.encoding_var,
            value="ordinal",
            command=self.on_encoding_selected
        )
        self.ordinal_radio.grid(row=2, column=0, padx=(175,5), pady=(30,5), sticky="w")

        self.onehot_radio = ttk.Radiobutton(
            self.content_frame,
            text="One-Hot Encoding (N Columns)",
            variable=self.encoding_var,
            value="onehot",
            command=self.on_encoding_selected
        )
        self.onehot_radio.grid(row=2, column=0, padx=(375,5), pady=(30,5), sticky="w")

        save_df_text = ttk.Label(
            self.content_frame,
            text="Save Changes to:",
            font=("Arial", 12)
        )
        save_df_text.grid(row=3, column=0, padx=5, pady=(30,15), sticky="w")


        self.current_df_radio = ttk.Radiobutton(
            self.content_frame,
            text="Current DataFrame",
            variable=self.save_df_var,
            value="current",
            command=self.on_save_df_selected
        )
        self.current_df_radio.grid(row=3, column=0, padx=(150,5), pady=(30,15), sticky="w")

        self.new_df_radio = ttk.Radiobutton(
            self.content_frame,
            text="New DataFrame:",
            variable=self.save_df_var,
            value="new",
            command=self.on_save_df_selected
        )
        self.new_df_radio.grid(row=3, column=0, padx=(275, 5), pady=(30,15), sticky="w")

        self.new_df_entry = ttk.Entry(
            self.content_frame,
            state="disabled",
            width=15
        )
        self.new_df_entry.grid(row=3, column=0, padx=(400, 5), pady=(30,15), sticky="w")
        
        self.column_frame = ttk.Frame(self.content_frame)
        self.column_frame.grid(row=4, column=0, padx=0, pady=0, sticky="w")
        self.on_encoding_selected()

        self.err_label = ttk.Label(self.content_frame, text="", font=("Arial", 10), foreground="red")
        self.err_label.grid(row=5, column=0, padx=5, pady=(5, 10), sticky="n")

        self.generate_btn.config(state="disabled")
        self.content_frame.grid_columnconfigure(0, weight=1)

    def on_encoding_selected(self):
        for widget in self.column_frame.winfo_children():
            widget.destroy()

        if self.encoding_var.get() == "ordinal":
            save_col_text = ttk.Label(
                self.column_frame,
                text="Save Column:",
                font=("Arial", 12)
            )
            save_col_text.grid(row=0, column=0, padx=5, pady=(30,15), sticky="w")

            self.current_col_radio = ttk.Radiobutton(
                self.column_frame,
                text="Current Column",
                variable=self.save_col_var,
                value="current",
                command=self.on_save_col_selected
            )
            self.current_col_radio.grid(row=0, column=0, padx=(150, 5), pady=(30,15), sticky="w")

            self.new_col_radio = ttk.Radiobutton(
                self.column_frame,
                text="New Column:",
                variable=self.save_col_var,
                value="new",
                command=self.on_save_col_selected
            )
            self.new_col_radio.grid(row=0, column=0, padx=(275, 5), pady=(30,15), sticky="w")

            self.new_col_entry = ttk.Entry(
                self.column_frame,
                state="disabled",
                width=15
            )
            self.new_col_entry.grid(row=0, column=0, padx=(400, 5), pady=(30,15), sticky="w")
        
        elif self.encoding_var.get() == "onehot":
            prefix_label = ttk.Label(self.column_frame, text="Column Prefix:", font=("Arial", 12))
            prefix_label.grid(row=0, column=0, padx=5, pady=(30, 5), sticky="w")

            self.prefix_entry = ttk.Entry(self.column_frame, width=15)
            self.prefix_entry.insert(0, f"{self.feature}")
            self.prefix_entry.grid(row=0, column=0, padx=(150, 5), pady=(30, 5), sticky="w")


    def on_save_df_selected(self):
        if self.save_df_var.get() == "new":
            self.new_df_entry.config(state="normal")
        else:
            self.new_df_entry.config(state="disabled")
        if self.encoding_var.get() == "onehot":
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
        nbins_str = self.nbins_entry.get().strip()
        if not nbins_str.isdigit() or int(nbins_str) < 2:
            self.err_label.config(text="Invalid: Number of bins must be an integer greater than 1")
            return False

        if self.save_df_var.get() == "new":
            name = self.new_df_entry.get()
            if not self.validate_name(name):
                self.err_label.config(text="Invalid DataFrame Name")
                return False
            df_names = self.winfo_toplevel().SessionData.getDFNames()
            if name in set(df_names):
                if not self.open_overwrite_popup("DataFrame", name):
                    return False

        if self.encoding_var.get() == "ordinal" and self.save_col_var.get() == "new":
            col = self.new_col_entry.get().strip()
            if not col:
                self.err_label.config(text="Invalid Column Name")
                return False
            if col in set(self.winfo_toplevel().SessionData.getDataFrame(self.current_df).columns):
                if not self.open_overwrite_popup(f"column within DataFrame {self.current_df}", col):
                    return False

        if self.encoding_var.get() == "onehot" and (not self.prefix_entry or not self.prefix_entry.get().strip()):
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

        code, imports = KBinsExecutor.generate(
            df=self.df_name,
            feature=self.feature,
            technique=self.tech,
            encoding=self.encoding_var.get(),
            nbins=int(self.nbins_entry.get().strip()),
            new_name=self.new_df_entry.get().strip() if self.save_df_var.get() == "new" else None,
            new_col=self.new_col_entry.get().strip() if self.encoding_var.get() == "ordinal" and self.save_col_var.get() == "new" else None,
            prefix=self.prefix_entry.get().strip() if self.encoding_var.get() == "onehot" else None,
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
        if hasattr(self, "new_col_entry"):
            self.new_col_entry.delete(0, tk.END)
            self.new_col_entry.config(state="disabled")

        self.encoding_var.set("ordinal")
        self.nbins_entry.delete(0, tk.END)

        if self.prefix_entry:
            self.prefix_entry.delete(0, tk.END)

        self.on_encoding_selected()
        self.err_label.config(text="")

