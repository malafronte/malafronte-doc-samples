"""Calcoli riusabili sul magazzino: valore, formattazione monetaria, codici.

Il modulo contiene **solo calcolo**: nessuna lettura, nessuna stampa, nessuna
domanda. Le funzioni ricevono dati, restituiscono risultati oppure sollevano
le eccezioni del proprio contratto.

Unità e domini dichiarati:

| Funzione | Ingresso | Risultato | Dominio |
|---|---|---|---|
| `valore_magazzino` | lista di record-dizionari | intero in **centesimi** | ogni record ha `quantita` e `prezzo_centesimi` interi non negativi |
| `formatta_centesimi` | intero non negativo | stringa `"euro,cc €"` | 0 o maggiore, `bool` escluso |
| `normalizza_codice` | stringa | stringa senza spazi iniziali e finali | almeno un carattere non bianco dopo la normalizzazione |

Politica d'errore, la stessa del cap. PY-18: un **argomento di tipo
sbagliato** è un uso sbagliato della funzione e produce `TypeError`; un **dato
fuori dominio** - il campo di un record, un intero negativo, un codice vuoto -
produce `ValueError` con una diagnosi che nomina posizione e campo. Il record
ricevuto da `valore_magazzino` è dato da validare: le sue violazioni restano
`ValueError`, come nel validatore del magazzino del cap. PY-20.

Ambiente: CPython sul computer. Il modulo non dipende da altri moduli del
corso: è questa autonomia a renderlo una piccola libreria.
"""


def _intero_non_negativo_dato(valore, nome):
    """Controlla un intero non negativo che è un **campo di un record**.

    Anche il tipo sbagliato è qui un dato non valido: il record viene dai dati
    del programma - un file, una lista costruita da un'altra funzione - e la
    diagnosi `ValueError` nomina il campo responsabile. `bool` non è ammesso:
    `True` è un intero per Python, ma non è una quantità di questo dominio.
    """
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(f"{nome}: atteso un intero, ricevuto {type(valore).__name__}")
    if valore < 0:
        raise ValueError(f"{nome}: atteso un intero non negativo, ricevuto {valore}")


def _intero_non_negativo_argomento(valore, nome):
    """Controlla un intero non negativo ricevuto come **argomento** diretto.

    Un argomento di tipo sbagliato è un difetto di programmazione del
    chiamante: produce `TypeError` e non viene trasformato in «dato non
    valido». Solo il valore negativo, che è un dato del dominio dichiarato,
    produce `ValueError`.
    """
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise TypeError(f"{nome}: atteso un intero, ricevuto {type(valore).__name__}")
    if valore < 0:
        raise ValueError(f"{nome}: atteso un intero non negativo, ricevuto {valore}")


def valore_magazzino(articoli):
    """Restituisce in centesimi il valore complessivo di una lista di articoli.

    Ogni articolo è un record-dizionario con i campi `quantita` e
    `prezzo_centesimi`, interi non negativi (`bool` escluso). Il calcolo è
    `quantita * prezzo_centesimi` sommato su tutti i record; la lista vuota vale
    0. La validazione è esplicita: un record non conforme produce `ValueError`
    con la posizione e il campo responsabili, e nessun risultato parziale viene
    restituito. L'argomento non è modificato; ricevere qualcosa che non è una
    lista è un uso sbagliato della funzione e produce `TypeError`.
    """
    if not isinstance(articoli, list):
        raise TypeError(f"articoli: attesa una lista di record, ricevuto {type(articoli).__name__}")
    totale_centesimi = 0
    for posizione, articolo in enumerate(articoli):
        if not isinstance(articolo, dict):
            raise ValueError(f"articolo {posizione}: atteso un record-dizionario, ricevuto {type(articolo).__name__}")
        for campo in ("quantita", "prezzo_centesimi"):
            if campo not in articolo:
                raise ValueError(f"articolo {posizione}: campo '{campo}' mancante")
            _intero_non_negativo_dato(articolo[campo], f"articolo {posizione}: campo '{campo}'")
        totale_centesimi += articolo["quantita"] * articolo["prezzo_centesimi"]
    return totale_centesimi


def formatta_centesimi(centesimi):
    """Converte un importo in centesimi nella stringa monetaria in euro.

    La conversione resta visibile nel codice: `centesimi // 100` dà gli euro e
    `centesimi % 100` i centesimi residui, scritti sempre con due cifre. Così
    lo zero dà `"0,00 €"` e i resti inferiori a 10 centesimi non perdono la
    cifra iniziale (`5` dà `"0,05 €"`). L'argomento è un intero non negativo:
    il tipo sbagliato produce `TypeError`, il valore negativo `ValueError`.
    """
    _intero_non_negativo_argomento(centesimi, "centesimi")
    euro = centesimi // 100
    resto = centesimi % 100
    return f"{euro},{resto:02d} €"


def normalizza_codice(testo):
    """Restituisce il codice senza spazi iniziali e finali.

    La normalizzazione **uniforma** ciò che è già lo stesso codice scritto con
    spazi accidentali: `normalizza_codice(" 007 ")` dà `"007"`. Non è la
    validazione dell'archivio: non controlla l'unicità, non accoda zeri, non
    cambia le maiuscole (`"00A"` resta `"00A"`) e non decide se il codice
    esiste. La validazione è un controllo separato, che rifiuta senza
    trasformare silenziosamente il dato ricevuto. Un argomento non testo
    produce `TypeError`; il testo vuoto dopo la normalizzazione `ValueError`.
    """
    if not isinstance(testo, str):
        raise TypeError(f"codice: atteso testo, ricevuto {type(testo).__name__}")
    normalizzato = testo.strip()
    if normalizzato == "":
        raise ValueError("codice: vuoto dopo la normalizzazione")
    return normalizzato
