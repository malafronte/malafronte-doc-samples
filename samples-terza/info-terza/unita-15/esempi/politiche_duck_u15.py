"""Letture sintetiche intere in °C; politiche autonome e client comune."""


def valida_intero(valore):
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError("atteso un intero non booleano")


def valida_valori(valori):
    if not isinstance(valori, list):
        raise ValueError("valori: attesa una lista")
    for valore in valori:
        valida_intero(valore)


class PoliticaSogliaMinima:
    def __init__(self, minimo):
        valida_intero(minimo)
        self._minimo = minimo

    def ammette(self, valore):
        valida_intero(valore)
        return valore >= self._minimo


class PoliticaIntervallo:
    def __init__(self, minimo, massimo):
        valida_intero(minimo)
        valida_intero(massimo)
        if minimo > massimo:
            raise ValueError("intervallo: minimo maggiore del massimo")
        self._minimo = minimo
        self._massimo = massimo

    def ammette(self, valore):
        valida_intero(valore)
        return self._minimo <= valore <= self._massimo


def seleziona(valori, politica):
    """Valida prima di delegare; preserva ordine, duplicati e lista ricevuta."""
    valida_valori(valori)
    risultato = []
    for valore in valori:
        ammesso = politica.ammette(valore)
        if type(ammesso) is not bool:
            raise TypeError("ammette: atteso esattamente bool")
        if ammesso:
            risultato.append(valore)
    return risultato
