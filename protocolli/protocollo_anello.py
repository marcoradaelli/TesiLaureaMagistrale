import numpy as np
from walks_core import crw, qrw, physics_utilities as ph


class protocollo_anello:
    def __init__(self, numero_punti_anello, posizione_iniziale, numero_run_montecarlo, numero_passi_prima_della_misura, lunghezza_stringa, delta_moneta = np.pi/4, eta_moneta = 0):
        self.numero_punti_anello = numero_punti_anello
        self.posizione_iniziale = posizione_iniziale
        self.numero_run_montecarlo = numero_run_montecarlo
        self.numero_passi_prima_della_misura = numero_passi_prima_della_misura
        self.lunghezza_stringa = lunghezza_stringa

        # Nel caso quantistico servono dei parametri di moneta iniziali.
        self.moneta_iniziale = np.array([np.cos(delta_moneta), np.sin(delta_moneta) * np.exp(1j * eta_moneta)])

        # Creo un anello classico ed uno quantistico, uguali.
        self.anello_quantistico = qrw.anello(numero_punti=self.numero_punti_anello)
        self.anello_classico = crw.anello(numero_punti=self.numero_punti_anello)

        # Crea i vettori per i dati.
        self.risultati_shannon_quantistico = []
        self.risultati_shannon_classico = []

    def esegui(self):
        for run in range(0, self.numero_run_montecarlo):
            # Stringhe di numeri ottenuti.
            stringa_quantistico = []
            stringa_classico = []

            # Inizializzo la posizione.
            posizione_attuale_classico = self.posizione_iniziale
            posizione_attuale_quantistico = self.posizione_iniziale
            for iterazione in range(0, self.lunghezza_stringa):
                # Creo due walker identici, uno quantistico e uno classico.
                walker_quantistico = qrw.walker(anello_ospite=self.anello_quantistico,
                                                posizione_iniziale=posizione_attuale_quantistico,
                                                moneta_iniziale=self.moneta_iniziale)
                walker_classico = crw.walker(anello_ospite=self.anello_classico,
                                             posizione_iniziale=posizione_attuale_classico)
                # Faccio evolvere entrambi i walker per il numero di passi previsto.
                for evoluzione in range(0, self.numero_passi_prima_della_misura):
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
            self.risultati_shannon_quantistico.append(ph.entropia_shannon(distribuzione_quantistica))
            self.risultati_shannon_classico.append(ph.entropia_shannon(distribuzione_classica))

            print("Terminato MC run ", run, "::: Shannon quantistica: ", ph.entropia_shannon(distribuzione_quantistica),
                  "      Shannon classica: ", ph.entropia_shannon(distribuzione_classica))

        # Alla fine di tutti i run MonteCarlo ho una serie di stime di entropia.
        self.risultati_shannon_quantistico = np.array(self.risultati_shannon_quantistico)
        self.risultati_shannon_classico = np.array(self.risultati_shannon_classico)
        self.average_shannon_quantistico = np.average(self.risultati_shannon_quantistico)
        self.average_shannon_classico = np.average(self.risultati_shannon_classico)
        self.devstd_shannon_quantistico = np.std(self.risultati_shannon_quantistico)
        self.devstd_shannon_classico = np.std(self.risultati_shannon_classico)

        print("Quantistico: ", self.average_shannon_quantistico, " +/- ", self.devstd_shannon_quantistico)
        print("Classico: ", self.average_shannon_classico, " +/-", self.devstd_shannon_classico)

        self.dict_risultati = {
            "average_quantistico": self.average_shannon_quantistico,
            "average_classico": self.average_shannon_classico,
            "devstd_quantistico": self.devstd_shannon_quantistico/np.sqrt(self.numero_run_montecarlo),
            "devstd_classico": self.devstd_shannon_classico/np.sqrt(self.numero_run_montecarlo)
        }

        return self.dict_risultati
