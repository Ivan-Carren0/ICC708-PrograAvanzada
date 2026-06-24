import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

COLORES = {
    'barrera': '#2d2d2d',
    'libre': '#f5f5f5',
    'visitado': '#aed6f1',
    'camino': '#f39c12',
    'inicio': '#27ae60',
    'meta': '#e74c3c',
    'nodo': '#d6eaf8',
    'arista': '#7f8c8d',
    'arista_camino': '#e67e22'
}

def hex_a_rgb(hex_color):
    from matplotlib.colors import hex2color
    return list(hex2color(hex_color))

def visualizar_laberinto(laberinto, visitados, camino, inicio, meta, algoritmo):
    filas, cols = len(laberinto), len(laberinto[0])
    display = np.zeros((filas, cols, 3))
    
    barrera = hex_a_rgb(COLORES['barrera'])
    libre = hex_a_rgb(COLORES['libre'])
    visitado = hex_a_rgb(COLORES['visitado'])
    camino_color = hex_a_rgb(COLORES['camino'])
    inicio_color = hex_a_rgb(COLORES['inicio'])
    meta_color = hex_a_rgb(COLORES['meta'])
    
    for r in range(filas):
        for c in range(cols):
            display[r, c] = barrera if laberinto[r][c] == 1 else libre
    
    for r, c in visitados:
        if (r, c) not in (inicio, meta):
            display[r, c] = visitado
    
    for r, c in camino:
        if (r, c) not in (inicio, meta):
            display[r, c] = camino_color
    
    if inicio:
        display[inicio[0], inicio[1]] = inicio_color
    if meta:
        display[meta[0], meta[1]] = meta_color
    
    fig, ax = plt.subplots(figsize=(max(8, cols*0.5), max(6, filas*0.5)))
    ax.imshow(display, interpolation='nearest')
    
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, filas, 1), minor=True)
    ax.grid(which='minor', color='#cccccc', linewidth=0.5)
    ax.tick_params(which='minor', size=0)
    
    ax.set_title(f'Laberinto — {algoritmo}   |   Costo: {len(camino)-1 if camino else "∞"}', 
                 fontsize=12, fontweight='bold')
    
    from matplotlib.patches import Patch
    leyenda = [
        Patch(color=COLORES['barrera'], label='Barrera'),
        Patch(color=COLORES['visitado'], label=f'Visitados ({len(visitados)})'),
        Patch(color=COLORES['camino'], label=f'Camino ({len(camino)} pasos)'),
        Patch(color=COLORES['inicio'], label='Inicio'),
        Patch(color=COLORES['meta'], label='Meta'),
    ]
    ax.legend(handles=leyenda, loc='upper right', bbox_to_anchor=(1.2, 1.02))
    
    plt.tight_layout()
    plt.show()

def visualizar_grafo(grafo, visitados, camino, inicio, meta, algoritmo, posiciones=None):
    nodos = list(grafo.keys())
    for vecinos in grafo.values():
        for nb, _ in vecinos:
            if nb not in nodos:
                nodos.append(nb)
    
    if posiciones is None:
        posiciones = {}
        n = len(nodos)
        for i, nodo in enumerate(sorted(nodos, key=str)):
            angulo = 2 * math.pi * i / n
            posiciones[nodo] = (math.cos(angulo), math.sin(angulo))
    
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_aspect('equal')
    ax.axis('off')
    
    camino_set = set(zip(camino, camino[1:])) if camino else set()
    
    aristas_dibujadas = set()
    for nodo, vecinos in grafo.items():
        for nb, peso in vecinos:
            arista = tuple(sorted([nodo, nb]))
            if arista in aristas_dibujadas:
                continue
            aristas_dibujadas.add(arista)
            
            x0, y0 = posiciones[nodo]
            x1, y1 = posiciones[nb]
            es_camino = (nodo, nb) in camino_set or (nb, nodo) in camino_set
            
            color = COLORES['arista_camino'] if es_camino else COLORES['arista']
            ax.plot([x0, x1], [y0, y1], color=color, linewidth=3 if es_camino else 1.2)
            
            ax.text((x0+x1)/2, (y0+y1)/2, str(peso), fontsize=8, ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.1', fc='white', alpha=0.7))
    
    radio = 0.15
    for nodo in nodos:
        x, y = posiciones[nodo]
        
        if nodo == inicio:
            color = COLORES['inicio']
        elif nodo == meta:
            color = COLORES['meta']
        elif nodo in camino:
            color = COLORES['camino']
        elif nodo in visitados:
            color = COLORES['visitado']
        else:
            color = COLORES['nodo']
        
        circulo = plt.Circle((x, y), radio, color=color, ec='#555', linewidth=1.2)
        ax.add_patch(circulo)
        
        idx = visitados.index(nodo) + 1 if nodo in visitados else ''
        label = f'{nodo}\n({idx})' if idx else str(nodo)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold')
    
    from matplotlib.patches import Patch
    leyenda = [
        Patch(color=COLORES['inicio'], label='Inicio'),
        Patch(color=COLORES['meta'], label='Meta'),
        Patch(color=COLORES['camino'], label=f'Camino ({len(camino)-1 if camino else "∞"} pasos)'),
        Patch(color=COLORES['visitado'], label=f'Visitados ({len(visitados)})'),
        Patch(color=COLORES['nodo'], label='No visitado'),
    ]
    ax.legend(handles=leyenda, loc='lower right')
    
    ax.set_title(f'Grafo — {algoritmo}   |   Costo: {len(camino)-1 if camino else "∞"}', 
                 fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.show()

def imprimir_resultados(escenario, algoritmo, visitados, camino, costo):
    sep = "=" * 50
    print(f"\n{sep}")
    print(f"  Escenario: {escenario}")
    print(f"  Algoritmo: {algoritmo}")
    print(sep)
    print(f"  Orden de visita ({len(visitados)}):")
    print(f"    {' → '.join(str(n) for n in visitados)}")
    print(f"\n  Camino encontrado ({len(camino)}):")
    if camino:
        print(f"    {' → '.join(str(n) for n in camino)}")
        print(f"\n  Costo total: {costo}")
    else:
        print("  No se encontró camino.")
    print(sep)