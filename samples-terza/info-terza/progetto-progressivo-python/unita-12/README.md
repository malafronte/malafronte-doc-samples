# Raccolta progressiva di programmi — fotografia U12

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 12**: conserva i programmi U1-U11 e aggiunge persistenza, gestione
degli errori e riproducibilità del registro, con moduli separati per dominio,
persistenza e interazione. È il riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografia precedente:
[`../unita-11/`](../unita-11/).

## Traguardi della tappa

- archivio JSON canonico con `versione_schema` intero, UTF-8 senza BOM, e
  esportazione CSV di consultazione;
- caricamento **tutto valido oppure nessun archivio**, con esiti distinti per
  assente, sintassi, struttura e dominio;
- salvataggio che preserva il file precedente nei byte se scrittura o
  sostituzione falliscono, e nessun falso messaggio di successo;
- CLI minima con modifiche pendenti, salvataggio esplicito, uscita e EOF
  gestiti esplicitamente;
- moduli separati: `registro_dominio.py`, `registro_persistenza.py`,
  `registro_cli.py`, senza import ciclici né effetti all'import.

## Struttura

```text
unita-12/
├── programmi/
│   ├── ... programmi U1-U11 invariati ...
│   ├── registro_dominio.py        # schema, validazione, operazioni
│   ├── registro_persistenza.py    # JSON, salvataggio sicuro, CSV
│   ├── registro_cli.py            # interazione a riga di comando
│   └── test_persistenza_u12.py    # suite della tappa
├── dati/unita-12/
│   ├── archivio_canonico.json     # 007/450, 012/0, 003/1200 centesimi
│   ├── archivio_vuoto.json
│   ├── archivio_sintassi_corrotta.json
│   ├── archivio_struttura_invalida.json
│   ├── archivio_versione_booleana.json
│   ├── archivio_dominio_invalido.json
│   ├── archivio_duplicati.json
│   └── archivio_campo_extra.json
├── risultati/ (unita-09, unita-11 invariati)
├── documentazione/
│   ├── unita-01/ ... unita-11/ (documenti invariati)
│   └── unita-12/
│       ├── schema-e-dati.md
│       ├── errori-e-recupero.md
│       └── riproducibilita.md
├── README.md, pyproject.toml, uv.lock, .python-version, .gitignore
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen                                # ricostruisce .venv/ dal lock
uv run pytest -q                                # suite cumulativa U5-U12
uv run pytest -q programmi/test_persistenza_u12.py
Copy-Item dati/unita-12/archivio_canonico.json dati/unita-12/archivio.json
uv run python programmi/registro_cli.py
```

## Sessioni reali

Esecuzione verificata su Windows 11, CPython 3.14.7, uv 0.12.15, pytest 9.1.1.
Suite cumulativa:

```text
> uv run --frozen pytest -q
........................................................................ [ 58%]
...................................................                      [100%]
123 passed in 0.37s
```

**123 test**: 99 delle tappe U5-U11 più 24 della tappa U12 — i casi
PU12-01-PU12-10 (compreso il secondo guasto), tre casi propri e dieci
regressioni della sessione CLI. Sessione CLI
reale, da `carica` a `esci`:

```text
> uv run python programmi/registro_cli.py
Comandi: carica, elenco, cerca, inserisci, aggiorna, elimina, salva, esporta, esci
registro> carica
Archivio caricato: 3 record.
registro> elenco
007 | locale | 4,50 euro (450 centesimi)
012 | nazionale | 0,00 euro (0 centesimi)
003 | locale | 12,00 euro (1200 centesimi)
locale: 2 preventivi, 16,50 euro
nazionale: 1 preventivi, 0,00 euro
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
registro> esporta
Esportazione CSV scritta in dati\unita-12\esportazione.csv.
registro> esci
Sessione terminata.
```

