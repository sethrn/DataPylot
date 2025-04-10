import tkinter as tk
from tkinter import ttk
import re

from components.Patterns.popup_dialog import PopupDialog
from components.Patterns.generate_frame import GenerateCodeFrame
from config.model_config import MODEL_CONFIG
from CodeGenerators.Training.gen_model import ModelGenerator

class HyperFrame(GenerateCodeFrame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager
        self.model_type = self.manager.params["model"]
        self.param_entries = {}

        save_label = ttk.Label(self.content_frame, text=f"Specify Model Name and (Optional) Hyperparameters for {self.model_type}", font=("Arial", 14))
        save_label.grid(row=0, column=0, padx=5, pady=(20,5), sticky="n")

        save_model_text = ttk.Label(self.content_frame, text="Enter Name for Model:", font=("Arial", 10))
        save_model_text.grid(row=1, column=0, padx=5, pady=(15, 5), sticky="w")

        self.model_name_entry = ttk.Entry(self.content_frame, width=15)
        self.model_name_entry.grid(row=1, column=0, padx=(225,5), pady=(15, 5), sticky="w")

        self.param_frame = ttk.Frame(self.content_frame)
        self.param_frame.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.build_param_fields()

        self.err_label = ttk.Label(self.content_frame, text="", foreground="red", font=("Arial", 10))
        self.err_label.grid(row=3, column=0, padx=5, pady=(5,10), sticky="n")

        self.generate_btn.config(state="normal")

        self.content_frame.grid_columnconfigure(0, weight=1)

    def build_param_fields(self):
        model_params = MODEL_CONFIG.get(self.model_type, [])
            
        for i, param in enumerate(model_params):
            label = ttk.Label(self.param_frame, text=f"{param['name']} ({param['type'].__name__})", font=("Arial", 10))
            label.grid(row=i, column=0, padx=5, pady=(15, 5), sticky="w")

            entry = ttk.Entry(self.param_frame, width=25)
            entry.insert(0, str(param.get("default", "None")))
            entry.grid(row=i, column=0, padx=(225,5), pady=5, sticky="w")

            self.param_entries[param["name"]] = {
                "widget": entry,
                "type": param["type"],
                "default": param.get("default", None),
                "allow_none": param.get("allow_none", False)
            }

    def validate_name(self, name):
        return re.match(r"^[A-Za-z]\w*$", name) is not None

    def validate_inputs(self):
        for name, info in self.param_entries.items():
            raw = info["widget"].get().strip()
            if raw.lower() == "none":
                 if not info.get("allow_none", False):
                    self.err_label.config(text=f"'{name}' cannot be None.")
                    return False
            else:
                try:
                    info["type"](raw)
                except ValueError:
                    self.err_label.config(text=f"Invalid value for '{name}'. Expected {info['type'].__name__}")
                    return False

        model_name = self.model_name_entry.get().strip().lower()
        if not self.validate_name(model_name):
            self.err_label.config(text="Invalid Model Name")
            return False
        if model_name in [name.lower for name in self.winfo_toplevel().SessionData.getModels()]:
            if not self.open_overwrite_popup("model", model_name):
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

        hyperparams = {}
        for name, info in self.param_entries.items():
            raw = info["widget"].get().strip().lower()
            if raw != "none":
                value = info["type"](raw)
            else:
                value = None
            if value == "" or value == info["default"]:
                continue
            hyperparams[name] = repr(value)

        self.manager.params["model_name"] = self.model_name_entry.get().strip()
        self.manager.params["hyperparams"] = hyperparams

        print(self.manager.params.items())
        
        code, imports = ModelGenerator.generate(
            params=self.manager.params,
            session=self.winfo_toplevel().SessionData,
            withImport=self.include_import_var.get()
        )
        
        if code:
            self.winfo_toplevel().SessionData.addOutput(code)
        if imports:
            self.winfo_toplevel().SessionData.addImports(imports)
        
        self.winfo_toplevel().main_stage.refresh_children()

