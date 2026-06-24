import csv
import os

GRAFOS_PREDEFINIDOS = {
    "1": {
        "nombre": "Grafo simple (8 nodos)",
        "grafo": {
            'A': [('B', 1), ('C', 4)],
            'B': [('A', 1), ('D', 2), ('E', 5)],
            'C': [('A', 4), ('F', 3)],
            'D': [('B', 2), ('E', 1), ('G', 6)],
            'E': [('B', 5), ('D', 1), ('H', 2)],
            'F': [('C', 3), ('G', 1)],
            'G': [('D', 6), ('F', 1), ('H', 3)],
            'H': [('E', 2), ('G', 3)],
        },
        "inicio_defecto": "A",
        "meta_defecto": "H",
        "posiciones": {
            'A': (0, 1), 'B': (1, 2), 'C': (1, 0),
            'D': (2, 2), 'E': (2, 1), 'F': (2, 0),
            'G': (3, 1), 'H': (4, 1),
        }
    },
    "2": {
        "nombre": "Árbol binario (7 nodos)",
        "grafo": {
            1: [(2, 1), (3, 1)],
            2: [(1, 1), (4, 1), (5, 1)],
            3: [(1, 1), (6, 1), (7, 1)],
            4: [(2, 1)], 5: [(2, 1)], 6: [(3, 1)], 7: [(3, 1)],
        },
        "inicio_defecto": 1,
        "meta_defecto": 7,
        "posiciones": {
            1: (0, 2), 2: (-1, 1), 3: (1, 1),
            4: (-1.5, 0), 5: (-0.5, 0), 6: (0.5, 0), 7: (1.5, 0),
        }
    }
}

LABERINTOS_PREDEFINIDOS = {
    "1": {
        "nombre": "Laberinto Predefinido (8×8)",
        "laberinto": [
            [0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,0],
            [0,1,1,1,1,1,1,0],
            [0,0,0,1,0,0,1,0],
            [1,0,0,1,1,0,1,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ],
        "inicio_defecto": (0, 0),
        "meta_defecto": (7, 7),
    }
}

def cargar_grafo_csv(ruta):
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró: {ruta}")
    
    with open(ruta, 'r', encoding='utf-8') as f:
        lector = csv.reader(f)
        filas = [fila for fila in lector if fila]
    
    if not filas:
        raise ValueError("El archivo CSV está vacío.")
    
    es_matriz = len(filas[0]) > 1 and len(filas[0]) == len(filas)
    
    grafo = {}
    
    if es_matriz:
        nodos = [fila[0].strip() for fila in filas]
        for i, fila in enumerate(filas):
            origen = fila[0].strip()
            grafo[origen] = []
            for j, peso in enumerate(fila[1:]):
                if j < len(nodos):
                    try:
                        p = float(peso.strip())
                        if p > 0:
                            grafo[origen].append((nodos[j], p))
                    except ValueError:
                        continue
    else:
        for fila in filas:
            origen = fila[0].strip()
            destino = fila[1].strip()
            peso = float(fila[2].strip()) if len(fila) > 2 else 1.0
            if origen not in grafo:
                grafo[origen] = []
            grafo[origen].append((destino, peso))
            if destino not in grafo:
                grafo[destino] = []
    
    return grafo

def cargar_laberinto_csv(ruta):
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró: {ruta}")
    
    laberinto = []
    with open(ruta, 'r', encoding='utf-8') as f:
        lector = csv.reader(f)
        for fila in lector:
            if fila:
                laberinto.append([int(celda.strip()) for celda in fila if celda.strip()])
    
    if not laberinto:
        raise ValueError("El archivo CSV del laberinto está vacío.")
    return laberinto