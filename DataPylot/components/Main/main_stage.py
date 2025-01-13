from tkinter import ttk

from components.Import.id_frame import IDFrame
from components.EDA.eda_frame import EDATabFrame
from components.Cleaning.dc_frame import DCTabFrame
from components.FeatEng.fe_frame import FETabFrame
from components.Training.mt_frame import MTTabFrame
from components.Eval.me_frame import METabFrame


class MainStage(ttk.Frame):
    def __init__(self, app):
        super().__init__(app)

        self.frame_mapping = {
            "Import Dataset": IDFrame,
            "EDA": EDATabFrame,
            "Data Cleaning": DCTabFrame, 
            "Feature Engineering": FETabFrame, 
            "Model Training": MTTabFrame,
            "Model Evaulation": METabFrame
        }

        self.label = ttk.Label(
            self, 
            text="Welcome to DataPylot! To get started, navigate to Import Dataset", 
            font=("Arial", 16)
        )
        self.label.grid(row=0, column=0, pady=(250,5), sticky="n")
        self.grid_columnconfigure(0, weight=1)
        

    def load_frame(self, tab_txt):
        if tab_txt in self.frame_mapping:
            for widget in self.winfo_children():
                widget.destroy()
            frame_class = self.frame_mapping[tab_txt]
            frame = frame_class(self)
            frame.pack(fill="both", expand=True)
