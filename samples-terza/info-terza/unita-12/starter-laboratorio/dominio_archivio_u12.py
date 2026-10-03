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

Stato del file: **incompleto, e lo dichiara**. I corpi con
`NotImplementedError` nominano la fase del laboratorio in cui si completano;
`riepilogo_archivio` è fornita completa come esempio di funzione pura di
servizio. La dimostrazione di esecuzione si trova nel riferimento formativo,
da leggere dopo le fasi indicate.

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
    raise NotImplementedError("fase L2: validazione di schema, tipi e domini")


def riga_a_materiale(riga, riferimento_riga):
    """Converte i campi testuali di una riga CSV in un record nuovo.

    `riga` è la lista di stringhe prodotta da `csv.reader`; `riferimento_riga`
    è il testo che individua la riga nella diagnosi (per esempio
    `"record 2 (riga fisica 3)"`). Le conversioni e la validazione sono
    controlli separati: un campo non convertibile viene diagnosticato con il
    proprio nome. Nessun risultato parziale: o la riga intera è valida, oppure
    si solleva `ValueError`.
    """
    raise NotImplementedError("fase L3: conversione dei campi CSV in record")


def materiale_a_riga(materiale):
    """Valida il record e restituisce i campi testuali nell'ordine dello schema.

    Il record ricevuto non viene modificato: la conversione produce una lista
    nuova di stringhe, pronta per `csv.writer`.
    """
    raise NotImplementedError("fase L4: conversione del record in campi CSV")


def cerca_materiale(materiali, codice):
    """Restituisce l'**indice** del codice richiesto, oppure `None` se assente.

    L'indice 0 è un risultato valido come qualunque altro: il chiamante non
    deve scrivere `if indice:`. La lista non viene modificata.
    """
    raise NotImplementedError("fase L2: ricerca per indice con distinzione di None")


def inserisci_materiale(materiali, materiale):
    """Aggiunge alla fine una **copia** del record, se valido e non duplicato.

    Successo: restituisce `None` e la lista contiene un elemento in più.
    Errore: solleva `ValueError` e la lista resta **invariata**.
    """
    raise NotImplementedError("fase L2: inserimento validato con copia del record")


def modifica_materiale(materiali, codice, descrizione, quantita):
    """Aggiorna descrizione e quantità del record con il codice richiesto.

    Il codice è l'identità del record e non viene modificato. Il candidato
    viene costruito e validato **per intero** prima di sostituire il record
    trovato: un dato non valido non produce aggiornamenti parziali.

    Successo: restituisce `True`. Codice assente: restituisce `False` senza
    cambiare nulla. Dato non valido: solleva `ValueError` con la lista invariata.
    """
    raise NotImplementedError("fase L2: aggiornamento senza effetti parziali")


def elimina_materiale(materiali, codice):
    """Elimina il record con il codice richiesto, senza porre domande.

    La conferma all'utente spetta alla CLI. Codice assente: restituisce
    `False`. Record eliminato: restituisce `True`.
    """
    raise NotImplementedError("fase L2: eliminazione con esito True/False")


def riepilogo_archivio(materiali):
    """Restituisce un record nuovo con i totali della raccolta.

    Chiavi: `materiali` (numero di record), `quantita_totale` (somma delle
    quantità). Archivio vuoto: tutti i valori sono zero. Nessun I/O.

    Funzione **fornita completa**: si usa, non si riscrive.
    """
    quantita_totale = 0
    for materiale in materiali:
        quantita_totale += materiale["quantita"]
    return {
        "materiali": len(materiali),
        "quantita_totale": quantita_totale,
    }
