"""Dominio del magazzino: validazione dei record e operazioni sulla raccolta.

Questo modulo contiene la **logica del dato**: definisce lo schema dell'articolo,
lo valida, converte le righe di testo in record e compie le operazioni di
ricerca, inserimento, aggiornamento ed eliminazione su una lista di
record-dizionari. Nessuna lettura da file, nessuna stampa, nessuna domanda:
chi importa `dominio_magazzino_u12` ottiene funzioni che ricevono dati e
restituiscono risultati, oppure sollevano le eccezioni previste dal contratto.

Schema dell'articolo (campi nell'ordine del CSV):

| Campo | Tipo | Regola |
|---|---|---|
| `codice` | `str` | non vuoto, senza spazi iniziali o finali, univoco nella raccolta; il confronto è esatto e sensibile alle maiuscole, gli zeri iniziali restano (`007` e `7` sono codici diversi) |
| `descrizione` | `str` | almeno un carattere non bianco; virgole, virgolette e accenti sono contenuto ordinario |
| `quantita` | `int` | maggiore o uguale a zero; `bool` non è ammesso |
| `prezzo_centesimi` | `int` | maggiore o uguale a zero, in centesimi; `bool` non è ammesso, nessuna conversione implicita da float |

Politica d'errore: le funzioni segnalano la violazione del contratto con
`ValueError` motivato (campo, valore e riferimento quando disponibile) e non
modificano mai la raccolta ricevuta quando rifiutano un'operazione. I difetti
di programmazione del chiamante non vengono trasformati in "dato non valido":
se la raccolta non è una lista di record validi, le eccezioni di linguaggio
restano visibili.

Ambiente: CPython sul computer. Dipende soltanto dal linguaggio, non dagli
altri moduli del corso.
"""

# Ordine dei campi: è lo schema ufficiale, usato dal CSV e dai controlli.
CAMPI_ARTICOLO = ("codice", "descrizione", "quantita", "prezzo_centesimi")


def valida_articolo(articolo):
    """Controlla schema, tipi e domini di un singolo articolo.

    Restituisce `None` se il record è valido; solleva `ValueError` con un
    messaggio che nomina il campo quando il record non è valido. Non modifica
    il record ricevuto.
    """
    if not isinstance(articolo, dict):
        raise ValueError(f"articolo: atteso un record-dizionario, ricevuto {type(articolo).__name__}")
    for campo in CAMPI_ARTICOLO:
        if campo not in articolo:
            raise ValueError(f"campo '{campo}': mancante")
    for campo in articolo:
        if campo not in CAMPI_ARTICOLO:
            raise ValueError(f"campo '{campo}': non previsto dallo schema")

    codice = articolo["codice"]
    if not isinstance(codice, str):
        raise ValueError(f"campo 'codice': atteso testo, ricevuto {type(codice).__name__}")
    if codice == "":
        raise ValueError("campo 'codice': non può essere vuoto")
    if codice != codice.strip():
        raise ValueError(f"campo 'codice': spazi iniziali o finali non ammessi, ricevuto {codice!r}")

    descrizione = articolo["descrizione"]
    if not isinstance(descrizione, str):
        raise ValueError(f"campo 'descrizione': atteso testo, ricevuto {type(descrizione).__name__}")
    if descrizione.strip() == "":
        raise ValueError("campo 'descrizione': serve almeno un carattere non bianco")

    for campo in ("quantita", "prezzo_centesimi"):
        valore = articolo[campo]
        if isinstance(valore, bool) or not isinstance(valore, int):
            raise ValueError(f"campo '{campo}': atteso un intero, ricevuto {type(valore).__name__}")
        if valore < 0:
            raise ValueError(f"campo '{campo}': atteso un valore maggiore o uguale a zero, ricevuto {valore}")
    return None


def _intero_da_testo(testo, campo, riferimento):
    """Converte un campo testuale in intero, con diagnosi su campo e riferimento.

    Conversione e controllo del dominio restano controlli distinti: qui cade
    soltanto la conversione; il segno viene controllato da `valida_articolo`.
    """
    try:
        return int(testo)
    except ValueError:
        raise ValueError(f"{riferimento}, campo '{campo}': il testo {testo!r} non è un intero") from None


def riga_a_articolo(riga, riferimento_riga):
    """Converte una riga di quattro campi testuali in un articolo nuovo.

    `riga` è la sequenza dei campi nell'ordine dello schema, come restituita
    dal lettore CSV; `riferimento_riga` è il testo che identifica la riga nei
    messaggi d'errore (per esempio "record 1 (riga fisica 2)"). Restituisce un
    dizionario nuovo; un dato malformato solleva `ValueError` con campo e
    riferimento, senza risultati parziali.
    """
    if len(riga) != len(CAMPI_ARTICOLO):
        attesi = ", ".join(CAMPI_ARTICOLO)
        raise ValueError(
            f"{riferimento_riga}: attesi {len(CAMPI_ARTICOLO)} campi ({attesi}), ricevuti {len(riga)}"
        )
    articolo = {
        "codice": riga[0],
        "descrizione": riga[1],
        "quantita": _intero_da_testo(riga[2], "quantita", riferimento_riga),
        "prezzo_centesimi": _intero_da_testo(riga[3], "prezzo_centesimi", riferimento_riga),
    }
    try:
        valida_articolo(articolo)
    except ValueError as errore:
        raise ValueError(f"{riferimento_riga}: {errore}") from None
    return articolo


