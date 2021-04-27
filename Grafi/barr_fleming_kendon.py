# Codice riferito all'articolo di Barr et al, "Simulation methods for quantum walks on graphs
# applied to formal language recognition" e liberamento ispirato all'implementazione Python di
# K. Barr nella tesi di PhD disponibile su https://etheses.whiterose.ac.uk/4975/1/kbarrfinalthesis.pdf

import numpy as np
from Grafi import grafi

# Algoritmo di Barr-Fleming-Kendon. Usa una moneta DFT (che cos'è?).
def crea_moneta(grafo: grafi.grafo):
    gradi_vertici = grafo.trova_grado_nodi()
    numero_stati_moneta = int(np.sum(gradi_vertici))

    moneta_totale = [[0 for i in range(numero_stati_moneta)] for j in range(numero_stati_moneta)]
    gia_popolati = 0

    for vertice in range(grafo.numero_vertici):
        grado = int(gradi_vertici[vertice])
        mat = [[0 for j in range(grado)] for k in range(grado)]
        for j in range(len(mat)):
            mat[j][j] = 1
        coin = np.fft.fft(mat)
        for j in range(len(coin)):
            for k in range(len(coin[j])):
                coin[j][k] = (1./np.sqrt(grado)) * coin[j][k]
        for j in range(len(coin)):
            for k in range(len(coin)):
                moneta_totale[gia_popolati + j][gia_popolati + k] = coin[j][k]
        gia_popolati += grado

    return moneta_totale