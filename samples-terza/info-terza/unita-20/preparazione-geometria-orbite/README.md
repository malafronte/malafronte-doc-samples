# Unità 20 — Preparazione su geometria ricorsiva, numeri complessi e orbite

Questo progetto raccoglie i dati canonici, gli esempi preparatori verificati e i test dei capitoli **PY-37** (*Frattali geometrici e costruzioni ricorsive*), **PY-38** (*Numeri complessi e iterazioni nel piano*) e **PY-39** (*Insiemi di Mandelbrot e di Julia: algoritmi a tempo di fuga*), oltre alle attività del laboratorio **LAB-PY-U20-A**.

## Comandi di verifica

Dalla cartella `preparazione-geometria-orbite`:

```powershell
uv sync --frozen
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
```

## Struttura dei moduli per lotto

- `dati_canonici.py` *(L1)* — Contratti condivisi, tolleranze, geometria dei livelli piccoli di Koch e Sierpiński, operazioni e tracce canoniche sui numeri complessi, i dodici casi discriminanti `M-01`–`M-07` e `J-01`–`J-05` e gli oracoli indipendenti su componenti reali.
- `geometria_esempi.py` *(previsto in L2)* — Costruzioni ricorsive finite della curva di Koch, del fiocco di neve di Koch e del triangolo di Sierpiński, conteggi e verifiche geometriche.
- `complessi_esempi.py` e `orbite_esempi.py` *(previsti in L3)* — Operazioni sul tipo `complex`, confronto con coppie di reali e costruzione di tabelle di orbita per `z_{n+1} = z_n^2 + c`.
- `fuga_esempi.py` *(L4)* — Kernel deterministico a tempo di fuga con esito `int | None`, classificazione per Mandelbrot (`z_0 = 0`, `R = 2`) e Julia (`R = max(2, |c|)`), oracolo indipendente su reali e chiamate delle due famiglie.
- `laboratorio/` *(L4)* — Starter di LAB-PY-U20-A (`fuga_lab_starter.py` con kernel e chiamate da completare, formattazione fornita) e casi pubblici (`test_pubblici.py`, LAB-A-01–LAB-A-11 con esito iniziale 5 superati e 6 con `NotImplementedError`).
- `tests/` — Suite `pytest` sui contratti e sugli oracoli canonici *(L1)* e sui moduli applicativi *(L2–L4: 42 test)*.
