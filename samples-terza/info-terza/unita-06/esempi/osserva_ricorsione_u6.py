"""Osservare Fibonacci: ingressi totali e profondità massima (Unità 6).

Collocare il file in `programmi/osserva_ricorsione_u6.py` della raccolta.
È la strumentazione guidata del laboratorio LAB-PY-U6: una versione
dichiaratamente osservatoria della funzione pura, che non ne cambia il
contratto. La lista `statistiche` è [ingressi totali, profondità massima]
e va azzerata prima di ogni prova; il parametro profondita parte da 1
perché il primo frame ha profondità 1.
Esecuzione: uv run python programmi/osserva_ricorsione_u6.py
"""


def fibonacci_osservata(n: int, profondita: int = 1, statistiche: list[int] | None = None) -> int:
    """Restituisce F(n) aggiornando la lista statistiche ricevuta.

    Ogni ingresso conta una chiamata (basi comprese); la profondità del
    primo frame è 1 e ogni figlio riceve profondita + 1. La funzione non
    usa globali né closure: la lista condivisa è il modello di U5.
    """
    if statistiche is None:
        statistiche = [0, 0]
    statistiche[0] += 1
    statistiche[1] = max(statistiche[1], profondita)
    if n == 0:
        return 0
    if n == 1:
        return 1
    precedente = fibonacci_osservata(n - 1, profondita + 1, statistiche)
    ancora_precedente = fibonacci_osservata(n - 2, profondita + 1, statistiche)
    return precedente + ancora_precedente


if __name__ == "__main__":
    for n in (0, 1, 2, 4, 5, 10):
        statistiche = [0, 0]
        valore = fibonacci_osservata(n, 1, statistiche)
        print(
            f"F({n}) = {valore}, chiamate totali = {statistiche[0]}, profondità massima = {statistiche[1]}"
        )
    # Due prove consecutive ripartono da statistiche azzerate (L07).
    statistiche = [0, 0]
    fibonacci_osservata(4, 1, statistiche)
    print("prima prova:", statistiche)
    statistiche = [0, 0]
    print("dopo l'azzeramento:", statistiche == [0, 0])
    fibonacci_osservata(4, 1, statistiche)
    print("seconda prova:", statistiche)
