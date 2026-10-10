# Raccolta progressiva di programmi - fotografia U15

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 15**: conserva i programmi U1-U14 e aggiunge i **criteri di
consultazione intercambiabili** — due politiche compatibili, un client
stabile e la scelta esplicita del componente nel punto di avvio — con la
suite condivisa e specifica, la documentazione delle scelte e il diagramma
UML. È il riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografia precedente:
[`../unita-14/`](../unita-14/).

## Traguardi della tappa

- **contratto comune** del criterio — `ammette(preventivo) -> bool` — con
  dati ammessi, risultato esatto, effetti, errori e invarianti dichiarati;
- **due componenti compatibili** — `PoliticaDestinazione` e `PoliticaSoglia`
  — usate dal medesimo client `seleziona_codici` senza modifiche;
- **client stabile**: lista nuova di codici nell'ordine, identità di dominio
  conservata, registro invariato, vuoto senza chiamate, `TypeError` su un
  risultato che non è esattamente `bool`;
- **scelta del componente nel punto di avvio** `consultazione_cli_u15.py`;
- **variante breve** `PoliticaSogliaEsclusiva`: terza implementazione
  integrata tramite il solo contratto (PU15-08);
- **prove condivise e specifiche** distinte, casi propri motivati, regressione
  U5-U14 verificata con la suite cumulativa.

## Struttura

```text
unita-15/
├── programmi/
│   ├── ... programmi U1-U14 invariati ...
│   ├── registro_consultazione_u15.py  # criteri intercambiabili e client
│   ├── consultazione_cli_u15.py       # punto di avvio: sceglie la concreta
│   └── test_consultazione_u15.py      # suite della tappa (14 test)
├── dati/unita-12/ (fixture invariate, dataset 007/012/003)
├── risultati/ (unita-09, unita-11 invariati)
├── documentazione/
│   ├── unita-01/ ... unita-14/ (documenti invariati)
│   └── unita-15/
│       ├── contratti-e-scelte.md      # promesse e confronto delle organizzazioni
│       ├── prove-e-regressione.md     # casi, diagnosi, variante breve
│       └── diagramma.puml             # UML delle classi e delle relazioni
├── README.md, pyproject.toml, uv.lock, .python-version, .gitignore
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen                                # ricostruisce .venv/ dal lock
uv run pytest -q                                # suite cumulativa U5-U15
uv run pytest -q programmi/test_consultazione_u15.py
Copy-Item dati/unita-12/archivio_canonico.json dati/unita-12/archivio.json
uv run python programmi/consultazione_cli_u15.py destinazione locale
uv run python programmi/consultazione_cli_u15.py soglia 500
```

## Sessioni reali

Esecuzione verificata su Windows 11, CPython 3.14.7, uv 0.12.15, pytest 9.1.1.
Suite cumulativa:

```text
> uv run --frozen pytest -q
........................................................................ [ 45%]
........................................................................ [ 90%]
...............                                                          [100%]
159 passed in 0.46s
```

**159 test**: 145 delle tappe U5-U14 più 14 della tappa U15 — le promesse
comuni e il vuoto su entrambe le implementazioni, i casi PU15-01-PU15-08
verificabili sul dominio, i tre casi propri motivati e la variante breve. Le
consultazioni reali con il dataset pubblicato:

```text
> uv run python programmi/consultazione_cli_u15.py destinazione locale
Criterio: destinazione = locale
Record consultati: 3
Codici ammessi: ['007', '003']
> uv run python programmi/consultazione_cli_u15.py soglia 500
Criterio: soglia >= 500 centesimi
Record consultati: 3
Codici ammessi: ['003']
> uv run python programmi/consultazione_cli_u15.py soglia-esclusiva 450
Criterio: soglia > 450 centesimi
Record consultati: 3
Codici ammessi: ['003']
```

Gli attesi coincidono con il caso PU15-04: locale → codici `[007, 003]`,
soglia ≥ 500 → `[003]`. La variante con soglia esclusiva 450 conferma il
confine diverso sulla stessa soglia. Con argomenti mancanti il programma
presenta la guida e termina senza effetti.

## Differenze rispetto alla tappa precedente

- nuovi `programmi/registro_consultazione_u15.py`, `consultazione_cli_u15.py`
  e `test_consultazione_u15.py`: la famiglia dei criteri, il client stabile,
  il punto di avvio e la suite con 14 test;
- nuova `documentazione/unita-15/` con contratti e scelte, prove e
  regressione, diagramma UML modificabile;
- nessun programma delle tappe precedenti è cambiato: modello U14,
  persistenza, CLI storiche e funzioni U5-U12 restano invariati e la suite
  cumulativa prova la regressione U5-U14.

## Limiti del riferimento

- La famiglia adottata è quella delle politiche di consultazione: gli
  esportatori in formati diversi sono un'alternativa equivalente, con attesi
  propri — il confronto è in `contratti-e-scelte.md`.
- La compatibilità dei criteri è strutturale e dichiarata dal contratto
  scritto: `ABC` e `Protocol` sono strumenti ammessi, non usati in questa
  realizzazione e confrontati nella documentazione.
- La variante breve è dimostrativa: un progetto reale aggiunge componenti
  quando servono, non per numero.
- La concorrenza di più sessioni sullo stesso archivio non è gestita: la
  consultazione legge e non scrive.

## Mappa delle prova

| Prova | Come si verifica | Atteso |
|---|---|---|
| PU15-01 | `uv run pytest -q programmi/test_consultazione_u15.py` | vuoto coerente, stato conservato, nessuna chiamata al criterio |
| PU15-02 | stesso comando | `007` conserva gli zeri; totale zero ammesso |
| PU15-03 | stesso comando | due implementazioni dalla stessa chiamata |
| PU15-04 | stesso comando | locale → `[007, 003]`; soglia ≥ 500 → `[003]` |
| PU15-05 | stesso comando | record, ordine e identità conservati; risultato protetto |
| PU15-06 | stesso comando | configurazione invalida: errore prima di ogni effetto |
| PU15-07 | stesso comando | guasto in scansione: stato conservato, nessun successo |
| PU15-08 | stesso comando | nuova implementazione dal solo contratto |
| Casi propri | stesso comando | confine incluso/escluso, difetti di tipo, ripetibilità |
| PU15-09 | `uv run pytest -q` | 159 test cumulativi superati, regressione U5-U14 |
| Consultazioni | `uv run python programmi/consultazione_cli_u15.py ...` | attesi PU15-04 e guida senza argomenti |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  - sezione *Unità 15 — Componenti intercambiabili nel registro*.
- Teoria di riferimento: OOP-05 - *Ereditarietà e sostituibilità*, OOP-06 -
  *Polimorfismo, duck typing e contratti*, OOP-07 - *Architettura e
  progettazione dei componenti*; laboratorio LAB-PY-U15.
