import tkinter as tk
from tkinter import ttk

from components.Patterns.operation_tabs import OperationTabFrame
from components.EDA.stats_frame import StatsFrame
from components.EDA.plot_frames import PlotFrames
from components.EDA.anom_miss_frame import MissingFrame
from components.EDA.anom_outlier_frame import OutlierFrame
from components.EDA.corr_frame import CorrelationFrame

class EDATabFrame(OperationTabFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_tab(PlotFrames, "Visualizations")
        self.add_tab(StatsFrame, "Summary Statistics")
        self.add_tab(MissingFrame, "Detect Missing Values")
        self.add_tab(OutlierFrame, "Detect Outliers")
        self.add_tab(CorrelationFrame, "Detect Correlations")