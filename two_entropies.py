from walks_core import qrw_density_matrix as qrw, anello, operatori_kraus as kraus, physics_utilities as phu
import numpy as np
from matplotlib import pyplot as plt

numero_passi = 100
numero_punti = numero_passi * 2 + 2
parametro_depo = 0.3
lista_kraus = kraus.canale_depolarizzatore(parametro_depo,numero_punti).lista_operatori_kraus()
a = anello.anello(numero_punti)
moneta_iniziale = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)])
w = qrw.walker(a,numero_passi + 1, moneta_iniziale,lista_kraus)

vett_shannon = []
vett_vonneumann = []

for passo in range(numero_passi):
    matrice_densita = w.passo()
    ddp,appo = w.ottieni_distribuzione_probabilita_con_coin()
    shannon = phu.entropia_shannon(ddp)
    vonneumann = phu.entropia_von_neumann(matrice_densita)
    vett_shannon.append(shannon)
    vett_vonneumann.append(vonneumann)
    print(f"Ok passo {passo}, Shannon {shannon}, Von Neumann {vonneumann}")

vett_shannon = np.array(vett_shannon)
vett_vonneumann = np.array(vett_vonneumann)
plt.suptitle("Randomness of quantum origin vs steps")
plt.title(f"Depolarisation parameter: {parametro_depo}")
plt.xlabel("Steps")
plt.ylabel("Entropy")
plt.plot(vett_vonneumann,label="Von Neumann entropy")
plt.plot(vett_shannon, label="Shannon entropy")
plt.plot(vett_shannon - vett_vonneumann, label="Randomness of quantum origin")
plt.legend()
plt.show()