"""TAD Nodo y Arista (lista de adyacencia)."""
from collections import namedtuple

Arista = namedtuple("Arista", ["destino", "peso"])


class Nodo:
    def __init__(self, indice, nombre):
        if not nombre:
            raise ValueError("nombre vacío")
        self.indice = indice
        self.nombre = nombre
        self._adyacentes = []  # list[Arista]

    def agregar_adyacente(self, d, p):
        for k, a in enumerate(self._adyacentes):
            if a.destino == d:
                self._adyacentes[k] = Arista(d, p)
                return
        self._adyacentes.append(Arista(d, p))

    def quitar_adyacente(self, d):
        for k, a in enumerate(self._adyacentes):
            if a.destino == d:
                self._adyacentes.pop(k)
                return True
        return False

    def peso_hacia(self, d):
        for a in self._adyacentes:
            if a.destino == d:
                return a.peso
        return None

    def adyacentes(self):
        return list(self._adyacentes)

    @property
    def grado(self):
        return len(self._adyacentes)
