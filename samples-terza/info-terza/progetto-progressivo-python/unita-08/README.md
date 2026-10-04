# Raccolta progressiva di programmi — fotografia U8

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 8**: conserva i programmi U1-U7 e aggiunge il registro di record con
i riepiloghi per destinazione. È il riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografie vicine:
[`../unita-07/`](../unita-07/) e [`../unita-09/`](../unita-09/).

## Traguardi della tappa

- record `{"codice", "destinazione", "totale_cent"}` da liste parallele, con
  codici stringa univoci e zeri iniziali conservati;
- `crea_registro`, `riepilogo_per_destinazione` e `cerca_preventivo` con
  effetti, alias e casi vuoti dichiarati;
- rifiuto di disallineamenti, codici vuoti e duplicati senza risultati
  parziali;
- regressione U5-U7 verificata insieme alle nuove operazioni.

## Struttura

```text
unita-08/
├── programmi/
│   ├── ... programmi U1-U7 invariati ...
│   ├── spedizione_u5.py            # acquisisce la sezione U8
│   ├── test_spedizione_u5.py       # suite U5 invariata
│   ├── test_totale_ricorsivo_u6.py # suite U6 invariata
│   ├── test_sintesi_u7.py          # suite U7 invariata
│   └── test_registro_u8.py         # suite della tappa
├── documentazione/
│   ├── unita-01/ ... unita-07/ (documenti invariati)
│   └── unita-08/progetto/contratti.md
├── README.md, pyproject.toml, uv.lock, .python-version, .gitignore
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen        # ricostruisce .venv/ dal lock
uv run pytest -q        # suite cumulativa U5-U8
```

## Sessioni reali

Esecuzione verificata su Windows 11 con CPython 3.14.7 e pytest 9.1.1:

```text
> uv run --frozen pytest -q
.....................................................................    [100%]
69 passed in 0.13s
```

La suite cumulativa scopre **69 test**: 30 U5, 12 U6, 15 U7 e 12 U8 — i casi
PU8-01-PU8-09 più tre casi propri. Il dataset canonico della tappa è codici
`["007", "008", "009"]` e coppie `[("locale", 300), ("nazionale", 900),
("locale", 500)]`: il riepilogo restituisce `locale` con conteggio 2 e totale
800 e `nazionale` con conteggio 1 e totale 900, per 1700 centesimi complessivi.

## Differenze rispetto alla tappa precedente

- `programmi/spedizione_u5.py` acquisisce la sezione «Registro di record»:
  `crea_registro`, `riepilogo_per_destinazione` e `cerca_preventivo`;
- nuovo `programmi/test_registro_u8.py` con 12 test, compresi alias,
  indipendenza dei risultati e preparazione dalle spedizioni U5;
- nuova `documentazione/unita-08/progetto/contratti.md` con lo schema dei
  campi e le motivazioni delle scelte.

## Limiti del riferimento

- Il record è un dizionario: le classi e le dataclass appartengono al progetto
  orientato agli oggetti e non sono anticipate.
- La ricerca è lineare e non costruisce indici per codice: l'indice è
  un'estensione successiva e il problema U8 non richiede analisi di complessità.
- Non ci sono menu CRUD né file di dati: appartengono alla tappa U12.
- Nessun file `riflessione.md`: è il documento personale dello studente.

## Mappa delle prove

| Prova | Come si verifica | Atteso |
|---|---|---|
| PU8-01-PU8-03 | `uv run pytest -q programmi/test_registro_u8.py` | Migrazione, riepilogo e totale canonico 1700 |
| PU8-04 rifiuti | stesso comando | `None` e argomenti conservati |
| PU8-05-PU8-06 | stesso comando | Ricerca `007`/`009`/`7`/`X99`, totali uguali e zero lecito |
| PU8-07-PU8-08 | stesso comando | Record e gruppi indipendenti; alias della ricerca su fixture separata |
| PU8-09 raccordo | stesso comando | Euro `[3, 9, 5]`, centesimi `[300, 900, 500]`, coerenza con U6 e U7 |
| Regressione U5-U7 | `uv run pytest -q` | 69 test complessivi superati, comprese le tre regressioni del sopra-media |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  — sezione *Unità 8 — Registro e riepiloghi dei preventivi*.
- Teoria di riferimento: cap. PY-12 — *Dizionari e insiemi*; cap. PY-09 per la
  pratica di test.
