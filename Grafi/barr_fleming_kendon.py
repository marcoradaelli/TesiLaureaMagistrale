# Codice riferito all'articolo di Barr et al, "Simulation methods for quantum walks on graphs
# applied to formal language recognition" e liberamento ispirato all'implementazione Python di
# K. Barr nella tesi di PhD disponibile su https://etheses.whiterose.ac.uk/4975/1/kbarrfinalthesis.pdf

import numpy as np
from Grafi import grafi

def primo_nodo(lista_adiacenza) -> np.array:
    numero = 0
    array = [0 for i in range(len(lista_adiacenza))]
    for i in range(len(lista_adiacenza)):
        array[i] = numero
        numero += len(lista_adiacenza[i])
    return np.array(array)

# Algoritmo di Barr-Fleming-Kendon. Usa una moneta DFT (che cos'è?).
def crea_moneta(grafo: grafi.grafo) -> np.array:
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

def crea_operatore_shift(grafo: grafi.grafo) -> np.array:
    degree = grafo.lista_adiacenza()
    nodeindex = primo_nodo(degree)
    size = nodeindex[len(grafo.matrice_adiacenza) - 1] + len(degree[len(grafo.matrice_adiacenza) - 1])
    array = [[0 for i in range(size)] for j in range(size)]

    for i in range(len(degree)):
        index1 = nodeindex[i]
        for j in range(len(degree[i])):
            coinstate1 = index1 + j
            node = degree[i][j]
            for k in range(len(degree[node])):
                if degree[node][k] == i:
                    coinstate2 = nodeindex[node] + k
            array[coinstate1][coinstate2] = 1
    return array

def crea_moneta_2(grafo: grafi.grafo):
    # Vettore dei gradi dei nodi del grafo.
    grado_nodi = grafo.trova_grado_nodi()

    # Ciclo sui nodi creando le matrici di coin di singolo nodo e le inserisco in una lista.
    lista_matrici_coin_singolo_nodo = []
    for n,nodo in enumerate(grafo.matrice_adiacenza):
        lista_matrici_coin_singolo_nodo.append(matrice_coin_fft(grado_nodi[n]))

    # A questo punto esegue la somma diretta delle matrici della lista.
    return somma_diretta_da_lista(lista_matrici_coin_singolo_nodo)

# Fornisce la matrice di coin tramite fft specificate le dimensioni.
def matrice_coin_fft(dimensioni: int) -> np.array:
    dimensioni = int(dimensioni)
    mat = [[0 for j in range(dimensioni)] for k in range(dimensioni)]
    for j in range(len(mat)):
        mat[j][j] = 1
    coin = np.fft.fft(mat)
    # La matrice va opportunamente normalizzata.
    coin = coin / np.sqrt(dimensioni)
    print(coin)
    return coin

# Esegue la somma diretta di matrici di una lista.
def somma_diretta_da_lista(lista: list) -> np.array:
    # Determina la dimensione della matrice finale.
    dimensione = 0
    for matrice in lista:
        dimensione += len(matrice)
    # Crea la matrice.
    somma_diretta = np.zeros((dimensione, dimensione), dtype=complex)
    accu_posizione = 0
    for matrice in lista:
        for i in range(len(matrice)):
            for j in range(len(matrice)):

                somma_diretta[accu_posizione + i][accu_posizione + j] = matrice[i][j]
        accu_posizione += len(matrice)

    return somma_diretta