import numpy as np
from matplotlib import pyplot as plt
from walks_core import qrw_density_matrix as qrw, operatori_kraus as kr, anello, physics_utilities as phu

# Topologia del grafo ospite.
numero_step = 50
dimensioni_anello = numero_step * 2 + 2
a = anello.anello(dimensioni_anello)
moneta_iniziale = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)])

rete_parametri_depolarizzazione = np.arange(0, 1, 0.01)
vett_shannon = []

max_p = 0
max_shannon = 0

for parametro in rete_parametri_depolarizzazione:
    print("=== PARAMETRO DEP. ", parametro, " ===")
    k = kr.canale_depolarizzatore(parametro, dimensioni_anello)
    lista_kraus = k.lista_operatori_kraus()
    w = qrw.walker(anello_ospite=a,
                   posizione_iniziale=numero_step + 1,
                   moneta_iniziale=moneta_iniziale,
                   operatori_kraus=lista_kraus)
    for step in range(numero_step):
        w.passo()
        #print("Eseguito passo ", step)
    ddp, appo = w.ottieni_distribuzione_probabilita()
    shannon = phu.entropia_shannon(ddp)
    if max_shannon < shannon:
        max_shannon = shannon
        max_p = parametro

    vett_shannon.append(shannon)

plt.plot(rete_parametri_depolarizzazione, vett_shannon)
plt.xlabel("Depolarization parameter")
plt.ylabel("Shannon entropy")
plt.suptitle("Shannon entropy vs depolarization parameter after a fixed number of steps")
plt.title("Number of steps: " + str(numero_step))
plt.show()

# Adesso provo a vedere come si sposta il massimo al variare del numero dei passi.
rete_passi = range(10,100,5)
depo_step = 0.5
vett_massimi = []
for numero_step in rete_passi:
    print("====== PASSI: ", numero_step, " ======")
    dimensioni_anello = numero_step * 2 + 2
    a = anello.anello(dimensioni_anello)
    moneta_iniziale = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)])

    rete_parametri_depolarizzazione = np.arange(0, 1, depo_step)
    vett_shannon = []

    for parametro in rete_parametri_depolarizzazione:
        print("Parametro dep: ", parametro)
        k = kr.canale_depolarizzatore(parametro, dimensioni_anello)
        lista_kraus = k.lista_operatori_kraus()
        w = qrw.walker(anello_ospite=a,
                       posizione_iniziale=numero_step + 1,
                       moneta_iniziale=moneta_iniziale,
                       operatori_kraus=lista_kraus)
        for step in range(numero_step):
            w.passo()
            #print("Eseguito passo ", step)
        ddp, appo = w.ottieni_distribuzione_probabilita()
        shannon = phu.entropia_shannon(ddp)

        vett_shannon.append(shannon)

    # Trovo il valore di depolarizzazione corrispondente al massimo.
    depo_max = np.argmax(vett_shannon) * depo_step
    print("Best depo: ", depo_max)
    vett_massimi.append(depo_max)



plt.plot(rete_passi, vett_massimi, marker="+", markersize=15)
plt.xlabel("Number of steps")
plt.ylabel("Best depolarization parameter")
plt.title("Best depolarization parameters for different number of steps")
plt.show()
print(f"Max Shannon: {max_shannon}, corrispondente a {max_p}")