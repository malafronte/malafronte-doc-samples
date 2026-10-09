"""Dataclass mutabile e valore RGB frozen (OOP-03 H–I, OOP-04 A–C).

Le due versioni conservano lo stesso dominio della classe esplicita;
validazione e regola delle componenti sono importate dal modulo precedente.
I nomi dei tipi sono distinti: campi corrispondenti non bastano per ==.
"""

from dataclasses import FrozenInstanceError, dataclass, field
from typing import ClassVar

from colori_espliciti_u14 import componente_valida, valida_rgb


@dataclass
class ColoreRGBDataclass:
    rosso: int
    verde: int
    blu: int

    def __post_init__(self):
        valida_rgb(self.rosso, self.verde, self.blu)

    def __str__(self):
        return f"RGB({self.rosso}, {self.verde}, {self.blu})"


@dataclass(frozen=True)
class ColoreRGB:
    rosso: int
    verde: int
    blu: int
    modello: ClassVar[str] = "RGB"

    def __post_init__(self):
        valida_rgb(self.rosso, self.verde, self.blu)

    def come_tupla(self):
        return (self.rosso, self.verde, self.blu)

    @classmethod
    def nero(cls):
        return cls(0, 0, 0)

    @classmethod
    def bianco(cls):
        return cls(255, 255, 255)

    @staticmethod
    def componente_valida(valore):
        return componente_valida(valore)

    def __str__(self):
        return f"RGB({self.rosso}, {self.verde}, {self.blu})"


@dataclass
class SchedaColori:
    """Contenitore pubblico per osservare default_factory, non una Palette."""

    titolo: str
    colori: list = field(default_factory=list)


@dataclass(frozen=True)
class DiarioFrozen:
    """Controesempio all'immutabilità profonda: la lista può ancora mutare."""

    titolo: str
    voci: list = field(default_factory=list)


if __name__ == "__main__":
    mutabile = ColoreRGBDataclass(12, 80, 160)
    mutabile.blu = -1  # DELIBERATAMENTE SCORRETTO: post_init non viene richiamato.
    print("stato invalido dopo l'assegnamento:", repr(mutabile))
    colore = ColoreRGB(12, 80, 160)
    try:
        colore.blu = 200
    except FrozenInstanceError:
        print("assegnamento frozen rifiutato")
    precedente = colore
    colore = ColoreRGB(colore.rosso, colore.verde, 200)
    print("valore precedente:", precedente, "| nuovo:", colore)
    prima = SchedaColori("prima")
    seconda = SchedaColori("seconda")
    prima.colori.append(colore)
    print("liste distinte:", prima.colori is not seconda.colori)
    diario = DiarioFrozen("prove")
    diario.voci.append("nota")
    print("contenuto mutabile:", diario.voci)
