from tkinter import ttk

from components.Patterns.operation_tabs import OperationTabFrame
from components.Patterns.generate_frame import GenerateCodeFrame
from components.Patterns.sequential_frames import SequentialFrameManager

from components.Import.id_frame import IDFrame
from components.EDA.eda_frame import EDATabFrame
from components.Cleaning.dc_frame import DCTabFrame
from components.FeatEng.fe_frame import FETabFrame
from components.Training.mt_frame import MTFrames
from components.Eval.me_frames import METabFrame
from components.Intro.intro_frame import IntroFrame


class MainStage(ttk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.tab_text = None
        self.frame = None
        self.frame_mapping = {
            "Import Dataset": IDFrame,
            "Data Analysis (EDA)": EDATabFrame,
            "Data Cleaning": DCTabFrame, 
            "Feature Engineering": FETabFrame, 
            "Model Training": MTFrames,
            "Model Evaluation": METabFrame
        }

        self.intro_frame = IntroFrame(self)
        self.intro_frame.grid(row=0, column=0, sticky="n")
        self.grid_columnconfigure(0, weight=1)

    def load_frame(self, tab_text):
        if tab_text in self.frame_mapping:
            for widget in self.winfo_children():
                widget.destroy()
            self.tab_text = tab_text
            frame_class = self.frame_mapping[tab_text]
            self.frame = frame_class(self)
            self.frame.pack(fill="both", expand=True)
            self.winfo_toplevel().SessionData.setAboutStep(tab_text)

    def refresh_children(self):
        if not self.tab_text:
            return

        if isinstance(self.frame, OperationTabFrame):
            self.frame.refresh_children()

        elif isinstance(self.frame, (SequentialFrameManager, GenerateCodeFrame)):
            self.load_frame(self.tab_text)

