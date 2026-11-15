"""TAD Grafo ponderado con lista de adyacencia."""
from nodo import Nodo, Arista
from matriz import Matriz

INF = float("inf")


class VerticeInexistenteError(IndexError):
    pass


class Grafo:
    def __init__(self, dirigido=False):
        self._dirigido = dirigido
        self._nodos = []
        self._por_nombre = {}
        self._num_aristas = 0

    @property
    def n(self):
        return len(self._nodos)

    @property
    def m(self):
        return self._num_aristas

    @property
    def dirigido(self):
        return self._dirigido

    def agregar_vertice(self, nombre):
        if not nombre or nombre in self._por_nombre:
            raise ValueError("nombre vacío o repetido")
        idx = len(self._nodos)
        self._nodos.append(Nodo(idx, nombre))
        self._por_nombre[nombre] = idx
        return idx

    def nombre(self, u):
        self._ver(u)
        return self._nodos[u].nombre

    def indice(self, nombre):
        return self._por_nombre[nombre]

    def _ver(self, *vs):
        for v in vs:
            if not (0 <= v < len(self._nodos)):
                raise VerticeInexistenteError(f"vértice {v} no existe")

    def agregar_arista(self, u, v, peso):
        self._ver(u, v)
        if u == v or peso <= 0:
            raise ValueError("bucle o peso no positivo")
        nueva = self._nodos[u].peso_hacia(v) is None
        self._nodos[u].agregar_adyacente(v, peso)
        if not self._dirigido:
            self._nodos[v].agregar_adyacente(u, peso)
        if nueva:
            self._num_aristas += 1

    def eliminar_arista(self, u, v):
        self._ver(u, v)
        existia = self._nodos[u].quitar_adyacente(v)
        if not self._dirigido:
            self._nodos[v].quitar_adyacente(u)
        if existia:
            self._num_aristas -= 1
        return existia

    def existe_arista(self, u, v):
        self._ver(u, v)
        return self._nodos[u].peso_hacia(v) is not None

    def peso(self, u, v):
        self._ver(u, v)
        p = self._nodos[u].peso_hacia(v)
        if p is None:
            raise KeyError((u, v))
        return p

    def vecinos(self, u):
        self._ver(u)
        return self._nodos[u].adyacentes()

    def grado(self, u):
        self._ver(u)
        return self._nodos[u].grado

    def lista_aristas(self):
        res = []
        for u, nodo in enumerate(self._nodos):
            for a in nodo._adyacentes:
                if self._dirigido or u < a.destino:
                    res.append((u, a.destino, a.peso))
        return res

    def a_matriz(self):
        """Matriz de distancias: 0 en la diagonal, w en aristas, INF en el resto."""
        n = len(self._nodos)
        W = Matriz(n, n, INF)
        for i in range(n):
            W.establecer(i, i, 0)
        for u, v, w in self.lista_aristas():
            W.establecer(u, v, w)
            if not self._dirigido:
                W.establecer(v, u, w)
        return W

    @classmethod
    def desde_aristas_unicas(cls, n, aristas, dirigido=False):
        """Carga masiva O(n + m) cuando se sabe que no hay aristas repetidas
        (evita la verificación O(deg) de agregar_arista; útil en los experimentos)."""
        g = cls(dirigido)
        for i in range(n):
            g.agregar_vertice(str(i))
        for u, v, w in aristas:
            g._nodos[u]._adyacentes.append(Arista(v, w))
            if not dirigido:
                g._nodos[v]._adyacentes.append(Arista(u, w))
            g._num_aristas += 1
        return g
