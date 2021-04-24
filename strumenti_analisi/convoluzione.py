import numpy as np

# Questa funzione esegue la convoluzione su Zp di una distribuzione di probabilità, secondo il formalismo
# di Sahlsten 2019.

def convoluzione_zp(f:np.array, g:np.array) -> np.array:
    p = len(f)
    if len(f) != len(g):
        raise Exception("Distribuzioni di diversa lunghezza!")

    risultato = np.zeros(p)
    for t in range(0,p):
        risultato[t] = 0
        for s in range(0,p):
            risultato[t] += f[(t-s) % p] * g[s]
    return risultato

def convoluzione_iterata(f:np.array, numero_volte) -> np.array:
    for i in range(0,numero_volte):
        f = convoluzione_zp(f, f)
    return f

def trasformata_fourier(f: np.array) -> np.array:
    p = len(f)
    risultato = np.zeros(p, dtype=complex)
    for k in range(0,p):
        risultato[k] = 0+0j
        for t in range(0,p):
            risultato[k] += f[t] * np.exp(-2*np.pi*1.j*k*t/p)
    return risultato

def diaconis_shashahani_bound(f: np.array, n: int) -> float:
    p = len(f)
    tdf = trasformata_fourier(f)
    somma = 0
    for i in range(1,p):
        somma += pow(abs(tdf[i]), 2 * n)
    risultato = 1/2 * np.sqrt(somma)
    return risultato