"""CLI dimostrativa: importa il modulo riusabile e presenta gli stessi dati.

Questo file è la parte **presentazione** del piccolo progetto: contiene
`input` e `print`, ma soltanto dentro `main()`. La guardia
`if __name__ == "__main__"` fa sì che l'import del modulo non avvii domande:
`import demo_import_u12` definisce le funzioni e non produce output.

Dipendenze: `random` della libreria standard e il modulo proprio
`utilita_u12`. La direzione degli import è CLI -> calcolo: `utilita_u12`
non importa nulla di questo file e non può creare un ciclo.

Ambiente: CPython sul computer, esecuzione dalla cartella `esempi/`.
"""

import random

from utilita_u12 import valore_magazzino

DESCRIZIONI = ["Vite lunga", "Caffè A", "Resistore 10k", "LED rosso", "Morsettiera"]


def genera_inventario(seed=7, numero=4):
    """Restituisce `numero` record di prova riproducibili con il seme dato.

    Ogni record ha `codice` (stringa con zeri iniziali), `descrizione`,
    `quantita` e `prezzo_centesimi`. Con lo stesso seme e lo stesso numero la
    sequenza è la stessa nella versione di CPython verificata dal corso: la
    riproducibilità si verifica con una coppia di chiamate, non si promette
    per qualunque versione futura del modulo `random`.
    """
    generatore = random.Random(seed)
    articoli = []
    for indice in range(numero):
        articoli.append(
            {
                "codice": f"{indice + 1:03d}",
                "descrizione": DESCRIZIONI[indice % len(DESCRIZIONI)],
                "quantita": generatore.randint(0, 20),
                "prezzo_centesimi": generatore.randint(1, 900),
            }
        )
    return articoli


def presentazione_riga(articoli):
    """Prima presentazione: un articolo per riga e il valore complessivo.

    La funzione formatta soltanto: il calcolo del totale resta di
    `valore_magazzino`, che viene chiamato e non duplicato.
    """
    righe = []
    for articolo in articoli:
        righe.append(
            f"{articolo['codice']} {articolo['descrizione']}: "
            f"{articolo['quantita']} pz x {articolo['prezzo_centesimi']} cent"
        )
    righe.append(f"valore complessivo: {valore_magazzino(articoli)} centesimi")
    return "\n".join(righe)


def presentazione_tabella(articoli):
    """Seconda presentazione: colonne allineate e lo stesso valore complessivo.

    Anche qui il totale arriva da `valore_magazzino`: cambiare presentazione
    non cambia il calcolo, e le due presentazioni mostrano lo stesso numero.
    """
    righe = ["codice  descrizione         quantita  prezzo  valore"]
    for articolo in articoli:
        valore = articolo["quantita"] * articolo["prezzo_centesimi"]
        righe.append(
            f"{articolo['codice']:>6}  {articolo['descrizione']:<18}"
            f"  {articolo['quantita']:>8}  {articolo['prezzo_centesimi']:>6}"
            f"  {valore:>6}"
        )
    righe.append(f"valore complessivo: {valore_magazzino(articoli)} centesimi")
    return "\n".join(righe)


def main():
    """Coordina la sessione dimostrativa: menu, scelta e presentazione."""
    articoli = genera_inventario()
    print("Inventario di prova con seme 7 (stessi dati a ogni esecuzione).")
    while True:
        print("1 - presentazione per riga")
        print("2 - presentazione a tabella")
        print("0 - termina")
        scelta = input("Scegli: ").strip()
        if scelta == "0":
            break
        if scelta == "1":
            print(presentazione_riga(articoli))
        elif scelta == "2":
            print(presentazione_tabella(articoli))
        else:
            print("comando non riconosciuto")


if __name__ == "__main__":
    main()
