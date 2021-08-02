import numpy as np
from matplotlib import pyplot as plt
from walks_core import qrw, crw_transition as crw, anello, physics_utilities as phu

numero_passi = 300
numero_punti = 25
moneta_iniziale = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)])
posizione_iniziale = 0

a = anello.anello(numero_punti)
q = qrw.walker(a,posizione_iniziale,moneta_iniziale)
c = crw.walker(a,posizione_iniziale)

vett_shannon_quantum = []
vett_shannon_classico = []
for passo in range(numero_passi):
    ddp_quantum, appo = q.ottieni_distribuzione_probabilita()
    ddp_classico, appo = c.ottieni_distribuzione_probabilita()
    e_quantum = phu.entropia_shannon(ddp_quantum)
    e_classico = phu.entropia_shannon(ddp_classico)
    vett_shannon_quantum.append(e_quantum)
    vett_shannon_classico.append(e_classico)
    print(f"Passo {passo} concluso")
    q.passo()
    c.passo()
plt.plot(vett_shannon_quantum, label="Quantum")
plt.plot(vett_shannon_classico, label="Classical")
plt.xlabel("Steps")
plt.ylabel("Shannon entropy")
plt.suptitle("Shannon entropy vs steps on a cycle")
plt.title(f"Number of points in the cycle: {numero_punti}")
plt.hlines(np.log2(numero_punti),0,numero_passi,color="green", label="Maximum value")
plt.legend()
plt.show()

ddp_quantum, appo = q.ottieni_distribuzione_probabilita()
ddp_classico, appo = c.ottieni_distribuzione_probabilita()
plt.plot(ddp_quantum, label="Quantum")
plt.plot(ddp_classico, label="Classical")
plt.title(f"Spatial distribution after {numero_passi} steps")
plt.xlabel("Position")
plt.ylabel("Probability")
plt.legend()
plt.show()