import data_loader
import numpy as np
from matplotlib import pyplot as plt
import time

path = "data/dipendenza_numero_misure.txt"
dati = data_loader.carica_file(path)

plt.errorbar(dati['numero passi prima di misura'], dati['ave quantistico'], yerr=dati['devstd quantistico'], label="Quantum")
plt.errorbar(dati['numero passi prima di misura'], dati['ave classico'], yerr=dati['devstd classico'], label="Classical")
plt.suptitle("Number of steps before measurement vs Shannon Entropy")
plt.title("Number of MonteCarlo steps: 100")
plt.xlabel("Number of steps before measurement")
plt.ylabel("Shannon entropy")
plt.legend()
plt.savefig('data/graphs/dipendenza_numero_misure' + str(time.time()) + ".png")

plt.show()


