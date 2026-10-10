"""Struttura richiesta al collaboratore; semantica documentata nel capitolo."""

from pathlib import Path
from typing import Protocol

from rilevazioni_u15 import Rilevazione


class Esportatore(Protocol):
    def esporta(self, rilevazioni: list[Rilevazione], percorso: Path) -> None:
        """Interfaccia: dati conservati; ValueError o OSError sul fallimento."""
        ...
