# Classi per la simulazione dei Quantum Random Walks, usando il formalismo della matrice densità.

import numpy as np
import random

from walks_core import physics_utilities as ph
from walks_core import anello as an

class walker:
    def __init__(self, anello_ospite: an.anello, posizione_iniziale: int, moneta_iniziale: np.array, operatori_kraus:list=None):
        # L'anello va passato come oggetto.
        if operatori_kraus is None:
            operatori_kraus = []
        self.anello_ospite = anello_ospite

        # La posizione iniziale si può passare sia come vettore che come numero.
        if not ph.is_np_array(posizione_iniziale):
            stato_posizione_iniziale = np.zeros(anello_ospite.numero_punti)
            stato_posizione_iniziale[posizione_iniziale] = 1.
        else:
            stato_posizione_iniziale = posizione_iniziale

        # Vettore di stato.
        self.vettore_stato = np.kron(stato_posizione_iniziale, moneta_iniziale)
        # Matrice di stato.
        self.matrice_densita = np.outer(self.vettore_stato, self.vettore_stato)

        # Prepara gli operatori di cammino.
        coin_up = np.array([1, 0])
        coin_down = np.array([0, 1])

        proj_up = np.outer(coin_up, coin_up)
        proj_down = np.outer(coin_down, coin_down)
        mix_up_down = np.outer(coin_up, coin_down)
        mix_down_up = np.outer(coin_down, coin_up)

        # Matrici di spostamento.
        to_right = np.eye(self.anello_ospite.numero_punti, k=1)
        to_left = np.eye(self.anello_ospite.numero_punti, k=-1)

        # Correzioni per la topologia ad anello.
        to_right[self.anello_ospite.numero_punti - 1][0] = 1
        to_left[0][self.anello_ospite.numero_punti - 1] = 1

        # Unitaria di spostamento.
        conditional_shift = np.kron(to_right, proj_up) + np.kron(to_left, proj_down)

        # Parametro della moneta.
        theta = np.pi / 4

        # Unitaria di coin flip.
        coin_flip = np.cos(theta) * proj_up - 1j * np.sin(theta) * mix_up_down - 1j * np.sin(theta) * mix_down_up + np.cos( theta) * proj_down
        total_coin_flip = np.kron(np.eye(self.anello_ospite.numero_punti), coin_flip)

        # Operatore totale di passo.
        self.operatore_passo = conditional_shift.dot(total_coin_flip)

        # Occorre fornire gli operatori di Kraus per la mappa quantistica che si vuole applicare.
        # Gli operatori vanni forniti come Python list.
        self.operatori_kraus = operatori_kraus

        # print("WK: Preparazione operatori riuscita.")

    def passo(self):
        # Prima di tutto applica gli operatori di Kraus sullo stato.
        accu_matrice_densita = np.zeros((self.anello_ospite.numero_punti * 2, self.anello_ospite.numero_punti * 2))
        for kraus in self.operatori_kraus:
            # .conj().T è la funzione di "daga" (= hermitian conjugate) di numpy (per gli array!).
            accu_matrice_densita = accu_matrice_densita + kraus.dot(self.matrice_densita.dot(kraus.conj().T))
        self.matrice_densita = accu_matrice_densita

        # Applica l'evoluzione unitaria.
        self.matrice_densita = self.operatore_passo.dot(self.matrice_densita.dot(self.operatore_passo.conj().T))

    def esegui_misura(self) -> float:
        # Kernel del Montecarlo. Uso una tecnica accept-reject.
        # Estraggo x uniformemente tra i punti.
        flag_individuato = False
        while not flag_individuato:
            x = random.randrange(0,self.anello_ospite.numero_punti)
            # print("WK: provo valore ", x, ".")
            ddp, max_probabilita = self.ottieni_distribuzione_probabilita()
            # print("WK: distribuzione ", ddp, ".")
            y = random.uniform(0,max_probabilita)
            flag_individuato = (y < ddp[x])
        # Alla fine della procedura ottengo quindi un numero x da usare, distribuito secondo la ddp.
        # print("WK: Estratto valore ", x, " da misura.")
        return x

    def ottieni_distribuzione_probabilita(self) -> (np.array,float):
        # Calcola la ddp associata alle posizioni correnti.
        distribuzione = np.zeros(self.anello_ospite.numero_punti)
        for k in range(0, self.anello_ospite.numero_punti):
            vettore_posizioni = np.zeros(self.anello_ospite.numero_punti)
            vettore_posizioni[k] = 1.
            proj_posizione = np.outer(vettore_posizioni, vettore_posizioni)
            proj_tot_posizione = np.kron(proj_posizione, np.eye(2))
            # In formalismo matriciale occorre usare la traccia.
            distribuzione[k] = np.trace(proj_tot_posizione.dot(self.matrice_densita))
        return distribuzione, max(distribuzione)

