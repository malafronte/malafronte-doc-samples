# Raccolta progressiva di programmi - fotografia U18

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 18**: conserva i programmi U1-U17 e aggiunge l'**indice hash di
consultazione per codice** — tabella con concatenamento, funzione hash
didattica, crescita per raddoppio e validazione riusata dal modello del
registro, con ricerca esatta costruita su una fotografia dei preventivi —
oltre alla documentazione dei contratti e dei costi e al diagramma aggiornato.
È il riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografia precedente:
[`../unita-17/`](../unita-17/).

## Traguardi della tappa

- **indice hash per codice** `IndiceHashU18`: la tabella con concatenamento del
  capitolo PY-34 è riprodotta nel progetto e adattata a **chiavi stringa**,
  con i codici `007`, `012` e `003` conservati come stringhe;
- **validazione riusata** dal modello del registro: `valida_chiave`
  richiama `valida_dominio_record` sul campo `codice`, senza duplicare regole
  né diagnosi;
- **ricerca esatta e fotografia ordinata**: `cerca` restituisce il record del
  codice, `fotografia_ordinata` le coppie in ordine lessicografico per la
  presentazione; gli intervalli restano interrogazioni dell'indice BST U17;
- **costruzione dopo il caricamento**: l'indice è costruito sulla proiezione
  pubblica `preventivi()` del registro e risponde a più interrogazioni sulla
  stessa fotografia;
- **ciclo di vita esplicito**: una modifica del registro richiede una nuova
  costruzione dell'indice e la vecchia fotografia continua a rappresentare i
  dati precedenti, grazie ai valori immutabili del modello U14;
- **punto di avvio** `indice_cli_u18.py` separato dalla struttura, che legge
  gli argomenti, costruisce l'indice dopo il caricamento e risponde a più
  interrogazioni nell'ordine della riga di comando;
- **costi separati**: `confronti_per` conta le chiavi esaminate nella catena
  con la regola dichiarata, e la suite PU18-12 confronta carico e fotografia;
- **prove** dei casi PU18-01–PU18-12 più tre casi propri motivati, con
  regressione U5–U17 verificata dalla suite cumulativa.

## Struttura

```text
unita-18/
├── programmi/
│   ├── ... programmi U1-U17 invariati ...
│   ├── indice_hash_u18.py         # tabella hash e indice per codice
│   ├── indice_cli_u18.py          # punto di avvio: interroga dopo il caricamento
│   └── test_indice_hash_u18.py    # suite della tappa (15 test)
├── dati/unita-12/ (fixture invariate, dataset 007/012/003)
├── risultati/ (unita-09, unita-11 invariati)
├── documentazione/
│   ├── unita-01/ ... unita-17/ (documenti invariati)
│   └── unita-18/
│       ├── indice-hash-contratto-e-costi.md  # contratto, varianti e costi
│       ├── prove-e-regressione.md            # casi, difetti plausibili, regressione
│       └── diagramma.puml                    # UML aggiornato con l'indice
└── README.md, pyproject.toml, uv.lock, .python-version, .gitignore
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync                                         # ricostruisce .venv/ dal lock
uv run pytest -q                                # suite cumulativa U5-U18
uv run pytest -q programmi/test_indice_hash_u18.py
Copy-Item dati/unita-12/archivio_canonico.json dati/unita-12/archivio.json
uv run python programmi/indice_cli_u18.py fotografia cerca 007 cerca 999 statistiche
```

## Sessioni reali

Esecuzione verificata su Windows 11, CPython 3.14.7, uv 0.12.15, pytest 9.1.1.
Suite cumulativa:

```text
> uv run --frozen pytest -q
........................................................................ [ 66%]
........................................................................ [ 99%]
.                                                                        [100%]
217 passed in 0.96s
```

**217 test**: 202 delle tappe U5–U17 più 15 della tappa U18 — i casi
PU18-01–PU18-12, i tre casi propri motivati e i controlli sugli invarianti
dell'indice. La sola suite della tappa riporta 15 test superati. Le
interrogazioni reali con il dataset pubblicato, sulla stessa fotografia:

Le interrogazioni reali con il dataset pubblicato, sulla stessa fotografia:

```text
> uv run python programmi/indice_cli_u18.py fotografia cerca 007 cerca 999 statistiche
fotografia caricata: 3 preventivi, indice costruito: 3 codici, carico 0.60
fotografia -> [003/locale/1200, 007/locale/450, 012/nazionale/0]
cerca 007 -> 007/locale/450
cerca 999 -> assente
statistiche -> codici 3, bucket 5, carico 0.60
interrogazioni eseguite: 4
```

L'indice risponde con la fotografia ordinata `["003", "007", "012"]` e lascia
alla raccolta del registro l'ordine `["007", "012", "003"]`. Con argomenti non
ammessi — per esempio `intervallo 003 007`, che appartiene allo strumento U17
— il programma presenta la guida e termina senza costruire l'indice.

## Differenze rispetto alla fotografia U17

I file U1–U17 restano invariati; la tappa U18 aggiunge i due moduli
dell'indice, il punto di avvio, la suite e i tre documenti di
`documentazione/unita-18/`. La regressione verificata riguarda i contratti
mantenuti: modello U14, persistenza U12, tariffe U3/U5, ordine della raccolta,
coda U16 e indice BST U17 non cambiano firma né comportamento, e la suite
U5–U17 supera per intero. I limiti dichiarati: l'indice rappresenta la
fotografia del momento della costruzione e ogni modifica del registro richiede
una nuova costruzione; la tabella del capitolo PY-34 è riprodotta nel progetto
con chiavi stringa per mantenere la fotografia autonoma, e i conteggi dei
confronti non includono il costo di hash e confronti fra testi.
