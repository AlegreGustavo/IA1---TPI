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

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TPI - Inteligencia Artificial 1")
        self.setGeometry(100, 100, 1200, 620)

        #self.button = QPushButton('Agregar Estado', self)
        #self.button.setGeometry(250, 350, 100, 30)
        #self.button.clicked.connect(self.agregarCirculo)

        #Los estados que conformará el árbol generado
        self.estados = []
        
        self.setGui()
        
    def setGui(self):
        ########################################
        #
        #   COLORES
        #
        ########################################
        qBVerde = QBrush(Qt.green)
        qBAzul = QBrush(Qt.blue)
        qBAmarillo = QBrush(Qt.yellow)
        qBRojo = QBrush(Qt.red)

        ########################################
        #
        #   BORDES
        #
        ########################################
        blackPen = QPen(Qt.black)
        blackPen.setWidth(5)
        
        
        ########################################
        #
        #   ESCENA DERECHA (RESULTADOS)
        #
        ########################################
        
        #############################################################
        # 
        #
        # Escena que corresponde al algoritmo de Escalada Simple:
        #
        #
        #
        escenaResultados_EscaladaSimple = QGraphicsScene(self)

        vistaEscaladaSimple = QGraphicsView(escenaResultados_EscaladaSimple, self)
        vistaEscaladaSimple.setGeometry(self.width() / 2, 0, self.width() / 2, self.height() / 2)
        vistaEscaladaSimple.setBackgroundBrush(qBVerde)
        
        qL_escaladaSimple = QLabel("<h1>Escalada Simple</h1>", parent=vistaEscaladaSimple)
        qL_escaladaSimple.move(10, 10)

        eR_escaladaSimpleLayout = QVBoxLayout()
        eR_escaladaSimpleLayout.addWidget(qL_escaladaSimple)
        
        vistaEscaladaSimple.setLayout(eR_escaladaSimpleLayout)
        
        ### 
        #
        # Vista que corresponde al grafo de la Escalada Simple:
        #
        ###
        vistaEscaladaSimpleGrafo = QGraphicsView(escenaResultados_EscaladaSimple, self)
        vistaEscaladaSimpleGrafo.setGeometry((self.width() / 2) + (self.width() / 4), 0, self.width() / 4, self.height() / 2)
        vistaEscaladaSimpleGrafo.setBackgroundBrush(qBRojo)
        
        vG_escaladaSimpleLayout = QVBoxLayout()
        
        centralWidgetEscaladaSimple = QWidget(vistaEscaladaSimpleGrafo)
        
        # Crear un nuevo canvas y agregarlo al layout vertical
        canvasEscaladaSimple = PlotCanvas(centralWidgetEscaladaSimple, width=50, height=40)
        
        # Crear un grafo aleatorio con Networkx
        G = nx.erdos_renyi_graph(5, 0.4)

        # Dibujar el grafo en el canvas
        pos = nx.spring_layout(G)
        nx.draw(G, pos, ax=canvasEscaladaSimple.axes, with_labels=True, nodelist=pos, node_color='skyblue', edge_color='black', node_size=500)
        canvasEscaladaSimple.draw()
        
        vG_escaladaSimpleLayout.addWidget(canvasEscaladaSimple)
        vistaEscaladaSimpleGrafo.setLayout(vG_escaladaSimpleLayout)
        ###
        
        ###
        #
        # Escena que corresponde al algoritmo de Máxima Pendiente:
        #
        escenaResultados_MaximaPendiente = QGraphicsScene(self)

        vistaMaximaPendiente = QGraphicsView(escenaResultados_MaximaPendiente, self)
        vistaMaximaPendiente.setGeometry(self.width() / 2, self.height() / 2, self.width() / 2, self.height() / 2)
        vistaMaximaPendiente.setBackgroundBrush(qBAmarillo)
        
        qL_maximaPendiente = QLabel("<h1>Máxima Pendiente</h1>", parent=vistaMaximaPendiente)
        qL_maximaPendiente.move(10, 10)

        eR_maximaPendienteLayout = QVBoxLayout()
        eR_maximaPendienteLayout.addWidget(qL_maximaPendiente)
        
        vistaMaximaPendiente.setLayout(eR_maximaPendienteLayout)
        
        ### Vista que corresponde al grafo de la Máxima Pendiente:###
        vistaMaximaPendienteGrafo = QGraphicsView(escenaResultados_MaximaPendiente, self)
        vistaMaximaPendienteGrafo.setGeometry((self.width() / 2) + (self.width() / 4), self.height() / 2, self.width() / 4, self.height() / 2)
        vistaMaximaPendienteGrafo.setBackgroundBrush(qBRojo)
        
        vG_maximaPendieteLayout = QVBoxLayout()
        
        centralWidgetMaximaPendiente = QWidget(vistaMaximaPendienteGrafo)
        
        # Crear un nuevo canvas y agregarlo al layout vertical
        canvasMaximaPendiente = PlotCanvas(centralWidgetMaximaPendiente, width=50, height=40)
        
        # Crear un grafo aleatorio con Networkx
        G = nx.erdos_renyi_graph(5, 0.4)

        # Dibujar el grafo en el canvas
        pos = nx.spring_layout(G)
        nx.draw(G, pos, ax=canvasMaximaPendiente.axes, with_labels=True, nodelist=pos, node_color='skyblue', edge_color='black', node_size=500)
        canvasMaximaPendiente.draw()
        
        vG_maximaPendieteLayout.addWidget(canvasMaximaPendiente)
        vistaMaximaPendienteGrafo.setLayout(vG_maximaPendieteLayout)
        ###

        ########################################
        #
        #   ESCENA IZQUIERDA (PROBLEMA)
        #
        ########################################
        
        #############################################################
        # 
        #
        # Escena que corresponde al Problema:
        #
        #
        #
        escenaProblema = QGraphicsScene(self)
        
        vistaProblema = QGraphicsView(escenaProblema, self)
        vistaProblema.setGeometry(0, 0, self.width() / 2, self.height() / 3)
        vistaProblema.setBackgroundBrush(qBAzul)
        
        qL_problema = QLabel("<h1>PROBLEMA</h1>", parent=vistaProblema)

        eP_problemaLayout = QVBoxLayout()
        eP_problemaLayout.addWidget(qL_problema)
        
        vistaProblema.setLayout(eP_problemaLayout)
        
        ### 
        #
        # Vista que corresponde al grafo que se ve en la escena del problema:
        ###
        vistaProblemaGrafo = QGraphicsView(escenaProblema, self)
        vistaProblemaGrafo.setGeometry(0, self.height() / 3, self.width() / 2, (self.height() / 3) + (self.height() / 3))
        vistaProblemaGrafo.setBackgroundBrush(qBRojo)
        
        vPG_problemaLayout = QVBoxLayout()
        
        centralWidget = QWidget(vistaProblemaGrafo)
        
        # Crear un nuevo canvas y agregarlo al layout vertical
        canvas = PlotCanvas(centralWidget, width=50, height=40)
        
        # Crear un grafo aleatorio con Networkx
        G = nx.erdos_renyi_graph(5, 0.4)

        # Dibujar el grafo en el canvas
        pos = nx.spring_layout(G)
        nx.draw(G, pos, ax=canvas.axes, with_labels=True, nodelist=pos, node_color='skyblue', edge_color='black', node_size=500)
        canvas.draw()
        
        vPG_problemaLayout.addWidget(canvas)
        vistaProblemaGrafo.setLayout(vPG_problemaLayout)
        ###



#Para dibujar los grafos:
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=50, height=50, dpi=100):
        self.fig, self.axes = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
    
    
# EJECUCIÓN DEL PROGRAMA:    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())