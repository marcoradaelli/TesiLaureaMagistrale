import numpy as np

def rappresenta_risultati_tramite_array(risultati: dict, numero_punti, numero_run):
    array = np.zeros(numero_punti)

    for chiave in risultati.keys():
        array[chiave] = risultati[chiave]

    return array / numero_run