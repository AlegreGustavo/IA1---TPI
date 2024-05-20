#Para dibujar los grafos:
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#Para dibujar los grafos:
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=150, height=150, dpi=75):
        self.fig, self.axes = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)