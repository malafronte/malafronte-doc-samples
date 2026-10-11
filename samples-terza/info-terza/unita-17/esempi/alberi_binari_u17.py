"""Alberi binari rappresentati con oggetti collegati — Unità 17, cap. PY-32.

Il modulo contiene la classe `Nodo` e le funzioni didattiche usate dal
capitolo: costruzione di un albero a mano, altezza in archi, visite
preordine, inordine e postordine, visita in ampiezza per livelli,
valutazione di espressioni e misure su gerarchie sintetiche di file,
conteggio dei nodi e delle foglie.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione: ogni funzione è autonoma e dimostrabile a sé.
"""

from __future__ import annotations

from collections import deque


class Nodo:
    """Nodo di un albero binario con due posizioni distinte per i figli.

    `valore` è il dato conservato nel nodo. `sinistro` e `destro` sono i
    riferimenti ai sottoalberi: ciascuno indica un altro `Nodo` oppure
    `None`, che rappresenta una posizione priva di sottoalbero.
    """

    def __init__(self, valore, sinistro=None, destro=None):
        self.valore = valore
        self.sinistro = sinistro
        self.destro = destro


def altezza(nodo):
    """Restituisce l'altezza del sottoalbero radicato in `nodo`, in archi.

    Convenzione: il sottoalbero vuoto ha altezza -1, una foglia ha
    altezza 0. Il valore -1 permette di ottenere 0 per una foglia con la
    stessa formula `1 + max(...)`.
    """
    if nodo is None:
        return -1
    return 1 + max(altezza(nodo.sinistro), altezza(nodo.destro))


def conta_nodi(nodo):
    """Restituisce il numero di nodi del sottoalbero radicato in `nodo`."""
    if nodo is None:
        return 0
    return 1 + conta_nodi(nodo.sinistro) + conta_nodi(nodo.destro)


def conta_foglie(nodo):
    """Restituisce il numero di foglie del sottoalbero radicato in `nodo`.

    Una foglia ha entrambe le posizioni dei figli vuote: il caso base
    `nodo is None` conta 0 e non è una foglia.
    """
    if nodo is None:
        return 0
    if nodo.sinistro is None and nodo.destro is None:
        return 1
    return conta_foglie(nodo.sinistro) + conta_foglie(nodo.destro)


def preordine(nodo, risultato=None):
    """Restituisce i valori del sottoalbero in ordine preordine.

    L'elaborazione del nodo precede le due chiamate ricorsive.
    """
    if risultato is None:
        risultato = []
    if nodo is None:
        return risultato
    risultato.append(nodo.valore)
    preordine(nodo.sinistro, risultato)
    preordine(nodo.destro, risultato)
    return risultato


def inordine(nodo, risultato=None):
    """Restituisce i valori del sottoalbero in ordine inordine.

    L'elaborazione del nodo è fra la chiamata sul sottoalbero sinistro e
    quella sul sottoalbero destro.
    """
    if risultato is None:
        risultato = []
    if nodo is None:
        return risultato
    inordine(nodo.sinistro, risultato)
    risultato.append(nodo.valore)
    inordine(nodo.destro, risultato)
    return risultato


def postordine(nodo, risultato=None):
    """Restituisce i valori del sottoalbero in ordine postordine.

    L'elaborazione del nodo segue entrambe le chiamate ricorsive.
    """
    if risultato is None:
        risultato = []
    if nodo is None:
        return risultato
    postordine(nodo.sinistro, risultato)
    postordine(nodo.destro, risultato)
    risultato.append(nodo.valore)
    return risultato


def ampiezza(nodo):
    """Restituisce i valori del sottoalbero in ordine di livello.

    La visita procede per livelli, da sinistra a destra: una coda
    conserva i nodi in attesa e l'uscita dal fronte preserva l'ordine
    di arrivo. Sull'albero vuoto restituisce la lista vuota.
    """
    risultato = []
    if nodo is None:
        return risultato
    coda = deque([nodo])
    while coda:
        corrente = coda.popleft()
        risultato.append(corrente.valore)
        if corrente.sinistro is not None:
            coda.append(corrente.sinistro)
        if corrente.destro is not None:
            coda.append(corrente.destro)
    return risultato


