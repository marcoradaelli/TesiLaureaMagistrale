import numpy as np
from matplotlib  import pyplot as plt
from walks_core import qrw, crw_transition as crw, anello, physics_utilities as phu

numero_passi = 5
a = anello.anello(numero_passi * 2 + 2)
moneta_iniziale = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)])
q = qrw.walker(a,posizione_iniziale=int(numero_passi + 1), moneta_iniziale=moneta_iniziale)
c = crw.walker(a,posizione_iniziale=int(numero_passi + 1))

vettore_q = []
vettore_c = []
vettore_teoria = []
for passo in range(numero_passi):
    p_q, appo = q.ottieni_distribuzione_probabilita()
    e_q = phu.entropia_shannon(p_q)
    vettore_q.append(e_q)
    p_c, appo = c.ottieni_distribuzione_probabilita()
    e_c = phu.entropia_shannon(p_c)
    vettore_c.append(e_c)
    vettore_teoria.append(phu.logC(passo/2.))
    print("Passo ", passo, "    eq: ", e_q, "    ec: ", e_c)
    print(p_c)
    print(p_q)
    q.passo()
    c.passo()

plt.plot(vettore_q, label="Quantum")
plt.plot(vettore_c, label="Classical")
#plt.plot(vettore_teoria, label="Asymptotic behaviour")
plt.legend()
plt.xlabel("Steps")
plt.ylabel("Shannon entropy")
plt.title("Shannon entropy vs steps")
plt.show()