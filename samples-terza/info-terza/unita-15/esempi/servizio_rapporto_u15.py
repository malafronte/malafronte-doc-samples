"""Coordinamento del caso d'uso e doppio di test in memoria."""

from pathlib import Path

from contratti_esportazione_u15 import Esportatore
from rilevazioni_u15 import Rilevazione, proiezioni


class EsportatoreMemoria:
    """Simula il salvataggio; osserva chiamate, dati e percorso."""

    def __init__(self):
        self.chiamate = 0
        self.record = []
        self.percorso = None

    def esporta(self, rilevazioni: list[Rilevazione], percorso: Path) -> None:
        record = proiezioni(rilevazioni)
        self.record = record
        self.percorso = percorso
        self.chiamate += 1


class ServizioRapporto:
    def __init__(self, esportatore: Esportatore):
        self._esportatore = esportatore

    def genera(self, rilevazioni: list[Rilevazione], percorso: Path) -> int:
        # Il dominio valida prima dell'effetto; una copia protegge la lista del chiamante.
        proiezioni(rilevazioni)
        if not isinstance(percorso, Path):
            raise ValueError("percorso: atteso Path")
        self._esportatore.esporta(list(rilevazioni), percorso)
        return len(rilevazioni)
