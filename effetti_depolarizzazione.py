# In questo codice studio gli effetti dell'inserimento di un canale depolarizzatore.
from walks_core import canale_depolarizzatore as ch
from protocolli import protocollo_anello_density_matrix as pr

# Parametri della simulazione.
numero_punti_anello = 25
posizione_iniziale = 5
parametro_depolarizzatore = 0.1
numero_run_montecarlo = 100
numero_passi_prima_della_misura = 10
lunghezza_stringa = 200

# Creo gli operatori di Kraus.
operatori_kraus = ch.canale_depolarizzatore(parametro=parametro_depolarizzatore,
                                            dimensioni_anello=numero_punti_anello).lista_operatori_kraus()

# Creo la simulazione.
simulazione = pr.protocollo_anello(numero_punti_anello=numero_punti_anello,
                     posizione_iniziale=posizione_iniziale,
                     numero_run_montecarlo=numero_run_montecarlo,
                     numero_passi_prima_della_misura=numero_passi_prima_della_misura,
                     lunghezza_stringa=lunghezza_stringa,
                     lista_operatori_kraus=operatori_kraus)

# Esegue la simulazione.
simulazione.esegui()