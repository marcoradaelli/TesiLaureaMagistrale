# Classi per la simulazione dei Classical Random Walks.

import numpy as np
import random
from walks_core import anello as an

from walks_core import physics_utilities as ph


class walker:
    def __init__(self, anello_ospite: an.anello, posizione_iniziale: int):
        # L'anello va passato come oggetto.
        self.anello_ospite = anello_ospite

        # La posizione iniziale si può passare sia come vettore che come numero.
        if not ph.is_np_array(posizione_iniziale):
            stato_posizione_iniziale = np.zeros(anello_ospite.numero_punti)
            stato_posizione_iniziale[posizione_iniziale] = 1.
        else:
            stato_posizione_iniziale = posizione_iniziale

        # Vettore di stato.
        self.stato = stato_posizione_iniziale

        # Prepara la matrice di transizione.
        self.matrice_transizione = 1/2 * np.eye(anello_ospite.numero_punti,k=1) + 1/2 * np.eye(anello_ospite.numero_punti,k=-1)
        # Correggo per la topologia ad anello.
        self.matrice_transizione[anello_ospite.numero_punti - 1,0] = 1/2
        self.matrice_transizione[0, anello_ospite.numero_punti-1] = 1/2

    def passo(self):
        self.stato = self.matrice_transizione.dot(self.stato)
        # print("WK: Eseguito passo.")

    def esegui_misura(self):
        # Kernel del Montecarlo. Uso una tecnica accept-reject.
        # Estraggo x uniformemente tra i punti.
        flag_individuato = False
        while not flag_individuato:
            x = random.randrange(0,self.anello_ospite.numero_punti)
            # print("WK: provo valore ", x, ".")
            ddp, max_probabilita = self.ottieni_distribuzione_probabilita()
            # print("WK: distribuzione_quantistica ", ddp, ".")
            y = random.uniform(0,max_probabilita)
            flag_individuato = (y < ddp[x])
        # Alla fine della procedura ottengo quindi un numero x da usare, distribuito secondo la ddp.
        # print("WK: Estratto valore ", x, " da misura.")
        return x

    def ottieni_distribuzione_probabilita(self):
        # Calcola la ddp associata alle posizioni correnti.
        distribuzione = self.stato
        return distribuzione, max(distribuzione)

