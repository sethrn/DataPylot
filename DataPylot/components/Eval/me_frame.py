import tkinter as tk
from tkinter import ttk

class METabFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)

        notebook.add(tab1, text="Performance Metrics")
        notebook.add(tab2, text="Visualizations")

        ttk.Label(tab1, text="Metrics Content").pack(pady=10)
        ttk.Label(tab2, text="Visualizations Content").pack(pady=10)