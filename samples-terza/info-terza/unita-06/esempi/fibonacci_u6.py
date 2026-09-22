"""Fibonacci ricorsivo e iterativo dell'Unità 6.

Collocare il file in `programmi/fibonacci_u6.py` della raccolta.
Le due versioni hanno lo stesso contratto e restituiscono un solo intero.
Esecuzione: uv run python programmi/fibonacci_u6.py
"""


def fibonacci_ric(n: int) -> int:
    """Restituisce F(n) secondo la definizione ricorsiva.

    Dominio: n intero non negativo. Due casi base: F(0) = 0, F(1) = 1.
    Il ramo non base esegue le due chiamate in sequenza, prima F(n-1)
    e poi F(n-2): la seconda inizia solo dopo il ritorno della prima.
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    precedente = fibonacci_ric(n - 1)
    ancora_precedente = fibonacci_ric(n - 2)
    return precedente + ancora_precedente


def fibonacci_iter(n: int) -> int:
    """Restituisce F(n) con la coppia di valori consecutivi già nota.

    Stesso dominio e stesso risultato della versione ricorsiva.
    La coppia (precedente, corrente) rappresenta F(i-1) e F(i)
    all'inizio di ogni iterazione con indice i.
    """
    if n <= 1:
        return n
    precedente = 0
    corrente = 1
    for indice in range(2, n + 1):
        successivo = precedente + corrente
        precedente = corrente
        corrente = successivo
    return corrente


if __name__ == "__main__":
    print("indice:  ", list(range(9)))
    print("ricorsiva:", [fibonacci_ric(n) for n in range(9)])
    print("iterativa:", [fibonacci_iter(n) for n in range(9)])
    print("concordano fino a 15:", all(fibonacci_ric(n) == fibonacci_iter(n) for n in range(16)))
