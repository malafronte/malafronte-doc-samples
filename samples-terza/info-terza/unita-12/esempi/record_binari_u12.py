"""Record binari a posizione calcolata: lettura e aggiornamento puntuale.

Formato dell'archivio: una sequenza di record di **due byte**, ciascuno un
intero senza segno a 16 bit in ordine little-endian (prima il byte meno
significativo). Non c'è intestazione né separatore: il record di indice `i`
inizia all'offset `i * 2` e occupa esattamente due byte. Il file canonico dei
tre valori `[10, 500, 65535]` ha quindi i byte `0A 00 F4 01 FF FF` e la
lunghezza di 6 byte.

Questo modulo contiene le sole operazioni sui record: riceve un percorso e
restituisce o aggiorna un valore, senza stampe né domande. La differenza
rispetto al CSV del cap. PY-20 sta nella posizione: qui ogni record si raggiunge
direttamente con un offset in byte, senza leggere quelli precedenti, e
l'aggiornamento di un record non tocca gli altri. Il modello regge perché i
record hanno dimensione fissa: un archivio a campi di lunghezza variabile, come
il CSV, non ha offset calcolabili in questo modo.

Politica d'errore: l'indice e il valore devono appartenere ai propri domini
**prima** di qualunque scrittura; un archivio di lunghezza dispari contiene un
record incompleto e viene rifiutato per intero, senza inventare uno zero per il
byte mancante. La distinzione del cap. PY-18 resta ferma: un argomento di tipo
sbagliato è un **difetto di programmazione** e produce `TypeError`; un valore
fuori dominio è un **dato non valido** e produce `ValueError` con diagnosi. I
file assenti e gli errori di accesso si propagano come `OSError` pertinenti.
L'aggiornamento è puntuale e **non transazionale**: una scrittura interrotta
può lasciare il record incompleto, ed è il motivo per cui l'archivio intero del
magazzino usa il protocollo del temporaneo invece di questa strategia.

Ambiente: CPython sul computer.
"""

from pathlib import Path

# Un record occupa due byte: 16 bit senza segno, da 0 a 65535.
BYTE_PER_RECORD = 2
VALORE_MASSIMO = 65535


def _valida_indice(indice, numero_record):
    """Controlla il tipo e il dominio dell'indice contro la dimensione reale.

    Un argomento che non è un intero è un uso sbagliato della funzione e
    produce `TypeError` (`bool` compreso: `True` è un intero per Python, ma non
    è un indice scritto come tale dal programma). L'indice negativo o oltre
    l'archivio è invece un dato fuori dominio e produce `ValueError` con una
    diagnosi che nomina il valore ricevuto.
    """
    if isinstance(indice, bool) or not isinstance(indice, int):
        raise TypeError(f"indice: atteso un intero, ricevuto {type(indice).__name__}")
    if indice < 0:
        raise ValueError(f"indice {indice}: negativo, gli indici partono da 0")
    if indice >= numero_record:
        raise ValueError(f"indice {indice}: fuori intervallo, l'archivio contiene {numero_record} record")


def _valida_valore(valore):
    """Controlla il tipo e il dominio di un valore da scrivere in un record.

    Il record è intero senza segno a due byte: il dominio è 0-65535. Un
    argomento non intero produce `TypeError`; il valore fuori dominio produce
    `ValueError` con diagnosi.
    """
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise TypeError(f"valore: atteso un intero, ricevuto {type(valore).__name__}")
    if valore < 0 or valore > VALORE_MASSIMO:
        raise ValueError(f"valore {valore}: fuori dominio, atteso un intero fra 0 e {VALORE_MASSIMO}")


def _dimensioni_archivio(archivio):
    """Restituisce `(numero_record, lunghezza)` dopo il controllo di struttura.

    L'archivio viene misurato con `seek` e `tell` sul file già aperto, senza
    leggere i contenuti. Una lunghezza non multipla di due segnala un record
    incompleto: l'intero archivio viene rifiutato, non soltanto l'ultimo
    record, perché la formula dell'offset non è più affidabile.
    """
    archivio.seek(0, 2)
    lunghezza = archivio.tell()
    if lunghezza % BYTE_PER_RECORD != 0:
        raise ValueError(
            f"archivio incompleto: {lunghezza} byte, attesi multipli di {BYTE_PER_RECORD}"
        )
    return lunghezza // BYTE_PER_RECORD, lunghezza


