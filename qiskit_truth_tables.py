import qiskit
from matplotlib import pyplot as plt
from qiskit.tools.visualization import circuit_drawer, plot_histogram
from walks_core import qrw, anello
from strumenti_analisi import utilita_qiskit as uq

provider = qiskit.IBMQ.enable_account("03eedbfafec2373720d3bee8a9275be24584fade4706f6cc29e5df02d5dbe31563134f62198b4f087fea923f3c61d26de19c4ec0c199c2af14d5aaebbc25679d")
# backend = provider.backend.ibm_qasm
backend = qiskit.Aer.get_backend("aer_simulator")

# Preparo i registri.
qr = qiskit.QuantumRegister(7,"q")
qr_all = qiskit.QuantumRegister(8,"qa")

classical = qiskit.ClassicalRegister(4,"class")

incrementer = qiskit.QuantumCircuit(qr,name="incr")

# === INCREMENTER ===
incrementer.cx(0, 1)
incrementer.ccx(1, 2, 3)
incrementer.ccx(3, 4, 5)
incrementer.cx(5, 6)
incrementer.ccx(3, 4, 5)
incrementer.cx(3, 4)
incrementer.ccx(1, 2, 3)
incrementer.cx(1, 2)
incrementer.cx(0, 1)
incrementer.x(0)

incrementer.draw(output="mpl")
plt.show()

# Trasformo l'incrementer in un gate.
gate_incrementer = incrementer.to_gate()
# Versione controlled.
ctrl_gate_incrementer = gate_incrementer.control(1)

# === DECREMENTER ===
decrementer = qiskit.QuantumCircuit(qr, name="decr")
decrementer.x(0)
decrementer.x(2)
decrementer.x(4)
decrementer.cx(0, 1)
decrementer.ccx(1, 2, 3)
decrementer.ccx(3, 4, 5)
decrementer.cx(5, 6)
decrementer.ccx(3, 4, 5)
decrementer.x(4)
decrementer.cx(3, 4)
decrementer.ccx(1, 2, 3)
decrementer.x(2)
decrementer.cx(1, 2)
decrementer.cx(0, 1)

decrementer.draw(output="mpl")
plt.show()

gate_decrementer = decrementer.to_gate()

# Versione controlled.
ctrl_gate_decrementer = gate_decrementer.control(1)

# Combino in un nuovo circuito.
circuit = qiskit.QuantumCircuit(qr_all)
# Coin-flip unitary.
circuit.h(0)

circuit.append(ctrl_gate_incrementer,qr_all)
# Uno dei due spostamenti deve essere legato ad un condizionamento negato!
circuit.x(0)
circuit.append(ctrl_gate_decrementer, qr_all)
circuit.x(0)

circuit.draw(output="mpl")
plt.show()

unitaria_passo = circuit.to_gate()

numero_passi = 15
qr_walk = qiskit.QuantumRegister(8)
cr_walk = qiskit.ClassicalRegister(4)
walk = qiskit.QuantumCircuit(qr_walk, cr_walk)

# Definizione dello stato iniziale.
coin_input = 0
posizione_input = "0000"
lista_input = list(posizione_input)
# Correggo per la convenzione di ordine.
lista_input.reverse()  # Attenzione: l'uso di reverse modifica la lista!
for i in range(len(posizione_input)):
    if int(lista_input[i]) == 1:
        walk.x(i * 2 + 1)
if coin_input == 1:
    walk.x(0)

for passo in range(numero_passi):
    walk.append(unitaria_passo, qr_walk)

# Fase di misura.
walk.measure(1,0)
walk.measure(3,1)
walk.measure(5,2)
walk.measure(7,3)
walk.draw(output="mpl")
plt.show()

# Esecuzione.
numero_run = 1000
job = qiskit.execute(walk,backend,shots=numero_run)
result = job.result()
outputprobabilities = result.get_counts()
plot_histogram(outputprobabilities)
plt.show()

# Eseguo anche un random walk simulato classicamente.
a = anello.anello(16)
w = qrw.walker(a,0,[1,0],"hadamard")
for passo in range(numero_passi):
    w.passo()
sim_ddp, appo = w.ottieni_distribuzione_probabilita()
exe_ddp = uq.rappresenta_risultati_tramite_array(outputprobabilities.int_outcomes(),16,numero_run)
plt.plot(sim_ddp, label="My simulation")
plt.plot(exe_ddp, label="ibm_qasm")
plt.legend()
plt.xlabel("Position")
plt.ylabel("Probability")
plt.suptitle("Realization of a DT-QRW with a circuit-like architecture")
plt.title("Number of steps: " + str(numero_passi) + "; Run on ibm_qasm: " + str(numero_run))
plt.show()