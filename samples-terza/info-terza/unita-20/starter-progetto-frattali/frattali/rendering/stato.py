"""Stato del rendering cooperativo a blocchi (da completare, tappa FR-M6).

Contratto: il lavoro fotografa la configurazione all'avvio, avanza per
blocchi di righe con identificatore crescente e stati
(`pronto`, `in_calcolo`, `annullato`, `completato`, `errore`); una callback
con identificatore diverso o stato diverso da `in_calcolo` non applica
alcun effetto; il risultato parziale resta etichettato e l'esportazione
riguarda l'ultimo risultato completo (requisiti FR-07 e FR-08).
"""

STATI_LAVORO = ("pronto", "in_calcolo", "annullato", "completato", "errore")


def nuovo_lavoro(configurazione: object, id_lavoro: object):
    """Crea un lavoro in stato `pronto` (da completare, FR-M6)."""
    raise NotImplementedError("FR-M6: fotografare la configurazione con identificatore.")


def avvia_lavoro(lavoro: object):
    """Porta il lavoro in `in_calcolo` (da completare, FR-M6)."""
    raise NotImplementedError("FR-M6: azzerare righe ed errore all'avvio.")


def annulla_lavoro(lavoro: object):
    """Annulla il lavoro conservando il parziale (da completare, FR-M6)."""
    raise NotImplementedError("FR-M6: True con passaggio ad annullato, False altrimenti.")


def esegui_blocco(lavoro: object, id_atteso: object, calcola_riga: object):
    """Esegue un blocco se lavoro e identificatore sono correnti (da completare, FR-M6)."""
    raise NotImplementedError("FR-M6: no-op su id diverso o stato non in_calcolo.")


def etichetta_risultato(lavoro: object):
    """Dichiara risultato completo, parziale o assente (da completare, FR-M6)."""
    raise NotImplementedError("FR-M6: completo solo se stato completato.")
