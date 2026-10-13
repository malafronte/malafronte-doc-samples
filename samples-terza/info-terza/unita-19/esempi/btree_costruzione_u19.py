"""Costruzione di riferimento di un B-tree — Unità 19 (cap. PY-35).

Il modulo fornisce la funzione `costruisci_btree_riferimento`, basata
sull'inserimento dal basso del contenitore didattico: costruisce un nuovo
indice del B-tree dalle coppie date e rifiuta le chiavi duplicate prima di
esporre il risultato. La reimplementazione autonoma della costruzione
appartiene all'approfondimento; nel percorso comune la funzione è codice di
riferimento fornito, spiegato nel suo scopo, contratto e rapporto con le
divisioni già studiate.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from btree_modello_u19 import BTreeDidattico


def costruisci_btree_riferimento(voci, grado_minimo=2, tipo_chiave=int):
    """Costruisce un nuovo B-tree con le coppie `(chiave, dato)` date.

    La funzione inserisce le coppie nell'ordine ricevuto in un B-tree vuoto
    con il grado minimo e il dominio indicati. Quando le voci contengono una
    chiave duplicata, la funzione solleva `ValueError` prima di esporre il
    risultato e non consegna strutture parziali; la sequenza sorgente resta
    invariata. L'indice restituito supera `controlla_invarianti`.
    """
    visti = set()
    for chiave, _dato in voci:
        if chiave in visti:
            raise ValueError(f"chiave {chiave!r} duplicata nelle voci")
        visti.add(chiave)
    albero = BTreeDidattico(grado_minimo=grado_minimo, tipo_chiave=tipo_chiave)
    for chiave, dato in voci:
        albero.inserisci(chiave, dato)
    albero.controlla_invarianti()
    return albero


def traccia_inserimenti(chiavi, grado_minimo=2):
    """Restituisce la fotografia del B-tree dopo ogni inserimento dato.

    Per ogni chiave la funzione registra le chiavi della radice del B-tree,
    le chiavi dei figli della radice e l'altezza del B-tree. La traccia
    documenta la sequenza D2 del capitolo senza esporre stati temporanei come
    stati stabili validi.
    """
    albero = BTreeDidattico(grado_minimo=grado_minimo, tipo_chiave=int)
    traccia = []
    for chiave in chiavi:
        albero.inserisci(chiave, f"dato-{chiave}")
        albero.controlla_invarianti()
        traccia.append(
            {
                "dopo": chiave,
                "radice": albero.radice.chiavi(),
                "figli": [figlio.chiavi() for figlio in albero.radice.figli],
                "altezza": albero.altezza(),
                "dimensione": len(albero),
            }
        )
    return traccia
