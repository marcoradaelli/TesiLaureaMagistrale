import qiskit
from matplotlib import pyplot as plt
from qiskit.tools.visualization import circuit_drawer, plot_histogram

provider = qiskit.IBMQ.enable_account("03eedbfafec2373720d3bee8a9275be24584fade4706f6cc29e5df02d5dbe31563134f62198b4f087fea923f3c61d26de19c4ec0c199c2af14d5aaebbc25679d")
# backend = provider.backend.ibm_qasm
backend = qiskit.Aer.get_backend("aer_simulator")

# Preparo i registri.
A0 = qiskit.QuantumRegister(1,"qa0")
A1 = qiskit.QuantumRegister(1,"qa1")
A2 = qiskit.QuantumRegister(1,"qa2")
A3 = qiskit.QuantumRegister(1,"qa3")
C0 = qiskit.QuantumRegister(1,"qc0")
C1 = qiskit.QuantumRegister(1,"qc1")
C2 = qiskit.QuantumRegister(1,"qc2")
coin = qiskit.QuantumRegister(1,"coin")

classical = qiskit.ClassicalRegister(4,"class")

circ = qiskit.QuantumCircuit(A0,C0,A1,C1,A2,C2,A3,coin,classical)

# Condizionamento coin.
circ.cx(7,0)
circ.cx(7,2)
circ.cx(7,4)
circ.cx(7,6)

# Incrementer
circ.cx(0,1)
circ.ccx(1,2,3)
circ.ccx(3,4,5)
circ.cx(5,6)
circ.ccx(3,4,5)
# circ.ccx(1,2,3)
# circ.cx(0,1)
# circ.cx(0,1)
# circ.ccx(1,2,3)
circ.cx(3,4)
circ.ccx(1,2,3)
# circ.cx(0,1)
# circ.cx(0,1)
circ.cx(1,2)
circ.cx(0,1)
circ.x(0)

# # Decrementer
# circ.x(0)
# circ.x(2)
# circ.x(4)
# circ.cx(0,1)
# circ.ccx(1,2,3)
# circ.ccx(3,4,5)
# circ.cx(5,6)
# circ.ccx(3,4,5)
# #circ.ccx(1,2,3)
# #circ.cx(0,1)
# circ.x(4)
# #circ.cx(0,1)
# #circ.ccx(1,2,3)
# circ.cx(3,4)
# circ.ccx(1,2,3)
# #circ.cx(0,1)
# circ.x(2)
# #circ.cx(0,1)
# circ.cx(1,2)
# circ.cx(0,1)

circ.measure(0,0)
circ.measure(2,1)
circ.measure(4,2)
circ.measure(6,3)

numero_run = 1000
job = qiskit.execute(circ,backend,shots=numero_run)
result = job.result()
counts = result.get_counts()
plot_histogram(counts)
plt.show()

circ.draw(output="mpl")
plt.show()