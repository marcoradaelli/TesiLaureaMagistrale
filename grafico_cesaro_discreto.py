import numpy as np
from matplotlib import pyplot as plt
from walks_core import qrw, anello, physics_utilities as phu

numero_punti_anello = 25
a = anello.anello(numero_punti_anello)
moneta_iniziale = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)])
w = qrw.walker(a,0,moneta_iniziale)

numero_passi = 200
vett_entropie_cesaro = []
vett_cumulativa_probabilita = np.zeros(numero_punti_anello)
vett_entropie_ordinarie = []

for passo in range(1,numero_passi):
    w.passo()
    ddp, appo = w.ottieni_distribuzione_probabilita()
    entropia = phu.entropia_shannon(ddp)
    vett_entropie_ordinarie.append(entropia)
    # Cumulo per calcolare la DDP alla Cesaro.
    for punto in range(numero_punti_anello):
        vett_cumulativa_probabilita[punto] += ddp[punto]
    ddp_cesaro = vett_cumulativa_probabilita/passo
    entropia_cesaro = phu.entropia_shannon(ddp_cesaro)
    vett_entropie_cesaro.append(entropia_cesaro)

max_entropia = np.log2(numero_punti_anello)
plt.plot(vett_entropie_ordinarie, label="Ordinary")
plt.plot(vett_entropie_cesaro, label="Cesaro")
plt.hlines(max_entropia,0,numero_passi, label="Maximal entropy", colors="red")
plt.legend()
plt.xlabel("Steps")
plt.ylabel("Probability")
plt.suptitle("Ordinary and Cesaro Shannon entropies vs steps")
plt.title("Number of points in the cycle: " + str(numero_punti_anello))
plt.show()