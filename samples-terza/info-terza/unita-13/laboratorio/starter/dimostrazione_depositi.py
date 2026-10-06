"""Dimostrazione dei casi pubblici del laboratorio LAB-PY-U13.

Questo script esegue i **casi pubblici LAB13-01…LAB13-12** sulla versione
procedurale e ne stampa la trascrizione. Serve a due scopi:

- osservare il comportamento atteso **prima** di scrivere la classe;
- avere un oracolo di confronto: la variante a oggetti deve produrre gli
  stessi risultati e gli stessi stati per ogni passo.

Il file è una cornice di esecuzione, non la soluzione del laboratorio. Non
contiene classi: la classe `Deposito` va scritta dallo studente e verificata
con una propria suite.

Ambiente: CPython sul computer, dalla directory che contiene questo file:

    python dimostrazione_depositi.py

La trascrizione è deterministica: la stessa esecuzione produce sempre lo
stesso elenco di righe.
"""

from depositi_procedurali import carica, nuovo_deposito, preleva, situazione, spazio_libero


def mostra(titolo, righe):
    """Stampa un blocco della trascrizione con un'intestazione."""
    print(f"--- {titolo} ---")
    for riga in righe:
        print(riga)
    print()


def caso_costruzione(titolo, etichetta, capacita, quantita):
    """LAB13-01…LAB13-04: costruzioni valide e rifiutate."""
    righe = []
    try:
        deposito = nuovo_deposito(etichetta, capacita, quantita)
    except ValueError as errore:
        righe.append(f"rifiuto: {errore}")
        righe.append("nessun deposito prodotto")
    else:
        righe.append(f"deposito: {situazione(deposito)}")
        righe.append(f"spazio libero: {spazio_libero(deposito)}")
    mostra(titolo, righe)


def caso_operazione(titolo, capacita, quantita, operazione, unita):
    """LAB13-05…LAB13-10: carichi e prelievi con i loro esiti."""
    righe = []
    deposito = nuovo_deposito("kit-a", capacita, quantita)
    righe.append(f"prima: {situazione(deposito)}")
    try:
        esito = operazione(deposito, unita)
    except ValueError as errore:
        righe.append(f"errore di input: {errore}")
        righe.append(f"dopo: {situazione(deposito)} (invariato)")
    else:
        righe.append(f"risultato: {esito}")
        righe.append(f"dopo: {situazione(deposito)}")
    mostra(titolo, righe)


def caso_indipendenza():
    """LAB13-11: due depositi indipendenti e un alias."""
    primo = nuovo_deposito("kit-a", 5, 0)
    secondo = nuovo_deposito("kit-b", 5, 0)
    alias = primo
    carica(primo, 3)
    carica(secondo, 1)
    righe = [
        f"primo:   {situazione(primo)}",
        f"secondo: {situazione(secondo)}",
        f"alias è primo: {alias is primo}",
        f"alias dopo il carico su primo: {situazione(alias)}",
        "mutare attraverso l'alias si vede da ogni nome collegato",
    ]
    mostra("LAB13-11 - istanze indipendenti e alias", righe)


def caso_equivalenza():
    """LAB13-12: la sequenza canonica e i suoi esiti attesi."""
    deposito = nuovo_deposito("kit-a", 5, 0)
    sequenza = (
        ("carica", 3, True, {"etichetta": "kit-a", "capacita": 5, "quantita": 3}),
        ("preleva", 4, False, {"etichetta": "kit-a", "capacita": 5, "quantita": 3}),
        ("carica", 2, True, {"etichetta": "kit-a", "capacita": 5, "quantita": 5}),
        ("carica", 1, False, {"etichetta": "kit-a", "capacita": 5, "quantita": 5}),
        ("preleva", 5, True, {"etichetta": "kit-a", "capacita": 5, "quantita": 0}),
        ("carica", 0, True, {"etichetta": "kit-a", "capacita": 5, "quantita": 0}),
    )
    righe = []
    tutti_corretti = True
    for operazione, unita, risultato_atteso, stato_atteso in sequenza:
        funzione = carica if operazione == "carica" else preleva
        risultato = funzione(deposito, unita)
        stato = situazione(deposito)
        coerente = risultato == risultato_atteso and stato == stato_atteso
        tutti_corretti = tutti_corretti and coerente
        righe.append(
            f"{operazione}({unita}) -> {risultato} atteso {risultato_atteso}, "
            f"stato {stato} atteso {stato_atteso}, coerente: {coerente}"
        )
    righe.append(f"sequenza interamente coerente: {tutti_corretti}")
    mostra("LAB13-12 - sequenza canonica ed equivalenza", righe)


def main():
    """Esegue tutti i casi pubblici nell'ordine del documento del laboratorio."""
    caso_costruzione("LAB13-01 - capacita 5, quantita 0", "kit-a", 5, 0)
    caso_costruzione("LAB13-02 - capacita 0", "kit-a", 0, 0)
    caso_costruzione("LAB13-03a - quantita iniziale al confine inferiore", "kit-a", 5, 0)
    caso_costruzione("LAB13-03b - quantita iniziale al confine superiore", "kit-a", 5, 5)
    caso_costruzione("LAB13-04 - quantita iniziale invalida", "kit-a", 5, 6)
    caso_operazione("LAB13-05 - carico esatto", 5, 3, carica, 2)
    caso_operazione("LAB13-06 - carico oltre limite", 5, 3, carica, 3)
    caso_operazione("LAB13-07 - prelievo esatto", 5, 3, preleva, 3)
    caso_operazione("LAB13-08 - prelievo oltre disponibilita", 5, 3, preleva, 4)
    caso_operazione("LAB13-09a - carico negativo", 5, 3, carica, -1)
    caso_operazione("LAB13-09b - carico booleano", 5, 3, carica, True)
    caso_operazione("LAB13-10 - carico di zero unita", 5, 3, carica, 0)
    caso_indipendenza()
    caso_equivalenza()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
