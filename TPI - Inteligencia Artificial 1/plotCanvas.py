#Para dibujar los grafos:
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

#Para dibujar los grafos:
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=50, height=50, dpi=100):
        self.fig, self.axes = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)