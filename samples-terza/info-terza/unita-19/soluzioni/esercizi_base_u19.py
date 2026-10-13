"""Soluzioni di riferimento degli esercizi di base — Unità 19.

Il modulo raccoglie le funzioni usate nelle soluzioni guidate della raccolta
di base: verifica della sequenza D2, query strumentate, costruzione
dell'indice di record, visita ordinata e tabella di conteggi sullo stesso
carico. Ogni funzione è eseguibile con contesto e import dichiarati nelle
soluzioni della pagina.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from btree_costruzione_u19 import costruisci_btree_riferimento, traccia_inserimenti
from btree_modello_u19 import BTreeDidattico
from confronto_strutture_u19 import (
    AdattatoreBTree,
    AdattatoreDict,
    AdattatoreLista,
    esegui_confronto,
)
from dati_btree_u19 import RECORD_D6, costruisci_d1, costruisci_d2_finale
from indice_record_u19 import costruisci_indice_record, intervallo_chiuso


def verifica_sequenza_d2():
    """Verifica stati intermedi, forma finale e contatori della sequenza D2.

    La funzione restituisce il dizionario con la traccia degli inserimenti
    `1..10`, le chiavi della radice finale, l'altezza e i conteggi delle
    query `4`, `10`, `0`, `11` come coppie `(nodi, confronti)`.
    """
    traccia = traccia_inserimenti(range(1, 11))
    finale = costruisci_d2_finale()
    conteggi = {}
    for query in (4, 10, 0, 11):
        esito = finale.ricerca_con_conteggi(query)
        conteggi[query] = (esito.nodi, esito.confronti)
    return {
        "traccia": traccia,
        "radice": finale.radice.chiavi(),
        "altezza": finale.altezza(),
        "dimensione": len(finale),
        "conteggi": conteggi,
    }


def verifica_ricerche_d1():
    """Verifica esiti e percorsi delle cinque query canoniche su D1.

    La funzione restituisce il dizionario `{query: (trovato, nodi)}` per le
    query `20`, `17`, `15`, `4`, `40` sul B-tree D1.
    """
    albero = costruisci_d1()
    return {
        query: (albero.ricerca_con_conteggi(query).trovato, albero.ricerca_con_conteggi(query).nodi)
        for query in (20, 17, 15, 4, 40)
    }


def verifica_indice_record():
    """Verifica l'indice dei record D6: ordine, intervallo e casi limite.

    La funzione restituisce il dizionario con le chiavi ordinate
    dell'indice, i codici dell'intervallo `"007".."021"`, l'esito
    dell'intervallo vuoto e la distinzione fra `"007"` e `"7"`.
    """
    indice = costruisci_indice_record()
    chiavi = [chiave for chiave, _dato in indice.voci_ordinate()]
    intervallo = [chiave for chiave, _dato in intervallo_chiuso(indice, "007", "021")]
    vuoto = intervallo_chiuso(indice, "030", "031")
    return {
        "chiavi": chiavi,
        "intervallo": intervallo,
        "intervallo_vuoto": vuoto,
        "record_007": indice.cerca("007"),
        "codici_distinti": indice.cerca("007") != indice.cerca("7"),
    }


def verifica_confronto_carico():
    """Confronta le strutture sullo stesso carico di otto chiavi crescenti.

    La funzione esegue lista, B-tree e `dict` sulle query `1`, `5`, `8`, `0`
    e `9` e restituisce il dizionario con `coerente` e il numero di righe
    del confronto. La preparazione di ciascun indice resta separata dalle
    query misurate.
    """
    voci = [(chiave, f"dato-{chiave}") for chiave in range(1, 9)]
    esito = esegui_confronto(
        voci, [1, 5, 8, 0, 9], adattatori=(AdattatoreLista, AdattatoreBTree, AdattatoreDict)
    )
    return {"coerente": esito["coerente"], "righe": len(esito["righe"])}


def visita_ordinata_completa(voci, grado_minimo=2):
    """Costruisce il B-tree dalle voci e ne restituisce la visita ordinata.

    La funzione di riferimento della soluzione T03 alterna ogni figlio del
    nodo del B-tree alla voce successiva del nodo e comprende le voci dei
    nodi interni del B-tree, restituendo ogni coppia una sola volta in ordine
    crescente di chiave.
    """
    return costruisci_btree_riferimento(list(voci)).voci_ordinate()


def albero_minimo_esempio():
    """Restituisce un B-tree vuoto pronto per le prove di costruzione."""
    return BTreeDidattico(grado_minimo=2, tipo_chiave=int)


def record_d6():
    """Restituisce i record canonici D6 del catalogo dei materiali."""
    return RECORD_D6
