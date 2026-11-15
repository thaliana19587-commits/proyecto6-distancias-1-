import os, sys, random, unittest
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(RAIZ, "src"), os.path.join(RAIZ, "bench")]

from grafo import Grafo, INF, VerticeInexistenteError
from grafo_matriz import GrafoMatriz
from matriz import Matriz
from floyd_warshall import floyd_warshall, reconstruir_camino, longitud_camino
from cargar_csv import cargar_grafo, cargar_grafo_matriz
from generador import aristas_aleatorias

CSV = os.path.join(RAIZ, "data", "red_alto_magdalena.csv")


class TestMatriz(unittest.TestCase):
    def test_basico(self):
        m = Matriz(2, 3, 0)
        m.establecer(1, 2, 7)
        self.assertEqual(m.obtener(1, 2), 7)
        c = m.copia(); c.establecer(0, 0, 9)
        self.assertEqual(m.obtener(0, 0), 0)
        with self.assertRaises(IndexError):
            m.obtener(2, 0)


class TestGrafos(unittest.TestCase):
    def test_grafo_lista(self):
        g = Grafo()
        a, b = g.agregar_vertice("A"), g.agregar_vertice("B")
        g.agregar_arista(a, b, 3)
        self.assertEqual((g.m, g.peso(b, a), g.grado(a)), (1, 3, 1))
        self.assertTrue(g.eliminar_arista(a, b))
        self.assertEqual(g.m, 0)
        with self.assertRaises(VerticeInexistenteError):
            g.peso(0, 5)
        with self.assertRaises(ValueError):
            g.agregar_arista(a, b, -1)

    def test_grafo_matriz_igual_a_lista(self):
        n = 30
        ar = aristas_aleatorias(n, 0.2, 1)
        gm = GrafoMatriz.desde_aristas(n, ar)
        gl = Grafo()
        for i in range(n):
            gl.agregar_vertice(str(i))
        for u, v, w in ar:
            gl.agregar_arista(u, v, w)
        self.assertEqual(gm.m, gl.m)
        self.assertEqual(sorted(gm.lista_aristas()), sorted(gl.lista_aristas()))
        self.assertEqual(gm.a_matriz().a_listas(), gl.a_matriz().a_listas())


class TestFloydWarshall(unittest.TestCase):
    def test_red_real_resultados_del_informe(self):
        g = cargar_grafo(CSV)
        i = g.indice
        D, S = floyd_warshall(g)
        self.assertEqual(D.obtener(i("Flandes"), i("Tocaima")), 23 + 5)
        self.assertEqual(reconstruir_camino(S, i("Flandes"), i("Tocaima")),
                         [i("Flandes"), i("Girardot"), i("Agua de Dios"), i("Tocaima")])
        self.assertEqual(D.obtener(i("Nilo"), i("Guataquí")), 51)
        self.assertEqual(reconstruir_camino(S, i("Nilo"), i("Guataquí")),
                         [i(x) for x in ("Nilo", "Ricaurte", "Girardot", "Nariño", "Guataquí")])
        self.assertEqual(D.obtener(i("Girardot"), i("Guataquí")), 36)

    def test_lista_y_matriz_dan_lo_mismo(self):
        g = cargar_grafo(CSV)
        gm = cargar_grafo_matriz(CSV)
        self.assertEqual(floyd_warshall(g)[0].a_listas(), floyd_warshall(gm)[0].a_listas())

    def test_sin_camino_y_mismo_vertice(self):
        g = GrafoMatriz.desde_aristas(4, [(0, 1, 2), (2, 3, 5)])
        D, S = floyd_warshall(g)
        self.assertEqual(D.obtener(0, 3), INF)
        self.assertEqual(reconstruir_camino(S, 0, 3), [])
        self.assertEqual(reconstruir_camino(S, 2, 2), [2])
        with self.assertRaises(IndexError):
            reconstruir_camino(S, 0, 9)

    def test_dirigido(self):
        g = GrafoMatriz.desde_aristas(3, [(0, 1, 1), (1, 2, 1)], dirigido=True)
        D, S = floyd_warshall(g)
        self.assertEqual(D.obtener(0, 2), 2)
        self.assertEqual(D.obtener(2, 0), INF)

    def test_contra_networkx_y_caminos_consistentes(self):
        import networkx as nx
        for n, dens, sem in [(20, 0.1, 1), (40, 0.3, 2), (60, 0.7, 3)]:
            ar = aristas_aleatorias(n, dens, sem)
            gm = GrafoMatriz.desde_aristas(n, ar)
            D, S = floyd_warshall(gm)
            G = nx.Graph()
            G.add_nodes_from(range(n))
            G.add_weighted_edges_from(ar)
            ref = dict(nx.floyd_warshall(G))
            for u in range(n):
                for v in range(n):
                    self.assertEqual(D.obtener(u, v), ref[u][v])
                    p = reconstruir_camino(S, u, v)
                    self.assertEqual(p[0], u); self.assertEqual(p[-1], v)
                    self.assertEqual(longitud_camino(gm, p), D.obtener(u, v))


if __name__ == "__main__":
    unittest.main()
