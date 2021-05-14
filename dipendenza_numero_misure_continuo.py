from protocolli import protocollo_anello_continuo
import random
import time

# Inizializzo il seed del random.
random.seed(1)

vett_numero_passi = []
vett_average_quantistico = []
vett_average_classico = []
vett_devstd_quantistico = []
vett_devstd_classico = []

# File di output.
out = open("data/dipendenza_numero_misure_continuo.txt", mode="a")
out.write("$ tempo prima di misura /// ave quantistico /// devstd quantistico"
          "/// ave classico /// devstd classico\n")
out.write("# Timestamp di esecuzione: " + str(time.time()) + "\n")
tempo_iniziale = time.time()

# Ciclo sul numero di passi da fare prima di una misura.
for tempo_prima_della_misura in range(1,20):
    print("===== AVVIO PER TEMPO ", tempo_prima_della_misura, " =====")

    vett_numero_passi.append(tempo_prima_della_misura)
    # Creo un esperimento MC per il protocollo anello con il dato numero di passi prima della misura.
    esperimento = protocollo_anello_continuo.protocollo_anello(numero_punti_anello=25,
                                                      posizione_iniziale=5,
                                                      numero_run_montecarlo=100,
                                                      tempo_prima_della_misura=tempo_prima_della_misura,
                                                      lunghezza_stringa=100)
    risultati = esperimento.esegui()
    vett_average_quantistico.append(risultati['average_quantistico'])
    vett_average_classico.append(risultati['average_classico'])
    vett_devstd_quantistico.append(risultati['devstd_quantistico'])
    vett_devstd_classico.append(risultati['devstd_classico'])

    out.write(str(tempo_prima_della_misura) + "///" + str(risultati['average_quantistico']) + "///" +
              str(risultati['devstd_quantistico']) + "///" + str(risultati['average_classico']) + "///" +
              str(risultati['devstd_classico']) + "\n")

    print("Eseguita scrittura su file.")

out.write("# Tempo di esecuzione: " + str(time.time() - tempo_iniziale) + "\n")
out.close()