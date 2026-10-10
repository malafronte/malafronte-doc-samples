# Raccolta progressiva di programmi - fotografia U13

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 13**: conserva i programmi U1-U12 e aggiunge la variante a oggetti
del registro — la classe di sessione `RegistroPreventivi` — con la CLI di
raccordo, la suite della tappa e la documentazione della rifattorizzazione.
È il riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografia precedente:
[`../unita-12/`](../unita-12/).

## Traguardi della tappa

- classe con **stato utile di sessione** — i preventivi inseriti o caricati —
  e operazioni verificabili, con i soli costrutti dell'Unità 13;
- algoritmi delle tappe precedenti **riconoscibili**: la classe delega alle
  funzioni già verificate di `registro_dominio.py`, senza riscriverle;
- due istanze indipendenti, senza contenitori condivisi;
- conversioni esplicite `per_lista()` e `sostituisci_da_lista()`, con politica
  di copia dichiarata su entrambi i confini — tutto valido oppure nessun
  effetto;
- schema JSON canonico, CSV, tariffe, riepiloghi e politiche U12 invariati:
  la suite cumulativa è la prova della regressione.

## Struttura

```text
unita-13/
├── programmi/
│   ├── ... programmi U1-U12 invariati ...
│   ├── registro_oggetti_u13.py     # classe di sessione del registro
│   ├── registro_cli_u13.py         # CLI della variante a oggetti
│   └── test_oggetti_u13.py         # suite della tappa (11 test)
├── dati/unita-12/ (fixture invariate)
├── risultati/ (unita-09, unita-11 invariati)
├── documentazione/
│   ├── unita-01/ ... unita-12/ (documenti invariati)
│   └── unita-13/
│       ├── modello.md              # stato, invarianti, interfaccia, scelte
│       ├── confronto.md            # classe contro funzioni
│       └── prove.md                # casi, diagnosi, modifica breve
├── README.md, pyproject.toml, uv.lock, .python-version, .gitignore
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen                                # ricostruisce .venv/ dal lock
uv run pytest -q                                # suite cumulativa U5-U13
uv run pytest -q programmi/test_oggetti_u13.py
Copy-Item dati/unita-12/archivio_canonico.json dati/unita-12/archivio.json
uv run python programmi/registro_cli_u13.py
```

## Sessioni reali

Esecuzione verificata su Windows 11, CPython 3.14.7, uv 0.12.15, pytest 9.1.1.
Suite cumulativa:

```text
> uv run --frozen pytest -q
........................................................................ [ 53%]
..............................................................           [100%]
134 passed in 0.72s
```

**134 test**: 123 delle tappe U5-U12 più 11 della tappa U13 — i casi
PU13-01-PU13-08, i due casi propri PR-13-1 e PR-13-2 e la prova della modifica
breve. Sessione CLI reale, da `carica` a `esci`:

```text
> uv run python programmi/registro_cli_u13.py
Comandi: carica, elenco, cerca, inserisci, aggiorna, elimina, salva, esporta, esci
registro> carica
Archivio caricato: 3 record.
registro> elenco
007 | locale | 4,50 euro (450 centesimi)
012 | nazionale | 0,00 euro (0 centesimi)
003 | locale | 12,00 euro (1200 centesimi)
locale: 2 preventivi, 16,50 euro
nazionale: 1 preventivi, 0,00 euro
totale complessivo: 16,50 euro
registro> cerca
codice: 007
007 | locale | 4,50 euro (450 centesimi)
registro> inserisci
codice: 020
destinazione: nazionale
totale in centesimi: 75
Record inserito.
registro> salva
Archivio salvato.
registro> esci
Sessione terminata.
```

La CLI mantiene i comportamenti già verificati in U12 — inizializzazione con
`carica`, modifiche pendenti, salvataggio esplicito, EOF gestito — e presenta
in più il totale complessivo, aggiunto dalla modifica breve della tappa.

## Differenze rispetto alla tappa precedente

- nuovi `programmi/registro_oggetti_u13.py`, `registro_cli_u13.py` e
  `test_oggetti_u13.py`: la classe di sessione, il suo raccordo con CLI e
  persistenza e la suite con 11 test;
- nuova `documentazione/unita-13/` con modello, confronto e prove;
- nessun programma delle tappe precedenti è cambiato: `registro_dominio.py`
  resta la sede degli algoritmi e la suite cumulativa prova la regressione.

## Limiti del riferimento

- Costrutti dell'Unità 13 soltanto: nessuna proprietà, dataclass, eccezione di
  dominio né metodo speciale — appartengono all'Unità 14.
- Il singolo preventivo resta un dizionario: la classe `Preventivo` non è
  richiesta e non è la soluzione attesa, come ricorda la consegna U13.
- I rifiuti restano booleani dichiarati; la CLI non distingue le cause di un
  rifiuto con messaggi diversi, come già in U12.
- La concorrenza di più sessioni sullo stesso archivio non è gestita.

## Mappa delle prova

| Prova | Come si verifica | Atteso |
|---|---|---|
| PU13-01 | `uv run pytest -q programmi/test_oggetti_u13.py` | sessioni indipendenti, nessun contenitore condiviso |
| PU13-02 | stesso comando | `007` e `7` distinti in memoria, ricerca ed esportazione |
| PU13-03 | stesso comando | totale zero conservato nel round-trip e nel riepilogo |
| PU13-04 | stesso comando | rifiuti con esito `False` e stato interamente conservato |
| PU13-05 | stesso comando | salvataggio e ricarico con dati e ordine equivalenti |
| PU13-06 | stesso comando | archivio corrotto distinto; guasto con byte invariati e temporaneo eliminato |
| PU13-07 | stesso comando | riepilogo uguale a quello procedurale sul dataset noto |
| PU13-08 | stesso comando | snapshot e record consultati protetti dalle mutazioni esterne |
| PR-13-1, PR-13-2 | stesso comando | politica di copia verificata su ingresso e uscita |
| Modifica breve | stesso comando | `totale_complessivo_cent` derivato e senza effetti |
| Regressione | `uv run pytest -q` | 134 test complessivi superati |
| Sessione CLI | `uv run python programmi/registro_cli_u13.py` | comandi e presentazione come documentato, totale complessivo in elenco |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  - sezione *Unità 13 - Dalla soluzione procedurale agli oggetti*.
- Teoria di riferimento: OOP-01 - *Perché gli oggetti*, OOP-02 - *Classi,
  istanze e invarianti*; laboratorio LAB-PY-U13.