Comportamenti di confine verificati: la fine dell'input (EOF) su qualunque
punto di lettura termina la sessione con `Input terminato: le modifiche non
salvate restano solo in memoria.`; `esci` con modifiche pendenti chiede
conferma e con `n` prosegue; un'operazione rifiutata non rende pendente il
salvataggio.

La sessione inizia **non inizializzata**: prima di consultare, modificare,
salvare o esportare occorre eseguire `carica`. Un archivio assente avvia un
registro vuoto, senza scrivere; un primo caricamento invalido lascia la
sessione non inizializzata e non autorizza il salvataggio. Con modifiche
pendenti, `carica` rifiuta il ricaricamento: i record restano in memoria e
l'uscita continua a richiedere conferma. Dopo un salvataggio riuscito si può
ricaricare; dopo un guasto la protezione resta attiva.

## Differenze rispetto alla tappa precedente

- nuovi `programmi/registro_dominio.py`, `registro_persistenza.py` e
  `registro_cli.py`: dominio, persistenza e interazione con responsabilità
  distinte e dipendenze in una sola direzione;
- nuovo `programmi/test_persistenza_u12.py` con 24 test, compresi i guasti
  deterministici di scrittura e sostituzione, i riavvii e le sessioni CLI;
- nuova cartella `dati/unita-12/` con le fixture sintetiche discriminanti;
- nuova `documentazione/unita-12/` con schema, errori e riproducibilità;
- `.gitignore` esclude i file di lavoro della sessione CLI.

I programmi delle tappe precedenti restano **invariati**: `spedizione_u5.py`
conserva la CLI tariffaria U5 e le funzioni già verificate, che il dominio del
registro riunisce senza cambiarne i contratti. La suite cumulativa è la prova
della regressione U5-U11.

## Limiti del riferimento

- Nessuna classe, dataclass, `pickle`, database, GUI né framework CLI: la
  consegna U12 li esclude e il record resta un dizionario.
- Il CSV di consultazione non è reversibile verso il documento canonico e non
  sostituisce il JSON.
- La concorrenza di più processi sullo stesso archivio non è gestita.
- Un errore di lettura diverso dall'assenza del file non viene classificato:
  la politica delle classi di errore è descritta in
  [`errori-e-recupero.md`](documentazione/unita-12/errori-e-recupero.md).

## Mappa delle prova

| Prova | Come si verifica | Atteso |
|---|---|---|
| PU12-01 | `uv run pytest -q programmi/test_persistenza_u12.py` | Vuoto valido distinto da assente e corrotto |
| PU12-02-PU12-03 | stesso comando | `007` nel round-trip, `007` ≠ `7`, zero ammesso e presentato `0,00` |
| PU12-04-PU12-05 | stesso comando | Rifiuti con diagnosi su campo e valore, nessun effetto parziale |
| PU12-06-PU12-07 | stesso comando | Sintassi con posizione distinta da struttura |
| PU12-08 | stesso comando | Guasti di scrittura e sostituzione: byte invariati, temporaneo eliminato |
| PU12-09 | stesso comando | Riavvio equivalente dopo salvataggio riuscito |
| PU12-10 | `uv run pytest -q` | Aggregati e viste coerenti; 123 test complessivi superati |
| Casi propri PR-1, PR-2, PR-3 | stesso comando | Versione booleana rifiutata, campo extra rifiutato, CSV senza BOM |
| Sessione CLI | `uv run python programmi/registro_cli.py` | Comandi, modifiche pendenti, conferma di uscita ed EOF come documentato |
| Regressioni CLI | `uv run pytest -q programmi/test_persistenza_u12.py -k cli` | Dieci test su inizializzazione, ricaricamento, guasti, EOF e vuoto intenzionale |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  — sezione *Unità 12 — Persistenza, errori e riproducibilità del registro*.
- Teoria di riferimento: cap. PY-18 — *Errori ed eccezioni*, PY-19 — *Percorsi
  e file di testo*, PY-20 — *CSV, JSON e record persistenti*, PY-22 —
  *Librerie e distribuzione*.
