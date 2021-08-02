from walks_core import anello, qrw as discreto, qrw_continuous as continuo, physics_utilities as phu
from Grafi import grafi
import discrete_continuous as dcc
import numpy as np
from matplotlib import pyplot as plt

tempo_evoluzione = 100
# Stimo il coefficiente di conversione
print("=== STIMO COEFFICIENTE DI CONVERSIONE ===")
coefficiente_conversione = dcc.ottieni_fattore_conversione(tempo_minimo=0.1,tempo_massimo=10,tempo_step=0.1,numero_passi_massimo=30 ,disegna_grafici=False)
print(coefficiente_conversione)
passi_evoluzione = int(tempo_evoluzione / coefficiente_conversione)

# Creo l'anello.
a = anello.anello(numero_punti=passi_evoluzione * 2 + 1)
g = grafi.grafo_linea(numero_punti=passi_evoluzione * 2 + 1)

# Creo i walker.
cont_walker = continuo.walker(g,passi_evoluzione + 1, "laplaciano")
moneta_iniziale = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)])
discr_walker = discreto.walker(a,passi_evoluzione + 1, moneta_iniziale)

# Eseguo l'evoluzione.
cont_ddp = cont_walker.ottieni_distribuzione_probabilita_a_tempo(tempo_evoluzione)
print("=== EVOLUZIONE DISCRETA ===")
for passo in range(passi_evoluzione):
    discr_walker.passo()
    print("Eseguito passo ", passo)
# Per il walker discreto medio (come di consueto) su due passi successivi.
discr_ddp,appo = discr_walker.ottieni_distribuzione_probabilita(verboso=True)
discr_walker.passo()
discr_ddp_2, appo = discr_walker.ottieni_distribuzione_probabilita(verboso=True)
discr_ddp = 0.5*(discr_ddp + discr_ddp_2)

# Disegno le due distribuzioni di probabilità.
plt.plot(cont_ddp, label="Continuous walk")
plt.plot(discr_ddp, label="Discrete walk")
plt.xlabel("Position")
plt.ylabel("Probability")
plt.title("Probability distributions in continuous- and discrete-time QRW")
plt.legend()
plt.show()

# Calcolo le due deviazioni standard.
discr_devstd = phu.devstd(discr_ddp)
cont_devstd = phu.devstd(cont_ddp)
print("Deviazione standard discreto: ", discr_devstd)
print("Deviazione standard continuo: ", cont_devstd)

# Taglio le distribuzioni a fissata devstd (e le rinormalizzo).
rete_punti_taglio = np.arange(0.4,1.4,0.01)
cont_vett_distanze = []
discr_vett_distanze = []
cont_vett_shannon = []
discr_vett_shannon = []
cont_vett_fidelity = []
discr_vett_fidelity = []
vett_entropia_massima = []
for punto_taglio in rete_punti_taglio:
    cont_ddp_tagliata = phu.taglia_ddp_in_base_a_devstd(cont_ddp,punto_taglio)
    discr_ddp_tagliata = phu.taglia_ddp_in_base_a_devstd(discr_ddp, punto_taglio)
    cont_supporto_tagliata = phu.intervallo_supporto_distribuzione(cont_ddp_tagliata)
    discr_supporto_tagliata = phu.intervallo_supporto_distribuzione(discr_ddp_tagliata)
    cont_uniforme_su_tagliata = phu.distribuzione_uniforme_in_intervallo(len(cont_ddp),cont_supporto_tagliata)
    discr_uniforme_su_tagliata = phu.distribuzione_uniforme_in_intervallo(len(discr_ddp),discr_supporto_tagliata)
    vett_entropia_massima.append(np.log2(discr_supporto_tagliata[1]-discr_supporto_tagliata[0]))
    cont_kolmogorov = phu.kolmogorov_distance(cont_uniforme_su_tagliata,cont_ddp_tagliata)
    discr_kolmogorov = phu.kolmogorov_distance(discr_uniforme_su_tagliata,discr_ddp_tagliata)
    cont_shannon = phu.entropia_shannon(cont_ddp_tagliata)
    discr_shannon = phu.entropia_shannon(discr_ddp_tagliata)
    cont_fidelity = phu.fidelity(cont_uniforme_su_tagliata, cont_ddp_tagliata)
    discr_fidelity = phu.fidelity(discr_uniforme_su_tagliata, discr_ddp_tagliata)
    print("Per ", punto_taglio, " deviazioni standard: Kolmogorov distance continuo ", cont_kolmogorov, "   discreto: ", discr_kolmogorov)
    cont_vett_distanze.append(cont_kolmogorov)
    discr_vett_distanze.append(discr_kolmogorov)
    cont_vett_shannon.append(cont_shannon)
    discr_vett_shannon.append(discr_shannon)
    cont_vett_fidelity.append(cont_fidelity)
    discr_vett_fidelity.append(discr_fidelity)

plt.plot(rete_punti_taglio, discr_vett_distanze, label="Discrete")
plt.plot(rete_punti_taglio, cont_vett_distanze, label="Continuous")
plt.xlabel("Cut point ($\sigma$ units)")
plt.ylabel("Kolmogorov distance")
plt.legend()
plt.suptitle("Kolmogorov distance from uniform distribution vs cut point")
plt.title("Number of discrete steps: " +  str(passi_evoluzione) + "; adimensional time: " + str(tempo_evoluzione))
plt.show()

plt.plot(rete_punti_taglio, discr_vett_shannon, label="Discrete")
plt.plot(rete_punti_taglio, cont_vett_shannon, label="Continuous")
plt.xlabel("Cut point ($\sigma$ units)")
plt.ylabel("Shannon entropy")
plt.legend()
plt.suptitle("Shannon entropy vs cut point")
plt.title("Number of discrete steps: " +  str(passi_evoluzione) + "; adimensional time: " + str(tempo_evoluzione))
plt.show()

plt.plot(rete_punti_taglio, discr_vett_fidelity, label="Discrete")
plt.plot(rete_punti_taglio, cont_vett_fidelity, label="Continuous")
plt.xlabel("Cut point ($\sigma$ units)")
plt.ylabel("Fidelity")
plt.legend()
plt.suptitle("Fidelity with the uniform vs cut point")
plt.title("Number of discrete steps: " +  str(passi_evoluzione) + "; adimensional time: " + str(tempo_evoluzione))
plt.show()

print("Calcolo entropia massima")

discr_vett_shannon = np.array(discr_vett_shannon)
cont_vett_shannon = np.array(cont_vett_shannon)
vett_entropia_massima = np.array(vett_entropia_massima)

plt.plot(rete_punti_taglio, discr_vett_shannon/vett_entropia_massima, label="Discrete")
plt.plot(rete_punti_taglio, cont_vett_shannon/vett_entropia_massima, label="Continuous")
plt.xlabel("Cut point ($\sigma$ units)")
plt.ylabel("Randomness generation efficiency")
plt.legend()
plt.suptitle("Randomness generation efficiency vs cut point")
plt.title("Number of discrete steps: " +  str(passi_evoluzione) + "; adimensional time: " + str(tempo_evoluzione))

# Sottografico entropia
plt.axes([.23,.4,.3,.3])
plt.plot(rete_punti_taglio, discr_vett_shannon, label="Discrete")
plt.plot(rete_punti_taglio, cont_vett_shannon, label="Continuous")
plt.title("Shannon entropy vs cut point")
plt.xlabel("Cut point")
plt.ylabel("Shannon entropy")
plt.show()

