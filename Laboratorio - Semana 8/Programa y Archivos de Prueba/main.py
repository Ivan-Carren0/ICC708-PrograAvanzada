import os
import sys

from algoritmos import (
    bfs_graph, dfs_graph, ucs_graph, astar_graph,
    bfs_maze, dfs_maze, ucs_maze, astar_maze
)
from visualizacion import visualizar_laberinto, visualizar_grafo, imprimir_resultados
from loaders import GRAFOS_PREDEFINIDOS, LABERINTOS_PREDEFINIDOS, cargar_grafo_csv, cargar_laberinto_csv

ALGORITMOS = {"1": "BFS", "2": "DFS", "3": "UCS", "4": "A*"}
ALGO_FNS_GRAFO = {"1": bfs_graph, "2": dfs_graph, "3": ucs_graph, "4": astar_graph}
ALGO_FNS_MAZE = {"1": bfs_maze, "2": dfs_maze, "3": ucs_maze, "4": astar_maze}

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def preguntar(mensaje, opciones=None, defecto=None):
    while True:
        sufijo = f" [{'/'.join(opciones)}]" if opciones else ""
        if defecto is not None:
            sufijo += f" (Enter={defecto})"
        respuesta = input(f"  {mensaje}{sufijo}: ").strip()
        if respuesta == "" and defecto is not None:
            return defecto
        if opciones is None or respuesta in opciones:
            return respuesta
        print(f"Opción inválida. Elige: {', '.join(opciones)}")

def menu_principal():
    limpiar()
    print("\n" + "=" * 50)
    print("  BÚSQUEDA EN GRAFOS Y LABERINTOS")
    print("=" * 50)
    print("\n  1 → Grafo / Árbol")
    print("  2 → Laberinto")
    print("  0 → Salir\n")
    return preguntar("Opción", ["1", "2", "0"])

def menu_algoritmo():
    print("\n  Selecciona algoritmo:")
    print("    1 → BFS")
    print("    2 → DFS")
    print("    3 → UCS")
    print("    4 → A*\n")
    return preguntar("Opción", ["1", "2", "3", "4"])

def flujo_grafo():
    print("\n" + "=" * 50)
    print("  ESCENARIO: GRAFO")
    print("=" * 50)
    print("\n  Fuente:")
    print("    1 → Grafo simple (8 nodos)")
    print("    2 → Árbol binario (7 nodos)")
    print("    3 → Cargar desde CSV\n")
    
    fuente = preguntar("Opción", ["1", "2", "3"])
    posiciones = None
    
    if fuente == "3":
        ruta = preguntar("Ruta del archivo CSV")
        try:
            grafo = cargar_grafo_csv(ruta)
            print(f"\nGrafo cargado: {len(grafo)} nodos")
        except Exception as e:
            print(f"\nError: {e}")
            input("\n  Presiona Enter para continuar...")
            return
        inicio_def = meta_def = None
    else:
        datos = GRAFOS_PREDEFINIDOS[fuente]
        grafo = datos["grafo"]
        posiciones = datos["posiciones"]
        inicio_def = datos["inicio_defecto"]
        meta_def = datos["meta_defecto"]
        print(f"\n  ✓ {datos['nombre']} cargado")
    
    print()
    inicio = preguntar("Nodo inicial", defecto=str(inicio_def) if inicio_def else None)
    meta = preguntar("Nodo objetivo", defecto=str(meta_def) if meta_def else None)
    
    nodos = list(grafo.keys())
    if nodos and isinstance(nodos[0], int):
        try:
            inicio = int(inicio)
            meta = int(meta)
        except ValueError:
            pass
    
    if inicio not in grafo:
        print(f"Nodo '{inicio}' no existe")
        input("\n  Presiona Enter...")
        return
    
    algo = menu_algoritmo()
    nombre_algo = ALGORITMOS[algo]
    
    visitados, camino, costo = ALGO_FNS_GRAFO[algo](grafo, inicio, meta)
    imprimir_resultados("Grafo", nombre_algo, visitados, camino, costo)
    
    print("\n  Mostrando visualización...")
    visualizar_grafo(grafo, visitados, camino, inicio, meta, nombre_algo, posiciones)
    input("\n  Presiona Enter para continuar...")

def flujo_laberinto():
    print("\n" + "=" * 50)
    print("  ESCENARIO: LABERINTO")
    print("=" * 50)
    print("\n  Fuente:")
    print("    1 → Laberinto predefinido (8×8)")
    print("    2 → Cargar desde CSV\n")
    
    fuente = preguntar("Opción", ["1", "2"])
    
    if fuente == "1":
        datos = LABERINTOS_PREDEFINIDOS["1"]
        laberinto = datos["laberinto"]
        inicio_def = datos["inicio_defecto"]
        meta_def = datos["meta_defecto"]
        print(f"\n{datos['nombre']} cargado")
    else:
        ruta = preguntar("Ruta del archivo CSV")
        try:
            laberinto = cargar_laberinto_csv(ruta)
            print(f"\nLaberinto cargado: {len(laberinto)}×{len(laberinto[0])}")
        except Exception as e:
            print(f"\nError: {e}")
            input("\n  Presiona Enter...")
            return
        inicio_def = meta_def = None
    
    filas, cols = len(laberinto), len(laberinto[0])
    
    print("\n  Laberinto:")
    for fila in laberinto:
        print("    " + " ".join("·" if c == 0 else "█" for c in fila))
    
    print(f"\n  Posiciones: fila (0-{filas-1}), columna (0-{cols-1})")
    
    inicio = None
    while inicio is None:
        entrada = preguntar("Posición inicial (fila,col)", defecto=str(inicio_def) if inicio_def else None)
        try:
            f, c = map(int, entrada.replace(" ", "").split(","))
            if 0 <= f < filas and 0 <= c < cols and laberinto[f][c] == 0:
                inicio = (f, c)
            else:
                print("Celda inválida o barrera")
        except:
            print("Formato inválido. Usa: fila,col")
    
    meta = None
    while meta is None:
        entrada = preguntar("Posición objetivo (fila,col)", defecto=str(meta_def) if meta_def else None)
        try:
            f, c = map(int, entrada.replace(" ", "").split(","))
            if 0 <= f < filas and 0 <= c < cols and laberinto[f][c] == 0:
                meta = (f, c)
            else:
                print("Celda inválida o barrera")
        except:
            print("Formato inválido. Usa: fila,col")
    
    algo = menu_algoritmo()
    nombre_algo = ALGORITMOS[algo]
    
    visitados, camino, costo = ALGO_FNS_MAZE[algo](laberinto, inicio, meta)
    imprimir_resultados("Laberinto", nombre_algo, visitados, camino, costo)
    
    print("\n  Mostrando visualización...")
    visualizar_laberinto(laberinto, visitados, camino, inicio, meta, nombre_algo)
    input("\n  Presiona Enter para continuar...")

def main():
    while True:
        opcion = menu_principal()
        if opcion == "0":
            sys.exit(0)
        elif opcion == "1":
            flujo_grafo()
        else:
            flujo_laberinto()

if __name__ == "__main__":
    main()