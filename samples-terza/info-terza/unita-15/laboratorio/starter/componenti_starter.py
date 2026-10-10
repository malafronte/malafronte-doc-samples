"""LAB-PY-U15: client pronto, due componenti da completare deliberatamente."""

from pathlib import Path

from politiche_duck_u15 import PoliticaSogliaMinima, valida_intero
from rilevazioni_u15 import dataset, proiezioni
from servizio_rapporto_u15 import ServizioRapporto


class PoliticaIntervalloLaboratorio:
    def __init__(self, minimo, massimo):
        valida_intero(minimo)
        valida_intero(massimo)
        if minimo > massimo:
            raise ValueError("intervallo invertito")
        self._minimo = minimo
        self._massimo = massimo

    def ammette(self, valore):
        """Intero non booleano -> bool, estremi inclusi, nessuna modifica."""
        # TODO L03: validare la lettura e realizzare la decisione.
        raise NotImplementedError("L03: completare la politica")


class EsportatoreMemoriaLaboratorio:
    def __init__(self):
        self.chiamate = 0
        self.record = []
        self.percorso = None

    def esporta(self, rilevazioni, percorso):
        """Proiezioni copiate, Path registrato, una chiamata, ritorno None."""
        # TODO L05: validare prima di registrare; nessuna scrittura su disco.
        raise NotImplementedError("L05: completare il collaboratore")


def seleziona_rilevazioni(rilevazioni, politica):
    """Client pronto: lista nuova, ordine e duplicati, validazione preventiva."""
    proiezioni(rilevazioni)
    risultato = []
    for rilevazione in rilevazioni:
        ammesso = politica.ammette(rilevazione.valore)
        if type(ammesso) is not bool:
            raise TypeError("ammette: atteso bool")
        if ammesso:
            risultato.append(rilevazione)
    return risultato


def genera_rapporto(rilevazioni, politica, esportatore, percorso: Path):
    selezionate = seleziona_rilevazioni(rilevazioni, politica)
    return ServizioRapporto(esportatore).genera(selezionate, percorso)


def main():
    # L02: questa prima dimostrazione funziona prima dei completamenti.
    selezionate = seleziona_rilevazioni(dataset(), PoliticaSogliaMinima(18))
    print([(r.codice, r.valore) for r in selezionate])
    # L05: usare genera_rapporto con il collaboratore completato e Path scelto.


if __name__ == "__main__":
    main()
