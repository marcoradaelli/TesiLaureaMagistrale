import numpy as np
from matplotlib import pyplot as plt
from walks_core import qrw, crw_transition as crw, anello

a = anello.anello(numero_punti=1000)
delta_moneta=np.pi/4
eta_moneta = 0
q = qrw.walker(anello_ospite=a,posizione_iniziale=500,moneta_iniziale=np.array([np.cos(delta_moneta), np.sin(delta_moneta) * np.exp(1j * eta_moneta)]))
q_h = qrw.walker(anello_ospite=a,posizione_iniziale=500,moneta_iniziale=np.array([1,0]),tipo_moneta="hadamard")
c = crw.walker(anello_ospite=a,posizione_iniziale=500)

numero_passi = 500
for passo in range(numero_passi):
    q.passo()
    q_h.passo()
    c.passo()
    print("Fatto passo ", passo)

ddp_q, appo = q.ottieni_distribuzione_probabilita(verboso=True)
ddp_qh, appo = q_h.ottieni_distribuzione_probabilita(verboso=True)
ddp_c, appo = c.ottieni_distribuzione_probabilita()

# Seleziono solo i termini pari.
ddp_qh = ddp_qh[::2]
ddp_q = ddp_q[::2]
ddp_c = ddp_c[::2]

print("Avvio creazione grafici")
plt.plot(range(0,1000,2), ddp_q, label="Quantum")
plt.plot(range(0,1000,2), ddp_c, label="Classical")
plt.xlabel("Positions")
plt.ylabel("Probabilities")
plt.legend()
plt.suptitle("Classical vs Quantum discrete walks on the line")
plt.title("Number of steps: 500")
print("Chiedo disegno")
plt.show()

plt.plot(range(0,1000,2), ddp_qh, label="Hadamard")
plt.plot(range(0,1000,2), ddp_q, label="Unbiased")
plt.xlabel("Positions")
plt.ylabel("Probabilities")
plt.legend()
plt.suptitle("Hadamard vs unbiased discrete walks on the line")
plt.title("Number of steps: 500")
plt.plot()
plt.show()