"""Punto di avvio del confronto delle consultazioni del registro (U19).

Responsabilità del modulo: comporre il programma — caricare l'archivio,
costruire la raccolta, **costruire ogni indice dopo il caricamento** sulla
stessa fotografia e rispondere a più interrogazioni con risultati
verificati. Le strutture dell'indice vivono nei moduli delle tappe:
`indice_bst_u17.py`, `indice_hash_u18.py` e `indice_btree_u19.py`; qui non
c'è logica di ricerca, soltanto adattatori, verifica e presentazione.

Uso, dalla root del progetto:

    uv run python programmi/confronto_cli_u19.py fotografia
    uv run python programmi/confronto_cli_u19.py cerca 007
    uv run python programmi/confronto_cli_u19.py intervallo 003 012
    uv run python programmi/confronto_cli_u19.py confronta
    uv run python programmi/confronto_cli_u19.py fotografia cerca 007 confronta

Ogni interrogazione è descritta dai propri argomenti e viene eseguita
nell'ordine della riga di comando sulla stessa fotografia degli indici. Il
comando `confronta` esegue le query esatte e l'intervallo su scansione,
lista ordinata, BST, hash e B-tree, verifica l'equivalenza contro `dict` e
`sorted` con filtro e salva `risultati/unita-19/confronto.csv` con colonne,
modello e interrogazioni. Chiavi non ammesse e comandi sconosciuti vengono
rifiutati **prima di ogni effetto**: il programma presenta la guida e
termina senza costruire gli indici.
"""

import bisect
import csv
import sys
from pathlib import Path

from indice_bst_u17 import costruisci_indice as costruisci_bst
from indice_btree_u19 import costruisci_indice as costruisci_btree
from indice_btree_u19 import valida_chiave
from indice_hash_u18 import costruisci_indice as costruisci_hash
from registro_modello_u14 import RegistroPreventivi
from registro_persistenza import carica_archivio

PERCORSO_PREDEFINITO = Path("dati") / "unita-12" / "archivio.json"
PERCORSO_CSV = Path("risultati") / "unita-19" / "confronto.csv"
ARGOMENTI_PER_INTERROGAZIONE = {
    "fotografia": 0,
    "statistiche": 0,
    "cerca": 1,
    "intervallo": 2,
    "confronta": 0,
}
GUIDA = (
    "Uso: confronto_cli_u19.py "
    "[fotografia | statistiche | cerca <codice> | intervallo <min> <max> | confronta] ..."
)


def interpreta_interrogazioni(argomenti):
    """Restituisce la lista delle coppie `(comando, valori)`; None se non ammesse.

    Le chiavi vengono convalidate con `valida_chiave` dell'indice B-tree, che
    riusa la validazione del modello del registro.
    """
    interrogazioni = []
    posizione = 0
    while posizione < len(argomenti):
        comando = argomenti[posizione]
        if comando not in ARGOMENTI_PER_INTERROGAZIONE:
            return None
        quanti = ARGOMENTI_PER_INTERROGAZIONE[comando]
        valori = argomenti[posizione + 1 : posizione + 1 + quanti]
        if len(valori) < quanti:
            return None
        try:
            for valore in valori:
                valida_chiave(valore)
        except TypeError, ValueError:
            return None
        interrogazioni.append((comando, valori))
        posizione = posizione + 1 + quanti
    return interrogazioni if interrogazioni else None


def formatta_record(record):
    """Restituisce il record come testo `codice/destinazione/totale_cent`."""
    return f"{record.codice}/{record.destinazione}/{record.totale_cent}"


def costruisci_tutti(preventivi):
    """Costruisce i cinque indici sulla stessa fotografia dei preventivi.

    La costruzione di ciascun indice resta separata dalle interrogazioni:
    il rapporto registra la preparazione prima delle query.
    """
    coppie = [(record.codice, record) for record in preventivi]
    return {
        "scansione": list(coppie),
        "lista-ordinata": sorted(coppie, key=lambda voce: voce[0]),
        "bst": costruisci_bst(preventivi),
        "hash": costruisci_hash(preventivi),
        "b-tree": costruisci_btree(preventivi),
    }


def cerca_ovunque(indici, codice):
    """Cerca il codice in ogni indice e restituisce le righe di esito."""
    righe = []
    chiavi_ordinate = [codice for codice, _record in indici["lista-ordinata"]]
    posizione = bisect.bisect_left(chiavi_ordinate, codice)
    if posizione < len(chiavi_ordinate) and chiavi_ordinate[posizione] == codice:
        righe.append(
            ("lista-ordinata", formatta_record(indici["lista-ordinata"][posizione][1]))
        )
    else:
        righe.append(("lista-ordinata", "assente"))
    trovata = next(
        (record for chiave, record in indici["scansione"] if chiave == codice), None
    )
    righe.append(
        ("scansione", formatta_record(trovata) if trovata is not None else "assente")
    )
    for nome in ("bst", "hash", "b-tree"):
        try:
            righe.append((nome, formatta_record(indici[nome].cerca(codice))))
        except KeyError:
            righe.append((nome, "assente"))
    return righe


