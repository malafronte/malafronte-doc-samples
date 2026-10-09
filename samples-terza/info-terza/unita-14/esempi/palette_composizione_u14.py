"""Contenimento, condivisione e delega con volume e colori (OOP-04 A–C).

Palette compone la propria lista e condivide i valori RGB frozen.
PannelloAudio crea il proprio volume e aggrega una palette già esistente.
Nessuna GUI e nessuna riproduzione di suoni: si studiano dati e operazioni.
"""

from colori_modello_dati_u14 import ColoreRGB
from volume_audio_u14 import VolumeAudio


def testo_colori(colori):
    testi = []
    for colore in colori:
        testi.append(str(colore))
    return ", ".join(testi)


class Palette:
    """Sequenza di colori con lista propria; ripetizioni ammesse."""

    def __init__(self, colori):
        candidato = list(colori)
        for colore in candidato:
            if not isinstance(colore, ColoreRGB):
                raise ValueError("colori: attesi valori ColoreRGB frozen")
        self._colori = candidato

    def colori(self):
        return tuple(self._colori)

    def indice_di(self, cercato):
        if not isinstance(cercato, ColoreRGB):
            raise ValueError("cercato: atteso un ColoreRGB frozen")
        for indice, presente in enumerate(self._colori):
            if presente == cercato:
                return indice
        return None


class PannelloAudio:
    """Coordina un volume proprio e una palette esterna condivisibile."""

    def __init__(self, livello, limite_massimo, palette):
        if not isinstance(palette, Palette):
            raise ValueError("palette: attesa una Palette")
        self._volume = VolumeAudio(livello, limite_massimo)
        self._palette = palette

    @property
    def livello(self):
        return self._volume.livello

    @property
    def silenzioso(self):
        return self._volume.silenzioso

    def configura_volume(self, livello, limite_massimo):
        return self._volume.configura(livello, limite_massimo)

    def testo_posizione(self, colore):
        indice = self._palette.indice_di(colore)
        if indice is None:
            return "colore assente"
        return f"colore in posizione {indice}"


if __name__ == "__main__":
    blu = ColoreRGB(12, 80, 160)
    elenco = [blu, ColoreRGB.bianco()]
    palette = Palette(elenco)
    elenco.append(ColoreRGB.nero())
    print("dimensioni:", len(elenco), len(palette.colori()))
    print("elemento condiviso:", palette.colori()[0] is blu)
    print("ricerca per valore:", palette.indice_di(ColoreRGB(12, 80, 160)))
    primo = PannelloAudio(70, 80, palette)
    secondo = PannelloAudio(20, 80, palette)
    primo.configura_volume(40, 50)
    print("volumi indipendenti:", primo.livello, secondo.livello)
    print(primo.testo_posizione(ColoreRGB(12, 80, 160)))
    print(secondo.testo_posizione(ColoreRGB.nero()))
