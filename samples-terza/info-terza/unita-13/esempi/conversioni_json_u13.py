"""Conversioni JSON della variante a oggetti del magazzino (OOP-02, sez. J).

Una classe **non** si serializza da sola: `json.dumps` non sa convertire un
`Articolo` e restituisce un `TypeError`. Il passaggio fra oggetti e testo JSON
resta quindi una conversione **esplicita**, in due tempi:

1. **proiezione**: l'oggetto produce un record-dizionario di dati semplici con
   `dati()`;
2. **ricostruzione**: i dati vengono validati e servono a costruire
   un'istanza **nuova**.

Il documento JSON del magazzino conserva lo schema già usato dal progetto
progressivo e dalla versione procedurale:

```json
{"versione_schema": 1, "articoli": [{"codice": "007", ...}, ...]}
```

`versione_schema` permette di riconoscere il formato senza interpretarlo a
occhio. I nomi e l'ordine dei campi degli articoli sono quelli dello schema
CSV. I campi numerici restano numeri JSON e vengono **validati** alla
ricostruzione: `true`, `2.5` e `-1` non diventano dati validi per coercizione.

Nessuna serializzazione opaca: `__dict__` non è uno schema e `pickle` non
sostituisce né la validazione né il formato dichiarato.

Ambiente: CPython sul computer. Dipende da `articolo_u13` e da
`dominio_magazzino_u13`.
"""

import json

from articolo_u13 import CAMPI_ARTICOLO, Articolo
from dominio_magazzino_u13 import riepilogo_magazzino

# Versione del formato del documento JSON del magazzino.
VERSIONE_SCHEMA = 1


def articoli_a_dati(articoli):
    """Proietta la raccolta nel documento JSON come strutture semplici.

    Restituisce un dizionario nuovo con `versione_schema` e `articoli`, dove
    ogni articolo è il record prodotto da `dati()`. Nessuna mutazione: i
    dizionari risultanti non condividono nulla con le istanze.
    """
    return {
        "versione_schema": VERSIONE_SCHEMA,
        "articoli": [articolo.dati() for articolo in articoli],
    }


def dati_a_articoli(documento):
    """Ricostruisce una lista di `Articolo` dal documento JSON validato.

    Controlla la forma del documento, la versione dello schema, il numero e i
    nomi dei campi di ogni articolo, la conversione dei tipi e l'unicità dei
    codici. Un dato fuori contratto solleva `ValueError` con la diagnosi e
    **nessuna lista parziale** viene restituita.
    """
    if not isinstance(documento, dict):
        raise ValueError(
            f"documento: atteso un dizionario, ricevuto {type(documento).__name__}"
        )
    if "versione_schema" not in documento:
        raise ValueError("campo 'versione_schema': mancante")
    if documento["versione_schema"] != VERSIONE_SCHEMA:
        raise ValueError(
            f"campo 'versione_schema': attesa la versione {VERSIONE_SCHEMA}, "
            f"ricevuta {documento['versione_schema']!r}"
        )
    extra_documento = [chiave for chiave in documento if chiave != "versione_schema"]
    if "articoli" not in documento:
        raise ValueError("campo 'articoli': mancante")
    extra_documento = [chiave for chiave in extra_documento if chiave != "articoli"]
    if extra_documento:
        raise ValueError(f"campo '{extra_documento[0]}': non previsto dallo schema")

    elenco = documento["articoli"]
    if not isinstance(elenco, list):
        raise ValueError(f"campo 'articoli': attesa una lista, ricevuta {type(elenco).__name__}")

    articoli = []
    codici = set()
    for posizione, record in enumerate(elenco, start=1):
        if not isinstance(record, dict):
            raise ValueError(
                f"articolo {posizione}: atteso un dizionario, ricevuto {type(record).__name__}"
            )
        mancanti = [campo for campo in CAMPI_ARTICOLO if campo not in record]
        if mancanti:
            raise ValueError(f"articolo {posizione}, campo '{mancanti[0]}': mancante")
        extra = [chiave for chiave in record if chiave not in CAMPI_ARTICOLO]
        if extra:
            raise ValueError(f"articolo {posizione}, campo '{extra[0]}': non previsto dallo schema")
        try:
            articolo = Articolo(
                record["codice"],
                record["descrizione"],
                record["quantita"],
                record["prezzo_centesimi"],
            )
        except ValueError as errore:
            raise ValueError(f"articolo {posizione}: {errore}") from None
        codice = articolo.dati()["codice"]
        if codice in codici:
            raise ValueError(f"articolo {posizione}: il codice {codice!r} è già presente")
        codici.add(codice)
        articoli.append(articolo)
    return articoli


def articoli_a_testo(articoli):
    """Restituisce la rappresentazione JSON della raccolta.

    `ensure_ascii=False` conserva gli accenti come caratteri leggibili;
    `indent=2` rende il documento confrontabile con una differenza di testo.
    """
    return json.dumps(articoli_a_dati(articoli), ensure_ascii=False, indent=2)


def testo_a_articoli(testo):
    """Ricostruisce la raccolta da una rappresentazione JSON.

    Un testo non conforme alla sintassi JSON solleva `json.JSONDecodeError`;
    un documento conforme nella sintassi ma non nello schema solleva
    `ValueError` dalla validazione. Le due diagnosi restano distinte.
    """
    documento = json.loads(testo)
    return dati_a_articoli(documento)


if __name__ == "__main__":
    # Round-trip completo: istanze -> testo JSON -> nuove istanze.
    originali = [
        Articolo("007", "Vite, lunga", 4, 25),
        Articolo("012", 'Caffè "A"', 2, 350),
    ]
    testo = articoli_a_testo(originali)
    print(testo)
    ricostruiti = testo_a_articoli(testo)
    print("numero di articoli:", len(ricostruiti))
    print(
        "dati equivalenti:",
        [a.dati() for a in originali] == [a.dati() for a in ricostruiti],
    )
    print("istanze distinte:", ricostruiti[0] is not originali[0])
    print("riepilogo:", riepilogo_magazzino(ricostruiti))
