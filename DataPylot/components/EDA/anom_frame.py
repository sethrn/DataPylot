from components.Patterns.operation_tabs import OperationTabFrame
from components.EDA.anom_outlier_frame import OutlierFrame
from components.EDA.anom_miss_frame import MissingFrame

class AnomalyTabFrame(OperationTabFrame):
     def __init__(self, parent):
        super().__init__(parent)

        self.add_tab(OutlierFrame, "Detect Outliers")
        self.add_tab(MissingFrame, "Detect Missing Values")
