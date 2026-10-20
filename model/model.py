import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self.lista_nodi_totale = DAO.getAllNodes()

        self.idMapObject = {}
        for nodo in self.lista_nodi_totale:
            self.idMapObject[nodo.id] = nodo

        self._grafo = nx.DiGraph()


    def lista_all_generi(self):
        lista_generi = DAO.getAllGeneri()
        return lista_generi


    def crea_grafo(self, genere):
        self._grafo.clear()

        lista_id = DAO.getNodi(genere)

        lista_nodi = []

        for id_nodo in lista_id:
            nodo = self.idMapObject[id_nodo]
            lista_nodi.append(nodo)

        self._grafo.add_nodes_from(lista_nodi)

        for nodo in list(self._grafo.nodes()):
            DAO.fillAttori(nodo)

        self.add_archi()

    def add_archi(self):
        lista_nodi = list(self._grafo.nodes())

        for i in range(len(lista_nodi)):
            for j in range(i + 1, len(lista_nodi)):

                f1 = lista_nodi[i]
                f2 = lista_nodi[j]
                lista_attori_f1 = f1.lista_attori
                lista_attori_f2 = f2.lista_attori

                count = 0
                for attore1 in lista_attori_f1:
                    for attore2 in lista_attori_f2:
                        if attore1 == attore2:
                            count += 1


                if count > 0:
                    if f1.year is not None and f2.year is not None:
                        if f1.year <= f2.year:
                            self._grafo.add_edge(f1,f2)
                        if f1.year >= f2.year:
                            self._grafo.add_edge(f2, f1)
                    else:
                        self._grafo.add_edge(f1, f2)
                        self._grafo.add_edge(f2, f1)




    #def numero_film_in_componente_connessa_max(self):
     #   return len(max(nx.connected_components(self._grafo), key=len))

    def numero_componenti_connesse(self):
        return nx.number_weakly_connected_components(self._grafo)


    def film_maggiore_archi_uscenti(self):
        conto_ottimo = None
        film = None
        for nodo in list(self._grafo.nodes()):
            num_archi = len(list(self._grafo.neighbors(nodo)))
            if conto_ottimo is None:
                conto_ottimo = num_archi
                film = nodo
            if num_archi > conto_ottimo:
                conto_ottimo = num_archi
                film = nodo

        return film, conto_ottimo

    def numero_film_in_componente_connessa_max(self):
       return len(max(nx.weakly_connected_components(self._grafo), key=len))

    def info_componente_connessa_maggiore(self):
        lista_nodi = list(max(nx.weakly_connected_components(self._grafo), key=len))
        lista_ordinata = sorted(lista_nodi, key=lambda nodo: nodo.numero_attori_recitanti(), reverse=True)
        return lista_ordinata



    def crea_ricorsione(self, source, N):
        self.soluzione = []
        self.votazione_ottima = None

        self._grafo_non_orientato = self._grafo.to_undirected()

        self.dizionario = {}
        for nodo in list(self._grafo.nodes()):
            self.dizionario[nodo] = nx.node_connected_component(self._grafo_non_orientato, nodo)

        self.ricorsione([source], N)

        return self.soluzione, self.votazione_ottima

    def ricorsione(self, parziale, N):
        if len(parziale) == N:
            if self.votazione_ottima is None:
                self.soluzione = copy.deepcopy(parziale)
                self.votazione_ottima = self.calcola_somma_voti_lista(parziale)
            if self.calcola_somma_voti_lista(parziale) > self.votazione_ottima:
                self.soluzione = copy.deepcopy(parziale)
                self.votazione_ottima = self.calcola_somma_voti_lista(parziale)
            return

        for nodo_candidato in list(self._grafo.nodes):

            if self.is_ammissibile2(nodo_candidato, parziale):
                parziale.append(nodo_candidato)
                self.ricorsione(parziale, N)
                parziale.pop()


    def is_ammissibile(self, nodo_candidato, parziale):
        ammissibile = True
        set_connesso = nx.node_connected_component(self._grafo, nodo_candidato)
        set_parziale = set(parziale)

        set_comune = set_connesso & set_parziale
        if len(set_comune) != 0:
            ammissibile = False

        return ammissibile

    def lista_nodi_connessi_a_source(self, source):
        set_nuovo = set()
        for nodo in list(self._grafo.nodes):
            if self._grafo.has_edge(nodo, source) or self._grafo.has_edge(source,nodo):
                set_nuovo.add(nodo)
        return set_nuovo


    def is_ammissibile2(self, nodo_candidato, parziale):
        ammissibile = True
        set_candidato = self.dizionario[nodo_candidato]

        set_parziale = set(parziale)

        set_comuni = set_candidato & set_parziale

        if len(set_comuni) != 0:
            ammissibile = False
        if nodo_candidato in parziale:
            ammissibile = False



        return ammissibile


    def calcola_somma_voti_lista(self, lista):
        count = 0
        for film in lista:
            if film.avg_rating is not None:
                count += film.avg_rating

        return count


    def ordina_listaFilm_per_titolo(self, lista):
        lista_ordinata = sorted(lista, key=lambda film : film.title)
        return lista_ordinata

    def lista_film_completa(self):
        lista_film = list(self._grafo.nodes())
        lista_ordinata = sorted(lista_film, key=lambda film: film.title)
        return lista_ordinata























    def return_lista_nodi(self):
        return list(self._grafo.nodes())

    def num_nodi(self):
        return len(self._grafo.nodes)

    def num_archi(self):
        return len(self._grafo.edges)