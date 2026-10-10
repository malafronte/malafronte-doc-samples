# Confine MicroPython — ESP-07

La suite U15 verifica solo CPython e collaboratori simulati.
Le pagine ESP-00/ESP-04/ESP-06 non specificano ancora modello di scheda,
sensore, pinout e firmware: nessun adattatore `machine`, cablaggio o fattore
di conversione viene quindi presentato come verificato.

Prima della prova su scheda registrare modello, revisione, firmware,
datasheet del sensore, unità native, tensioni, pin e schema approvato dal docente.
Il contratto richiesto è `leggi()` → numero finito in °C, bool escluso,
con errore documentato; `accendi()`/`spegni()` → None.
L'esaurimento è specifico del simulatore finito, non imposto al sensore reale.

Tenere il modulo che importa `machine` distinto dalla logica; verificare prima
gli import sul firmware, poi unità e letture con uno strumento di confronto,
infine comandi e condizioni di errore. Montare disalimentato; usare soltanto
carichi didattici in bassa tensione approvati, senza rete elettrica o attuatori di potenza.
La prova elettrica e quella software hanno verbali distinti.
