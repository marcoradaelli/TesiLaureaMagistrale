from walks_core import qrw_continuous as qrw
from Grafi import grafi
import matplotlib.pyplot as plt
import numpy as np
from walks_core import physics_utilities as ph

grafo_ospite = grafi.grafo_anello(numero_punti=11, disegna_grafo=True)
w = qrw.walker(grafo_ospite=grafo_ospite,posizione_iniziale=5)

vett_entropie_shannon = []
vett_prob_totali = []

for tempo in range(0,1000,10):
    ddp = w.ottieni_distribuzione_probabilita_a_tempo(tempo)
    vett_entropie_shannon.append(ph.entropia_shannon(ddp))
    vett_prob_totali.append(np.sum(ddp))
plt.plot(vett_entropie_shannon)
vett_entropia_massima = np.log2(grafo_ospite.numero_vertici) * np.ones(100)
plt.plot(vett_entropia_massima)
plt.show()
plt.plot(vett_prob_totali)
plt.show()