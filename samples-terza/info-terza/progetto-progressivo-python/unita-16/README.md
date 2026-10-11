# Raccolta progressiva di programmi - fotografia U16

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 16**: conserva i programmi U1-U15 e aggiunge la **coda di richieste
di consultazione** - due rappresentazioni FIFO intercambiabili, richieste con
criterio, servizio di elaborazione separato dalla CLI e prove della tappa -
oltre alla documentazione delle scelte e al diagramma aggiornato. È il
riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografia precedente:
[`../unita-15/`](../unita-15/).

## Traguardi della tappa

- **richieste di consultazione** `RichiestaConsultazione` con codice e criterio,
  dove il criterio è lo stesso contratto U15 - `ammette(preventivo) -> bool` e
  `descrizione() -> str`;
- **coda FIFO con due rappresentazioni** - `CodaDequeU16` su
  `collections.deque` e `CodaConcatenataU16` sulla catena di nodi - usate dal
  medesimo servizio senza modifiche;
- **servizio di elaborazione** `ServizioConsultazione` separato dalla CLI:
  ordine di arrivo, dati del registro presi **nel momento dell'elaborazione**,
  politica di errore fronte, calcolo, estrazione e vuoto che restituisce `None`;
- **punto di avvio** `coda_cli_u16.py` che sceglie la rappresentazione della
  coda alla luce del sole e accoda le richieste nell'ordine della riga di
  comando;
- **conservazione del registro**: la consultazione non modifica dati, ordine e
  schema dell'archivio; i codici conservano gli zeri significativi;
- **prove** dei casi PU16-01-PU16-09 più tre casi propri motivati, con
  regressione U5-U15 verificata dalla suite cumulativa.

## Struttura

```text
unita-16/
├── programmi/
│   ├── ... programmi U1-U15 invariati ...
│   ├── coda_richieste_u16.py      # richieste, due code FIFO, servizio
│   ├── coda_cli_u16.py            # punto di avvio: sceglie la rappresentazione
│   └── test_coda_richieste_u16.py # suite della tappa (18 test)
├── dati/unita-12/ (fixture invariate, dataset 007/012/003)
├── risultati/ (unita-09, unita-11 invariati)
├── documentazione/
│   ├── unita-01/ ... unita-15/ (documenti invariati)
│   └── unita-16/
│       ├── contratti-e-scelta-struttura.md  # contratti e scelta della coda
│       ├── prove-e-regressione.md           # casi, diagnosi, casi propri
│       └── diagramma.puml                   # UML aggiornato con la coda
└── README.md, pyproject.toml, uv.lock, .python-version, .gitignore
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen                                # ricostruisce .venv/ dal lock
uv run pytest -q                                # suite cumulativa U5-U16
uv run pytest -q programmi/test_coda_richieste_u16.py
Copy-Item dati/unita-12/archivio_canonico.json dati/unita-12/archivio.json
uv run python programmi/coda_cli_u16.py destinazione locale soglia 500 soglia 0
uv run python programmi/coda_cli_u16.py concatenata destinazione locale soglia 500 soglia 0
```

## Sessioni reali

Esecuzione verificata su Windows 11, CPython 3.14.7, uv 0.12.15, pytest 9.1.1.
Suite cumulativa:

```text
> uv run --frozen pytest -q
........................................................................ [ 39%]
........................................................................ [ 79%]
......................................                                   [100%]
182 passed in 0.82s
```

**182 test**: 164 delle tappe U5-U15 più 18 della tappa U16 - i casi
PU16-01-PU16-09 su entrambe le rappresentazioni, i tre casi propri motivati e
la politica di errore fronte, calcolo, estrazione. Le elaborazioni reali con
il dataset pubblicato, identiche con `deque` e con la coda concatenata:

```text
> uv run --frozen python programmi/coda_cli_u16.py destinazione locale soglia 500 soglia 0
R01 [destinazione = locale] -> [007, 003]
R02 [soglia >= 500 centesimi] -> [003]
R03 [soglia >= 0 centesimi] -> [007, 012, 003]
richieste elaborate: 3, pendenti: 0
```

## Differenze rispetto alla fotografia U15

I file U1-U15 restano invariati; la tappa U16 aggiunge i due moduli della coda,
il punto di avvio, la suite e i tre documenti di `documentazione/unita-16/`.
La regressione verificata riguarda i contratti mantenuti: `seleziona_codici` e
i criteri U15 non cambiano firma né comportamento, e la suite U5-U15 supera per
intero. I limiti dichiarati: le richieste pendenti sono stato in memoria, la
persistenza della coda è un'estensione con schema separato, e la coda
concatenata didattica duplica nel progetto i meccanismi già spiegati nel
capitolo PY-23 per mantenere la fotografia autonoma.
