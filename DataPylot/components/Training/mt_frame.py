import tkinter as tk
from tkinter import ttk
from pandas.api.types import is_numeric_dtype

from components.Patterns.sequential_frames import SequentialFrameManager
from components.Training.train_test_frame import TTFrame
from components.Training.hyper_frame import HyperFrame

class MTFrames(SequentialFrameManager):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_frame(ModelFrame, self)
        self.show_frame(0)
        self.next_btn.config(state="disabled")

    def next_frame(self):
        if self.current_index == 0:
            if len(self.frames) > 1:
                self.frames = self.frames[:1]
            self.add_frame(TTFrame, self)
            self.show_frame(1)
        elif self.current_index == 1:
            
            tt_params = self.frames[1].get_training_params()
            if tt_params["approach"] == "cv" and not tt_params["kfolds"]:
                self.frames[1].update_warning(True)
            else:
                self.frames[1].update_warning(False)
                if len(self.frames) > 2:
                    self.frames = self.frames[:2]
                self.params.update(tt_params)
                self.add_frame(HyperFrame, self)
                self.show_frame(2)


class ModelFrame(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager

        self.df_names = self.winfo_toplevel().SessionData.getDFNames()
        self.type_var = tk.StringVar(value="")
        self.numeric_feats = None
        self.all_feats = tk.BooleanVar(value=False)

        top_label = ttk.Label(
            self, text="Train a Model",
            font=("Arial", 14))
        top_label.grid(row=0, column=0, padx=5, pady=(20,5), sticky="n")

        # Select DataFrame
        select_df_text = ttk.Label(self, text="Select DataFrame:", font=("Arial", 12))
        select_df_text.grid(row=1, column=0, padx=5, pady=(20, 5), sticky="w")

        self.df_dropdown = ttk.Combobox(self, state="readonly", values=self.df_names, width=30)
        self.df_dropdown.grid(row=1, column=0, padx=(250, 5), pady=(20, 5), sticky="w")
        self.df_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_df_selected())

        # Select Regression or Classification
        select_type_text = ttk.Label(self, text="Select Task Type:", font=("Arial", 12))
        select_type_text.grid(row=2, column=0, padx=5, pady=(15, 5), sticky="w")

        self.class_radio = ttk.Radiobutton(self, text="Classifiation", variable=self.type_var, 
            value="class", state="disabled", command=self.on_type_selected)
        self.class_radio.grid(row=2, column=0, padx=(250,5), pady=(15,5), sticky="w")                                    
        
        self.reg_radio = ttk.Radiobutton(self, text="Regression", variable=self.type_var, 
            value="reg", state="disabled", command=self.on_type_selected)
        self.reg_radio.grid(row=2, column=0, padx=(375,5), pady=(15,5), sticky="w")  

        # Select Target Feature
        select_target_text = ttk.Label(self, text="Select Target Feature:", font=("Arial", 12))
        select_target_text.grid(row=3, column=0, padx=5, pady=(15, 5), sticky="w")

        self.target_dropdown = ttk.Combobox(self, state="disabled", width=30)
        self.target_dropdown.grid(row=3, column=0, padx=(250, 5), pady=(15, 5), sticky="w")
        self.target_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_target_selected())

        # Select Input Features
        select_input_text = ttk.Label(self, text="Select Input Features:", font=("Arial", 12))
        select_input_text.grid(row=4, column=0, padx=5, pady=(10, 5), sticky="w")

        self.input_listbox = tk.Listbox(self, selectmode="extended", exportselection=False, height=10, width=30)
        self.input_listbox.grid(row=4, column=0, padx=(250,5), pady=(10,5), sticky="w")
        self.input_listbox.bind("<<ListboxSelect>>", lambda e: self.on_input_selected())

        self.all_checkbox = ttk.Checkbutton(
            self, state="disabled", text="Select All Features", variable=self.all_feats, command=self.on_all_selected)
        self.all_checkbox.grid(row=5, column=0, padx=(300,5), pady=(5,5), sticky="w")

        instruction_label = ttk.Label(
            self,
            text="Hold Ctlrl key and Click to select multiple features at once or Hold Shift key and Click to select a range of features",
            font=("Arial", 8)
        )
        instruction_label.grid(row=6, column=0, padx=5, pady=(5, 5), sticky="n")

        # Select Model
        select_model_text = ttk.Label(self, text="Select ML Model:", font=("Arial", 12))
        select_model_text.grid(row=7, column=0, padx=5, pady=(10, 5), sticky="w")

        self.model_dropdown = ttk.Combobox(self, state="disabled", width=30)
        self.model_dropdown.grid(row=7, column=0, padx=(250,5), pady=(10,5), sticky="w")
        self.model_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_model_selected())

        self.grid_columnconfigure(0, weight=1)

    def on_df_selected(self):
        self.manager.params.clear()

        self.df_name = self.df_dropdown.get()
        self.df = self.winfo_toplevel().SessionData.getDataFrame(self.df_name)

        self.type_var.set("")

        self.target_dropdown.set("")
        self.target_dropdown.config(state="disabled",values=[])

        self.input_listbox.delete(0, tk.END)
        self.input_listbox.config(state="disabled")

        self.all_feats.set(False)
        self.all_checkbox.config(state="disabled")

        self.model_dropdown.set("")
        self.model_dropdown.config(state="disabled", values=[])

        if self.df is not None:
            self.manager.params["df"] = self.df_name
            self.class_radio.config(state="enabled")
            self.reg_radio.config(state="enabled")

    def on_type_selected(self):
        self.tech = self.type_var.get()
        if self.tech == "reg":
            self.features = [feature for feature in self.df.columns if is_numeric_dtype(self.df[feature])]
        elif self.tech == "class": # allow all, have to consider encoded vars
            self.features = list(self.df.columns)
        
        self.target_dropdown.config(state="readonly", values=self.features)
        self.target_dropdown.set("")
        self.manager.params["tech"] = self.tech

        self.input_listbox.delete(0, tk.END)
        self.input_listbox.config(state="disabled")

        self.all_feats.set(False)
        self.all_checkbox.config(state="disabled")

        self.model_dropdown.set("")
        self.model_dropdown.config(state="disabled", values=[])

    def on_target_selected(self):
        self.target = self.target_dropdown.get()
        self.manager.params["target"] = self.target

        input_features = [feat for feat in self.features if feat != self.target]

        self.input_listbox.config(state="normal")
        self.input_listbox.delete(0, tk.END)
        for feat in input_features:
            self.input_listbox.insert(tk.END, feat)

        self.all_feats.set(False)
        self.all_checkbox.config(state="normal")
        self.model_dropdown.set("")
        self.model_dropdown.config(state="disabled", values=[])

    def on_input_selected(self):
        selected_indices = self.input_listbox.curselection()
        inputs = [self.input_listbox.get(i) for i in selected_indices]
        self.manager.params["inputs"] = inputs
        
        self.all_feats.set(False)
       
        self.determine_models()

    def on_all_selected(self):
        self.input_listbox.select_clear(0, tk.END)

        if self.all_feats.get():
            self.input_listbox.select_set(0, tk.END)
            self.manager.params["inputs"] = list(self.input_listbox.get(0, tk.END))
            self.determine_models()
        else:
            self.manager.params["inputs"] = []
            self.model_dropdown.set("")
            self.model_dropdown.config(state="disabled", values=[])

    def determine_models(self):
        inputs = self.manager.params["inputs"]

        all_numeric = all(is_numeric_dtype(self.df[col]) for col in inputs)

        available_models = []

        if self.tech == "reg":
            if all_numeric:
                available_models = [
                    "LinearRegression", "Ridge", "Lasso", "ElasticNet",
                    "DecisionTreeRegressor", "RandomForestRegressor",
                    "SVR", "KNeighborsRegressor"
                ]
        elif self.tech == "class":
            if all_numeric:
                available_models = [
                    "LogisticRegression", "KNeighborsClassifier",
                    "DecisionTreeClassifier", "RandomForestClassifier",
                    "SVC", "GaussianNB"
                ]
            else:
                available_models = [
                    "DecisionTreeClassifier", "RandomForestClassifier", "CategoricalNB"
                ]

        self.model_dropdown.config(state="readonly", values=available_models)
        self.model_dropdown.set("")

    def on_model_selected(self):
        model = self.model_dropdown.get()
        self.manager.params["model"] = model
        self.manager.next_btn.config(state="normal")
