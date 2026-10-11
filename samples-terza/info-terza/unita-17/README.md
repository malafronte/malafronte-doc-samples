# Unità 17 — Alberi binari e alberi binari di ricerca

Materiali eseguibili dell'Unità 17 del corso di Programmazione in terza:
alberi binari rappresentati con oggetti collegati, alberi binari di
ricerca con chiavi intere e dati associati, indice di record, query su
intervallo, invarianti e costi in funzione dell'altezza.

## Ambiente

- **Sistema operativo:** indifferente; comandi verificati su Windows con PowerShell.
- **Python:** 3.14 (dichiarata in `pyproject.toml` e `.python-version`).
- **Gestione degli ambienti:** `uv`, con ambiente virtuale locale nella cartella corrente.
- **Dipendenze:** nessuna dipendenza di esecuzione; `pytest` e `ruff` nel gruppo di sviluppo.

## Installazione

Dalla cartella `unita-17`:

```powershell
uv sync --frozen
```

## Esecuzione degli esempi

I moduli in `esempi/` non eseguono operazioni all'importazione e si
importano da un proprio programma, da un test o da una sessione
interattiva. Per una verifica immediata dei dati canonici:

```powershell
uv run python -c "from esempi.alberi_binari_u17 import costruisci_albero_d1, altezza, conta_foglie; a = costruisci_albero_d1(); print(altezza(a), conta_foglie(a))"
```

Il programma di verifica delle soluzioni si esegue con la suite, come
indicato nella sezione successiva.

## Contenuto

| Cartella | Contenuto |
|---|---|
| `esempi/` | `alberi_binari_u17.py` (cap. PY-32), `bst_u17.py` (cap. PY-33), `indice_schede_u17.py`, `confronto_altezze_u17.py`. |
| `soluzioni/` | `esercizi_base_u17.py` e `problemi_algoritmici_u17.py`, soluzioni formative della raccolta e della banca algoritmica. |
| `laboratorio/` | `indice_bst_starter.py` (deliberatamente incompleto), `dati_schede.py`, `test_pubblici.py` (casi LAB17-01…LAB17-12). |
| `dati/` | `ordini_inserimento.json`, ordini di inserimento e conteggi attesi dei dataset D1 e D2. |
| `tests/` | Suite degli esempi completi. |

## Prove

```powershell
uv run pytest -q
uv run pytest -q laboratorio/test_pubblici.py
```

La suite `tests/` verifica i moduli completi e le soluzioni formative ed
è interamente verde. La suite `laboratorio/test_pubblici.py` riguarda lo
starter: all'inizio del laboratorio i test sui metodi `TODO` falliscono
con `NotImplementedError`, come previsto, e diventano verdi con il
completamento delle fasi L2-L5.

Le funzioni di verifica dei moduli in `soluzioni/` si richiamano dalla
suite (`tests/test_soluzioni_formative_u17.py`), che colloca `esempi/` e
`soluzioni/` nel percorso degli import tramite la configurazione di
pytest.

## Qualità del codice

```powershell
uv run ruff check .
uv run ruff format --check .
```

## Dati e output attesi

Il dataset D1 è la sequenza `[40, 20, 60, 10, 30, 50, 70, 25, 35, 55]`,
con 10 nodi, 5 foglie e altezza 3 in archi. I due ordini del dataset D2
producono altezze 2 e 6 con 10 e 21 nodi esaminati nella costruzione. I
valori completi sono in `dati/ordini_inserimento.json` e nelle tabelle
dei capitoli.

## Convenzioni

- Altezza in archi: `altezza(None) = -1`, foglia `0`.
- Chiavi intere uniche, con `bool` escluso dal dominio.
- Duplicati rifiutati con `ValueError`; chiave assente in `cerca` con `KeyError`; `rimuovi` restituisce `bool`.
- Intervallo chiuso agli estremi; estremi invertiti con `ValueError`.
