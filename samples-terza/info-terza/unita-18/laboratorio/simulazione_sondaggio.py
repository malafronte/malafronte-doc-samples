"""Simulazione completa del sondaggio per il laboratorio LAB-PY-U18.

Il modulo è fornito completo: la simulazione con il marcatore nella posizione
6 (caso LAB18-13) usa questi strumenti senza richiedere allo studente una
seconda implementazione. La politica e i tre stati delle posizioni sono quelli
del capitolo: ricerca oltre i marcatori, aggiornamento della chiave presente e
riuso del marcatore dopo la verifica dei duplicati.
"""

from __future__ import annotations

from tracce_sondaggio_u18 import SondaggioLineare, traccia_canonica

__all__ = ["SondaggioLineare", "traccia_canonica", "simulazione_lab13"]


def simulazione_lab13():
    """Esegue la simulazione del caso LAB18-13 e ne restituisce gli esiti.

    La sequenza inserisce `5, 12, 19`, rimuove `12`, cerca e aggiorna `19`:
    ogni esito è una coppia `(posizione_o_valore, spiegazione)` verificata
    dalla suite pubblica.
    """
    tabella = SondaggioLineare(7)
    tabella.inserisci(5, "E5")
    tabella.inserisci(12, "E12")
    tabella.inserisci(19, "E19")
    posizioni_iniziali = [p for p, s in enumerate(tabella.fotografia()) if s[0] == "occupata"]
    tabella.rimuovi(12)
    valore_oltre_marcatore = tabella.cerca(19)
    tabella.inserisci(19, "E19b")
    tabella.inserisci(26, "E26")
    return {
        "posizioni_iniziali": posizioni_iniziali,
        "valore_19_oltre_marcatore": valore_oltre_marcatore,
        "valore_19_aggiornato": tabella.cerca(19),
        "posizione_riusata_26": tabella.fotografia()[6],
        "marcatori_finali": tabella.marcatori,
    }
