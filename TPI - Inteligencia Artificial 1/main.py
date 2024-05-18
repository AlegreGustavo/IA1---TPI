######
#   TPI DE INTELIGENCIA ARTIFICIAL
#
#
#
#
######

import sys
import random
import math

from constantes import *

from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QPushButton, QLabel, QGraphicsScene, QGraphicsView, QGraphicsItem, QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
from PySide6.QtCore import Qt, QPoint

#Para crear y administrar los grafos:
import networkx as nx

import random

#Para dibujar los grafos:
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from plotCanvas import *

from vista.menu import *
from vista.problema import *
from vista.EscaladaSimple import *
from vista.MaximaPendiente import *
from vista.mensajeAlerta import *

from Estado import *

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TPI - Inteligencia Artificial 1")
        self.setGeometry(100, 100, 1200, 620)

        # Los estados que conformará el árbol generado
        self.estados = []
        # Estado INICIAL y FINAL:
        self.estadoInicial = None
        self.estadoFinal = None
        
        #Variables de Escala Simple para el Paso a Paso
        self.grafoEscaladaSimple = nx.Graph()  # Grafo vacío
        self.posEscaladaSimple = {}  # Diccionario vacío
        self.nodosEscaladaSimple = {}
        self.indiceSimple = -1
        
        #Variables de Máxima Pendiente para el Paso a Paso
        self.grafoMaximaPendiente = nx.Graph()  # Grafo vacío
        self.posMaximaPendiente = {}  # Diccionario vacío
        self.nodosMaximaPendiente = {}
        self.indiceMaxima = -1
        
        #Variables para estado y nodo Final
        self.estadoFinalSimple = None
        self.nodoFinalSimple = None
        self.estadoFinalMaxima = None
        self.nodoFinalMaxima = None
        
        ########################################
        #
        #   ESCENA SUPERIOR (MENÚ)
        #
        ########################################
        self.escenaMenu = EscenaMenu(self)
        
        ########################################
        #
        #   ESCENA IZQUIERDA (PROBLEMA)
        #
        ########################################
        self.escenaProblema = EscenaProblema(self)
        
        ########################################
        #
        #   ESCENA DERECHA (RESULTADOS)
        #
        ########################################
        self.escenaEscaladaSimple = EscaladaSimple(self)
        self.escenaMaximaPendiente = MaximaPendiente(self)
        
        #Mensaje de alerta:
        self.ventanaAlerta = MensajeAlerta()
        
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
        
        self.botonDibujarArbol = QPushButton('Dibujar Árbol', self)
        self.botonDibujarArbol.setGeometry(15, 220, 100, 50)
        self.botonDibujarArbol.clicked.connect(self.dibujarGrafoCargado)
        
        self.heuristica_label = QLabel("Heurística:", self)
        self.heuristica_label.setGeometry(15, 230, 150, 150)
        self.heuristica_list = QListWidget(self)
        self.heuristica_list.setGeometry(15, 315, 80, 250)
        self.estadoInicial_label = QLabel("Estado Inicial: ", self)
        self.estadoInicial_label.setGeometry(15, 250, 200,50)
        self.estadoFinal_label = QLabel("Estado Final: ", self)
        self.estadoFinal_label.setGeometry(15, 265, 200,50)
        
        
        # Botón de resolución:
        self.botonDibujarArbol = QPushButton('RESOLVER', self)
        self.botonDibujarArbol.setGeometry(150, 220, 100, 50)
        self.botonDibujarArbol.clicked.connect(self.dibujarGrafoCargado)
        
    def dibujarGrafoCargado(self):
        self.limpiarEscenas()
        self.limpiarEstados()
        
        #PRUEBA EJERCICIO PRÁCTICO
        #Estados creados de forma estática para probar el Algoritmo
        A = Estado("A", 45, (75, 75))
        B = Estado("B", 20, (75, 17.5))
        C = Estado("C", 50, (36, 12))
        D = Estado("D", 20, (55, 2))
        E = Estado("E", 35, (25, 15))
        F = Estado("F", 15, (53, 23))
        G = Estado("G", 00, (27.5, 25))
        H = Estado("H", 90, (75, 40))
        I = Estado("I", 15, (38, 33))
        J = Estado("J", 10, (45, 30))
        K = Estado("K", 90, (38, 43))
        
        self.estados = [A, B, C, D, E, F, G, H, I, J, K]

        #Relaciones entre nodos
        A.agregarRelacion(D)
        A.agregarRelacion(C)
        A.agregarRelacion(E)
        A.agregarRelacion(B)
        B.agregarRelacion(A)
        B.agregarRelacion(E)
        B.agregarRelacion(H)
        C.agregarRelacion(A)
        C.agregarRelacion(D)
        C.agregarRelacion(F)
        C.agregarRelacion(G)
        C.agregarRelacion(E)
        D.agregarRelacion(A)
        D.agregarRelacion(F)
        D.agregarRelacion(C)
        E.agregarRelacion(A)
        E.agregarRelacion(B)
        E.agregarRelacion(C)
        E.agregarRelacion(H)
        E.agregarRelacion(B)
        F.agregarRelacion(G)
        F.agregarRelacion(D)
        F.agregarRelacion(C)
        G.agregarRelacion(C)
        G.agregarRelacion(F)
        G.agregarRelacion(J)
        G.agregarRelacion(I)
        G.agregarRelacion(H)
        H.agregarRelacion(B)
        H.agregarRelacion(E)
        H.agregarRelacion(G)
        H.agregarRelacion(I)
        H.agregarRelacion(K)
        I.agregarRelacion(K)
        I.agregarRelacion(H)
        I.agregarRelacion(G)
        J.agregarRelacion(K)
        J.agregarRelacion(G)
        K.agregarRelacion(I)
        K.agregarRelacion(J)
        K.agregarRelacion(H)
        
        self.establecerNodoInicial(A.nombre)
        self.establecerNodoFinal(G.nombre)
        # Actualización de los estados de la lista:
        self.escenaMenu.actualizarListaEstados(self.estados)
        #Actualización de los estados en el combobox de relaciones:
        self.escenaMenu.actualizarComboRelaciones(self.estados)
        
        self.dibujarGrafo()
    
    def assign_positions(self, G, root_node, pos):
        queue = [(root_node, None, 0)]  # cola para el recorrido BFS
        x_offsets = {root_node: 0}  # diccionario para almacenar los desplazamientos horizontales de los nodos

        while queue:
            node, parent, level = queue.pop(0)
            if parent is None:  # Si es el nodo raíz
                pos[node] = (0, 0)  # Fijar la posición del nodo raíz en el centro
            else:
                pos[node] = (pos[parent][0] + x_offsets[node], -level)  # Posicionar en relación con el padre
            children = list(G.neighbors(node))
            num_children = len(children)
            if num_children > 0:
                child_x_offset = - (num_children - 1) / 2
                for child in children:
                    if child != parent:
                        queue.append((child, node, level + 1))
                        x_offsets[child] = child_x_offset
                        child_x_offset += 1

    def resolve_node_overlap(self, pos):
        """
        Resuelve el solapamiento de nodos ajustando las posiciones.
        """
        # Creamos un diccionario para rastrear las posiciones ya ocupadas
        occupied_positions = {}
        
        # Lista para mantener un seguimiento de los nodos que se han movido
        moved_nodes = set()
        
        for node, position in pos.items():
            # Si la posición ya está ocupada por otro nodo
            while position in occupied_positions:
                # Mover el nodo un paso a la derecha
                position = (position[0] + 1, position[1])
                # Marcar el nodo como movido
                moved_nodes.add(node)
            
            # Marcar la posición como ocupada por el nodo actual
            occupied_positions[position] = node
            
            # Actualizar la posición en el diccionario pos
            pos[node] = position
        
        return moved_nodes
    
    def construir_edges(self, solucion, grafoResultado):
        """
        Convierte el arreglo de la Solución Escalada Simple a su "forma edges"
        """
        edges = [] #(x, y)
        for estado in solucion:
            for edge in estado.relaciones:
                edges.append( (estado.nombre, edge.nombre) )
        # Obtener el primer valor de la lista de bordes y asignarlo a estadoInicial
        estadoInicial = edges[0][0]
        
        # Agregar bordes al grafo
        grafoResultado.add_edges_from(edges)
        
        # Crear un diccionario de posiciones predeterminadas con None para todos los nodos
        pos = {node: None for node in grafoResultado.nodes()}

        # Fijar la posición del nodo raíz en el centro
        pos[estadoInicial] = (0, 0)

        # Ejecutar el algoritmo para asignar posiciones
        self.assign_positions(grafoResultado, estadoInicial, pos)

        # Resolver el solapamiento de nodos
        self.resolve_node_overlap(pos)
        
        return pos
    
    def construirGrafoProblema(self):
        grafo = nx.Graph()
        for estado in self.estados:
            grafo.add_node(estado.nombre, h=estado.valor)
            # CONTROL: Si el estado no tiene relaciones.
            if estado.relaciones != []:
                for relacion in estado.relaciones:
                    grafo.add_edge(estado.nombre, relacion.nombre)

        return grafo
    
    def construirGrafoEscaladaSimple(self):
        grafoEscaladaSimple = nx.Graph()
        solucionEscaladaSimple = self.escaladaSimple(self.estados)
        #CONTROL: Que la solucion del algoritmo Escalada Simple tenga más de un estado (si no tiene relaciones no debería por qué construir sus edges)
        posEscaladaSimple = (0, 0)
        if len(solucionEscaladaSimple) > 1:
            posEscaladaSimple = self.construir_edges(solucionEscaladaSimple, grafoEscaladaSimple)
        self.grafoEscaladaSimple = grafoEscaladaSimple
        self.posEscaladaSimple = posEscaladaSimple
        self.nodosEscaladaSimple = list(self.grafoEscaladaSimple.nodes())
        self.indiceSimple = -1
        
        #Para agregar colores al paso a paso
        for nodo in grafoEscaladaSimple.nodes():
            if nodo == self.estadoFinalSimple.nombre: self.nodoFinalSimple = nodo
        
        return grafoEscaladaSimple, posEscaladaSimple    
    
    def construirGrafoMaximaPendiente(self):
        grafoMaximaPendiente = nx.Graph()
        solucionMaximaPendiente = self.maximaPendiente(self.estados)
        #CONTROL: Que la solucion del algoritmo Máxima Pendiente tenga más de un estado (si no tiene relaciones no debería por qué construir sus edges)
        posMaximaPendiente = (0, 0)
        if len(solucionMaximaPendiente) > 1:
            posMaximaPendiente = self.construir_edges(solucionMaximaPendiente, grafoMaximaPendiente)
        self.grafoMaximaPendiente = grafoMaximaPendiente
        self.posMaximaPendiente = posMaximaPendiente
        self.nodosMaximaPendiente = list(self.grafoMaximaPendiente.nodes())
        self.indiceMaxima = -1
        
        #Para agregar colores al paso a paso
        for nodo in grafoMaximaPendiente.nodes():
            if nodo == self.estadoFinalMaxima.nombre: self.nodoFinalMaxima = nodo
            
        return grafoMaximaPendiente, posMaximaPendiente
    
    def limpiarEscenas(self):
        #Limpiar canvas de las escenas:
        plt.close()
        self.escenaProblema.limpiarCanvas()
        self.escenaEscaladaSimple.limpiarCanvas()
        self.escenaMaximaPendiente.limpiarCanvas()
        
    def dibujarEscenas(self, grafo, grafoEscaladaSimple, grafoMaximaPendiente, posEscaladaSimple, posMaximaPendiente):
        # Dibujar el grafo en el canvas
        self.escenaProblema.dibujarGrafo(grafo)
        if grafoEscaladaSimple and posEscaladaSimple and grafoMaximaPendiente and posMaximaPendiente != None:
            self.escenaEscaladaSimple.dibujarGrafo(grafoEscaladaSimple, posEscaladaSimple)
            self.escenaMaximaPendiente.dibujarGrafo(grafoMaximaPendiente, posMaximaPendiente)  
        
    def dibujarGrafo(self):
        grafo = self.construirGrafoProblema()
        grafoEscaladaSimple = None
        grafoMaximaPendiente = None
        posEscaladaSimple = None
        posMaximaPendiente = None
        # CONTROL: si no hay estado inicial (¿Y tal vez final) no generará estas soluciones:
        if self.estadoInicial != None:
            grafoEscaladaSimple, posEscaladaSimple = self.construirGrafoEscaladaSimple()
            grafoMaximaPendiente, posMaximaPendiente = self.construirGrafoMaximaPendiente()
        self.limpiarEscenas()
        self.dibujarEscenas(grafo, grafoEscaladaSimple, grafoMaximaPendiente, posEscaladaSimple, posMaximaPendiente)
        self.actualizarDatosProblema()
        
    def siguiente_paso_simple(self):
        if self.indiceSimple < len(self.nodosEscaladaSimple) - 1:
            self.indiceSimple += 1
            self.escenaEscaladaSimple.visualizacion_arbol_paso_a_paso(self.grafoEscaladaSimple, self.nodosEscaladaSimple, self.indiceSimple, self.posEscaladaSimple, self.nodoFinalSimple)
    
    def siguiente_paso_maxima(self):
        if self.indiceMaxima < len(self.nodosMaximaPendiente) - 1:
            self.indiceMaxima += 1
            self.escenaMaximaPendiente.visualizacion_arbol_paso_a_paso(self.grafoMaximaPendiente, self.nodosMaximaPendiente, self.indiceMaxima, self.posMaximaPendiente, self.nodoFinalMaxima)
    
    def dibujarGrafoBacup_borrar(self):
        grafo = nx.Graph()
        grafoEscaladaSimple = nx.Graph()
        grafoMaximaPendiente = nx.Graph()
        posEscaladaSimple = []
        posMaximaPendiente = []
        
        for estado in self.estados:
            grafo.add_node(estado.nombre, h=estado.valor, node_color=estado.color)
            for relacion in estado.relaciones:
                grafo.add_edge(estado.nombre, relacion.nombre)
   
        solucionEscaladaSimple = self.escaladaSimple(self.estados)
        for estado in solucionEscaladaSimple:
            grafoEscaladaSimple.add_node(estado.nombre, h=estado.valor)
            for relacion in estado.relaciones:
                grafoEscaladaSimple.add_edge(estado.nombre, relacion.nombre)
        posEscaladaSimple = self.construir_edges(solucionEscaladaSimple, grafoEscaladaSimple)
        
        solucionMaximaPendiente = self.maximaPendiente(self.estados)
        for estado in solucionMaximaPendiente:
            grafoMaximaPendiente.add_node(estado.nombre, h=estado.valor)
            for relacion in estado.relaciones:
                grafoMaximaPendiente.add_edge(estado.nombre, relacion.nombre)
        posMaximaPendiente = self.construir_edges(solucionMaximaPendiente, grafoMaximaPendiente)
        
        #Limpiar canvas de las escenas:
        self.escenaProblema.limpiarCanvas()
        self.escenaEscaladaSimple.limpiarCanvas()
        self.escenaMaximaPendiente.limpiarCanvas()
        
        # Dibujar el grafo en el canvas
        self.escenaProblema.dibujarGrafo(grafo)
        self.escenaEscaladaSimple.dibujarGrafo(grafoEscaladaSimple, posEscaladaSimple)
        self.escenaMaximaPendiente.dibujarGrafo(grafoMaximaPendiente, posMaximaPendiente)

    #ESCALADA SIMPLE:
    def escaladaSimple(self, estadosBuscar):
        estadosSolucion = []        
        
        self.estadoFinalSimple = self.estadoFinal

        #Se definen estado inicial como el estado actual, antes de empezar el recorrido.
        estadoActual = self.estadoInicial

        #Los algoritmos no garantizan encontrar el resultado óptimo. Por lo que "solucionEncontrada" sirve
        # como "mejor resultado encontrado", que no tiene por qué ser igual al "Estado Final" = resultado óptimo.
        solucionEncontrada = estadoActual
        fin = False
        
        #Para construir el árbol solución:
        estadoAgregarSolucion = Estado(estadoActual.nombre, estadoActual.valor, estadoActual.posicion)
        estadosSolucion.append(estadoAgregarSolucion)
        
        while not fin and solucionEncontrada != self.estadoFinal:
            estadoNuevo = None
            #
            # Se obtiene un nuevo estado, pidiéndole al estadoActual que le pase, de sus hijos, el primero mejor que encuentre.
            # El algoritmo puede ser de "MINIMIZACIÓN" o "MAXIMIZACIÓN"
            #
            # La diferencia con Máxima Pendiente estaría acá. Mientras el Escalada Simple devuelve el "primero mejor" que encuentre
            # entre sus hijos, el de Máxima Pendiente buscará el "mejor" entre todos sus hijos, y devolverá ese estado/nodo
            #
            
            #ESCALADA SIMPLE
            relacionesOrdenadas = self.ordenarEstados(estadoActual.relaciones)
            for relacion in relacionesOrdenadas:
                if relacion.valor < estadoActual.valor:
                    estadoNuevo = relacion
                    relacionAgregarSolucion = Estado(relacion.nombre, relacion.valor, relacion.posicion)
                    estadoAgregarSolucion.agregarRelacion(relacionAgregarSolucion)
                    break
                else:
                    relacionAgregarSolucion = Estado(relacion.nombre, relacion.valor, relacion.posicion)
                    estadoAgregarSolucion.agregarRelacion(relacionAgregarSolucion)
                    
            # Si encuentra un estado hijo mejor, entra por el lado del True. Cambia el estado actual por ese nuevo encontrado, y lo
            # agrega al "caminoHecho" hasta el momento.
            if estadoNuevo != None:
                estadoActual = estadoNuevo
                estadoAgregarSolucion = Estado(estadoActual.nombre, estadoActual.valor, estadoActual.posicion)
                estadosSolucion.append(estadoAgregarSolucion)
                
            # Si no encuentra un estado hijo mejor, puede que haya llegado al final o se haya topado con una meseta u otro de esos casos
            # Por lo que solo se sale del While. La solución encontrada será el último estado en el que estaba.
            else:
                fin = True
            solucionEncontrada = estadoActual
        return estadosSolucion
    
    #MAXIMA PENDIENTE:
    def maximaPendiente(self, estadosBuscar):
        estadosSolucion = []
        self.estadoFinalMaxima = self.estadoFinal

        #Se definen estado inicial como el estado actual, antes de empezar el recorrido.
        estadoActual = self.estadoInicial

        #Los algoritmos no garantizan encontrar el resultado óptimo. Por lo que "solucionEncontrada" sirve
        # como "mejor resultado encontrado", que no tiene por qué ser igual al "Estado Final" = resultado óptimo.
        solucionEncontrada = estadoActual
        fin = False
        
        #Para construir el árbol solución:
        estadoAgregarSolucion = Estado(estadoActual.nombre, estadoActual.valor, estadoActual.posicion)
        estadosSolucion.append(estadoAgregarSolucion)

        while not fin and solucionEncontrada != self.estadoFinal:
            estadoNuevo = None
            #
            # Se obtiene un nuevo estado, pidiéndole al estadoActual que le pase, de sus hijos, el primero mejor que encuentre.
            # El algoritmo puede ser de "MINIMIZACIÓN" o "MAXIMIZACIÓN"
            #
            # La diferencia con Máxima Pendiente estaría acá. Mientras el Escalada Simple devuelve el "primero mejor" que encuentre
            # entre sus hijos, el de Máxima Pendiente buscará el "mejor" entre todos sus hijos, y devolverá ese estado/nodo
            #
            
            #MÁXIMA PENDIENTE
            sucesor = estadoActual.valor
            relacionesOrdenadas = self.ordenarEstados(estadoActual.relaciones)
            for relacion in relacionesOrdenadas:
                if relacion == self.estadoFinal:
                    relacionAgregarSolucion = Estado(relacion.nombre, relacion.valor, relacion.posicion)
                    estadoAgregarSolucion.agregarRelacion(relacionAgregarSolucion)
                    break
                if relacion.valor < estadoActual.valor and relacion.valor < sucesor:
                    estadoNuevo = relacion
                    sucesor = relacion.valor
                    relacionAgregarSolucion = Estado(relacion.nombre, relacion.valor, relacion.posicion)
                    if not self.enCamino(estadosSolucion, relacionAgregarSolucion):
                        estadoAgregarSolucion.agregarRelacion(relacionAgregarSolucion)
                else:
                    relacionAgregarSolucion = Estado(relacion.nombre, relacion.valor, relacion.posicion)
                    if not self.enCamino(estadosSolucion, relacionAgregarSolucion):
                        estadoAgregarSolucion.agregarRelacion(relacionAgregarSolucion)
                    
            # Si encuentra un estado hijo mejor, entra por el lado del True. Cambia el estado actual por ese nuevo encontrado, y lo
            # agrega al "caminoHecho" hasta el momento.
            if estadoNuevo != None:
                estadoActual = estadoNuevo
                estadoAgregarSolucion = Estado(estadoActual.nombre, estadoActual.valor, estadoActual.posicion)
                estadosSolucion.append(estadoAgregarSolucion)
                
            # Si no encuentra un estado hijo mejor, puede que haya llegado al final o se haya topado con una meseta u otro de esos casos
            # Por lo que solo se sale del While. La solución encontrada será el último estado en el que estaba.
            else:
                fin = True
            solucionEncontrada = estadoActual
        return estadosSolucion
    
    def enCamino(self, solucion, relacionEvaluar):
        """
        Función para evaluar si una relación ya fue recorrida. De esta forma, el árbol no creará conexiones múltiples a los nodos.
        """
        retorno = False
        
        for estado in solucion:
            for relacion in estado.relaciones:
                if relacion.nombre == relacionEvaluar.nombre:
                    retorno = True
        
        return retorno
        
    def ordenarEstados(self, relaciones):
        #Por ahora solo orden alfabético ascendente:
        estadosOrdenados = sorted(relaciones, key=lambda x: x.nombre.lower())
        return estadosOrdenados
    
    def crearSeparador(self):
        # Crear un separador vertical
        separador = QFrame()
        separador.setFrameShape(QFrame.VLine)
        separador.setFrameShadow(QFrame.Sunken)
        separador.setLineWidth(2)
        return separador
        
    def agregarEstado(self, nombre, x, y):
        #valor = self.calcularDistancia(x, y, estadoFinal.x, estadoFinal.y, metodoLinealManhattan)
        valor = random.randint(1, 99)
        pos = (x, y)
        estadoNuevo = Estado(nombre, valor, pos)
        self.estados.append(estadoNuevo)
        
        # Actualización de los estados de la lista:
        self.escenaMenu.actualizarListaEstados(self.estados)
        #Actualización de los estados en el combobox de relaciones:
        self.escenaMenu.actualizarComboRelaciones(self.estados)
        
    def calcularDistanciaEuclidea(a, b):
        """
        Args:
            a (int): punto a
            b (int): punto b

        Returns:
            int: el valor de la distancia Euclídea entre los puntos pasados.
        """
        # Desempaquetamos las coordenadas de los puntos a y b
        x1, y1 = a
        x2, y2 = b
        
        # Calculamos la distancia Euclídea
        distanciaEuclidea = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
        return distanciaEuclidea
    
    def calcularDistanciaManhattan(a, b):
        """
        Args:
            a (int): punto a
            b (int): punto b

        Returns:
            int: el valor de la distancia Manhattan entre los puntos pasados.
        """
        # Desempaquetamos las coordenadas de los puntos a y b
        x1, y1 = a
        x2, y2 = b
        
        # Calculamos la distancia Euclídea
        distanciaManhattan = abs(x2 - x1) + abs(y2 - y1)
        
        return distanciaManhattan 
    
    def establecerNodoInicial(self, nombreEstadoInicial):
        """
        Establece como nodo inicial al nodo con el nombre del estado pasado como @nombreEstadoInicial    
        """
        for estado in self.estados:
            if estado.nombre == nombreEstadoInicial:
                estado.establecerInicial()
                self.estadoInicial = estado
    
    def establecerNodoFinal(self, nombreEstadoFinal):
        """
        Establece como nodo final al nodo con el nombre del estado pasado como @nombreEstadoFinal     
        """
        for estado in self.estados:
            if estado.nombre == nombreEstadoFinal:
                estado.establecerFinal()
                self.estadoFinal = estado
    
    def quitarInicialFinal(self):
        """
        Elimina el nodo inicial y final de la lista de @self.estados.
        """
        for estado in self.estados:
            estado.establecerNormal()
        
    def limpiarEstados(self):
        self.estadoInicial = None
        self.estadoFinal = None
        self.estados = []
        
        #Variables de Escala Simple para el Paso a Paso
        self.grafoEscaladaSimple = nx.Graph()  # Grafo vacío
        self.posEscaladaSimple = {}  # Diccionario vacío
        self.nodosEscaladaSimple = {}
        self.indiceSimple = -1
        
        #Variables de Máxima Pendiente para el Paso a Paso
        self.grafoMaximaPendiente = nx.Graph()  # Grafo vacío
        self.posMaximaPendiente = {}  # Diccionario vacío
        self.nodosMaximaPendiente = {}
        self.indiceMaxima = -1
        
        #Variables para estado y nodo Final
        self.estadoFinalSimple = None
        self.nodoFinalSimple = None
        self.estadoFinalMaxima = None
        self.nodoFinalMaxima = None
        
    def devolverRelaciones(self, nombreEstado):
        relaciones = []
        for estado in self.estados:
            if estado.nombre == nombreEstado:
                relaciones = estado.relaciones
        return relaciones
    
    def devolverRelacionesNoConoce(self, nombreEstado):
        estadosNoConoce = []
        for estado in self.estados:
            if estado.nombre != nombreEstado:
                relaciones = self.devolverRelaciones(estado.nombre)
                conoce = False
                for relacion in relaciones:
                    if relacion.nombre == nombreEstado:
                        conoce = True
                if conoce == False:
                    estadosNoConoce.append(estado)
        return estadosNoConoce
        
    def dibujarGrafoAleatorio(self, cantidadEstados):
        self.limpiarEstados()
        self.limpiarEscenas()
        estadoAgregar = None
        i = 0
        while i < cantidadEstados:
            noRepetido = True
            # CONTROL: se me hace que acá hay un bucle infinito a veces. Quién sabe.
            while noRepetido:
                nombre = chr(random.randint(65, 90))    # Genera una letra aleatoria en mayúscula
                noRepetido = self.existeNombreEstado(nombre)
            valor = random.randint(1, 99)               # El valor será determinado con las funciones de Heurística
            x = random.randint(1, 99)
            y = random.randint(1, 99)
            estadoAgregar = Estado(nombre, valor, (x, y))
            i = i + 1
            self.estados.append(estadoAgregar)
        
        for estado in self.estados:
            # [:] es para hacer una copia del arreglo. Si no se hace así, se pasa el arreglo por referencia.
            listaEstadosAuxiliar = self.estados[:]      
            listaEstadosAuxiliar.remove(estado)
           
            # Quitar las relaciones del estado de la listaEstadosAuxiliar:
            for relacion in estado.relaciones:
                #CONTROL: solo verificar que no sea vacío:
                if relacion != None:
                    listaEstadosAuxiliar.remove(relacion)
            # CONTROL: solo que la listaEstadosAuxiliar no sea 0
            if len(listaEstadosAuxiliar) > 0:
                relacionesEstado = random.randint(1, len(listaEstadosAuxiliar))
                while len(estado.relaciones) < relacionesEstado:
                    posicionRandom = random.randint(0, len(listaEstadosAuxiliar)-1)
                    self.agregarRelacionNombre(listaEstadosAuxiliar[posicionRandom].nombre, estado.nombre)
                    listaEstadosAuxiliar.remove(listaEstadosAuxiliar[posicionRandom])
        
        estadoInicialAleatorio = self.estados[random.randint(0, len(self.estados)-1)]
        self.establecerNodoInicial(estadoInicialAleatorio.nombre)
        estadoFinalAleatorio = self.estados[random.randint(0, len(self.estados)-1)]
        self.establecerNodoFinal(estadoFinalAleatorio.nombre)        
        # Actualización de los estados de la lista:
        self.escenaMenu.actualizarListaEstados(self.estados)
        #Actualización de los estados en el combobox de relaciones:
        self.escenaMenu.actualizarComboRelaciones(self.estados)
        self.dibujarGrafo()
        
    def existeNombreEstado(self, nombre):
        """
        Función para verificar si el nombre pasado ya existe entre los estados presentes.
        Si el nombre del estado ya se encuentra, devuelve True; caso contrario, devuelve False.
        """
        retorno = False
        for estado in self.estados:
            if estado.nombre == nombre:
                retorno = True
        return retorno

    def agregarRelacionNombre(self, nombre, nombreRelacion):
        """
        Función que agrega la relación de dos estaos a partir de los nombres pasados. Primero busca los objetos del arreglo.
        Después, solo agrega la relación.
        """
        relacion = None
        for estado in self.estados:
            if estado.nombre == nombreRelacion:
                relacion = estado
        
        for estado in self.estados:
            if estado.nombre == nombre:
                estado.agregarRelacion(relacion)
                relacion.agregarRelacion(estado)
                
    def quitarRelacionNombre(self, nombre, nombreRelacionQuitar):
        """
        Función que quita la relación de dos estados a partir de los nombres pasados. Primero busca los objetos del arreglo de estados.
        Después, solo quita la relación.
        """
        relacion = None
        for estado in self.estados:
            if estado.nombre == nombreRelacionQuitar:
                relacion = estado
        
        for estado in self.estados:
            if estado.nombre == nombre:
                estado.quitarRelacion(relacion)
                relacion.quitarRelacion(estado)
                
    def actualizarDatosProblema(self):
        self.estadoInicial_label.setText("Estado Inicial: ")
        self.estadoFinal_label.setText("Estado Final: ")
        self.heuristica_list.clear()
        
        # CONTROL: verificando que exista el estado inicial:
        if self.estadoInicial != None:
            self.estadoInicial_label.setText(self.estadoInicial_label.text() + self.estadoInicial.nombre)
        if self.estadoFinal != None:
            self.estadoFinal_label.setText(self.estadoFinal_label.text() + self.estadoFinal.nombre)
        for estado in self.estados:
            if estado != None:
                self.heuristica_list.addItem(estado.nombre + ': ' + str(estado.valor))
                
    def mostrarAlerta(self, mensaje):
        self.ventanaAlerta.mostrarAlerta(mensaje)
    
# EJECUCIÓN DEL PROGRAMA:    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())