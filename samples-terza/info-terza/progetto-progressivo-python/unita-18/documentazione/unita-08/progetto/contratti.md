# Contratti — registro di record e riepiloghi (U8)

Documento della tappa U8, scritto prima del codice. Le coppie U7 diventano
record con un codice sintetico univoco; la rappresentazione precedente resta
valida e non viene sostituita.

## Schema dei campi

| Campo | Tipo | Dominio | Unità |
|---|---|---|---|
| `codice` | `str` | stringa non vuota e unica nel registro | — |
| `destinazione` | `str` | esattamente `locale` oppure `nazionale` | — |
| `totale_cent` | `int` | intero non negativo | **centesimi** |

I codici sono **stringhe** e conservano gli zeri iniziali: `"007"` e `"7"` sono
codici diversi. Gli importi non si reinterpretano come euro: restano
centesimi, come nelle coppie U7. Le destinazioni ammesse sono sempre e solo
`locale` e `nazionale`: `estero` resta rifiutato dal validatore U5.

## Funzioni richieste

| Firma | Contratto |
|---|---|
| `crea_registro(codici, preventivi)` | Liste di uguale lunghezza, codici stringa non vuoti e unici, coppie nel dominio U7. Restituisce una **lista nuova di dizionari nuovi** con i tre campi, conservando ordine e argomenti. Lunghezze discordanti, codice vuoto o duplicato → `None`, senza risultato parziale. Due liste vuote → `[]`. |
| `riepilogo_per_destinazione(registro)` | Registro valido con codici unici. Restituisce un dizionario con **entrambe** le chiavi `locale` e `nazionale`, ciascuna associata a un **record nuovo** con i campi interi `conteggio` e `totale_cent`. Argomento invariato; senza dati, entrambi i campi valgono 0. |
| `cerca_preventivo(registro, codice)` | Restituisce il record corrispondente oppure `None`. Non muta il registro. Il record restituito è **quello contenuto nella lista**, non una copia. |

## Scelte motivate

La migrazione dalle liste parallele controlla prima le lunghezze, poi i codici
vuoti e infine i duplicati: qualunque controllo fallisca il risultato è `None`
e nessun record parziale viene restituito. La verifica dei duplicati usa una
lista di codici già visti: il confronto `in` sulle stringhe è il costrutto
disponibile in questa tappa.

Il riepilogo costruisce due record nuovi a ogni chiamata: i gruppi sono
indipendenti fra loro e fra chiamate successive. Le due grandezze — numero di
preventivi e somma in centesimi — restano separate e non si sommano.

La ricerca restituisce deliberatamente l'**alias** del record: la scelta
permette l'aggiornamento diretto di un record già consultato e va dichiarata.
Il caso PU8-08 mostra la differenza: la ricerca da sola non modifica nulla,
mentre la modifica del record ricevuto si vede anche nel registro.

## Casi limite

- **Zeri iniziali**: `crea_registro(["007", "7"], ...)` produce due record
  distinti; la ricerca li risolve separatamente.
- **Importo zero**: `totale_cent` pari a 0 è un importo valido, non un dato
  mancante.
- **Lista vuota**: `crea_registro([], [])` → `[]`; il riepilogo di un registro
  vuoto ha entrambi i gruppi a zero.
- **Duplicati di totale**: record con lo stesso importo sono record distinti e
  il riepilogo li conta tutti.

## Unità e conversioni

La conversione euro → centesimi appartiene alla costruzione delle coppie U7 e
si esegue **una sola volta**: qui gli importi sono già in centesimi. Il
confronto con il totale ricorsivo U6 usa la lista dei soli `totale_cent`, senza
nuove conversioni.
