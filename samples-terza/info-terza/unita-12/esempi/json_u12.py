"""Serializzazione JSON e confronto con il formato CSV.

Il modulo mostra come una lista di articoli diventi testo JSON e ritorni
record validi. Distingue tre controlli che il parsing **non** compie da solo:

1. **sintassi**: `json.loads` accetta soltanto testo JSON valido e altrimenti
   solleva `JSONDecodeError` (una sottoclasse di `ValueError`);
2. **struttura**: la radice deve essere una lista e ogni elemento un oggetto
   con i campi dello schema;
3. **dominio**: tipi, segni e unicità dei codici valgono come nel CSV: un JSON
   sintatticamente valido può contenere `true` al posto di una quantità, e
   `true` non è una quantità di questo schema.

Scrittura: `ensure_ascii=False` mantiene gli accenti leggibili nel testo,
`allow_nan=False` esclude `NaN` e infiniti, che non sono valori JSON
interoperabili; il file viene scritto UTF-8 **senza BOM**, come richiede la
RFC 8259 per i documenti di interscambio.

Ambiente: CPython sul computer. Dipende dal modulo di dominio per i controlli
sui record.
"""

import json
from pathlib import Path

from dominio_magazzino_u12 import CAMPI_ARTICOLO
from dominio_magazzino_u12 import valida_articolo


def serializza_articoli(articoli):
    """Restituisce il testo JSON della lista di articoli, senza BOM.

    I numeri restano numeri, gli accenti restano accenti. La validazione dei
    record è precondizione, come negli altri moduli di calcolo: la scrittura
    di un archivio usa invece `persistenza_magazzino_u12.salva_articoli`, che
    valida tutto prima di scrivere.
    """
    return json.dumps(articoli, ensure_ascii=False, indent=2, allow_nan=False)


def deserializza_articoli(testo):
    """Ricostruisce la lista di articoli da testo JSON, con tre controlli.

    Sintassi (`JSONDecodeError`), struttura e dominio (`ValueError`) sono
    diagnosi distinte. La lista restituita è nuova e nell'ordine del
    documento; i codici duplicati vengono rifiutati come nel caricamento CSV.
    Questa è la politica canonica: come `json.load`, **non** rileva i nomi
    duplicati dentro lo stesso oggetto (ne resta l'ultimo valore).
    """
    return _deserializza(testo, senza_doppioni=False)


def deserializza_articoli_strict(testo):
    """Come `deserializza_articoli`, ma rifiuta anche i nomi JSON duplicati.

    Il controllo dei nomi duplicati **non** è di `json.load`: qui è un
    meccanismo esplicito, l'`object_pairs_hook` passato al parser, che riceve
    le coppie (nome, valore) dell'oggetto prima della costruzione del
    dizionario e solleva `ValueError` al secondo nome uguale.
    """
    return _deserializza(testo, senza_doppioni=True)


def _rifiuta_nomi_doppi(coppie):
    """`object_pairs_hook` esplicito contro i nomi duplicati in un oggetto."""
    oggetto = {}
    for nome, valore in coppie:
        if nome in oggetto:
            raise ValueError(f"nome JSON duplicato: {nome!r}")
        oggetto[nome] = valore
    return oggetto


def _deserializza(testo, senza_doppioni):
    if senza_doppioni:
        dati = json.loads(testo, object_pairs_hook=_rifiuta_nomi_doppi)
    else:
        dati = json.loads(testo)
    if not isinstance(dati, list):
        raise ValueError(f"radice errata: attesa una lista, ricevuta {type(dati).__name__}")
    articoli = []
    codici = set()
    for posizione, record in enumerate(dati, start=1):
        if not isinstance(record, dict):
            raise ValueError(
                f"record {posizione}: atteso un oggetto JSON, ricevuto {type(record).__name__}"
            )
        try:
            valida_articolo(record)
        except ValueError as errore:
            raise ValueError(f"record {posizione}: {errore}") from None
        if record["codice"] in codici:
            raise ValueError(f"record {posizione}: il codice {record['codice']!r} è già presente")
        codici.add(record["codice"])
        articoli.append(dict(record))
    return articoli


def salva_json(percorso, articoli):
    """Scrive la lista di articoli come documento JSON UTF-8 senza BOM.

    Aggiunge il terminatore finale di riga, come fa ogni file di testo del
    corso. Questa scrittura è **diretta**: il protocollo del temporaneo della
    persistenza CSV serve quando la destinazione deve sopravvivere a un
    guasto, ed è il tema del problema PY-U12-T16.
    """
    with open(percorso, "w", encoding="utf-8") as uscita:
        uscita.write(serializza_articoli(articoli) + "\n")


def carica_json(percorso):
    """Legge un documento JSON di articoli e applica i tre controlli.

    Il file è aperto come UTF-8 senza BOM, secondo il contratto. Un documento
    con firma iniziale non viene decodificato male: il parser segnala la
    presenza del BOM come errore di sintassi, e il capitolo mostra il
    messaggio. Se il contratto di interscambio ammettesse il BOM, sarebbe il
    caso di usare `utf-8-sig` come per il CSV.
    """
    with open(percorso, "r", encoding="utf-8") as sorgente:
        return deserializza_articoli(sorgente.read())


if __name__ == "__main__":
    # Dimostrazione: round-trip, tipi ricostruiti e diagnosi separate.
    magazzino = [
        {"codice": "007", "descrizione": "Vite, lunga", "quantita": 4, "prezzo_centesimi": 25},
        {"codice": "012", "descrizione": 'Caffè "A"', "quantita": 2, "prezzo_centesimi": 350},
    ]
    testo = serializza_articoli(magazzino)
    print(testo)
    ricostruiti = deserializza_articoli(testo)
    print("round-trip identico:", ricostruiti == magazzino)
    print("tipo della quantita:", type(ricostruiti[0]["quantita"]).__name__)

    for titolo, documento in [
        ("radice sbagliata", '{"articoli": []}'),
        ("campo mancante", '[{"codice": "1", "descrizione": "x", "quantita": 1}]'),
        ("booleano come quantita", '[{"codice": "1", "descrizione": "x", "quantita": true, "prezzo_centesimi": 0}]'),
        ("codice duplicato", '[{"codice": "1", "descrizione": "x", "quantita": 1, "prezzo_centesimi": 0},'
                             ' {"codice": "1", "descrizione": "y", "quantita": 1, "prezzo_centesimi": 0}]'),
    ]:
        try:
            deserializza_articoli(documento)
        except ValueError as errore:
            print(f"{titolo}: {errore}")
    doppio = '[{"codice": "1", "descrizione": "x", "quantita": 1, "quantita": 2, "prezzo_centesimi": 0}]'
    print("nomi duplicati, politica canonica:", deserializza_articoli(doppio))
    try:
        deserializza_articoli_strict(doppio)
    except ValueError as errore:
        print("nomi duplicati, strict:", errore)
