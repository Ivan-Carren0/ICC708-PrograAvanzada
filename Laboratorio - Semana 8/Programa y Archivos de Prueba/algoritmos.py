from collections import deque
import heapq

def reconstruir_camino(padres, inicio, meta):
    camino = []
    actual = meta
    while actual is not None:
        camino.append(actual)
        actual = padres.get(actual)
    camino.reverse()
    return camino if camino and camino[0] == inicio else []

def bfs_graph(grafo, inicio, meta):
    visitados = []
    padres = {inicio: None}
    cola = deque([inicio])
    
    while cola:
        nodo = cola.popleft()
        visitados.append(nodo)
        if nodo == meta:
            camino = reconstruir_camino(padres, inicio, meta)
            return visitados, camino, len(camino) - 1
        
        for vecino, _ in grafo.get(nodo, []):
            if vecino not in padres:
                padres[vecino] = nodo
                cola.append(vecino)
    
    return visitados, [], float('inf')

def dfs_graph(grafo, inicio, meta):
    visitados = []
    padres = {inicio: None}
    pila = [inicio]
    
    while pila:
        nodo = pila.pop()
        if nodo in visitados:
            continue
        visitados.append(nodo)
        if nodo == meta:
            camino = reconstruir_camino(padres, inicio, meta)
            return visitados, camino, len(camino) - 1
        
        for vecino, _ in reversed(grafo.get(nodo, [])):
            if vecino not in padres:
                padres[vecino] = nodo
                pila.append(vecino)
    
    return visitados, [], float('inf')

def ucs_graph(grafo, inicio, meta):
    visitados = []
    padres = {inicio: (0, None)}
    heap = [(0, inicio, None)]
    
    while heap:
        costo, nodo, padre = heapq.heappop(heap)
        if nodo in [v for v, _ in visitados]:
            continue
        padres[nodo] = (costo, padre)
        visitados.append(nodo)
        
        if nodo == meta:
            camino = reconstruir_camino_ucs(padres, inicio, meta)
            return visitados, camino, costo
        
        for vecino, peso in grafo.get(nodo, []):
            if vecino not in padres:
                heapq.heappush(heap, (costo + peso, vecino, nodo))
    
    return visitados, [], float('inf')

def astar_graph(grafo, inicio, meta, heuristica=None):
    if heuristica is None:
        heuristica = lambda n, g: 0
    
    visitados = []
    padres = {}
    g_costo = {inicio: 0}
    heap = [(heuristica(inicio, meta), 0, inicio, None)]
    
    while heap:
        f, g, nodo, padre = heapq.heappop(heap)
        if nodo in padres:
            continue
        padres[nodo] = (g, padre)
        visitados.append(nodo)
        
        if nodo == meta:
            camino = reconstruir_camino_ucs(padres, inicio, meta)
            return visitados, camino, g
        
        for vecino, peso in grafo.get(nodo, []):
            nuevo_g = g + peso
            if vecino not in padres and nuevo_g < g_costo.get(vecino, float('inf')):
                g_costo[vecino] = nuevo_g
                heapq.heappush(heap, (nuevo_g + heuristica(vecino, meta), nuevo_g, vecino, nodo))
    
    return visitados, [], float('inf')

def reconstruir_camino_ucs(padres, inicio, meta):
    camino = []
    actual = meta
    while actual is not None:
        camino.append(actual)
        _, actual = padres[actual]
    camino.reverse()
    return camino if camino and camino[0] == inicio else []

DIRECCIONES = [(-1,0), (1,0), (0,-1), (0,1)]

def vecinos_maze(laberinto, fila, col):
    filas, cols = len(laberinto), len(laberinto[0])
    vecinos = []
    for df, dc in DIRECCIONES:
        f, c = fila + df, col + dc
        if 0 <= f < filas and 0 <= c < cols and laberinto[f][c] == 0:
            vecinos.append((f, c))
    return vecinos

def bfs_maze(laberinto, inicio, meta):
    visitados = []
    padres = {inicio: None}
    cola = deque([inicio])
    
    while cola:
        pos = cola.popleft()
        visitados.append(pos)
        if pos == meta:
            camino = reconstruir_camino(padres, inicio, meta)
            return visitados, camino, len(camino) - 1
        
        for vecino in vecinos_maze(laberinto, *pos):
            if vecino not in padres:
                padres[vecino] = pos
                cola.append(vecino)
    
    return visitados, [], float('inf')

def dfs_maze(laberinto, inicio, meta):
    visitados = []
    padres = {inicio: None}
    pila = [inicio]
    
    while pila:
        pos = pila.pop()
        if pos in visitados:
            continue
        visitados.append(pos)
        if pos == meta:
            camino = reconstruir_camino(padres, inicio, meta)
            return visitados, camino, len(camino) - 1
        
        for vecino in vecinos_maze(laberinto, *pos):
            if vecino not in padres:
                padres[vecino] = pos
                pila.append(vecino)
    
    return visitados, [], float('inf')

def ucs_maze(laberinto, inicio, meta):
    visitados = []
    padres = {inicio: (0, None)}
    heap = [(0, inicio, None)]
    
    while heap:
        costo, pos, padre = heapq.heappop(heap)
        if pos in [p for p, _ in visitados]:
            continue
        padres[pos] = (costo, padre)
        visitados.append(pos)
        
        if pos == meta:
            camino = reconstruir_camino_ucs(padres, inicio, meta)
            return visitados, camino, costo
        
        for vecino in vecinos_maze(laberinto, *pos):
            if vecino not in padres:
                heapq.heappush(heap, (costo + 1, vecino, pos))
    
    return visitados, [], float('inf')

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_maze(laberinto, inicio, meta):
    visitados = []
    padres = {}
    g_costo = {inicio: 0}
    heap = [(manhattan(inicio, meta), 0, inicio, None)]
    
    while heap:
        f, g, pos, padre = heapq.heappop(heap)
        if pos in padres:
            continue
        padres[pos] = (g, padre)
        visitados.append(pos)
        
        if pos == meta:
            camino = reconstruir_camino_ucs(padres, inicio, meta)
            return visitados, camino, g
        
        for vecino in vecinos_maze(laberinto, *pos):
            nuevo_g = g + 1
            if vecino not in padres and nuevo_g < g_costo.get(vecino, float('inf')):
                g_costo[vecino] = nuevo_g
                heapq.heappush(heap, (nuevo_g + manhattan(vecino, meta), nuevo_g, vecino, pos))
    
    return visitados, [], float('inf')