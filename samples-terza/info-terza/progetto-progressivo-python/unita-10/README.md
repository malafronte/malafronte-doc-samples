# Raccolta progressiva di programmi — fotografia U10

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 10**: conserva i programmi U1-U9 e aggiunge le viste ordinate per la
consultazione del registro. È il riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografie vicine:
[`../unita-09/`](../unita-09/) e [`../unita-11/`](../unita-11/).

## Traguardi della tappa

- `vista_per_codice`, `vista_per_totale` e `cerca_per_codice` con liste nuove,
  record condivisi dichiarati e sorgente invariata;
- ordinamento per inserimento stabile, scelto e motivato, con `sorted` come
  oracolo e non come delega;
- ricerca dicotomica sulla vista per codice;
- analisi dei costi di preparazione, consultazione, `q` consultazioni e
  aggiornamento.

## Struttura

```text
unita-10/
├── programmi/
│   ├── ... programmi U1-U9 invariati ...
│   ├── spedizione_u5.py            # acquisisce la sezione U10
│   ├── test_spedizione_u5.py, test_totale_ricorsivo_u6.py,
│   │   test_sintesi_u7.py, test_registro_u8.py, test_analisi_u9.py
│   └── test_viste_u10.py           # suite della tappa
├── risultati/unita-09/             # campioni e grafico U9 invariati
├── documentazione/
│   ├── unita-01/ ... unita-09/ (documenti invariati)
│   └── unita-10/confronto-consultazioni.md
├── README.md, pyproject.toml, uv.lock, .python-version, .gitignore
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen        # ricostruisce .venv/ dal lock
uv run pytest -q        # suite cumulativa U5-U10
```

## Sessioni reali

Esecuzione verificata su Windows 11 con CPython 3.14.7 e pytest 9.1.1:

```text
> uv run pytest -q
........................................................................ [ 83%]
..............                                                           [100%]
86 passed in 0.10s
```

**86 test**: 75 delle tappe U5-U9 più 11 della tappa U10 — i casi
PU10-01-PU10-08, il confronto con `sorted` come oracolo e due casi propri. Il
dataset di riferimento ha codici `["007", "009", "012", "003", "011"]` e
totali `450, 1200, 450, 200, 450` centesimi: la vista per totale restituisce
`["003", "007", "012", "011", "009"]` — i tre record da 450 nell'ordine di
ingresso — e la vista per codice `["003", "007", "009", "011", "012"]`.

## Differenze rispetto alla tappa precedente

- `programmi/spedizione_u5.py` acquisisce la sezione «Viste ordinate»:
  `chiave_codice`, `chiave_totale`, `ordina_inserimento`, `vista_per_codice`,
  `vista_per_totale` e `cerca_per_codice`;
- nuovo `programmi/test_viste_u10.py` con 11 test, compresi stabilità sui
  marcatori, invarianza della sorgente e comportamento della vista non
  aggiornata;
- nuovo `documentazione/unita-10/confronto-consultazioni.md` con i costi di
  preparazione, consultazione e aggiornamento.

## Limiti del riferimento

- L'ordinamento per inserimento è una scelta motivata, non l'unica ammessa:
  qualunque ordinamento elementare studiato sarebbe accettabile se motivato e
  verificato. La varietà delle scelte è un esito desiderato.
- I record sono condivisi fra registro e vista: non ci sono copie profonde,
  come dichiarato nei contratti. Dopo una modifica ai dati la vista va
  ricostruita prima di essere usata per la ricerca dicotomica.
- I costi di questa tappa sono **conteggi**: l'esperimento comparativo fra
  procedimenti è della tappa U11. Nessun file `riflessione.md`, documento
  personale dello studente.

## Mappa delle prova

| Prova | Come si verifica | Atteso |
|---|---|---|
| PU10-01-PU10-04 | `uv run pytest -q programmi/test_viste_u10.py` | Vuoto, singolo record, ordine lessicografico, ricerca presente/assente |
| PU10-05-PU10-06 | stesso comando | Stabilità sui tre totali uguali, campi associati ai record |
| PU10-07-PU10-08 | stesso comando | Sorgente invariata; vista non aggiornata dopo l'aggiunta di un record |
| Oracolo `sorted` | stesso comando | Stessi ordini sui due criteri |
| Casi propri PR-1, PR-2 | stesso comando | Chiavi tutte uguali; mutazione del record condiviso |
| Regressione U5-U9 | `uv run pytest -q` | 86 test complessivi superati |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  — sezione *Unità 10 — Viste ordinate per la consultazione del registro*.
- Teoria di riferimento: cap. PY-14 — *Ricerche e ordinamenti elementari*;
  cap. PY-13 per la parte sui costi.
