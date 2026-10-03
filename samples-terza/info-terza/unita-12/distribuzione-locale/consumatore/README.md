# consumatore-utilita-u12 — progetto consumatore

Progetto **diverso e indipendente** da `../autore/`: serve a dimostrare che la
libreria personale `utilita_magazzino-u12` si può usare senza dipendere dalla
cartella dei sorgenti dell'autore. Qui non ci sono copie del codice della
libreria, nessuna modifica a `sys.path` e nessuna variabile d'ambiente: la
dipendenza è dichiarata nel `pyproject.toml` e risolta installando la **wheel**
nell'ambiente di questo progetto.

## Struttura

```text
consumatore/
├── pyproject.toml     # dipendenza dalla wheel locale (path + lock)
├── .python-version    # 3.14, interprete del corso
├── uv.lock            # risoluzione bloccata
├── README.md
├── usa_utilita.py     # usa la libreria e stampa l'origine del package
└── .venv/             # ambiente proprio (non si versiona)
```

## Comandi verificati

Prerequisito: la wheel esiste, prodotta dall'autore con `uv build` nella
cartella `../autore/dist/`. Dalla cartella `consumatore/`:

```powershell
uv add ..\autore\dist\utilita_magazzino_u12-0.1.0-py3-none-any.whl
uv run python usa_utilita.py
```

`uv add` registra la dipendenza nel `pyproject.toml` - `dependencies` più la
fonte in `[tool.uv.sources]` con il percorso della wheel - e produce il
`uv.lock`. L'esecuzione mostra i risultati della libreria e l'**origine del
package importato**: `utilita_magazzino_u12.__file__` è dentro la `.venv` di
questo progetto (`site-packages`), non nella cartella `autore/src/`.

## Ricostruzione in ambiente nuovo

Cancellando la `.venv` e rieseguendo `uv run python usa_utilita.py`, `uv`
ricrea l'ambiente dal `uv.lock` e reinstalla la wheel dichiarata. Il lock
**non materializza la wheel**: è necessario che quel file esista ancora in
`../autore/dist/`, oppure venga reso disponibile sulla nuova postazione. Questo
è il limite della dipendenza da artefatto locale, rispetto a una dipendenza da
un indice di package.

## Quando la wheel viene ricostruita

Il `uv.lock` registra anche l'**hash** della wheel installata. Se l'autore
modifica la libreria ed esegue di nuovo `uv build`, la wheel ha lo stesso nome
ma contenuto diverso: `uv` rifiuta il ricambio con `Hash mismatch` fra hash
atteso e hash calcolato, e non installa un artefatto diverso da quello
bloccato. Il comando di aggiornamento è esplicito - si ripete la risoluzione
della sola dipendenza - e poi l'ambiente si riallinea:

```powershell
uv lock --refresh-package utilita-magazzino-u12
uv sync
```

Il controllo non è un difetto: è il lock che fa il proprio lavoro. Se la
wheel cambiasse nome o versione - per esempio `0.2.0` - la dipendenza andrebbe
dichiarata di nuovo con `uv add`.

## Che cosa non è questa dimostrazione

La wheel è installabile in un ambiente Python: **non** è un eseguibile autonomo
e **non** è un installer Windows. Il repository con i sorgenti non è una
pubblicazione su un indice di package. La pubblicazione su TestPyPI/PyPI è un
approfondimento separato, descritto nella guida `dev-tools/librerie-personali`
del sito e non eseguita in questo materiale.

Versioni verificate: CPython 3.14.7, uv 0.12.15, Windows 11.
