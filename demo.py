"""Demostración: calcula con Floyd-Warshall la matriz de distancias de la red
de municipios y muestra caminos.

Uso:
    python demo.py                      -> matriz completa y 5 caminos de ejemplo
    python demo.py Flandes Tocaima      -> distancia y camino entre dos municipios
"""
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(RAIZ, "src"))

from cargar_csv import cargar_grafo
from floyd_warshall import floyd_warshall, reconstruir_camino
from grafo import INF

g = cargar_grafo(os.path.join(RAIZ, "data", "red_alto_magdalena.csv"))
D, S = floyd_warshall(g)
nombres = [g.nombre(i) for i in range(g.n)]


def consulta(origen, destino):
    u, v = g.indice(origen), g.indice(destino)
    camino = reconstruir_camino(S, u, v)
    d = D.obtener(u, v)
    if not camino:
        print(f"{origen} -> {destino}: no hay camino")
    else:
        ruta = " -> ".join(g.nombre(x) for x in camino)
        print(f"{origen} -> {destino}: {d:g} km  ({ruta})")


if len(sys.argv) == 3:
    try:
        consulta(sys.argv[1], sys.argv[2])
    except KeyError:
        print("Municipio no encontrado. Opciones:", ", ".join(nombres))
    sys.exit()

print(f"Red: {g.n} municipios, {g.m} vias directas\n")
print("Matriz de distancias minimas (km):\n")
ancho = 13
print(" " * ancho + "".join(n[:6].rjust(8) for n in nombres))
for i in range(g.n):
    fila = "".join(("inf" if D.obtener(i, j) == INF else f"{D.obtener(i, j):g}").rjust(8)
                   for j in range(g.n))
    print(nombres[i].ljust(ancho) + fila)

print("\nCaminos de ejemplo:")
for a, b in [("Flandes", "Tocaima"), ("Nilo", "Guataquí"), ("Girardot", "Guataquí"),
             ("Nilo", "Tocaima"), ("Tocaima", "Guataquí")]:
    consulta(a, b)
