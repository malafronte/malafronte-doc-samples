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
- `finestra_griglia.py` *(L6)* — Coordinatore puro eseguibile a blocchi senza Tkinter (stati, fotografia, `id_lavoro` con invalidazione) e finestra Tkinter preparatoria con `after`, avanzamento, annullamento, zoom dell'anteprima e conservazione esplicita di `PhotoImage`; import pigro di `tkinter` dentro `avvia_dimostrazione`.
- `laboratorio/` *(L6)* — Starter LAB-B (`finestra_lab_starter.py` con punti di lavoro nelle fasi 3–4) e casi pubblici (`test_pubblici.py`, LAB-B-01–LAB-B-08, esito iniziale 5/3).
- `collaudo_gui_l6.py` *(L6)* — Collaudo manuale della finestra reale con misure dei blocchi, annullamento, ciclo `after` e chiusura durante il calcolo; richiede un display, fuori dalla suite `pytest`.
- `configurazione_esempio.py` *(L7)* — Oggetti di valore immutabili, contratti `Protocol` con implementazioni sostituibili (classificatori, produttori, colorazioni), composizione `ConfigurazioneFrattale`, `ArchivioConfigurazioni` con salvataggio atomico e aiuti per i costi; senza Tkinter né Pillow.
- `tests/` — Suite `pytest` eseguibile senza apertura di finestre grafiche sui contratti *(L1: 12 test)* e sui moduli applicativi *(L5: 12 test in `test_immagini_l5.py`; L6: 12 test in `test_finestra_griglia_l6.py`; L7: 15 test in `test_configurazione_l7.py`, totale 51)*.
