"""Caso intenzionalmente incompatibile per il checker; import sicuro."""

from typing import Protocol


class PoliticaSelezione(Protocol):
    def ammette(self, valore: int) -> bool:
        """Dichiarazione di interfaccia."""
        ...


class Corretta:
    def ammette(self, valore: int) -> bool:
        return valore >= 8


class FirmaErrata:
    def ammette(self, valore: int, limite: int) -> bool:
        return valore >= limite


def usa(politica: PoliticaSelezione) -> bool:
    return politica.ammette(8)


def contrasto():
    usa(Corretta())
    usa(FirmaErrata())  # Errore intenzionale: parametro obbligatorio aggiunto.
