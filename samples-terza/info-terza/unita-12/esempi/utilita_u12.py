"""Modulo riusabile: calcolo del valore di un inventario già in memoria.

Questo modulo contiene **solo calcolo**: nessuna lettura, nessuna stampa,
nessuna domanda. Chi importa `utilita_u12` ottiene funzioni che ricevono dati
e restituiscono risultati, senza effetti osservabili sull'ambiente.

Contratto di `valore_magazzino`: l'argomento è una lista di record-dizionari
già validi, ciascuno con i campi `quantita` (intero maggiore o uguale a zero)
e `prezzo_centesimi` (intero maggiore o uguale a zero). Il risultato è il
valore complessivo **in centesimi**, come intero. La validazione dei campi
arriva con il cap. PY-18: qui la precondizione fa parte del contratto e il
modulo si fida del chiamante.

Ambiente: CPython sul computer. Nessuna lettura da tastiera, nessuna stampa.
"""


def valore_magazzino(articoli):
    """Restituisce in centesimi il valore complessivo dell'inventario.

    Precondizione: ogni record ha `quantita` e `prezzo_centesimi` interi
    maggiori o uguali a zero. L'argomento non viene modificato; il risultato è
    sempre un intero, anche per la lista vuota, dove vale 0.
    """
    totale_centesimi = 0
    for articolo in articoli:
        totale_centesimi += articolo["quantita"] * articolo["prezzo_centesimi"]
    return totale_centesimi


if __name__ == "__main__":
    # Dimostrazione minima: gli stessi dati della CLI dimostrativa.
    prova = [
        {"codice": "007", "descrizione": "Vite, lunga", "quantita": 4, "prezzo_centesimi": 25},
        {"codice": "012", "descrizione": 'Caffè "A"', "quantita": 2, "prezzo_centesimi": 350},
    ]
    print(f"valore complessivo: {valore_magazzino(prova)} centesimi")
