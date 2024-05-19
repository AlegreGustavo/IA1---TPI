import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QGraphicsScene, QGraphicsView, QGraphicsItem, QWidget
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
        self.vistaProblema = QGraphicsView(self, self.master)
        self.vistaProblemaGrafo = QGraphicsView(self, self.master)
        
        #Layout Escena Problema:
        self.eP_problemaLayout = QVBoxLayout()
        self.vistaProblema.setLayout(self.eP_problemaLayout)      

        # Crear un layout vertical para el manejo del canvas
        self.vPG_problemaLayout = QVBoxLayout()
        self.centralWidget = QWidget(self.vistaProblemaGrafo)

        self.vistaProblemaGrafo.setLayout(self.vPG_problemaLayout)
        ###
        
        #CANVAS para dibujar los gráficos:
        self.canvas = None
        
        self.setGui()
        
    @property
    def master(self):
        return self.__master
        
    @master.setter
    def master(self, master):
        self.__master = master
        
    def setGui(self):
        self.vistaProblema.setGeometry(0, 0, self.master.width() / 2, self.master.height() / 3)
        
        qL_problema = QLabel("<h1>PROBLEMA</h1>", parent=self.vistaProblema)
        self.eP_problemaLayout.addWidget(qL_problema)
        
        
        
        ### 
        #
        # Vista que corresponde al grafo que se ve en la escena del problema:
        ###
        self.vistaProblemaGrafo.setGeometry(0, self.master.height() / 3, self.master.width() / 2, (self.master.height() / 3) + (self.master.height() / 3))
        
        # Crear un nuevo canvas y agregarlo al layout vertical
        self.canvas = PlotCanvas(self.centralWidget, width=50, height=40)
        
        self.vPG_problemaLayout.addWidget(self.canvas)
        
    def dibujarGrafo(self, grafo):
        pos = []
        # Dibujar el grafo en el canvas
        pos = nx.spring_layout(grafo)
        nx.draw(grafo, pos, ax=self.canvas.axes, with_labels=True, nodelist=pos, node_color='skyblue', edge_color='black', node_size=500)
        self.canvas.draw()
        
    def limpiarCanvas(self):
        # Eliminar el gráfico existente si ya hay un canvas
        if self.canvas:
            self.vPG_problemaLayout.removeWidget(self.canvas)
            self.canvas.deleteLater()  # Eliminar el canvas antiguo

        # Crear un nuevo canvas y agregarlo al layout vertical
        self.canvas = PlotCanvas(self.centralWidget, width=5, height=4)
        self.vPG_problemaLayout.addWidget(self.canvas)