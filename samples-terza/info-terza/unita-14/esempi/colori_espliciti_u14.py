"""ColoreRGB esplicito: metodi, rappresentazioni e uguaglianza (OOP-03 E–G).

RGB usa tre componenti intere non booleane da 0 a 255: rosso, verde, blu.
Il modulo rappresenta dati, senza finestre, immagini o conversioni cromatiche.
L'uguaglianza richiede lo stesso tipo concreto e tutte le componenti uguali.
"""


def componente_valida(valore):
    return isinstance(valore, int) and not isinstance(valore, bool) and 0 <= valore <= 255


def valida_rgb(rosso, verde, blu):
    for nome, valore in (("rosso", rosso), ("verde", verde), ("blu", blu)):
        if not componente_valida(valore):
            raise ValueError(f"{nome}: atteso un intero non booleano da 0 a 255")


class ColoreRGB:
    """Colore osservabile, senza aggiornamenti pubblici delle componenti."""

    def __init__(self, rosso, verde, blu):
        valida_rgb(rosso, verde, blu)
        self._rosso = rosso
        self._verde = verde
        self._blu = blu

    @property
    def rosso(self):
        return self._rosso

    @property
    def verde(self):
        return self._verde

    @property
    def blu(self):
        return self._blu

    def come_tupla(self):
        return (self._rosso, self._verde, self._blu)

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
        return f"RGB({self._rosso}, {self._verde}, {self._blu})"

    def __repr__(self):
        return f"ColoreRGB(rosso={self._rosso}, verde={self._verde}, blu={self._blu})"

    def __eq__(self, altro):
        if type(altro) is not type(self):
            return NotImplemented
        return (
            self._rosso == altro._rosso and self._verde == altro._verde and self._blu == altro._blu
        )


if __name__ == "__main__":
    a = ColoreRGB(12, 80, 160)
    b = ColoreRGB(12, 80, 160)
    print(a)
    print([a])
    print("valori uguali:", a == b, "| stessa istanza:", a is b)
    print("tipo estraneo:", a.__eq__((12, 80, 160)))
    print("nero:", ColoreRGB.nero().come_tupla())
    print("bianco:", ColoreRGB.bianco().come_tupla())
