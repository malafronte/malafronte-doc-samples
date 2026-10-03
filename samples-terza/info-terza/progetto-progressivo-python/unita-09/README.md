# Raccolta progressiva di programmi — fotografia U9

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 9**: conserva i programmi U1-U8 e aggiunge l'analisi del costo di
riepilogo e consultazione, con script, campioni reali e dossier. È il
riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografie vicine:
[`../unita-08/`](../unita-08/) e [`../unita-10/`](../unita-10/).

## Traguardi della tappa

- modello di costo per `riepilogo_per_destinazione` e `cerca_preventivo`, con
  dimensione `n`, operazioni contate, casi e spazio dichiarati;
- varianti strumentate che contano visite e confronti senza modificare le
  funzioni di produzione;
- campagna di misura con `time.perf_counter`, correttezza verificata prima del
  timer, campioni conservati e grafico con tabella equivalente;
- lettura critica dei risultati: distinzione fra provato e osservato.

## Struttura

```text
unita-09/
├── programmi/
│   ├── ... programmi U1-U8 invariati ...
│   ├── analisi_costi_u9.py        # conteggi, misure e campioni
│   ├── grafico_costi_u9.py        # grafico dai campioni
│   └── test_analisi_u9.py         # suite della tappa
├── risultati/unita-09/
│   ├── misure_u9.json             # campioni reali con metadati
│   └── costi_u9.png               # grafico equivalente alla tabella
├── documentazione/
│   ├── unita-01/ ... unita-08/ (documenti invariati)
│   └── unita-09/progetto/dossier-analisi.md
├── README.md, pyproject.toml, uv.lock, .python-version, .gitignore
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen                               # ricostruisce .venv/ dal lock
uv run pytest -q                               # suite cumulativa U5-U9
uv run python programmi/analisi_costi_u9.py    # rigenera i campioni
uv run python programmi/grafico_costi_u9.py    # rigenera il grafico
```

`matplotlib` è fra le dipendenze del progetto da questa tappa: serve al solo
grafico e non entra nelle funzioni di produzione.

## Sessioni reali

Esecuzione verificata su Windows 11, CPython 3.14.7, uv 0.12.15, pytest 9.1.1,
matplotlib 3.11. Suite cumulativa:

```text
> uv run pytest -q
........................................................................ [ 96%]
...                                                                      [100%]
75 passed in 0.09s
```

**75 test**: 66 delle tappe U5-U8 più 9 della tappa U9 — i casi PU9-01-PU9-08 e
il controllo della mediana. La campagna di misura produce:

```text
> uv run python programmi/analisi_costi_u9.py
Conteggi e misure - riepilogo e consultazione del registro
Ripetizioni: 5; chiamate per lotto: 20

operazione                                  n  op. contate    mediana s
riepilogo_per_destinazione                100          100  0.000013200
cerca_preventivo_ultima_posizione         100          100  0.000003830
cerca_preventivo_assente                  100          100  0.000003740
riepilogo_per_destinazione               1000         1000  0.000124795
cerca_preventivo_ultima_posizione        1000         1000  0.000034385
cerca_preventivo_assente                 1000         1000  0.000045365
riepilogo_per_destinazione              10000        10000  0.001334475
cerca_preventivo_ultima_posizione       10000        10000  0.000345025
cerca_preventivo_assente                10000        10000  0.000332090

Sequenza di 10 query sul registro di 10000 record: 1675 confronti complessivi
```

I campioni completi — con minimo, mediana, massimo e metadati — sono in
[`risultati/unita-09/misure_u9.json`](risultati/unita-09/misure_u9.json); la
tabella e la lettura critica sono nel
[`dossier-analisi.md`](documentazione/unita-09/progetto/dossier-analisi.md).

## Differenze rispetto alla tappa precedente

- nuovi `programmi/analisi_costi_u9.py` e `programmi/grafico_costi_u9.py`:
  strumentazione e misure **accanto** alle funzioni esistenti, che non
  cambiano;
- nuovo `programmi/test_analisi_u9.py` con 9 test sui conteggi e sui casi
  PU9;
- nuova cartella `risultati/unita-09/` con i campioni realmente misurati e il
  grafico; le durate appartengono alla postazione che le ha prodotte;
- `pyproject.toml` acquisisce `matplotlib` fra le dipendenze del progetto.

## Limiti del riferimento

- I tempi non sono valori di accettazione: cambiano con la macchina e non
  dimostrano da soli un ordine di crescita. Il dossier distingue ciò che è
  provato dai conteggi e ciò che è soltanto osservato.
- Il dataset è sintetico e deterministico, con codici di lunghezza `L = 6`:
  una lunghezza diversa cambierebbe il costo dei confronti e andrebbe
  dichiarata.
- Nessun archivio CSV/JSON del registro: la persistenza dei dati è della tappa
  U12. Il JSON qui contiene solo campioni di misura.
- Nessun file `riflessione.md`: è il documento personale dello studente.

## Mappa delle prova

| Prova | Come si verifica | Atteso |
|---|---|---|
| PU9-01-PU9-02 | `uv run pytest -q programmi/test_analisi_u9.py` | Riepilogo esatto; vuoto con zero visite e costo fisso separato |
| PU9-03-PU9-04 | stesso comando | Confronti 1/3/3 per `007`, `009`, assente; `7` distinto da `007` |
| PU9-05-PU9-07 | stesso comando | Stessa lunghezza con posizioni diverse; correttezza prima dei tempi; ripetizioni stabili |
| PU9-08 | stesso comando e `dossier-analisi.md` | Formule del modello verificate; nessuna deduzione asintotica dai soli tempi |
| Regressione U5-U8 | `uv run pytest -q` | 75 test complessivi superati |
| Campioni e grafico | `analisi_costi_u9.py` e `grafico_costi_u9.py` | JSON e PNG rigenerabili, tabella equivalente nel dossier |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  — sezione *Unità 9 — Analizzare il costo dei riepiloghi e delle consultazioni*.
- Teoria di riferimento: cap. PY-13 — *Complessità e analisi degli algoritmi*;
  guida *Misurare le prestazioni di Python* nelle guide `dev-tools`.
