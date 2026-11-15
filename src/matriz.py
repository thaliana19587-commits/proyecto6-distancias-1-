"""TAD Matriz (arreglo bidimensional)."""


class Matriz:
    def __init__(self, filas, columnas, valor=0):
        if filas <= 0 or columnas <= 0:
            raise ValueError("dimensiones deben ser > 0")
        self._filas = filas
        self._columnas = columnas
        self._datos = [[valor] * columnas for _ in range(filas)]

    @property
    def filas(self):
        return self._filas

    @property
    def columnas(self):
        return self._columnas

    def _verificar(self, i, j):
        if not (0 <= i < self._filas and 0 <= j < self._columnas):
            raise IndexError(f"celda ({i}, {j}) fuera de rango")

    def obtener(self, i, j):
        self._verificar(i, j)
        return self._datos[i][j]

    def establecer(self, i, j, x):
        self._verificar(i, j)
        self._datos[i][j] = x

    def copia(self):
        m = Matriz(self._filas, self._columnas)
        m._datos = [fila[:] for fila in self._datos]
        return m

    def a_listas(self):
        return [fila[:] for fila in self._datos]
