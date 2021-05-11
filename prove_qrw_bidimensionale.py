from walks_core import qrw_2d, physics_utilities as phu
from matplotlib import pyplot as plt
import numpy as np

matrice_flip = np.eye(4)
numero_passi = 30

w = qrw_2d.walker(numero_punti_per_dimensione=10,tipo_moneta="personalizzata",matrice_flip_moneta=matrice_flip)

for passo in range(numero_passi):
    w.passo()
    ddp = w.ottieni_distribuzione_probabilita()
    plt.matshow(ddp)
    plt.savefig("data/graphs/grafici_2d_identita/" + str(passo) + ".png")
    plt.show()