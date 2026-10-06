# Unità 13 — sorgenti Python d'esempio (cap. OOP-01 e OOP-02)

Sorgenti d'esempio dell'**Unità 13** del corso di informatica della terza:
dalla soluzione procedurale agli oggetti. Contengono la prima classe del corso,
gli attributi e `self`, le istanze indipendenti e gli alias, gli invarianti con
rifiuto ed errore, il contatore con capacità, la classe `Articolo` e la variante
a oggetti del magazzino persistente del cap. PY-20.

Come per le altre unità, questi sorgenti non si distribuiscono come download dal
sito: le pagine li mostrano con `RemoteCode` e citano il percorso di questo
repository.

## Mappa dei file

### `esempi/`

- `esempi_concettuali_u13.py` — **esempi concettuali autonomi**, in quattro
  sezioni indipendenti: convertitore centimetri → millimetri (OOP-01, sez. D–F),
  classe `Contatore` (OOP-02, sez. A–F), classe `Limiti` con invariante e
  aggiornamento coerente (OOP-02, sez. G), classe `Misura` con proiezione dei
  dati e round-trip CSV/JSON (OOP-02, sez. J).
- `contatore_procedurale_u13.py` — **contatore di eventi** in forma procedurale:
  record e funzioni con invariante `valore >= 0` (OOP-01, sez. A–B e G).
- `istanze_alias_self_u13.py` — **varianti didattiche complete** su attributi,
  nomi locali, `self`, alias e copie (OOP-02, sez. C–F): chiamata legata ed
  esplicita, metodo difettoso che aggiorna un locale, metodo che riassegna
  `self`, alias e copia di lista.
- `contatore_capacita_u13.py` — **contatore con capacità**: versione procedurale,
  classe `ContatoreCapacita` e sequenza canonica verificata su entrambe
  (OOP-02, sez. H).
- `articolo_u13.py` — classe `Articolo` e validazione condivisa dello schema
  (OOP-02, sez. J).
- `dominio_magazzino_u13.py` — operazioni esterne su una lista di `Articolo`:
  ricerca, inserimento, aggiornamento, eliminazione, riepilogo e conversioni
  testuali.
- `persistenza_magazzino_u13.py` — caricamento e salvataggio CSV con le
  politiche U12 conservate.
- `cli_magazzino_u13.py` — menu e stato di sessione, con gli stessi comandi e
  gli stessi messaggi della versione procedurale.
- `conversioni_json_u13.py` — proiezione JSON esplicita del magazzino con
  `versione_schema` e ricostruzione validata.

### `test/`

Suite `pytest` che deriva gli attesi dalle specifiche: `CONC-01…CONC-08` sugli
esempi concettuali, `OGG-01…OGG-12` sul contatore con capacità, `ART-01…ART-05`
su `Articolo`, `MAGO-01…MAGO-12` sul magazzino e sulle conversioni.

### `dati/`

- `magazzino_canonico.csv` — i due articoli canonici del capitolo;
- `fixture-invalidi/` — archivi malformati per le diagnosi manuali e per le
  prove di caricamento: intestazione errata, codici duplicati, intero non
  convertibile, BOM iniziale, byte non UTF-8.

### `esercizi/`

- `soluzioni_u13.py` — soluzioni eseguibili della banca di base.
- `soluzioni_algoritmica_u13.py` — soluzioni eseguibili della famiglia
  algoritmica.

### `laboratorio/starter/`

Starter del laboratorio **LAB-PY-U13**: versione procedurale funzionante,
cornice di esecuzione dei casi pubblici e istruzioni. **Non** contiene la classe
risolutiva né una suite completata.

## Ambiente e comandi

CPython 3.14 sul computer, da questa directory.

```powershell
uv sync --group dev
uv run pytest -q
uv run ruff check .
uv run python esempi/esempi_concettuali_u13.py
```

La suite non richiede modifiche a `sys.path`: `pyproject.toml` dichiara i
percorsi dei moduli per `pytest`. I moduli delle soluzioni dipendono dalla
classe `Articolo`, che vive in `esempi/`: per eseguirli direttamente si
dichiara la ricerca in quel percorso nella sessione di shell, senza toccare i
sorgenti.

```powershell
$env:PYTHONPATH = "esempi"
uv run python esercizi/soluzioni_u13.py
uv run python esercizi/soluzioni_algoritmica_u13.py
```

La dimostrazione del laboratorio si prova in
un **processo separato**, dalla sua directory:

```powershell
cd laboratorio/starter
python dimostrazione_depositi.py
```

## Note di lettura

- Gli esempi concettuali non importano dalle applicazioni complete: ciascuno è
  eseguibile con le sole definizioni del proprio punto della lezione.
- Le varianti **deliberatamente difettose** vivono soltanto in
  `istanze_alias_self_u13.py` e nei frammenti marcati dei test: non fanno parte
  dei programmi validi.
- `modifica_articolo` **muta l'istanza esistente**, mentre la versione U12
  sostituiva il record nella lista: la differenza di aliasing è dichiarata nel
  modulo di dominio e verificata dai test.
