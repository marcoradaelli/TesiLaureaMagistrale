from strumenti_analisi import data_loader
from matplotlib import pyplot as plt
import time

path = "../data/dipendenza_numero_misure_continuo.txt"
dati = data_loader.carica_file(path)

plt.errorbar(dati['tempo prima di misura'], dati['ave quantistico'], yerr=dati['devstd quantistico'], label="Quantum")
plt.errorbar(dati['tempo prima di misura'], dati['ave classico'], yerr=dati['devstd classico'], label="Classical")
plt.suptitle("Shannon entropy vs time before measurement")
plt.title("Number of MonteCarlo steps: 100")
plt.xlabel("Time before measurement")
plt.ylabel("Shannon entropy")
plt.legend()
plt.savefig('../data/graphs/dipendenza_dimensioni_anello_continuo_' + str(time.time()) + ".png")
# Disegno il grafico.
plt.show()
