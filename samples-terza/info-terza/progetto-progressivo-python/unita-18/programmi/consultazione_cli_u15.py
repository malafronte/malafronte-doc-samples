"""Punto di avvio della consultazione: sceglie il criterio concreto (U15).

Responsabilità del modulo: comporre il programma — caricare l'archivio,
costruire la raccolta, **scegliere l'implementazione concreta** del criterio
e presentare l'esito. Il client `seleziona_codici` e i criteri non cambiano
quando se ne aggiunge uno nuovo: la scelta vive qui, alla luce del sole.

Uso, dalla root del progetto:

    uv run python programmi/consultazione_cli_u15.py destinazione locale
    uv run python programmi/consultazione_cli_u15.py soglia 500
    uv run python programmi/consultazione_cli_u15.py soglia-esclusiva 500

Con argomenti mancanti o non ammessi il programma presenta la guida e termina
senza effetti, prima di caricare qualsiasi file.
"""
import sys
from pathlib import Path

from registro_modello_u14 import RegistroPreventivi
from registro_consultazione_u15 import (
    ErroreConfigurazione,
    PoliticaDestinazione,
    PoliticaSoglia,
    PoliticaSogliaEsclusiva,
    seleziona_codici,
)
from registro_persistenza import carica_archivio

PERCORSO_PREDEFINITO = Path("dati") / "unita-12" / "archivio.json"
GUIDA = (
    "Uso: consultazione_cli_u15.py <destinazione|soglia|soglia-esclusiva> <valore>"
)


def costruisci_criterio(argomenti):
    """Restituisce il criterio scelto dagli argomenti; None se non ammesso.

    Qui — e soltanto qui — si decide quale implementazione concreta usare.
    """
    if len(argomenti) != 2:
        return None
    scelta, valore = argomenti
    try:
        if scelta == "destinazione":
            return PoliticaDestinazione(valore)
        if scelta == "soglia":
            return PoliticaSoglia(int(valore))
        if scelta == "soglia-esclusiva":
            return PoliticaSogliaEsclusiva(int(valore))
    except (ErroreConfigurazione, ValueError):
        return None
    return None


def main() -> None:
    """Carica l'archivio, applica il criterio scelto e presenta i codici."""
    criterio = costruisci_criterio(sys.argv[1:])
    if criterio is None:
        print(GUIDA)
        return

    caricato, esito, dettaglio = carica_archivio(PERCORSO_PREDEFINITO)
    if esito != "":
        print(f"Caricamento non riuscito ({esito}): {dettaglio}")
        return
    registro = RegistroPreventivi()
    registro.sostituisci_da_lista(caricato)

    codici = seleziona_codici(registro, criterio)
    print(f"Criterio: {criterio.descrizione()}")
    print(f"Record consultati: {registro.numero}")
    print(f"Codici ammessi: {codici}")


if __name__ == "__main__":
    main()
