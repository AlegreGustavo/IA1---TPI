import math

def calcular_distancias(x, y):
    # Desempaquetamos las coordenadas
    x1, y1 = x
    x2, y2 = y
    
    # Calculamos la distancia Euclídea
    distancia_euclidea = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    # Calculamos la distancia de Manhattan
    distancia_manhattan = abs(x2 - x1) + abs(y2 - y1)
    
    # Mostramos los resultados
    print(f"Distancia Euclídea: {distancia_euclidea}")
    print(f"Distancia de Manhattan: {distancia_manhattan}")

# Ejemplo de uso
punto_x = (1, 2)
punto_y = (4, 6)
calcular_distancias(punto_x, punto_y)
