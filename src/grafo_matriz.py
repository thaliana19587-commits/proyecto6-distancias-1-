"""GrafoMatriz: grafo ponderado guardado como matriz de adyacencia (Θ(n²) memoria)."""
from matriz import Matriz
from grafo import INF, VerticeInexistenteError


class GrafoMatriz:
    def __init__(self, n, dirigido=False, nombres=None):
        if n <= 0:
            raise ValueError("n debe ser > 0")
        self._n = n
        self._dirigido = dirigido
        self._nombres = list(nombres) if nombres else [str(i) for i in range(n)]
        self._W = Matriz(n, n, INF)
        for i in range(n):
            self._W.establecer(i, i, 0)
        self._m = 0

    @property
    def n(self):
        return self._n

    @property
    def m(self):
        return self._m

    @property
    def dirigido(self):
        return self._dirigido

    def nombre(self, u):
        self._ver(u)
        return self._nombres[u]

    def _ver(self, *vs):
        for v in vs:
            if not (0 <= v < self._n):
                raise VerticeInexistenteError(f"vértice {v} no existe")

    def agregar_arista(self, u, v, peso):
        self._ver(u, v)
        if u == v or peso <= 0:
            raise ValueError("bucle o peso no positivo")
        if self._W.obtener(u, v) == INF:
            self._m += 1
        self._W.establecer(u, v, peso)
        if not self._dirigido:
            self._W.establecer(v, u, peso)

    def eliminar_arista(self, u, v):
        self._ver(u, v)
        if self._W.obtener(u, v) == INF:
            return False
        self._W.establecer(u, v, INF)
        if not self._dirigido:
            self._W.establecer(v, u, INF)
        self._m -= 1
        return True

    def existe_arista(self, u, v):
        self._ver(u, v)
        return u != v and self._W.obtener(u, v) != INF

    def peso(self, u, v):
        self._ver(u, v)
        if not self.existe_arista(u, v):
            raise KeyError((u, v))
        return self._W.obtener(u, v)

    def vecinos(self, u):
        self._ver(u)
        return [(v, self._W.obtener(u, v)) for v in range(self._n)
                if v != u and self._W.obtener(u, v) != INF]

    def lista_aristas(self):
        res = []
        for u in range(self._n):
            for v in range(self._n):
                if u != v and self._W.obtener(u, v) != INF and (self._dirigido or u < v):
                    res.append((u, v, self._W.obtener(u, v)))
        return res

    def a_matriz(self):
        return self._W.copia()

    @classmethod
    def desde_aristas(cls, n, aristas, dirigido=False, nombres=None):
        g = cls(n, dirigido, nombres)
        for u, v, w in aristas:
            g.agregar_arista(u, v, w)
        return g

    @classmethod
    def desde_grafo(cls, g):
        nombres = [g.nombre(i) for i in range(g.n)]
        return cls.desde_aristas(g.n, g.lista_aristas(), g.dirigido, nombres)
