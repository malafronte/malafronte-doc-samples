# Starter — Laboratorio dei frattali (Unità 20)

Materiale iniziale del progetto autonomo: package `frattali/` con
infrastruttura fornita e operazioni da completare, quattro configurazioni
JSON valide, casi pubblici di accettazione e protocollo dei requisiti.
I kernel preparatori dei capitoli PY-37–PY-42 restano consultabili per
confronto; trasferimento, integrazione, variante personale e spiegazione
sono lavoro autonomo.

## Stato iniziale

Il comando di stato elenca le operazioni fornite e quelle da completare:

```powershell
uv sync --frozen
uv run python -m frattali stato
```

Esito iniziale previsto: le operazioni di dominio di base, I/O PNG,
finestra minima e ambiente sono fornite; le operazioni dei generatori,
delle coordinate, delle palette, della matrice, dello stato cooperativo,
della configurazione e della persistenza sono da completare e i casi
pubblici corrispondenti falliscono con `NotImplementedError`.

## Comandi di verifica

Dalla cartella `starter-progetto-frattali`:

```powershell
uv sync --frozen
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
uv run python -m frattali stato
uv run python -m tkinter
```

Il comando `genera` resta incompleto finché le tappe non sono svolte e
termina con un errore motivato invece di un prodotto parziale:

```powershell
uv run python -m frattali genera --config configurazioni/mandelbrot.json --png mandelbrot.png
```

La funzione `immagine_da_configurazione` in `frattali/__main__.py` è da
completare nelle tappe FR-M5/FR-M7: carica e valida il JSON, sceglie il
generatore e restituisce l'immagine completa. Lo smistamento `main`, il
comando di stato e il collegamento fra immagine e salvataggio sono forniti.
I tre test di `tests/test_comandi_forniti.py` verificano questa infrastruttura
con sostituti, senza fornire gli algoritmi assegnati. L'esito iniziale
dell'intera suite è **6 casi superati e 14 falliti** con `NotImplementedError`.

## Struttura e lavoro previsto

| Percorso | Stato | Lavoro dello studente |
|---|---|---|
| `frattali/__init__.py` | Fornito | Conservare l'inizializzazione senza effetti grafici |
| `frattali/__main__.py` | In parte fornito | Completare `immagine_da_configurazione` in FR-M5/FR-M7; usare lo smistamento e l'I/O PNG forniti |
| `frattali/dominio.py` (eccezioni, vista, immagine) | Fornito | Completare parametri delle famiglie e configurazione |
| `frattali/algoritmi/` | Da completare | Kernel geometrici e numerici con la convenzione unica |
| `frattali/rendering/coordinate.py`, `colori.py` | Da completare | Campionamento, zoom, palette e legenda |
| `frattali/rendering/immagini.py` (I/O PNG) | Fornito | Completare matrice, statistiche e traduzione in RGB |
| `frattali/rendering/stato.py` | Da completare | Fotografia, stati, blocchi e annullamento |
| `frattali/persistenza.py` | Da completare | Schema v1, round-trip, atomicità e preservazione |
| `frattali/interfaccia.py` (finestra minima) | Fornita | Completare generazione, annullamento, zoom ed esportazione |
| `configurazioni/` | Fornite e valide | Usarle per le prove, aggiungerne di motivate |
| `tests/test_pubblici.py` (FR-A01–FR-A15) | Forniti | Farli passare, aggiungere almeno tre casi propri motivati |
| `tests/test_comandi_forniti.py` | Forniti | Conservare le regressioni dell'infrastruttura CLI |
| `documentazione/protocollo-requisiti.md` | Fornito | Compilarlo durante il lavoro con stati ed evidenze |

Il contributo dello starter (finestra minima, I/O PNG, valori di base,
test pubblici) è dichiarato nella rubrica della consegna e non sostituisce
progettazione, integrazione e spiegazione personale.

## Ambiente

CPython `>=3.14` con `pillow`, `pytest` e `ruff` nel gruppo di sviluppo.
La suite non apre finestre grafiche; la finestra si prova con
l'interprete effettivo del progetto e con il collaudo manuale descritto
nella consegna.
