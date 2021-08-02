import discrete_continuous as dc
from walks_core import qrw_continuous, physics_utilities, qrw, anello
import numpy as np
from Grafi import grafi
from matplotlib import pyplot as plt

def taglia_ddp_in_base_a_devstd(ddp: list, dist: float) -> np.array:
    # La distanza va passata in unità di devstd.
    valore_medio = physics_utilities.media(ddp)
    devstd = physics_utilities.devstd(ddp)

    # Individuo gli estremi del taglio.
    estremo_sinistro = valore_medio - dist*devstd
    estremo_destro = valore_medio + dist*devstd

    # Valuto di non essere uscito dalla ddp.
    if estremo_sinistro < 0 or estremo_destro > len(ddp):
        raise Exception("Uscito dagli estremi della distribuzione,")

    # Procedo a copiare solo la parte di distribuzione all'interno del limite.
    nuova_ddp = np.zeros(len(ddp))
    for x in range(len(ddp)):
        if estremo_sinistro <= x <= estremo_destro:
            nuova_ddp[x] = ddp[x]

    # Rinormalizzo la distribuzione ottenuta.
    totale = np.sum(nuova_ddp)
    nuova_ddp = nuova_ddp/totale

    return nuova_ddp

# Definisco un grafo a linea.
numero_punti = 1000
grafo_linea = grafi.grafo_linea(numero_punti)

# Definisco il walker.
w = qrw_continuous.walker(grafo_ospite=grafo_linea,
                          posizione_iniziale=int(numero_punti/2),
                          tipo_evoluzione="laplaciano")

tempo = 220
ddp = w.ottieni_distribuzione_probabilita_a_tempo(tempo)
devstd = physics_utilities.devstd(ddp)
media = physics_utilities.media(ddp)
print("Deviazione standard: ", devstd)
rete_punti_taglio = np.arange(0.4,1.4,0.01)
vett_distanze = []
for punto_taglio in rete_punti_taglio:
    ddp_tagliata = taglia_ddp_in_base_a_devstd(ddp,punto_taglio)
    supporto_ddp_tagliata = physics_utilities.intervallo_supporto_distribuzione(ddp_tagliata)
    uniforme_su_tagliata = physics_utilities.distribuzione_uniforme_in_intervallo(len(ddp),supporto_ddp_tagliata)
    distanza_kolmogorov = physics_utilities.kolmogorov_distance(uniforme_su_tagliata,ddp_tagliata)
    print("Per ", punto_taglio, " deviazioni standard: Kolmogorov distance ", distanza_kolmogorov)
    vett_distanze.append(distanza_kolmogorov)

plt.plot(rete_punti_taglio, vett_distanze)
plt.suptitle("Kolmogorov distance from uniform distribution vs cut point")
plt.title("Total evolution time: " + str(tempo))
plt.xlabel("Cut point ($\sigma$ units)")
plt.ylabel("Kolmogorov distance from uniform")
plt.hlines(min(vett_distanze), xmin=0.4, xmax=1.4, colors="orange")
plt.show()

plt.plot(ddp)
plt.vlines([media - 0.5*devstd, media + 0.5*devstd], colors="yellow",ymin=0,ymax=0.01, label="0.5 $\sigma$")
plt.vlines([media - devstd, media + devstd], colors="orange",ymin=0,ymax=0.01, label="1 $\sigma$")
plt.vlines([media - 1.2*devstd, media + 1.2*devstd],ymin=0,ymax=0.01, colors="purple", label="1.2 $\sigma$")
plt.vlines([media - 1.4*devstd, media + 1.4*devstd],ymin=0,ymax=0.01, colors="red", label="1.4 $\sigma$")
plt.legend()
plt.title("Probability distribution after evolution time " + str(tempo))
plt.ylabel("Probability")
plt.xlabel("Position")
plt.show()

# Cerco di capire la posizione dei "corni" nel tempo.
rete_tempi = np.arange(1,220,5)
cutoff = 1.3 # In unità di sigma.
vett_posizione_corni = []
vett_devstd = []
vett_entro_cutoff = []

for tempo in rete_tempi:
    ddp_a_tempo = w.ottieni_distribuzione_probabilita_a_tempo(tempo)
    massimo = max(ddp_a_tempo)
    posizione_corni = np.where(ddp_a_tempo == massimo)[0][0]
    media = physics_utilities.media(ddp_a_tempo)
    # Attenzione all'instabilità numerica!
    posizione_corni = abs(posizione_corni - media)
    vett_posizione_corni.append(posizione_corni)
    devstd = physics_utilities.devstd(ddp_a_tempo)
    vett_devstd.append(devstd)
    minimo = int(media - cutoff * devstd)
    massimo = int(media + int(cutoff * devstd))
    vett_entro_cutoff.append(np.sum(ddp_a_tempo[minimo:massimo]))
    print("Tempo ", tempo, ":::: posizione corni ", posizione_corni)

plt.plot(rete_tempi, vett_posizione_corni, marker='+',linestyle='-')
plt.title("Distance of probability maxima from origin vs time")
plt.xlabel("Time")
plt.ylabel("Distance")
plt.show()

# Cerco di capire la relazione tra la distanza dei massimi dall'origine e la deviazione standard.
vett_rapporti = np.array(vett_posizione_corni) / np.array(vett_devstd)
plt.plot(rete_tempi, vett_rapporti, marker='+', linestyle='-')
plt.title("Distance of probability maxima from the origin in time-local $\sigma$ units")
plt.xlabel("Time")
plt.ylabel("Distance (time-local $\sigma$ units)")
plt.show()

# Cerco di capire quanta probabilità devo escludere fermandomi ad un cutoff.
plt.plot(rete_tempi, vett_entro_cutoff)
plt.title("Cumulative probability by " + str(cutoff) + " $\sigma$ from origin")
plt.xlabel("Time")
plt.ylabel("Cumulative probability")
plt.show()

