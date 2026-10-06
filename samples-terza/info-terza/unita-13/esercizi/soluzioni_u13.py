"""Soluzioni eseguibili della banca di base U13.

Raccoglie il codice delle schede che richiedono una realizzazione completa:
PY-U13-T01 (`Serbatoio`), PY-U13-T02 (`Scontrino`), PY-U13-T04 (`Iscrizione`),
PY-U13-T06 (conversioni testuali di `Articolo`), PY-U13-X02 (`Contatore` con i
tre metodi a confronto) e PY-U13-X03 (`Orario` con le conversioni).

Ogni sezione è autonoma e dichiara il proprio contratto. Le schede
concettuali — C, P, E e X01 — hanno soluzione testuale nella pagina e non
richiedono un modulo. Ambiente: CPython sul computer.
"""

from articolo_u13 import CAMPI_ARTICOLO, Articolo, valida_dati_articolo

# --- PY-U13-T01: Serbatoio -------------------------------------------------


def _valida_intero_non_negativo(valore, nome):
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(f"{nome}: atteso un intero, ricevuto {type(valore).__name__}")
    if valore < 0:
        raise ValueError(f"{nome}: atteso un valore non negativo, ricevuto {valore}")


class Serbatoio:
    """Acqua contenuta in un serbatoio a capacità fissata.

    Invariante: `0 <= acqua <= capacita`, interi non booleani.
    """

    def __init__(self, capacita, acqua=0):
        _valida_intero_non_negativo(capacita, "capacita")
        _valida_intero_non_negativo(acqua, "acqua")
        if acqua > capacita:
            raise ValueError(f"acqua: {acqua} supera la capacita {capacita}")
        self._capacita = capacita
        self._acqua = acqua

    def stato(self):
        return {"capacita": self._capacita, "acqua": self._acqua}

    def spazio_libero(self):
        return self._capacita - self._acqua

    def riempi(self, litri):
        _valida_intero_non_negativo(litri, "litri")
        if self._acqua + litri > self._capacita:
            return False
        self._acqua = self._acqua + litri
        return True


# --- PY-U13-T02: Scontrino -------------------------------------------------


class Scontrino:
    """Totale di un acquisto in centesimi. Invariante: `totale >= 0`."""

    def __init__(self, totale):
        _valida_intero_non_negativo(totale, "totale")
        self._totale = totale

    def totale(self):
        return self._totale

    def aggiungi(self, prezzo_centesimi):
        _valida_intero_non_negativo(prezzo_centesimi, "prezzo_centesimi")
        candidato = self._totale + prezzo_centesimi
        self._totale = candidato
        return candidato


# --- PY-U13-T04: Iscrizione ------------------------------------------------


class Iscrizione:
    """Posti di un corso sportivo. Invariante: iscritti + posti = capacita."""

    def __init__(self, capacita):
        if isinstance(capacita, bool) or not isinstance(capacita, int):
            raise ValueError(f"capacita: atteso un intero, ricevuto {type(capacita).__name__}")
        if capacita <= 0:
            raise ValueError(f"capacita: atteso un valore positivo, ricevuto {capacita}")
        self._capacita = capacita
        self._iscritti = 0

    def stato(self):
        return {
            "capacita": self._capacita,
            "iscritti": self._iscritti,
            "posti_disponibili": self._capacita - self._iscritti,
        }

    def occupazione_percentuale(self):
        return self._iscritti * 100 // self._capacita

    def iscrivi(self, partecipanti):
        if isinstance(partecipanti, bool) or not isinstance(partecipanti, int):
            raise ValueError(
                f"partecipanti: atteso un intero, ricevuto {type(partecipanti).__name__}"
            )
        if partecipanti < 0:
            raise ValueError(
                f"partecipanti: atteso un valore non negativo, ricevuto {partecipanti}"
            )
        if partecipanti > self._capacita - self._iscritti:
            return False
        self._iscritti = self._iscritti + partecipanti
        return True


# --- PY-U13-T06: conversioni testuali di Articolo --------------------------


def _intero_da_testo(testo, campo, riferimento):
    try:
        return int(testo)
    except ValueError:
        raise ValueError(
            f"{riferimento}, campo '{campo}': il testo {testo!r} non è un intero"
        ) from None


