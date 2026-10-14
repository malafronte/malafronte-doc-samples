# Unità 20 — Preparazione su immagini, coordinate, interfaccia grafica e persistenza

Questo progetto raccoglie i contratti, le fixture canoniche, gli esempi preparatori e i test dei capitoli **PY-40** (*Immagini raster, coordinate del piano e colorazione*), **PY-41** (*Interfaccia grafica con Tkinter ed esplorazione reattiva*) e **PY-42** (*Progettazione a componenti, persistenza JSON, test e analisi dei costi*), oltre alle attività del laboratorio **LAB-PY-U20-B**.

## Comandi di verifica

Dalla cartella `preparazione-immagini-interfaccia`:

```powershell
uv sync --frozen
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
```

## Struttura dei moduli per lotto

- `contratti_raster_json.py` *(L1)* — Contratti condivisi, griglie canoniche `4×2` e `1×1` con campionamento al centro del pixel, tabelle cromatiche deterministiche (`"binaria"`, `"bande"`, `"gradiente"`), limiti matematici e operativi, schema JSON versione `1` per le quattro famiglie (`"koch"`, `"sierpinski"`, `"mandelbrot"`, `"julia"`) e oracoli di validazione.
- `coordinate_esempi.py`, `palette_esempi.py` e `griglia_pillow.py` *(L5)* — Trasformazione tra pixel e piano complesso, adattamento geometrico con scala uniforme, zoom e spostamento con limiti operativi, strategie di colorazione con legenda e generazione/esportazione PNG con Pillow (matrice degli esiti, statistiche di costo, riapertura verificata).
- `finestra_griglia.py` *(previsto in L6)* — Finestra Tkinter preparatoria con calcolo cooperativo a blocchi (`after`), avanzamento, annullamento tramite `id_lavoro` e conservazione esplicita di `PhotoImage`.
- `configurazione_esempio.py` *(previsto in L7)* — Modello a componenti sostituibili, validazione di dominio e salvataggio/caricamento JSON atomico tramite file temporaneo.
- `tests/` — Suite `pytest` eseguibile senza apertura di finestre grafiche sui contratti *(L1: 12 test)* e sui moduli applicativi *(L5: 12 test in `test_immagini_l5.py`)*.
