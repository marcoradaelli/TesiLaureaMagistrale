import numpy as np
from walks_core import qrw,crw,anello
from strumenti_analisi import convoluzione as conv

a = anello.anello(25)
q_walk = qrw.walker(anello_ospite=a,
                    posizione_iniziale=1,
                    moneta_iniziale=np.array([np.cos(np.pi/4), np.sin(np.pi/4)]))
c_walk = crw.walker(anello_ospite=anello,
                    posizione_iniziale=1)

for i in range(0,10):
    q_walk.passo()

distribuzione, appo= q_walk.ottieni_distribuzione_probabilita()
tdf = conv.trasformata_fourier(distribuzione)

print(distribuzione)
print(tdf)
print(conv.diaconis_shashahani_bound(distribuzione,100))
print(conv.entropy_convolution_bound(distribuzione,100))