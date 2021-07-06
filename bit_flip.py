import numpy as np
from matplotlib import pyplot as plt
from walks_core import qrw_density_matrix as qrw, operatori_kraus as kr, anello, physics_utilities as phu

numero_step = 100
dimensione_anello = numero_step * 2 + 2
a = anello.anello(dimensione_anello)

moneta_iniziale = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)])

lista_parametri = np.arange(0,.5,.1)
for parametro in lista_parametri:
    kraus = kr.phase_flip(parametro,dimensione_anello)
    lista_kraus = kraus.lista_operatori_kraus()
    w = qrw.walker(a,numero_step + 1,moneta_iniziale,lista_kraus)
    vett_shannon = []
    for passo in range(numero_step):
        w.passo()
        ddp, appo = w.ottieni_distribuzione_probabilita()
        entropia = phu.entropia_shannon(ddp)
        vett_shannon.append(entropia)
        print("Fatto passo ", passo, " per parametro ", parametro)
    plt.plot(vett_shannon, label="$p$ = " + str(parametro))
plt.xlabel("Steps")
plt.ylabel("Shannon entropy")
plt.title("Shannon entropy vs steps with phase-flip")
plt.legend(title="Phase-flip probability")
plt.show()