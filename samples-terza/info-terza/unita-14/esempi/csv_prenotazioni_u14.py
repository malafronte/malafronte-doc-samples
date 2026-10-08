"""Persistenza CSV delle prenotazioni: schema, conversioni e import/export (OOP-04, sez. G).

Il file è la fotografia di un registro: una riga per prenotazione, con i
cinque dati separati da virgole. Lo schema è dichiarato, non scoperto:

| Campo | Contenuto |
|---|---|
| `codice` | testo, confronto esatto |
| `aula` | testo, confronto esatto |
| `inizio_min` | minuti da mezzanotte, testo convertito in intero |
| `fine_min` | minuti da mezzanotte, testo convertito in intero |
| `partecipanti` | intero positivo |

La riga non contiene un `Intervallo` serializzato implicitamente: inizio e
fine sono due colonne, e il valore composito viene **costruito** dal
dominio dopo la conversione. Campo testuale → numero convertito → oggetto
costruito sono tre passaggi distinti, con diagnosi distinte.

Politiche (le stesse già adottate dal corso in PY-20 e U13): lettura con
`csv.reader`, `newline=""` e `utf-8-sig` (accetta il BOM quando c'è);
scrittura UTF-8 **senza** BOM su file temporaneo nella stessa directory,
chiusura e sostituzione finale. Se la scrittura fallisce, il file
precedente resta com'era.

L'**importazione** segue la politica del lotto: tutte le righe vengono
lette e convertite in candidati; poi una sola chiamata a
`registra_lotto` decide per intero. Un duplicato, un conflitto o un record
invalido impedisce la sostituzione e il registro resta intatto. Questo
comportamento è diverso dal rifiuto locale con prosecuzione del problema
U13-T09: qui non esistono importazioni parziali.

Questo componente **non scrive mai** nella lista interna del registro e non
conosce percorsi di dominio: riceve un percorso e un registro, usa le loro
operazioni pubbliche.

Ambiente: CPython sul computer. Dipende da `Prenotazione`, `Intervallo` e
dal registro.
"""

import csv
import os
from pathlib import Path

from intervalli_u14 import Intervallo
from prenotazioni_u14 import Prenotazione, RegistroPrenotazioni

CAMPI_PRENOTAZIONE = ("codice", "aula", "inizio_min", "fine_min", "partecipanti")


def _valida_intestazione(intestazione):
    """Controlla l'intestazione del file CSV. Nessun risultato."""
    if tuple(intestazione) != CAMPI_PRENOTAZIONE:
        attesi = ", ".join(CAMPI_PRENOTAZIONE)
        ricevuti = ", ".join(intestazione)
        raise ValueError(f"intestazione non valida: attesi ({attesi}), ricevuti ({ricevuti})")
    return None


def _intero_da_testo(testo, campo, riferimento):
    """Converte un campo testuale in intero, con diagnosi di campo e riga."""
    try:
        return int(testo)
    except ValueError:
        raise ValueError(
            f"{riferimento}, campo '{campo}': il testo {testo!r} non è un intero"
        ) from None


def riga_a_prenotazione(riga, riferimento_riga):
    """Converte una riga di campi testuali in una `Prenotazione` valida.

    Il numero di campi, le conversioni e i domini vengono controllati in
    quest'ordine; gli errori nominano riga e campo responsabile. La
    costruzione dell'oggetto avviene per ultima: un candidato invalido non
    esiste come valore.
    """
    if len(riga) != len(CAMPI_PRENOTAZIONE):
        attesi = ", ".join(CAMPI_PRENOTAZIONE)
        raise ValueError(
            f"{riferimento_riga}: attesi {len(CAMPI_PRENOTAZIONE)} campi ({attesi}), "
            f"ricevuti {len(riga)}"
        )
    codice = riga[0]
    aula = riga[1]
    inizio_min = _intero_da_testo(riga[2], "inizio_min", riferimento_riga)
    fine_min = _intero_da_testo(riga[3], "fine_min", riferimento_riga)
    partecipanti = _intero_da_testo(riga[4], "partecipanti", riferimento_riga)
    try:
        intervallo = Intervallo(inizio_min, fine_min)
        return Prenotazione(codice, aula, intervallo, partecipanti)
    except ValueError as errore:
        raise ValueError(f"{riferimento_riga}: {errore}") from None


