"""Orologi dell'Unità 13: prima classe, varianti e interfaccia validata.

Orologio (OOP-02 A–F): attributi pubblici ore/minuti; dati validi forniti
dal chiamante, nessuna validazione. avanza restituisce la nuova coppia.
OrologioDigitale (OOP-02 G): dati interni e interfaccia validata equivalente
alle operazioni procedurali di OOP-01; avanza e imposta restituiscono None.
Entrambi sono modelli a 24 ore senza data né avanzamento automatico.
Le varianti didattiche illustrano difetti e confronti, non sono API da riusare.
Ambiente: CPython sul computer, nessuna dipendenza esterna.
"""


class Orologio:
    """Prima classe: ore/minuti e durata sono forniti validi dal chiamante."""

    def __init__(self, ore, minuti):
        self.ore = ore
        self.minuti = minuti

    def avanza(self, minuti_trascorsi):
        totale = self.ore * 60 + self.minuti
        candidato = (totale + minuti_trascorsi) % 1440
        self.ore = candidato // 60
        self.minuti = candidato % 60
        return self.ore, self.minuti

    def testo(self):
        return f"{self.ore:02d}:{self.minuti:02d}"


class OrologioConLocale:
    """Variante difettosa: calcola e restituisce, ma non modifica lo stato."""

    def __init__(self, ore, minuti):
        self.ore = ore
        self.minuti = minuti

    def avanza(self, minuti_trascorsi):
        totale = self.ore * 60 + self.minuti
        candidato = (totale + minuti_trascorsi) % 1440
        ore = candidato // 60
        minuti = candidato % 60
        return ore, minuti


class OrologioConSelfRiassegnato:
    """Variante didattica: self cambia oggetto, il riferimento esterno no."""

    def __init__(self, ore, minuti):
        self.ore = ore
        self.minuti = minuti

    def imposta_su_altro(self, ore, minuti):
        altro = Orologio(0, 0)
        self = altro
        self.ore = ore
        self.minuti = minuti
        return self.ore, self.minuti


class OrologioTreMetodi:
    """PY-U13-X02: dati validi assunti; mutazione, riassegnamento, creazione."""

    def __init__(self, ore, minuti):
        self.ore = ore
        self.minuti = minuti

    def muta(self, ore, minuti):
        self.ore = ore
        self.minuti = minuti
        return self.ore, self.minuti

    def riassegna(self, ore, minuti):
        self = OrologioTreMetodi(ore, minuti)
        return self.ore, self.minuti

    def ricostruisce(self, ore, minuti):
        return OrologioTreMetodi(ore, minuti)


def _valida_intero_non_negativo(valore, nome):
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(f"{nome}: atteso un intero, ricevuto {type(valore).__name__}")
    if valore < 0:
        raise ValueError(f"{nome}: atteso un valore non negativo, ricevuto {valore}")
    return None


def _valida_orario(ore, minuti):
    _valida_intero_non_negativo(ore, "ore")
    _valida_intero_non_negativo(minuti, "minuti")
    if ore >= 24:
        raise ValueError(f"ore: atteso un valore da 0 a 23, ricevuto {ore}")
    if minuti >= 60:
        raise ValueError(f"minuti: atteso un valore da 0 a 59, ricevuto {minuti}")
    return None


class OrologioDigitale:
    """Orologio validato: ore 0–23 e minuti 0–59, interi non booleani.

    Le garanzie riguardano lo stato inizialmente valido e le operazioni
    pubbliche: gli attributi interni sono tali per convenzione, non sono
    protetti da accessi arbitrari. Ogni errore lascia lo stato invariato.
    """

    def __init__(self, ore=0, minuti=0):
        _valida_orario(ore, minuti)
        self._ore = ore
        self._minuti = minuti

    def imposta(self, ore, minuti):
        _valida_orario(ore, minuti)
        self._ore = ore
        self._minuti = minuti
        return None

    def avanza(self, minuti_trascorsi):
        _valida_intero_non_negativo(minuti_trascorsi, "minuti_trascorsi")
        totale = self._ore * 60 + self._minuti
        candidato = (totale + minuti_trascorsi) % 1440
        self._ore = candidato // 60
        self._minuti = candidato % 60
        return None

    def leggi(self):
        return self._ore, self._minuti

    def testo(self):
        return f"{self._ore:02d}:{self._minuti:02d}"


if __name__ == "__main__":
    primo = OrologioDigitale(23, 58)
    secondo = OrologioDigitale(8, 15)
    primo.avanza(5)
    secondo.avanza(45)
    print(primo.testo(), secondo.testo())
    primo.imposta(12, 30)
    print(primo.testo(), secondo.testo())
