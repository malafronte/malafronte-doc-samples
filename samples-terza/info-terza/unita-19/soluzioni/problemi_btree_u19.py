"""Soluzioni di riferimento dei problemi algoritmici — Unità 19.

Il modulo raccoglie le funzioni usate nelle soluzioni guidate della famiglia
«B-tree, invarianti e scelta delle strutture»: sequenza che aumenta
l'altezza, verifica dell'ordine globale con limiti ereditati, query di
intervallo, scelta per un carico di consultazioni, verifica di indici
equivalenti, conteggio degli accessi a blocchi, traccia speculare di D5 e
capienza del nodo nel modello a blocchi.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

import math

from btree_costruzione_u19 import costruisci_btree_riferimento
from btree_modello_u19 import BTreeDidattico, NodoBTree
from confronto_strutture_u19 import (
    AdattatoreBTree,
    AdattatoreDict,
    AdattatoreLista,
    esegui_confronto,
)
from dati_btree_u19 import RECORD_D6, costruisci_d2_finale, costruisci_d5_iniziale
from indice_record_u19 import costruisci_indice_record, intervallo_chiuso


def sequenza_aumento_altezza():
    """Restituisce strategia, traccia e verifica dell'aumento di altezza.

    Con grado minimo 2 gli inserimenti crescenti `1..4` provocano la divisione
    della radice del B-tree e l'altezza passa da 0 a 1. La funzione
    restituisce il dizionario con la strategia, le altezze osservate e
    l'altezza finale.
    """
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    altezze = []
    for chiave in (1, 2, 3, 4):
        albero.inserisci(chiave, f"dato-{chiave}")
        altezze.append(albero.altezza())
    albero.controlla_invarianti()
    return {
        "strategia": "inserimenti crescenti 1..4 con t = 2 fino alla divisione della radice",
        "altezze": altezze,
        "altezza_finale": albero.altezza(),
    }


def verifica_limiti_ereditati(albero):
    """Controlla l'ordine globale del B-tree con i limiti degli antenati.

    La funzione esegue `controlla_invarianti` sul B-tree e restituisce `True`
    quando nessun discendente del B-tree supera i limiti ereditati
    dall'antenato, anche quando il discendente è ordinato rispetto al padre
    locale del nodo. Una violazione solleva `AssertionError`.
    """
    albero.controlla_invarianti()
    return True


def query_intervallo_record(primo, ultimo):
    """Restituisce le coppie ordinate dell'indice D6 nell'intervallo chiuso.

    La funzione sceglie visita ordinata completa e filtro, con costo `O(n)`
    dichiarato della versione comune; un intervallo con il limite inferiore
    maggiore del superiore solleva `ValueError`.
    """
    return intervallo_chiuso(costruisci_indice_record(), primo, ultimo)


def dossier_consultazioni():
    """Costruisce il dossier minimo per un carico di consultazioni esatte.

    La funzione verifica lista, B-tree e `dict` sulle stesse query del
    catalogo D6 e restituisce il dizionario con la scelta motivata, i
    risultati equivalenti e l'alternativa con il suo limite.
    """
    voci = [(f"{numero:03d}", f"dato-{numero:03d}") for numero in (3, 7, 12, 17, 21, 34, 42)]
    voci.append(("7", "dato-7"))
    esito = esegui_confronto(
        voci, ["007", "021", "999"], adattatori=(AdattatoreLista, AdattatoreBTree, AdattatoreDict)
    )
    return {
        "scelta": "dict per query esatte ripetute con modifiche occasionali",
        "alternativa": "B-tree quando servono anche viste ordinate e intervalli",
        "coerente": esito["coerente"],
        "righe": len(esito["righe"]),
    }


def verifica_indici_equivalenti():
    """Confronta ricerca lineare, B-tree e `dict` sugli stessi record D6.

    La funzione restituisce `True` quando ogni struttura restituisce gli
    stessi record completi, distingue `"007"` da `"7"` e tratta il dato `0`
    come valore legittimo; i duplicati sono rifiutati prima della consegna.
    """
    indice = costruisci_indice_record()
    voci_record = [
        (codice, (codice, descrizione, quantita)) for codice, descrizione, quantita in RECORD_D6
    ]
    lineare = AdattatoreLista(voci_record)
    nativo = AdattatoreDict(voci_record)
    for codice in ("003", "007", "012", "017", "021", "034", "042", "7"):
        assert lineare.cerca(codice) == indice.cerca(codice) == nativo.cerca(codice)
    try:
        indice.cerca("999")
    except KeyError:
        return True
    return False


def conta_accessi_blocchi(chiavi_query, radice_residente=False, conserva_cache=True):
    """Conta trasferimenti e visite per le query sul B-tree D2 concluso.

    La funzione costruisce il B-tree D2 con gli inserimenti `1..10`, poi
    conta per ciascuna query i nodi del B-tree visitati e, nel modello
    ideale un nodo-un blocco, i trasferimenti simulati. La cache conserva
    tutti i nodi acquisiti senza espulsioni; `conserva_cache=False` la riporta
    allo stato iniziale prima di ogni query. Con radice residente la radice
    è già nella cache iniziale e richiede zero trasferimenti.

    Il B-tree resta invariato: la tupla delle chiavi identifica ciascun nodo
    del percorso. Il risultato è una lista di dizionari con `query`, `nodi`
    e `trasferimenti`, così le query ripetute restano righe distinte.
    """
    albero = costruisci_d2_finale()
    iniziale = {tuple(albero.radice.chiavi())} if radice_residente else set()
    cache = set(iniziale)
    risultato = []
    for query in chiavi_query:
        if not conserva_cache:
            cache = set(iniziale)
        esito = albero.ricerca_con_conteggi(query)
        trasferimenti = 0
        for chiavi_nodo in esito.percorso:
            blocco = tuple(chiavi_nodo)
            if blocco not in cache:
                trasferimenti += 1
                cache.add(blocco)
        risultato.append({"query": query, "nodi": esito.nodi, "trasferimenti": trasferimenti})
    return risultato


def traccia_speculare_d5():
    """Costruisce la traccia speculare di D5 con prestito dal destro.

    La radice iniziale è `[40]`: il sinistro `[20]` ha foglie `[10]`, `[30]`,
    il destro `[50, 60]` ha foglie `[45]`, `[55]`, `[70]`. Eliminare `10`
    rende carente il sinistro dopo una fusione; il destro presta `50` al
    padre e trasferisce il figlio `[45]` al sinistro. Una copia con quel
    figlio omesso deve fallire il controllo degli invarianti.
    """

    def _iniziale():
        def _foglia(chiave):
            return NodoBTree([(chiave, f"dato-{chiave}")])

        albero = BTreeDidattico(grado_minimo=2)
        sinistro = NodoBTree([(20, "dato-20")], [_foglia(10), _foglia(30)])
        destro = NodoBTree(
            [(50, "dato-50"), (60, "dato-60")],
            [_foglia(45), _foglia(55), _foglia(70)],
        )
        albero.radice = NodoBTree([(40, "dato-40")], [sinistro, destro])
        albero.dimensione = 9
        albero.controlla_invarianti()
        return albero

    albero = _iniziale()
    attese = [voce for voce in albero.voci_ordinate() if voce[0] != 10]
    albero.rimuovi(10)
    albero.controlla_invarianti()
    sinistro, destro = albero.radice.figli
    foglia_trasferita = [nodo.chiavi() for nodo in sinistro.figli] == [[20, 30], [45]]

    corrotto = _iniziale()
    corrotto.rimuovi(10)
    corrotto.radice.figli[0].figli.pop()
    diagnosi = ""
    try:
        corrotto.controlla_invarianti()
    except AssertionError as errore:
        diagnosi = str(errore)

    coerente = (
        albero.radice.chiavi() == [50]
        and sinistro.chiavi() == [40]
        and destro.chiavi() == [60]
        and [nodo.chiavi() for nodo in destro.figli] == [[55], [70]]
        and foglia_trasferita
        and albero.voci_ordinate() == attese
        and len(albero) == 8
        and albero.altezza() == 2
        and "figli" in diagnosi
    )
    return {
        "albero": albero,
        "foglia_trasferita": foglia_trasferita,
        "coerente": coerente,
        "diagnosi": diagnosi,
        "traccia": [
            "eliminare 10; fusione [] + 20 + [30] nella foglia [20, 30]",
            "nodo sinistro carente: zero voci, un figlio [20, 30]",
            "40 dal padre al sinistro; 50 dal fratello destro al padre",
            "figlio [45] dal destro al sinistro; nuova radice [50]",
        ],
    }


def capienza_nodo_blocco(dimensione_blocco=4096, intestazione=16, voce=16, riferimento=8):
    """Ricava il grado minimo ammissibile nel modello a blocchi dichiarato.

    Un nodo interno al massimo del B-tree occupa `intestazione + voce(2t-1) +
    riferimento(2t)` byte; con le dimensioni sintetiche del capitolo
    (`4096`, `16`, `16`, `8`) il vincolo `48t <= 4096` ammette `t <= 85`. La
    funzione restituisce il dizionario con `t_massimo`, `occupazione` e il
    limite d'altezza per `n = 10000` associazioni del B-tree. Le dimensioni
    sono ipotesi di progetto, senza attribuzione alle tuple di CPython.
    """
    # Forma diretta del vincolo: intestazione + voce*(2t-1) + riferimento*2t <= blocco.
    t_massimo = (dimensione_blocco - intestazione + voce) // (2 * voce + 2 * riferimento)
    occupazione = intestazione + voce * (2 * t_massimo - 1) + riferimento * 2 * t_massimo
    limite_altezza = math.log((10000 + 1) / 2, t_massimo)
    return {"t_massimo": t_massimo, "occupazione": occupazione, "limite_altezza": limite_altezza}


def albero_d5():
    """Restituisce lo stato iniziale D5 per le prove di riparazione."""
    return costruisci_d5_iniziale()


def indice_d6():
    """Restituisce l'indice dei record D6 per le prove di equivalenza."""
    return costruisci_indice_record()


def btree_riferimento(voci, grado_minimo=2, tipo_chiave=int):
    """Costruisce il B-tree di riferimento dalle voci per le prove guidate."""
    return costruisci_btree_riferimento(
        list(voci), grado_minimo=grado_minimo, tipo_chiave=tipo_chiave
    )