def prenotazione_a_riga(prenotazione):
    """Proietta una prenotazione nei cinque campi testuali dello schema.

    Proiezione esplicita: i campi del file sono scelti uno per uno, non
    esportati in blocco. Il chiamante riceve una lista nuova di stringhe.
    """
    return [
        prenotazione.codice,
        prenotazione.aula,
        str(prenotazione.intervallo.inizio_min),
        str(prenotazione.intervallo.fine_min),
        str(prenotazione.partecipanti),
    ]


def leggi_candidati(percorso):
    """Legge il file e restituisce la lista dei candidati `Prenotazione`.

    Solleva `FileNotFoundError` se il file non esiste e `ValueError` per
    intestazione, conversioni o domini invalidi, con il riferimento della
    riga. Nessuna scrittura, nessuna modifica al registro.
    """
    with open(percorso, encoding="utf-8-sig", newline="") as flusso:
        lettore = csv.reader(flusso)
        try:
            intestazione = next(lettore)
        except StopIteration:
            raise ValueError("file senza intestazione") from None
        _valida_intestazione(intestazione)
        candidati = []
        for numero, riga in enumerate(lettore, start=2):
            riferimento = f"riga {numero}"
            if riga == []:
                raise ValueError(f"{riferimento}: riga vuota")
            candidati.append(riga_a_prenotazione(riga, riferimento))
    return candidati


def importa_lotto(percorso, registro):
    """Importa l'intero file nel registro: tutto o nulla.

    Legge e converte tutte le righe in candidati, poi chiama una sola volta
    `registra_lotto`. In caso di rifiuto l'eccezione sale al chiamante e il
    registro conserva lo stato precedente. `None` sul successo.
    """
    candidati = leggi_candidati(percorso)
    registro.registra_lotto(candidati)
    return None


def esporta_registro(percorso, registro):
    """Scrive il registro su file CSV con la sostituzione protetta.

    Prima scrive un temporaneo nella stessa directory del destino, lo
    chiude e solo allora lo sostituisce: se la scrittura fallisce, il file
    precedente resta integro, il temporaneo viene rimosso e l'errore sale
    al chiamante. Il registro non apre file e non conosce percorsi: è
    questo componente a proiettare i valori con `prenotazione_a_riga`.
    """
    percorso = Path(percorso)
    temporaneo = percorso.with_name(percorso.name + ".tmp")
    try:
        with open(temporaneo, "w", encoding="utf-8", newline="") as flusso:
            scrittore = csv.writer(flusso)
            scrittore.writerow(CAMPI_PRENOTAZIONE)
            for prenotazione in registro.prenotazioni():
                scrittore.writerow(prenotazione_a_riga(prenotazione))
        os.replace(temporaneo, percorso)
    except Exception as errore:
        try:
            temporaneo.unlink()
        except OSError:
            errore.add_note(f"temporaneo non rimosso: {temporaneo}")
        raise
    return None


if __name__ == "__main__":
    import tempfile

    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("PR-01", "Lab A", Intervallo(540, 600), 20))
    registro.registra(Prenotazione("PR-02", "Lab A", Intervallo(600, 660), 18))

    with tempfile.TemporaryDirectory() as cartella:
        archivio = Path(cartella) / "prenotazioni.csv"
        esporta_registro(archivio, registro)
        print("contenuto esportato:")
        print(archivio.read_text(encoding="utf-8"), end="")

        print("round-trip su un registro nuovo:")
        altro = RegistroPrenotazioni()
        importa_lotto(archivio, altro)
        print(altro.riepilogo()["numero_prenotazioni"], "prenotazioni")

        conflittuale = Path(cartella) / "lotto_conflitto.csv"
        conflittuale.write_text(
            "codice,aula,inizio_min,fine_min,partecipanti\n"
            "PR-09,Lab C,540,600,5\n"
            "PR-10,Lab A,570,630,5\n",
            encoding="utf-8",
        )
        try:
            importa_lotto(conflittuale, registro)
        except Exception as errore:  # ConflittoPrenotazione, mostrata in pagina
            print("importazione rifiutata:", type(errore).__name__, "-", errore)
        print("registro invariato:", registro.riepilogo()["numero_prenotazioni"])
