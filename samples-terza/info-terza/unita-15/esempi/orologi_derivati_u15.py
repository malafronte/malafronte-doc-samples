"""Specializzazioni con lo stesso contratto delle operazioni comuni."""

from orologi_base_u15 import OrologioDigitale, valida_orario


class OrologioConEtichetta(OrologioDigitale):
    def __init__(self, ore, minuti, etichetta):
        if not isinstance(etichetta, str) or not etichetta.strip():
            raise ValueError("etichetta: atteso testo non vuoto")
        super().__init__(ore, minuti)
        self._etichetta = etichetta.strip()

    def descrizione(self):
        return f"{self._etichetta} — {self.testo()}"


class OrologioConSveglia(OrologioDigitale):
    def __init__(self, ore, minuti, ore_sveglia, minuti_sveglia):
        valida_orario(ore_sveglia, minuti_sveglia)
        super().__init__(ore, minuti)
        self._sveglia = (ore_sveglia, minuti_sveglia)

    def imposta_sveglia(self, ore, minuti):
        valida_orario(ore, minuti)
        self._sveglia = (ore, minuti)
        return None

    def leggi_sveglia(self):
        return self._sveglia

    def descrizione(self):
        ore, minuti = self._sveglia
        return f"{super().descrizione()}; sveglia {ore:02d}:{minuti:02d}"
