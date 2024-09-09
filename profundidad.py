# profundidad.py
def buscar_profundidad(laberinto, inicio, meta):
    """
    Realiza una búsqueda en profundidad (DFS) en el laberinto.

    :param laberinto: Representación del laberinto como una lista de listas.
    :param inicio: Coordenadas de inicio en el laberinto (x, y).
    :param meta: Coordenadas de la meta en el laberinto (x, y).
    :return: Lista de tuplas (x, y) que representan el camino desde el inicio hasta la meta.
    """
    stack = [inicio]
    visitados = set()
    padres = {inicio: None}

    while stack:
        nodo_actual = stack.pop()

        if nodo_actual == meta:
            # Construir el camino desde el inicio hasta la meta
            camino = []
            while nodo_actual:
                camino.append(nodo_actual)
                nodo_actual = padres[nodo_actual]
            return camino[::-1]  # Devolver el camino en el orden correcto

        if nodo_actual in visitados:
            continue

        visitados.add(nodo_actual)
        x, y = nodo_actual

        # Explorar los vecinos (arriba, abajo, izquierda, derecha)
        vecinos = [
            (x - 1, y),  # Arriba
            (x + 1, y),  # Abajo
            (x, y - 1),  # Izquierda
            (x, y + 1)   # Derecha
        ]

        for vecino in vecinos:
            if (0 <= vecino[0] < len(laberinto) and
                0 <= vecino[1] < len(laberinto[0]) and
                laberinto[vecino[0]][vecino[1]] != 1 and
                vecino not in visitados):
                stack.append(vecino)
                padres[vecino] = nodo_actual

    return []  # No se encontró ningún camino

# Ejemplo de uso (para pruebas):
if __name__ == "__main__":
    laberinto = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    inicio = (0, 0)
    meta = (4, 4)
    camino = buscar_profundidad(laberinto, inicio, meta)
    print("Camino encontrado:", camino)
