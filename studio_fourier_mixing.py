import numpy as np
import matplotlib.pyplot as plt
from walks_core import qrw,crw_transition as crw,anello
from strumenti_analisi import convoluzione as conv
from strumenti_analisi import data_loader as loader

a = anello.anello(25)
q_walk = qrw.walker(anello_ospite=a,
                    posizione_iniziale=1,
                    moneta_iniziale=np.array([np.cos(np.pi/4), np.sin(np.pi/4)]))
c_walk = crw.walker(anello_ospite=a,
                    posizione_iniziale=1)

# Fisso la distribuzione da convolvere.
numero_passi_singolo = 10
for i in range(0,numero_passi_singolo):
    q_walk.passo()
    c_walk.passo()

distribuzione_quantistica, appo= q_walk.ottieni_distribuzione_probabilita()
distribuzione_classica, appo = c_walk.ottieni_distribuzione_probabilita()

massimo_convoluzioni = 100
vettore_diaconis_shashahani_classico = []
vettore_bound_entropia_classico = []
vettore_diaconis_shashahani_quantistico = []
vettore_bound_entropia_quantistico = []

for numero_convoluzioni in range(1,massimo_convoluzioni):
    vettore_diaconis_shashahani_classico.append(conv.diaconis_shashahani_bound(distribuzione_classica,numero_convoluzioni))
    vettore_bound_entropia_classico.append(conv.entropy_convolution_bound(distribuzione_classica,numero_convoluzioni))
    vettore_diaconis_shashahani_quantistico.append(conv.diaconis_shashahani_bound(distribuzione_quantistica, numero_convoluzioni))
    vettore_bound_entropia_quantistico.append(conv.entropy_convolution_bound(distribuzione_quantistica,numero_convoluzioni))
    print("Calcolato per ", numero_convoluzioni, " convoluzioni")

plt.plot(vettore_bound_entropia_quantistico, label="Quantum")
plt.plot(vettore_bound_entropia_classico, label="Classical")
plt.suptitle("Diaconis-Shashahani bound for entropy")
plt.title("Number of steps of the single probability distribution: " + str(numero_passi_singolo))
plt.xlabel("Number of convolutions")
plt.ylabel("Diaconis-Shashahani bound")
plt.legend()
plt.show()

# Pulisco i random walk per partire con la nuova simulazione.
del c_walk
del q_walk

# Riavvio i random walk dalla posizione iniziale.
q_walk = qrw.walker(anello_ospite=a,
                    posizione_iniziale=1,
                    moneta_iniziale=np.array([np.cos(np.pi/4), np.sin(np.pi/4)]))
c_walk = crw.walker(anello_ospite=a,
                    posizione_iniziale=1)

# Fisso il numero di convoluzioni da eseguire.
numero_convoluzioni = 100
minimo_passi = 2
massimo_passi = 50

vettore_bound_entropia_classico = []
vettore_bound_entropia_quantistico = []
for passo in range(minimo_passi, massimo_passi):
    c_walk.passo()
    q_walk.passo()

    c_distr,appo = c_walk.ottieni_distribuzione_probabilita()
    q_distr,appo = q_walk.ottieni_distribuzione_probabilita()
    vettore_bound_entropia_classico.append(conv.entropy_convolution_bound(c_distr,numero_convoluzioni))
    vettore_bound_entropia_quantistico.append(conv.entropy_convolution_bound(q_distr,numero_convoluzioni))

plt.plot(vettore_bound_entropia_quantistico, label="Quantum")
plt.plot(vettore_bound_entropia_classico, label="Classical")
plt.suptitle("Diaconis-Shashahani bound for entropy")
plt.title("Number of convolutions: " + str(numero_convoluzioni))
plt.xlabel("Number of single steps")
plt.ylabel("Diaconis-Shashahani bound")
plt.legend()
plt.show()