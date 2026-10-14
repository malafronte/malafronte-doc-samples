"""Collaudo manuale della finestra dimostrativa PY-41 — Unità 20 (L6).

Lo script apre la finestra reale nell'interprete del progetto, la guida
programmaticamente e registra evidenze per il registro di lavoro:

- ambiente e hardware della prova;
- apertura reale, titoli, etichette, focus, ridimensionabilità e tastiera;
- avanzamento a blocchi con durate misurate sulla configurazione di
  riferimento `160×120` con blocchi di 8 righe;
- annullamento a metà, nuovo lavoro con invalidazione delle callback
  precedenti, risultato parziale etichettato;
- campi invalidi con messaggi, clic dentro/fuori, zoom e ripristino
  dell'anteprima;
- ciclo `after` reale lasciato avanzare da solo e chiusura durante il
  calcolo senza callback su widget distrutti;
- schermata della finestra salvata nella destinazione indicata.

Esecuzione dalla cartella `preparazione-immagini-interfaccia`:

```powershell
uv run python collaudo_gui_l6.py --dest C:/Users/genna/AppData/Local/Temp/opencode/collaudo-l6
```

Lo script non fa parte della suite `pytest`: apre finestre reali e richiede
un display. I test di correttezza restano indipendenti dalla velocità
dell'hardware; le durate qui misurate sono obiettivi prestazionali osservati.
"""

from __future__ import annotations

import argparse
import os
import platform
import sys
import time
from types import SimpleNamespace

from finestra_griglia import avvia_dimostrazione


def stampa_sezione(titolo: str) -> None:
    print(f"--- {titolo} ---")


def imposta_campi(app, larghezza: str, altezza: str, blocco: str) -> None:
    for campo, valore in (
        (app.campo_larghezza, larghezza),
        (app.campo_altezza, altezza),
        (app.campo_blocco, blocco),
    ):
        campo.config(state="normal")
        campo.delete(0, "end")
        campo.insert(0, valore)


