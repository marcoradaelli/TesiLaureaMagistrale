import numpy as np
from matplotlib import pyplot as plt
from walks_core import operatori_kraus as kr, qrw_density_matrix as qrw_misto, anello, physics_utilities as phu, qrw as qrw_puro

# Ciclo sui valori del parametro di depolarizzazione.
p_min = 0
p_max = 1.1
p_step = 0.2
numero_passi = 50
dimensioni_anello = numero_passi * 2 + 2
a = anello.anello(dimensioni_anello)
posizione_iniziale = numero_passi + 1
moneta_iniziale = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)])
vettore_superamenti = []
for p in np.arange(p_min,p_max,p_step):
    lista_kraus = kr.canale_depolarizzatore(parametro=p, dimensioni_anello=dimensioni_anello).lista_operatori_kraus()
    q = qrw_misto.walker(a, posizione_iniziale, moneta_iniziale, lista_kraus)
    q_puro = qrw_puro.walker(a, posizione_iniziale, moneta_iniziale)
    vettore_shannon = []
    vettore_von_neumann = []
    superamento_impostato = False
    for passo in range(numero_passi):
        q.passo()
        q_puro.passo()
        ddp, appo = q.ottieni_distribuzione_probabilita()
        ddp_puro, appo = q_puro.ottieni_distribuzione_probabilita()
        matrice_densita = q.matrice_densita
        vn = phu.entropia_von_neumann(matrice_densita)
        vettore_von_neumann.append(vn)
        s = phu.entropia_shannon(ddp)
        s_puro = phu.entropia_shannon(ddp_puro)
        if s_puro > s and not superamento_impostato:
            vettore_superamenti.append(passo)
            superamento_impostato = True
            print("IMPOSTATO SUPERAMENTO per p = ", p)
        print(f"[p = {p}] Calcolato passo ", passo, ";    entropia di Shannon: ", f"{s:.2f}","    entropia di Von Neumann", f"{vn:.2f}")
        vettore_shannon.append(s)
    #plt.plot(vettore_shannon, label="p=" + f"{p:.2f}")
    plt.plot(vettore_von_neumann, label="p=" + f"{p:.2f}")
    if not superamento_impostato:
        vettore_superamenti.append(numero_passi)
#plt.title("Shannon entropy vs steps with depolarization")
plt.title("Von Neumann entropy vs steps with depolarization")
plt.xlabel("Steps")
#plt.ylabel("Shannon entropy")
plt.ylabel("Von Neumann entropy")
plt.legend(title="Depolarization parameter")
plt.show()

plt.plot(np.arange(p_min, p_max, p_step),vettore_superamenti)
plt.show()
