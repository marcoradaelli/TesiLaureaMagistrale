import numpy as np
from matplotlib import pyplot as plt
from walks_core import qrw_2d, physics_utilities as phu

numero_punti_per_dimensione = 11
numero_passi = 200
lista_monete = ["hadamard","DFT","grover"]

lista_walker = []
lista_liste_shannon = []

for moneta in lista_monete:
    w = qrw_2d.walker(numero_punti_per_dimensione,moneta)
    lista_walker.append(w)
    lista_liste_shannon.append([])

for passo in range(numero_passi):
    print(f"Inizio passo {passo}")
    for w in range(len(lista_walker)):
        lista_walker[w].passo()
        ddp = lista_walker[w].ottieni_distribuzione_probabilita()
        entropia = phu.entropia_shannon(ddp)
        lista_liste_shannon[w].append(entropia)

for moneta in range(len(lista_liste_shannon)):
    plt.plot(lista_liste_shannon[moneta], label=lista_monete[moneta])
plt.legend()
max_entropia = 2*np.log2(numero_punti_per_dimensione)
plt.hlines(max_entropia,0,numero_passi)
plt.xlabel("Steps")
plt.ylabel("Shannon entropy")
plt.suptitle("Entropy vs steps with different coins")
plt.title(f"Number of points per dimension: {numero_punti_per_dimensione}")
plt.show()