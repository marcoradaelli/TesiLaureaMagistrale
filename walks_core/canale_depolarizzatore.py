# Questa classe descrive un canale depolarizzatore da applicare al coin.
# L'obiettivo è costruire una lista di operatori di Kraus per il canale.

import numpy as np

class canale_depolarizzatore:
    def __init__(self, parametro: float, dimensioni_anello: int):
        self.parametro = parametro
        self.dimensioni_anello = dimensioni_anello

    def lista_operatori_kraus(self) -> list:
        # Definisco le matrici di Pauli.
        sigma_0 = np.eye(2)
        sigma_1 = np.array([[0,1],[1,0]])
        sigma_2 = np.array([[0,-1j],[1j,0]])
        sigma_3 = np.array([[1,0],[0,-1]])

        kr1 = np.sqrt(1 - 3/4 * self.parametro) * sigma_0
        kr2 = np.sqrt(self.parametro/4) * sigma_1
        kr3 = np.sqrt(self.parametro/4) * sigma_2
        kr4 = np.sqrt(self.parametro/4) * sigma_3

        # Applico il prodotto tensore per rendere utilizzabili.
        kr1 = np.kron(np.eye(self.dimensioni_anello), kr1)
        kr2 = np.kron(np.eye(self.dimensioni_anello), kr2)
        kr3 = np.kron(np.eye(self.dimensioni_anello), kr3)
        kr4 = np.kron(np.eye(self.dimensioni_anello), kr4)

        return [kr1, kr2, kr3, kr4]