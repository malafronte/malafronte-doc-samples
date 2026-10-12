"""Funzione hash didattica, indici e distribuzione delle chiavi — Unità 18.

Il modulo riusa `hash_didattico` della tabella concatenata e aggiunge gli
strumenti di calcolo del capitolo: trasformazione dell'hash in indice per una
capacità data, traccia dell'accumulatore testuale, costruzione di famiglie di
chiavi con lo stesso indice e riepilogo della distribuzione delle lunghezze
dei bucket.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from __future__ import annotations

from tabella_hash_u18 import hash_didattico


def _valida_capacita(capacita):
    """Convalida la capacità contro il dominio delle posizioni."""
    if isinstance(capacita, bool) or not isinstance(capacita, int):
        raise TypeError(f"capacità attesa di tipo int, ricevuto {type(capacita).__name__}")
    if capacita < 1:
        raise ValueError(f"capacità minima 1, ricevuto {capacita}")


def indice_per(chiave, capacita):
    """Restituisce il bucket selezionato da `chiave` in una tabella di `capacita`.

    La chiave segue il dominio della tabella concatenata; la capacità è un
    intero positivo. Con divisore positivo il resto Python è un indice fra `0`
    e `capacita - 1` anche per interi negativi.
    """
    _valida_capacita(capacita)
    return hash_didattico(chiave) % capacita


def traccia_accumulatore(testo):
    """Restituisce i passi dell'hash testuale come lista di tuple.

    Ogni passo riporta il carattere esaminato, il suo codice `ord` e il valore
    dell'accumulatore dopo l'aggiornamento. La lista vuota descrive la stringa
    vuota, il cui hash è 0.
    """
    if type(testo) is not str:
        raise TypeError(f"testo atteso di tipo str, ricevuto {type(testo).__name__}")
    accumulatore = 0
    passi = []
    for carattere in testo:
        accumulatore = (31 * accumulatore + ord(carattere)) % 65521
        passi.append((carattere, ord(carattere), accumulatore))
    return passi


def famiglia_stesso_indice(capacita, resto, quantita):
    """Restituisce `quantita` chiavi intere distinte con indice `resto`.

    Ogni chiave ha la forma `resto + j * capacita`, con `j = 0, 1, ...`: tutte
    selezionano lo stesso bucket perché aggiungono multipli della capacità.
    Il resto è compreso fra `0` e `capacita - 1`; la quantità è non negativa e
    sul vuoto il risultato è la lista vuota.
    """
    _valida_capacita(capacita)
    if isinstance(resto, bool) or not isinstance(resto, int):
        raise TypeError(f"resto atteso di tipo int, ricevuto {type(resto).__name__}")
    if not 0 <= resto < capacita:
        raise ValueError(f"resto {resto} fuori dall'intervallo per capacità {capacita}")
    if isinstance(quantita, bool) or not isinstance(quantita, int):
        raise TypeError(f"quantità attesa di tipo int, ricevuto {type(quantita).__name__}")
    if quantita < 0:
        raise ValueError(f"quantità minima 0, ricevuto {quantita}")
    return [resto + j * capacita for j in range(quantita)]


def riepilogo_distribuzione(lunghezze):
    """Riepiloga la distribuzione delle lunghezze dei bucket in un dizionario.

    Il risultato riporta il numero di associazioni `n`, il numero di bucket
    `m`, il carico `n / m`, i bucket vuoti, la lunghezza massima e gli indici
    dei bucket che raggiungono il massimo. Con `n = 0` tutte le grandezze
    restano definite: il massimo delle lunghezze è 0 e ogni bucket lo
    raggiunge. La media da sola non descrive la concentrazione: il massimo e
    i vuoti la rendono osservabile.
    """
    if not isinstance(lunghezze, list):
        raise TypeError("lunghezze attese come lista di interi")
    for lunghezza in lunghezze:
        if isinstance(lunghezza, bool) or not isinstance(lunghezza, int):
            raise TypeError("lunghezze attese come lista di interi")
        if lunghezza < 0:
            raise ValueError(f"lunghezza negativa non ammessa: {lunghezza}")
    numero_bucket = len(lunghezze)
    if numero_bucket == 0:
        raise ValueError("occorre almeno un bucket per il riepilogo")
    totale = sum(lunghezze)
    massimo = max(lunghezze)
    return {
        "n": totale,
        "m": numero_bucket,
        "carico": totale / numero_bucket,
        "bucket_vuoti": sum(1 for lunghezza in lunghezze if lunghezza == 0),
        "lunghezza_massima": massimo,
        "indici_massimo": [
            posizione for posizione, lunghezza in enumerate(lunghezze) if lunghezza == massimo
        ],
    }
