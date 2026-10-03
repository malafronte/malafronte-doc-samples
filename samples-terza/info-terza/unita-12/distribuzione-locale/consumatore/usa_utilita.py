"""Consumatore della libreria personale `utilita_magazzino_u12`.

Questo script vive in un progetto **diverso** da quello dell'autore: non
aggiunge la cartella dei sorgenti a `sys.path`, non contiene una copia del
codice della libreria e non sa dove si trovino i file di `autore/`. La libreria
è disponibile perché la wheel è stata installata nell'ambiente di questo
progetto: l'ultima riga della stampa mostra l'origine reale del package
importato, che è dentro la `.venv` del consumatore.

Esecuzione dalla cartella `consumatore/`:

    uv run python usa_utilita.py
"""

import utilita_magazzino_u12
from utilita_magazzino_u12 import formatta_centesimi
from utilita_magazzino_u12 import normalizza_codice
from utilita_magazzino_u12 import valore_magazzino

ARTICOLI = [
    {"codice": " 007 ", "descrizione": "Vite, lunga", "quantita": 4, "prezzo_centesimi": 25},
    {"codice": "012", "descrizione": 'Caffè "A"', "quantita": 2, "prezzo_centesimi": 350},
]


def main():
    print("versione del package:", utilita_magazzino_u12.__version__)
    print("origine del package:", utilita_magazzino_u12.__file__)
    totale_centesimi = valore_magazzino(ARTICOLI)
    print("valore complessivo:", totale_centesimi, "centesimi")
    print("valore formattato:", formatta_centesimi(totale_centesimi))
    for articolo in ARTICOLI:
        print("codice normalizzato:", normalizza_codice(articolo["codice"]))


if __name__ == "__main__":
    main()
