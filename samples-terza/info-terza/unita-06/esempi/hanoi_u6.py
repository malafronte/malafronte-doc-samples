"""Generatore ricorsivo delle mosse della torre di Hanoi (Unità 6).

Collocare il file in `programmi/hanoi_u6.py` della raccolta.
Generazione e presentazione sono separate: la funzione non stampa,
accoda le mosse alla lista ricevuta e restituisce None.
Esecuzione: uv run python programmi/hanoi_u6.py
"""


def hanoi(
    n: int,
    origine: str,
    destinazione: str,
    appoggio: str,
    mosse: list[tuple[int, str, str]],
) -> None:
    """Accoda alla lista ricevuta le mosse del trasferimento di n dischi.

    Dominio: n intero non negativo; etichette dei tre pioli distinte;
    stato logico iniziale con n dischi ordinati sull'origine.
    Effetto: aggiunge 2**n - 1 tuple (disco, origine, destinazione) in coda,
    conservando l'eventuale prefisso già presente. Restituisce None.
    """
    if n == 0:
        return
    hanoi(n - 1, origine, appoggio, destinazione, mosse)
    mosse.append((n, origine, destinazione))
    hanoi(n - 1, appoggio, destinazione, origine, mosse)


if __name__ == "__main__":
    mosse = []
    hanoi(3, "A", "C", "B", mosse)
    print("numero di mosse:", len(mosse))
    for disco, origine, destinazione in mosse:
        print(f"sposta il disco {disco} da {origine} a {destinazione}")
