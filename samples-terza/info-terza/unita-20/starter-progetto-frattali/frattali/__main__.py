"""Entry point del Laboratorio dei frattali (in parte da completare).

Comandi:

- `uv run python -m frattali stato`: elenca le operazioni fornite e quelle
  ancora da completare (fornito, tappa FR-M1);
- `uv run python -m frattali genera --config <file> --png <file>`: riproduce
  un'immagine dai parametri (da completare, tappe FR-M5 e FR-M7).

Il comando `genera` dichiara esplicitamente lo stato incompleto e termina
con un errore motivato: un programma incompleto non viene presentato come
prodotto eseguibile completo.
"""

import argparse
import sys


def operazioni_stato() -> dict[str, bool]:
    """Restituisce lo stato di ogni operazione: `True` se fornita (fornito, FR-M1)."""
    from frattali import dominio
    from frattali.algoritmi import geometrici, quadratici
    from frattali.rendering import colori, coordinate, immagini, stato

    sonde: dict[str, object] = {
        "dominio.valori": lambda: dominio.VistaComplessa(0.0, 0.0, 3.5),
        "dominio.parametri": lambda: dominio.ParametriMandelbrot(),
        "dominio.configurazione": lambda: dominio.ConfigurazioneFrattale(None, None, None, None),
        "algoritmi.quadratici": lambda: quadratici.classifica_mandelbrot(1 + 0j, 3),
        "algoritmi.geometrici": lambda: geometrici.produci_koch(1, "curva", 3.0),
        "rendering.coordinate": lambda: coordinate.punto_da_pixel(0, 0, 4, 2, 0.0, 0.0, 4.0),
        "rendering.colori": lambda: colori.colora_esito(None, 6, "bande"),
        "rendering.immagini": lambda: immagini.costruisci_matrice_esiti(None, None),
        "rendering.stato": lambda: stato.nuovo_lavoro(None, 1),
        "persistenza": lambda: __import__(
            "frattali.persistenza", fromlist=["carica_configurazione"]
        ).carica_configurazione("assente.json"),
    }
    esiti: dict[str, bool] = {}
    for nome, sonda in sonde.items():
        try:
            sonda()
        except NotImplementedError:
            esiti[nome] = False
        except Exception:
            esiti[nome] = True
        else:
            esiti[nome] = True
    return esiti


def comando_stato() -> int:
    """Stampa lo stato delle operazioni e restituisce `0` (fornito, FR-M1)."""
    esiti = operazioni_stato()
    for nome in sorted(esiti):
        stato = "fornita" if esiti[nome] else "da completare"
        print(f"- {nome}: {stato}")
    mancanti = sum(1 for pronta in esiti.values() if not pronta)
    print(f"Operazioni da completare: {mancanti} su {len(esiti)}.")
    return 0


def immagine_da_configurazione(percorso: str) -> object:
    """Restituisce l'immagine completa descritta dal JSON (da completare, FR-M5/FR-M7).

    Il completamento richiede caricamento validato, scelta del generatore e
    produzione dell'immagine della famiglia richiesta. Per le famiglie numeriche,
    `costruisci_matrice_esiti(configurazione, classifica_punto)` riceve un
    classificatore effettivo; `matrice_a_immagine(matrice, configurazione)`
    riceve due argomenti. Le famiglie geometriche richiedono il proprio disegno.
    Questa funzione non salva file: l'I/O PNG resta nel comando fornito.
    """
    raise NotImplementedError(
        "FR-M5/FR-M7: completare immagine_da_configurazione con caricamento, "
        "generatore della famiglia e immagine completa."
    )


def comando_genera(configurazione: str, destinazione_png: str) -> int:
    """Collega la generazione da completare all'I/O PNG (fornito, FR-M1)."""
    from frattali.rendering import immagini

    try:
        immagine = immagine_da_configurazione(configurazione)
        immagini.salva_png(immagine, destinazione_png)
    except NotImplementedError as causa:
        print(f"Generazione non ancora disponibile: {causa}")
        print("Completare le tappe FR-M1–FR-M7 seguendo il protocollo dei requisiti.")
        return 2
    print(f"Immagine scritta in {destinazione_png}.")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Smista i comandi `stato` e `genera` (fornito, FR-M1)."""
    parser = argparse.ArgumentParser(prog="frattali", description=__doc__)
    sotto = parser.add_subparsers(dest="comando", required=True)
    sotto.add_parser("stato", help="Elenca le operazioni fornite e da completare.")
    genera = sotto.add_parser("genera", help="Riproduce un'immagine dai parametri.")
    genera.add_argument("--config", required=True, help="File JSON di configurazione.")
    genera.add_argument("--png", required=True, help="File PNG di destinazione.")
    argomenti = parser.parse_args(argv)
    if argomenti.comando == "stato":
        return comando_stato()
    return comando_genera(argomenti.config, argomenti.png)


if __name__ == "__main__":
    sys.exit(main())
