import numpy as np
from walks_core import qrw,anello
from strumenti_analisi import convoluzione as conv

a = anello.anello(25)
walk = qrw.walker(anello_ospite=a,
                  posizione_iniziale=1,
                  moneta_iniziale=np.array([np.cos(np.pi/4), np.sin(np.pi/4)]))

for i in range(0,10):
    walk.passo()

distribuzione, appo= walk.ottieni_distribuzione_probabilita()
tdf = conv.trasformata_fourier(distribuzione)

print(distribuzione)
print(tdf)