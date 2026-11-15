"""Grafos aleatorios conexos con densidad dada (m = d * n(n-1)/2)."""
import random


def aristas_aleatorias(n, densidad, semilla=0):
    rnd = random.Random(semilla)
    m_obj = min(max(n - 1, round(densidad * n * (n - 1) / 2)), n * (n - 1) // 2)
    usadas, aristas = set(), []
    orden = list(range(n))
    rnd.shuffle(orden)
    for i in range(1, n):  # árbol generador: garantiza conectividad
        u, v = orden[i], orden[rnd.randrange(i)]
        usadas.add((min(u, v), max(u, v)))
        aristas.append((min(u, v), max(u, v), rnd.randint(1, 100)))
    if m_obj > len(aristas):
        todos = [(u, v) for u in range(n) for v in range(u + 1, n) if (u, v) not in usadas]
        for u, v in rnd.sample(todos, m_obj - len(aristas)):
            aristas.append((u, v, rnd.randint(1, 100)))
    return aristas
