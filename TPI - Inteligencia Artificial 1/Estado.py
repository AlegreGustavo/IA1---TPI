from constantes import *

#Clase Estados
class Estado:
    def __init__(self, nombre, valor, posicion, tipo=None):
        self.__nombre = nombre
        self.__valor = valor
        self.__posicion = posicion
        self.__tipo = tipo
        
        self.__relaciones = []
                
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre
        
    @property
    def valor(self):
        return self.__valor
    
    @valor.setter
    def valor(self, valor):
        self.__valor = valor
        
    @property
    def posicion(self):
        return self.__posicion
    
    @posicion.setter
    def posicion(self, posicion):
        self.__posicion = posicion
        
    @property
    def tipo(self):
        return self.__tipo
    
    @tipo.setter
    def tipo(self, tipo):
        self.__tipo = tipo
        
    @property
    def relaciones(self):
        return self.__relaciones
    
    @relaciones.setter
    def relaciones(self, relaciones):
        self.__relaciones = relaciones
        
    def agregarRelacion(self, relacion):
        self.__relaciones.append(relacion)
        
    def quitarRelacion(self, relacion):
        self.__relaciones.remove(relacion)
        
    def establecerInicial(self):
        self.__tipo = "INICIAL"
        
    def establecerFinal(self):
        self.__valor = 0
        self.__tipo = "FINAL"
        
    def establecerNormal(self):
        self.__tipo = None
    
    def color(self):
        """
        Función que devuelve el color con que se pintará el nodo, dependiendo el tipo del Estado.
        """
        color = COLOR_NODO
        
        if self.__tipo == "INICIAL":
            color = COLOR_NODO_INICIAL
        if self.__tipo == "FINAL":
            color = COLOR_NODO_FINAL
            
        return color
        
    def __str__(self):
        salida = self.__nombre
    
        return salida