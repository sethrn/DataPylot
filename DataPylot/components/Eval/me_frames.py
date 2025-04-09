import tkinter as tk
from tkinter import ttk

from components.Patterns.generate_frame import GenerateCodeFrame
from components.Patterns.operation_tabs import OperationTabFrame
from config.model_eval_config import MODEL_EVAL_CONFIG

from CodeGenerators.Eval.gen_metrics import MetricsGenerator
from CodeGenerators.Eval.gen_model_vis import VisualsGenerator

class METabFrame(OperationTabFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_tab(MetricsFrame, "Performance Metrics")
        self.add_tab(VisualsFrame, "Performance Visualizations")

class MetricsFrame(GenerateCodeFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.metric_vars = []

        self.model_names = self.winfo_toplevel().SessionData.getModels()

        top_label = ttk.Label(self.content_frame, text="Generate Performance Metrics", font=("Arial", 14))
        top_label.grid(row=0, column=0, padx=5, pady=(20, 5), sticky="n")

        self.model_label = ttk.Label(self.content_frame, text="Select Model:", font=("Arial", 12))
        self.model_label.grid(row=1, column=0, padx=5, pady=(15, 5), sticky="w")

        self.model_dropdown = ttk.Combobox(self.content_frame, state="readonly", values=self.model_names, width=30)
        self.model_dropdown.grid(row=1, column=0, padx=(250, 5), pady=(15, 5), sticky="w")
        self.model_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_model_selected())

        self.metric_label = ttk.Label(self.content_frame, text="Select Metric(s):", font=("Arial", 12))
        self.metric_label.grid(row=2, column=0, padx=5, pady=(15, 5), sticky="w")

        self.metric_options = ttk.Frame(self.content_frame)
        self.metric_options.grid(row=2, column=0, padx=(250, 5), pady=(15, 5), sticky="nsew")

        self.generate_btn.config(state="disabled")
        self.content_frame.grid_columnconfigure(0, weight=1)

    def on_model_selected(self):
        for widget in self.metric_options.winfo_children():
            widget.destroy()
        self.metric_vars.clear()

        model_name = self.model_dropdown.get()
        model_type = self.winfo_toplevel().SessionData.getModelType(model_name)

        if model_type:
            model_info = MODEL_EVAL_CONFIG.get(model_type, {})
            model_metrics = model_info.get("metrics", [])

            if model_metrics:
                for i, metric in enumerate(model_metrics):
                    var = tk.BooleanVar(value=False)
                    check = ttk.Checkbutton(
                        self.metric_options, text=metric,
                        variable=var, command=self.on_metric_selected
                    )
                    check.grid(row=i, column=0, padx=5, pady=(15, 5), sticky="w")
                    self.metric_vars.append((metric, var))
            else:
                label = ttk.Label(self.metric_options, text="No Metrics Available.", font=("Arial", 12))
                label.grid(row=0, column=0, padx=0, pady=(15, 5), sticky="w")

    def on_metric_selected(self):
        if any(var.get() for _, var in self.metric_vars) and self.model_dropdown.get():
            self.generate_btn.config(state="normal")
        else:
            self.generate_btn.config(state="disabled")

    def generate_code(self):
        model_name = self.model_dropdown.get()
        selected_metrics = [metric for metric, var in self.metric_vars if var.get()]

        code, imports = MetricsGenerator.generate(
            model_name=model_name, metrics=selected_metrics, withImport=self.include_import_var.get()
        )

        if code:
            self.winfo_toplevel().SessionData.addOutput(code)

        if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

        self.winfo_toplevel().main_stage.refresh_children()

class VisualsFrame(GenerateCodeFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.visual_var = tk.StringVar(value="")

        self.model_names = self.winfo_toplevel().SessionData.getModels()

        top_label = ttk.Label(self.content_frame, text="Generate a Performance Visualization", font=("Arial", 14))
        top_label.grid(row=0, column=0, padx=5, pady=(20,5), sticky="n")

        self.model_label = ttk.Label(self.content_frame, text="Select Model:", font=("Arial", 12))
        self.model_label.grid(row=1, column=0, padx=5, pady=(15,5), sticky="w")

        self.model_dropdown = ttk.Combobox(self.content_frame, state="readonly", values=self.model_names, width=30)
        self.model_dropdown.grid(row=1, column=0, padx=(250,5), pady=(15,5), sticky="w")
        self.model_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_model_selected())

        self.vis_label = ttk.Label(self.content_frame, text="Select Visualization:", font=("Arial", 12))
        self.vis_label.grid(row=2, column=0, padx=5, pady=(15,5), sticky="w")

        self.visual_options = ttk.Frame(self.content_frame)
        self.visual_options.grid(row=2, column=0, padx=(250, 5), pady=(15,5), sticky="nsew")

        self.generate_btn.config(state="disabled")
        self.content_frame.grid_columnconfigure(0, weight=1)

    def on_model_selected(self):
        for widget in self.visual_options.winfo_children():
            widget.destroy()

        model_name = self.model_dropdown.get()
        model_type = self.winfo_toplevel().SessionData.getModelType(model_name)

        if model_type:
            model_info = MODEL_EVAL_CONFIG.get(model_type, {})
            model_visuals = model_info.get("visuals", [])

            if model_visuals:
                for i, visual in enumerate(model_visuals):
                    visual_option = ttk.Radiobutton(self.visual_options, text=visual, 
                                                    variable=self.visual_var, value=visual,
                                                    command=self.on_visual_selected)
                    visual_option.grid(row=i, column=0, padx=0, pady=(15,5), sticky="w")

            else:
                visual_option = ttk.Label(self.visual_options, text="No Visualizations Available.", font=("Arial", 12))
                visual_option.grid(row=0, column=0, padx=0, pady=(15,5), sticky="w")
     
    def on_visual_selected(self):
       if self.model_dropdown.get() and self.visual_var.get():
            self.generate_btn.config(state="normal")

    def generate_code(self):
        model_name = self.model_dropdown.get()
        visual = self.visual_var.get()

        code, imports = VisualsGenerator.generate(
            model_name=model_name, visual=visual, withImport=self.include_import_var.get())

        if code:
            self.winfo_toplevel().SessionData.addOutput(code)
        if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

        self.winfo_toplevel().main_stage.refresh_children()

