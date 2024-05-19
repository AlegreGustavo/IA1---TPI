from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QPushButton, QLabel, QLineEdit, QListWidget, QComboBox, QRadioButton
from PySide6.QtWidgets import QCheckBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Widget principal y diseño
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Sección "Agregar Estado", "Lista Estado" y "Conoce a"
        agregarEstado_listaEstado_conoceA_layout = QHBoxLayout()

        # Sección "Agregar Estado"
        agregar_estado_layout = QVBoxLayout()
        
        
        label_seccion_agregar_estado = QLabel("Agregar Estado:")
        label_nombre = QLabel("Nombre:")
        self.input_estado = QLineEdit()
        
        label_posicion_x = QLabel("Posición x:")
        self.input_posicion_x = QLineEdit()
        
        label_posicion_y = QLabel("Posición y:")
        self.input_posicion_y = QLineEdit()

        button_agregar_estado = QPushButton("Agregar")

        agregar_estado_layout.addWidget(label_seccion_agregar_estado)
        agregar_estado_layout.addWidget(label_nombre)
        agregar_estado_layout.addWidget(self.input_estado)
        
        agregar_estado_layout.addWidget(label_posicion_x)
        agregar_estado_layout.addWidget(self.input_posicion_x)
        
        agregar_estado_layout.addWidget(label_posicion_y)
        agregar_estado_layout.addWidget(self.input_posicion_y)

        agregar_estado_layout.addWidget(button_agregar_estado)

        # Sección "Lista Estados"
        lista_estados_layout = QVBoxLayout()
        self.listaEstados_label = QLabel("Lista de Estados:")
        self.lista_estados = QListWidget()
        
        # RadioButtons de la sección "Lista Estados"
        self.listaEstados_esInicial_radioButton = QRadioButton("¿Es el Estado Inicial?", self)
        self.listaEstados_esFinal_radioButton = QRadioButton("¿Es el Estado Final?", self)
        
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
        
        self.cantidadMaximaRelaciones = QLabel("Cantidad máxima de relaciones:")
        self.cantidadMaximaRelaciones_input = QLineEdit()
        
        self.dibujar_grafo_button = QPushButton("Dibujar grafo aleatorio")
        
        dibujar_grafo_layout.addWidget(self.dibujar_grafo_label)
        dibujar_grafo_layout.addWidget(self.cantidadEstados_label)
        dibujar_grafo_layout.addWidget(self.cantidadEstados_input)
        dibujar_grafo_layout.addWidget(self.cantidadMaximaRelaciones)
        dibujar_grafo_layout.addWidget(self.cantidadMaximaRelaciones_input)
        dibujar_grafo_layout.addWidget(self.dibujar_grafo_button)

        # Sección "Paso a Paso"
        navigation_layout = QVBoxLayout()
        self.pasoAPaso_label = QLabel("Paso a paso:")
        self.anterior_button = QPushButton("Anterior")
        self.siguiente_button = QPushButton("Siguiente")
        navigation_layout.addWidget(self.pasoAPaso_label)
        navigation_layout.addWidget(self.anterior_button)
        navigation_layout.addWidget(self.siguiente_button)
        
        definirHeuristica_dibujarGrafoAleatorio_pasoAPaso_layout.addLayout(definir_heuristica_layout)
        definirHeuristica_dibujarGrafoAleatorio_pasoAPaso_layout.addLayout(dibujar_grafo_layout)
        definirHeuristica_dibujarGrafoAleatorio_pasoAPaso_layout.addLayout(navigation_layout)

        # Agregar todas las secciones al diseño principal
        main_layout.addLayout(agregarEstado_listaEstado_conoceA_layout)
        main_layout.addLayout(definirHeuristica_dibujarGrafoAleatorio_pasoAPaso_layout)

        # Establecer el diseño principal en el widget principal
        main_widget.setLayout(main_layout)

        # Establecer el widget principal en la ventana principal
        self.setCentralWidget(main_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
