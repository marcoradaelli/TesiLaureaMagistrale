from walks_core import qrw_density_matrix as qrw, anello, operatori_kraus as kraus, physics_utilities as phu, qrw as qrw_puro
import numpy as np
from matplotlib import pyplot as plt

numero_passi = 150
numero_punti = numero_passi * 2 + 2
parametro_depo = 0
lista_kraus = kraus.canale_depolarizzatore(parametro_depo,numero_punti).lista_operatori_kraus()
a = anello.anello(numero_punti)
# moneta_iniziale = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)])
moneta_iniziale = [1,0]
w = qrw.walker(a,0, moneta_iniziale,lista_kraus)
w_puro = qrw_puro.walker(a,0,moneta_iniziale)

np.set_printoptions(precision=2, suppress=True)

vett_vonneumann_generale = []
vett_vonneumann_posizionale = []

for passo in range(numero_passi):
    w.passo()
    w_puro.passo()

    matrice_densita = w.matrice_densita
    matrice_densita_puro = np.outer(w_puro.stato_totale, w_puro.stato_totale.conj())

    print(f"=== PASSO {passo}. Matrici equivalenti? {np.allclose(matrice_densita,matrice_densita_puro)}")
    print(f"Traccia misto: {np.trace(matrice_densita)}, traccia puro: {np.trace(matrice_densita_puro)}")

    md_posizione = phu.traccia_parziale_coin(matrice_densita)

    #print(f"Purezza generale: {phu.purezza(matrice_densita)}")
    #print(f"Purezza posizionale: {phu.purezza(md_posizione)}")
    print(f"Entropia Von Neumann generale: {phu.entropia_von_neumann(matrice_densita)}")
    print(f"Entropia Von Neumann posizionale (=entanglement entropy): {phu.entropia_von_neumann(md_posizione)}")

    vett_vonneumann_generale.append(phu.entropia_von_neumann(matrice_densita))
    vett_vonneumann_posizionale.append(phu.entropia_von_neumann(md_posizione))

plt.title("Entanglement entropy vs steps")
plt.xlabel("Steps")
plt.ylabel("Entanglement entropy")
plt.plot(vett_vonneumann_posizionale, label="Positional")
plt.show()