# Raccolta progressiva di programmi — fotografia U11

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 11**: conserva i programmi U1-U10 e aggiunge il confronto fra
strategie di ordinamento, con esperimento, campioni e relazione. È il
riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografie vicine:
[`../unita-10/`](../unita-10/) e [`../unita-12/`](../unita-12/).

## Traguardi della tappa

- almeno due strategie di ordinamento sullo stesso criterio, una delle quali
  divide et impera: ordinamento per inserimento e MergeSort stabile;
- `fondi_ordinate`, `ordina_fusione` e la query sul **primo indice**
  `primo_indice_per_totale`, distinta dalla ricerca per codice che restituisce
  un record;
- esperimento con famiglie di input, seme riproducibile, copie indipendenti,
  parità verificata e preparazione separata dal costo delle query;
- scelta motivata e condizionata a input e uso, con `sorted` come riferimento.

## Struttura

```text
unita-11/
├── programmi/
│   ├── ... programmi U1-U10 invariati ...
│   ├── spedizione_u5.py              # acquisisce la sezione U11
│   ├── confronto_ordinamenti_u11.py  # esperimento e campioni
│   ├── grafico_ordinamenti_u11.py    # grafico dai campioni
│   └── test_ordinamenti_u11.py       # suite della tappa
├── risultati/
│   ├── unita-09/ (misure_u9.json, costi_u9.png)
│   └── unita-11/ (misure_u11.json, confronto_u11.png)
├── documentazione/
│   ├── unita-01/ ... unita-10/ (documenti invariati)
│   └── unita-11/relazione-confronto.md
├── README.md, pyproject.toml, uv.lock, .python-version, .gitignore
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen                                  # ricostruisce .venv/ dal lock
uv run pytest -q                                  # suite cumulativa U5-U11
uv run python programmi/confronto_ordinamenti_u11.py
uv run python programmi/grafico_ordinamenti_u11.py
```

## Sessioni reali

Esecuzione verificata su Windows 11, CPython 3.14.7, uv 0.12.15, pytest 9.1.1,
matplotlib 3.11. Suite cumulativa:

```text
> uv run pytest -q
........................................................................ [ 75%]
........................                                                 [100%]
96 passed in 0.12s
```

**96 test**: 86 delle tappe U5-U10 più 10 della tappa U11 — i casi
PU11-01-PU11-08 e due casi propri sulla fusione stabile e sul primo indice.
L'esperimento produce, fra le altre, queste mediane in millisecondi:

```text
famiglia              n procedimento      mediana s
inverso            5000 inserimento        2.762640
inverso            5000 fusione            0.014924
inverso            5000 sorted             0.000383
quasi_ordinato     5000 inserimento        0.001425
quasi_ordinato     5000 fusione            0.016376
pseudo_casuale     5000 inserimento        1.474705
pseudo_casuale     5000 fusione            0.019978
```

I campioni completi sono in
[`risultati/unita-11/misure_u11.json`](risultati/unita-11/misure_u11.json); la
lettura dei risultati, le tabelle complete e la scelta motivata sono nella
[`relazione-confronto.md`](documentazione/unita-11/relazione-confronto.md).

## Differenze rispetto alla tappa precedente

- `programmi/spedizione_u5.py` acquisisce la sezione «Strategie di ordinamento
  a confronto»: `fondi_ordinate`, `ordina_fusione`, `primo_indice_per_totale`;
- nuovi `programmi/confronto_ordinamenti_u11.py` e
  `programmi/grafico_ordinamenti_u11.py` per l'esperimento;
- nuovo `programmi/test_ordinamenti_u11.py` con 10 test;
- nuova cartella `risultati/unita-11/` e
  `documentazione/unita-11/relazione-confronto.md`.

## Limiti del riferimento

- Le due strategie sono stabili entrambe: il confronto è sulla robustezza e
  sui costi, non sulla stabilità. Una variante instabile — per esempio
  QuickSort — andrebbe confrontata anche su multinsieme e ordine relativo, con
  contratto esplicito: non è richiesta da questa consegna.
- I tempi non sono valori di accettazione e la relazione non propone una
  classifica universale: la scelta è condizionata a famiglia di input,
  dimensione e numero di consultazioni.
- Le funzioni del riferimento implementano i procedimenti studiati e non
  delegano a `sorted`, che resta un riferimento per il risultato.
- Nessun file `riflessione.md`: è il documento personale dello studente.

## Mappa delle prova

| Prova | Come si verifica | Atteso |
|---|---|---|
| PU11-01-PU11-04 | `uv run pytest -q programmi/test_ordinamenti_u11.py` | Vuoto, singolo record, marcatori stabili, ordine inverso |
| PU11-05-PU11-06 | stesso comando | Query ripetute sul primo indice; vista non aggiornata dopo le modifiche |
| PU11-07-PU11-08 | stesso comando | `007` e `7` distinti; stesso risultato di `sorted` |
| Casi propri PR-1, PR-2 | stesso comando | Fusione stabile e input invariati; primo indice su totali tutti uguali |
| Parità fra strategie | `confronto_ordinamenti_u11.py` | Stesso ordine dei marcatori per inserimento, fusione e `sorted` |
| Regressione U5-U10 | `uv run pytest -q` | 96 test complessivi superati |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  — sezione *Unità 11 — Scelta e confronto delle strategie di ordinamento*.
- Teoria di riferimento: cap. PY-15 — *Divide et impera e confronto degli
  ordinamenti*; cap. PY-14 per le ricerche e il contratto del primo indice.
