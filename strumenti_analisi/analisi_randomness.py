import numpy as np
from scipy import special as sc
from matplotlib import pyplot as plt
from nistrng import *

# I protocolli standard NIST sono costruiti per sequenze di bit.
# Questa libreria prende quindi in ingresso una stringa di bit.

# Questa funzione esegue di seguito i test, restituendo i valori in dizionario.
def esegui_tutti_test(stringa):
    dict_risposta = {}
    counter_test_superati = 0
    counter_test_falliti = 0

    dict_risposta['frequency-monobit'] = {}
    _frequency_monobit_test = frequency_monobit_test(stringa)
    dict_risposta['frequency-monobit']['p-value'] = _frequency_monobit_test[1]
    dict_risposta['frequency-monobit']['passed'] = _frequency_monobit_test[0]
    if _frequency_monobit_test[0]:
        counter_test_superati += 1
    else:
        counter_test_falliti += 1

    dict_risposta['runs'] = {}
    _runs_test = runs_test(stringa)
    dict_risposta['runs']['p-value'] = _runs_test[1]
    dict_risposta['runs']['passed'] = _runs_test[0]
    if _runs_test[0]:
        counter_test_superati += 1
    else:
        counter_test_falliti += 1

    # Alla fine registra anche i totali.
    dict_risposta['totale riusciti'] = counter_test_superati
    dict_risposta['totale falliti'] = counter_test_falliti
    return dict_risposta

def frequency_monobit_test(stringa):
    accumulatore = stringa.count("1") - stringa.count("0")

    valore_test = abs(accumulatore)/np.sqrt(len(stringa))
    p_value = sc.erfc(valore_test/np.sqrt(2.))

    # Ritorna sia se il test è passato sia il p-value.
    return (p_value > 0.01), p_value

def runs_test(stringa):
    vObs = 0
    # Frazione di 1.
    pi = stringa.count("1")
    n = len(stringa)
    stringa = list(stringa)

    for k in range(0,n-1):
        if stringa[k] != stringa[k+1]:
            vObs += 1

    p_value = sc.erfc(abs(vObs - 2*n*pi*(1-pi))/(2*np.sqrt(2*n)*pi*(1-pi)))

    return (p_value > 0.01), p_value

def esegui_tutti_automatico(stringa):
    stringa = np.array(list(stringa))
    eligible_battery: dict = check_eligibility_all_battery(stringa, SP800_22R1A_BATTERY)
    eligible_battery = eligible_battery['monobit']
    results = run_all_battery(stringa, eligible_battery, False)
    print("Test results:")
    for result, elapsed_time in results:
        if result.passed:
            print("- PASSED - score: " + str(
                np.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")
        else:
            print("- FAILED - score: " + str(
                np.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")

