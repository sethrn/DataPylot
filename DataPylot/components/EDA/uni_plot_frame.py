import tkinter as tk
from tkinter import ttk

from components.Patterns.generate_frame import GenerateCodeFrame
from CodeGenerators.EDA.gen_uni import UnivariatePlotGenerator

class UniPlotFrame(GenerateCodeFrame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager
        self.plot_type = manager.params.get('type')

        top_label = ttk.Label(
            self.content_frame, 
            text=f"Customize {self.plot_type} (Optional)", 
            font=("Arial", 12)
        )
        top_label.grid(row=0, column=0, padx=5, pady=5, sticky="n")

        self.title_var = tk.StringVar()
        title_label = ttk.Label(
            self.content_frame, 
            text="Set Plot Title:",
            font=("Arial", 10)
        )
        title_label.grid(row=1, column=0, padx=5, pady=(25,5), sticky="w")

        self.title_entry = ttk.Entry(
            self.content_frame,
            textvariable=self.title_var,
            width=30
        )
        self.title_entry.grid(row=1, column=0, padx=(250,5), pady=(25,5), sticky="w")

        xaxis_label = ttk.Label(
            self.content_frame, 
            text="Set X Axis Tick Rotation:", 
            font=("Arial", 10)
        )
        xaxis_label.grid(row=2, column=0, padx=5, pady=(25,5), sticky="w")

        self.xaxis_value = tk.StringVar(value="0")
        self.xaxis_entry = ttk.Entry(
            self.content_frame,
            textvariable=self.xaxis_value,
            width=5
        )
        self.xaxis_entry.grid(row=2, column=0, padx=(250,5), pady=(25,5), sticky="w")

        self.xaxis_err = ttk.Label(
            self.content_frame,
            text="",
            font=("Arial", 10)
        )
        self.xaxis_err.grid(row=2, column=0, padx=(350,5), pady=(25,5), sticky="w")
        
        color_label = ttk.Label(
            self.content_frame, 
            text="Set Color:", 
            font=("Arial", 10)
        )
        color_label.grid(row=3, column=0, padx=5, pady=(25,5), sticky="w")

        self.color_entry = ttk.Combobox(
            self.content_frame,
            state="readonly",
            values=['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'black', 'white'],
            width=30
        )
        self.color_entry.grid(row=3, column=0, padx=(250,5), pady=(25,5), sticky="w")

        self.content_frame.grid_columnconfigure(0, weight=1)

    def validate_rotation(self, rotation):
        try:
            rotation = int(rotation)
            return rotation >= 0
        except ValueError:
            return False

    def generate_code(self):
        title = self.title_var.get().strip()
        rotation = self.xaxis_value.get().strip()
        color = self.color_entry.get()

        if not self.validate_rotation(rotation):
            self.xaxis_err.config(
                text="Invalid rotation value",
                foreground="red"
            )
            return
        else:
            self.xaxis_err.config(text="")

        rotation = int(rotation)

        code, imports = UnivariatePlotGenerator.generate(
            df=self.manager.params.get('df'),
            feature=self.manager.params.get('feature'), 
            plot=self.plot_type, 
            title=title, 
            rotation=rotation, 
            color=color,
            withImport=self.include_import_var.get()
        )
        if code:
            self.winfo_toplevel().SessionData.addOutput(code)
        if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

        self.reset_inputs()

    def reset_inputs(self):
        self.title_var.set("")
        self.xaxis_value.set("0")
        self.color_entry.set("")