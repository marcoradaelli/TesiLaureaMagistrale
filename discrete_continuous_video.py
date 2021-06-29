from walks_core import qrw as qrw_discrete, qrw_continuous, physics_utilities as ph, anello as an
from Grafi import grafi
import numpy as np
from matplotlib import pyplot as plt
from strumenti_analisi import generatore_video

# E un tempo minimo e massimo e step per il continuo.
tempo_minimo = 9
tempo_massimo = 12
tempo_step = 0.01
numero_passi_discreto = 30

dimensione_spazio = max([numero_passi_discreto * 10,30])
posizione_iniziale = int(dimensione_spazio / 2)
moneta_iniziale = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)])

anello = an.anello(dimensione_spazio)
grafo = grafi.grafo_linea(dimensione_spazio)

dt_qrw = qrw_discrete.walker(anello, posizione_iniziale=posizione_iniziale, moneta_iniziale=moneta_iniziale)

# Calcolo la distribuzione del rw discreto di riferimento.
for passo in range(numero_passi_discreto):
    dt_qrw.passo()
print("Finita evoluzione discreta.")
# Medio tra due distribuzioni di probabilità successive in modo da evitare il problema della parità.
ddp_dt_passo_1, appo = dt_qrw.ottieni_distribuzione_probabilita()
dt_qrw.passo()
ddp_dt_passo_2, appo = dt_qrw.ottieni_distribuzione_probabilita()
ddp_dt = 1/2 * (ddp_dt_passo_1 + ddp_dt_passo_2)

shannon_discreto = ph.entropia_shannon(ddp_dt)

ct_qrw = qrw_continuous.walker(grafo, posizione_iniziale=posizione_iniziale)

rete_tempi = np.arange(tempo_minimo, tempo_massimo, tempo_step)
vett_fidelity = []
vett_shannon = []
vett_kolmogorov = []
for indice_tempo, tempo in enumerate(rete_tempi):
    ddp_ct = ct_qrw.ottieni_distribuzione_probabilita_a_tempo(tempo)
    fidelity = ph.fidelity(ddp_ct, ddp_dt)
    kolmogorov = ph.kolmogorov_distance(ddp_ct, ddp_dt)
    shannon_continuo = ph.entropia_shannon(ddp_ct)
    vett_shannon_discreto = np.ones(len(vett_shannon)) * shannon_discreto
    print("Tempo ", tempo, ":::: fidelity = ", fidelity)

    # Disegno grafico.
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
    fig.suptitle('Continuous vs discrete with ' + str(numero_passi_discreto) + " discrete steps")
    ax1.set_title("Time: " + str(round(tempo,2)) + " ; fidelity: " + str(round(fidelity,2)))
    ax1.plot(ddp_dt)
    ax1.plot(ddp_ct)
    # ax1.set_ylim((0,0.25))
    ax1.set_xlabel("Position")
    ax1.set_ylabel("Probability")
    ax2.plot(rete_tempi[:len(vett_fidelity)],vett_fidelity)
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Fidelity")
    ax3.plot(rete_tempi[:len(vett_kolmogorov)], vett_kolmogorov)
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Kolmogorov")
    ax4.plot(rete_tempi[:len(vett_fidelity)], vett_shannon_discreto)
    ax4.plot(rete_tempi[:len(vett_fidelity)], vett_shannon)
    ax4.set_xlabel("Time")
    ax4.set_ylabel("Shannon")
    plt.savefig("data/graphs/grafici_continuous_discrete/pro_video/" + str(indice_tempo) + ".png")
    plt.show()
    vett_fidelity.append(fidelity)
    vett_shannon.append(shannon_continuo)
    vett_kolmogorov.append(kolmogorov)

cartella_immagini = '/Users/marco.radaelli/OneDrive - studenti.unimi.it/Università/Tesi di Laurea Magistrale/Codice/data/graphs/grafici_continuous_discrete/pro_video'
generatore_video.genera_video(cartella_immagini,fps=4)