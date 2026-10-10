"""Il ricevente cls segue la classe sulla quale si chiama la factory."""

from orologi_base_u15 import valida_intero


class Contatore:
    def __init__(self, valore):
        valida_intero(valore, "valore")
        self.valore = valore

    @classmethod
    def zero(cls):
        return cls(0)


class ContatoreEtichettato(Contatore):
    def __init__(self, valore, etichetta="Conteggio"):
        super().__init__(valore)
        self.etichetta = etichetta
