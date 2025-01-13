import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

class GenerateCodeFrame(ttk.Frame, ABC):
    def __init__(self, parent):
        super().__init__(parent)

        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

        self.gen_frame = ttk.Frame(self)
        self.gen_frame.pack(side="bottom", fill="x", pady=10)

        self.include_import_var = tk.BooleanVar(value=False)
        self.import_btn = ttk.Checkbutton(
            self.gen_frame,
            text="Include Import Statements",
            variable=self.include_import_var
        )

        self.generate_btn= ttk.Button(
            self.gen_frame,
            text="Generate Code",
            command=self.generate_code
        )

        self.generate_btn.pack(side="right", padx=5)
        self.import_btn.pack(side="right", padx=5)

    @abstractmethod
    def generate_code(self, *args, **kwargs):
        raise NotImplementedError("generate_code not implemented")

        