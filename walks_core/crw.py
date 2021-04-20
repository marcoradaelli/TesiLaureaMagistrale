# Classi per la simulazione dei Classical Random Walks
import random


class anello:
    def __init__(self, numero_punti):
        self.numero_punti = numero_punti
        # print("AN: Creato anello di ", self.numero_punti, " punti.")


class walker:
    def __init__(self, anello_ospite, posizione_iniziale):
        self.anello_ospite = anello_ospite
        self.posizione_iniziale = posizione_iniziale
        self.posizione_attuale = posizione_iniziale

    def passo(self):
        # Estrae casualmente se muoversi verso destra o verso sinistra.
        x = random.choice([1, -1])
        self.posizione_attuale = (self.posizione_attuale + x) % self.anello_ospite.numero_punti

        # Nel caso classico la misura non comporta alcuna modifica dello stato, quindi restituisce la posizione.
        return self.posizione_attuale

    def esegui_misura(self):
        return self.posizione_attuale