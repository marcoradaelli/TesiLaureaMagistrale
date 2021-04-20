import numpy as np

def carica_file(percorso):
    # Nomi delle colonne in riga con segno $.
    # Separatore ///
    # Ignoro righe con segno #.

    file = open(percorso)
    righe = file.readlines()

    intestazioni = None
    dict_dati = {}

    for riga in righe:
        if riga[0] == "$":
            # Riga di intestazioni.
            intestazioni = riga.split("///")
            for intestazione in intestazioni:
                dict_dati[intestazione.replace("$","").replace("\n","").strip()] = []

        elif riga[0] == "#":
            # Riga di commento.
            continue
        else:
            dati_riga = riga.split("///")
            for n,colonna in enumerate(dict_dati.keys()):
                dict_dati[colonna].append(float(dati_riga[n]))

    # Trasformo in array di numpy per futura comodità.
    for key in dict_dati.keys():
        dict_dati[key] = np.array(dict_dati[key])

    return dict_dati