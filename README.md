# Red de ciudades de la Unidad 3

Ejecutar con Python 3: `python main.py`. Solo usa la biblioteca estándar.

- R1: seis ciudades, siete carreteras bidireccionales y distancias ficticias positivas; lista de adyacencia y grados.
- R2: BFS propio con cola; informa tramos, ciudades alcanzables, conectividad y vértices aislados.
- R3: Dijkstra provisto sin modificaciones; distancias mínimas y ciudades más cercanas y lejanas, excluyendo el origen y los destinos inalcanzables.
- R4: compara rutas completas y sus costos. Reconstruye la ruta de BFS con padres y recupera un camino óptimo siguiendo las distancias devueltas por Dijkstra.

## Prueba

En opción 4, usa Quito y Cuenca. BFS elige Quito -> Cuenca (1 tramo, 600 km). Dijkstra permite Quito -> Ambato -> Riobamba -> Cuenca (3 tramos, 300 km).

Desde Quito: Ambato 100 km, Riobamba 160 km, Cuenca 300 km, Guayaquil 480 km y Loja 450 km. La más cercana es Ambato y la más lejana Guayaquil. La red es conexa y no tiene vértices aislados.

El enunciado usa escalas como saltos: aquí se muestran tramos/aristas para evitar ambigüedad. Las paradas intermedias de una ruta entre ciudades distintas son tramos menos uno.

## Complejidad

V: ciudades; E: carreteras. Construir red O(V+E); mostrar red O(V+E); calcular todos los grados O(V); BFS O(V+E); Dijkstra y comparación completa O((V+E) log V). El factor logarítmico se debe a las operaciones de la cola de prioridad.
