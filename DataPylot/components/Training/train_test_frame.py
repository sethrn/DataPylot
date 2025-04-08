import tkinter as tk
from tkinter import ttk

class TTFrame(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)
        self.manager = manager

        self.approach_var = tk.StringVar()
        self.test_size_var = tk.DoubleVar(value=0.2)
        self.kfolds_var = tk.StringVar()
        self.stratify_var = tk.BooleanVar(value=True)
        self.warning_var = tk.StringVar(value="")

        top_label = ttk.Label(self, text="Specify Training Options", font=("Arial", 14))
        top_label.grid(row=0, column=0, padx=5, pady=(20, 5), sticky="n")
        
        approach_label = ttk.Label(self, text="Select Training Approach", font=("Arial", 11))
        approach_label.grid(row=1, column=0, padx=5, pady=(15,5), sticky="w")

        self.split_radio = ttk.Radiobutton(
            self, text="Use standard train/test split", variable=self.approach_var,
            value="split", command=self.on_approach_selected
        )
        self.split_radio.grid(row=1, column=0, padx=(250,5), pady=(15,5), sticky="w")

        self.cv_radio = ttk.Radiobutton(
            self, text="Perform K-fold cross validation", variable=self.approach_var,
            value="cv", command=self.on_approach_selected
        )
        self.cv_radio.grid(row=2, column=0, padx=(250,5), pady=(15,5), sticky="w")

        self.split_label = ttk.Label(self, text="Test size (fraction of total):", font=("Arial", 11))
        self.split_label.grid(row=3, column=0, padx=5, pady=(20, 5), sticky="w")

        self.split_slider = ttk.Scale(self, from_=0.05, to=0.5, length=200,
                                      variable=self.test_size_var, command=self.on_slider_change)
        self.split_slider.grid(row=3, column=0, padx=(250, 5), pady=(20, 5), sticky="w")
                                      
        self.slider_value_label = ttk.Label(self, text="0.20", font=("Arial", 10))
        self.slider_value_label.grid(row=3, column=0, padx=(450, 5), pady=(20, 5), sticky="w")

        # Placeholder for dynamic controls
        self.dynamic_label = ttk.Label(self, font=("Arial", 11))
        self.dynamic_label.grid(row=4, column=0, padx=5, pady=(10, 5), sticky="w")

        self.kfolds_entry = ttk.Entry(self, textvariable=self.kfolds_var, width=10)

        self.stratify_check = ttk.Checkbutton(
            self, text="Stratify by target", variable=self.stratify_var
        )

        self.warning_label = ttk.Label(self, textvariable=self.warning_var, font=("Arial", 9))
        self.warning_label.grid(row=6, column=0, padx=5, pady=(5, 0), sticky="n")

        self.grid_columnconfigure(0, weight=1)

    def on_approach_selected(self):
        approach = self.approach_var.get()

        if approach == "cv":
            self.dynamic_label.config(text="Number of folds:")
            self.kfolds_var.set("5")
            self.kfolds_entry.grid(row=4, column=0, padx=(250, 5), pady=(10, 5), sticky="w")
            self.stratify_check.grid_remove()
            self.split_label.config(text="Validation size per fold (fraction):")

        else:
            self.dynamic_label.config(text="Stratify classes:")
            self.stratify_check.grid(row=4, column=0, padx=(250, 5), pady=(10, 5), sticky="w")
            self.kfolds_entry.grid_remove()
            self.split_label.config(text="Test size (fraction of total):")

        self.manager.next_btn.config(state="normal")

    def on_slider_change(self, event):
        value = self.test_size_var.get()
        snapped_value = round(value / 0.05) * 0.05
        if snapped_value == value:
            return
        self.split_slider.set(snapped_value)
        self.slider_value_label.config(text=f"{snapped_value:.2f}")

        if snapped_value < 0.1 or snapped_value > 0.4:
            self.warning_var.set("Consider test size between 0.1 and 0.4 for balanced results.")
        else:
            self.warning_var.set("")

    def get_training_params(self):
        approach = self.approach_var.get()
        test_size = round(self.test_size_var.get(), 2)
        stratify = self.stratify_var.get() if approach == "split" else False
        kfolds = int(self.kfolds_var.get()) if approach == "cv" and self.kfolds_var.get().isdigit() else None

        return {
            "approach": approach,
            "test_size": test_size,
            "stratify": stratify,
            "kfolds": kfolds
        }

    def update_warning(self, warning):
        if warning:
            self.warning_var.set("K-folds value must be a digit.")
        else:
            self.warning_var.set("")