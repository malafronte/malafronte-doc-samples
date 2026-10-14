"""Starter del laboratorio LAB-PY-U20-A — Unità 20 (L4).

Il file fornisce l'infrastruttura del laboratorio, lasciando allo studente
il lavoro previsto dalle fasi:

- forniti: import dei dati canonici, dei moduli verificati di geometria,
  complessi e orbite, formattazione degli esiti (`riga_tabella_esito`) e
  stampa di tabelle (`stampa_casi`);
- da completare (fase 4): `esito_fuga` con la convenzione unica del contratto
  (controllo iniziale su `z_0`, poi aggiornamento e confronto stretto);
- da completare (fase 5): `esito_mandelbrot` (seme zero, `R = 2.0`) ed
  `esito_julia` (parametro fisso, `R = max(2.0, |c|)`).

La soluzione completa e verificata dei meccanismi è negli esempi
preparatori (`fuga_esempi.py`); questo starter conserva il lavoro richiesto.
Eseguire dalla radice del progetto `preparazione-geometria-orbite`:

```powershell
uv run pytest -q laboratorio/test_pubblici.py
```
"""

from dati_canonici import EsitoFugaCanonico


def esito_fuga(z_iniziale: complex, c: complex, limite_iterazioni: int, raggio_fuga: float):
    """Classifica un punto con il kernel a tempo di fuga (da completare, fase 4).

    Restituisce un `EsitoFugaCanonico` con `indice_fuga` (`int | None`),
    `aggiornamenti_eseguiti` e `valore_finale`, seguendo l'ordine del
    contratto: controllo iniziale su `z_0`, poi per `n = 1, ..., N`
    aggiornamento e confronto stretto, infine `None` a budget esaurito.
    """
    raise NotImplementedError("Fase 4: implementare il kernel con la convenzione unica.")


def esito_mandelbrot(c: complex, limite_iterazioni: int):
    """Classifica il parametro `c` di Mandelbrot (da completare, fase 5)."""
    raise NotImplementedError("Fase 5: seme z_0 = 0 fisso e raggio R = 2.0.")


def esito_julia(z_iniziale: complex, c: complex, limite_iterazioni: int):
    """Classifica il seme `z_0` di Julia (da completare, fase 5)."""
    raise NotImplementedError("Fase 5: parametro c fisso e raggio R = max(2.0, |c|).")


def riga_tabella_esito(codice: str, esito: EsitoFugaCanonico) -> str:
    """Formatta una riga della tabella degli esiti (fornita, fasi 4–5)."""
    if not isinstance(esito, EsitoFugaCanonico):
        raise TypeError("Il parametro 'esito' richiede un EsitoFugaCanonico.")
    indice = "None" if esito.indice_fuga is None else str(esito.indice_fuga)
    return (
        f"{codice:>6} | fuga: {indice:>4} | "
        f"aggiornamenti: {esito.aggiornamenti_eseguiti:>3} | "
        f"finale: {esito.valore_finale}"
    )


def stampa_casi(casi: list[tuple[str, EsitoFugaCanonico]]) -> None:
    """Stampa la tabella degli esiti dei casi dati (fornita, fasi 4–5)."""
    for codice, esito in casi:
        print(riga_tabella_esito(codice, esito))
