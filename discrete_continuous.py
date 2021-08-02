from walks_core import qrw as qrw_discrete, qrw_continuous, physics_utilities as ph, anello as an
from Grafi import grafi
import numpy as np
from matplotlib import pyplot as plt

def ottieni_fattore_conversione(numero_passi_massimo=30,tempo_minimo=0, tempo_massimo=10, tempo_step=0.1, disegna_grafici=True):
    vett_numero_passi = []
    vett_tempi_fidelity_massima = []
    vett_fidelity_massime = []
    for numero_passi_discreto in range(2,numero_passi_massimo):
        vett_numero_passi.append(numero_passi_discreto)
        dimensione_spazio = max([numero_passi_discreto * 10,30])
        posizione_iniziale = int(dimensione_spazio / 2)
        moneta_iniziale = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4) * np.exp(1j * 0)])

        anello = an.anello(dimensione_spazio)
        grafo = grafi.grafo_linea(dimensione_spazio)

        dt_qrw = qrw_discrete.walker(anello, posizione_iniziale=posizione_iniziale, moneta_iniziale=moneta_iniziale)

        # Calcolo la distribuzione del rw discreto di riferimento.
        for passo in range(numero_passi_discreto):
            dt_qrw.passo()
        print("Finita evoluzione discreta.")
        # Medio tra due distribuzioni di probabilità successive in modo da evitare il problema della parità.
        ddp_dt_passo_1, appo = dt_qrw.ottieni_distribuzione_probabilita()
        dt_qrw.passo()
        ddp_dt_passo_2, appo = dt_qrw.ottieni_distribuzione_probabilita()
        ddp_dt = 1 / 2 * (ddp_dt_passo_1 + ddp_dt_passo_2)

        # Eseguo per tutti i tempi desiderati con il continuo.
        ct_qrw = qrw_continuous.walker(grafo, posizione_iniziale=posizione_iniziale)

        rete_tempi = np.arange(tempo_minimo, tempo_massimo, tempo_step)
        vett_fidelity = []
        for tempo in rete_tempi:
            ddp_ct = ct_qrw.ottieni_distribuzione_probabilita_a_tempo(tempo)
            # print(len(ddp_ct), "     ", len(ddp_dt))
            fidelity = ph.fidelity(ddp_ct, ddp_dt)
            # print("Tempo ", tempo, ":::: fidelity = ", fidelity)
            vett_fidelity.append(fidelity)

        fidelity_massima = max(vett_fidelity)
        tempo_fidelity_massima = rete_tempi[vett_fidelity.index(fidelity_massima)]
        vett_tempi_fidelity_massima.append(tempo_fidelity_massima)
        vett_fidelity_massime.append(fidelity_massima)
        stima_durata_passo = tempo_fidelity_massima / numero_passi_discreto
        print("Numero passi: ", numero_passi_discreto, "; Stima durata di un passo: ", stima_durata_passo)

    polinomio_fit = np.polyfit(vett_numero_passi, vett_tempi_fidelity_massima,1)
    print(polinomio_fit)
    trend_polinomio = np.poly1d(polinomio_fit)

    # Sistema di disegno (che può essere spento).
    if disegna_grafici:
        plt.plot(vett_numero_passi,vett_tempi_fidelity_massima,marker="+",markersize=15, linestyle="None")
        plt.plot(vett_numero_passi,trend_polinomio(vett_numero_passi))
        plt.title("Discrete-continuous relation")
        plt.xlabel("Number of discrete steps")
        plt.ylabel("Continuous time")

        a = plt.axes([0.25, 0.6, .2, .2])
        plt.title("Maximal fidelity")
        plt.xlabel("Steps")
        plt.ylabel("Fidelity")
        plt.plot(vett_numero_passi, vett_fidelity_massime)
        plt.show()

        plt.plot(vett_numero_passi,vett_fidelity_massime)
        plt.title("Maximal fidelity")
        plt.xlabel("Number of discrete steps")
        plt.ylabel("Fidelity")
        plt.show()

    return trend_polinomio.coefficients[0]

ottieni_fattore_conversione()