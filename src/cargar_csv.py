"""Carga de grafos desde CSV con columnas: origen,destino,km (por nombre de municipio)."""
import csv
from grafo import Grafo
from grafo_matriz import GrafoMatriz


def cargar_grafo(ruta, dirigido=False):
    g = Grafo(dirigido)
    with open(ruta, newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            a, b = fila["origen"].strip(), fila["destino"].strip()
            for nom in (a, b):
                if nom not in g._por_nombre:
                    g.agregar_vertice(nom)
            g.agregar_arista(g.indice(a), g.indice(b), float(fila["km"]))
    return g


def cargar_grafo_matriz(ruta, dirigido=False):
    return GrafoMatriz.desde_grafo(cargar_grafo(ruta, dirigido))
