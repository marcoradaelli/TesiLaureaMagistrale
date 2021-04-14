# Classi per la simulazione dei Quantum Random Walks.

import numpy as np
import random

import physics_utilities as ph

class anello:
    def __init__(self, numero_punti):
        self.numero_punti = numero_punti
        # print("AN: Creato anello di ", self.numero_punti, " punti.")

class walker:
    def __init__(self, anello_ospite, posizione_iniziale, moneta_iniziale):
        # L'anello va passato come oggetto.
        self.anello_ospite = anello_ospite

        # La posizione iniziale si può passare sia come vettore che come numero.
        if not ph.is_np_array(posizione_iniziale):
            stato_posizione_iniziale = np.zeros(anello_ospite.numero_punti)
            stato_posizione_iniziale[posizione_iniziale] = 1.
        else:
            stato_posizione_iniziale = posizione_iniziale

        # Vettore di stato.
        self.stato_totale = np.kron(stato_posizione_iniziale, moneta_iniziale)

        # print("WK: Impostazione condizioni iniziali riuscita.")

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
            x = random.randrange(0,self.anello_ospite.numero_punti)
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
        distribuzione = np.zeros(self.anello_ospite.numero_punti)
        for k in range(0, self.anello_ospite.numero_punti):
            vettore_posizioni = np.zeros(self.anello_ospite.numero_punti)
            vettore_posizioni[k] = 1.
            proj_posizione = np.outer(vettore_posizioni, vettore_posizioni)
            proj_tot_posizione = np.kron(proj_posizione, np.eye(2))
            distribuzione[k] = pow(np.linalg.norm(proj_tot_posizione.dot(self.stato_totale)),2)
        return distribuzione, max(distribuzione)

