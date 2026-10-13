"""Persistenza del registro dei preventivi: JSON canonico e CSV (U12).

Formato canonico: documento JSON con la radice `{"versione_schema": 1,
"preventivi": [...]}`, UTF-8 **senza BOM**. Il CSV di consultazione con
intestazione `codice,destinazione,totale_cent` non sostituisce il documento
canonico: è una lettura per altri lettori.

Politica di caricamento **tutto valido oppure nessun archivio**: se un controllo
fallisce nessuna lista parziale viene pubblicata. Gli esiti sono distinti —
`assente`, `sintassi`, `struttura`, `dominio` — e la diagnosi di sintassi
riporta la posizione del parser.

Politica di salvataggio: scrittura su file temporaneo nella cartella di
destinazione e sostituzione finale; se la scrittura o la sostituzione falliscono
il file precedente resta identico nei byte, il temporaneo viene eliminato e
nessun esito di successo viene annunciato.

Nessun effetto all'import: il modulo non legge né scrive file.
"""
import csv
import json
import os
from pathlib import Path

from registro_dominio import VERSIONE_SCHEMA, valida_registro, valida_struttura_documento


def documento_del_registro(registro: list) -> dict:
    """Restituisce il documento JSON-ready con la radice dello schema.

    I record sono copiati in nuovi dizionari: il documento non condivide gli
    oggetti del registro in memoria.
    """
    preventivi = []
    for record in registro:
        preventivi.append(dict(record))
    return {"versione_schema": VERSIONE_SCHEMA, "preventivi": preventivi}


def carica_archivio(percorso):
    """Carica e valida l'archivio; restituisce (registro, esito, dettaglio).

    Esiti: `""` con il registro caricato, oppure `assente`, `sintassi`,
    `struttura`, `dominio` con registro `None`. Il dettaglio descrive la
    diagnosi — per la sintassi include riga e colonna del parser. Nessun
    risultato parziale: o l'intero documento è valido, o non c'è archivio.
    Un errore di lettura diverso dall'assenza del file non è classificato e
    viene propagato come errore del sistema operativo.
    """
    try:
        testo = Path(percorso).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, "assente", "file non trovato"

    try:
        dati = json.loads(testo)
    except json.JSONDecodeError as problema:
        dettaglio = f"riga {problema.lineno}, colonna {problema.colno}: {problema.msg}"
        return None, "sintassi", dettaglio

    errore = valida_struttura_documento(dati)
    if errore != "":
        return None, "struttura", errore

    registro = []
    for record in dati["preventivi"]:
        registro.append(dict(record))
    errore = valida_registro(registro)
    if errore != "":
        return None, "dominio", errore
    return registro, "", ""


def salva_archivio(percorso, registro: list) -> bool:
    """Salva il registro nel documento JSON; True solo dopo la sostituzione.

    Il file precedente resta identico nei byte se la scrittura o la
    sostituzione falliscono: in quel caso il temporaneo viene eliminato e il
    risultato è False, senza annunci di successo.
    """
    destinazione = Path(percorso)
    temporaneo = destinazione.with_name(destinazione.name + ".tmp")
    testo = json.dumps(documento_del_registro(registro), indent=2, ensure_ascii=False)
    try:
        _scrivi_temporaneo(temporaneo, testo + "\n")
        _sostituisci_file(temporaneo, destinazione)
    except OSError:
        _elimina_temporaneo(temporaneo)
        return False
    return True


def esporta_csv(percorso, registro: list) -> bool:
    """Esporta il CSV di consultazione; True se la scrittura riesce.

    Intestazione `codice,destinazione,totale_cent`, una riga per record
    nell'ordine del registro. Il file è UTF-8 senza BOM e non è il documento
    canonico.
    """
    try:
        with open(percorso, "w", encoding="utf-8", newline="") as file_csv:
            scrittore = csv.writer(file_csv)
            scrittore.writerow(["codice", "destinazione", "totale_cent"])
            for record in registro:
                scrittore.writerow(
                    [record["codice"], record["destinazione"], record["totale_cent"]]
                )
    except OSError:
        return False
    return True


# --- Punti di intervento per le prove di guasto, deterministiche ---


def _scrivi_temporaneo(percorso, testo: str) -> None:
    """Scrive il testo del temporaneo in UTF-8 senza BOM."""
    Path(percorso).write_text(testo, encoding="utf-8")


def _sostituisci_file(sorgente, destinazione) -> None:
    """Sostituisce il file di destinazione con il temporaneo."""
    os.replace(sorgente, destinazione)


def _elimina_temporaneo(percorso) -> None:
    """Elimina il temporaneo se esiste: la politica non lascia file sparsi."""
    try:
        Path(percorso).unlink()
    except FileNotFoundError:
        pass
