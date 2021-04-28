import numpy as np
import networkx as nx
from matplotlib import pyplot as plt

class grafo:
    def __init__(self, matrice_adiacenza: np.array, disegna_grafo = False, controlla_regolare = False):
        self.matrice_adiacenza = matrice_adiacenza
        self.matrice_adiacenza = matrice_adiacenza
        self.numero_vertici = len(matrice_adiacenza)
        if controlla_regolare:
            self.ottieni_grado() # La funzione salva il grado nel membro di classe.

        if disegna_grafo:
            self.disegna_grafo()

    def ottieni_grado(self):
        # Ricavo un candidato grado dalla prima riga.
        candidato_grado = 0
        for el in self.matrice_adiacenza[0]:
            candidato_grado += el

        # E poi controllo tutte le righe.
        for riga in self.matrice_adiacenza:
            somma_riga = 0
            for el in riga:
                somma_riga += el
            if somma_riga != candidato_grado:
                raise Exception("Il grafo non è regolare!")

        self.grado = candidato_grado
        return int(candidato_grado)

    def disegna_grafo(self):
        nx_grafo = nx.from_numpy_array(self.matrice_adiacenza)
        nx.draw(nx_grafo, cmap=plt.get_cmap('jet'))
        plt.show()

    def ricava_matrice_coin_shift(self):
        pass

    def trova_grado_nodi(self) -> np.array:
        vettore_gradi = []
        for v, vertice in enumerate(self.matrice_adiacenza):
            accu_grado = 0
            for altro_vertice in self.matrice_adiacenza[v]:
                accu_grado += altro_vertice
            vettore_gradi.append(accu_grado)
        return np.array(vettore_gradi)

    def lista_adiacenza(self) -> np.array:
        vettore_nodi = []
        for v, nodo in enumerate(self.matrice_adiacenza):
            lista_adiacenza_nodo = []
            for n, altro_nodo in enumerate(self.matrice_adiacenza[v]):
                if altro_nodo == 1:
                    # Se c'è collegamento.
                    lista_adiacenza_nodo.append(n)
            lista_adiacenza_nodo = np.array(lista_adiacenza_nodo)
            vettore_nodi.append(lista_adiacenza_nodo)
        vettore_nodi = np.array(vettore_nodi)

        return np.array(vettore_nodi)

# Classi figlie per particolari tipi di grafo.

class grafo_anello(grafo):
    def __init__(self, numero_punti: int, disegna_grafo: bool = False):
        matrice_adiacenza = np.eye(numero_punti, k=-1) + np.eye(numero_punti, k=1)
        matrice_adiacenza[numero_punti - 1, 0] = 1
        matrice_adiacenza[0, numero_punti - 1] = 1
        super().__init__(matrice_adiacenza, disegna_grafo=disegna_grafo)

class grafo_completo(grafo):
    def __init__(self, numero_punti: int, disegna_grafo: bool = False):
        matrice_adiacenza = np.ones((numero_punti, numero_punti)) - np.eye(numero_punti)
        super().__init__(matrice_adiacenza, disegna_grafo=disegna_grafo)