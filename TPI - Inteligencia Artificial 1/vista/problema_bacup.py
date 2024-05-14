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
        self.vistaProblema = QGraphicsView(self, self.master)
        self.vistaProblemaGrafo = QGraphicsView(self, self.master)
        self.problemaWidget = QWidget()
        
        #Layout Escena Problema:
        self.eP_problemaLayout = QVBoxLayout()
        self.vistaProblema.setLayout(self.eP_problemaLayout)      

        # Crear un layout vertical para el manejo del canvas
        self.vPG_problemaLayout = QVBoxLayout()
        self.centralWidget = QWidget(self.vistaProblemaGrafo)

        self.vistaProblemaGrafo.setLayout(self.vPG_problemaLayout)
        ###
        
        # Sección "Agregar Estado", "Lista Estado" y "Conoce a"
        agregarEstado_listaEstado_conoceA_layout = QHBoxLayout()

        # Sección "Agregar Estado"
        agregar_estado_layout = QVBoxLayout()
        
        
        label_seccion_agregar_estado = QLabel("Agregar Estado:")
        label_nombre = QLabel("Nombre:")
        self.input_estado = QLineEdit()
        
        agregarEstado_nombre_layout = QHBoxLayout()
        agregarEstado_nombre_layout.addWidget(label_nombre)
        agregarEstado_nombre_layout.addWidget(self.input_estado)
        
        label_posicion_x = QLabel("Posición x:")
        self.input_posicion_x = QLineEdit()
        agregarEstado_posicionX_layout = QHBoxLayout()
        agregarEstado_posicionX_layout.addWidget(label_posicion_x)
        agregarEstado_posicionX_layout.addWidget(self.input_posicion_x)
        
        label_posicion_y = QLabel("Posición y:")
        self.input_posicion_y = QLineEdit()
        agregarEstado_posicionY_layout = QHBoxLayout()
        agregarEstado_posicionY_layout.addWidget(label_posicion_y)
        agregarEstado_posicionY_layout.addWidget(self.input_posicion_y)

        button_agregar_estado = QPushButton("Agregar")

        agregar_estado_layout.addWidget(label_seccion_agregar_estado)
        agregar_estado_layout.addLayout(agregarEstado_nombre_layout)
        agregar_estado_layout.addLayout(agregarEstado_posicionX_layout)
        agregar_estado_layout.addLayout(agregarEstado_posicionY_layout)

        agregar_estado_layout.addWidget(button_agregar_estado)
        button_agregar_estado.clicked.connect(master.agregarEstado(self.input_estado.text(), self.input_posicion_x.text(), self.input_posicion_y.text()))

        # Sección "Lista Estados"
        lista_estados_layout = QVBoxLayout()
        self.listaEstados_label = QLabel("Lista de Estados:")
        self.lista_estados = QListWidget()
        
        # RadioButtons de la sección "Lista Estados"
        self.listaEstados_esInicial_radioButton = QRadioButton("¿Es el Estado Inicial?")
        self.listaEstados_esFinal_radioButton = QRadioButton("¿Es el Estado Final?")
        
        lista_estados_layout.addWidget(self.listaEstados_label)
        lista_estados_layout.addWidget(self.lista_estados)
        lista_estados_layout.addWidget(self.listaEstados_esInicial_radioButton)
        lista_estados_layout.addWidget(self.listaEstados_esFinal_radioButton)

        # Sección "Conoce a:"
        conoce_a_layout = QVBoxLayout()
        self.conoce_a_label = QLabel("Conoce a:")
        self.conoce_a_list = QListWidget()
        
        # ComboBox de la sección "Conoce a:"
        self.conoce_a_ComboBox_label = QLabel("Agregar una relación con:")
        self.conoce_a_comboBox = QComboBox()
        self.conoce_a_comboBox.addItem("Estado 1")
        self.conoce_a_comboBox.addItem("Estado 2")
        
        conoce_a_layout.addWidget(self.conoce_a_label)
        conoce_a_layout.addWidget(self.conoce_a_list)
        conoce_a_layout.addWidget(self.conoce_a_ComboBox_label)
        conoce_a_layout.addWidget(self.conoce_a_comboBox)
        
        agregarEstado_listaEstado_conoceA_layout.addLayout(agregar_estado_layout)
        agregarEstado_listaEstado_conoceA_layout.addLayout(lista_estados_layout)
        agregarEstado_listaEstado_conoceA_layout.addLayout(conoce_a_layout)


        #Sección "Definir Heurística", "Dibujar grafo aleatorio" y "Paso a Paso"
        definirHeuristica_dibujarGrafoAleatorio_pasoAPaso_layout = QHBoxLayout()
        
        # Sección "Definir Heurística"
        definir_heuristica_layout = QVBoxLayout()
        self.heuristica_label = QLabel("Definir Heurística:")
        
        # ComboBox de la sección "Definir Heurística:"
        self.definirHeuristica_comboBox = QComboBox()
        self.definirHeuristica_comboBox.addItem("Distancia Línea Recta")
        self.definirHeuristica_comboBox.addItem("Distancia Manhatan")
        definir_heuristica_layout.addWidget(self.heuristica_label)
        definir_heuristica_layout.addWidget(self.definirHeuristica_comboBox)

        # Sección "Dibujar grafo aleatorio"
        dibujar_grafo_layout = QVBoxLayout()
        self.dibujar_grafo_label = QLabel("Dibujar grafo aleatorio")
        
        self.cantidadEstados_label = QLabel("Cantidad Estados:")
        self.cantidadEstados_input = QLineEdit()
        
        dibujarGrafoAleatorio_cantidadEstados_layout = QHBoxLayout()
        dibujarGrafoAleatorio_cantidadEstados_layout.addWidget(self.cantidadEstados_label)
        dibujarGrafoAleatorio_cantidadEstados_layout.addWidget(self.cantidadEstados_input)
        
        self.cantidadMaximaRelaciones = QLabel("Cantidad máxima de relaciones:")
        self.cantidadMaximaRelaciones_input = QLineEdit()
        
        dibujarGrafoAleatorio_cantidadRelaciones_layout = QHBoxLayout()
        dibujarGrafoAleatorio_cantidadRelaciones_layout.addWidget(self.cantidadMaximaRelaciones)
        dibujarGrafoAleatorio_cantidadRelaciones_layout.addWidget(self.cantidadMaximaRelaciones_input)
        
        self.dibujar_grafo_button = QPushButton("Dibujar grafo aleatorio")
        #self.dibujar_grafo_button.clicked.connect()
        
        dibujar_grafo_layout.addWidget(self.dibujar_grafo_label)
        dibujar_grafo_layout.addLayout(dibujarGrafoAleatorio_cantidadEstados_layout)
        dibujar_grafo_layout.addLayout(dibujarGrafoAleatorio_cantidadRelaciones_layout)
        dibujar_grafo_layout.addWidget(self.dibujar_grafo_button)

        # Sección "Paso a Paso"
        navigation_layout = QVBoxLayout()
        self.pasoAPaso_label = QLabel("Paso a paso:")
        
        self.anterior_button = QPushButton("Anterior")
        self.siguiente_button = QPushButton("Siguiente")
        
        pasoAPaso_layout = QHBoxLayout()
        pasoAPaso_layout.addWidget(self.anterior_button)
        pasoAPaso_layout.addWidget(self.siguiente_button)
        
        navigation_layout.addWidget(self.pasoAPaso_label)
        navigation_layout.addLayout(pasoAPaso_layout)
        
        definirHeuristica_dibujarGrafoAleatorio_pasoAPaso_layout.addLayout(definir_heuristica_layout)
        definirHeuristica_dibujarGrafoAleatorio_pasoAPaso_layout.addLayout(dibujar_grafo_layout)
        definirHeuristica_dibujarGrafoAleatorio_pasoAPaso_layout.addLayout(navigation_layout)

        # Agregar todas las secciones al diseño principal
        self.eP_problemaLayout.addLayout(agregarEstado_listaEstado_conoceA_layout)
        self.eP_problemaLayout.addLayout(definirHeuristica_dibujarGrafoAleatorio_pasoAPaso_layout)

        # Establecer el diseño principal en el layout de la vistaProblema
        self.vistaProblema.setLayout(self.eP_problemaLayout)
        
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
        self.vistaProblema.setGeometry(0, 0, self.master.width() / 2, self.master.height() / 2)
        
        ### 
        #
        # Vista que corresponde al grafo que se ve en la escena del problema:
        ###
        self.vistaProblemaGrafo.setGeometry(0, self.master.height() / 2, self.master.width() / 2, (self.master.height() / 3) + (self.master.height() / 2))
        
        # Crear un nuevo canvas y agregarlo al layout vertical
        self.canvas = PlotCanvas(self.centralWidget, width=50, height=40)
        
        self.vPG_problemaLayout.addWidget(self.canvas)
        
    def dibujarGrafo(self, grafo):
        pos = []
        # Dibujar el grafo en el canvas
        pos = nx.spring_layout(grafo)
        nx.draw(grafo, pos, ax=self.canvas.axes, with_labels=True, nodelist=pos, node_color='skyblue', edge_color='black', node_size=400)
        self.canvas.draw()
        
    def limpiarCanvas(self):
        # Eliminar el gráfico existente si ya hay un canvas
        if self.canvas:
            self.vPG_problemaLayout.removeWidget(self.canvas)
            self.canvas.deleteLater()  # Eliminar el canvas antiguo

        # Crear un nuevo canvas y agregarlo al layout vertical
        self.canvas = PlotCanvas(self.centralWidget, width=4, height=3)
        self.vPG_problemaLayout.addWidget(self.canvas)