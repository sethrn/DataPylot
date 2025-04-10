import tkinter as tk
from tkinter import ttk

class IntroFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ttk.Label(
            self, 
            text="Welcome to DataPylot", 
            font=("Helvetica", 24, "bold")
        ).pack(pady=(20, 10), anchor="n")

        ttk.Label(
            self, 
            text="Your no-code, no-AI tool for applying supervised machine learning,\n"
                 "enabling you to hone in on your analysis, decision-making, and strategy.",
            font=("Helvetica", 16)
        ).pack(pady=(0, 20), anchor="n")

        ttk.Label(
            self, 
            text="What DataPylot Helps You Do:", 
            font=("Helvetica", 20, "bold")
        ).pack(pady=(0, 5), anchor="n")

        ttk.Label(self, text="- Explore your data with visualizations, statistics, and reports", font=("Helvetica", 14)).pack(anchor="w", padx=15)
        ttk.Label(self, text="- Clean your data", font=("Helvetica", 14)).pack(anchor="w", padx=15)
        ttk.Label(self, text="- Manipulate your data and create features ", font=("Helvetica", 14)).pack(anchor="w", padx=15)
        ttk.Label(self, text="- Train supervised machine learning models", font=("Helvetica", 14)).pack(anchor="w", padx=15)
        ttk.Label(self, text="- Assess model performance through metrics and visualizations", font=("Helvetica", 14)).pack(anchor="w", padx=15)

        ttk.Label(
            self, 
            text="How It Works:", 
            font=("Helvetica", 20, "bold")
        ).pack(pady=(20, 5), anchor="n")

        ttk.Label(self, text="- Start by uploading a dataset", font=("Helvetica", 14)).pack(anchor="w", padx=15)
        ttk.Label(self, text="- Choose options at each step", font=("Helvetica", 14)).pack(anchor="w", padx=15)
        ttk.Label(self, text="- Undo the latest change if needed", font=("Helvetica", 14)).pack(anchor="w", padx=15)
        ttk.Label(self, text="- Download your DataFrame anytime", font=("Helvetica", 14)).pack(anchor="w", padx=15)
        ttk.Label(self, text="- If you modify your data outside of DataPylot, download it and re-upload to stay in sync", font=("Helvetica", 14)).pack(anchor="w", padx=15)
        
        ttk.Label(
            self, 
            text="Designed to help you build intuition in applying machine learning, instead of focusing on the code.",
            font=("Helvetica", 16, "italic")
        ).pack(pady=(20, 5), anchor="w")

        ttk.Label(
            self, 
            text=("Get started by clicking 'Import Dataset' on the left."),
            font=("Helvetica", 16)
        ).pack(anchor="w", padx=0)
