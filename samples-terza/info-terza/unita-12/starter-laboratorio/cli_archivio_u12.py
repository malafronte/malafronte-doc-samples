"""Interfaccia a riga di comando dell'archivio materiali del LAB-PY-U12.

Il modulo contiene la **presentazione e il coordinamento**: menu, messaggi,
domande, stato di sessione e scelta del recupero. La logica del dato resta in
`dominio_archivio_u12` e le operazioni di file in `persistenza_archivio_u12`:
le dipendenze vanno dalla CLI verso gli altri due moduli, mai in direzione
contraria.

Comandi del menu (scelte testuali, come nel cap. PY-05):

| Scelta | Comportamento |
|---|---|
| `1` | elenco e riepilogo; non modifica dati né flag |
| `2` | ricerca per codice; distingue presente, assente e posizione 0 |
| `3` | inserimento validato; il duplicato è rifiutato |
| `4` | aggiornamento di descrizione e quantità; il record invalido non è applicato neppure in parte |
| `5` | eliminazione per codice dopo conferma `s/n` |
| `6` | salvataggio esplicito; su successo il flag delle modifiche si azzera |
| `0` | uscita: con modifiche pendenti salva e termina solo su successo |
| altro | messaggio di comando sconosciuto, stato invariato |

Politica della sessione: la CLI tiene il flag `modificato` - `True` solo dopo
una mutazione riuscita, `False` solo dopo un salvataggio riuscito - e non lo
affida alle funzioni di persistenza. Alla fine dello stream di input la
sessione viene dichiarata **interrotta**: nessuna scrittura implicita, avviso
se restano modifiche non salvate. Codici di uscita: 0 uscita dalla voce `0`,
1 interruzione o archivio non valido, 2 uso errato.

Stato del file: **incompleto, e lo dichiara**. Le funzioni di presentazione
sono fornite complete; il corpo di `main` si completa nella fase L5 e si
affina nelle fasi L6 e L7. La sola `main` pone domande, e solo sotto la
guardia di avvio: importare questo modulo non chiede nulla.

Ambiente: CPython sul computer.
"""

# Gli import qui sotto sono quelli del corpo di `main` da completare: restano
# dichiarati anche finché il corpo è uno stub, e le marcature di esenzione lo
# dichiarano.
import csv  # noqa: F401
import sys

from dominio_archivio_u12 import cerca_materiale  # noqa: F401
from dominio_archivio_u12 import elimina_materiale  # noqa: F401
from dominio_archivio_u12 import inserisci_materiale  # noqa: F401
from dominio_archivio_u12 import modifica_materiale  # noqa: F401
from dominio_archivio_u12 import riepilogo_archivio
from persistenza_archivio_u12 import carica_materiali  # noqa: F401
from persistenza_archivio_u12 import salva_materiali  # noqa: F401


def mostra_menu():
    """Restituisce le righe del menu come testo, senza stamparle.

    Funzione **fornita completa**: si usa, non si riscrive.
    """
    return (
        "1 - elenco e riepilogo\n"
        "2 - ricerca per codice\n"
        "3 - inserimento\n"
        "4 - aggiornamento\n"
        "5 - eliminazione\n"
        "6 - salvataggio\n"
        "0 - uscita"
    )


def riga_materiale(materiale):
    """Restituisce la riga di testo di un record, senza stamparla.

    Funzione **fornita completa**: si usa, non si riscrive.
    """
    return f"{materiale['codice']} | {materiale['descrizione']} | {materiale['quantita']}"


def righe_situazione(materiali):
    """Restituisce le righe dell'elenco con il riepilogo, senza stamparle.

    Funzione **fornita completa**: si usa, non si riscrive.
    """
    righe = [riga_materiale(materiale) for materiale in materiali]
    if not righe:
        righe = ["(archivio vuoto)"]
    riepilogo = riepilogo_archivio(materiali)
    righe.append(
        f"materiali: {riepilogo['materiali']} - "
        f"quantita totale: {riepilogo['quantita_totale']}"
    )
    return righe


def normalizza_conferma(testo):
    """Riduce la risposta dell'utente a `s`, `n` oppure testo non ammesso.

    La convenzione della sessione è `s/n`, con `strip()` e `casefold()`;
    qualunque altra risposta viene normalizzata in `""` e non conferma.

    Funzione **fornita completa**: si usa, non si riscrive.
    """
    risposta = testo.strip().casefold()
    if risposta in ("s", "n"):
        return risposta
    return ""


def main(argv):
    """Coordina caricamento, menu, flag delle modifiche e recupero.

    `argv` segue la convenzione di `sys.argv`: `argv[1]` è il percorso
    dell'archivio. Restituisce il codice di uscita dichiarato nel docstring
    del modulo. La guardia `if __name__ == "__main__"` è l'unico avvio
    automatico: importare questo modulo non pone domande.
    """
    raise NotImplementedError("fase L5: coordinamento del menu, del flag e del recupero")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
