# Raccolta progressiva di programmi — fotografia U5

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 5**: conserva i programmi U1-U4 e aggiunge il preventivo di
spedizione in funzioni pure, la sua suite di test e le operazioni sui
preventivi. È il riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso: una possibile realizzazione completa, non la cronologia
che ogni studente deve costruire con i propri commit.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografie vicine:
[`../unita-04/`](../unita-04/) e [`../unita-06/`](../unita-06/).

## Traguardi della tappa

- decomposizione del preventivo in cinque funzioni pure con contratti scritti;
- CLI con `main` e guardia di avvio: import del modulo senza interazione;
- suite di test sui casi pubblici SP01-SP22 e SP-L01-SP-L06;
- operazioni sulle collezioni di preventivi con effetti dichiarati:
  registrazione in posto, anteprima con lista nuova, riepilogo con tupla.

## Struttura

```text
unita-05/
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
├── uv.lock
├── programmi/
│   ├── 01_hello.py ... 03_messaggio_multiriga.py
│   ├── trasferimento_dati.py
│   ├── preventivo_spedizione.py
│   ├── indovina_numero.py
│   ├── spedizione_u5.py
│   └── test_spedizione_u5.py
└── documentazione/
    ├── unita-01/ ... unita-04/ (documenti delle tappe precedenti)
    └── unita-05/progetto/
        ├── contratti.md
        ├── casi-di-prova.md
        └── diagnosi.md
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen                       # ricostruisce .venv/ dal lock (pytest incluso)
uv run python --version                # Python 3.14.7
uv run python programmi/spedizione_u5.py           # CLI del preventivo
uv run pytest -q programmi/test_spedizione_u5.py   # suite della tappa
```

## Sessioni reali

Esecuzione verificata su Windows 11 con CPython 3.14.7, uv 0.12.15 e pytest
9.1.1. La suite dichiara **30 test**, tutti scoperti e superati:

```text
> uv run pytest -q programmi/test_spedizione_u5.py
..............................                                           [100%]
30 passed in 0.06s
```

Mappa dei 30 test: 21 sui casi SP (SP01-SP18, SP20-SP22), 6 sui casi SP-L, 3
casi propri. Il caso SP19 riguarda la conversione della CLI e si verifica con
la sessione manuale riportata in
[`documentazione/unita-05/progetto/casi-di-prova.md`](documentazione/unita-05/progetto/casi-di-prova.md),
insieme alle dieci sessioni CLI richieste e agli attesi completi.

Un processo che importa il modulo non avvia l'interazione:

```text
> uv run python -c "import sys; sys.path.insert(0, 'programmi'); import spedizione_u5; print('import riuscito senza interazione')"
import riuscito senza interazione
```

## Differenze rispetto alla tappa precedente

- nuovo `programmi/spedizione_u5.py`: le cinque funzioni pure di tariffazione,
  `main` con guardia di avvio e le tre operazioni M26-M27 sulle liste di
  importi;
- nuovo `programmi/test_spedizione_u5.py`: 30 test espliciti senza
  parametrizzazione;
- nuova `documentazione/unita-05/progetto/` con contratti, casi di prova e la
  diagnosi guidata;
- `pyproject.toml` acquisisce `pytest` fra le dipendenze di sviluppo e
  `uv.lock` è stato rigenerato e verificato con `uv sync --frozen`;
- il programma monolitico `preventivo_spedizione.py` della tappa U3 resta
  presente e invariato, come riferimento del prima/dopo.

## Limiti del riferimento

- Le cinque funzioni di logica non gestiscono input non conformi: la
  validazione produce i messaggi di errore ma le funzioni di calcolo assumono
  dati ammessi, come dichiarato nei contratti. `try/except` non è richiesto.
- Nessuna parametrizzazione, fixture complessa o misura di copertura: la
  consegna U5 non li richiede e la suite resta leggibile.
- Non è presente `documentazione/unita-05/progetto/riflessione.md`: è la
  riflessione personale dello studente. La
  [`diagnosi.md`](documentazione/unita-05/progetto/diagnosi.md) non racconta un
  errore personale: documenta un difetto iniettato in una copia temporanea e
  gli esiti realmente osservati della suite.

## Mappa delle prove

| Prova | Come si verifica | Atteso |
|---|---|---|
| Casi SP01-SP18, SP20-SP22 | `uv run pytest -q programmi/test_spedizione_u5.py` | 21 test verdi sulle funzioni |
| Casi SP-L01-SP-L06 | stessa suite | 6 test verdi, effetti e identità come da contratto |
| Casi propri PR-1, PR-2, PR-3 | stessa suite | 3 test verdi, incluso il caso discriminante della diagnosi |
| Sessioni CLI | `uv run python programmi/spedizione_u5.py` per SP03, SP04, SP08, SP12, SP15-SP20 | Output uguali agli attesi, nessuna riga di costo sui rifiuti |
| Import senza interazione | processo che importa il modulo | Nessuna domanda e nessuna stampa |
| Diagnosi del difetto | copia temporanea con il supplemento omesso | 6 fallimenti su 30, poi 30 verdi dopo la correzione |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  — sezione *Unità 5 — Funzioni e test per il preventivo di spedizione*.
- Teoria di riferimento: cap. PY-07, PY-08 e PY-09; guida a pytest nelle guide
  `dev-tools` del sito.
- Confronto prima/dopo: `programmi/preventivo_spedizione.py` (U3,
  monolitico) e `programmi/spedizione_u5.py` (U5, a funzioni).
