# Classi per la simulazione dei Quantum Random Walks su grafi regolari.

import numpy as np
import random

from walks_core import physics_utilities as ph
from Grafi import grafi, generatore_matrici_grafi_regolari as gmgr

class walker:
    def __init__(self, grafo_ospite: grafi.grafo, posizione_iniziale, moneta_iniziale=None):
        # L'anello va passato come oggetto.
        self.grafo_ospite = grafo_ospite

        # La posizione iniziale si può passare sia come vettore che come numero.
        if not ph.is_np_array(posizione_iniziale):
            stato_posizione_iniziale = np.zeros(grafo_ospite.numero_vertici)
            stato_posizione_iniziale[posizione_iniziale] = 1.
        else:
            stato_posizione_iniziale = posizione_iniziale

        # Se non viene passata la moneta iniziale.
        if moneta_iniziale is None:
            moneta_iniziale = np.zeros(self.grafo_ospite.ottieni_grado())
            moneta_iniziale[0] = 1

        # Vettore di stato.
        self.stato_totale = np.kron(stato_posizione_iniziale, moneta_iniziale)

        # Lista delle matrici di spostamento.
        self.lista_matrici_spostamento = gmgr.genera_matrici_spostamento(grafo=self.grafo_ospite)

        # Proiettori sugli stati di base della moneta.
        self.lista_proiettori_stati_base_moneta = gmgr.genera_proiettori_base_moneta(grafo=self.grafo_ospite)

        # Unitaria di spostamento.
        conditional_shift = np.zeros((len(self.stato_totale), len(self.stato_totale)))
        for stato_moneta in range(len(self.lista_matrici_spostamento)):
            conditional_shift += np.kron(self.lista_matrici_spostamento[stato_moneta], self.lista_proiettori_stati_base_moneta[stato_moneta])

        # Unitaria di coin flip.
        coin_flip = gmgr.genera_matrice_coin(grafo=self.grafo_ospite)
        total_coin_flip = np.kron(np.eye(self.grafo_ospite.numero_vertici), coin_flip)

        self.operatore_passo = conditional_shift.dot(total_coin_flip)
        # print("WK: Preparazione operatori riuscita.")

    def passo(self):
        self.stato_totale = self.operatore_passo.dot(self.stato_totale)
        # print("WK: Eseguito passo.")

    def esegui_misura(self):
        # Kernel del Montecarlo. Uso una tecnica accept-reject.
        # Estraggo x uniformemente tra i punti.
        # TODO: provare con random.choices, fornendo i pesi.
        flag_individuato = False
        while not flag_individuato:
            x = random.randrange(0, self.grafo_ospite.numero_vertici)
            # print("WK: provo valore ", x, ".")
            ddp, max_probabilita = self.ottieni_distribuzione_probabilita()
            # print("WK: distribuzione ", ddp, ".")
            y = random.uniform(0,max_probabilita)
            flag_individuato = (y < ddp[x])
        # Alla fine della procedura ottengo quindi un numero x da usare, distribuito secondo la ddp.
        # print("WK: Estratto valore ", x, " da misura.")
        return x

    def ottieni_distribuzione_probabilita(self):
        # Calcola la ddp associata alle posizioni correnti.
        distribuzione = np.zeros(self.grafo_ospite.numero_vertici)
        for k in range(0, self.grafo_ospite.numero_vertici):
            vettore_posizioni = np.zeros(self.grafo_ospite.numero_vertici)
            vettore_posizioni[k] = 1.
            proj_posizione = np.outer(vettore_posizioni, vettore_posizioni)
            proj_tot_posizione = np.kron(proj_posizione, np.eye(self.grafo_ospite.ottieni_grado()))
            distribuzione[k] = pow(np.linalg.norm(proj_tot_posizione.dot(self.stato_totale)),2)
        return distribuzione, max(distribuzione)

