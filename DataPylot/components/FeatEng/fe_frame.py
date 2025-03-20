import tkinter as tk
from tkinter import ttk

from components.Patterns.operation_tabs import OperationTabFrame
from components.FeatEng.scale_frame import ScaleFrames
from components.FeatEng.encode_frame import EncodingFrames
from components.FeatEng.bin_frame import BinFrame
from components.FeatEng.interact_frame import InteractionFrame


class FETabFrame(OperationTabFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_tab(ScaleFrames, "Scale Numeric Feature")
        self.add_tab(EncodingFrames, "Encode Feature")
        self.add_tab(BinFrame, "Bin Features")
        self.add_tab(InteractionFrame, "Create Interaction Term")