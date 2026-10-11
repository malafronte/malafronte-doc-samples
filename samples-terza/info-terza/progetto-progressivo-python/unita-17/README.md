# Raccolta progressiva di programmi - fotografia U17

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 17**: conserva i programmi U1-U16 e aggiunge l'**indice BST di
consultazione per codice** - chiavi stringa in ordine lessicografico,
validazione riusata dal modello del registro, ricerca esatta e intervalli
chiusi costruiti su una fotografia dei preventivi - oltre alla documentazione
dei contratti e dei costi e al diagramma aggiornato. È il riferimento di
confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografia precedente:
[`../unita-16/`](../unita-16/).

## Traguardi della tappa

- **indice BST per codice** `IndiceBSTU17`: la struttura ad albero del
  capitolo PY-33 è riprodotta nel progetto e adattata a **chiavi stringa**,
  con l'ordine lessicografico di Python e i codici `007`, `012` e `003`
  conservati come stringhe;
- **validazione riusata** dal modello del registro: `valida_chiave`
  richiama `valida_dominio_record` sul campo `codice`, senza duplicare regole
  né diagnosi;
- **ricerca esatta e intervalli chiusi**: `cerca` restituisce il record del
  codice, `intervallo` le coppie con codice compreso fra due estremi inclusi,
  `inordine` la vista ordinata dell'indice;
- **costruzione dopo il caricamento**: l'indice è costruito sulla proiezione
  pubblica `preventivi()` del registro e risponde a più interrogazioni sulla
  stessa fotografia;
- **ciclo di vita esplicito**: una modifica del registro richiede una nuova
  costruzione dell'indice e la vecchia fotografia continua a rappresentare i
  dati precedenti, grazie ai valori immutabili del modello U14;
- **punto di avvio** `indice_cli_u17.py` separato dalla struttura, che legge
  gli argomenti, costruisce l'indice dopo il caricamento e risponde a più
  interrogazioni nell'ordine della riga di comando;
- **costi separati**: `misura_costruzione` e `misura_ricerca` contano i nodi
  esaminati con la regola dichiarata, e la suite PU17-09 confronta sequenze
  crescenti e mescolate;
- **prove** dei casi PU17-01-PU17-10 più tre casi propri motivati, con
  regressione U5-U16 verificata dalla suite cumulativa.

## Struttura

```text
unita-17/
├── programmi/
│   ├── ... programmi U1-U16 invariati ...
│   ├── indice_bst_u17.py        # struttura ad albero e indice per codice
│   ├── indice_cli_u17.py        # punto di avvio: interroga dopo il caricamento
│   └── test_indice_bst_u17.py   # suite della tappa (20 test)
├── dati/unita-12/ (fixture invariate, dataset 007/012/003)
├── risultati/ (unita-09, unita-11 invariati)
├── documentazione/
│   ├── unita-01/ ... unita-16/ (documenti invariati)
│   └── unita-17/
│       ├── indice-contratto-e-costi.md  # contratto, varianti e costi
│       ├── prove-e-regressione.md       # casi, difetti plausibili, regressione
│       └── diagramma.puml               # UML aggiornato con l'indice
└── README.md, pyproject.toml, uv.lock, .python-version, .gitignore
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync                                         # ricostruisce .venv/ dal lock
uv run pytest -q                                # suite cumulativa U5-U17
uv run pytest -q programmi/test_indice_bst_u17.py
Copy-Item dati/unita-12/archivio_canonico.json dati/unita-12/archivio.json
uv run python programmi/indice_cli_u17.py ordine cerca 007 cerca 999 intervallo 003 007 statistiche
```

## Sessioni reali

Esecuzione verificata su Windows 11, CPython 3.14.7, uv 0.12.15, pytest 9.1.1.
Suite cumulativa:

```text
> uv run --frozen pytest -q
........................................................................ [ 35%]
........................................................................ [ 71%]
..........................................................               [100%]
202 passed in 0.47s
```

**202 test**: 182 delle tappe U5-U16 più 20 della tappa U17 - i casi
PU17-01-PU17-10, i tre casi propri motivati e i controlli sugli invarianti
dell'indice. La sola suite della tappa riporta 20 test superati. Le
interrogazioni reali con il dataset pubblicato, sulla stessa fotografia:

```text
> uv run python programmi/indice_cli_u17.py ordine cerca 007 cerca 999 intervallo 003 007 statistiche
fotografia caricata: 3 preventivi, indice costruito: 3 codici, altezza 1
ordine -> [003, 007, 012]
cerca 007 -> 007/locale/450
cerca 999 -> assente
intervallo 003 007 -> [003/locale/1200, 007/locale/450]
statistiche -> codici 3, altezza 1, minimo 003, massimo 012
interrogazioni eseguite: 5
```

L'indice risponde con la vista inordine `["003", "007", "012"]` e lascia alla
raccolta del registro l'ordine `["007", "012", "003"]`. Con argomenti non
ammessi - per esempio `intervallo 007 003`, con estremi invertiti - il
programma presenta la guida e termina senza costruire l'indice.

## Differenze rispetto alla fotografia U16

I file U1-U16 restano invariati; la tappa U17 aggiunge i due moduli
dell'indice, il punto di avvio, la suite e i tre documenti di
`documentazione/unita-17/`. La regressione verificata riguarda i contratti
mantenuti: modello U14, persistenza U12, tariffe U3/U5, ordine della raccolta
e coda U16 non cambiano firma né comportamento, e la suite U5-U16 supera per
intero. I limiti dichiarati: l'indice rappresenta la fotografia del momento
della costruzione e ogni modifica del registro richiede una nuova
costruzione; la struttura ad albero del capitolo PY-33 è riprodotta nel
progetto con chiavi stringa per mantenere la fotografia autonoma, e i
conteggi dei nodi esaminati non includono il costo dei confronti fra testi.