def main() -> None:
    parser = argparse.ArgumentParser(description="Collaudo manuale della finestra PY-41.")
    parser.add_argument("--dest", required=True, help="Cartella per schermata ed evidenze.")
    args = parser.parse_args()

    import tkinter as tk

    import PIL

    stampa_sezione("ambiente")
    print(f"python: {sys.version.split()[0]}")
    print(f"tk: {tk.TkVersion} / tcl: {tk.TclVersion}")
    print(f"pillow: {PIL.__version__}")
    print(f"sistema: {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"processore: {platform.processor() or 'n/d'} x{os.cpu_count()}")

    app = avvia_dimostrazione(avvia_ciclo=False)
    radice = app.radice
    radice.geometry("+120+120")
    radice.update_idletasks()
    radice.update()

    stampa_sezione("finestra")
    print(f"esiste: {radice.winfo_exists()}, titolo: {radice.title()}")
    print(f"ridimensionabile: {radice.resizable()}")
    print(f"focus su genera: {radice.focus_get() == app.pulsante_genera}")
    print(f"zona canvas: {app.tela.cget('width')}x{app.tela.cget('height')}")
    print(f"escape vincolato: {bool(radice.bind('<Escape>'))}")

    stampa_sezione("riferimento-160x120-blocco-8")
    imposta_campi(app, "160", "120", "8")
    contatore_prima = app.contatore_lavori
    app.genera()
    assert app.contatore_lavori == contatore_prima + 1
    durate: list[float] = []
    while app.lavoro_corrente.stato == "in_calcolo":
        app._cancella_callback_pendente()
        inizio = time.perf_counter()
        app._corpo_blocco()
        radice.update()
        durate.append((time.perf_counter() - inizio) * 1000.0)
    print(f"blocchi: {len(durate)}, stato: {app.lavoro_corrente.stato}")
    print(f"durata max iterazione: {max(durate):.1f} ms, media: {sum(durate) / len(durate):.1f} ms")
    print(f"durata max blocco interno: {app.durata_massima_blocco_ms:.1f} ms")
    print(f"progresso: {app.etichetta_stato.cget('text')[:80]}")
    print(f"salva abilitato: {str(app.pulsante_salva.cget('state')) == 'normal'}")

    stampa_sezione("annullamento-e-nuovo-lavoro")
    app.genera()
    for _ in range(3):
        app._cancella_callback_pendente()
        app._corpo_blocco()
        radice.update()
    righe_prima = len(app.lavoro_corrente.righe)
    id_vecchio = app.lavoro_corrente.id_lavoro
    app.annulla()
    print(f"stato dopo annulla: {app.lavoro_corrente.stato}, righe: {righe_prima}")
    app._corpo_blocco()
    radice.update()
    print(f"righe dopo callback obsoleta: {len(app.lavoro_corrente.righe)} (attese {righe_prima})")
    app.genera()
    print(f"nuovo id: {app.lavoro_corrente.id_lavoro} (precedente {id_vecchio})")
    while app.lavoro_corrente.stato == "in_calcolo":
        app._cancella_callback_pendente()
        app._corpo_blocco()
        radice.update()
    print(f"nuovo lavoro completato: {app.lavoro_corrente.stato}")

    stampa_sezione("annullamento-da-tastiera")
    app.genera()
    app._cancella_callback_pendente()
    app._corpo_blocco()
    radice.update()
    radice.event_generate("<Escape>")
    radice.update()
    print(f"stato dopo Escape: {app.lavoro_corrente.stato}")

    stampa_sezione("campi-clic-zoom")
    imposta_campi(app, "abc", "120", "8")
    contatore_prima = app.contatore_lavori
    app.genera()
    print(f"nuovo lavoro con campo invalido: {app.contatore_lavori == contatore_prima}")
    print(f"messaggio: {app.etichetta_messaggio.cget('text')[:100]}")
    imposta_campi(app, "160", "120", "8")
    app.genera()
    while app.lavoro_corrente.stato == "in_calcolo":
        app._cancella_callback_pendente()
        app._corpo_blocco()
        radice.update()
    app.al_clic(SimpleNamespace(x=88.0, y=68.0))
    print(f"clic interno: {app.etichetta_cella.cget('text')}")
    app.al_clic(SimpleNamespace(x=4.0, y=68.0))
    print(f"clic esterno: {app.etichetta_cella.cget('text')}")
    base = app.anteprima.size if app.anteprima is not None else (0, 0)
    app.cambia_zoom(1)
    zoomata = app.anteprima.size if app.anteprima is not None else (0, 0)
    app.ripristina_anteprima()
    ripristinata = app.anteprima.size if app.anteprima is not None else (0, 0)
    print(f"anteprima: {base} -> zoom {zoomata} -> ripristino {ripristinata}")

    try:
        from PIL import ImageGrab

        radice.update()
        bbox = (
            radice.winfo_rootx(),
            radice.winfo_rooty(),
            radice.winfo_rootx() + radice.winfo_width(),
            radice.winfo_rooty() + radice.winfo_height(),
        )
        os.makedirs(args.dest, exist_ok=True)
        schermata = ImageGrab.grab(bbox=bbox)
        percorso = os.path.join(args.dest, "screenshot-finestra-demo.png")
        schermata.save(percorso)
        print(f"schermata: {percorso} {schermata.size}")
    except Exception as causa:
        print(f"schermata non catturata: {causa}")

    stampa_sezione("ciclo-after-reale")
    imposta_campi(app, "40", "30", "6")
    app.genera()
    termine = time.perf_counter() + 2.0
    while app.lavoro_corrente.stato == "in_calcolo" and time.perf_counter() < termine:
        radice.update()
        time.sleep(0.01)
    print(f"stato dopo ciclo after reale: {app.lavoro_corrente.stato}")
    print(f"righe: {app.lavoro_corrente.righe_completate} di 30")

    stampa_sezione("chiusura-durante-calcolo")
    imposta_campi(app, "800", "600", "1")
    app.genera()
    termine = time.perf_counter() + 0.3
    while time.perf_counter() < termine:
        radice.update()
        time.sleep(0.01)
    app.chiudi()
    radice.update()
    print(f"finestra valida dopo chiudi: {app.finestra_valida}")
    print("collaudo-gui-completato")


if __name__ == "__main__":
    main()
