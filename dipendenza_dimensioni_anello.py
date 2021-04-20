from protocolli import protocollo_anello
import random
import time
import numpy as np

# Inizializzo il seed del random.
random.seed(1)

vett_punti_anello = []
vett_average_quantistico = []
vett_average_classico = []
vett_devstd_quantistico = []
vett_devstd_classico = []

# File di output.
out = open("data/dipendenza_punti_anello.txt", mode="a")
out.write("# Dipendenza delle performance dal numero di punti nell'anello\n")
out.write("$ numero punti anello /// ave quantistico /// devstd quantistico"
          "/// ave classico /// devstd classico /// entropia max\n")
out.write("# Timestamp di esecuzione: " + str(time.time()) + "\n")
tempo_iniziale = time.time()

# Ciclo sul numero di passi da fare prima di una misura.
for numero_punti_anello in range(3,49,2):
    print("===== AVVIO PER NUMERO PUNTI ANELLO ", numero_punti_anello, " =====")

    vett_punti_anello.append(numero_punti_anello)
    # Creo un esperimento MC per il protocollo anello con il dato numero di passi prima della misura.
    esperimento = protocollo_anello.protocollo_anello(numero_punti_anello=numero_punti_anello,
                                                      posizione_iniziale=1,
                                                      numero_run_montecarlo=100,
                                                      numero_passi_prima_della_misura=numero_punti_anello,
                                                      lunghezza_stringa=100)
    risultati = esperimento.esegui()
    vett_average_quantistico.append(risultati['average_quantistico'])
    vett_average_classico.append(risultati['average_classico'])
    vett_devstd_quantistico.append(risultati['devstd_quantistico'])
    vett_devstd_classico.append(risultati['devstd_classico'])

    out.write(str(numero_punti_anello) + "///" + str(risultati['average_quantistico']) + "///" +
              str(risultati['devstd_quantistico']) + "///" + str(risultati['average_classico']) + "///" +
              str(risultati['devstd_classico']) + "///" + str(np.log2(numero_punti_anello)) + "\n")

    print("Eseguita scrittura su file.")

out.write("# Tempo di esecuzione: " + str(time.time() - tempo_iniziale) + "\n")
out.close()