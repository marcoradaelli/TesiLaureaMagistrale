import numpy as np
from matplotlib import pyplot as plt
from walks_core import qrw_continuous as qrw, crw_continuous as crw
from Grafi import grafi

grafo = grafi.grafo_linea(numero_punti=1000)
q = qrw.walker(grafo_ospite=grafo,posizione_iniziale=500,tipo_evoluzione="laplaciano")
c = crw.walker(grafo_ospite=grafo, posizione_iniziale=500)

tempo = 200

c_ddp = c.ottieni_distribuzione_probabilita_a_tempo(tempo)
q_ddp = q.ottieni_distribuzione_probabilita_a_tempo(tempo)

plt.plot(q_ddp, label="Quantum")
plt.plot(c_ddp, label="Classical")
plt.suptitle("Classical vs Quantum continuous random walks on the line")
plt.title("Time: " + str(tempo))
plt.legend()
plt.show()