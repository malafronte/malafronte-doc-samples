"""Dominio del registro dei preventivi: schema, validazione e operazioni (U12).

Responsabilità del modulo: dichiarare lo schema dei dati, separare i controlli
di **struttura** da quelli di **dominio**, e offrire le operazioni sul registro
in memoria — inserimento, aggiornamento, eliminazione e consultazione. Nessuna
lettura, nessuna scrittura, nessuna stampa: l'import del modulo non ha effetti.

Le operazioni già verificate nelle tappe U6-U11 — riepiloghi, viste ordinate,
ricerche — restano nel modulo storico `spedizione_u5.py` e sono riunite qui
come superficie del registro: la dipendenza va in una sola direzione, dal
dominio verso la logica già collaudata, e nessun contratto storico cambia.

Le rappresentazioni distinte del progetto restano quelle note: gli importi
della CLI U5 sono in euro, quelli del registro in **centesimi** interi; i
codici sono stringhe con zeri iniziali significativi.
"""
from spedizione_u5 import (
    cerca_per_codice,
    cerca_preventivo,
    matrice_riepilogo,
    ordina_fusione,
    ordina_inserimento,
    primo_indice_per_totale,
    riepilogo_per_destinazione,
    vista_per_codice,
    vista_per_totale,
)

VERSIONE_SCHEMA = 1
DESTINAZIONI_AMMESSE = ("locale", "nazionale")
CAMPI_RECORD = ("codice", "destinazione", "totale_cent")


# --- Validazione: struttura e dominio sono controlli separati ---


def valida_struttura_documento(dati) -> str:
    """Controlla la struttura del documento e restituisce "" oppure l'errore.

    Struttura attesa: un dizionario con le chiavi `versione_schema` e
    `preventivi`; `versione_schema` intero **non booleano**; `preventivi`
    lista di dizionari, ciascuno con esattamente i tre campi dello schema.
    Nessun controllo sui valori: il dominio è di `valida_dominio_record`.
    """
    if not isinstance(dati, dict):
        return "struttura: la radice del documento non è un oggetto"
    if set(dati.keys()) != {"versione_schema", "preventivi"}:
        return "struttura: attese le sole chiavi versione_schema e preventivi"
    versione = dati["versione_schema"]
    if isinstance(versione, bool) or not isinstance(versione, int):
        return "struttura: versione_schema deve essere un intero, non un booleano"
    if versione != VERSIONE_SCHEMA:
        return "struttura: versione_schema non supportata"
    preventivi = dati["preventivi"]
    if not isinstance(preventivi, list):
        return "struttura: preventivi deve essere una lista"
    for posizione in range(len(preventivi)):
        record = preventivi[posizione]
        if not isinstance(record, dict):
            return f"struttura: l'elemento {posizione} non è un oggetto"
        if set(record.keys()) != set(CAMPI_RECORD):
            return f"struttura: l'elemento {posizione} non ha esattamente i campi dello schema"
    return ""


def valida_dominio_record(record: dict) -> str:
    """Controlla i valori di un record e restituisce "" oppure l'errore.

    Dominio: `codice` stringa non vuota, `destinazione` fra quelle ammesse,
    `totale_cent` intero non negativo — i booleani non sono interi dello
    schema. La diagnosi nomina campo e valore non ammessi.
    """
    codice = record["codice"]
    if not isinstance(codice, str) or codice == "":
        return f"dominio: codice non ammesso: {codice!r}"
    destinazione = record["destinazione"]
    if destinazione not in DESTINAZIONI_AMMESSE:
        return f"dominio: destinazione non ammessa: {destinazione!r}"
    totale_cent = record["totale_cent"]
    if isinstance(totale_cent, bool) or not isinstance(totale_cent, int):
        return f"dominio: totale_cent deve essere un intero: {totale_cent!r}"
    if totale_cent < 0:
        return f"dominio: totale_cent non può essere negativo: {totale_cent}"
    return ""


def valida_registro(registro: list) -> str:
    """Controlla dominio e unicità dei codici; restituisce "" oppure l'errore.

    I codici sono stringhe e `"007"` è diverso da `"7"`: il duplicato si
    rileva sul confronto esatto fra stringhe.
    """
    codici_visti = []
    for record in registro:
        errore = valida_dominio_record(record)
        if errore != "":
            return errore
        if record["codice"] in codici_visti:
            return f"dominio: codice duplicato: {record['codice']!r}"
        codici_visti.append(record["codice"])
    return ""


# --- Operazioni sul registro in memoria ---


def crea_record(codice: str, destinazione: str, totale_cent: int) -> dict:
    """Restituisce un record nuovo con i tre campi dello schema.

    Precondizione: i dati sono nel dominio; la validazione è responsabilità di
    chi chiama, con `valida_dominio_record`.
    """
    return {
        "codice": codice,
        "destinazione": destinazione,
        "totale_cent": totale_cent,
    }


def inserisci_record(registro: list, codice: str, destinazione: str, totale_cent: int):
    """Aggiunge un record in coda e restituisce True, oppure False senza effetti.

    Effetto: modifica la lista ricevuta in posto. Rifiuta — senza risultati
    parziali — dati fuori dominio e codici già presenti.
    """
    record = crea_record(codice, destinazione, totale_cent)
    if valida_dominio_record(record) != "":
        return False
    if cerca_preventivo(registro, codice) is not None:
        return False
    registro.append(record)
    return True


def aggiorna_record(registro: list, codice: str, destinazione: str, totale_cent: int):
    """Aggiorna il record del codice e restituisce True, oppure False senza effetti.

    Effetto: modifica in posto il record già presente; la lista non cambia
    lunghezza. Con codice assente o dati fuori dominio nessun campo viene
    toccato.
    """
    record = crea_record(codice, destinazione, totale_cent)
    if valida_dominio_record(record) != "":
        return False
    da_aggiornare = cerca_preventivo(registro, codice)
    if da_aggiornare is None:
        return False
    da_aggiornare["destinazione"] = destinazione
    da_aggiornare["totale_cent"] = totale_cent
    return True


def elimina_record(registro: list, codice: str) -> bool:
    """Elimina il record del codice e restituisce True, oppure False se assente.

    Effetto: modifica la lista ricevuta in posto.
    """
    record = cerca_preventivo(registro, codice)
    if record is None:
        return False
    registro.remove(record)
    return True


# --- Presentazione ---


def formatta_euro(totale_cent: int) -> str:
    """Restituisce l'importo in centesimi come testo in euro, con la virgola.

    Esempi: 0 -> `0,00`, 450 -> `4,50`, 1200 -> `12,00`. Precondizione: intero
    non negativo. La conversione in centesimi non viene ripetuta: qui si
    formatta soltanto.
    """
    euro = totale_cent // 100
    centesimi = totale_cent % 100
    return f"{euro},{centesimi:02d}"
