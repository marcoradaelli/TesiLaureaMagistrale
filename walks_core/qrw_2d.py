# Classi per la simulazione dei Quantum Random Walks su un grafo illimitato bidimensionale.

import numpy as np
import random

from walks_core import physics_utilities as ph
from Grafi import barr_fleming_kendon as bfk

matrice_hadamard = 1/np.sqrt(2) * np.array([[1,1],[1,-1]])
matrice_unbiased = 1 / np.sqrt(2) * np.array([[1, -1j], [-1j, 1]])

class walker:
    def __init__(self, numero_punti_per_dimensione: int, tipo_moneta:str="hadamard", matrice_flip_moneta = None):
        self.numero_punti_per_dimensione = numero_punti_per_dimensione

        # Posizione iniziale.
        riga_punto_iniziale = self.numero_punti_per_dimensione//2
        colonna_punto_iniziale = self.numero_punti_per_dimensione//2
        print("Posizione iniziale: ", (riga_punto_iniziale, colonna_punto_iniziale))
        stato_orizzontale_iniziale = np.zeros(self.numero_punti_per_dimensione)
        stato_orizzontale_iniziale[riga_punto_iniziale] = 1.
        stato_verticale_iniziale = np.zeros(self.numero_punti_per_dimensione)
        stato_verticale_iniziale[colonna_punto_iniziale] = 1.
        stato_posizione_iniziale = np.kron(stato_orizzontale_iniziale, stato_verticale_iniziale)

        stato_moneta_orizzontale = np.zeros(2)
        stato_moneta_orizzontale[1] = 1.
        stato_moneta_verticale = np.zeros(2)
        stato_moneta_verticale[0] = 1.
        stato_moneta_iniziale = np.kron(stato_moneta_orizzontale, stato_moneta_verticale)
        
        self.stato_totale = np.kron(stato_posizione_iniziale, stato_moneta_iniziale)

        if tipo_moneta == "hadamard":
            operatore_coin = np.kron(matrice_hadamard, matrice_hadamard)
        elif tipo_moneta == "unbiased":
            operatore_coin = np.kron(matrice_unbiased, matrice_unbiased)
        elif tipo_moneta == "DFT":
            operatore_coin = bfk.matrice_coin_fft(4)
        elif tipo_moneta == "grover":
            operatore_coin = 1/2 * (np.ones(4) - 2 * np.eye(4))
        elif tipo_moneta == "personalizzata":
            if matrice_flip_moneta is None:
                raise Exception("Matrice di moneta personalizzata non inserita!")
            operatore_coin = matrice_flip_moneta
        else:
            raise Exception("Moneta non riconosciuta!")

        identita_posizioni = np.kron(np.eye(numero_punti_per_dimensione),np.eye(numero_punti_per_dimensione))
        self.operatore_totale_coin = np.kron(identita_posizioni,operatore_coin)

        print("Matrice di moneta unitaria? ", ph.verifica_matrice_unitaria(self.operatore_totale_coin))

        matrice_su = np.eye(numero_punti_per_dimensione, k=1)
        matrice_giu = np.eye(numero_punti_per_dimensione, k=-1)
        matrice_su[numero_punti_per_dimensione - 1][0] = 1
        matrice_giu[0][numero_punti_per_dimensione-1] = 1
        proiettore_su = np.array([[1,0],[0,0]])
        proiettore_giu = np.array([[0,0],[0,1]])

        shift_orizzontale_su = np.kron(matrice_su, np.eye(numero_punti_per_dimensione))
        shift_orizzontale_giu = np.kron(matrice_giu, np.eye(numero_punti_per_dimensione))
        shift_verticale_su = np.kron(np.eye(numero_punti_per_dimensione), matrice_su)
        shift_verticale_giu = np.kron(np.eye(numero_punti_per_dimensione), matrice_giu)

        shift_totale_orizzontale = np.kron(shift_orizzontale_su, np.kron(proiettore_su, np.eye(2))) + np.kron(shift_orizzontale_giu, np.kron(proiettore_giu, np.eye(2)))
        shift_totale_verticale = np.kron(shift_verticale_su, np.kron(np.eye(2), proiettore_su)) + np.kron(shift_verticale_giu, np.kron(np.eye(2), proiettore_giu))

        print("Matrice di shift verticale unitaria? ", ph.verifica_matrice_unitaria(shift_totale_verticale))
        print("Matrice di shift orizzontale unitaria? ", ph.verifica_matrice_unitaria(shift_totale_orizzontale))

        self.shift_totale = shift_totale_verticale.dot(shift_totale_orizzontale)

        print("Matrice di shift generale unitaria? ", ph.verifica_matrice_unitaria(self.shift_totale))

        self.operatore_passo = self.shift_totale.dot(self.operatore_totale_coin)

        print("WK: creati operatori. Dimensione totale operatore passo: ", np.shape(self.operatore_passo))

    def passo(self):
        self.stato_totale = self.operatore_passo.dot(self.stato_totale)
        # print("WK: norma del vettore stato ", np.linalg.norm(self.stato_totale))
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
        accu_probabilita = 0
        # Calcola la ddp associata alle posizioni correnti.
        distribuzione = np.zeros((self.numero_punti_per_dimensione, self.numero_punti_per_dimensione))
        for orizzontale in range(0, self.numero_punti_per_dimensione):
            # print("Avvio calcoli riga ", orizzontale)
            for verticale in range(0, self.numero_punti_per_dimensione):
                # print("Avvio calcoli colonna ", verticale)
                # Costruisco il proiettore sullo stato.
                vett_orizzontale = np.zeros(self.numero_punti_per_dimensione)
                vett_orizzontale[orizzontale] = 1
                vett_verticale = np.zeros(self.numero_punti_per_dimensione)
                vett_verticale[verticale] = 1
                vett_posizioni = np.kron(vett_orizzontale, vett_verticale)
                proj_posizione = np.outer(vett_posizioni, vett_posizioni)
                proj_tot_posizione = np.kron(proj_posizione, np.kron(np.eye(2), np.eye(2)))
                valore_posizione = pow(np.linalg.norm(proj_tot_posizione.dot(self.stato_totale)),2)
                distribuzione[verticale][orizzontale] = valore_posizione
                accu_probabilita += valore_posizione
        #print("Probabilità totale: ", accu_probabilita)
        return distribuzione

