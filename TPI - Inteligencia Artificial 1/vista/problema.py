import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGraphicsScene, QGraphicsView, QGraphicsItem, QWidget, QLineEdit, QListWidget, QComboBox, QRadioButton
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
from PySide6.QtCore import Qt, QPoint

#Para crear y administrar los grafos:
import networkx as nx

#Para dibujar los grafos:
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from plotCanvas import *

class EscenaProblema(QGraphicsScene):
    def __init__(self, master):
        super().__init__()
        self.__master = master

        #Vistas dentro de la Escena:
        self.vistaProblemaGrafo = QGraphicsView(self, self.master)

        # Crear un layout vertical para el manejo del canvas
        self.vPG_problemaLayout = QVBoxLayout()
        self.centralWidget = QWidget(self.vistaProblemaGrafo)

        self.vistaProblemaGrafo.setLayout(self.vPG_problemaLayout)
        ###
        
        #CANVAS para dibujar los gráficos:
        self.canvas = None
        self.pos = []
        
        self.setGui()
        
    @property
    def master(self):
        return self.__master
        
    @master.setter
    def master(self, master):
        self.__master = master
        
    def setGui(self):
        ### 
        #
        # Vista que corresponde al grafo que se ve en la escena del problema:
        ###
        self.vistaProblemaGrafo.setGeometry(150, self.master.height() / 3, self.master.width() / 2 - 150, self.master.height() * 2 / 3)
        
        # Crear un nuevo canvas y agregarlo al layout vertical
        self.canvas = PlotCanvas(self.centralWidget, width=50, height=40)
        
        self.vPG_problemaLayout.addWidget(self.canvas)
        
    def dibujarGrafo(self, grafo):
        """
        Dibujar el grafo en el canvas
        """
        if self.pos == []:
            self.pos = nx.spring_layout(grafo)
        nx.draw(grafo, self.pos, ax=self.canvas.axes, with_labels=True, nodelist=self.pos, node_color='skyblue', edge_color='black', node_size=400)
        self.canvas.draw()
        
    def limpiarCanvas(self):
        """
        Eliminar el gráfico existente si ya hay un canvas
        """
        if self.canvas:
            self.vPG_problemaLayout.removeWidget(self.canvas)
            self.canvas.deleteLater()  # Eliminar el canvas antiguo

        # Crear un nuevo canvas y agregarlo al layout vertical
        self.canvas = PlotCanvas(self.centralWidget, width=4, height=3)
        self.vPG_problemaLayout.addWidget(self.canvas)