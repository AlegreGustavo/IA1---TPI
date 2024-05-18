from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QMessageBox

class MensajeAlerta(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mensaje de Alerta con PySide6")
        self.setGeometry(100, 100, 400, 200)

        # Crear un widget central para la ventana principal
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # Crear un layout vertical para el widget central
        self.layout = QVBoxLayout(self.centralWidget)

    def mostrar_alerta(self):
        mensaje = "Este es un mensaje de alerta."
        self.mostrar_mensaje_alerta(mensaje)
        
    def mostrarAlerta(self, mensaje):
        self.mostrar_mensaje_alerta(mensaje)

    def mostrar_mensaje_alerta(self, texto):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(texto)
        msg_box.setWindowTitle("Alerta")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()