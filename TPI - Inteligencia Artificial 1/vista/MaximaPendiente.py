import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QGraphicsScene, QGraphicsView, QGraphicsItem, QWidget, QLineEdit
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
        
        self.cantPasos = 0
        self.cantNiveles = 0
        self.minimoLocal = "No"
        self.estadoObjetivo = "No"
        
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
        
        # Preguntas y sus correspondientes QLineEdit
        qL_seEncontroObjetivo = QLabel("¿Se encontró el estado objetivo?", parent=self.vistaMaximaPendiente)
        qL_seEncontroObjetivo.move(20, 60)
        self.qLE_seEncontroObjetivo = QLineEdit(parent=self.vistaMaximaPendiente)
        self.qLE_seEncontroObjetivo.setReadOnly(True)
        self.qLE_seEncontroObjetivo.move(250, 60)
        
        qL_seEncontroMinimoLocal = QLabel("¿Se encontró un mínimo local?", parent=self.vistaMaximaPendiente)
        qL_seEncontroMinimoLocal.move(20, 90)
        self.qLE_seEncontroMinimoLocal = QLineEdit(parent=self.vistaMaximaPendiente)
        self.qLE_seEncontroMinimoLocal.setReadOnly(True)
        self.qLE_seEncontroMinimoLocal.move(250, 90)
        
        qL_cantidadPasos = QLabel("Cantidad de Pasos:", parent=self.vistaMaximaPendiente)
        qL_cantidadPasos.move(20, 120)
        self.qLE_cantidadPasos = QLineEdit(parent=self.vistaMaximaPendiente)
        self.qLE_cantidadPasos.setReadOnly(True)
        self.qLE_cantidadPasos.move(250, 120)
        
        qL_cantidadNiveles = QLabel("Cantidad de Niveles:", parent=self.vistaMaximaPendiente)
        qL_cantidadNiveles.move(20, 150)
        self.qLE_cantidadNiveles = QLineEdit(parent=self.vistaMaximaPendiente)
        self.qLE_cantidadNiveles.setReadOnly(True)
        self.qLE_cantidadNiveles.move(250, 150)

        # Agregar los widgets al layout
        self.eR_maximaPendienteLayout.addWidget(qL_maximaPendiente)
        self.eR_maximaPendienteLayout.addWidget(qL_seEncontroObjetivo)
        self.eR_maximaPendienteLayout.addWidget(self.qLE_seEncontroObjetivo)
        self.eR_maximaPendienteLayout.addWidget(qL_seEncontroMinimoLocal)
        self.eR_maximaPendienteLayout.addWidget(self.qLE_seEncontroMinimoLocal)
        self.eR_maximaPendienteLayout.addWidget(qL_cantidadPasos)
        self.eR_maximaPendienteLayout.addWidget(self.qLE_cantidadPasos)
        self.eR_maximaPendienteLayout.addWidget(qL_cantidadNiveles)
        self.eR_maximaPendienteLayout.addWidget(self.qLE_cantidadNiveles)
        
        # Establecer el layout en la vista de Máxima Pendiente
        self.vistaMaximaPendiente.setLayout(self.eR_maximaPendienteLayout)
        
        ### Vista que corresponde al grafo de la Máxima Pendiente ###
        self.vistaMaximaPendienteGrafo.setGeometry((self.master.width() / 2) + (self.master.width() / 6), self.master.height() * 2 / 3, self.master.width() / 3, self.master.height() / 3)
        
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
        
    def visualizacion_arbol_paso_a_paso(self, grafoMaximaPendiente, nodos, i, posMaximaPendiente, nodoFinal, estado_menor_valor):
        self.limpiarCanvas()
        GenerarInforme = False
        subgrafo = grafoMaximaPendiente.subgraph(nodos[:i+1])
        pos = dict(list(posMaximaPendiente.items())[:i+1])
        
        # Diccionario para asignar colores a los nodos
        colores = ['yellow' if node == next(iter(subgrafo.nodes())) else 'skyblue' for node in subgrafo.nodes()]
        
        # Variables para almacenar posiciones de las anotaciones
        anotaciones = []

        # Si el nodoFinal no es igual al último nodo del grafo y el subgrafo es igual al grafoMaximaPendiente, el último nodo del subgrafo será ROJO
        if nodoFinal != list(grafoMaximaPendiente.nodes())[-1] and nx.is_isomorphic(subgrafo, grafoMaximaPendiente):
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
                y_pos = posicion_minimo_local[1] - 0.40
                
                if (min(pos.values(), key=lambda x: x[1])[1]) > y_pos:
                    y_pos = min(pos.values(), key=lambda x: x[1])[1] - 0.30
                
                # Agregar anotación
                anotaciones.append((x_pos, y_pos, "Mínimo Local"))
            
            self.minimoLocal = "Sí"
            GenerarInforme = True
            self.estadoObjetivo = "No"

        # Si el nodoFinal es igual al último nodo del grafo y el subgrafo es igual al grafoMaximaPendiente, el último nodo del subgrafo será VERDE
        if nodoFinal == list(grafoMaximaPendiente.nodes())[-1] and nx.is_isomorphic(subgrafo, grafoMaximaPendiente):
            colores[-1] = 'green'
            
            # Calcular la posición del texto
            x_pos = pos[list(subgrafo.nodes())[-1]][0]
            y_pos = min(pos.values(), key=lambda x: x[1])[1] - 0.40  # Ubicado abajo del todo
            # Agregar anotación
            anotaciones.append((x_pos, y_pos, "Estado Objetivo"))
        
            self.estadoObjetivo = "Sí"
            GenerarInforme = True
            self.minimoLocal = "No"

        nx.draw(subgrafo, pos, ax=self.canvas.axes, with_labels=True, nodelist=pos, node_color=colores, edge_color='black', node_size=500)
        
        # Ajustar los límites del gráfico para asegurar que las anotaciones sean visibles
        x_min = min(pos.values(), key=lambda x: x[0])[0] - 0.5
        x_max = max(pos.values(), key=lambda x: x[0])[0] + 0.5
        y_min = min(pos.values(), key=lambda x: x[1])[1] - 0.5
        y_max = max(pos.values(), key=lambda x: x[1])[1] + 0.5

        for (x, y, texto) in anotaciones:
            self.canvas.axes.text(x, y, texto, fontsize=8, fontweight='bold', ha='center', va='center', bbox=dict(facecolor='white', edgecolor='white', pad=1))
            if y < y_min:
                y_min = y - 0.5

        self.canvas.axes.set_xlim(x_min, x_max)
        self.canvas.axes.set_ylim(y_min, y_max)

        plt.title("Máxima Pendiente (Cantidad de Pasos: {})".format(i+1))
        self.cantPasos = format(i+1)
        
        ultimo_y_positivo = abs(list(pos.items())[-1][1][1]) + 1
        self.cantNiveles = ultimo_y_positivo
        
        # Agregar texto al pie de la figura
        plt.text(0.5, -0.1, f"Cantidad de Niveles: {ultimo_y_positivo}", fontsize=10, ha='center', transform=self.canvas.axes.transAxes)
        
        self.canvas.draw()
        
        if(GenerarInforme):
            self.actualizarValores()
        
        plt.close(self.canvas.fig)  # Cerrar la figura después de dibujarla

        
    def limpiarCanvas(self):
        # Eliminar el gráfico existente si ya hay un canvas
        if self.canvas:
            self.vG_maximaPendieteLayout.removeWidget(self.canvas)
            self.canvas.deleteLater()  # Eliminar el canvas antiguo

        # Crear un nuevo canvas y agregarlo al layout vertical
        self.canvas = PlotCanvas(self.centralWidget, width=5, height=4)
        self.vG_maximaPendieteLayout.addWidget(self.canvas)
    
    def actualizarValores(self):
        self.qLE_seEncontroObjetivo.setText(str(self.estadoObjetivo))
        self.qLE_seEncontroMinimoLocal.setText(str(self.minimoLocal))
        self.qLE_cantidadPasos.setText(str(self.cantPasos))
        self.qLE_cantidadNiveles.setText(str(self.cantNiveles))