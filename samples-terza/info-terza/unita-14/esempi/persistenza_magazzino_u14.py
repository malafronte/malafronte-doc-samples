"""Persistenza del magazzino composto: CSV e JSON con le politiche storiche (OOP-04).

Raccordo fra il `Magazzino` U14 e i file. Le politiche sono quelle già
verificate in U12 e U13, **identiche**: CSV con intestazione esatta
`codice,descrizione,quantita,prezzo_centesimi`, `csv.reader`/`csv.writer`
con `newline=""`, ingresso UTF-8 con o senza BOM (`utf-8-sig`), uscita
UTF-8 **senza** BOM; JSON con schema `{"versione_schema": 1, "articoli":
[...]}`. Il salvataggio valida tutto, scrive un temporaneo nella stessa
directory della destinazione, lo chiude e solo allora lo sostituisce: su
guasto il file precedente resta integro.

Caricamento: **tutto valido oppure nessun dato caricato**; ogni record
diventa una istanza nuova nel magazzino. Le conversioni restano esplicite:
campo testuale → numero convertito → oggetto costruito sono passaggi
distinti; nessuna esportazione opaca di `__dict__`, nessun `asdict`
indiscriminato, nessun `pickle`.

Questo modulo usa **solo le operazioni pubbliche** del magazzino:
`inserisci` per costruire, `articoli` per proiettare. Non scrive mai
nella lista interna e il magazzino non conosce percorsi.

Ambiente: CPython sul computer. Dipende dal modello U14.
"""

import csv
import json
import os
import tempfile
from pathlib import Path

from articolo_proprieta_u14 import CAMPI_ARTICOLO
from magazzino_composto_u14 import Magazzino

VERSIONE_SCHEMA_JSON = 1


def _intero_da_testo(testo, campo, riferimento):
    """Converte un campo testuale in intero, con diagnosi di campo e record."""
    try:
        return int(testo)
    except ValueError:
        raise ValueError(
            f"{riferimento}, campo '{campo}': il testo {testo!r} non è un intero"
        ) from None


def _valida_intestazione(intestazione):
    """Controlla che l'intestazione del CSV coincida con lo schema esatto."""
    nomi = list(intestazione)
    duplicati = [nome for nome in nomi if nomi.count(nome) > 1]
    if duplicati:
        raise ValueError(f"intestazione con nomi duplicati: {duplicati[0]!r}")
    mancanti = [campo for campo in CAMPI_ARTICOLO if campo not in nomi]
    if mancanti:
        raise ValueError(f"intestazione: colonna mancante {mancanti[0]!r}")
    extra = [nome for nome in nomi if nome not in CAMPI_ARTICOLO]
    if extra:
        raise ValueError(f"intestazione: colonna non prevista {extra[0]!r}")
    if nomi != list(CAMPI_ARTICOLO):
        attesa = ", ".join(CAMPI_ARTICOLO)
        raise ValueError(f"intestazione: ordine delle colonne diverso da {attesa}")


def riga_a_dati(riga, riferimento_riga):
    """Converte una riga CSV nei quattro dati dell'articolo, già validati."""
    if len(riga) != len(CAMPI_ARTICOLO):
        attesi = ", ".join(CAMPI_ARTICOLO)
        raise ValueError(
            f"{riferimento_riga}: attesi {len(CAMPI_ARTICOLO)} campi ({attesi}), "
            f"ricevuti {len(riga)}"
        )
    quantita = _intero_da_testo(riga[2], "quantita", riferimento_riga)
    prezzo_centesimi = _intero_da_testo(riga[3], "prezzo_centesimi", riferimento_riga)
    return (riga[0], riga[1], quantita, prezzo_centesimi)


def dati_a_riga(dat):
    """Proietta i dati di un articolo nei quattro campi testuali dello schema."""
    return [dat.codice, dat.descrizione, str(dat.quantita), str(dat.prezzo_centesimi)]


def carica_magazzino(percorso):
    """Legge l'archivio CSV e restituisce un **nuovo** `Magazzino` popolato.

    `FileNotFoundError` se il file non esiste, `UnicodeDecodeError` per byte
    non UTF-8, `csv.Error` per strutture malformate, `ValueError` per
    intestazione, conversioni, domini o duplicati, con il riferimento della
    riga. Nessun magazzino parziale: l'istanza viene restituita solo dopo
    che l'intero file ha superato i controlli; una lettura interrotta prima
    non consegna nulla al chiamante.
    """
    percorso = Path(percorso)
    magazzino = Magazzino()
    with open(percorso, encoding="utf-8-sig", newline="") as sorgente:
        lettore = csv.reader(sorgente, strict=True)
        try:
            intestazione = next(lettore)
        except StopIteration:
            raise ValueError("archivio senza intestazione") from None
        _valida_intestazione(intestazione)
        for numero, riga in enumerate(lettore, start=2):
            if riga == []:
                continue
            riferimento = f"riga {numero}"
            dati = riga_a_dati(riga, riferimento)
            try:
                magazzino.inserisci(*dati)
            except ValueError as errore:
                raise ValueError(f"{riferimento}: {errore}") from None
    return magazzino


