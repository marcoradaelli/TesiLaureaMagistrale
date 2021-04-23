# In questo codice studio gli effetti dell'inserimento di un canale depolarizzatore.
from walks_core import operatori_kraus as ch
from protocolli import protocollo_anello_density_matrix
import random
import time

# Inizializzo il seed del random.
random.seed(1)

vett_numero_passi = []
vett_average_quantistico = []
vett_average_classico = []
vett_devstd_quantistico = []
vett_devstd_classico = []

parametro_depolarizzazione = 1

# File di output.
out = open("data/dipendenza_numero_misure_depolarizzato.txt", mode="a")
out.write(f"# Valore parametro di depolarizzazione: {parametro_depolarizzazione}")
out.write("$ numero passi prima di misura /// ave noise /// devstd noise /// ave quantum /// devstd quantum \n")
out.write("# Timestamp di esecuzione: " + str(time.time()) + "\n")
tempo_iniziale = time.time()

# Ciclo sul numero di passi da fare prima di una misura.
for numero_passi_prima_della_misura in [5,10,20]:
    print("===== AVVIO PER NUMERO PASSI ", numero_passi_prima_della_misura, " =====")

    vett_numero_passi.append(numero_passi_prima_della_misura)
    # Creo un esperimento MC per il protocollo anello con il dato numero di passi prima della misura.
    operatori_kraus = ch.canale_depolarizzatore(parametro=parametro_depolarizzazione, dimensioni_anello=25).lista_operatori_kraus()
    esperimento = protocollo_anello_density_matrix.protocollo_anello(numero_punti_anello=25,
                                                      posizione_iniziale=5,
                                                      numero_run_montecarlo=10,
                                                      numero_passi_prima_della_misura=numero_passi_prima_della_misura,
                                                      lunghezza_stringa=100,
                                                      lista_operatori_kraus=operatori_kraus)
    risultati = esperimento.esegui()
    vett_average_quantistico.append(risultati['average_quantistico'])
    vett_devstd_quantistico.append(risultati['devstd_quantistico'])

    out.write(str(numero_passi_prima_della_misura) + "///" + str(risultati['average_quantistico']) + "///" +
              str(risultati['devstd_quantistico']) + "\n")

    print("Eseguita scrittura su file.")

out.write("# Tempo di esecuzione: " + str(time.time() - tempo_iniziale) + "\n")
out.close()