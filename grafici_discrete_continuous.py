from walks_core import qrw as discrete,anello,qrw_continuous as continuous, physics_utilities as phu
from Grafi import grafi
import numpy as np
from matplotlib import pyplot as plt

numero_punti = 50
numero_passi = int(numero_punti/2)-1
posizione_iniziale = numero_passi + 1
tempo_iniziale = 0
tempo_finale = 40
tempo_step = 0.002

# Preparo la ddp discreta.
a = anello.anello(numero_punti)
g = grafi.grafo_linea(numero_punti)
discr = discrete.walker(a,posizione_iniziale,np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)]))
for i in range(numero_passi):
    discr.passo()
ddp_1, appo = discr.ottieni_distribuzione_probabilita()
discr.passo()
ddp_2, appo = discr.ottieni_distribuzione_probabilita()
ddp_discr = (ddp_1 + ddp_2) * .5

# Considero il cammino continuo.
cont = continuous.walker(g,posizione_iniziale)
rete_tempi = np.arange(tempo_iniziale,tempo_finale,tempo_step)
vett_fidelity = []
vett_kolmogorov = []
for tempo in rete_tempi:
    ddp_cont = cont.ottieni_distribuzione_probabilita_a_tempo(tempo)
    fidelity = phu.fidelity(ddp_cont,ddp_discr)
    kolmogorov = phu.kolmogorov_distance(ddp_cont, ddp_discr)
    print("Calcolato a tempo ", tempo, "  fidelity: ", fidelity, "  Kolmogorov: ", kolmogorov)
    vett_fidelity.append(fidelity)
    vett_kolmogorov.append(kolmogorov)
plt.plot(rete_tempi,vett_kolmogorov)
plt.suptitle("Kolmogorov distance vs continuous time")
plt.title("Number of discrete steps: " + str(numero_passi))
plt.xlabel("Adimensionalized time")
plt.ylabel("Kolmogorov distance")
plt.show()
plt.plot(rete_tempi,vett_fidelity)
plt.suptitle("Fidelity vs continuous time")
plt.title("Number of discrete steps: " + str(numero_passi))
plt.xlabel("Adimensionalized time")
plt.ylabel("Fidelity")
plt.show()

# Individuo il punto di massimo.
tempo_max = rete_tempi[np.argmax(vett_fidelity)]
# Disegno le due distribuzioni a quel tempo.
ddp_cnt = cont.ottieni_distribuzione_probabilita_a_tempo(tempo_max)
plt.plot(ddp_discr, label="Discrete")
plt.plot(ddp_cnt, label="Continuous")
plt.suptitle("Comparison between continuous and discrete probability distributions")
plt.title("Number of discrete steps: " + str(numero_passi) + "; adimensional time: " + str(tempo_max))
plt.legend()
plt.show()