def _salva_con_temporaneo(percorso, righe):
    """Scrive le righe con il protocollo del temporaneo. Funzione interna."""
    percorso = Path(percorso)
    temporaneo = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="",
            delete=False,
            dir=percorso.parent,
            prefix=percorso.name + ".",
            suffix=".tmp",
        ) as uscita:
            temporaneo = Path(uscita.name)
            scrittore = csv.writer(uscita, lineterminator="\n")
            for riga in righe:
                scrittore.writerow(riga)
        temporaneo.replace(percorso)
    except Exception as errore:
        if temporaneo is not None:
            try:
                temporaneo.unlink()
            except OSError:
                errore.add_note(f"temporaneo non rimosso: {temporaneo}")
        raise
    return None


def salva_magazzino(percorso, magazzino):
    """Scrive l'intero magazzino nel file CSV con la sostituzione protetta.

    Prima proietta tutti gli articoli (le proiezioni sono già dati validi:
    un articolo raggiungibile solo dall'API non può essere invalido), poi
    scrive su temporaneo e sostituisce. Su errore la destinazione resta
    invariata e l'eccezione sale al chiamante. `None` sul successo.
    """
    righe = [list(CAMPI_ARTICOLO)]
    for dat in magazzino.articoli():
        righe.append(dati_a_riga(dat))
    _salva_con_temporaneo(percorso, righe)
    return None


def articoli_a_json(magazzino):
    """Proietta il magazzino nel dizionario JSON con la versione dello schema.

    Nuovo dizionario, nuova lista, nuovi record: la rappresentazione è
    costruita campo per campo dal modello, non esportata in blocco.
    """
    return {
        "versione_schema": VERSIONE_SCHEMA_JSON,
        "articoli": [
            {
                "codice": dat.codice,
                "descrizione": dat.descrizione,
                "quantita": dat.quantita,
                "prezzo_centesimi": dat.prezzo_centesimi,
            }
            for dat in magazzino.articoli()
        ],
    }


def json_a_magazzino(dati):
    """Ricostruisce un `Magazzino` dal dizionario JSON, con controlli espliciti.

    `ValueError` se la struttura non è quella dichiarata: manca la versione,
    la lista, un campo, o un dominio non è rispettato. Anche qui valgono le
    conversioni esplicite: nessuna fiducia nei tipi letti dal file.
    """
    if not isinstance(dati, dict):
        raise ValueError(f"radice JSON: atteso un oggetto, ricevuto {type(dati).__name__}")
    if "versione_schema" not in dati:
        raise ValueError("radice JSON: manca 'versione_schema'")
    if dati["versione_schema"] != VERSIONE_SCHEMA_JSON:
        raise ValueError(
            f"versione_schema non supportata: attesa {VERSIONE_SCHEMA_JSON}, "
            f"ricevuta {dati['versione_schema']!r}"
        )
    if "articoli" not in dati:
        raise ValueError("radice JSON: manca 'articoli'")
    if not isinstance(dati["articoli"], list):
        raise ValueError(
            f"campo 'articoli': attesa una lista, ricevuto {type(dati['articoli']).__name__}"
        )
    magazzino = Magazzino()
    for posizione, record in enumerate(dati["articoli"], start=1):
        riferimento = f"articolo {posizione}"
        if not isinstance(record, dict):
            raise ValueError(f"{riferimento}: atteso un oggetto, ricevuto {type(record).__name__}")
        for campo in CAMPI_ARTICOLO:
            if campo not in record:
                raise ValueError(f"{riferimento}: manca il campo {campo!r}")
        try:
            magazzino.inserisci(
                record["codice"],
                record["descrizione"],
                record["quantita"],
                record["prezzo_centesimi"],
            )
        except ValueError as errore:
            raise ValueError(f"{riferimento}: {errore}") from None
    return magazzino


def salva_magazzino_json(percorso, magazzino):
    """Scrive il magazzino in JSON con la sostituzione protetta. `None` sul successo."""
    percorso = Path(percorso)
    temporaneo = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="",
            delete=False,
            dir=percorso.parent,
            prefix=percorso.name + ".",
            suffix=".tmp",
        ) as uscita:
            temporaneo = Path(uscita.name)
            json.dump(articoli_a_json(magazzino), uscita, ensure_ascii=False, indent=2)
            uscita.write("\n")
        temporaneo.replace(percorso)
    except Exception as errore:
        if temporaneo is not None:
            try:
                temporaneo.unlink()
            except OSError:
                errore.add_note(f"temporaneo non rimosso: {temporaneo}")
        raise
    return None


def carica_magazzino_json(percorso):
    """Legge il file JSON e ricostruisce un `Magazzino` con `json_a_magazzino`."""
    with open(percorso, encoding="utf-8-sig") as sorgente:
        dati = json.load(sorgente)
    return json_a_magazzino(dati)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("uso: python persistenza_magazzino_u14.py <archivio.csv>")
        raise SystemExit(2)
    sorgente = Path(sys.argv[1])
    magazzino = carica_magazzino(sorgente)
    print("caricato:", magazzino.riepilogo())

    destinazione_csv = Path(str(sorgente) + ".copia.csv")
    salva_magazzino(destinazione_csv, magazzino)
    print("round-trip CSV identico:", sorgente.read_bytes() == destinazione_csv.read_bytes())

    destinazione_json = Path(str(sorgente) + ".json")
    salva_magazzino_json(destinazione_json, magazzino)
    ritorno = carica_magazzino_json(destinazione_json)
    print("round-trip JSON equivalente:", ritorno.riepilogo() == magazzino.riepilogo())

    os.remove(destinazione_csv)
    os.remove(destinazione_json)
