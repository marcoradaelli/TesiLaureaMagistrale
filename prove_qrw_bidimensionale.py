from walks_core import qrw_2d, physics_utilities as phu
from matplotlib import pyplot as plt
import numpy as np

numero_punti = 25
numero_passi = 200

w = qrw_2d.walker(numero_punti_per_dimensione=numero_punti)

vett_entropia = []

for passo in range(numero_passi):
    w.passo()
    if passo % 10 == 0:
        ddp = w.ottieni_distribuzione_probabilita()
        plt.matshow(ddp)
        plt.suptitle("Probability distribution with Hadamard coin")
        plt.title("Number of steps: " + str(passo))
        plt.show()
        vett_entropia.append(phu.entropia_shannon(ddp))

ddp = w.ottieni_distribuzione_probabilita()

plt.matshow(ddp)
plt.suptitle("Probability distribution with Hadamard coin")
plt.title("Number of steps: " + str(numero_passi))
plt.show()

entropia_massima = np.log2(numero_punti*numero_punti)
plt.plot(entropia_massima * np.ones(len(vett_entropia)))
plt.plot(vett_entropia)
plt.suptitle("Entropy vs steps with Hadamard coin")
plt.title("Number of points per dimension: 25")
plt.xlabel("Steps")
plt.ylabel("Shannon entropy")
plt.show()