"""Starter del confronto fra strutture — laboratorio LAB-PY-U19 (fasi L5–L6).

Il modulo esegue gli stessi dati e le stesse query su lista non ordinata,
B-tree dello starter e `dict`, verifica i risultati equivalenti e salva il
CSV con preparazione e query separate. La funzione `dossier_scelta` è il
lavoro dello studente della fase L6: motiva la scelta per il carico
dichiarato con requisiti, ipotesi, evidenze, decisione, alternativa e limite.

Ambiente: CPython sul computer, esecuzione con `uv run python
laboratorio/confronto_starter.py` dalla cartella `unita-19`.
"""

from __future__ import annotations

import csv

from dati_catalogo import coppie_indice, query_laboratorio
from ricerca_btree_starter import BTreeDidattico


def costruisci_indici():
    """Costruisce lista, B-tree e `dict` dalle stesse coppie del catalogo."""
    coppie = coppie_indice()
    lista = list(coppie)
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=str)
    for chiave, dato in coppie:
        albero.inserisci(chiave, dato)
    tabella = dict(coppie)
    return {"lista": lista, "b-tree": albero, "dict": tabella}


def cerca_lista(coppie, chiave):
    """Cerca la chiave nella lista con scansione e conta i confronti."""
    confronti = 0
    for candidata, dato in coppie:
        confronti += 1
        if candidata == chiave:
            return dato, confronti
    raise KeyError(chiave)


def esegui_confronto():
    """Esegue le stesse query sui tre indici e verifica l'equivalenza.

    La costruzione degli indici resta fuori dalle misure; ogni riga registra
    struttura, query, esito e metrica con unità. La funzione restituisce il
    dizionario con `righe` e `coerente`.
    """
    indici = costruisci_indici()
    interrogazioni = query_laboratorio()
    domande = interrogazioni["riuscite"] + interrogazioni["fallite"]
    righe = []
    coerente = True
    for domanda in domande:
        presente_atteso = domanda in indici["dict"]
        atteso = indici["dict"].get(domanda)
        try:
            esito_lista, confronti = cerca_lista(indici["lista"], domanda)
            presente_lista = True
        except KeyError:
            presente_lista, esito_lista = False, None
            confronti = len(indici["lista"])
        try:
            esito_btree = indici["b-tree"].cerca(domanda)
            presente_btree = True
        except KeyError:
            presente_btree, esito_btree = False, None
        # La strumentazione raccoglie metriche dopo la consultazione da verificare.
        strumento = indici["b-tree"].ricerca_con_conteggi(domanda)
        confronti_btree = strumento["ordine"] + strumento["uguaglianza"]
        metrica_btree = f"nodi={strumento['nodi']} confronti={confronti_btree}"
        if strumento["trovato"] != presente_btree or (
            presente_btree and strumento["dato"] != esito_btree
        ):
            coerente = False
        for nome, presente, dato, metrica in (
            ("lista", presente_lista, esito_lista, f"confronti={confronti}"),
            ("b-tree", presente_btree, esito_btree, metrica_btree),
            ("dict", presente_atteso, atteso, "oracolo"),
        ):
            if presente != presente_atteso or (presente and dato != atteso):
                coerente = False
            righe.append(
                {
                    "struttura": nome,
                    "query": domanda,
                    "esito": f"trovato:{dato!r}" if presente else "assente",
                    "metrica": metrica,
                }
            )
    return {"righe": righe, "coerente": coerente}


def salva_csv(righe, percorso="risultati_confronto.csv"):
    """Salva le righe del confronto in CSV con colonne fissate."""
    with open(percorso, "w", newline="", encoding="utf-8") as archivio:
        scrittore = csv.DictWriter(archivio, fieldnames=["struttura", "query", "esito", "metrica"])
        scrittore.writeheader()
        scrittore.writerows(righe)


def dossier_scelta(carico):
    """TODO (L6): motiva la scelta della struttura per il `carico` dato.

    Il carico è il dizionario con `nome`, `operazioni`, `frequenza` e
    `organizzazione`. La funzione restituisce il dizionario con `requisiti`,
    `ipotesi`, `evidenze`, `decisione`, `alternativa` e `limite`.
    """
    raise NotImplementedError("dossier_scelta da completare nella fase L6")


if __name__ == "__main__":
    esito = esegui_confronto()
    salva_csv(esito["righe"])
    print(f"righe={len(esito['righe'])} coerente={esito['coerente']} csv=risultati_confronto.csv")
