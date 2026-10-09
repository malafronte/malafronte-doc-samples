"""CLI del magazzino composto: stesso menu funzionale, nuova delega (OOP-04).

Il menu, i messaggi e le politiche di salvataggio sono **gli stessi della
versione U13**: `"1"` elenco e riepilogo, `"2"` ricerca per codice, `"3"`
inserimento, `"4"` aggiornamento, `"5"` eliminazione con conferma, `"6"`
salvataggio, `"0"` salvataggio e uscita. Restano il flag delle modifiche
pendenti, il carico singolo all'avvio, la distinzione fra file assente e
file corrotto e il ritorno al menu quando il salvataggio di uscita fallisce.

Che cosa cambia: la sessione conserva un **`Magazzino`** invece di una lista
e chiama le sue operazioni pubbliche. L'inserimento legge quattro dati e
affida alla raccolta costruzione e unicità; la ricerca restituisce lo
snapshot `DatiArticolo`; la modifica passa per `Magazzino.modifica`. La
funzione `formatta_centesimi` resta una funzione di modulo: una conversione
pura non guadagna a diventare un metodo.

Stato della sessione: il magazzino e il flag `modificato`, che diventa
`True` solo dopo un'operazione riuscita e torna `False` solo dopo un
salvataggio riuscito. Nessuna uscita che dichiari salvato ciò che non lo è.

Codici di uscita: 0 sessione terminata con la voce "0", 1 interruzione per
fine dell'input oppure archivio non valido all'avvio, 2 argomenti non
validi.

Ambiente: CPython sul computer. La guardia `if __name__ == "__main__"` è
l'unico punto che avvia il menu.
"""

import csv
import sys
from pathlib import Path

from magazzino_composto_u14 import Magazzino
from persistenza_magazzino_u14 import (
    carica_magazzino,
    riga_a_dati,
    salva_magazzino,
)

MENU = """\
1 - elenco e riepilogo
2 - ricerca per codice
3 - inserimento
4 - aggiornamento
5 - eliminazione
6 - salvataggio
0 - salvataggio e uscita"""


def formatta_centesimi(centesimi):
    """Formatta i centesimi come euro. Funzione pura, nessun stato."""
    segni = "-" if centesimi < 0 else ""
    return f"{segni}{abs(centesimi) // 100},{abs(centesimi) % 100:02d} €"


def riga_articolo(dat):
    """Riga di presentazione di uno snapshot `DatiArticolo`. Non stampa."""
    prezzo = formatta_centesimi(dat.prezzo_centesimi)
    return f"{dat.codice} - {dat.descrizione} - quantita {dat.quantita} - prezzo {prezzo}"


def righe_situazione(magazzino):
    """Restituisce le righe dell'elenco e del riepilogo. Non stampa."""
    righe = []
    proiezioni = magazzino.articoli()
    if not proiezioni:
        righe.append("(magazzino vuoto)")
    for dat in proiezioni:
        righe.append(riga_articolo(dat))
    riepilogo = magazzino.riepilogo()
    righe.append(f"articoli: {riepilogo['articoli']}")
    righe.append(f"quantita complessiva: {riepilogo['quantita_totale']}")
    valore = riepilogo["valore_centesimi"]
    righe.append(f"valore complessivo: {valore} centesimi = {formatta_centesimi(valore)}")
    return righe


def leggi_articolo_da_tastiera(codice):
    """Legge i tre campi modificabili e restituisce i quattro dati del candidato.

    Usa `riga_a_dati` per le conversioni numeriche, con il riferimento
    "dati inseriti": la CLI mostra le stesse diagnosi di conversione del
    caricamento dal file. Il magazzino controlla i domini prima di
    modificare lo stato; la tupla comprende anche il codice ricevuto.
    """
    descrizione = input("descrizione> ")
    quantita = input("quantita> ")
    prezzo_centesimi = input("prezzo_centesimi> ")
    return riga_a_dati([codice, descrizione, quantita, prezzo_centesimi], "dati inseriti")


def main(argv=None):
    """Coordina caricamento, menu, flag delle modifiche e salvataggio."""
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 1:
        print("uso: python cli_magazzino_u14.py <archivio.csv>")
        return 2
    percorso = Path(argv[0])
    try:
        magazzino = carica_magazzino(percorso)
        totale = magazzino.riepilogo()["articoli"]
        print(f"archivio caricato: {totale} articoli da {percorso}")
    except FileNotFoundError:
        print(f"archivio assente: si parte con un magazzino vuoto ({percorso})")
        magazzino = Magazzino()
    except UnicodeDecodeError as errore:
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
                    for riga in righe_situazione(magazzino):
                        print(riga)
                case "2":
                    codice = input("codice> ").strip()
                    trovato = magazzino.cerca(codice)
                    if trovato is None:
                        print(f"articolo assente: nessun codice {codice!r}")
                    else:
                        print("articolo presente")
                        print(riga_articolo(trovato))
                case "3":
                    codice = input("codice> ").strip()
                    try:
                        codice, descrizione, quantita, prezzo = leggi_articolo_da_tastiera(codice)
                        magazzino.inserisci(codice, descrizione, quantita, prezzo)
                    except ValueError as errore:
                        print(f"inserimento rifiutato: {errore}")
                    else:
                        modificato = True
                        print(f"articolo {codice!r} inserito")
                case "4":
                    codice = input("codice> ").strip()
                    try:
                        codice, descrizione, quantita, prezzo = leggi_articolo_da_tastiera(codice)
                        applicato = magazzino.modifica(codice, descrizione, quantita, prezzo)
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
                    trovato = magazzino.cerca(codice)
                    if trovato is None:
                        print(f"articolo assente: nessun codice {codice!r}")
                    else:
                        print(riga_articolo(trovato))
                        conferma = input("conferma l'eliminazione? (s/n) ").strip().casefold()
                        if conferma == "s":
                            magazzino.elimina(codice)
                            modificato = True
                            print(f"articolo {codice!r} eliminato")
                        else:
                            print("eliminazione annullata")
                case "6":
                    try:
                        salva_magazzino(percorso, magazzino)
                    except (OSError, csv.Error, ValueError) as errore:
                        print(f"salvataggio non riuscito: {errore}")
                        for nota in getattr(errore, "__notes__", []):
                            print(nota)
                        print("le modifiche restano in memoria")
                    else:
                        modificato = False
                        print(f"archivio salvato: {percorso}")
                case "0":
                    if not modificato:
                        print("chiusura senza modifiche pendenti")
                        return 0
                    try:
                        salva_magazzino(percorso, magazzino)
                    except (OSError, csv.Error, ValueError) as errore:
                        print(f"salvataggio non riuscito: {errore}")
                        for nota in getattr(errore, "__notes__", []):
                            print(nota)
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
