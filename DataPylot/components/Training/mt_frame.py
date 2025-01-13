import tkinter as tk
from tkinter import ttk

class MTTabFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)

        notebook.add(tab1, text="Model Training")
        notebook.add(tab2, text="Cross Validation")

        ttk.Label(tab1, text="Model Training Content").pack(pady=10)
        ttk.Label(tab2, text="Cross Validation Content").pack(pady=10)