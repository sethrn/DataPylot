import tkinter as tk
from tkinter import ttk

from components.Cleaning.remove_frame import RemoveFeatureFrame
from components.Patterns.operation_tabs import OperationTabFrame
from components.Cleaning.missing_frame import MissingFrame
from components.Cleaning.outlier_frames import OutlierFrames
from components.Cleaning.rename_frames import RenameFrames

class DCTabFrame(OperationTabFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.add_tab(MissingFrame, "Handle Missing Values")
        self.add_tab(OutlierFrames, "Handle Numeric Outliers")
        self.add_tab(RenameFrames, "Rename Feature Values")
        self.add_tab(RemoveFeatureFrame, "Remove Features")