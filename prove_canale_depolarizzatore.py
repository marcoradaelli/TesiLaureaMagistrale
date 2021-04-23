from walks_core import anello as an
from walks_core import operatori_kraus as ch
from walks_core import qrw_density_matrix as qrw_dm
from walks_core import qrw
from walks_core import crw

import numpy as np
import matplotlib.pyplot as plt

numero_punti_anello = 25
posizione_iniziale = 5
numero_passi_prima_misura = 4

anello = an.anello(numero_punti=numero_punti_anello)
canale = ch.canale_depolarizzatore(parametro=0.1, dimensioni_anello=numero_punti_anello)
moneta_iniziale = np.array([np.cos(np.pi/4), np.sin(np.pi/4)])

walker_dm = qrw_dm.walker(anello, posizione_iniziale, moneta_iniziale, canale.lista_operatori_kraus())
walker_qrw = qrw.walker(anello,posizione_iniziale,moneta_iniziale)
walker_crw = crw.walker(anello, posizione_iniziale)

for i in range(0, numero_passi_prima_misura):
    walker_dm.passo()
    walker_qrw.passo()
    walker_crw.passo()

# Ricavo le distribuzioni di probabilità.
pd_dm, appo = walker_dm.ottieni_distribuzione_probabilita()
pd_qrw, appo = walker_qrw.ottieni_distribuzione_probabilita()

plt.title("Equivalence of formalisms")
plt.plot(pd_qrw, label="State vector")
plt.plot(pd_dm, label="Density matrix")
plt.xlabel("Position")
plt.ylabel("Probability")
plt.legend()
plt.show()
