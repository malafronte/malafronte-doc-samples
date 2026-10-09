"""Prima versione di VolumeAudio: un campo controllato (OOP-03 A e B).

Il livello è un'impostazione intera da 0 a 100, non una misura in decibel.
La classe non riproduce suoni. Il silenzio è derivato dal livello zero.
Ambiente: CPython sul computer; nessuna dipendenza esterna.
"""


def valida_livello(valore, nome="livello"):
    """Rifiuta booleani, non interi e valori fuori da 0–100."""
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(f"{nome}: atteso un intero non booleano")
    if not 0 <= valore <= 100:
        raise ValueError(f"{nome}: atteso un valore da 0 a 100")


class VolumeAudio:
    """Impostazione modificabile attraverso la proprietà livello."""

    def __init__(self, livello):
        valida_livello(livello)
        self._livello = livello

    @property
    def livello(self):
        return self._livello

    @livello.setter
    def livello(self, valore):
        valida_livello(valore)
        self._livello = valore

    @property
    def silenzioso(self):
        return self._livello == 0


if __name__ == "__main__":
    volume = VolumeAudio(30)
    print(volume.livello, volume.silenzioso)
    volume.livello = 0
    print(volume.livello, volume.silenzioso)
    try:
        volume.livello = 120
    except ValueError as errore:
        print(errore)
    print(volume.livello, volume.silenzioso)
