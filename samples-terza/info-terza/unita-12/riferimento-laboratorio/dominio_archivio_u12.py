"""Dominio dell'archivio materiali: validazione, conversione e operazioni CRUD.

Questo modulo contiene la **logica del dato** del LAB-PY-U12: definisce lo
schema del materiale di laboratorio, lo valida, converte le righe di testo in
record e compie le operazioni di ricerca, inserimento, aggiornamento ed
eliminazione su una lista di record-dizionari. Nessuna lettura da file,
nessuna stampa, nessuna domanda: chi importa `dominio_archivio_u12` ottiene
funzioni che ricevono dati e restituiscono risultati, oppure sollevano le
eccezioni previste dal contratto.

Schema del materiale (campi nell'ordine del CSV):

| Campo | Tipo | Regola |
|---|---|---|
| `codice` | `str` | non vuoto, senza spazi iniziali o finali, univoco nella raccolta; il confronto è esatto e sensibile alle maiuscole, gli zeri iniziali restano (`007` e `7` sono codici diversi) |
| `descrizione` | `str` | almeno un carattere non bianco; virgole, virgolette e accenti sono contenuto ordinario |
| `quantita` | `int` | maggiore o uguale a zero; `bool` non è ammesso |

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
CAMPI_MATERIALE = ("codice", "descrizione", "quantita")


def valida_materiale(materiale):
    """Controlla schema, tipi e domini di un singolo materiale.

    Restituisce `None` se il record è valido; solleva `ValueError` con un
    messaggio che nomina il campo quando il record non è valido. Non modifica
    il record ricevuto.
    """
    if not isinstance(materiale, dict):
        raise ValueError(
            f"materiale: atteso un record-dizionario, ricevuto {type(materiale).__name__}"
        )
    for campo in CAMPI_MATERIALE:
        if campo not in materiale:
            raise ValueError(f"campo '{campo}': mancante")
    for campo in materiale:
        if campo not in CAMPI_MATERIALE:
            raise ValueError(f"campo '{campo}': non previsto dallo schema")

    codice = materiale["codice"]
    if not isinstance(codice, str):
        raise ValueError(f"campo 'codice': atteso testo, ricevuto {type(codice).__name__}")
    if codice == "":
        raise ValueError("campo 'codice': non può essere vuoto")
    if codice != codice.strip():
        raise ValueError(
            f"campo 'codice': spazi iniziali o finali non ammessi, ricevuto {codice!r}"
        )

    descrizione = materiale["descrizione"]
    if not isinstance(descrizione, str):
        raise ValueError(
            f"campo 'descrizione': atteso testo, ricevuto {type(descrizione).__name__}"
        )
    if descrizione.strip() == "":
        raise ValueError("campo 'descrizione': deve contenere almeno un carattere non bianco")

    quantita = materiale["quantita"]
    if isinstance(quantita, bool):
        # bool è una sottoclasse di int: `True` non è una quantità di questo schema.
        raise ValueError(f"campo 'quantita': atteso un intero, ricevuto {type(quantita).__name__}")
    if not isinstance(quantita, int):
        raise ValueError(f"campo 'quantita': atteso un intero, ricevuto {type(quantita).__name__}")
    if quantita < 0:
        raise ValueError(f"campo 'quantita': negativa ({quantita})")
    return None


def riga_a_materiale(riga, riferimento_riga):
    """Converte i campi testuali di una riga CSV in un record nuovo.

    `riga` è la lista di stringhe prodotta da `csv.reader`; `riferimento_riga`
    è il testo che individua la riga nella diagnosi (per esempio
    `"record 2 (riga fisica 3)"`). Le conversioni e la validazione sono
    controlli separati: un campo non convertibile viene diagnosticato con il
    proprio nome. Nessun risultato parziale: o la riga intera è valida, oppure
    si solleva `ValueError`.
    """
    if not isinstance(riga, (list, tuple)):
        raise ValueError(f"{riferimento_riga}: attesa una lista di campi")
    if len(riga) != len(CAMPI_MATERIALE):
        attesi = len(CAMPI_MATERIALE)
        raise ValueError(
            f"{riferimento_riga}: attesi {attesi} campi ({', '.join(CAMPI_MATERIALE)}), "
            f"ricevuti {len(riga)}"
        )
    quantita_testo = riga[2]
    try:
        quantita = int(quantita_testo)
    except ValueError:
        raise ValueError(
            f"{riferimento_riga}, campo 'quantita': valore non convertibile in intero "
            f"({quantita_testo!r})"
        ) from None
    materiale = {
        "codice": riga[0],
        "descrizione": riga[1],
        "quantita": quantita,
    }
    try:
        valida_materiale(materiale)
    except ValueError as errore:
        raise ValueError(f"{riferimento_riga}, {errore}") from None
    return materiale


def materiale_a_riga(materiale):
    """Valida il record e restituisce i campi testuali nell'ordine dello schema.

    Il record ricevuto non viene modificato: la conversione produce una lista
    nuova di stringhe, pronta per `csv.writer`.
    """
    valida_materiale(materiale)
    return [
        materiale["codice"],
        materiale["descrizione"],
        str(materiale["quantita"]),
    ]


def cerca_materiale(materiali, codice):
    """Restituisce l'**indice** del codice richiesto, oppure `None` se assente.

    L'indice 0 è un risultato valido come qualunque altro: il chiamante non
    deve scrivere `if indice:`. La lista non viene modificata.
    """
    for indice, materiale in enumerate(materiali):
        if materiale["codice"] == codice:
            return indice
    return None


def inserisci_materiale(materiali, materiale):
    """Aggiunge alla fine una **copia** del record, se valido e non duplicato.

    Successo: restituisce `None` e la lista contiene un elemento in più.
    Errore: solleva `ValueError` e la lista resta **invariata**.
    """
    valida_materiale(materiale)
    if cerca_materiale(materiali, materiale["codice"]) is not None:
        raise ValueError(f"campo 'codice': il codice {materiale['codice']!r} è già presente")
    materiali.append(dict(materiale))
    return None


def modifica_materiale(materiali, codice, descrizione, quantita):
    """Aggiorna descrizione e quantità del record con il codice richiesto.

    Il codice è l'identità del record e non viene modificato. Il candidato
    viene costruito e validato **per intero** prima di sostituire il record
    trovato: un dato non valido non produce aggiornamenti parziali.

    Successo: restituisce `True`. Codice assente: restituisce `False` senza
    cambiare nulla. Dato non valido: solleva `ValueError` con la lista invariata.
    """
    indice = cerca_materiale(materiali, codice)
    if indice is None:
        return False
    candidato = {
        "codice": codice,
        "descrizione": descrizione,
        "quantita": quantita,
    }
    valida_materiale(candidato)
    materiali[indice] = candidato
    return True


def elimina_materiale(materiali, codice):
    """Elimina il record con il codice richiesto, senza porre domande.

    La conferma all'utente spetta alla CLI. Codice assente: restituisce
    `False`. Record eliminato: restituisce `True`.
    """
    indice = cerca_materiale(materiali, codice)
    if indice is None:
        return False
    del materiali[indice]
    return True


def riepilogo_archivio(materiali):
    """Restituisce un record nuovo con i totali della raccolta.

    Chiavi: `materiali` (numero di record), `quantita_totale` (somma delle
    quantità). Archivio vuoto: tutti i valori sono zero. Nessun I/O.
    """
    quantita_totale = 0
    for materiale in materiali:
        quantita_totale += materiale["quantita"]
    return {
        "materiali": len(materiali),
        "quantita_totale": quantita_totale,
    }


if __name__ == "__main__":
    # Dimostrazione sotto guardia: nessun effetto all'import del modulo.
    esempio = {"codice": "007", "descrizione": "Vite, lunga", "quantita": 4}
    print("validazione di un record valido:", valida_materiale(esempio))
    raccolta = []
    inserisci_materiale(raccolta, esempio)
    inserisci_materiale(raccolta, {"codice": "012", "descrizione": 'Caffè "A"', "quantita": 2})
    print("indice di 007:", cerca_materiale(raccolta, "007"))
    print("indice di 999:", cerca_materiale(raccolta, "999"))
    print("riepilogo:", riepilogo_archivio(raccolta))
    try:
        inserisci_materiale(raccolta, {"codice": "007", "descrizione": "duplicato", "quantita": 1})
    except ValueError as errore:
        print("duplicato rifiutato:", errore)
    print("record dopo il rifiuto:", len(raccolta))
