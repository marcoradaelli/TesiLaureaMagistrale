from Grafi import grafi
from walks_core import qrw as discr, qrw_continuous as cont, anello, physics_utilities as phu
import numpy as np
from matplotlib import pyplot as plt
import discrete_continuous as fact_conv

fattore_conversione = fact_conv.ottieni_fattore_conversione(disegna_grafici=False)
print("FATTORE DI CONVERSIONE: ", fattore_conversione)
tempo_continuo_massimo = 15
numero_passi_massimo = int(tempo_continuo_massimo /fattore_conversione)
numero_punti = numero_passi_massimo * 2 + 2
posizione_iniziale = numero_passi_massimo + 1
moneta_iniziale = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)])

a = anello.anello(numero_punti)
g = grafi.grafo_linea(numero_punti)
c = cont.walker(g,posizione_iniziale)
d = discr.walker(a,posizione_iniziale,moneta_iniziale)

vett_massimi_cont = []
vett_massimi_discr = []
vett_tempi_equiv = []

for passo in range(numero_passi_massimo):
    tempo_equivalente = passo * fattore_conversione
    ddp_c = c.ottieni_distribuzione_probabilita_a_tempo(tempo_equivalente)
    ddp_d,appo = d.ottieni_distribuzione_probabilita()

    d.passo()
    # Trovo i massimi.
    max_c = np.argmax(ddp_c)
    dist_max_c = abs(posizione_iniziale - max_c)
    vett_massimi_cont.append(dist_max_c)
    max_d = np.argmax(ddp_d)
    dist_max_d = abs(posizione_iniziale - max_d)
    vett_massimi_discr.append(dist_max_d)
    vett_tempi_equiv.append(tempo_equivalente)
    fidelity = phu.fidelity(ddp_d,ddp_c)
    print(f"Ok passo {passo}, continuo {dist_max_c}, discreto {dist_max_d}, fidelity {fidelity}")

plt.clf()
plt.plot(vett_tempi_equiv,vett_massimi_discr, label="Discrete")
plt.plot(vett_tempi_equiv,vett_massimi_cont, label="Continuous")
plt.title("Distance of lateral peaks from origin vs time")
plt.legend()
plt.xlabel("Time")
plt.ylabel("Distance from origin")
plt.show()