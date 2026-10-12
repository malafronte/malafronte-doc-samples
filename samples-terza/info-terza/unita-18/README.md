# Unità 18 — Tabelle hash

Materiali eseguibili dell'Unità 18 del corso di Programmazione in terza:
funzione hash didattica e indici, tabella hash con concatenamento e crescita
per raddoppio, chiavi hashable e uguaglianza, simulazione dell'indirizzamento
aperto con marcatori, indice di record con codici testuali e confronto di
strategie sullo stesso carico di lavoro.

## Ambiente

- **Sistema operativo:** indifferente; comandi verificati su Windows con PowerShell.
- **Python:** 3.14 (dichiarata in `pyproject.toml` e `.python-version`).
- **Gestione degli ambienti:** `uv`, con ambiente virtuale locale nella cartella corrente.
- **Dipendenze:** nessuna dipendenza di esecuzione; `pytest` e `ruff` nel gruppo di sviluppo.

## Installazione

Dalla cartella `unita-18`:

```powershell
uv sync --frozen
```

## Esecuzione degli esempi

I moduli in `esempi/` non eseguono operazioni all'importazione e si
importano da un proprio programma, da un test o da una sessione
interattiva. Per una verifica immediata dei dati canonici:

```powershell
uv run python esempi/dimostrazione_hash_u18.py
```

Il programma di verifica delle soluzioni si esegue con la suite, come
indicato nella sezione successiva.

## Contenuto

| Cartella | Contenuto |
|---|---|
| `esempi/` | `tabella_hash_u18.py` (tabella concatenata), `hash_chiavi_u18.py` (indici e distribuzione), `chiavi_native_u18.py` (hashability), `indice_record_u18.py` (indice di record), `tracce_sondaggio_u18.py` (sondaggio e marcatori), `confronto_indici_u18.py` (confronto di strategie), `dimostrazione_hash_u18.py` (tracce canoniche). |
| `soluzioni/` | `esercizi_base_u18.py` e `problemi_hash_u18.py`, soluzioni formative della raccolta e della banca algoritmica. |
| `laboratorio/` | `indice_hash_starter.py` (deliberatamente incompleto), `dati_catalogo.py`, `simulazione_sondaggio.py` (fornita completa), `dati/catalogo.csv`, `dati/catalogo_duplicato.csv`, `test_pubblici.py` (casi LAB18-01…LAB18-14). |
| `tests/` | Suite degli esempi completi e delle soluzioni formative. |

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
suite (`tests/test_soluzioni_u18.py`), che colloca `esempi/`, `soluzioni/`
e `laboratorio/` nel percorso degli import tramite la configurazione di
pytest.

## Qualità del codice

```powershell
uv run ruff check .
uv run ruff format --check .
```

## Dati e output attesi

La traccia base usa capacità `m = 5`, inserimento in testa e hash intero:
`12, 7, 22, 17` condividono il bucket 2, l'aggiornamento di `7` conserva
`n = 4` e il carico `0.8`. La crescita con `12, 7, 22, 17, 3, 8` produce
`n = 6`, `m = 10` e carico `0.6`. I codici `"007"`, `"012"`, `"003"`,
`"017"` hanno hash `47671`, `47697`, `47667`, `47702` e indici `1, 2, 2, 2`
con `m = 5`. Il sondaggio con `m = 7` colloca `5, 12, 19` nelle posizioni
`5, 6, 0`; la rimozione di `12` marca la posizione 6.

## Convenzioni

- Chiavi di tipo esatto `int` oppure `str`, con `bool` escluso dal dominio.
- Duplicati nella tabella: aggiornamento; duplicati nel dataset applicativo: `ValueError`.
- Chiave assente in `cerca` con `KeyError`; `rimuovi` restituisce il valore rimosso.
- Soglia di crescita 1.0 con raddoppio; `coppie()` fuori dal contratto applicativo.
- Intervallo degli indici sempre fra `0` e `m - 1`, anche con interi negativi.
