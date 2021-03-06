# Simulazione di Quantum Random Walks

## Obiettivi
Questa libreria Python, basata su numpy, si propone di permettere la simulazione di random walk quantistici.
La libreria tenta di unire un approccio di simulazione MonteCarlo con un meccanismo più analitico. 

Il nocciolo della libreria è nella directory <code>walks_core</code>, e permette di simulare:
<ul>
<li> un random walk classico su anello (<code>crw_transition.py</code>)</li>
<li> un random walk quantistico su anello (<code>qrw.py</code>)</li>
<li> un random walk quantistico su anello in formalismo di matrice densità (<code>crw.py</code>)</li>
<li> un random walk quantistico su grafo (<code>qrw_grafo.py</code>, in costruzione)</li>
</ul>

In aggiunta, nella directory è presente il codice <code>physics_utilities.py</code> 
che permette di calcolare alcune funzionim utili all'analisi "veloce" dei random walks,
come l'entropia di Shannon. 
