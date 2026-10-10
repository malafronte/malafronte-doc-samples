"""Formati e scrittura con temporaneo chiuso prima della sostituzione."""

import csv
import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from rilevazioni_u15 import proiezioni, rilevazione_da_record


def scrivi_atomico(percorso, scrivi):
    """Il file precedente resta intatto fino alla sostituzione riuscita."""
    temporaneo = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=percorso.parent,
            prefix=".rapporto-",
            suffix=".tmp",
            delete=False,
        ) as stream:
            temporaneo = Path(stream.name)
            scrivi(stream)
        temporaneo.replace(percorso)
    finally:
        if temporaneo is not None:
            temporaneo.unlink(missing_ok=True)


def scrivi_csv(stream, record):
    writer = csv.DictWriter(stream, fieldnames=["codice", "valore", "unita"])
    writer.writeheader()
    writer.writerows(record)


def scrivi_json(stream, record):
    json.dump(record, stream, ensure_ascii=False, indent=2)
    stream.write("\n")


class EsportatoreCSV:
    def esporta(self, rilevazioni, percorso):
        record = proiezioni(rilevazioni)
        scrivi_atomico(percorso, lambda stream: scrivi_csv(stream, record))
        return None


class EsportatoreJSON:
    def esporta(self, rilevazioni, percorso):
        record = proiezioni(rilevazioni)
        scrivi_atomico(percorso, lambda stream: scrivi_json(stream, record))
        return None


def leggi_csv(percorso):
    risultato = []
    with percorso.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream)
        if next(reader, None) != ["codice", "valore", "unita"]:
            raise ValueError("CSV: intestazione diversa dallo schema")
        for numero, riga in enumerate(reader, start=2):
            if len(riga) != 3:
                raise ValueError(f"riga {numero}: attesi tre campi")
            try:
                valore = int(riga[1])
                risultato.append(
                    rilevazione_da_record(
                        {
                            "codice": riga[0],
                            "valore": valore,
                            "unita": riga[2],
                        }
                    )
                )
            except ValueError as errore:
                raise ValueError(f"riga {numero}: {errore}") from errore
    return risultato


def leggi_json(percorso):
    with percorso.open(encoding="utf-8") as stream:
        record = json.load(stream)
    if not isinstance(record, list):
        raise ValueError("JSON: attesa una lista di record")
    return [rilevazione_da_record(voce) for voce in record]
