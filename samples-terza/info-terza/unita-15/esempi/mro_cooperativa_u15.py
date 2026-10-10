"""Diamante autonomo: cooperazione e stesso ricevente."""


class Base:
    def passaggi(self):
        return ["Base"]


class Sinistra(Base):
    def passaggi(self):
        return ["Sinistra"] + super().passaggi()


class Destra(Base):
    def passaggi(self):
        return ["Destra"] + super().passaggi()


class Derivata(Sinistra, Destra):
    def passaggi(self):
        return ["Derivata"] + super().passaggi()


class Invertita(Destra, Sinistra):
    def passaggi(self):
        return ["Invertita"] + super().passaggi()


if __name__ == "__main__":
    print([classe.__name__ for classe in Derivata.__mro__])
    print(Derivata().passaggi())
    print(Sinistra().passaggi())
    print(Invertita().passaggi())
