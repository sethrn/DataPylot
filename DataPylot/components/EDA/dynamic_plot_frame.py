import tkinter as tk
from tkinter import ttk
import pandas as pd
from pandas.api.types import is_numeric_dtype

from components.Patterns.generate_frame import GenerateCodeFrame
from config.plotting_config import BIVARIATE_CONFIG, MULTIVARIATE_CONFIG, UNIVARIATE_CONFIG
from CodeGenerators.EDA.gen_uni import UnivariatePlotGenerator
from CodeGenerators.EDA.gen_bi import BivariatePlotGenerator
from CodeGenerators.EDA.gen_multi import MultivariatePlotGenerator

class DynamicPlotFrame(GenerateCodeFrame):
    def __init__(self, parent, manager):
        super().__init__(parent)
        self.manager = manager

        if self.manager.params.get("class") == "uni":
            self.config = UNIVARIATE_CONFIG
            
            self.generator = UnivariatePlotGenerator
        elif self.manager.params.get("class") == "bi":
            self.config = BIVARIATE_CONFIG
            self.generator = BivariatePlotGenerator
        elif self.manager.params.get("class") == "multi":
            self.config = MULTIVARIATE_CONFIG
            self.generator = MultivariatePlotGenerator
        else:
            return

        self.df_name = self.manager.params.get("df_name")
        self.plot_type = self.manager.params.get("type")
        self.options = self.config.get(self.plot_type).get("options")
        self.widgets = []
        self.widget_vars = []
        self.input_types = []
        self.required_op_idx = []

        options = self.config.get(self.plot_type)["options"]
        self.required_op_idx = [i for i, option in enumerate(options) if option.get("required")]


        self.df = self.winfo_toplevel().SessionData.getDataFrame(self.df_name)
        if not isinstance(self.df, pd.DataFrame):
            return
        self.columns = self.df.columns
        self.numeric_columns = [feature for feature in self.df.columns if is_numeric_dtype(self.df[feature])]

        top_label = ttk.Label(
            self.content_frame,
            text=f"Customize {self.plot_type} for {self.df_name}",
            font=("Arial", 14)
        )
        top_label.grid(row=0, column=0, padx=5, pady=(20, 5), sticky="n")

        for i, option in enumerate(self.options):
            req_or_type_text = ""
            if i in self.required_op_idx:
                req_or_type_text = "(required)"
            elif option.get("entry") == "entry":
                req_or_type_text = f"({option.get('entry_type')})"

            option_label = ttk.Label(
                self.content_frame,
                text=f"{option.get('label')} {req_or_type_text}",
                font=("Arial", 10)
            )
            option_label.grid(row=i + 1, column=0, padx=5, pady=(10, 5), sticky="w")

            entry_type = option.get("entry_type")
            entry_kind = option.get("entry")
            default = option.get("default")
            self.input_types.append(entry_type)

            if entry_kind == "dropdown":
                cb = ttk.Combobox(self.content_frame, state="readonly", width=30)

                if entry_type == "any":
                    cb["values"] = list(self.columns)
                elif entry_type == "numeric":
                    cb["values"] = self.numeric_columns
                elif isinstance(entry_type, list):
                    cb["values"] = entry_type

                cb.bind("<<ComboboxSelected>>", lambda e: self.validate_required_inputs())
                cb.grid(row=i + 1, column=0, padx=(200, 5), pady=(10, 5), sticky="w")
                self.widgets.append(cb)
                self.widget_vars.append(cb)

            elif entry_kind == "checkbox":
                var = tk.BooleanVar(value=default)
                cb = ttk.Checkbutton(self.content_frame, text="enabled", variable=var, command=self.validate_required_inputs)
                cb.grid(row=i + 1, column=0, padx=(200, 5), pady=(10, 5), sticky="w")
                self.widgets.append(cb)
                self.widget_vars.append(var)

            elif entry_kind == "entry":
                var = tk.StringVar(value=str(default) if default is not None else "")
                entry = ttk.Entry(self.content_frame, textvariable=var)
                entry.grid(row=i + 1, column=0, padx=(200, 5), pady=(10, 5), sticky="w")
                self.widgets.append(entry)
                self.widget_vars.append(var)

            elif entry_kind == "text":
                var = tk.StringVar(value=default or "")
                entry = ttk.Entry(self.content_frame, textvariable=var, width=50)
                entry.grid(row=i + 1, column=0, padx=(200, 5), pady=(10, 5), sticky="w")
                self.widgets.append(entry)
                self.widget_vars.append(var)

        self.err_label = ttk.Label(
            self.content_frame,
            text="",
            foreground="red",
            font=("Arial", 9)
        )
        self.err_label.grid(row=len(self.options)+1, column=0, pady=(10, 5), sticky="s")

        self.content_frame.grid_columnconfigure(0, weight=1)
        self.generate_btn.config(state=("disabled" if self.required_op_idx else "normal"))

    def validate_required_inputs(self):
        for idx in self.required_op_idx:
            val = self._get_widget_value(idx)
            if not val:
                self.generate_btn.config(state="disabled")
                return False
        self.generate_btn.config(state="normal")
        return True

    def validate_optional_inputs(self):
        self.err_label.config(text="")

        for i, var in enumerate(self.widget_vars):
            if i in self.required_op_idx:
                continue
            if isinstance(var, tk.StringVar):
                val = var.get().strip()
                if val == "":
                    continue
                expected_type = self.input_types[i]
                try:
                    if expected_type == "int":
                        int(val)
                    elif expected_type == "float":
                        float(val)
                    else:
                        continue
                except Exception:
                    self.err_label.config(text=f"Invalid input for '{self.options[i]['label']}', must be of type {expected_type}")
                    return False

                if self.options[i]['label'] == "Alpha (Transparency)":
                    alpha_val = float(val)
                    if not (0 < alpha_val <= 1.0):
                        self.err_label.config(text=f"Invalid input for '{self.options[i]['label']}', must be in range of 0 to 1")
                        return False

        return True


    def _get_widget_value(self, idx):
        widget = self.widget_vars[idx]
        if isinstance(widget, tk.StringVar) or isinstance(widget, tk.BooleanVar):
            return widget.get()
        elif isinstance(widget, ttk.Combobox):
            return widget.get()
        return None

    def generate_code(self):
        if not self.validate_required_inputs():
            return

        if not self.validate_optional_inputs():
            return
        params = {}

        for i, option in enumerate(self.options):
            val = self._get_widget_value(i)
            if val == "" or val is None:
                if i in self.required_op_idx:
                    return
                else:
                    val = None
            params[option["label"]] = val

        code, imports = self.generator.generate(
            df=self.df_name,
            plot_type=self.plot_type,
            params=params,
            withImport=self.include_import_var.get()
        )

        if code:
            self.winfo_toplevel().SessionData.addOutput(code)
        if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

        self.winfo_toplevel().main_stage.refresh_children()
        