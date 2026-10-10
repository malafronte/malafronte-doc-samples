# Schema e dati del registro persistente (U12)

Documento dello schema adottato per l'archivio dei preventivi. Fa parte della
consegna: campi, tipi, domini, identità e politiche sono dichiarati prima del
codice e verificati dai test.

## Formato canonico

Il documento canonico è un file **JSON** con la radice dichiarata:

```json
{
  "versione_schema": 1,
  "preventivi": [
    {"codice": "007", "destinazione": "locale", "totale_cent": 450}
  ]
}
```

Codifica UTF-8 **senza BOM**, come da RFC 8259. Il CSV di consultazione con
intestazione `codice,destinazione,totale_cent` è una lettura per altri lettori
e **non** sostituisce il documento canonico: non contiene la versione dello
schema e non viene usato per il caricamento.

## Campi

| Campo | Tipo | Dominio | Identità e unità |
|---|---|---|---|
| `versione_schema` | intero, **non booleano** | valore `1` | versione del formato, non un importo |
| `preventivi` | lista di oggetti | anche vuota | ordine dei record conservato nel round-trip |
| `codice` | stringa | non vuota, unica nel documento | identità del record; zeri iniziali significativi: `"007"` ≠ `"7"` |
| `destinazione` | stringa | esattamente `locale` oppure `nazionale` | nessuna normalizzazione in fase di caricamento |
| `totale_cent` | intero | non negativo, zero ammesso | **centesimi**; i booleani non sono interi dello schema |

In Python `True == 1` e `isinstance(True, int)` è vero: per questo la
validazione esclude esplicitamente i booleani dal campo `versione_schema` e da
`totale_cent`. Il caso è verificato da `test_proprio_1` e dal test su
`totale_cent` non intero.

## Politiche

- **Campi extra**: un oggetto con campi oltre i tre dello schema è
  **rifiutato**. La politica è stretta: un campo ignoto può nascondere un
  errore di scrittura e non viene ignorato.
- **Campi mancanti**: un oggetto senza uno dei tre campi è rifiutato, con la
  stessa diagnosi di struttura.
- **Chiavi della radice**: attese esattamente `versione_schema` e `preventivi`;
  chiavi aggiuntive o mancanti rifiutano il documento.
- **Versioni diverse da 1**: rifiutate come struttura; il campo non è un
  intero qualsiasi ma la versione del formato supportato.

## Validazione separata in due livelli

| Livello | Controlla | Funzione | Esito |
|---|---|---|---|
| Struttura | forma del documento, tipi di base dei campi, campi extra o mancanti | `valida_struttura_documento` | `struttura` |
| Dominio | codice stringa non vuoto, destinazione ammessa, intero non negativo, codici univoci | `valida_dominio_record` e `valida_registro` | `dominio` |

Un documento può essere sintatticamente valido, strutturalmente valido e
comunque fuori dominio: per esempio un record con destinazione `estero`. I due
controlli non vanno fusi, perché rispondono a domande diverse — «il documento
ha la forma giusta?» e «i valori sono ammessi?» — e producono diagnosi diverse.

## Dati sintetici di riferimento

Le fixture di `dati/unita-12/` sono soltanto sintetiche e coprono i casi
discriminanti: `archivio_canonico.json` con codici `007`, `012`, `003` e totali
`450`, `0`, `1200` centesimi — il codice con zeri e il totale zero sono i casi
che ogni scorciatoia sbaglia — più gli archivi vuoto, corrotto, fuori schema,
con versione booleana, con duplicati e con campo extra.
