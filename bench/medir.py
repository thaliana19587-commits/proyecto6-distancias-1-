"""Entrega 3: memoria (matriz vs listas) y tiempo de Floyd-Warshall para tres densidades.
Uso: python bench/medir.py   -> escribe bench/resultados_memoria.csv y resultados_tiempo.csv"""
import os, sys, csv, time, gc, tracemalloc
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(RAIZ, "src"), os.path.join(RAIZ, "bench")]
from grafo import Grafo
from grafo_matriz import GrafoMatriz
from floyd_warshall import floyd_warshall
from generador import aristas_aleatorias

DENSIDADES = [0.05, 0.30, 0.80]            # rala, media, densa
N_MEMORIA = list(range(50, 1001, 50))       # 50 ... 1000
N_TIEMPO = [50, 100, 200, 300, 400, 500]


def bytes_de(constructor):
    gc.collect()
    tracemalloc.start()
    obj = constructor()
    actual, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return obj, actual


def memoria():
    filas = []
    for d in DENSIDADES:
        for n in N_MEMORIA:
            ar = aristas_aleatorias(n, d, semilla=n)
            m = len(ar)
            _, b_lista = bytes_de(lambda: Grafo.desde_aristas_unicas(n, ar))
            _, b_mat = bytes_de(lambda: GrafoMatriz.desde_aristas(n, ar))
            filas.append(dict(densidad=d, n=n, m=m, bytes_lista=b_lista, bytes_matriz=b_mat,
                              celdas_lista=n + 4 * m, celdas_matriz=n * n,
                              razon_bytes=round(b_mat / b_lista, 3)))
            print("mem", d, n, filas[-1]["razon_bytes"], flush=True)
    return filas


def tiempo():
    filas = []
    for d in DENSIDADES:
        for n in N_TIEMPO:
            ar = aristas_aleatorias(n, d, semilla=n)
            g = GrafoMatriz.desde_aristas(n, ar)
            mejor = None
            for _ in range(2 if n <= 300 else 1):
                t0 = time.perf_counter()
                floyd_warshall(g)
                dt = time.perf_counter() - t0
                mejor = dt if mejor is None else min(mejor, dt)
            filas.append(dict(densidad=d, n=n, m=len(ar), segundos=round(mejor, 4),
                              seg_sobre_n3=mejor / n ** 3))
            print("t", d, n, filas[-1]["segundos"], flush=True)
    return filas


def guardar(nombre, filas):
    with open(os.path.join(RAIZ, "bench", nombre), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader(); w.writerows(filas)


if __name__ == "__main__":
    guardar("resultados_memoria.csv", memoria())
    guardar("resultados_tiempo.csv", tiempo())
