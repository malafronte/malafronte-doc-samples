# Raccolta progressiva di programmi — fotografia U1

Questa cartella è la **fotografia completa della raccolta al termine
dell'Unità 1**: contiene i file del progetto, i primi tre programmi e la
documentazione della tappa. È il riferimento di confronto della
[Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
del sito del corso: mostra una possibile realizzazione completa, non la
cronologia che ogni studente deve costruire con i propri commit.

La cartella è autonoma: copiata in una posizione separata, si esegue con i
soli comandi di questo README, senza dipendere dalle altre cartelle
`unita-NN` di questo repository.

## Traguardi della tappa

- progetto inizializzato con `uv`, interprete CPython 3.14 e ambiente
  ricostruibile con `uv sync`;
- tre programmi eseguibili con `uv run python programmi/<file>`, ciascuno con
  un output intenzionale e documentato;
- README riproducibile, `.gitignore` che esclude `.venv/` e `__pycache__/`;
- spiegazione del flusso sorgente → interprete → processo → output applicata
  alla raccolta.

## Struttura

```text
unita-01/
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
├── uv.lock
├── programmi/
│   ├── 01_hello.py
│   ├── 02_benvenuto.py
│   └── 03_messaggio_multiriga.py
└── documentazione/
    └── unita-01/
        └── flusso-sorgente-processo.md
```

## Ambiente e comandi verificati

Dalla root di questa cartella:

```powershell
uv sync --frozen          # ricostruisce .venv/ dal lock
uv run python --version   # Python 3.14.7
uv run python programmi/01_hello.py
uv run python programmi/02_benvenuto.py
uv run python programmi/03_messaggio_multiriga.py
```

## Sessioni reali

Esecuzione verificata su Windows 11 con CPython 3.14.7 e uv 0.12.15. Gli
output sono riprodotti integralmente, compresi i caratteri di fine riga: ogni
istruzione `print` produce una riga e va a capo.

```text
> uv run python programmi/01_hello.py
Ciao dal progetto raccolta-programmi.
```

```text
> uv run python programmi/02_benvenuto.py
Benvenuto nella raccolta di programmi.
Corso di informatica - classe terza, indirizzo informatico.
Strumenti del progetto: CPython 3.14, uv e Git.
```

```text
> uv run python programmi/03_messaggio_multiriga.py
Il programma descrive tre momenti dell'esecuzione.
1. Il sorgente contiene le istruzioni scritte dal programmatore.
2. L'interprete esegue le istruzioni in ordine.
3. Il processo mostra l'output a schermo.
```

Per ogni programma: il sorgente è il file in `programmi/`, l'interprete è
CPython avviato da `uv run`, il processo è l'esecuzione che legge il sorgente e
produce l'output mostrato. Il percorso completo è descritto in
[`documentazione/unita-01/flusso-sorgente-processo.md`](documentazione/unita-01/flusso-sorgente-processo.md).

## Differenze rispetto alla tappa precedente

Nessuna: questa è la prima fotografia della raccolta. La fotografia U2 è in
[`../unita-02/`](../unita-02/) e conserva integralmente questi file.

## Limiti del riferimento

- I tre programmi usano soltanto `print` e stringhe: input, conversioni,
  f-string, selezioni, cicli e funzioni arrivano nelle unità successive.
- Questa fotografia **non contiene cronologia Git**: la raccolta dello studente
  deve avere almeno quattro commit piccoli e coerenti, di cui almeno uno di
  correzione. Nessuna storia finta viene fornita, perché la cronologia è un
  lavoro dello studente e non un file da copiare.
- `.venv/`, `__pycache__/` e `uv.lock` sono gestiti come indicato nella
  sezione seguente: le prime due non si versionano, il lock sì.

## Mappa delle prova

| Prova | Come si verifica | Atteso |
|---|---|---|
| Esecuzione dei tre programmi | `uv run python programmi/<file>` dalla root | Output uguale a quello delle sessioni reali |
| Andamento a capo | Confronto fra righe stampate e istruzioni `print` | Una riga di output per istruzione, ciascuna terminata dal proprio a capo |
| Ambiente ricostruito | `uv sync --frozen` su una copia pulita della cartella | `uv run python --version` risponde 3.14.7 |
| File superflui | `git status` nella raccolta dello studente | `.venv/` e `__pycache__/` non risultano da versionare |

## Collegamenti

- Pagina del progetto: [Raccolta progressiva di programmi](https://github.com/malafronte/info-terza/blob/main/src/content/docs/progetti/progetto-progressivo-python.mdx)
  — sezione *Unità 1 — Raccolta iniziale*.
- Percorso guidato: [laboratorio U1](https://github.com/malafronte/info-terza/tree/main/src/content/docs/laboratori/laboratorio-python/unita-01-primo-progetto-versionato.mdx).
- Teoria di riferimento: cap. PY-01 — *Programmi, algoritmi e linguaggi*.
- Guida operativa: *Documentare un progetto Python* e *Configurazione
  iniziale*, nelle guide `dev-tools` del sito.