def valuta(nodo):
    """Restituisce il valore dell'espressione rappresentata dall'albero.

    Una foglia conserva un operando intero; un nodo interno conserva un
    operatore fra '+', '-' e '*' con due sottoalberi. La valutazione
    segue l'ordine postordine: prima gli operandi, poi l'operazione.
    Un albero vuoto, un operando non intero e un operatore sconosciuto
    o con un solo figlio sollevano `ValueError`.
    """
    if nodo is None:
        raise ValueError("espressione vuota: nessun nodo da valutare")
    if nodo.sinistro is None and nodo.destro is None:
        if isinstance(nodo.valore, bool) or not isinstance(nodo.valore, int):
            raise ValueError(f"operando non intero: {nodo.valore!r}")
        return nodo.valore
    if nodo.sinistro is None or nodo.destro is None:
        raise ValueError(f"operatore con un solo figlio: {nodo.valore!r}")
    sinistro = valuta(nodo.sinistro)
    destro = valuta(nodo.destro)
    if nodo.valore == "+":
        return sinistro + destro
    if nodo.valore == "-":
        return sinistro - destro
    if nodo.valore == "*":
        return sinistro * destro
    raise ValueError(f"operatore sconosciuto: {nodo.valore!r}")


def infissa(nodo):
    """Restituisce l'espressione in notazione infissa con parentesi.

    Una foglia produce il proprio operando; un nodo interno racchiude
    fra parentesi la forma infissa dei figli con l'operatore nel mezzo.
    Le parentesi rendono visibile la struttura che la sola sequenza
    inordine non conserva. Un albero vuoto solleva `ValueError`.
    """
    if nodo is None:
        raise ValueError("espressione vuota: nessun nodo da rappresentare")
    if nodo.sinistro is None and nodo.destro is None:
        return str(nodo.valore)
    return f"({infissa(nodo.sinistro)} {nodo.valore} {infissa(nodo.destro)})"


def trova(nodo, nome):
    """Restituisce il percorso dei nomi fino a `nome`, oppure None.

    Il valore di ogni nodo è la coppia `(nome, byte)`, con `byte`
    pari a None per le directory. La ricerca segue l'ordine preordine
    e si arresta alla prima corrispondenza, senza visitare il resto.
    """
    if nodo is None:
        return None
    attuale, _byte = nodo.valore
    if attuale == nome:
        return [attuale]
    for figlio in (nodo.sinistro, nodo.destro):
        percorso = trova(figlio, nome)
        if percorso is not None:
            return [attuale, *percorso]
    return None


def dimensione_totale(nodo):
    """Restituisce i byte conservati nel sottoalbero radicato in `nodo`.

    Il valore di ogni nodo è la coppia `(nome, byte)`: un file
    contribuisce con i propri byte, una directory con la somma dei
    figli. Il calcolo segue l'ordine postordine: prima i contenuti,
    poi la somma che li raccoglie. Un sottoalbero vuoto contribuisce
    con 0 byte.
    """
    if nodo is None:
        return 0
    _nome, byte = nodo.valore
    if byte is not None:
        return byte
    totale = 0
    if nodo.sinistro is not None:
        totale += dimensione_totale(nodo.sinistro)
    if nodo.destro is not None:
        totale += dimensione_totale(nodo.destro)
    return totale


def costruisci_albero_d1():
    """Costruisce a mano l'albero binario di riferimento D1.

    D1 conserva i valori `[40, 20, 60, 10, 30, 50, 70, 25, 35, 55]`
    nella forma mostrata dal capitolo: la costruzione è esplicita e non
    usa alcuna regola di ordinamento, perché il capitolo PY-32 tratta
    alberi binari generici.
    """
    nodo_25 = Nodo(25)
    nodo_35 = Nodo(35)
    nodo_55 = Nodo(55)
    nodo_10 = Nodo(10)
    nodo_30 = Nodo(30, nodo_25, nodo_35)
    nodo_50 = Nodo(50, None, nodo_55)
    nodo_70 = Nodo(70)
    nodo_20 = Nodo(20, nodo_10, nodo_30)
    nodo_60 = Nodo(60, nodo_50, nodo_70)
    return Nodo(40, nodo_20, nodo_60)


def profondita_valore(nodo, valore, profondita=0):
    """Restituisce la profondità del primo nodo con `valore`, oppure None.

    La radice ha profondità 0; la profondità di un figlio supera di 1
    quella del padre. La ricerca attraversa tutto il sottoalbero perché
    un albero binario generico non offre scorciatoie.
    """
    if nodo is None:
        return None
    if nodo.valore == valore:
        return profondita
    trovato = profondita_valore(nodo.sinistro, valore, profondita + 1)
    if trovato is not None:
        return trovato
    return profondita_valore(nodo.destro, valore, profondita + 1)
