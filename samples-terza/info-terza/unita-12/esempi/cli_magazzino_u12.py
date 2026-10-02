"""CLI del magazzino: menu, stato di sessione e salvataggio esplicito.

Questo modulo presenta l'interfaccia a riga di comando del magazzino. Le
decisioni sui dati appartengono al modulo di dominio, la lettura e la
scrittura del file al modulo di persistenza; qui restano il menu, i messaggi,
il flag delle modifiche pendenti e il recupero dagli errori.

Stato della sessione: la lista `articoli` e il flag `modificato`. Il flag
diventa `True` solo quando un'operazione è **riuscita** e torna `False` solo
dopo un salvataggio riuscito. Il salvataggio non è automatico: la voce "6"
salva e resta nel menu, la voce "0" salva (se serve) e termina. Se il
salvataggio fallisce i dati restano in memoria e il menu continua: non si
esce mai dichiarando salvato ciò che non lo è.

Fine della sessione: la voce "0" è l'unico modo di terminare con salvataggio.
Se l'input si interrompe (EOF) il programma segnala l'interruzione, termina
**senza scrittura implicita** e avvisa se restano modifiche in memoria.

Codici di uscita: 0 sessione terminata con la voce "0", 1 interruzione per
fine dell'input oppure archivio non valido all'avvio, 2 argomenti non validi.

Ambiente: CPython sul computer. La guardia `if __name__ == "__main__"` è
l'unico punto che avvia il menu: importare questo modulo non produce domande
né scritture.
"""

import csv
import sys
from pathlib import Path

from dominio_magazzino_u12 import cerca_articolo
from dominio_magazzino_u12 import elimina_articolo
from dominio_magazzino_u12 import formatta_centesimi
from dominio_magazzino_u12 import inserisci_articolo
from dominio_magazzino_u12 import modifica_articolo
from dominio_magazzino_u12 import riga_a_articolo
from dominio_magazzino_u12 import riepilogo_magazzino
from persistenza_magazzino_u12 import carica_articoli
from persistenza_magazzino_u12 import salva_articoli

MENU = """\
1 - elenco e riepilogo
2 - ricerca per codice
3 - inserimento
4 - aggiornamento
5 - eliminazione
6 - salvataggio
0 - salvataggio e uscita"""


def riga_articolo(articolo):
    """Restituisce la riga di presentazione di un articolo. Non stampa."""
    prezzo = formatta_centesimi(articolo["prezzo_centesimi"])
    return f"{articolo['codice']} - {articolo['descrizione']} - quantita {articolo['quantita']} - prezzo {prezzo}"


def righe_situazione(articoli):
    """Restituisce le righe dell'elenco e del riepilogo. Non stampa."""
    righe = []
    if not articoli:
        righe.append("(magazzino vuoto)")
    for articolo in articoli:
        righe.append(riga_articolo(articolo))
    riepilogo = riepilogo_magazzino(articoli)
    righe.append(f"articoli: {riepilogo['articoli']}")
    righe.append(f"quantita complessiva: {riepilogo['quantita_totale']}")
    valore = riepilogo["valore_centesimi"]
    righe.append(f"valore complessivo: {valore} centesimi = {formatta_centesimi(valore)}")
    return righe


def leggi_articolo_da_tastiera(codice):
    """Legge i tre campi modificabili e costruisce il record candidato.

    Usa `riga_a_articolo` per la conversione e la validazione, con il
    riferimento "dati inseriti": così la CLI mostra le stesse diagnosi del
    caricamento dal file. Un dato non valido solleva `ValueError` prima che
    l'operazione venga tentata.
    """
    descrizione = input("descrizione> ")
    quantita = input("quantita> ")
    prezzo = input("prezzo_centesimi> ")
    return riga_a_articolo([codice, descrizione, quantita, prezzo], "dati inseriti")


