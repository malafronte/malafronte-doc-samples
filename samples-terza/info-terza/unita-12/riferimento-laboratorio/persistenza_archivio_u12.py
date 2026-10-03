"""Persistenza dell'archivio materiali: caricamento e salvataggio in CSV.

Il modulo contiene le sole operazioni di I/O sull'archivio. Le regole dei dati
restano nel modulo di dominio, che qui viene importato per la validazione:
la dipendenza va in un'unica direzione, dalla persistenza verso il dominio.

Formato dell'archivio: CSV UTF-8 con intestazione esatta
`codice,descrizione,quantita`, un record per riga, campi con virgole o
virgolette racchiusi fra virgolette come fa il modulo `csv`. I file scritti da
questo modulo **non hanno BOM** e usano il terminatore `\n`; il caricamento
accetta UTF-8 con o senza BOM grazie al codec `utf-8-sig`.

Politica del caricamento: **tutto valido oppure nessun archivio caricato**.
I record vengono raccolti in una lista temporanea e resi noti al chiamante
solo dopo che l'intero file ha superato i controlli; un errore lascia il
chiamante con i propri dati precedenti e non produce liste parziali.

Politica del salvataggio: si valida l'intera raccolta, si scrive una copia
temporanea nella **stessa directory** della destinazione, la si chiude e solo
allora la si sostituisce all'archivio. Se qualcosa fallisce prima della
sostituzione il vecchio file resta valido e il temporaneo viene rimosso. Il
protocollo protegge dai guasti di scrittura di un singolo processo: non è una
transazione e non protegge da interruzioni elettriche o scritture concorrenti.

Ambiente: CPython sul computer.
"""

import csv
import tempfile
from pathlib import Path

from dominio_archivio_u12 import CAMPI_MATERIALE
from dominio_archivio_u12 import materiale_a_riga
from dominio_archivio_u12 import riga_a_materiale
from dominio_archivio_u12 import valida_materiale


def _valida_intestazione(intestazione):
    """Controlla che l'intestazione del CSV coincida con lo schema esatto.

    Distingue i casi utili alla diagnosi: nomi duplicati, colonne mancanti,
    colonne non previste e stesso insieme di colonne in ordine diverso.
    """
    nomi = list(intestazione)
    duplicati = [nome for nome in nomi if nomi.count(nome) > 1]
    if duplicati:
        raise ValueError(f"intestazione con nomi duplicati: {duplicati[0]!r}")
    mancanti = [campo for campo in CAMPI_MATERIALE if campo not in nomi]
    if mancanti:
        raise ValueError(f"intestazione: colonna mancante {mancanti[0]!r}")
    extra = [nome for nome in nomi if nome not in CAMPI_MATERIALE]
    if extra:
        raise ValueError(f"intestazione: colonna non prevista {extra[0]!r}")
    if nomi != list(CAMPI_MATERIALE):
        attesa = ", ".join(CAMPI_MATERIALE)
        raise ValueError(f"intestazione: ordine delle colonne diverso da {attesa}")


def carica_materiali(percorso):
    """Legge l'archivio CSV e restituisce una lista nuova di materiali validi.

    Il file viene aperto in lettura testuale con `utf-8-sig`, che accetta UTF-8
    con o senza BOM iniziale, e con `newline=""`, come richiede il modulo
    `csv`. Se il file non esiste si propaga `FileNotFoundError`; se contiene
    byte non UTF-8 si propaga `UnicodeDecodeError`; se è strutturalmente
    malformato si propaga `csv.Error`; se intestazione, record o domini non
    sono ammessi si solleva `ValueError` con la diagnosi. Nessuno di questi
    errori restituisce una lista parziale.
    """
    percorso = Path(percorso)
    materiali = []
    codici = set()
    with open(percorso, "r", encoding="utf-8-sig", newline="") as sorgente:
        lettore = csv.reader(sorgente, strict=True)
        try:
            intestazione = next(lettore)
        except StopIteration:
            raise ValueError(
                "archivio senza intestazione: il file non contiene alcuna riga"
            ) from None
        _valida_intestazione(intestazione)
        numero_record = 0
        for record in lettore:
            if record == []:
                # Riga fisica vuota: il lettore la segnala con una lista vuota.
                # Non è un record e viene ignorata. Un record con campi vuoti
                # è invece ["", "", ""] e il validatore lo rifiuta.
                continue
            numero_record += 1
            riferimento = f"record {numero_record} (riga fisica {lettore.line_num})"
            materiale = riga_a_materiale(record, riferimento)
            if materiale["codice"] in codici:
                raise ValueError(
                    f"{riferimento}, campo 'codice': il codice {materiale['codice']!r} "
                    "è già presente"
                )
            codici.add(materiale["codice"])
            materiali.append(materiale)
    return materiali


def _valida_raccolta(materiali):
    """Controlla tutti i record e l'unicità dei codici prima di qualunque I/O."""
    codici = set()
    for posizione, materiale in enumerate(materiali, start=1):
        try:
            valida_materiale(materiale)
        except ValueError as errore:
            raise ValueError(f"record {posizione}: {errore}") from None
        if materiale["codice"] in codici:
            raise ValueError(
                f"record {posizione}: il codice {materiale['codice']!r} è già presente"
            )
        codici.add(materiale["codice"])


def salva_materiali(percorso, materiali):
    """Scrive l'intera raccolta nel file CSV con il protocollo del temporaneo.

    Sequenza: validare tutto, creare il temporaneo nella directory della
    destinazione, scrivere intestazione e record, chiudere, sostituire la
    destinazione. Il messaggio di successo spetta al chiamante e va dato solo
    dopo il ritorno da questa funzione. Su qualunque errore prima della
    sostituzione la destinazione precedente resta invariata e l'eccezione
    primaria si propaga al chiamante. La lista ricevuta non viene modificata.
    """
    percorso = Path(percorso)
    _valida_raccolta(materiali)
    temporaneo = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="",
            delete=False,
            dir=percorso.parent,
            prefix=percorso.name + ".",
            suffix=".tmp",
        ) as uscita:
            # delete=False: il temporaneo deve sopravvivere alla chiusura,
            # perché è la sostituzione finale a renderlo archivio.
            temporaneo = Path(uscita.name)
            scrittore = csv.writer(uscita, lineterminator="\n")
            scrittore.writerow(CAMPI_MATERIALE)
            for materiale in materiali:
                scrittore.writerow(materiale_a_riga(materiale))
        temporaneo.replace(percorso)
    except Exception as errore:
        if temporaneo is not None:
            try:
                temporaneo.unlink()
            except OSError:
                # La pulizia non deve nascondere il guasto primario: si lascia
                # una nota sul residuo e si rilancia l'errore originario.
                errore.add_note(f"temporaneo non rimosso: {temporaneo}")
        raise
    return None


if __name__ == "__main__":
    # Dimostrazione minima sotto guardia: rilettura dopo la riscrittura.
    import os
    import sys

    if len(sys.argv) != 2:
        print("uso: python persistenza_archivio_u12.py <archivio.csv>")
        raise SystemExit(2)
    sorgente = Path(sys.argv[1])
    destinazione = Path(str(sorgente) + ".copia.csv")
    materiali = carica_materiali(sorgente)
    print(f"caricati {len(materiali)} materiali da {sorgente}")
    salva_materiali(destinazione, materiali)
    print(f"archivio riscritto in {destinazione}")
    print("uguale all'originale:", sorgente.read_bytes() == destinazione.read_bytes())
    os.remove(destinazione)
