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

class MaximaPendiente(QGraphicsScene):
    def __init__(self, master):
        super().__init__()
        self.__master = master
        
        #Vistas dentro de la Escena:
        self.vistaMaximaPendiente = QGraphicsView(self, self.master)
        self.vistaMaximaPendienteGrafo = QGraphicsView(self, self.master)
        
        #Layout Maxima Pendiente:
        self.eR_maximaPendienteLayout = QVBoxLayout()
        self.vistaMaximaPendiente.setLayout(self.eR_maximaPendienteLayout)      

        # Crear un layout vertical para el manejo del canvas
        self.vG_maximaPendieteLayout = QVBoxLayout()
        self.centralWidget = QWidget(self.vistaMaximaPendienteGrafo)

        self.vistaMaximaPendienteGrafo.setLayout(self.vG_maximaPendieteLayout)
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
        self.vistaMaximaPendiente.setGeometry(self.master.width() / 2, self.master.height() * 2 / 3, self.master.width() / 2, self.master.height() / 3)
        
        qL_maximaPendiente = QLabel("<h2>Máxima Pendiente</h2>", parent=self.vistaMaximaPendiente)
        qL_maximaPendiente.move(10, 10)

        self.eR_maximaPendienteLayout.addWidget(qL_maximaPendiente)
        
        self.vistaMaximaPendiente.setLayout(self.eR_maximaPendienteLayout)
        
        ### Vista que corresponde al grafo de la Máxima Pendiente:###
        self.vistaMaximaPendienteGrafo.setGeometry((self.master.width() / 2) + (self.master.width() / 6), self.master.height() * 2 / 3, self.master.width() / 3, self.master.height() /3 )
        
        centralWidgetMaximaPendiente = QWidget(self.vistaMaximaPendienteGrafo)
        
        # Crear un nuevo canvas y agregarlo al layout vertical
        self.canvas = PlotCanvas(centralWidgetMaximaPendiente, width=50, height=40)
        
        self.vG_maximaPendieteLayout.addWidget(self.canvas)
        self.vistaMaximaPendienteGrafo.setLayout(self.vG_maximaPendieteLayout)
        ###
    
    def dibujarGrafo(self, grafo, pos):
        # Dibujar el grafo en el canvas
        nx.draw(grafo, pos, ax=self.canvas.axes, with_labels=True, nodelist=pos, node_color='skyblue', edge_color='black', node_size=500)
        self.canvas.draw()
        
    def visualizacion_arbol_paso_a_paso(self, grafoMaximaPendiente, nodos, i, posMaximaPendiete, nodoFinal):
        self.limpiarCanvas()
        subgrafo = grafoMaximaPendiente.subgraph(nodos[:i+1])
        pos = dict(list(posMaximaPendiete.items())[:i+1])
        
        # Diccionario para asignar colores a los nodos
        colores = ['yellow' if node == next(iter(subgrafo.nodes())) else 'skyblue' for node in subgrafo.nodes()]
        # Si el nodoFinal no es igual al último nodo del rafo y el subgrafo es igual al grafoEscaladaSimple, el último nodo del subgrafo será ROJO
        if nodoFinal != list(grafoMaximaPendiente.nodes())[-1] and nx.is_isomorphic(subgrafo, grafoMaximaPendiente):
            colores[-1] = 'red'
            
            # Calcular la posición del texto
            x_pos = pos[list(subgrafo.nodes())[-1]][0]
            y_pos = min(pos.values(), key=lambda x: x[1])[1] - 0.35  # Ubicado abajo del todo
            # Agregar anotación
            plt.text(x_pos, y_pos, "Mínimo Local", fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.3))
            
        # Si el nodoFinal es igual al último nodo del grafo y el subgrafo es igual al grafoEscaladaSimple, el último nodo del subgrafo será VERDE
        if nodoFinal == list(grafoMaximaPendiente.nodes())[-1] and nx.is_isomorphic(subgrafo, grafoMaximaPendiente):
            colores[-1] = 'green'
            
            # Calcular la posición del texto
            x_pos = pos[list(subgrafo.nodes())[-1]][0]
            y_pos = min(pos.values(), key=lambda x: x[1])[1] - 0.35  # Ubicado abajo del todo
            # Agregar anotación
            plt.text(x_pos, y_pos, "Estado Objetivo", fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.3))
        
        nx.draw(subgrafo, pos, ax=self.canvas.axes, with_labels=True, nodelist=pos, node_color=colores, edge_color='black', node_size=500)
        plt.title("Máxima Pendiente (Paso {})".format(i+1))
        self.canvas.draw()
        
        plt.close(self.canvas.fig)  # Cerrar la figura después de dibujarla
        
    def limpiarCanvas(self):
        # Eliminar el gráfico existente si ya hay un canvas
        if self.canvas:
            self.vG_maximaPendieteLayout.removeWidget(self.canvas)
            self.canvas.deleteLater()  # Eliminar el canvas antiguo

        # Crear un nuevo canvas y agregarlo al layout vertical
        self.canvas = PlotCanvas(self.centralWidget, width=5, height=4)
        self.vG_maximaPendieteLayout.addWidget(self.canvas)