def main(argv=None):
    """Coordina caricamento, menu, flag delle modifiche e salvataggio.

    `argv` è la lista degli argomenti della riga di comando (senza il nome del
    programma): serve esattamente un argomento, il percorso dell'archivio.
    """
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 1:
        print("uso: python cli_magazzino_u12.py <archivio.csv>")
        return 2
    percorso = Path(argv[0])
    try:
        articoli = carica_articoli(percorso)
        print(f"archivio caricato: {len(articoli)} articoli da {percorso}")
    except FileNotFoundError:
        print(f"archivio assente: si parte con un magazzino vuoto ({percorso})")
        articoli = []
    except UnicodeDecodeError as errore:
        # UnicodeDecodeError è una sottoclasse di ValueError: il gestore
        # specifico deve precedere quello generico.
        print(f"archivio non leggibile come UTF-8: {errore}")
        return 1
    except csv.Error as errore:
        print(f"archivio CSV malformato: {errore}")
        return 1
    except ValueError as errore:
        print(f"archivio non valido: {errore}")
        print("nessun dato caricato: correggere il file prima di ripartire")
        return 1
    except OSError as errore:
        print(f"errore di accesso all'archivio: {errore}")
        return 1

    modificato = False
    while True:
        print(MENU)
        try:
            scelta = input("scelta> ").strip()
            match scelta:
                case "1":
                    for riga in righe_situazione(articoli):
                        print(riga)
                case "2":
                    codice = input("codice> ").strip()
                    indice = cerca_articolo(articoli, codice)
                    if indice is None:
                        print(f"articolo assente: nessun codice {codice!r}")
                    else:
                        print(f"articolo presente in posizione {indice}")
                        print(riga_articolo(articoli[indice]))
                case "3":
                    codice = input("codice> ").strip()
                    try:
                        articolo = leggi_articolo_da_tastiera(codice)
                        inserisci_articolo(articoli, articolo)
                    except ValueError as errore:
                        print(f"inserimento rifiutato: {errore}")
                    else:
                        modificato = True
                        print(f"articolo {codice!r} inserito")
                case "4":
                    codice = input("codice> ").strip()
                    try:
                        candidato = leggi_articolo_da_tastiera(codice)
                        applicato = modifica_articolo(
                            articoli,
                            codice,
                            candidato["descrizione"],
                            candidato["quantita"],
                            candidato["prezzo_centesimi"],
                        )
                    except ValueError as errore:
                        print(f"aggiornamento rifiutato: {errore}")
                    else:
                        if applicato:
                            modificato = True
                            print(f"articolo {codice!r} aggiornato")
                        else:
                            print(f"articolo assente: nessun codice {codice!r}")
                case "5":
                    codice = input("codice> ").strip()
                    if cerca_articolo(articoli, codice) is None:
                        print(f"articolo assente: nessun codice {codice!r}")
                    else:
                        print(riga_articolo(articoli[cerca_articolo(articoli, codice)]))
                        conferma = input("conferma l'eliminazione? (s/n) ").strip().casefold()
                        if conferma == "s":
                            elimina_articolo(articoli, codice)
                            modificato = True
                            print(f"articolo {codice!r} eliminato")
                        else:
                            print("eliminazione annullata")
                case "6":
                    try:
                        salva_articoli(percorso, articoli)
                    except (OSError, csv.Error, ValueError) as errore:
                        print(f"salvataggio non riuscito: {errore}")
                        print("le modifiche restano in memoria")
                    else:
                        modificato = False
                        print(f"archivio salvato: {percorso}")
                case "0":
                    if not modificato:
                        print("chiusura senza modifiche pendenti")
                        return 0
                    try:
                        salva_articoli(percorso, articoli)
                    except (OSError, csv.Error, ValueError) as errore:
                        print(f"salvataggio non riuscito: {errore}")
                        print("si resta nel menu con le modifiche in memoria")
                    else:
                        modificato = False
                        print(f"archivio salvato: {percorso}")
                        return 0
                case _:
                    print(f"comando non riconosciuto: {scelta!r}")
        except EOFError:
            print("sessione interrotta: l'input è terminato")
            if modificato:
                print("attenzione: restano modifiche non salvate in memoria")
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
