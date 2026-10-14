"""Persistenza JSON delle configurazioni (da completare, tappa FR-M7).

Contratto: lo schema versionato (`versione_schema = 1`) conserva i
parametri delle quattro famiglie, non i pixel; i complessi diventano
oggetti con chiavi `reale` e `immaginaria`; il salvataggio è atomico
(temporaneo nella stessa directory e sostituzione finale) e preserva il
file precedente in caso di errore; il caricamento fallito preserva la
configurazione corrente; booleani nei campi interi e costanti non finite
si rifiutano (requisito FR-09).
"""


def salva_configurazione(percorso: object, configurazione: object):
    """Salva la configurazione con scrittura atomica (da completare, FR-M7)."""
    raise NotImplementedError("FR-M7: validare, serializzare e sostituire alla fine.")


def carica_configurazione(percorso: object):
    """Carica e valida la configurazione (da completare, FR-M7)."""
    raise NotImplementedError("FR-M7: leggere, validare come la GUI, preservare il corrente.")
