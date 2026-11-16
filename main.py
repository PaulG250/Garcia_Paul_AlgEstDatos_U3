"""Red ficticia de ciudades: las distancias son didácticas, no reales."""
import heapq
from collections import deque


def crear_red():
    # R1: construir la lista de adyacencia: O(V + E).
    red = {c: [] for c in ['Quito', 'Ambato', 'Riobamba', 'Cuenca', 'Guayaquil', 'Loja']}
    carreteras = [('Quito', 'Cuenca', 600), ('Quito', 'Ambato', 100),
                  ('Ambato', 'Riobamba', 60), ('Riobamba', 'Cuenca', 140),
                  ('Cuenca', 'Guayaquil', 180), ('Cuenca', 'Loja', 150),
                  ('Guayaquil', 'Loja', 400)]
    for a, b, km in carreteras:
        red[a].append((b, km))
        red[b].append((a, km))
    return red


def bfs(grafo, origen):
    # R2: O(V + E), con lista de adyacencia.
    distancias = {origen: 0}
    padres = {origen: None}
    cola = deque([origen])
    while cola:
        ciudad = cola.popleft()
        for vecino, _ in grafo[ciudad]:
            if vecino not in distancias:
                distancias[vecino] = distancias[ciudad] + 1
                padres[vecino] = ciudad
                cola.append(vecino)
    return distancias, padres


# R3: función provista en el enunciado, sin modificaciones.
# O((V + E) log V): el factor logarítmico procede del heap.
def dijkstra(grafo, origen):
    """Devuelve {ciudad: distancia_minima_desde_origen}."""
    dist = {ciudad: float('inf') for ciudad in grafo}
    dist[origen] = 0
    heap = [(0, origen)]          # cola de prioridad
    while heap:
        d, u = heapq.heappop(heap)      # el mas cercano pendiente
        if d > dist[u]:
            continue                    # ya teniamos una ruta mejor
        for vecino, peso in grafo[u]:
            if dist[u] + peso < dist[vecino]:    # relajacion
                dist[vecino] = dist[u] + peso
                heapq.heappush(heap, (dist[vecino], vecino))
    return dist


def reconstruir(padres, destino):
    ruta = []
    while destino is not None:
        ruta.append(destino)
        destino = padres[destino]
    return ruta[::-1]


def ruta_minima(grafo, distancias, origen, destino):
    # R4: recuperar un camino óptimo sin modificar Dijkstra: O(V + E).
    # Seguimos solo aristas que respeten las distancias mínimas.
    padres = {origen: None}
    cola = deque([origen])
    while cola:
        u = cola.popleft()
        if u == destino:
            return reconstruir(padres, destino)
        for v, peso in grafo[u]:
            if v not in padres and distancias[u] + peso == distancias[v]:
                padres[v] = u
                cola.append(v)
    return []


def comparar(grafo, origen, destino):
    # R4 completo: O((V + E) log V), dominado por Dijkstra.
    saltos, padres = bfs(grafo, origen)
    dist = dijkstra(grafo, origen)
    if destino not in saltos:
        print('No existe ruta entre estas ciudades.')
        return
    ruta_bfs = reconstruir(padres, destino)
    ruta_km = ruta_minima(grafo, dist, origen, destino)
    pesos = {(u, v): p for u in grafo for v, p in grafo[u]}
    km_bfs = sum(pesos[a, b] for a, b in zip(ruta_bfs, ruta_bfs[1:]))
    print('Menos tramos:', ' -> '.join(ruta_bfs), '|', saltos[destino], 'tramos |', km_bfs, 'km')
    print('Menos kilómetros:', ' -> '.join(ruta_km), '|', len(ruta_km)-1, 'tramos |', dist[destino], 'km')
    print('BFS minimiza tramos; Dijkstra minimiza la suma de kilómetros.')


def pedir_ciudad(grafo, mensaje):
    while True:
        entrada = input(mensaje).strip().casefold()
        for ciudad in grafo:
            if ciudad.casefold() == entrada:
                return ciudad
        print('Ciudad no válida. Opciones:', ', '.join(grafo))


def main():
    grafo = crear_red()
    print('Red didáctica: los kilómetros son ficticios.')
    while True:
        print('\n1. Red y grados\n2. BFS y conectividad\n3. Distancias mínimas\n4. Comparar rutas\n0. Salir')
        opcion = input('Opción: ').strip()
        if opcion == '0':
            break
        if opcion == '1':
            # Grado de cada vértice: O(1); todos los grados: O(V).
            for ciudad, vecinos in grafo.items():
                print(ciudad, '| grado:', len(vecinos), '| conexiones:', vecinos)
        elif opcion in {'2', '3', '4'}:
            origen = pedir_ciudad(grafo, 'Origen: ')
            if opcion == '2':
                saltos, _ = bfs(grafo, origen)
                for ciudad, cantidad in saltos.items():
                    print(ciudad, ':', cantidad, 'tramos desde el origen')
                faltan = set(grafo) - set(saltos)
                print('Red conexa.' if not faltan else 'No alcanzables: ' + ', '.join(sorted(faltan)))
                aisladas = [c for c in grafo if not grafo[c]]
                print('Ciudades aisladas:', ', '.join(aisladas) or 'Ninguna')
            elif opcion == '3':
                dist = dijkstra(grafo, origen)
                for ciudad, km in dist.items():
                    print(ciudad, ':', km, 'km' if km != float('inf') else '(no alcanzable)')
                otras = {c: km for c, km in dist.items() if c != origen and km != float('inf')}
                if otras:
                    minimo, maximo = min(otras.values()), max(otras.values())
                    print('Más cercanas:', [c for c in otras if otras[c] == minimo], minimo, 'km')
                    print('Más lejanas:', [c for c in otras if otras[c] == maximo], maximo, 'km')
            else:
                destino = pedir_ciudad(grafo, 'Destino (prueba Quito a Cuenca): ')
                comparar(grafo, origen, destino)
        else:
            print('Opción no válida.')


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print('\nPrograma finalizado.')
