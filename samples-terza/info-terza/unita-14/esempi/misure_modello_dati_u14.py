"""Modello dati della misura: classe esplicita, dataclass e frozen (OOP-03, sez. F–I).

La misura del capitolo amplia quella della sezione J di OOP-02: ora il
record ha **due** campi, `codice` e `valore_cm`, e il capitolo li usa per
confrontare quattro scelte di rappresentazione.

Schema della misura:

| Campo | Tipo | Regola |
|---|---|---|
| `codice` | `str` | non vuoto, senza spazi agli estremi, confronto esatto |
| `valore_cm` | `int` | intero non booleano >= 0, in centimetri |

Le versioni, con nomi distinti per poterle confrontare nello stesso modulo:

- `MisuraEsplicita` — classe scritta a mano, con `__str__`, `__repr__` e
  `__eq__` che restituisce `NotImplemented` per i tipi estranei;
- `MisuraDataclass` — stessa struttura con `@dataclass`: `__init__`,
  `__repr__` ed `__eq__` sono generati, la validazione resta scritta in
  `__post_init__`;
- `MisuraFrozen` — dataclass `frozen=True` con soli contenuti immutabili:
  il valore conservato da raccolte e registri;
- `SchedaMisurazioni` — dataclass con `field(default_factory=list)`: ogni
  istanza costruisce la **propria** lista. Il default mutabile condiviso
  (`misure: list = []`) non è nemmeno definibile: `@dataclass` lo rifiuta
  alla definizione con `ValueError`, e i test mostrano il rifiuto;
- `DiarioFrozen` — dataclass frozen con una lista interna: mostra che
  `frozen` blocca gli assegnamenti, non le mutazioni dei contenuti;
- `MisuraCheStampa` — DELIBERATAMENTE DIFETTOSA: `__str__` che stampa
  invece di restituire la stringa.

L'uguaglianza è **di valore** su tutti i campi, con compatibilità del tipo
dichiarata: due misure con gli stessi dati sono uguali ma non identiche, e
una misura esplicita non diventa uguale a una dataclass solo perché i campi
corrispondono.

Ambiente: CPython sul computer. Dipende soltanto dal linguaggio.
"""

from dataclasses import dataclass, field


def _valida_codice(codice):
    """Controlla il codice: testo non vuoto, senza spazi agli estremi."""
    if not isinstance(codice, str):
        raise ValueError(f"campo 'codice': atteso testo, ricevuto {type(codice).__name__}")
    if codice == "":
        raise ValueError("campo 'codice': non può essere vuoto")
    if codice != codice.strip():
        raise ValueError(
            f"campo 'codice': spazi iniziali o finali non ammessi, ricevuto {codice!r}"
        )
    return None


def _valida_valore_cm(valore):
    """Controlla il valore: intero non booleano non negativo, in centimetri."""
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(f"campo 'valore_cm': atteso un intero, ricevuto {type(valore).__name__}")
    if valore < 0:
        raise ValueError(f"campo 'valore_cm': atteso un valore non negativo, ricevuto {valore}")
    return None


def valida_misura(codice, valore_cm):
    """Valida la coppia completa della misura. Unica sede delle regole."""
    _valida_codice(codice)
    _valida_valore_cm(valore_cm)
    return None


class MisuraEsplicita:
    """Misura con classe scritta a mano: str, repr ed eq espliciti.

    `__str__` restituisce il testo per chi legge; `__repr__` il testo
    diagnostico con tipo e campi. `__eq__` confronta tutti i campi e
    restituisce `NotImplemented` quando l'altro operando è di un tipo per il
    quale il confronto non è definito. Python può allora richiedere il
    confronto all'altro operando; se entrambi restituiscono `NotImplemented`,
    il ripiego di `==` è l'identità.
    """

    def __init__(self, codice, valore_cm):
        valida_misura(codice, valore_cm)
        self._codice = codice
        self._valore_cm = valore_cm

    @property
    def codice(self):
        return self._codice

    @property
    def valore_cm(self):
        return self._valore_cm

    def __str__(self):
        return f"{self._codice}: {self._valore_cm} cm"

    def __repr__(self):
        return f"MisuraEsplicita(codice={self._codice!r}, valore_cm={self._valore_cm})"

    def __eq__(self, altro):
        if not isinstance(altro, MisuraEsplicita):
            return NotImplemented
        return self._codice == altro._codice and self._valore_cm == altro._valore_cm


