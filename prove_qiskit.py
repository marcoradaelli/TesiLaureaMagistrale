import numpy as np
import qiskit
from qiskit import Aer
from qiskit.tools.visualization import plot_histogram, plot_state_city
from matplotlib import pyplot as plt
from walks_core import qrw, anello

def rappresenta_risultati_tramite_array(risultati: dict, numero_punti, numero_run):
    array = np.zeros(numero_punti)

    for chiave in risultati.keys():
        array[chiave] = risultati[chiave]

    return array / numero_run

# Preparazione di Qiskit.
provider = qiskit.IBMQ.enable_account("03eedbfafec2373720d3bee8a9275be24584fade4706f6cc29e5df02d5dbe31563134f62198b4f087fea923f3c61d26de19c4ec0c199c2af14d5aaebbc25679d")
backend = provider.backend.ibmq_16_melbourne

circ = qiskit.QuantumCircuit(8,5)

numero_passi = 5

numero_run = 1000

# Inizializzazione dei qubit.
# Ricordo che all'inizio sono tutti in |0> per default di Qiskit.
circ.x(0)
circ.x(1)
circ.x(2)
circ.x(4)

for passo in range(numero_passi):
    # Coin shift: Hadamard sull'ultimo qubit di coin.
    circ.h(7)

    # Primo blocco
    circ.cx(7,0)
    circ.cx(7,1)
    circ.cx(7,2)
    circ.cx(7,4)
    circ.cx(7,6)

    # Secondo blocco
    circ.ccx(0,1,3)
    circ.ccx(2,3,5)
    circ.ccx(4,5,6)
    circ.ccx(2,3,5)
    circ.ccx(2,3,4)

    # Terzo blocco
    circ.ccx(0,1,3)
    circ.ccx(0,1,2)
    circ.cx(0,1)
    circ.x(0)
    circ.cx(7,0)
    circ.cx(7,1)
    circ.cx(7,2)
    circ.cx(7,4)
    circ.cx(7,6)

# Misuro alla fine dei passi.
circ.measure(0,0)
circ.measure(1,1)
circ.measure(2,2)
circ.measure(4,3)
circ.measure(6,4)

# backend = Aer.get_backend("aer_simulator")
# job = backend.run(circ,shots=numero_run,memory=False)
job = qiskit.execute(circ,backend,shots=numero_run)

result = job.result()

# outputstate = result.get_statevector(circ, decimals=3)
outputprobabilities = result.get_counts()
print(outputprobabilities)
plot_histogram(outputprobabilities)
plt.show()
arr_risultati = rappresenta_risultati_tramite_array(outputprobabilities.int_outcomes(),pow(2,5), numero_run)
plt.plot(arr_risultati, label="Qiskit")

print(outputprobabilities.int_outcomes())

a = anello.anello(numero_punti=pow(2,5))
q = qrw.walker(a,posizione_iniziale=16,moneta_iniziale=[1,0], tipo_moneta="hadamard")
for passo in range(numero_passi):
    q.passo()
ddp, appo = q.ottieni_distribuzione_probabilita()
plt.plot(np.flip(ddp), label="Theory")
plt.legend()
plt.show()