def leggi_record_due_byte(percorso, indice):
    """Restituisce il valore intero del record di indice `indice`.

    Il record è letto all'offset `indice * 2` e interpretato come intero senza
    segno a 16 bit little-endian. L'indice deve essere un intero non negativo
    minore del numero di record; il file deve esistere ed essere lungo un
    multiplo di due byte. Nessuno zero sintetico viene restituito: un argomento
    di tipo sbagliato produce `TypeError`, i casi fuori dominio producono
    `ValueError` e gli errori di sistema si propagano come `OSError`.
    """
    percorso = Path(percorso)
    with open(percorso, "rb") as archivio:
        numero_record, _ = _dimensioni_archivio(archivio)
        _valida_indice(indice, numero_record)
        archivio.seek(indice * BYTE_PER_RECORD)
        dati = archivio.read(BYTE_PER_RECORD)
    if len(dati) != BYTE_PER_RECORD:
        raise ValueError(f"record {indice}: incompleto, {len(dati)} byte disponibili su {BYTE_PER_RECORD}")
    return int.from_bytes(dati, "little")


def aggiorna_record_due_byte(percorso, indice, valore):
    """Scrive `valore` nel record di `indice` e restituisce `None`.

    I controlli precedono la scrittura: dominio del valore, struttura
    dell'archivio e intervallo dell'indice vengono verificati sulla dimensione
    reale del file, e un esito negativo non ha effetti - un argomento di tipo
    sbagliato produce `TypeError`, i casi fuori dominio `ValueError`. La
    scrittura apre il file in `r+b` - che **non tronca**, a differenza di `wb` -
    e sostituisce i due byte dell'offset `indice * 2`; gli altri record e la
    lunghezza restano invariati. La funzione non è transazionale: protegge
    dagli errori di dominio, non da un'interruzione durante i due byte di
    scrittura.
    """
    percorso = Path(percorso)
    _valida_valore(valore)
    with open(percorso, "r+b") as archivio:
        numero_record, _ = _dimensioni_archivio(archivio)
        _valida_indice(indice, numero_record)
        archivio.seek(indice * BYTE_PER_RECORD)
        archivio.write(valore.to_bytes(BYTE_PER_RECORD, "little"))
    return None


def traccia_seek(percorso):
    """Restituisce la traccia di posizioni e letture su un archivio binario.

    La traccia è una lista di triple `(operazione, posizione, byte_letti)`:
    `posizione` è il valore di `tell()` **dopo** l'operazione e `byte_letti`
    contiene i byte restituiti da `read`, oppure `None` per le operazioni che
    non leggono. Serve a osservare `seek` dalle tre origini - inizio, posizione
    corrente, fine - e il valore `b""` di fine file su un archivio binario.
    """
    percorso = Path(percorso)
    traccia = []
    with open(percorso, "rb") as archivio:
        traccia.append(("apertura", archivio.tell(), None))
        archivio.seek(4)
        traccia.append(("seek(4) da inizio", archivio.tell(), None))
        lettura = archivio.read(BYTE_PER_RECORD)
        traccia.append(("read(2)", archivio.tell(), lettura))
        archivio.seek(-4, 1)
        traccia.append(("seek(-4, 1) da posizione corrente", archivio.tell(), None))
        lettura = archivio.read(BYTE_PER_RECORD)
        traccia.append(("read(2)", archivio.tell(), lettura))
        archivio.seek(-2, 2)
        traccia.append(("seek(-2, 2) da fine", archivio.tell(), None))
        lettura = archivio.read(BYTE_PER_RECORD)
        traccia.append(("read(2)", archivio.tell(), lettura))
        lettura = archivio.read(BYTE_PER_RECORD)
        traccia.append(("read(2) a fine file", archivio.tell(), lettura))
    return traccia


if __name__ == "__main__":
    # Dimostrazione sull'archivio canonico, in una cartella temporanea:
    # la fixture di `dati/binari/` non viene toccata.
    import tempfile

    with tempfile.TemporaryDirectory() as cartella:
        prova = Path(cartella) / "record.bin"
        prova.write_bytes(bytes([0x0A, 0x00, 0xF4, 0x01, 0xFF, 0xFF]))
        print("byte iniziali:", prova.read_bytes().hex(" ").upper())
        print("record 0:", leggi_record_due_byte(prova, 0))
        print("record 1:", leggi_record_due_byte(prova, 1))
        print("record 2:", leggi_record_due_byte(prova, 2))
        aggiorna_record_due_byte(prova, 1, 42)
        print("dopo aggiornamento del record 1 a 42:", prova.read_bytes().hex(" ").upper())
        for operazione, posizione, byte_letti in traccia_seek(prova):
            print(f"{operazione:38} tell={posizione} letto={byte_letti!r}")
