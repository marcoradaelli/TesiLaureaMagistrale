from strumenti_analisi import data_loader
from matplotlib import pyplot as plt
import time

path = "../data/dipendenza_numero_misure.txt"
dati = data_loader.carica_file(path)

plt.errorbar(dati['numero punti anello'], dati['ave quantistico'], yerr=dati['devstd quantistico'], label="Quantum")
plt.errorbar(dati['numero punti anello'], dati['ave classico'], yerr=dati['devstd classico'], label="Classical")
plt.suptitle("Number of points in the cycle vs Shannon Entropy")
plt.title("Number of MonteCarlo steps: 100")
plt.xlabel("Number of points in the cycle")
plt.ylabel("Shannon entropy")
plt.legend()
plt.savefig('data/graphs/dipendenza_dimensioni_anello' + str(time.time()) + ".png")
# Disegno il grafico.
plt.show()


