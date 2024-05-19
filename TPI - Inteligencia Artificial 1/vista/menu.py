import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGraphicsScene, QGraphicsView, QGraphicsItem, QWidget, QLineEdit, QListWidget, QComboBox, QRadioButton, QCheckBox
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
from PySide6.QtCore import Qt, QPoint

#Para crear y administrar los grafos:
import networkx as nx

class EscenaMenu(QGraphicsScene):
    def __init__(self, master):
        super().__init__()
        self.__master = master

        #Vistas dentro de la Escena:
        self.vistaMenu = QGraphicsView(self, self.master)
        self.problemaWidget = QWidget()
        
        #Layout Escena Problema:
        self.eP_problemaLayout = QVBoxLayout()
        self.vistaMenu.setLayout(self.eP_problemaLayout)
        
        # Layout General:
        menu_layout = QHBoxLayout()

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
        button_agregar_estado.clicked.connect(self.agregarEstado)

        agregar_estado_layout.addWidget(label_seccion_agregar_estado)
        agregar_estado_layout.addLayout(agregarEstado_nombre_layout)
        agregar_estado_layout.addLayout(agregarEstado_posicionX_layout)
        agregar_estado_layout.addLayout(agregarEstado_posicionY_layout)

        agregar_estado_layout.addWidget(button_agregar_estado)

        # Sección "Lista Estados"
        lista_estados_layout = QVBoxLayout()
        self.listaEstados_label = QLabel("Lista de Estados:")
        self.lista_estados = QListWidget()
        self.lista_estados.clicked.connect(self.actualizarListaConoceA)
        
        # RadioButtons de la sección "Lista Estados"
        self.listaEstados_esInicial_CheckBox = QCheckBox("¿Es el Estado Inicial?")
        self.listaEstados_esFinal_CheckBox = QCheckBox("¿Es el Estado Final?")
        self.listaEstados_esInicial_CheckBox.clicked.connect(self.establecerNodoInicial)
        self.listaEstados_esFinal_CheckBox.clicked.connect(self.establecerNodoFinal)
        self.btnConoceA_borrorEstado = QPushButton("Borrar Estado")
        self.btnConoceA_borrorEstado.clicked.connect(self.borrarEstado)
        
        lista_estados_layout.addWidget(self.listaEstados_label)
        lista_estados_layout.addWidget(self.lista_estados)
        lista_estados_layout.addWidget(self.listaEstados_esInicial_CheckBox)
        lista_estados_layout.addWidget(self.listaEstados_esFinal_CheckBox)
        lista_estados_layout.addWidget(self.btnConoceA_borrorEstado)

        # Sección "Conoce a:"
        conoce_a_layout = QVBoxLayout()
        self.conoce_a_label = QLabel("Conoce a:")
        self.conoce_a_list = QListWidget()
        
        # ComboBox de la sección "Conoce a" ("Agregar una relación con")
        self.conoce_a_ComboBox_label = QLabel("Agregar una relación con:")
        self.conoce_a_comboBox = QComboBox()
        self.btnConoceA_AgregarRelacion = QPushButton("Agregar Relación")
        self.btnConoceA_AgregarRelacion.clicked.connect(self.agregarRelacion)
        self.btnConoceA_quitarRelacion = QPushButton("Quitar Relación")
        self.btnConoceA_quitarRelacion.clicked.connect(self.quitarRelacion)
        
        conoce_a_layout.addWidget(self.conoce_a_label)
        conoce_a_layout.addWidget(self.conoce_a_list)
        conoce_a_layout.addWidget(self.btnConoceA_quitarRelacion)
        conoce_a_layout.addWidget(self.conoce_a_ComboBox_label)
        conoce_a_layout.addWidget(self.conoce_a_comboBox)
        conoce_a_layout.addWidget(self.btnConoceA_AgregarRelacion)
        
        # Sección "Definir Heurística"
        definir_heuristica_layout = QVBoxLayout()
        self.heuristica_label = QLabel("Definir Heurística:")
        
        # ComboBox de la sección "Definir Heurística:"
        self.definirHeuristica_comboBox = QComboBox()
        self.definirHeuristica_comboBox.addItem("Euclidea")
        self.definirHeuristica_comboBox.addItem("Manhhatan")
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
        
        #self.cantidadMaximaRelaciones = QLabel("Cantidad máxima de relaciones:")
        #self.cantidadMaximaRelaciones_input = QLineEdit()
        
        dibujarGrafoAleatorio_cantidadRelaciones_layout = QHBoxLayout()
        # dibujarGrafoAleatorio_cantidadRelaciones_layout.addWidget(self.cantidadMaximaRelaciones)
        # dibujarGrafoAleatorio_cantidadRelaciones_layout.addWidget(self.cantidadMaximaRelaciones_input)
        
        self.dibujar_grafo_button = QPushButton("Dibujar grafo aleatorio")
        self.dibujar_grafo_button.clicked.connect(self.dibujarGrafoAleatorio)
        
        dibujar_grafo_layout.addWidget(self.dibujar_grafo_label)
        dibujar_grafo_layout.addLayout(dibujarGrafoAleatorio_cantidadEstados_layout)
        dibujar_grafo_layout.addLayout(dibujarGrafoAleatorio_cantidadRelaciones_layout)
        dibujar_grafo_layout.addWidget(self.dibujar_grafo_button)

        # Sección "Paso a Paso"
        navigation_layout = QVBoxLayout()
        self.pasoAPaso_label = QLabel("Paso a paso:")
        
        self.maxima_button = QPushButton("Maxima")
        self.maxima_button.clicked.connect(self.master.siguiente_paso_maxima)     
        self.simple_button = QPushButton("Simple")
        self.simple_button.clicked.connect(self.master.siguiente_paso_simple)      
        
        pasoAPaso_layout = QHBoxLayout()
        pasoAPaso_layout.addWidget(self.maxima_button)
        pasoAPaso_layout.addWidget(self.simple_button)
        
        navigation_layout.addWidget(self.pasoAPaso_label)
        navigation_layout.addLayout(pasoAPaso_layout)
        
        # Agregar cada sección al layout principal:
        menu_layout.addLayout(agregar_estado_layout)
        menu_layout.addWidget(self.__master.crearSeparador())
        menu_layout.addLayout(lista_estados_layout)
        menu_layout.addWidget(self.__master.crearSeparador())
        menu_layout.addLayout(conoce_a_layout)
        menu_layout.addWidget(self.__master.crearSeparador())
        menu_layout.addLayout(definir_heuristica_layout)
        menu_layout.addWidget(self.__master.crearSeparador())
        menu_layout.addLayout(dibujar_grafo_layout)
        menu_layout.addWidget(self.__master.crearSeparador())
        menu_layout.addLayout(navigation_layout)

        # Agregar todas las secciones al diseño principal
        self.eP_problemaLayout.addLayout(menu_layout)

        # Establecer el diseño principal en el layout de la vistaMenu
        self.vistaMenu.setLayout(self.eP_problemaLayout)
        
        self.setGui()
        
    def agregarEstado(self):
        nombreEstado = self.input_estado.text()
        if nombreEstado == "":
            self.master.mostrarAlerta("Ingrese un nombre para el Estado, por favor")
        else:    
            if self.master.existeNombreEstado(nombreEstado):
                self.master.mostrarAlerta("El nombre del Estado ya existe. Por favor elige uno nuevo.")
            else:
                self.master.agregarEstado(nombreEstado, self.input_posicion_x.text(), self.input_posicion_y.text())
                self.master.dibujarGrafo()
        
    def actualizarListaEstados(self, estadosParaLista):
        self.lista_estados.clear()
        for estado in estadosParaLista:
            self.lista_estados.addItem(estado.nombre)
            
    def actualizarComboRelaciones(self, estadosParaCombo):
        self.conoce_a_comboBox.clear()
        for estado in estadosParaCombo:
            self.conoce_a_comboBox.addItem(estado.nombre)
            
    def dibujarGrafoAleatorio(self):
        cantidadEstados = self.cantidadEstados_input.text()
        # CONTROL: que la cantidad ingresada sea un número.
        if not cantidadEstados.isalnum():
            self.master.mostrarAlerta("La cantidad de Estados ingresada no es correcta. Por favor ingrese un número.")
        else:
            # CONTROL: que la cantidad ingresada sea mayor a cero.
            if int(cantidadEstados) == 0:
                self.master.mostrarAlerta("Por favor ingrese un número mayor a cero.")
            else:
                self.master.dibujarGrafoAleatorio(int(cantidadEstados))
        
    def actualizarListaConoceA(self):
        self.conoce_a_list.clear()
        relaciones = self.master.devolverRelaciones(self.lista_estados.currentItem().text())
        for estado in relaciones:
            self.conoce_a_list.addItem(estado.nombre)
        
        noConoce = self.master.devolverRelacionesNoConoce(self.lista_estados.currentItem().text())
        self.actualizarComboRelaciones(noConoce)
        
    def agregarRelacion(self):
        nombreEstado = self.lista_estados.currentItem().text()
        nombreRelacionAgregar = self.conoce_a_comboBox.currentText()
        self.master.agregarRelacionNombre(nombreEstado, nombreRelacionAgregar)
        
        # Actualizar tanto la lista como el combobox:
        self.actualizarListaConoceA()
        # Redibujar los grafos:
        self.master.dibujarGrafo()
        
    def quitarRelacion(self):
        nombreEstado = self.lista_estados.currentItem().text()
        nombreRelacionQuitar = self.conoce_a_list.currentItem().text()
        self.master.quitarRelacionNombre(nombreEstado, nombreRelacionQuitar)
        # Actualizar tanto la lista como el combobox:
        self.actualizarListaConoceA()
        # Redibujar los grafos:
        self.master.dibujarGrafo()
        
    def borrarEstado(self):
        nombreEstado = self.lista_estados.currentItem().text()
        self.master.borrarEstadoNombre(nombreEstado)
        #Actualiza Lista de Estados:
        item = self.lista_estados.findItems(nombreEstado, Qt.MatchExactly)[0]
        if item is not None:
            self.lista_estados.takeItem(self.lista_estados.row(item))
        # Actualizar tanto la lista como el combobox:
        self.actualizarListaConoceA()
        # Redibujar los grafos:
        self.master.dibujarGrafo()
            
    def heuristicaUsada(self):
        heuristica = self.definirHeuristica_comboBox.currentText()
        return heuristica
    
    def establecerNodoInicial(self):
        if self.lista_estados.currentItem() != None:
            nombre_estado = self.lista_estados.currentItem().text()
            if self.listaEstados_esInicial_CheckBox.isChecked():
                self.master.establecerNodoInicial(nombre_estado)
        else:
            self.master.mostrarAlerta("La puta que te parió, seleccioná un estado por favor.")
    
    def establecerNodoFinal(self):
        if self.lista_estados.currentItem() != None:
            nombre_estado = self.lista_estados.currentItem().text()
            if self.listaEstados_esFinal_CheckBox.isChecked():
                self.master.establecerNodoFinal(nombre_estado)
        else:
            self.master.mostrarAlerta("La puta que te parió, seleccioná un estado por favor.")
            
    @property
    def master(self):
        return self.__master
        
    @master.setter
    def master(self, master):
        self.__master = master
        
    def setGui(self):
        self.vistaMenu.setGeometry(0, 0, self.master.width(), self.master.height() / 3)