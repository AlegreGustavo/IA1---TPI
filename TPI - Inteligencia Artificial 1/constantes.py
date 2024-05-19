# CONSTANTES:
COLOR_NODO = "skyblue"
COLOR_NODO_INICIAL = "green"
COLOR_NODO_FINAL = "red"

TAMANIO_NODOS = 200

import networkx as nx
import matplotlib.pyplot as plt
import random

def dibujar_grafo(grafo, atributos_nodos):
    # Creamos un diccionario para mapear los nombres de los nodos con sus atributos
    nodos_atributos = {nodo: atributos_nodos[nodo] for nodo in grafo.nodes()}
    
    # Obtenemos los atributos personalizados para cada nodo
    colores = [nodos_atributos[nodo]["color"] for nodo in grafo.nodes()]
    tamanos = [nodos_atributos[nodo]["size"]*300 for nodo in grafo.nodes()]  # Escalamos los tamaños para una mejor visualización
    
    # Dibujamos el grafo
    nx.draw(grafo, with_labels=True, node_color=colores, node_size=tamanos)
    plt.show()

def generar_grafo_aleatorio(num_nodos):
    # Creamos un grafo vacío
    grafo = nx.Graph()

    # Creamos nodos aleatorios y les asignamos atributos personalizados
    atributos_nodos = {}
    for i in range(num_nodos):
        # Generamos un nombre aleatorio para el nodo
        nombre_nodo = f"Nodo_{i+1}"
        
        # Asignamos un tamaño aleatorio entre 0.1 y 1
        size = random.uniform(0.1, 1)
        
        # Asignamos un color aleatorio en formato hexadecimal
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        
        # Agregamos el nodo al grafo con sus atributos
        grafo.add_node(nombre_nodo)
        atributos_nodos[nombre_nodo] = {"size": size, "color": color}
    
    # Agregamos aristas aleatorias
    for nodo1 in grafo.nodes():
        for nodo2 in grafo.nodes():
            if nodo1 != nodo2 and random.random() < 0.3:  # Probabilidad de conexión
                grafo.add_edge(nodo1, nodo2)
    
    return grafo, atributos_nodos

if __name__ == "__main__":
    num_nodos = int(input("Ingrese el número de nodos en el grafo: "))
    grafo, atributos_nodos = generar_grafo_aleatorio(num_nodos)
    dibujar_grafo(grafo, atributos_nodos)
