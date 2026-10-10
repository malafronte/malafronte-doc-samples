"""Variante nominale: base astratta con codice comune per valida."""

from abc import ABC, abstractmethod

from politiche_duck_u15 import valida_intero


class PoliticaSelezione(ABC):
    def valida(self, valore):
        valida_intero(valore)

    @abstractmethod
    def ammette(self, valore):
        raise NotImplementedError("la classe concreta realizza la decisione")


class PoliticaSogliaMinima(PoliticaSelezione):
    def __init__(self, minimo):
        self.valida(minimo)
        self._minimo = minimo

    def ammette(self, valore):
        self.valida(valore)
        return valore >= self._minimo


class PoliticaIntervallo(PoliticaSelezione):
    def __init__(self, minimo, massimo):
        self.valida(minimo)
        self.valida(massimo)
        if minimo > massimo:
            raise ValueError("intervallo: minimo maggiore del massimo")
        self._minimo = minimo
        self._massimo = massimo

    def ammette(self, valore):
        self.valida(valore)
        return self._minimo <= valore <= self._massimo
