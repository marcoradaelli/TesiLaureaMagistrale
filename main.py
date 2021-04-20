import numpy as np
import random
from walks_core import crw, qrw, physics_utilities as ph
from strumenti_analisi import analisi_randomness as ar

# Parametri della simulazione.
numero_punti_anello = 33
posizione_iniziale = 4
numero_run_montecarlo = 1
numero_passi_prima_della_misura = 1000
lunghezza_stringa = 100

# Nel caso quantistico servono dei parametri di moneta iniziali.
delta = np.pi/4
eta = 0
moneta_iniziale = np.array([np.cos(delta), np.sin(delta)*np.exp(1j*eta)])

# Creo un anello classico ed uno quantistico, uguali.
anello_quantistico = qrw.anello(numero_punti=numero_punti_anello)
anello_classico = crw.anello(numero_punti=numero_punti_anello)

# Vettori per i risultati.
risultati_shannon_quantistico = []
risultati_shannon_classico = []

# Avvio i run del MonteCarlo.
random.seed(1)
for run in range(0,numero_run_montecarlo):
    # Stringhe di numeri ottenuti.
    stringa_quantistico = []
    stringa_classico = []

    # Inizializzo la posizione.
    posizione_attuale_classico = posizione_iniziale
    posizione_attuale_quantistico = posizione_iniziale
    for iterazione in range(0, lunghezza_stringa):
        # Creo due walker identici, uno quantistico e uno classico.
        walker_quantistico = qrw.walker(anello_ospite=anello_quantistico,
                                        posizione_iniziale=posizione_attuale_quantistico,
                                        moneta_iniziale=moneta_iniziale)
        walker_classico = crw.walker(anello_ospite=anello_classico,
                                     posizione_iniziale=posizione_attuale_classico)
        # Faccio evolvere entrambi i walker per il numero di passi previsto.
        for evoluzione in range(0,numero_passi_prima_della_misura):
            walker_quantistico.passo()
            walker_classico.passo()
        # Alla fine delle evoluzioni eseguo una misura su entrambi, e salvo il risultato.
        misura_quantistica = walker_quantistico.esegui_misura()
        misura_classica = walker_classico.esegui_misura()
        stringa_quantistico.append(misura_quantistica)
        stringa_classico.append(misura_classica)
        # La nuova posizione iniziale sarà quella finale dell'attuale iterazione, per entrambi i walk.
        posizione_attuale_classico = misura_classica
        posizione_attuale_quantistico = misura_quantistica

    # Alla fine di un run MonteCarlo mi trovo con due stringhe di numeri casuali ottenute con i due metodi.
    # Calcolo le distribuzioni a partire dai risultati.
    distribuzione_quantistica = ph.calcola_distribuzione_da_risultati(stringa_quantistico)
    distribuzione_classica = ph.calcola_distribuzione_da_risultati(stringa_classico)
    # Calcolo le entropie di Shannon corrispondenti.
    risultati_shannon_quantistico.append(ph.entropia_shannon(distribuzione_quantistica))
    risultati_shannon_classico.append(ph.entropia_shannon(distribuzione_classica))

    print("Terminato MC run ", run, "::: Shannon quantistica: ", ph.entropia_shannon(distribuzione_quantistica),
          "      Shannon classica: ", ph.entropia_shannon(distribuzione_classica))

    # Preparo le stringhe binarie da sottoporre ai test.
    stringa_binaria_quantistico = ph.converti_in_stringa_binaria(stringa_quantistico)
    stringa_binaria_classico = ph.converti_in_stringa_binaria(stringa_classico)
    print("Quantistico: ", ar.esegui_tutti_test(stringa_binaria_quantistico))
    print("Classico: ", ar.esegui_tutti_test(stringa_binaria_classico))

# Alla fine di tutti i run MonteCarlo ho una serie di stime di entropia.
risultati_shannon_quantistico = np.array(risultati_shannon_quantistico)
risultati_shannon_classico = np.array(risultati_shannon_classico)
average_shannon_quantistico = np.average(risultati_shannon_quantistico)
average_shannon_classico = np.average(risultati_shannon_classico)
devstd_shannon_quantistico = np.std(risultati_shannon_quantistico)
devstd_shannon_classico = np.std(risultati_shannon_classico)

print("Quantistico: ", average_shannon_quantistico, " +/- ", devstd_shannon_quantistico)
print("Classico: ", average_shannon_classico, " +/-", devstd_shannon_classico)