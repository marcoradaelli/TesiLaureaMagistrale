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