"""Articolo con proprietà e DatiArticolo frozen (OOP-03, sez. K; OOP-04, richiami).

Confronto circoscritto con la versione U13 (`articolo_u13.py`): lo **schema
esterno non cambia** — quattro campi `codice`, `descrizione`, `quantita`,
`prezzo_centesimi`, stessi domini, stesse unità in centesimi — e la
validazione resta **una sola funzione pura** chiamata da costruzione,
aggiornamento e conversioni.

| Campo | Tipo | Regola |
|---|---|---|
| `codice` | `str` | non vuoto, senza spazi agli estremi, confronto esatto |
| `descrizione` | `str` | almeno un carattere non bianco |
| `quantita` | `int` | intero non booleano >= 0 |
| `prezzo_centesimi` | `int` | intero non booleano >= 0, in centesimi |

Che cosa cambia rispetto a U13:

- i campi si osservano con **proprietà** di sola lettura: il codice resta
  stabile e gli altri campi non diventano assegnabili singolarmente
  soltanto per esibire un setter; l'aggiornamento passa da `aggiorna`,
  che valida il candidato completo prima delle scritture;
- `valore_centesimi` resta un valore **derivato**, ora come proprietà;
- la proiezione `dati()` restituisce uno snapshot frozen `DatiArticolo`,
  non un dizionario mutabile: utile per confronti, copie e conversioni.

`DatiArticolo` **non sostituisce** l'articolo mutabile: è il valore-fotografia
dei quattro campi. Un nuovo snapshot con gli stessi dati è uguale al
precedente ma non è l'istanza originale, e due articoli con gli stessi dati
restano istanze distinte.

Ambiente: CPython sul computer. Dipende soltanto dal linguaggio.
"""

from dataclasses import dataclass

CAMPI_ARTICOLO = ("codice", "descrizione", "quantita", "prezzo_centesimi")


def valida_dati_articolo(codice, descrizione, quantita, prezzo_centesimi):
    """Controlla i quattro campi dell'articolo. Restituisce `None` se validi.

    È l'unica sede delle regole dello schema, identica alla U13: la chiamano
    la costruzione, l'aggiornamento, lo snapshot e le conversioni.
    """
    if not isinstance(codice, str):
        raise ValueError(f"campo 'codice': atteso testo, ricevuto {type(codice).__name__}")
    if codice == "":
        raise ValueError("campo 'codice': non può essere vuoto")
    if codice != codice.strip():
        raise ValueError(
            f"campo 'codice': spazi iniziali o finali non ammessi, ricevuto {codice!r}"
        )
    if not isinstance(descrizione, str):
        raise ValueError(
            f"campo 'descrizione': atteso testo, ricevuto {type(descrizione).__name__}"
        )
    if descrizione.strip() == "":
        raise ValueError("campo 'descrizione': serve almeno un carattere non bianco")
    for valore, nome in ((quantita, "quantita"), (prezzo_centesimi, "prezzo_centesimi")):
        if isinstance(valore, bool) or not isinstance(valore, int):
            raise ValueError(f"campo '{nome}': atteso un intero, ricevuto {type(valore).__name__}")
        if valore < 0:
            raise ValueError(
                f"campo '{nome}': atteso un valore maggiore o uguale a zero, ricevuto {valore}"
            )
    return None


@dataclass(frozen=True)
class DatiArticolo:
    """Snapshot frozen dei quattro campi primitivi dell'articolo.

    Valore di passaggio fra il magazzino, le conversioni CSV/JSON e i test:
    con campi immutabili resta coerente per tutta la sua durata. Due
    snapshot con gli stessi dati sono uguali (`==`) pur essendo istanze
    distinte (`is`).
    """

    codice: str
    descrizione: str
    quantita: int
    prezzo_centesimi: int

    def __post_init__(self):
        valida_dati_articolo(
            self.codice,
            self.descrizione,
            self.quantita,
            self.prezzo_centesimi,
        )


class Articolo:
    """Articolo del magazzino osservato con proprietà di sola lettura.

    Invariante dell'istanza: i quattro campi rispettano sempre lo schema.
    Il `codice` è stabile; l'aggiornamento degli altri tre campi avviene
    **solo** attraverso `aggiorna`, che valida il candidato completo prima
    di ogni scrittura: un rifiuto lascia l'articolo esattamente com'era.
    """

    def __init__(self, codice, descrizione, quantita, prezzo_centesimi):
        """Crea l'articolo dopo la validazione della quadrupla completa."""
        valida_dati_articolo(codice, descrizione, quantita, prezzo_centesimi)
        self._codice = codice
        self._descrizione = descrizione
        self._quantita = quantita
        self._prezzo_centesimi = prezzo_centesimi

    @property
    def codice(self):
        """Codice stabile dell'articolo. Sola lettura."""
        return self._codice

    @property
    def descrizione(self):
        """Descrizione corrente. Sola lettura: si cambia con `aggiorna`."""
        return self._descrizione

    @property
    def quantita(self):
        """Quantità corrente. Sola lettura: si cambia con `aggiorna`."""
        return self._quantita

    @property
    def prezzo_centesimi(self):
        """Prezzo corrente in centesimi. Sola lettura."""
        return self._prezzo_centesimi

    @property
    def valore_centesimi(self):
        """Valore di magazzino `quantita * prezzo_centesimi`. Derivato."""
        return self._quantita * self._prezzo_centesimi

    def ha_codice(self, codice):
        """`True` se `codice` coincide con quello dell'articolo. Confronto esatto."""
        return self._codice == codice

    def dati(self):
        """Restituisce uno **snapshot frozen** `DatiArticolo` dei quattro campi.

        Proiezione esplicita del modello, non la copia generica degli
        attributi: modificare il risultato non modifica l'articolo.
        """
        return DatiArticolo(
            self._codice,
            self._descrizione,
            self._quantita,
            self._prezzo_centesimi,
        )

    def aggiorna(self, descrizione, quantita, prezzo_centesimi):
        """Aggiorna i tre campi modificabili. `None` sul successo.

        Il candidato completo viene validato **prima** di ogni assegnamento:
        un campo non valido solleva `ValueError` e lascia tutti i campi
        esattamente come prima. Il codice è stabile e non compare fra gli
        argomenti.
        """
        valida_dati_articolo(self._codice, descrizione, quantita, prezzo_centesimi)
        self._descrizione = descrizione
        self._quantita = quantita
        self._prezzo_centesimi = prezzo_centesimi
        return None


if __name__ == "__main__":
    articolo = Articolo("007", "Vite, lunga", 4, 25)
    print("osservazione:", (articolo.codice, articolo.descrizione, articolo.quantita))
    print("prezzo:", articolo.prezzo_centesimi, "centesimi")
    print("valore derivato:", articolo.valore_centesimi, "centesimi")

    try:
        articolo.codice = "008"
    except AttributeError as errore:
        print("scrittura sul codice rifiutata:", errore)

    articolo.aggiorna("Vite, lunga", 6, 25)
    print("dopo aggiorna:", articolo.dati())

    try:
        articolo.aggiorna("Vite, lunga", -1, 25)
    except ValueError as errore:
        print("aggiornamento rifiutato:", errore)
    print("stato conservato:", articolo.dati())

    snapshot = articolo.dati()
    uguale = DatiArticolo("007", "Vite, lunga", 6, 25)
    print("snapshot uguali:", snapshot == uguale, "| distinti:", snapshot is uguale)
    print("snapshot non è l'articolo:", snapshot == articolo)
