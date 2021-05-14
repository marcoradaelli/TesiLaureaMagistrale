from walks_core import qrw_continuous as qrw
from Grafi import grafi
import matplotlib.pyplot as plt
import numpy as np
from walks_core import physics_utilities as ph
from strumenti_analisi import convoluzione as conv

numero_punti_anello = 25
numero_valori = 10000
posizione_iniziale = 10
tempo_prima_della_misura = 10

grafo = grafi.grafo_anello(numero_punti=numero_punti_anello, disegna_grafo=True)
w = qrw.walker(grafo_ospite=grafo, posizione_iniziale=posizione_iniziale)
ddp = w.ottieni_distribuzione_probabilita_a_tempo(tempo=tempo_prima_della_misura)
plt.plot(ddp)
plt.show()

vett_conv = []
for numero_conv in range(1,100):
    vett_conv.append(sum(conv.convoluzione_iterata(f=ddp, numero_volte=numero_conv)))

plt.plot(vett_conv)
plt.show()