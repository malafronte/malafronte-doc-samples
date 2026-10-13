"""Punto di avvio dell'indice hash di consultazione (U18).

Responsabilità del modulo: comporre il programma — caricare l'archivio,
costruire la raccolta, **costruire l'indice dopo il caricamento** e rispondere
a più interrogazioni sulla stessa fotografia. La struttura dell'indice vive in
`indice_hash_u18.py`: qui non c'è logica di ricerca, soltanto la lettura degli
argomenti e la presentazione dei risultati.

Uso, dalla root del progetto:

    uv run python programmi/indice_cli_u18.py fotografia
    uv run python programmi/indice_cli_u18.py cerca 007
    uv run python programmi/indice_cli_u18.py statistiche
    uv run python programmi/indice_cli_u18.py fotografia cerca 007 cerca 999

Ogni interrogazione è descritta dai propri argomenti — `fotografia` e
`statistiche` non ne hanno, `cerca` ne prende uno — e viene eseguita
nell'ordine della riga di comando sulla stessa fotografia dell'indice. Le
query d'intervallo appartengono all'indice BST della tappa U17: qui un
intervallo proposto viene rifiutato con la guida, che indirizza allo strumento
della tappa precedente. Chiavi non ammesse e comandi sconosciuti vengono
rifiutati **prima di ogni effetto**: il programma presenta la guida e termina
senza costruire l'indice. La validazione delle chiavi è quella dell'indice,
`valida_chiave`.
"""

import sys
from pathlib import Path

from indice_hash_u18 import costruisci_indice, valida_chiave
from registro_modello_u14 import RegistroPreventivi
from registro_persistenza import carica_archivio

PERCORSO_PREDEFINITO = Path("dati") / "unita-12" / "archivio.json"
ARGOMENTI_PER_INTERROGAZIONE = {"fotografia": 0, "statistiche": 0, "cerca": 1}
GUIDA = (
    "Uso: indice_cli_u18.py "
    "[fotografia | statistiche | cerca <codice>] ... "
    "(intervalli: indice_cli_u17.py)"
)


def interpreta_interrogazioni(argomenti):
    """Restituisce la lista delle coppie `(comando, valori)`; None se non ammesse.

    La lettura è sequenziale: ogni comando consuma il numero dichiarato di
    argomenti successivi e la lista risultante conserva l'ordine della riga
    di comando. Le chiavi vengono convalidate con `valida_chiave`.
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


def esegui_interrogazione(indice, comando, valori):
    """Esegue un'interrogazione sull'indice e restituisce la riga di esito."""
    if comando == "fotografia":
        voci = ", ".join(
            formatta_record(record) for _codice, record in indice.fotografia_ordinata()
        )
        return f"fotografia -> [{voci}]"
    if comando == "cerca":
        try:
            record = indice.cerca(valori[0])
        except KeyError:
            return f"cerca {valori[0]} -> assente"
        return f"cerca {valori[0]} -> {formatta_record(record)}"
    if len(indice) == 0:
        return "statistiche -> nessun codice"
    return (
        f"statistiche -> codici {len(indice)}, bucket {indice.capacita}, "
        f"carico {indice.fattore_carico:.2f}"
    )


def main() -> None:
    """Carica l'archivio, costruisce l'indice e risponde nell'ordine ricevuto."""
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

    # La costruzione avviene dopo il caricamento: l'indice è la fotografia
    # dei preventivi e risponde a ogni interrogazione senza essere ricostruito.
    indice = costruisci_indice(registro.preventivi())
    print(
        f"fotografia caricata: {registro.numero} preventivi, "
        f"indice costruito: {len(indice)} codici, carico {indice.fattore_carico:.2f}"
    )
    for comando, valori in interrogazioni:
        print(esegui_interrogazione(indice, comando, valori))
    print(f"interrogazioni eseguite: {len(interrogazioni)}")


if __name__ == "__main__":
    main()