@dataclass
class MisuraDataclass:
    """Misura come dataclass: init, repr ed eq generati dal decoratore.

    Le annotazioni dichiarano i campi ma **non controllano** i valori: la
    validazione resta un codice scritto, eseguito da `__post_init__` alla
    costruzione. Le assegnazioni successive non passano da `__post_init__`.
    """

    codice: str
    valore_cm: int

    def __post_init__(self):
        valida_misura(self.codice, self.valore_cm)


@dataclass(frozen=True)
class MisuraFrozen:
    """Misura come valore: `frozen=True` blocca gli assegnamenti dei campi.

    Con soli contenuti immutabili (due stringhe/interi), il valore resta
    coerente per tutta la sua durata: è la forma adatta a essere conservata
    da una raccolta. Il tentativo di assegnare un campo solleva
    `dataclasses.FrozenInstanceError`.
    """

    codice: str
    valore_cm: int

    def __post_init__(self):
        valida_misura(self.codice, self.valore_cm)


@dataclass
class SchedaMisurazioni:
    """Scheda che raccoglie misure in una lista costruita per istanza.

    `field(default_factory=list)` chiama `list` a ogni costruzione: due
    schede hanno liste distinte e le aggiunte non si vedono fra loro.
    """

    titolo: str
    misure: list = field(default_factory=list)


@dataclass(frozen=True)
class DiarioFrozen:
    """Dataclass frozen con un contenuto mutabile: il limite di `frozen`.

    Gli assegnamenti dei campi sono bloccati, ma `voci` resta una lista:
    `voci.append(...)` continua a funzionare e cambia il valore osservato
    attraverso il campo. `frozen` non è immutabilità profonda.
    """

    titolo: str
    voci: list = field(default_factory=list)


class MisuraCheStampa:
    """DELIBERATAMENTE DIFETTOSA: `__str__` stampa invece di restituire.

    `__str__` deve **restituire** una stringa. Qui il metodo stampa un testo
    per conto proprio e restituisce `None`: `print` scrive il testo laterale
    e poi fallisce, perché `str()` non ha ricevuto una stringa. La classe
    serve a mostrare il sintomo, non è un modello da riusare.
    """

    def __init__(self, codice, valore_cm):
        valida_misura(codice, valore_cm)
        self._codice = codice
        self._valore_cm = valore_cm

    def __str__(self):
        print(f"{self._codice}: {self._valore_cm} cm")
        return None


if __name__ == "__main__":
    a = MisuraEsplicita("007", 12)
    b = MisuraEsplicita("007", 12)
    alias = a
    diversa = MisuraEsplicita("012", 12)
    print("str:", str(a), "| print:", end=" ")
    print(a)
    print("repr:", repr(a))
    print("in lista (usa repr):", [a, diversa])
    print("a == b:", a == b, "| a is b:", a is b)
    print("a == alias:", a == alias, "| a is alias:", a is alias)
    print("a == diversa:", a == diversa)
    print("chiamata diretta con tipo estraneo:", a.__eq__("007"))
    print("confronto ordinario con tipo estraneo:", a == "007")

    d = MisuraDataclass("007", 12)
    print("dataclass repr:", repr(d))
    print("dati uguali, tipi diversi:", a == d, "|", d == a)

    f = MisuraFrozen("007", 12)
    g = MisuraFrozen("007", 12)
    print("frozen uguali:", f == g, "| non identiche:", f is g)
    try:
        f.valore_cm = 20
    except Exception as errore:  # FrozenInstanceError, mostrata in pagina
        print("assegnamento frozen rifiutato:", type(errore).__name__)

    s1 = SchedaMisurazioni("prima")
    s2 = SchedaMisurazioni("seconda")
    s1.misure.append(MisuraDataclass("007", 12))
    print("liste indipendenti:", len(s1.misure), len(s2.misure))

    c1 = SchedaMisurazioni("prima")
    c2 = SchedaMisurazioni("seconda")
    print("liste indipendenti fin dalla costruzione:", c1.misure is c2.misure)

    diario = DiarioFrozen("prove")
    diario.voci.append("una voce")
    print("frozen con lista interna, mutazione riuscita:", diario.voci)

    print("versione difettosa, __str__ che stampa:")
    try:
        print(MisuraCheStampa("012", 30))
    except TypeError as errore:
        print("print rifiutata:", errore)

    for codice, valore in (("", 12), (" 7", 12), ("007", -1), ("007", True), ("007", "12")):
        try:
            MisuraDataclass(codice, valore)
        except ValueError as errore:
            print("costruzione rifiutata:", errore)
