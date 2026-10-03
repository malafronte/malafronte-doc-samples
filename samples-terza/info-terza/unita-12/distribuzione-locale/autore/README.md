# utilita-magazzino-u12 — progetto autore

Piccola libreria personale usata dal cap. PY-22 del corso per mostrare
l'intera filiera **dai sorgenti alla distribuzione installabile**. Il package
`utilita_magazzino_u12` espone tre funzioni già incontrate nel corso,
riorganizzate come API pubblica con validazione esplicita:

| Funzione | Risultato |
|---|---|
| `valore_magazzino(articoli)` | valore complessivo di un inventario, in centesimi |
| `formatta_centesimi(centesimi)` | stringa monetaria `"euro,cc €"` (es. `800` → `8,00 €`) |
| `normalizza_codice(testo)` | codice senza spazi iniziali e finali |

## Struttura

```text
autore/
├── pyproject.toml                 # metadati, backend di build e dipendenze di sviluppo
├── .python-version                # 3.14, interprete del corso
├── uv.lock                        # risoluzione delle dipendenze bloccata
├── README.md
├── src/
│   └── utilita_magazzino_u12/
│       ├── __init__.py            # API pubblica e versione
│       └── calcoli.py             # implementazione
└── tests/
    └── test_calcoli.py            # casi discriminanti: zero, ordinario, dominio
```

Il layout è quello **`src`**: il package vive sotto `src/` e non è importabile
dalla cartella di lavoro per caso - solo l'installazione lo rende disponibile,
così un test non passa perché Python trova il file accanto al test stesso.

## Comandi verificati

Dalla cartella `autore/`, con `uv` e l'interprete del corso:

```powershell
uv sync                            # crea .venv e installa il progetto in modalità modificabile
uv run pytest tests/ -q            # esegue la suite
uv build                           # produce dist/ con wheel e sdist
```

`uv sync` installa il progetto stesso in modalità **modificabile** dentro la
`.venv` locale: è ciò che rende importabile il package durante lo sviluppo. La
wheel prodotta da `uv build` è invece un artefatto **separato dai sorgenti**, e
sarà installata dal progetto consumatore descritto in `../consumatore/`.

Versioni verificate: CPython 3.14.7, uv 0.12.15, hatchling come backend di
build, pytest 9.1.1 (dipendenza di sviluppo dichiarata in `pyproject.toml`).
