# Unità 16 - Array dinamici, liste concatenate, pile e code

Riferimenti didattici CPython 3.14 per PY-23 e PY-24: modello a raddoppio
dell'array dinamico, nodi e collegamenti, lista semplicemente concatenata,
ADT pila e coda con quattro rappresentazioni, annullamenti ed elaborazione
delle richieste.

## Ambiente ed esecuzione

Dalla cartella `unita-16`, con uv già installato:

```powershell
uv sync --locked
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
uv run python esempi/nodi_collegamenti_u16.py
uv run python esempi/array_dinamico_modello_u16.py
uv run python esempi/annullamenti_u16.py
uv run python esempi/richieste_u16.py
uv run pytest -q laboratorio/test_lista_coda_starter.py
```

Gli import fra esempi sono fra moduli nella stessa directory; pytest dichiara i
percorsi nel manifest, senza alterazioni di `sys.path`. I file non aprono
interazioni all'import. La suite del laboratorio fallisce deliberatamente finché
le parti marcate `TODO` dello starter non sono completate.

## Manifest dei ruoli

| File/cartella | Ruolo e pagina |
|---|---|
| `esempi/array_dinamico_modello_u16.py` | PY-23 B-C: lunghezza, capacità, ridimensionamento e conteggi del modello |
| `esempi/nodi_collegamenti_u16.py` | PY-23 D-E: classe `Nodo`, costruzione della catena, attraversamento e ricerca |
| `esempi/lista_concatenata_u16.py` | PY-23 F-L: `ListaConcatenata`, nodo interno `_Nodo` e `controlla_invarianti` |
| `esempi/pile_code_u16.py` | PY-24 A-D: `PilaLista`, `PilaConcatenata`, `CodaDeque`, `CodaConcatenata` e client comune |
| `esempi/annullamenti_u16.py` | PY-24 E: `ContatoreAnnullabile` con pila degli stati precedenti |
| `esempi/richieste_u16.py` | PY-24 F: `Richiesta`, `Esito` e `ServizioRichieste` con collaboratore sostituibile |
| `tests/` | Invarianti, casi limite, identità dei nodi, contratti comuni e dataset canonici |
| `soluzioni/` | Soluzioni formative della raccolta di base e della famiglia algoritmica |
| `laboratorio/` | Starter incompleto deliberato e casi pubblici LAB16-01…LAB16-12 |
