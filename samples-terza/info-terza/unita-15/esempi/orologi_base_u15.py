"""Modello a minuti U15, autonomo dalla versione U13."""


def valida_intero(valore, nome):
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(f"{nome}: atteso un intero non booleano")


def valida_orario(ore, minuti):
    valida_intero(ore, "ore")
    valida_intero(minuti, "minuti")
    if not 0 <= ore <= 23 or not 0 <= minuti <= 59:
        raise ValueError("orario: ore 0–23 e minuti 0–59")


class OrologioDigitale:
    """Orario software; gli aggiornamenti riusciti restituiscono None."""

    def __init__(self, ore=0, minuti=0):
        valida_orario(ore, minuti)
        self._minuti = ore * 60 + minuti

    def imposta(self, ore, minuti):
        valida_orario(ore, minuti)
        self._minuti = ore * 60 + minuti
        return None

    def avanza(self, minuti_trascorsi):
        valida_intero(minuti_trascorsi, "minuti trascorsi")
        if minuti_trascorsi < 0:
            raise ValueError("minuti trascorsi: atteso un valore non negativo")
        self._minuti = (self._minuti + minuti_trascorsi) % 1440
        return None

    def leggi(self):
        return self._minuti // 60, self._minuti % 60

    def testo(self):
        ore, minuti = self.leggi()
        return f"{ore:02d}:{minuti:02d}"

    def descrizione(self):
        return f"Ora {self.testo()}"
