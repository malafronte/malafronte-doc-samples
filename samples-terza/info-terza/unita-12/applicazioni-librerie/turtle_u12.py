"""Disegni con turtle: poligoni regolari, penna, rotazione e chiusura.

Applicazione della libreria `turtle` dell'Unità 12: la geometria del disegno
è separata dalla finestra. Le funzioni ricevono un oggetto "penna" con i
metodi `forward`, `left`, `penup`, `pendown` e `color`: la tartaruga reale di
`turtle` li possiede, e anche un oggetto di prova può fornirli. Questo rende
la geometria verificabile senza aprire una finestra.

Contratti:

- `angoli_poligono(lati)` → grado di rotazione esterno di un poligono regolare
  di `lati` lati; `lati` deve essere un intero maggiore o uguale a 3.
- `disegna_poligono(penna, lati, lato, colore=None)` → disegna un poligono
  regolare e restituisce `None`; `lato` deve essere positivo; la penna parte
  e finisce con il tratto abbassato.
- `disegna_due_figure(penna, lati, lato)` → poligono a sinistra, spostamento
  senza tratto, poligono a destra; dimostra `penup`/`pendown`.

Errori: `TypeError` per argomenti di tipo sbagliato, `ValueError` per i dati
fuori dominio (meno di tre lati, lato non positivo). La finestra si chiude
con un clic grazie a `turtle.exitonclick()`: la chiusura fa parte dell'esempio
e non va rimossa senza un metodo equivalente.

Ambiente: CPython sul computer con Tcl/Tk disponibile, come verificato dalla
guida `uv run python -m tkinter`. La libreria `turtle` è parte della libreria
standard: nessuna installazione.
"""

import turtle


def angoli_poligono(lati):
    """Restituisce il grado di rotazione esterno di un poligono regolare.

    Un poligono di `lati` lati chiude il percorso dopo `lati` rotazioni
    esterne: la somma degli angoli esterni di qualunque poligono convesso è
    360 gradi, quindi ciascuno misura `360 / lati`.
    """
    if isinstance(lati, bool) or not isinstance(lati, int):
        raise TypeError(f"lati: atteso un intero, ricevuto {type(lati).__name__}")
    if lati < 3:
        raise ValueError(f"lati: un poligono ha almeno 3 lati, ricevuto {lati}")
    return 360 / lati


def disegna_poligono(penna, lati, lato, colore=None):
    """Disegna un poligono regolare con la penna ricevuta e restituisce `None`.

    La penna parte con il tratto abbassato e lo riabbassa se era sollevata:
    il chiamante non deve conoscere lo stato intermedio. `colore`, se
    presente, viene impostato prima del tratto.
    """
    if isinstance(lato, bool) or not isinstance(lato, (int, float)):
        raise TypeError(f"lato: atteso un numero, ricevuto {type(lato).__name__}")
    if lato <= 0:
        raise ValueError(f"lato: deve essere positivo, ricevuto {lato}")
    rotazione = angoli_poligono(lati)
    if colore is not None:
        penna.color(colore)
    penna.pendown()
    for _ in range(lati):
        penna.forward(lato)
        penna.left(rotazione)
    return None


def disegna_due_figure(penna, lati, lato):
    """Disegna due poligoni affiancati sollevando la penna fra l'uno e l'altro.

    Dimostra `penup`/`pendown`: lo spostamento non lascia traccia. I due
    poligoni hanno lo stesso numero di lati e la stessa lunghezza di lato.
    """
    disegna_poligono(penna, lati, lato, colore="steel blue")
    penna.penup()
    penna.forward(lato * 2.2)
    penna.pendown()
    disegna_poligono(penna, lati, lato, colore="dark orange")
    return None


if __name__ == "__main__":
    # Dimostrazione sotto guardia: la finestra si apre solo all'esecuzione
    # diretta del file e si chiude con un clic sulla finestra.
    schermo = turtle.Screen()
    schermo.title("LAB-PY-U12 - poligoni con turtle")
    tartaruga = turtle.Turtle()
    tartaruga.speed(3)

    # Variante 1: il numero dei lati cambia, la procedura no.
    disegna_poligono(tartaruga, lati=6, lato=80, colore="steel blue")

    tartaruga.penup()
    tartaruga.goto(0, -180)
    tartaruga.setheading(0)
    tartaruga.pendown()

    # Variante 2: due figure separate nello stesso spazio di disegno.
    disegna_due_figure(tartaruga, lati=3, lato=60)

    tartaruga.penup()
    tartaruga.hideturtle()
    schermo.exitonclick()
