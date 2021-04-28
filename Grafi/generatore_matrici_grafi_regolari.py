from Grafi import grafi
import numpy as np
import copy

def genera_matrici_spostamento(grafo:grafi.grafo):
    # La matrice di adiacenza va suddivisa in componenti unitarie.
    grado = int(grafo.ottieni_grado())
    numero_vertici = grafo.numero_vertici

    copia_matrice_adiacenza = copy.deepcopy(grafo.matrice_adiacenza)

    lista_matrici_spostamento = []
    for indice in range(grado):
        matrice_attuale = np.zeros((numero_vertici, numero_vertici))
        for vertice_provenienza in range(numero_vertici):
            vertice_destinazione = np.nonzero(copia_matrice_adiacenza[vertice_provenienza])
            vertice_destinazione_num = vertice_destinazione[0][0]
            del vertice_destinazione
            vertice_destinazione = vertice_destinazione_num
            matrice_attuale[vertice_provenienza][vertice_destinazione] = 1
            copia_matrice_adiacenza[vertice_provenienza][vertice_destinazione] = 0
        lista_matrici_spostamento.append(matrice_attuale)

    return lista_matrici_spostamento

def genera_matrice_coin(grafo: grafi.grafo):
    # Genero la matrice come FFT (analogo a Barr-Fleming-Kendon).
    dimensioni_matrice = int(grafo.ottieni_grado())
    mat = [[0 for j in range(dimensioni_matrice)] for k in range(dimensioni_matrice)]
    for j in range(len(mat)):
        mat[j][j] = 1
    coin = np.fft.fft(mat)
    # La matrice va opportunamente normalizzata.
    coin = coin / np.sqrt(dimensioni_matrice)
    return coin

def genera_proiettori_base_moneta(grafo: grafi.grafo):
    # Genero una lista di proiettori sugli stati di base della moneta.
    dimensioni_matrice = int(grafo.ottieni_grado())
    lista_proiettori = []
    for stato in range(dimensioni_matrice):
        proiettore_stato = np.zeros(dimensioni_matrice)
        proiettore_stato[stato] = 1
        lista_proiettori.append(np.outer(proiettore_stato, proiettore_stato))
    return lista_proiettori