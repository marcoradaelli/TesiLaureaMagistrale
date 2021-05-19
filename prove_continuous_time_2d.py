from Grafi import grafi
from walks_core import qrw_continuous, crw_continuous
from walks_core import physics_utilities as ph
import numpy as np
from matplotlib import pyplot as plt
from strumenti_analisi import integratore_tempo as integ

numero_punti = 25

grafo = grafi.grafo_anello(numero_punti=numero_punti, disegna_grafo=False)

# Caso classico.
w = crw_continuous.walker(grafo_ospite=grafo,posizione_iniziale=1)
vett_entropie = []
vett_tempi = np.arange(0,30,0.1)
for t in vett_tempi:
    vett_entropie.append(ph.entropia_shannon(w.ottieni_distribuzione_probabilita_a_tempo(t)))
plt.plot(vett_tempi, vett_entropie)
plt.hlines(np.log2(numero_punti),xmin=min(vett_tempi),xmax=max(vett_tempi), colors="orange")
plt.xlabel("Time")
plt.ylabel("Shannon entropy")
plt.suptitle("Classical random walk on the ring")
plt.title("Number of points: " + str(numero_punti))
plt.show()

# Caso quantistico
w = qrw_continuous.walker(grafo_ospite=grafo, posizione_iniziale=1)
vett_entropie = []
for t in vett_tempi:
    vett_entropie.append(ph.entropia_shannon(w.ottieni_distribuzione_probabilita_a_tempo(t)))
plt.plot(vett_tempi, vett_entropie)
plt.hlines(np.log2(numero_punti),xmin=min(vett_tempi),xmax=max(vett_tempi), colors="orange")
plt.xlabel("Time")
plt.ylabel("Shannon entropy")
plt.suptitle("Quantum random walk on the ring")
plt.title("Number of points: " + str(numero_punti))
plt.show()

# Caso quantistico con time average.
vett_entropie = []
passo_integrazione = 0.01
for t in vett_tempi:
    distr_cesaro = integ.integra(w.ottieni_distribuzione_probabilita_a_tempo,0,30,passo_integrazione)
    vett_entropie.append(ph.entropia_shannon(distr_cesaro))
    print("Ok per tempo ", t)
plt.plot(vett_tempi,vett_entropie)
plt.hlines(np.log2(numero_punti),xmin=min(vett_tempi),xmax=max(vett_tempi), colors="orange")
plt.xlabel("Time")
plt.ylabel("Cesaro Shannon entropy")
plt.suptitle("Quantum random walk on the ring - Cesaro distribution")
plt.title("Number of points: " + str(numero_punti))
plt.show()
