from components.Patterns.operation_tabs import OperationTabFrame
from components.EDA.vis_uni_frames import UnivariateFrames
from components.EDA.vis_bi_frames import BivariateFrames
from components.EDA.vis_multi_frames import MultivariateFrames

class VisualizationTabFrame(OperationTabFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_tab(UnivariateFrames, "Univariate")
        self.add_tab(BivariateFrames, "Bivariate")
        self.add_tab(MultivariateFrames, "Multivariate")