def articolo_a_riga(articolo):
    """Proiezione testuale dell'articolo nell'ordine dello schema."""
    dati = articolo.dati()
    valida_dati_articolo(
        dati["codice"], dati["descrizione"], dati["quantita"], dati["prezzo_centesimi"]
    )
    return [
        dati["codice"],
        dati["descrizione"],
        str(dati["quantita"]),
        str(dati["prezzo_centesimi"]),
    ]


def riga_a_articolo(riga, riferimento_riga):
    """Istanza nuova da quattro campi testuali, con diagnosi distinte."""
    if len(riga) != len(CAMPI_ARTICOLO):
        attesi = ", ".join(CAMPI_ARTICOLO)
        raise ValueError(
            f"{riferimento_riga}: attesi {len(CAMPI_ARTICOLO)} campi ({attesi}), "
            f"ricevuti {len(riga)}"
        )
    quantita = _intero_da_testo(riga[2], "quantita", riferimento_riga)
    prezzo = _intero_da_testo(riga[3], "prezzo_centesimi", riferimento_riga)
    try:
        return Articolo(riga[0], riga[1], quantita, prezzo)
    except ValueError as errore:
        raise ValueError(f"{riferimento_riga}: {errore}") from None


# --- PY-U13-X02: mutazione, riassegnamento e nuova istanza -----------------


class ContatoreTreMetodi:
    """Contatore con tre metodi che agiscono in modo diverso sul chiamante."""

    def __init__(self, valore):
        self.valore = valore

    def muta(self, nuovo):
        self.valore = nuovo
        return self.valore

    def riassegna(self, nuovo):
        self = ContatoreTreMetodi(nuovo)
        return self.valore

    def ricostruisce(self, nuovo):
        return ContatoreTreMetodi(nuovo)


# --- PY-U13-X03: Orario e le sue conversioni -------------------------------


class Orario:
    """Minuti trascorsi da mezzanotte, da 0 a 1439 compresi."""

    def __init__(self, minuti):
        if isinstance(minuti, bool) or not isinstance(minuti, int):
            raise ValueError(f"minuti: atteso un intero, ricevuto {type(minuti).__name__}")
        if minuti < 0 or minuti > 1439:
            raise ValueError(f"minuti: atteso un valore fra 0 e 1439, ricevuto {minuti}")
        self._minuti = minuti

    def dati(self):
        return {"minuti": self._minuti}


INTESTAZIONE_ORARIO = ("minuti",)


def orario_a_campi(orario):
    return [str(orario.dati()["minuti"])]


def campi_a_orario(campi, riferimento):
    if len(campi) != len(INTESTAZIONE_ORARIO):
        raise ValueError(
            f"{riferimento}: attesi {len(INTESTAZIONE_ORARIO)} campi, ricevuti {len(campi)}"
        )
    minuti = _intero_da_testo(campi[0], "minuti", riferimento)
    try:
        return Orario(minuti)
    except ValueError as errore:
        raise ValueError(f"{riferimento}: {errore}") from None


def dati_a_orario(dati):
    if not isinstance(dati, dict):
        raise ValueError(f"dati: atteso un dizionario, ricevuto {type(dati).__name__}")
    if "minuti" not in dati:
        raise ValueError("campo 'minuti': mancante")
    extra = [chiave for chiave in dati if chiave != "minuti"]
    if extra:
        raise ValueError(f"campo '{extra[0]}': non previsto dallo schema")
    return Orario(dati["minuti"])


if __name__ == "__main__":
    serbatoio = Serbatoio(10, 4)
    print("Serbatoio spazio libero:", serbatoio.spazio_libero())
    print("Serbatoio riempi(6):", serbatoio.riempi(6), serbatoio.stato())
    print("Scontrino:", Scontrino(0).aggiungi(250))
    iscrizione = Iscrizione(20)
    print("Iscrizione iscrivi(5):", iscrizione.iscrivi(5), iscrizione.stato())
    riga = articolo_a_riga(Articolo("007", "Vite, lunga", 4, 25))
    print("Articolo riga:", riga)
    print("Articolo ricostruito:", riga_a_articolo(riga, "record 1").dati())
    c = ContatoreTreMetodi(1)
    alias = c
    print("X02 muta:", c.muta(5), c.valore, alias.valore)
    print("X02 riassegna:", c.riassegna(9), c.valore)
    print("X02 ricostruisce:", c.ricostruisce(7).valore, c.valore)
    orario = Orario(720)
    print("Orario round-trip:", campi_a_orario(orario_a_campi(orario), "r1").dati())
