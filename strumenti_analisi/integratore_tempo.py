import numpy as np
from typing import Callable

def integra(funzione:Callable, tempo_iniziale:float, tempo_finale:float, passo_integrazione:float):
    intervallo_tempo = tempo_finale - tempo_iniziale
    accu = 0
    for t in np.arange(tempo_iniziale, tempo_finale, passo_integrazione):
        val = funzione(t)
        accu += val * passo_integrazione
    return 1./intervallo_tempo * accu