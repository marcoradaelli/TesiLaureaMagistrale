from strumenti_analisi import data_loader
from matplotlib import pyplot as plt
import time

path = "/Users/marco.radaelli/OneDrive - studenti.unimi.it/Università/Tesi di Laurea Magistrale/Codice/data/dipendenza_punti_anello.txt"
dati = data_loader.carica_file(path)

plt.errorbar(dati['numero punti anello'], dati['ave quantistico'], yerr=dati['devstd quantistico'], label="Quantum")
plt.errorbar(dati['numero punti anello'], dati['ave classico'], yerr=dati['devstd classico'], label="Classical")
plt.suptitle("Number of steps before measurement vs Shannon Entropy")
plt.title("Number of MonteCarlo runs: 100")
plt.xlabel("Number of steps before measurement $m$")
plt.ylabel("Shannon entropy")
plt.legend()
plt.savefig('data/graphs/dipendenza_numero_misure' + str(time.time()) + ".png")
# Disegno il grafico.
plt.show()