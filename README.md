# Proyecto 6 · Matriz de distancias entre municipios (Floyd-Warshall)

    src/nodo.py            Nodo y Arista
    src/grafo.py           TAD Grafo (lista de adyacencia)
    src/grafo_matriz.py    GrafoMatriz (matriz de adyacencia)  <- Entrega 2
    src/matriz.py          TAD Matriz (D y S)
    src/floyd_warshall.py  floyd_warshall + reconstruir_camino   <- Entrega 2
    src/cargar_csv.py      carga desde CSV (origen,destino,km)
    data/red_alto_magdalena.csv   instancia de 8 municipios (km aproximados; contrastar con INVÍAS / mapas)
    bench/medir.py         memoria y tiempo, 3 densidades        <- Entrega 3
    tests/test_proyecto.py 8 pruebas (incluye validación contra networkx)

    python -m unittest discover -s tests -v
    python bench/medir.py        # ~1 min; genera bench/resultados_*.csv

networkx se usa solo en las pruebas para validar; la solución no lo importa.
