import networkx as nx
from database.DAO import DAO
from itertools import combinations


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodes = []
        self.idMap = {}
        self._solBest = []
        self._pesoBest = 0


    def buildGraph(self, genere, minimo):
        self._grafo.clear()
        self.idMap = {}

        self._nodes = DAO.getNodes(genere, minimo)
        for n in self._nodes:
            self.idMap[n.id] = n

        self._grafo.add_nodes_from(self._nodes)

        for idFilm, idPersona in DAO.getInterpreti():
            if idFilm in self.idMap:
                self.idMap[idFilm].interpreti.add(idPersona)

        for c1, c2 in combinations(self._nodes, 2):
            peso = len(c1.interpreti & c2.interpreti)
            if peso > 0:
                self._grafo.add_edge(c1, c2, weight=peso)

    def getNodes(self):
        return self._nodes

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getGeneri(self):
        return DAO.getAllGeneri()

    def getGradoMax(self):
        best = None
        for n in sorted(self._nodes, key=str):
            if best is None or self._grafo.degree(n) > self._grafo.degree(best):
                best = n
        return best, self._grafo.degree(best)

    def getPesoMax(self):
        best = None
        for n in sorted(self._nodes, key=str):
            if best is None or self._grafo.degree(n, weight="weight") > self._grafo.degree(best, weight="weight"):
                best = n
        return best, self._grafo.degree(best, weight="weight")

    def getComponenti(self):
        componenti = list(nx.connected_components(self._grafo))
        numero = len(componenti)
        piuGrande = 0
        for c in componenti:
            if len(c) > piuGrande:
                piuGrande = len(c)
        return numero, piuGrande

    def getTopArchi(self):
        archi = []
        for u, v, dati in self._grafo.edges(data=True):
            nomi = sorted([str(u), str(v)])
            archi.append((nomi[0], nomi[1], dati["weight"]))
        archi.sort(key=lambda x: (-x[2], x[0], x[1]))
        return archi[:3]


    def getNumComponenti(self):
        return nx.number_connected_components(self._grafo)  # GIUSTO: quante sono

    def getComponenteMax(self):
        componenti = list(nx.connected_components(self._grafo))
        piuGrande = max(componenti, key= len)
        return sorted(piuGrande, key=lambda x: (-self._grafo.degree(x), str(x)))
    def getGrado(self, film):
        return self._grafo.degree(film)

    def getCammino(self, partenza):
        self._solBest = []
        self._pesoBest = 0
        self._ricorsione([partenza])
        return self._solBest, self._pesoBest

    def _ricorsione(self, parziale):
        sommaVoti = 0
        for f in parziale:
            sommaVoti += f.total_votes

        if len(parziale) > len(self._solBest) or \
                (len(parziale) == len(self._solBest) and sommaVoti > self._pesoBest):
            self._pesoBest = sommaVoti
            self._solBest = list(parziale)

        ultimo = parziale[-1]
        for vicino in self._grafo.neighbors(ultimo):
            if vicino in parziale:
                continue
            if vicino.avg_rating > ultimo.avg_rating:
                parziale.append(vicino)
                self._ricorsione(parziale)
                parziale.pop()
