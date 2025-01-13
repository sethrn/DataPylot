import tkinter as tk
from tkinter import ttk

class FETabFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)
        tab4 = ttk.Frame(notebook)

        notebook.add(tab1, text="Transform Feature")
        notebook.add(tab2, text="Encode Categorical Feature")
        notebook.add(tab3, text="Bin Numeric Feature")
        notebook.add(tab4, text="Create Interaction Term")

        ttk.Label(tab1, text="Transformations Content").pack(pady=10)
        ttk.Label(tab2, text="Encodings Content").pack(pady=10)
        ttk.Label(tab3, text="Binnings Content").pack(pady=10)
        ttk.Label(tab4, text="Interaction Term Content").pack(pady=10)