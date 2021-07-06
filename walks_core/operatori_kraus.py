# Questa classe descrive i modelli di rumore da applicare.
# L'obiettivo è costruire una lista di operatori di Kraus per il canale considerato.
# Il canale è descritto dalla classe astratta canale.

import numpy as np
import matrici_pauli as mp
import abc

class canale:
    def __init__(self, dimensioni_anello):
        self.dimensioni_anello  = dimensioni_anello
    @abc.abstractmethod
    def lista_operatori_kraus(self) -> list:
        pass

class canale_depolarizzatore(canale):
    def __init__(self, parametro: float, dimensioni_anello: int):
        super().__init__(dimensioni_anello)
        self.parametro = parametro

    def lista_operatori_kraus(self) -> list:
        # Definisco le matrici di Pauli.

        kr1 = np.sqrt(1 - 3/4 * self.parametro) * mp.sigma_0
        kr2 = np.sqrt(self.parametro/4) * mp.sigma_1
        kr3 = np.sqrt(self.parametro/4) * mp.sigma_2
        kr4 = np.sqrt(self.parametro/4) * mp.sigma_3

        # Applico il prodotto tensore per rendere utilizzabili.
        kr1 = np.kron(np.eye(self.dimensioni_anello), kr1)
        kr2 = np.kron(np.eye(self.dimensioni_anello), kr2)
        kr3 = np.kron(np.eye(self.dimensioni_anello), kr3)
        kr4 = np.kron(np.eye(self.dimensioni_anello), kr4)

        return [kr1, kr2, kr3, kr4]

class bit_flip(canale):
    def __init__(self, parametro: float, dimensioni_anello:int):
        self.dimensioni_anello = dimensioni_anello
        self.parametro = parametro

    def lista_operatori_kraus(self) -> list:
        kr0 = np.sqrt(self.parametro) * np.eye(2)
        kr1 = np.sqrt(1-self.parametro) * mp.sigma_1

        # Tensorizzo con l'identità sul position space.
        kr0 = np.kron(np.eye(self.dimensioni_anello),kr0)
        kr1 = np.kron(np.eye(self.dimensioni_anello),kr1)

        return [kr0, kr1]


class phase_flip(canale):
    def __init__(self, parametro: float, dimensioni_anello: int):
        self.dimensioni_anello = dimensioni_anello
        self.parametro = parametro

    def lista_operatori_kraus(self) -> list:
        kr0 = np.sqrt(self.parametro) * np.eye(2)
        kr1 = np.sqrt(1 - self.parametro) * mp.sigma_3

        # Tensorizzo con l'identità sul position space.
        kr0 = np.kron(np.eye(self.dimensioni_anello), kr0)
        kr1 = np.kron(np.eye(self.dimensioni_anello), kr1)

        return [kr0, kr1]

class bit_phase_flip(canale):
    def __init__(self, parametro: float, dimensioni_anello: int):
        self.dimensioni_anello = dimensioni_anello
        self.parametro = parametro

    def lista_operatori_kraus(self) -> list:
        kr0 = np.sqrt(self.parametro) * np.eye(2)
        kr1 = np.sqrt(1 - self.parametro) * mp.sigma_2

        # Tensorizzo con l'identità sul position space.
        kr0 = np.kron(np.eye(self.dimensioni_anello), kr0)
        kr1 = np.kron(np.eye(self.dimensioni_anello), kr1)

        return [kr0, kr1]