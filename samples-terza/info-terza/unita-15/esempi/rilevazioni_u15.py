"""Valori sintetici e schema esplicito: il codice identifica la fonte."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rilevazione:
    codice: str
    valore: int
    unita: str = "°C"

    def __post_init__(self):
        if not isinstance(self.codice, str) or not self.codice.strip():
            raise ValueError("codice: atteso testo non vuoto")
        if isinstance(self.valore, bool) or not isinstance(self.valore, int):
            raise ValueError("valore: atteso intero non booleano")
        if self.unita != "°C":
            raise ValueError("unita: atteso °C")


def rilevazione_a_record(rilevazione):
    if not isinstance(rilevazione, Rilevazione):
        raise ValueError("attesa una Rilevazione valida")
    return {
        "codice": rilevazione.codice,
        "valore": rilevazione.valore,
        "unita": rilevazione.unita,
    }


def rilevazione_da_record(record):
    if not isinstance(record, dict) or set(record) != {"codice", "valore", "unita"}:
        raise ValueError("schema: attesi esattamente codice, valore, unita")
    return Rilevazione(record["codice"], record["valore"], record["unita"])


def proiezioni(rilevazioni):
    if not isinstance(rilevazioni, list):
        raise ValueError("rilevazioni: attesa una lista")
    return [rilevazione_a_record(rilevazione) for rilevazione in rilevazioni]


def dataset():
    return [
        Rilevazione("007", 18),
        Rilevazione("Lab, A", 20),
        Rilevazione('Sonda "B"', -2),
        Rilevazione("007", 18),
    ]
