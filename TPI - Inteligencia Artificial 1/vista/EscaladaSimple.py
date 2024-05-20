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
from Estado import *

class EscaladaSimple(QGraphicsScene):
    def __init__(self, master):
        super().__init__()
        self.__master = master

        #Vistas dentro de la Escena:
        self.vistaEscaladaSimple = QGraphicsView(self, self.master)
        self.vistaEscaladaSimpleGrafo = QGraphicsView(self, self.master)
        
        #Layout Escalada Simple:
        self.eR_escaladaSimpleLayout = QVBoxLayout()
        self.vistaEscaladaSimple.setLayout(self.eR_escaladaSimpleLayout)      

        # Crear un layout vertical para el manejo del canvas
        self.vG_escaladaSimpleLayout = QVBoxLayout()
        self.centralWidget = QWidget(self.vistaEscaladaSimpleGrafo)

        self.vistaEscaladaSimpleGrafo.setLayout(self.vG_escaladaSimpleLayout)
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
        self.vistaEscaladaSimple.setGeometry(self.master.width() / 2, self.master.height() / 3, self.master.width() / 2, self.master.height() / 3)
        
        qL_escaladaSimple = QLabel("<h2>Escalada Simple</h2>", parent=self.vistaEscaladaSimple)
        qL_escaladaSimple.move(10, 10)

        self.eR_escaladaSimpleLayout.addWidget(qL_escaladaSimple)        
        ### 
        #
        # Vista que corresponde al grafo de la Escalada Simple:
        #
        ###
        self.vistaEscaladaSimpleGrafo.setGeometry((self.master.width() / 2) + (self.master.width() / 6), self.master.height() / 3, self.master.width() / 3, self.master.height() / 3)
        
        centralWidgetEscaladaSimple = QWidget(self.vistaEscaladaSimpleGrafo)
        
        # Crear un nuevo canvas y agregarlo al layout vertical
        self.canvas = PlotCanvas(centralWidgetEscaladaSimple, width=50, height=40)
                
        self.vG_escaladaSimpleLayout.addWidget(self.canvas)
        self.vistaEscaladaSimpleGrafo.setLayout(self.vG_escaladaSimpleLayout)
        ###
    
    def dibujarGrafo(self, grafo, pos):
        # Dibujar el grafo en el canvas
        nx.draw(grafo, pos, ax=self.canvas.axes, with_labels=True, nodelist=pos, node_color='skyblue', edge_color='black', node_size=500)
        self.canvas.draw()
        
    def visualizacion_arbol_paso_a_paso(self, grafoEscaladaSimple, nodos, i, posEscaladaSimple, nodoFinal, estado_menor_valor):
        self.limpiarCanvas()
        subgrafo = grafoEscaladaSimple.subgraph(nodos[:i+1])
        pos = dict(list(posEscaladaSimple.items())[:i+1])
        
        # Diccionario para asignar colores a los nodos
        colores = ['yellow' if node == next(iter(subgrafo.nodes())) else 'skyblue' for node in subgrafo.nodes()]
        
        # Si el nodoFinal no es igual al último nodo del subgrafo y el grafo es igual al grafoEscaladaSimple, el último nodo del subgrafo será ROJO
        if nodoFinal != list(grafoEscaladaSimple.nodes())[-1] and nx.is_isomorphic(subgrafo, grafoEscaladaSimple):
            # Variable para almacenar la posición donde se encontró estado_menor_valor
            indice_minimo_local = 0
            posicion_minimo_local = None

            # Recorrer el diccionario pos
            for nodo, posicion in pos.items():
                if nodo == estado_menor_valor.nombre:
                    posicion_minimo_local = posicion
                    colores[indice_minimo_local] = 'red'
                    break  # Salir del bucle una vez que se encuentre la primera coincidencia
                indice_minimo_local += 1
                
            # Si se encontró estado_menor_valor en el diccionario pos
            if posicion_minimo_local is not None:
                # Usar las coordenadas encontradas en posicion_minimo_local
                x_pos = posicion_minimo_local[0]
                y_pos = posicion_minimo_local[1] - 0.35
                
                if (min(pos.values(), key=lambda x: x[1])[1])>y_pos:
                    y_pos = min(pos.values(), key=lambda x: x[1])[1] - 0.15
                    
                # Agregar anotación
                plt.text(x_pos, y_pos, "Mínimo Local", fontsize=8, fontweight='bold', ha='center', va='center', bbox=dict(facecolor='white', edgecolor='white', pad=1))
    
        # Si el nodoFinal es igual al último nodo del subgrafo y el grafo es igual al grafoEscaladaSimple, el último nodo del subgrafo será VERDE
        if nodoFinal == list(grafoEscaladaSimple.nodes())[-1] and nx.is_isomorphic(subgrafo, grafoEscaladaSimple):
            colores[-1] = 'green'
            
            # Calcular la posición del texto
            x_pos = pos[list(subgrafo.nodes())[-1]][0]
            y_pos = min(pos.values(), key=lambda x: x[1])[1] - 0.40  # Ubicado abajo del todo
            # Agregar anotación
            plt.text(x_pos, y_pos, "Estado Objetivo", fontsize=8, fontweight='bold', ha='center', va='center', bbox=dict(facecolor='white', edgecolor='white', pad=1))

        nx.draw(subgrafo, pos, ax=self.canvas.axes, with_labels=True, nodelist=pos, node_color=colores, edge_color='black', node_size=500)
        plt.title("Escalada Simple (Paso {})".format(i+1))
        
        self.canvas.draw()
        
        plt.close(self.canvas.fig)  # Cerrar la figura después de dibujarla
        
    def limpiarCanvas(self):
        # Eliminar el gráfico existente si ya hay un canvas
        if self.canvas:
            self.vG_escaladaSimpleLayout.removeWidget(self.canvas)
            self.canvas.deleteLater()  # Eliminar el canvas antiguo

        # Crear un nuevo canvas y agregarlo al layout vertical
        self.canvas = PlotCanvas(self.centralWidget, width=5, height=4)
        self.vG_escaladaSimpleLayout.addWidget(self.canvas)