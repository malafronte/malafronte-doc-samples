"""Simulazione CPython: numeri finiti, °C, errore prima del comando."""

from math import isfinite


class LetturaEsaurita(Exception):
    """Il simulatore ha consumato tutte le posizioni."""


def valida_lettura(valore):
    if isinstance(valore, bool) or not isinstance(valore, (int, float)):
        raise ValueError("lettura: atteso numero non booleano")
    try:
        finito = isfinite(valore)
    except OverflowError as errore:
        raise ValueError("lettura: numero fuori dalla rappresentazione supportata") from errore
    if not finito:
        raise ValueError("lettura: atteso numero finito")


class SensoreCelsius:
    def __init__(self, sequenza):
        self._sequenza = list(sequenza)
        self._indice = 0

    @property
    def consumate(self):
        return self._indice

    def leggi(self):
        if self._indice == len(self._sequenza):
            raise LetturaEsaurita("sequenza terminata")
        valore = self._sequenza[self._indice]
        self._indice += 1
        valida_lettura(valore)
        return valore


class SensoreDecimi:
    def __init__(self, sequenza):
        self._sorgente = SensoreCelsius(sequenza)

    @property
    def consumate(self):
        return self._sorgente.consumate

    def leggi(self):
        valore = self._sorgente.leggi()
        if not isinstance(valore, int):
            raise ValueError("decimi: atteso intero non booleano")
        return valore / 10


class AttuatoreSimulato:
    def __init__(self):
        self._acceso = False

    @property
    def acceso(self):
        return self._acceso

    def accendi(self):
        self._acceso = True
        return None

    def spegni(self):
        self._acceso = False
        return None


class Controllore:
    def __init__(self, sensore, attuatore, soglia):
        valida_lettura(soglia)
        self._sensore = sensore
        self._attuatore = attuatore
        self._soglia = soglia
        self._passi = 0

    @property
    def passi(self):
        return self._passi

    def passo(self):
        lettura = self._sensore.leggi()
        valida_lettura(lettura)
        if lettura < self._soglia:
            self._attuatore.accendi()
        else:
            self._attuatore.spegni()
        self._passi += 1
        return None


class ControlloreIsteresi:
    def __init__(self, sensore, attuatore, minima, massima):
        valida_lettura(minima)
        valida_lettura(massima)
        if minima >= massima:
            raise ValueError("soglie: richiesta minima < massima")
        self._sensore = sensore
        self._attuatore = attuatore
        self._minima = minima
        self._massima = massima
        self._passi = 0

    @property
    def passi(self):
        return self._passi

    def passo(self):
        lettura = self._sensore.leggi()
        valida_lettura(lettura)
        if lettura < self._minima:
            self._attuatore.accendi()
        elif lettura >= self._massima:
            self._attuatore.spegni()
        self._passi += 1
        return None
