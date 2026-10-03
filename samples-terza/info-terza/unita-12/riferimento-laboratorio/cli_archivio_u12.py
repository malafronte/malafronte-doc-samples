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

Ambiente: CPython sul computer. Le funzioni di presentazione sono pure e non
leggono input: la sola `main` pone domande, e solo sotto la guardia di avvio.
"""

import csv
import sys

from dominio_archivio_u12 import cerca_materiale
from dominio_archivio_u12 import elimina_materiale
from dominio_archivio_u12 import inserisci_materiale
from dominio_archivio_u12 import modifica_materiale
from dominio_archivio_u12 import riepilogo_archivio
from persistenza_archivio_u12 import carica_materiali
from persistenza_archivio_u12 import salva_materiali


def mostra_menu():
    """Restituisce le righe del menu come testo, senza stamparle."""
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
    """Restituisce la riga di testo di un record, senza stamparla."""
    return f"{materiale['codice']} | {materiale['descrizione']} | {materiale['quantita']}"


def righe_situazione(materiali):
    """Restituisce le righe dell'elenco con il riepilogo, senza stamparle."""
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
    if len(argv) != 2:
        print("uso: python cli_archivio_u12.py <archivio.csv>")
        return 2
    percorso = argv[1]
    try:
        materiali = carica_materiali(percorso)
    except FileNotFoundError:
        print(f"archivio assente: {percorso} non esiste, si parte con la raccolta vuota")
        materiali = []
    except (UnicodeDecodeError, csv.Error, ValueError) as errore:
        print(f"archivio non valido: {errore}")
        print("nessuna modifica intrapresa: correggere il file e riprovare")
        return 1

    modificato = False
    try:
        while True:
            print()
            print(mostra_menu())
            scelta = input("scelta> ").strip()
            match scelta:
                case "1":
                    for riga in righe_situazione(materiali):
                        print(riga)
                case "2":
                    codice = input("codice da cercare> ").strip()
                    indice = cerca_materiale(materiali, codice)
                    if indice is None:
                        print(f"materiale {codice!r} assente")
                    else:
                        print(f"materiale {codice!r} in posizione {indice}: {riga_materiale(materiali[indice])}")
                case "3":
                    codice = input("codice> ").strip()
                    descrizione = input("descrizione> ")
                    quantita_testo = input("quantita> ").strip()
                    try:
                        quantita = int(quantita_testo)
                    except ValueError:
                        print(f"quantita non valida: {quantita_testo!r} non è un intero")
                        continue
                    try:
                        inserisci_materiale(
                            materiali,
                            {"codice": codice, "descrizione": descrizione, "quantita": quantita},
                        )
                    except ValueError as errore:
                        print(f"inserimento rifiutato: {errore}")
                    else:
                        modificato = True
                        print(f"materiale {codice!r} inserito")
                case "4":
                    codice = input("codice da aggiornare> ").strip()
                    if cerca_materiale(materiali, codice) is None:
                        print(f"materiale {codice!r} assente")
                        continue
                    descrizione = input("nuova descrizione> ")
                    quantita_testo = input("nuova quantita> ").strip()
                    try:
                        quantita = int(quantita_testo)
                    except ValueError:
                        print(f"quantita non valida: {quantita_testo!r} non è un intero")
                        continue
                    try:
                        aggiornato = modifica_materiale(materiali, codice, descrizione, quantita)
                    except ValueError as errore:
                        print(f"aggiornamento rifiutato: {errore}")
                        print("il record precedente è rimasto invariato")
                    else:
                        if aggiornato:
                            modificato = True
                            print(f"materiale {codice!r} aggiornato")
                        else:
                            print(f"materiale {codice!r} assente")
                case "5":
                    codice = input("codice da eliminare> ").strip()
                    if cerca_materiale(materiali, codice) is None:
                        print(f"materiale {codice!r} assente")
                        continue
                    conferma = normalizza_conferma(input("conferma eliminazione (s/n)> "))
                    if conferma != "s":
                        print("eliminazione annullata")
                        continue
                    if elimina_materiale(materiali, codice):
                        modificato = True
                        print(f"materiale {codice!r} eliminato")
                case "6":
                    try:
                        salva_materiali(percorso, materiali)
                    except (OSError, ValueError, csv.Error) as errore:
                        print(f"salvataggio non riuscito: {errore}")
                        print("dati e modifiche pendenti restano in memoria")
                    else:
                        modificato = False
                        print(f"archivio salvato in {percorso}")
                case "0":
                    if modificato:
                        try:
                            salva_materiali(percorso, materiali)
                        except (OSError, ValueError, csv.Error) as errore:
                            print(f"salvataggio non riuscito: {errore}")
                            print("si resta nel menu con i dati ancora in memoria")
                            continue
                        modificato = False
                        print(f"archivio salvato in {percorso}")
                    print("sessione terminata")
                    return 0
                case _:
                    print(f"comando sconosciuto: {scelta!r}")
    except EOFError:
        # L'interruzione riguarda l'intera sessione, anche i campi e le conferme.
        print("sessione interrotta: fine dell'input")
        if modificato:
            print("avviso: restano modifiche non salvate in memoria")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
