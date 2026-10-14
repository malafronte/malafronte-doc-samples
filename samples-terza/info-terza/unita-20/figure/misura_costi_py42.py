"""Confronto dei costi su due risoluzioni e due budget — Unità 20 (L7).

Lo script misura il lavoro di classificazione di Mandelbrot sulla vista
iniziale (centro `-0.5 + 0j`, ampiezza `3.5`) con due risoluzioni
(`160×120`, `320×240`) e due budget (`N = 25`, `N = 100`), registrando per
ogni combinazione il lavoro effettivo `K`, il limite superiore `W·H·N`,
il rapporto `K / (W·H)` e i secondi trascorsi. La preparazione resta
fuori dalla regione cronometrata; i tempi documentano ordini di
grandezza sull'hardware usato, non soglie per i test.

Esecuzione dalla cartella `preparazione-immagini-interfaccia`:

```powershell
uv run python ../figure/misura_costi_py42.py
```

Il rapporto in Markdown viene scritto in
`../figure/esperimenti_costi_py42.md`.
"""

import platform
import sys
import time
from pathlib import Path

CARTELLA_ESEMPI = Path(__file__).resolve().parent.parent / "preparazione-immagini-interfaccia"
sys.path.insert(0, str(CARTELLA_ESEMPI))

from configurazione_esempio import (  # noqa: E402
    ClassificatoreMandelbrot,
    misura_classificazione,
)


def main() -> None:
    figura = Path(__file__).resolve().parent
    centro = complex(-0.5, 0.0)
    ampiezza = 3.5
    righe: list[str] = []
    for larghezza, altezza in ((160, 120), (320, 240)):
        for limite in (25, 100):
            classificatore = ClassificatoreMandelbrot(limite_iterazioni=limite)
            esito = misura_classificazione(
                classificatore.classifica,
                larghezza,
                altezza,
                centro,
                ampiezza,
                limite,
            )
            lavoro = esito["lavoro_effettivo"]
            superiore = esito["limite_superiore"]
            medio = lavoro / (larghezza * altezza)
            righe.append(
                f"| `{larghezza}×{altezza}` | `{limite}` | `{lavoro}` | "
                f"`{superiore}` | `{medio:.1f}` | `{esito['secondi']:.2f}` |"
            )
    contenuto = f"""# Esperimenti sui costi PY-42 — Mandelbrot sulla vista iniziale

Vista: centro `-0.5 + 0j`, ampiezza orizzontale `3.5`. Hardware e ambiente:
`{platform.system()} {platform.release()} ({platform.machine()})`,
CPython `{platform.python_version()}`, Tk non richiesto. I tempi coprono il
solo doppio ciclo di campionamento e classificazione; la preparazione resta
fuori dalla regione cronometrata. I valori documentano ordini di grandezza
sulla macchina usata, non soglie universali per i test.

| Risoluzione | N | K (lavoro effettivo) | W·H·N (limite) | K per pixel | Secondi |
|---|---|---|---|---|---|
{chr(10).join(righe)}

Lettura: il raddoppio di risoluzione quadruplica pixel, limite superiore e
lavoro di campionamento `W·H`; il raddoppio di `N` alza il limite superiore
ma il lavoro effettivo cresce meno, perché i pixel esterni fuggono presto.
La colorazione dalla matrice costerebbe `Theta(W·H)` senza ricalcolare le
orbite; il salvataggio JSON dei soli parametri resta indipendente dai pixel.
"""
    destinazione = figura / "esperimenti_costi_py42.md"
    destinazione.write_text(contenuto, encoding="utf-8")
    print("\n".join(righe))
    print(f"rapporto: {destinazione}")


if __name__ == "__main__":
    inizio = time.perf_counter()
    main()
    print(f"totale: {time.perf_counter() - inizio:.1f} s")
