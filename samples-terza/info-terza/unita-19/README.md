# Unità 19 — B-tree e confronto fra strutture di ricerca

Sorgenti Python dei capitoli PY-35 e PY-36: B-tree didattico con grado
minimo, dati canonici D1–D6, costruzione di riferimento, simulazioni
verificate di cancellazione, indice di record e confronto riproducibile fra
strutture di ricerca.

## Esecuzione

Dalla cartella `unita-19`:

```powershell
uv sync --frozen
uv run python esempi/dimostrazione_ricerca_u19.py
uv run pytest -q
uv run pytest -q laboratorio/test_pubblici.py
```

La suite iniziale di `laboratorio/test_pubblici.py` fallisce nei punti di
consultazione (`NotImplementedError` in `cerca`, `contiene` e
`dossier_scelta`): i fallimenti attesi fanno parte del percorso del
laboratorio LAB-PY-U19 e scompaiono con il completamento delle fasi L2 e L6.

## Contenuti

- `esempi/btree_modello_u19.py` — `NodoBTree`, `BTreeDidattico`, `EsitoRicerca`.
- `esempi/btree_costruzione_u19.py` — `costruisci_btree_riferimento` e tracce D2.
- `esempi/dati_btree_u19.py` — stati D1–D6 e record del catalogo.
- `esempi/dimostrazione_ricerca_u19.py` — query canoniche su D1.
- `esempi/simulazioni_btree_u19.py` — scenari di cancellazione verificati.
- `esempi/indice_record_u19.py` — indice dei materiali con intervallo chiuso.
- `esempi/confronto_strutture_u19.py` — adattatori, protocollo e CSV.
- `soluzioni/` — funzioni delle soluzioni di base e dei problemi algoritmici.
- `laboratorio/` — starter incompleto, dati del catalogo e casi pubblici.
- `tests/` — prove degli esempi e delle soluzioni.
- `dati/` — catalogo CSV e carichi del dossier.