def articolo_a_riga(articolo):
    """Restituisce i campi testuali dell'articolo nell'ordine dello schema.

    Valida l'articolo prima della conversione e non lo modifica. I numeri
    diventano testo nella forma decimale ordinaria: la riga risultante è
    pronta per il record CSV.
    """
    valida_articolo(articolo)
    return [
        articolo["codice"],
        articolo["descrizione"],
        str(articolo["quantita"]),
        str(articolo["prezzo_centesimi"]),
    ]


def cerca_articolo(articoli, codice):
    """Restituisce l'indice dell'articolo con questo codice, oppure `None`.

    Il confronto è esatto. L'indice 0 è un risultato valido: non usare
    `if indice:` per controllare l'esito della ricerca. La raccolta non viene
    modificata.
    """
    for indice, articolo in enumerate(articoli):
        if articolo["codice"] == codice:
            return indice
    return None


def inserisci_articolo(articoli, articolo):
    """Aggiunge un articolo in fondo alla raccolta, come copia del record.

    Valida l'articolo e l'unicità del codice **prima** di aggiungere. Su
    successo restituisce `None`; su dato non valido o codice già presente
    solleva `ValueError` e la lista resta invariata.
    """
    valida_articolo(articolo)
    if cerca_articolo(articoli, articolo["codice"]) is not None:
        raise ValueError(f"campo 'codice': il codice {articolo['codice']!r} è già presente")
    articoli.append(dict(articolo))
    return None


def modifica_articolo(articoli, codice, descrizione, quantita, prezzo_centesimi):
    """Aggiorna descrizione, quantità e prezzo dell'articolo con questo codice.

    Il codice è identità dell'articolo e non viene modificato. Il record
    candidato viene costruito e validato **per intero** prima di sostituire
    quello trovato: un campo non valido lascia lo stato invariato e solleva
    `ValueError`. Restituisce `False` se il codice non esiste, `True` se
    l'aggiornamento è applicato.
    """
    indice = cerca_articolo(articoli, codice)
    if indice is None:
        return False
    candidato = {
        "codice": codice,
        "descrizione": descrizione,
        "quantita": quantita,
        "prezzo_centesimi": prezzo_centesimi,
    }
    valida_articolo(candidato)
    articoli[indice] = candidato
    return True


def elimina_articolo(articoli, codice):
    """Elimina l'articolo con questo codice. Nessuna domanda all'utente.

    Restituisce `False` se il codice non esiste, `True` se l'articolo è stato
    eliminato. La conferma all'utente è responsabilità di chi presenta
    l'interfaccia, non di questa funzione.
    """
    indice = cerca_articolo(articoli, codice)
    if indice is None:
        return False
    del articoli[indice]
    return True


def riepilogo_magazzino(articoli):
    """Restituisce un record nuovo con i totali della raccolta.

    Precondizione: gli articoli sono record validi. Il risultato contiene il
    numero di articoli, la quantità complessiva e il valore complessivo in
    centesimi; la lista vuota produce tre zeri. Nessuna lettura o scrittura.
    """
    quantita_totale = 0
    valore_centesimi = 0
    for articolo in articoli:
        quantita_totale += articolo["quantita"]
        valore_centesimi += articolo["quantita"] * articolo["prezzo_centesimi"]
    return {
        "articoli": len(articoli),
        "quantita_totale": quantita_totale,
        "valore_centesimi": valore_centesimi,
    }


def formatta_centesimi(centesimi):
    """Converte un importo in centesimi nella stringa monetaria in euro.

    La conversione resta visibile nel codice: `centesimi // 100` dà gli euro e
    `centesimi % 100` i centesimi residui, che vengono sempre scritti con due
    cifre. Così lo zero dà "0,00 €" e i resti inferiori a 10 centesimi non
    perdono la cifra iniziale ("5" dà "0,05 €"). L'argomento è un intero non
    negativo: questo controllo arriva con la validazione del cap. PY-18 e qui
    è precondizione dichiarata.
    """
    euro = centesimi // 100
    resto = centesimi % 100
    return f"{euro},{resto:02d} €"


if __name__ == "__main__":
    # Dimostrazione minima: gli stessi record canonici del capitolo PY-20.
    magazzino = [
        {"codice": "007", "descrizione": "Vite, lunga", "quantita": 4, "prezzo_centesimi": 25},
        {"codice": "012", "descrizione": 'Caffè "A"', "quantita": 2, "prezzo_centesimi": 350},
    ]
    print("indice di 007:", cerca_articolo(magazzino, "007"))
    print("indice di 999:", cerca_articolo(magazzino, "999"))
    riepilogo = riepilogo_magazzino(magazzino)
    print("riepilogo:", riepilogo)
    print("valore:", formatta_centesimi(riepilogo["valore_centesimi"]))
    try:
        inserisci_articolo(magazzino, {"codice": "007", "descrizione": "doppione", "quantita": 1, "prezzo_centesimi": 1})
    except ValueError as errore:
        print("rifiuto:", errore)
