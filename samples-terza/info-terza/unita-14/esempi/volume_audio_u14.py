"""VolumeAudio esteso con limite e candidato completo (OOP-03 C, OOP-04 B–C).

Invariante: 0 <= livello <= limite_massimo <= 100, con interi non booleani.
Ogni setter valida il nuovo stato; configura valuta l'intera coppia prima
delle scritture. Un errore di validazione non modifica alcun campo.
"""

from volume_audio_base_u14 import valida_livello


def valida_configurazione(livello, limite_massimo):
    valida_livello(livello)
    valida_livello(limite_massimo, "limite_massimo")
    if livello > limite_massimo:
        raise ValueError("livello: non può superare limite_massimo")


class VolumeAudio:
    """Impostazione audio con limite configurabile; non produce suoni."""

    def __init__(self, livello, limite_massimo=100):
        valida_configurazione(livello, limite_massimo)
        self._livello = livello
        self._limite_massimo = limite_massimo

    @property
    def livello(self):
        return self._livello

    @livello.setter
    def livello(self, valore):
        self.configura(valore, self._limite_massimo)

    @property
    def limite_massimo(self):
        return self._limite_massimo

    @limite_massimo.setter
    def limite_massimo(self, valore):
        self.configura(self._livello, valore)

    @property
    def silenzioso(self):
        return self._livello == 0

    def configura(self, livello, limite_massimo):
        valida_configurazione(livello, limite_massimo)
        self._livello = livello
        self._limite_massimo = limite_massimo
        return None


if __name__ == "__main__":
    for candidato in ((40, 50), (60, 50), (40, 120)):
        volume = VolumeAudio(70, 80)
        try:
            volume.configura(*candidato)
            print("configurazione accettata:", candidato)
        except ValueError as errore:
            print("configurazione rifiutata:", errore)
        print("stato:", (volume.livello, volume.limite_massimo))
