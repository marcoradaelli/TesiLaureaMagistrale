import numpy as np
from matplotlib import pyplot as plt
from walks_core import qrw_density_matrix as qrw, operatori_kraus as kr, anello, physics_utilities as phu

step_par_depo = 0.01

rete_parametri_depo = np.arange(0,1,step_par_depo)
vettore_walker = []
max_step = 70
dimensione_anello = max_step * 2 + 2
a = anello.anello(dimensione_anello)
moneta_iniziale = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)])
vett_massimi = []

# Creo i walker.
for par_depo in rete_parametri_depo:
    kraus = kr.canale_depolarizzatore(par_depo,dimensione_anello)
    lista_kraus = kraus.lista_operatori_kraus()
    w = qrw.walker(a,max_step+1,moneta_iniziale,lista_kraus)
    vettore_walker.append(w)

print("Walker creati con successo.")

rete_passi = range(1,max_step,2)

for passo in range(max_step):
    vett_entropie_passo_fissato = []
    for walker in vettore_walker:
        walker.passo()
        if passo in rete_passi:
            ddp, appo = walker.ottieni_distribuzione_probabilita()
            entropia = phu.entropia_shannon(ddp)
            vett_entropie_passo_fissato.append(entropia)
        print("Eseguito passo ", passo, " per il walker ", vettore_walker.index(walker))
    # Trovo il valore di p a cui corrisponde il massimo.
    if passo in rete_passi:
        depo_parametro_max = rete_parametri_depo[np.argmax(vett_entropie_passo_fissato)]
        vett_massimi.append(depo_parametro_max)
        print("== Finito passo ", passo, "; depo migliore: ", depo_parametro_max)

plt.plot(rete_passi, vett_massimi)
plt.xlabel("Steps")
plt.ylabel("Best $p$ parameter")
plt.title("Best depolarization $p$ parameter vs steps")
plt.show()