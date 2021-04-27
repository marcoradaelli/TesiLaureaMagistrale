from walks_core import anello, crw_transition, qrw
import numpy as np
from matplotlib import pyplot as plt

m = 10
p = 25
init = 12
a = anello.anello(p)
moneta_iniziale = [0.7071, 0.7071]
q = qrw.walker(a,init,moneta_iniziale=moneta_iniziale)
c = crw_transition.walker(a,init)

for passo in range(0,m):
    q.passo()
    c.passo()

#plt.plot(q.ottieni_distribuzione_probabilita())
plt.plot(q.ottieni_distribuzione_probabilita()[0], label="Quantum")
plt.plot(c.ottieni_distribuzione_probabilita()[0], label="Classical")
plt.title("Transition distribution")
plt.xlabel("Position")
plt.ylabel("Probability")
plt.legend()
plt.show()