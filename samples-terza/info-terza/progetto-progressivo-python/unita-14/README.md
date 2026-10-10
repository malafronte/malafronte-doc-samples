# Raccolta progressiva di programmi - fotografia U14

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 14**: conserva i programmi U1-U13 e aggiunge il modello robusto del
registro — il valore `Preventivo` frozen, la raccolta `RegistroPreventivi`
con eccezioni di dominio e dati derivati — con la CLI di confine, la suite
della tappa e la documentazione delle scelte. È il riferimento di confronto
della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README. Fotografia precedente:
[`../unita-13/`](../unita-13/).

## Traguardi della tappa

- **valore immutabile** `Preventivo`: dataclass frozen con validazione alla
  costruzione, uguaglianza per contenuto, `repr` leggibile;
- **raccolta responsabile**: unicità dei codici, ordine conservato,
  aggiornamenti che sostituiscono l'intero valore — nessuna modifica parziale;
- **dati derivati** `numero` e `totale_complessivo_cent` come proprietà, mai
  campi duplicati;
- **eccezioni di dominio** `DatoNonAmmesso`, `CodiceDuplicato`,
  `CodiceAssente`, presentate dalla CLI al proprio confine, senza `except`
  indiscriminati;
- **proiezioni esplicite** verso CSV e JSON: nessuna esportazione opaca degli
  attributi, nessun `pickle`; politiche di persistenza U12 invariate;
- snapshot protetti — tuple di valori frozen — ed effetti degli alias
  dichiarati e verificati.

## Struttura

```text
unita-14/
├── programmi/
│   ├── ... programmi U1-U13 invariati ...
│   ├── registro_modello_u14.py     # valore frozen e raccolta responsabile
│   ├── registro_cli_u14.py         # CLI: confine delle eccezioni di dominio
│   └── test_modello_u14.py         # suite della tappa (11 test)
├── dati/unita-12/ (fixture invariate)
├── risultati/ (unita-09, unita-11 invariati)
├── documentazione/
│   ├── unita-01/ ... unita-13/ (documenti invariati)
│   └── unita-14/
│       ├── contratti-e-rappresentazione.md
│       ├── componenti-e-conversioni.md
│       └── prove-e-revisione.md
├── README.md, pyproject.toml, uv.lock, .python-version, .gitignore
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen                                # ricostruisce .venv/ dal lock
uv run pytest -q                                # suite cumulativa U5-U14
uv run pytest -q programmi/test_modello_u14.py
Copy-Item dati/unita-12/archivio_canonico.json dati/unita-12/archivio.json
uv run python programmi/registro_cli_u14.py
```

## Sessioni reali

Esecuzione verificata su Windows 11, CPython 3.14.7, uv 0.12.15, pytest 9.1.1.
Suite cumulativa:

```text
> uv run --frozen pytest -q
........................................................................ [ 49%]
........................................................................ [ 99%]
.                                                                        [100%]
145 passed in 0.49s
```

**145 test**: 134 delle tappe U5-U13 più 11 della tappa U14 — i casi
PU14-01-PU14-08, i due casi propri PR-14-1 e PR-14-2 e la prova della modifica
breve. Sessione CLI reale sui rifiuti di dominio:

```text
> uv run python programmi/registro_cli_u14.py
Comandi: carica, elenco, cerca, inserisci, aggiorna, elimina, salva, esporta, esci
registro> carica
Archivio caricato: 3 record.
registro> inserisci
codice: 007
destinazione: locale
totale in centesimi: 900
Inserimento rifiutato: codice duplicato: '007'
registro> elenco
007 | locale | 4,50 euro (450 centesimi)
012 | nazionale | 0,00 euro (0 centesimi)
003 | locale | 12,00 euro (1200 centesimi)
locale: 2 preventivi, 16,50 euro
nazionale: 1 preventivi, 0,00 euro
totale complessivo: 16,50 euro
registro> aggiorna
codice: 007
destinazione: locale
totale in centesimi: -5
Aggiornamento rifiutato: dominio: totale_cent non può essere negativo: -5
registro> esci
Sessione terminata.
```

Le due operazioni rifiutate non rendono pendente il salvataggio: `esci`
termina senza chiedere conferma. Le diagnosi distinguono il vincolo della
raccolta dal dominio del valore, come richiesto dai contratti.

## Differenze rispetto alla tappa precedente

- nuovi `programmi/registro_modello_u14.py`, `registro_cli_u14.py` e
  `test_modello_u14.py`: il valore frozen, la raccolta con eccezioni di
  dominio, il confine della CLI e la suite con 11 test;
- nuova `documentazione/unita-14/` con contratti e rappresentazione,
  componenti e conversioni, prove e revisione;
- nessun programma delle tappe precedenti è cambiato: `registro_oggetti_u13.py`
  resta disponibile per il confronto fra i due modelli e la suite cumulativa
  prova la regressione.

## Limiti del riferimento

- La rappresentazione interna resta una lista: non sono introdotte strutture
  indicizzate né ricerche dicotomiche sulla raccolta.
- Un metodo statico o una factory per ogni classe non sono esibiti: la
  consegna li richiede soltanto dove rispondono a un requisito.
- La concorrenza di più sessioni sullo stesso archivio non è gestita.
- Le eccezioni di dominio sono tre e coerenti con la consegna: una gerarchia
  più ricca non è richiesta.

## Mappa delle prova

| Prova | Come si verifica | Atteso |
|---|---|---|
| PU14-01 | `uv run pytest -q programmi/test_modello_u14.py` | eq per contenuto, `is` distinto da `==` |
| PU14-02 | stesso comando | zeri e codici `007`/`7` distinti in ogni rappresentazione |
| PU14-03 | stesso comando | modifica invalida senza effetti parziali, ordine invariato |
| PU14-04 | stesso comando | duplicato con esito dichiarato, sessioni indipendenti |
| PU14-05 | stesso comando | snapshot protetti e alias come documentato |
| PU14-06 | stesso comando | round-trip con valori, tipi e documento equivalenti |
| PU14-07 | stesso comando | corrotto e guasto: politiche U12, nessuna perdita, nessun successo falso |
| PU14-08 | stesso comando | riepilogo e viste uguali alla versione procedurale |
| PR-14-1, PR-14-2 | stesso comando | sostituzione atomica e dati derivati aggiornati |
| Modifica breve | stesso comando | `per_destinazione` validata, ordinata e protetta |
| Regressione | `uv run pytest -q` | 145 test complessivi superati |
| Sessione CLI | `uv run python programmi/registro_cli_u14.py` | diagnosi distinte per valore e raccolta; rifiuti non pendenti |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  - sezione *Unità 14 — Oggetti robusti e modello dati del registro*.
- Teoria di riferimento: OOP-03 - *Oggetti robusti e modello dati*, OOP-04 -
  *Composizione e delega*; laboratorio LAB-PY-U14.
