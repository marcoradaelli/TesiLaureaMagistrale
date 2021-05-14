# Questa classe simula un classical random walk continuo su un grafo arbitrario.

from Grafi import grafi
import numpy as np
import scipy
import random

class walker:
    def __init__(self, grafo_ospite: grafi.grafo, posizione_iniziale: int):
        self.grafo_ospite = grafo_ospite
        self.laplaciano = self.grafo_ospite.ottieni_laplaciano()
        self.posizione_iniziale = posizione_iniziale
        self.stato_iniziale = np.zeros(self.grafo_ospite.numero_vertici)
        self.stato_iniziale[self.posizione_iniziale] = 1
        self.matrice_trasferimento = grafo_ospite.ottieni_laplaciano()

    def ottieni_distribuzione_probabilita_a_tempo(self, tempo:float):
        operatore_evoluzione = scipy.linalg.expm(- self.matrice_trasferimento * tempo)
        stato = operatore_evoluzione.dot(self.stato_iniziale)

        # Calcolo la distribuzione di probabilità.
        return stato

    def esegui_misura_a_tempo(self,tempo:float):
        flag_individuato = False
        while not flag_individuato:
            x = random.randrange(0, self.grafo_ospite.numero_vertici)
            # print("WK: provo valore ", x, ".")
            ddp = self.ottieni_distribuzione_probabilita_a_tempo(tempo=tempo)
            # print("WK: distribuzione ", ddp, ".")
            y = random.uniform(0, max(ddp))
            flag_individuato = (y < ddp[x])
        # Alla fine della procedura ottengo quindi un numero x da usare, distribuito secondo la ddp.
        # print("WK: Estratto valore ", x, " da misura.")
        return x
