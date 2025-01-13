import tkinter as tk
from tkinter import ttk

from components.Patterns.operation_tabs import OperationTabFrame
from components.EDA.stats_frame import StatsFrame
from components.EDA.vis_frame import VisualizationTabFrame
from components.EDA.anom_frame import AnomalyTabFrame
from components.EDA.corr_frame import CorrelationFrame

class EDATabFrame(OperationTabFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.add_tab(StatsFrame, "Summary Statistics")
        self.add_tab(VisualizationTabFrame, "Visualizations")
        self.add_tab(AnomalyTabFrame, "Detect Anomalies")
        self.add_tab(CorrelationFrame, "Detect Correlations")