def intervallo_ovunque(indici, minimo, massimo):
    """Esegue l'intervallo su ogni indice e restituisce le righe di esito."""
    righe = []
    attesi = [
        codice
        for codice, _record in indici["lista-ordinata"]
        if minimo <= codice <= massimo
    ]
    righe.append(("lista-ordinata", ",".join(attesi) if attesi else "vuoto"))
    filtrati = [
        codice for codice, _r in indici["scansione"] if minimo <= codice <= massimo
    ]
    righe.append(("scansione", ",".join(sorted(filtrati)) if filtrati else "vuoto"))
    for nome in ("bst", "hash", "b-tree"):
        if nome == "hash":
            voci = [
                codice
                for codice, _r in indici[nome].fotografia_ordinata()
                if minimo <= codice <= massimo
            ]
        elif nome == "bst":
            voci = [
                record.codice for _c, record in indici[nome].intervallo(minimo, massimo)
            ]
        else:
            voci = [codice for codice, _r in indici[nome].intervallo(minimo, massimo)]
        righe.append((nome, ",".join(voci) if voci else "vuoto"))
    return righe


def esegui_confronta(indici):
    """Esegue il confronto verificato e salva il CSV con colonne fissate.

    Le query esatte sono `007`, `012` e `999`; l'intervallo è `003..012`.
    Gli esiti sono verificati contro `dict` e `sorted` con filtro prima di
    ogni misura; la funzione restituisce le righe e l'esito della verifica.
    """
    oracolo = dict(indici["lista-ordinata"])
    righe = []
    coerente = True
    for codice in ("007", "012", "999"):
        atteso = formatta_record(oracolo[codice]) if codice in oracolo else "assente"
        for nome, esito in cerca_ovunque(indici, codice):
            if esito != atteso:
                coerente = False
            righe.append(
                {
                    "struttura": nome,
                    "query": f"cerca {codice}",
                    "esito": esito,
                    "atteso": atteso,
                }
            )
    attesi = ",".join(codice for codice in sorted(oracolo) if "003" <= codice <= "012")
    for nome, esito in intervallo_ovunque(indici, "003", "012"):
        if esito != (attesi if attesi else "vuoto"):
            coerente = False
        righe.append(
            {
                "struttura": nome,
                "query": "intervallo 003 012",
                "esito": esito,
                "atteso": attesi if attesi else "vuoto",
            }
        )
    PERCORSO_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(PERCORSO_CSV, "w", newline="", encoding="utf-8") as archivio:
        scrittore = csv.DictWriter(
            archivio, fieldnames=["struttura", "query", "esito", "atteso"]
        )
        scrittore.writeheader()
        scrittore.writerows(righe)
    return righe, coerente


def esegui_interrogazione(indici, comando, valori):
    """Esegue un'interrogazione sugli indici e restituisce le righe di esito."""
    if comando == "fotografia":
        voci = ", ".join(
            formatta_record(record)
            for _codice, record in indici["b-tree"].fotografia_ordinata()
        )
        return [f"fotografia -> [{voci}]"]
    if comando == "statistiche":
        albero = indici["b-tree"]
        return [f"statistiche -> codici {len(albero)}, altezza {albero.altezza}"]
    if comando == "cerca":
        return [
            f"{nome} -> {esito}" for nome, esito in cerca_ovunque(indici, valori[0])
        ]
    if comando == "intervallo":
        return [
            f"{nome} -> {esito}" for nome, esito in intervallo_ovunque(indici, *valori)
        ]
    righe, coerente = esegui_confronta(indici)
    return [
        f"confronta -> {len(righe)} righe, equivalenti: {coerente}, csv: {PERCORSO_CSV}"
    ]


def main() -> None:
    """Carica l'archivio, costruisce gli indici e risponde nell'ordine ricevuto."""
    argomenti = sys.argv[1:]
    interrogazioni = interpreta_interrogazioni(argomenti)
    if interrogazioni is None:
        print(GUIDA)
        return

    caricato, esito, dettaglio = carica_archivio(PERCORSO_PREDEFINITO)
    if esito != "":
        print(f"Caricamento non riuscito ({esito}): {dettaglio}")
        return
    registro = RegistroPreventivi()
    registro.sostituisci_da_lista(caricato)

    # La costruzione avviene dopo il caricamento: ogni indice è la fotografia
    # dei preventivi e risponde a ogni interrogazione senza essere ricostruito.
    indici = costruisci_tutti(registro.preventivi())
    print(
        f"fotografia caricata: {registro.numero} preventivi, "
        f"indici costruiti: {len(indici)} strutture"
    )
    for comando, valori in interrogazioni:
        for riga in esegui_interrogazione(indici, comando, valori):
            print(riga)
    print(f"interrogazioni eseguite: {len(interrogazioni)}")


if __name__ == "__main__":
    main()
