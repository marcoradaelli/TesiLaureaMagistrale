import numpy as np
from matplotlib import pyplot as plt
from Grafi import grafi, generatore_matrici_grafi_regolari as gmgr
from walks_core import qrw_grafo, physics_utilities

numero_punti = 5
# gc = grafi.grafo_completo(numero_punti)
ga = grafi.grafo_completo(numero_punti)
# wc = qrw_grafo.walker(grafo_ospite=gc,posizione_iniziale=1)
wa = qrw_grafo.walker(grafo_ospite=ga, posizione_iniziale=1)

# vettore_entropia_shannon_grafo_completo = []
vettore_entropia_shannon_anello = []

numero_passi = 100
for i in range(numero_passi):
    # ddp, appo = wc.ottieni_distribuzione_probabilita()
    # plt.plot(ddp, label="Passo " + str(i))
    ddp_anello, appo = wa.ottieni_distribuzione_probabilita()
    # Calcolo anche  l'entropia di Shannon al passo i.
    # vettore_entropia_shannon_grafo_completo.append(physics_utilities.entropia_shannon(ddp))
    vettore_entropia_shannon_anello.append(physics_utilities.entropia_shannon(ddp_anello))
    #wc.passo()
    wa.passo()
    # print("Eseguito passo ", i, " entropia completo: ", physics_utilities.entropia_shannon(ddp), " entropia anello: ", physics_utilities.entropia_shannon(ddp_anello))

plt.legend()
plt.show()

# plt.plot(vettore_entropia_shannon_grafo_completo)
plt.plot(vettore_entropia_shannon_anello)
plt.show()