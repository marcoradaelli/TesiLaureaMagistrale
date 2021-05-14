from walks_core import qrw_continuous as qrw
from walks_core import crw_continuous as crw
from Grafi import grafi
import matplotlib.pyplot as plt
import numpy as np
from walks_core import physics_utilities as ph

numero_punti = 25
posizione_iniziale = int(numero_punti/2)
tempo_finale = 3

grafo = grafi.grafo_anello(numero_punti=numero_punti, disegna_grafo=False)
w1 = qrw.walker(grafo_ospite=grafo, posizione_iniziale=posizione_iniziale, tipo_evoluzione="laplaciano")
w2 = crw.walker(grafo_ospite=grafo, posizione_iniziale=posizione_iniziale)

ddp_quantistica = w1.ottieni_distribuzione_probabilita_a_tempo(tempo=tempo_finale)
ddp_classica = w2.ottieni_distribuzione_probabilita_a_tempo(tempo=tempo_finale)

print("Quantum", np.sum(ddp_quantistica))
print("Classical", np.sum(ddp_classica))

plt.plot(ddp_quantistica, label="Quantum")
plt.plot(ddp_classica, label="Classical")
plt.legend()
plt.show()