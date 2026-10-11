"""Punto di avvio della coda di consultazione (U16).

Responsabilità del modulo: comporre il programma - caricare l'archivio,
costruire la raccolta, **scegliere la rappresentazione concreta della coda**,
accodare le richieste descritte dagli argomenti e presentare gli esiti
nell'ordine di arrivo. Il servizio e le richieste non cambiano quando la
rappresentazione della coda cambia: la scelta vive qui, alla luce del sole.

Uso, dalla root del progetto:

    uv run python programmi/coda_cli_u16.py destinazione locale soglia 500
    uv run python programmi/coda_cli_u16.py concatenata destinazione locale
    uv run python programmi/coda_cli_u16.py deque soglia 0

Il primo argomento facoltativo `deque` o `concatenata` sceglie la
rappresentazione della coda; il valore predefinito è `deque`. Ogni coppia
successiva `<criterio> <valore>` descrive una richiesta, accodata nell'ordine
in cui compare sulla riga di comando. Con argomenti mancanti o non ammessi il
programma presenta la guida e termina senza effetti, prima di accodare
qualsiasi richiesta.
"""
import sys
from pathlib import Path

from coda_richieste_u16 import (
    CodaConcatenataU16,
    CodaDequeU16,
    RichiestaConsultazione,
    ServizioConsultazione,
)
from registro_consultazione_u15 import (
    ErroreConfigurazione,
    PoliticaDestinazione,
    PoliticaSoglia,
)
from registro_modello_u14 import RegistroPreventivi
from registro_persistenza import carica_archivio

PERCORSO_PREDEFINITO = Path("dati") / "unita-12" / "archivio.json"
GUIDA = (
    "Uso: coda_cli_u16.py [deque|concatenata] <destinazione|soglia> <valore> ..."
)


def costruisci_coda(scelta):
    """Restituisce la coda vuota della rappresentazione scelta; None se non ammessa."""
    if scelta == "deque":
        return CodaDequeU16()
    if scelta == "concatenata":
        return CodaConcatenataU16()
    return None


def costruisci_richiesta(numero, criterio_testo, valore):
    """Restituisce la richiesta numero `numero`; None se la coppia non è ammessa."""
    try:
        if criterio_testo == "destinazione":
            criterio = PoliticaDestinazione(valore)
        elif criterio_testo == "soglia":
            criterio = PoliticaSoglia(int(valore))
        else:
            return None
    except (ErroreConfigurazione, ValueError):
        return None
    return RichiestaConsultazione(f"R{numero:02d}", criterio)


def main() -> None:
    """Carica l'archivio, accoda le richieste valide e presenta gli esiti in ordine."""
    argomenti = sys.argv[1:]
    coda = CodaDequeU16()
    if argomenti and argomenti[0] in ("deque", "concatenata"):
        coda = costruisci_coda(argomenti[0])
        argomenti = argomenti[1:]
    if not argomenti or len(argomenti) % 2 != 0:
        print(GUIDA)
        return

    servizio = ServizioConsultazione(coda)
    for numero in range(1, len(argomenti) // 2 + 1):
        criterio_testo, valore = argomenti[2 * (numero - 1) : 2 * numero]
        richiesta = costruisci_richiesta(numero, criterio_testo, valore)
        if richiesta is None:
            print(f"Richiesta R{numero:02d} non ammessa: {criterio_testo} {valore}")
            print(GUIDA)
            return
        servizio.accoda_richiesta(richiesta)

    caricato, esito, dettaglio = carica_archivio(PERCORSO_PREDEFINITO)
    if esito != "":
        print(f"Caricamento non riuscito ({esito}): {dettaglio}")
        return
    registro = RegistroPreventivi()
    registro.sostituisci_da_lista(caricato)

    for esito in servizio.elabora_tutte(registro):
        codici = ", ".join(esito.codici_ammessi) if esito.codici_ammessi else "nessuno"
        print(f"{esito.codice} [{esito.criterio}] -> [{codici}]")
    print(f"richieste elaborate: {servizio.elaborate}, pendenti: {len(servizio)}")


if __name__ == "__main__":
    main()
