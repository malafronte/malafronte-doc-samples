"""Articolo del magazzino: la classe e la validazione condivisa (OOP-02, sez. J).

La classe `Articolo` sostituisce il record-dizionario del magazzino del
cap. PY-20. Lo **schema esterno non cambia**: i quattro campi restano
`codice`, `descrizione`, `quantita`, `prezzo_centesimi`, nell'ordine del CSV,
e le regole di validazione sono le stesse già verificate in U12.

Schema dell'articolo (campi nell'ordine del CSV):

| Campo | Tipo | Regola |
|---|---|---|
| `codice` | `str` | non vuoto, senza spazi agli estremi |
| `descrizione` | `str` | almeno un carattere non bianco |
| `quantita` | `int` | intero non booleano >= 0 |
| `prezzo_centesimi` | `int` | intero non booleano >= 0, in centesimi |

Precisazioni sullo schema. Il confronto sui codici è **esatto** e sensibile
alle maiuscole: gli zeri iniziali restano e `007` e `7` sono codici diversi.
Nella descrizione virgole, virgolette e accenti sono contenuto ordinario.
Nessuna conversione implicita da float sui campi numerici.

Le regole vivono in **una sola funzione pura**, `valida_dati_articolo`,
riutilizzata dalla costruzione, dall'aggiornamento e dalle conversioni: non
esistono copie divergenti dello stesso schema.

Politica d'errore: i dati fuori contratto sollevano `ValueError` motivato che
nomina il campo. Un'operazione che rifiuta **non modifica** lo stato
dell'istanza. L'unicità del codice è un vincolo della **raccolta**, non del
singolo articolo: due istanze possono avere lo stesso codice quando non
appartengono alla stessa raccolta.

La convenzione `_nome` segnala implementazione interna; non impedisce
tecnicamente un accesso esterno né promette privacy o immutabilità.

Ambiente: CPython sul computer. Dipende soltanto dal linguaggio.
"""

# Ordine dei campi: è lo schema ufficiale, usato dal CSV e dai controlli.
CAMPI_ARTICOLO = ("codice", "descrizione", "quantita", "prezzo_centesimi")


def valida_dati_articolo(codice, descrizione, quantita, prezzo_centesimi):
    """Controlla i quattro campi dell'articolo. Restituisce `None` se validi.

    È l'**unica** sede delle regole dello schema: la chiamano la costruzione,
    l'aggiornamento e le conversioni. Controlla prima la forma di ogni campo,
    poi il suo dominio, nominando sempre il campo responsabile del rifiuto.
    Non modifica nulla e non costruisce istanze.
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
            raise ValueError(
                f"campo '{nome}': atteso un intero, ricevuto {type(valore).__name__}"
            )
        if valore < 0:
            raise ValueError(
                f"campo '{nome}': atteso un valore maggiore o uguale a zero, "
                f"ricevuto {valore}"
            )
    return None


class Articolo:
    """Un articolo del magazzino con stato proprio e codice stabile.

    Invariante dell'istanza: i quattro campi rispettano sempre lo schema
    dichiarato. Il `codice` è **identità dell'articolo** nel dominio del
    magazzino e non viene modificato da nessuna operazione di questo nucleo.
    """

    def __init__(self, codice, descrizione, quantita, prezzo_centesimi):
        """Crea l'articolo se tutti i quattro campi superano la validazione.

        La validazione avviene **prima** di ogni assegnamento: un campo non
        valido solleva `ValueError` e nessuna istanza viene restituita.
        """
        valida_dati_articolo(codice, descrizione, quantita, prezzo_centesimi)
        self._codice = codice
        self._descrizione = descrizione
        self._quantita = quantita
        self._prezzo_centesimi = prezzo_centesimi

    def dati(self):
        """Restituisce un **nuovo** record-dizionario con i quattro campi.

        È la proiezione esplicita del modello, non la copia generica degli
        attributi interni: i nomi dei campi sono quelli dello schema esterno e
        l'ordine è quello del CSV. Modificare il risultato non modifica
        l'articolo.
        """
        return {
            "codice": self._codice,
            "descrizione": self._descrizione,
            "quantita": self._quantita,
            "prezzo_centesimi": self._prezzo_centesimi,
        }

    def ha_codice(self, codice):
        """Restituisce `True` se `codice` coincide con quello dell'articolo.

        Confronto **esatto**, sensibile alle maiuscole e agli zeri iniziali.
        Nessuna mutazione.
        """
        return self._codice == codice

    def valore_centesimi(self):
        """Restituisce `quantita * prezzo_centesimi` in centesimi.

        Calcolo di dominio, senza I/O e senza accesso diretto ai campi da
        parte del chiamante.
        """
        return self._quantita * self._prezzo_centesimi

    def aggiorna(self, descrizione, quantita, prezzo_centesimi):
        """Aggiorna i tre campi modificabili. Nessun risultato su successo.

        Il candidato completo viene validato **prima** di qualunque
        assegnamento: un campo non valido solleva `ValueError` e lascia tutti
        i campi, compreso il codice, esattamente come prima. Il codice è
        stabile e non compare fra gli argomenti.
        """
        valida_dati_articolo(self._codice, descrizione, quantita, prezzo_centesimi)
        self._descrizione = descrizione
        self._quantita = quantita
        self._prezzo_centesimi = prezzo_centesimi
        return None


if __name__ == "__main__":
    # Dimostrazione minima: i due articoli canonici del capitolo.
    articoli = [
        Articolo("007", "Vite, lunga", 4, 25),
        Articolo("012", 'Caffè "A"', 2, 350),
    ]
    for articolo in articoli:
        print(articolo.dati(), "->", articolo.valore_centesimi(), "centesimi")
    print("007 ha codice 007:", articoli[0].ha_codice("007"))
    print("007 ha codice 7:  ", articoli[0].ha_codice("7"))
    articoli[0].aggiorna("Vite, lunga", 6, 25)
    print("dopo l'aggiornamento:", articoli[0].dati())
    try:
        articoli[0].aggiorna("descrizione valida", -1, 25)
    except ValueError as errore:
        print("rifiuto:", errore)
    print("stato conservato:", articoli[0].dati())
