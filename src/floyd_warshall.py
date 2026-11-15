"""Floyd-Warshall con matriz de sucesores y reconstrucción de caminos."""
from matriz import Matriz
from grafo import INF


def floyd_warshall(g, bitacora=None):
    """g: Grafo o GrafoMatriz. Devuelve (D, S) como Matriz.
    D[i][j] = distancia mínima (INF si no hay camino); S[i][j] = siguiente
    vértice de i hacia j (None si no hay camino). bitacora(k, d, sig) opcional."""
    D = g.a_matriz()
    n = D.filas
    d = D.a_listas()
    sig = [[None] * n for _ in range(n)]
    for i in range(n):
        sig[i][i] = i
        for j in range(n):
            if i != j and d[i][j] != INF:
                sig[i][j] = j
    for k in range(n):          # tres ciclos anidados: Θ(n³)
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            di, si = d[i], sig[i]
            for j in range(n):
                nuevo = dik + dk[j]
                if nuevo < di[j]:
                    di[j] = nuevo
                    si[j] = si[k]
        if bitacora:
            bitacora(k, d, sig)
    S = Matriz(n, n, None)
    S._datos = sig
    D._datos = d
    return D, S


def reconstruir_camino(S, u, v):
    """Lista [u, ..., v]; [] si no hay camino; [u] si u == v."""
    n = S.filas
    if not (0 <= u < n and 0 <= v < n):
        raise IndexError("vértice fuera de rango")
    if S.obtener(u, v) is None:
        return []
    camino = [u]
    while u != v:
        u = S.obtener(u, v)
        camino.append(u)
    return camino


def longitud_camino(g, camino):
    """Suma de pesos a lo largo de un camino (para validar contra D)."""
    return sum(g.peso(a, b) for a, b in zip(camino, camino[1:]))
