"""Dichiarazione strutturale per un checker; i test verificano la semantica."""

from typing import Protocol, runtime_checkable

from politiche_duck_u15 import valida_valori


@runtime_checkable
class PoliticaSelezione(Protocol):
    def ammette(self, valore: int) -> bool:
        """Dichiarazione di interfaccia per il controllo dei tipi."""
        ...


class SogliaAutonoma:
    def __init__(self, minimo: int):
        valida_valori([minimo])
        self._minimo = minimo

    def ammette(self, valore: int) -> bool:
        valida_valori([valore])
        return valore >= self._minimo


def seleziona(valori: list[int], politica: PoliticaSelezione) -> list[int]:
    valida_valori(valori)
    risultato = []
    for valore in valori:
        ammesso = politica.ammette(valore)
        if type(ammesso) is not bool:
            raise TypeError("ammette: atteso esattamente bool")
        if ammesso:
            risultato.append(valore)
    return risultato
