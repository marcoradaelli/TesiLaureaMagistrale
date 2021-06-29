import numpy as np

def is_np_array(a):
    return type(a) is np.ndarray

def logC(x):
    # Ritorna il logaritmo in base 2 oppure 0 se l'input è nullo.
    if x == 0:
        return 0
    else:
        return np.log2(x)

def entropia_shannon(v):
    v = np.ndarray.flatten(v)
    accu_entropia = 0
    for punto in v:
        accu_entropia += - punto * logC(punto)
    return accu_entropia


def calcola_distribuzione_da_risultati(vett_risultati):
    # Cerca il massimo dei risultati, che darà l'estremo della distribuzione.
    estremo_distribuzione = int(max(vett_risultati))
    distribuzione = np.zeros(estremo_distribuzione + 1)
    # Cicla su tutti i risultati, eseguendo il binnaggio.
    for risultato in vett_risultati:
        distribuzione[int(risultato)] += 1 / len(vett_risultati)

    return distribuzione


def converti_in_stringa_binaria(vett_risultati):
    stringa_binaria = ""
    # Trova il numero massimo nella stringa.
    valore_massimo = max(vett_risultati)
    # Determina in quanti bit deve essere rappresentato ogni numero.
    quanti_bit = int(np.log2(valore_massimo))
    massimo_accettabile = pow(2,int(np.log2(valore_massimo)))
    for numero in vett_risultati:
        if numero > massimo_accettabile:
            # Trascura i numeri troppo grandi.
            continue
        # Per funzionamento interno di bin, serve tagliare i primi due caratteri della stringa ritornata,
        stringa_binaria = stringa_binaria + bin(numero)[2:].zfill(quanti_bit)
    return stringa_binaria

def verifica_matrice_unitaria(matrice):
    return np.allclose(np.eye(len(matrice)), matrice.dot(matrice.T.conj()))

def fidelity(d1: list, d2: list) -> float:
    accu = 0

    if not len(d1) == len(d2):
        raise Exception("Distribuzioni di diverse dimensioni!")

    for i in range(len(d1)):
        accu += np.sqrt(d1[i] * d2[i])

    return accu

def kolmogorov_distance(d1:list, d2:list) -> float:
    accu = 0

    if not len(d1) == len(d2):
        raise Exception("Distribuzioni di diverse dimensioni!")

    for i in range(len(d1)):
        accu += np.abs(d1[i] - d2[i])

    return accu

def media(ddp: list) -> float:
    accu = 0
    for pos,el in enumerate(ddp):
        accu += pos*el
    return accu

def varianza(ddp: list) -> float:
    accu = 0
    valore_medio = media(ddp)
    for pos,el in enumerate(ddp):
        accu += pow((pos-valore_medio),2)*el
    return accu

def devstd(ddp:list) -> float:
    return np.sqrt(varianza(ddp))

def intervallo_supporto_distribuzione(ddp:list) -> tuple:
    # Ciclo finché non trovo un valore != 0.
    counter_min = 0
    for item in ddp:
        if item == 0:
            counter_min += 1
        else:
            break
    counter_max = len(ddp)
    for item in reversed(ddp):
        if item == 0:
            counter_max -= 1
        else:
            break
    return counter_min, counter_max

def distribuzione_uniforme_in_intervallo(dim:int, intervallo:tuple) -> np.array:
    # Restituisco una distribuzione uniforme su un intervallo ristretto.
    ddp = np.zeros(dim)
    min,max = intervallo
    lunghezza_intervallo = max - min
    for i in range(min, max):
        ddp[i] = 1/lunghezza_intervallo
    return ddp

def entropia_von_neumann(matrice:np.array):
    # Diagonalizza la matrice.
    list_autovalori = np.linalg.eigvals(matrice)
    accu = 0
    for av in list_autovalori:
        accu += - av * logC(av)
    return np.real(accu)