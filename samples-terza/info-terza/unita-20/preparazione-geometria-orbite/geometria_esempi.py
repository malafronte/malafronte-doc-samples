"""Costruzioni finite di Koch e Sierpiński con ricorsione ad accumulatore — Unità 20 (L2).

Il modulo implementa gli esempi preparatori del capitolo PY-37
(*Frattali geometrici e costruzioni ricorsive*) usando soltanto coppie `(x, y)`
di numeri reali, senza il tipo `complex` (che verrà introdotto in PY-38):

- Operazioni sui punti del piano cartesiano (`y` rivolto verso l'alto):
  somma di coordinate, vettore fra punti, punto medio e rotazione di 60 gradi.
- Curva di Koch sul segmento base, fiocco di neve di Koch sul triangolo
  equilatero percorso in senso orario e triangolo di Sierpiński con esclusione
  del triangolo centrale.
- Scelta del massimo livello entro un budget di elementi (problema PY-U20-T09).

Variante implementata: ogni funzione pubblica crea un accumulatore nuovo
(una lista vuota) e delega a un procedimento ricorsivo che aggiunge ciascun
elemento finale esattamente una volta con `append`. Il costo dichiarato
(`Theta(4**d)` per Koch, `Theta(3**d)` per Sierpiński, stack `O(d)`)
corrisponde a questa variante. Una versione che concatena ripetutamente le
liste dei sottoalberi (`risultato = ricorsione(...) + ricorsione(...)`)
copierebbe gli elementi già prodotti a ogni livello e introdurrebbe un fattore
aggiuntivo legato alla profondità; per questo il corso adotta l'accumulatore.

Ambiente: CPython 3.14 sul computer. Il modulo non esegue operazioni di I/O
né apre finestre grafiche all'importazione.
"""

import math

from dati_canonici import (
    COSENO_60,
    SENO_60,
    valida_intero_non_booleano,
    valida_reale_finito,
)

type Punto2D = tuple[float, float]
type Segmento2D = tuple[Punto2D, Punto2D]
type Triangolo2D = tuple[Punto2D, Punto2D, Punto2D]

STILI_TRIANGOLO_AMMESSI: tuple[str, str] = ("pieno", "contorno")


def valida_punto(valore: object, nome_parametro: str) -> Punto2D:
    """Verifica che `valore` sia una coppia `(x, y)` di reali finiti non booleani."""
    if not isinstance(valore, (tuple, list)) or len(valore) != 2:
        raise TypeError(f"Il parametro '{nome_parametro}' richiede una coppia (x, y).")
    x = valida_reale_finito(valore[0], f"{nome_parametro}[0]")
    y = valida_reale_finito(valore[1], f"{nome_parametro}[1]")
    return (x, y)


def valida_segmento(valore: object, nome_parametro: str) -> Segmento2D:
    """Verifica che `valore` sia una coppia di punti con estremi distinti."""
    if not isinstance(valore, (tuple, list)) or len(valore) != 2:
        raise TypeError(f"Il parametro '{nome_parametro}' richiede una coppia di punti (A, B).")
    a = valida_punto(valore[0], f"{nome_parametro}[0]")
    b = valida_punto(valore[1], f"{nome_parametro}[1]")
    if a == b:
        raise ValueError(f"Il segmento '{nome_parametro}' richiede due estremi distinti.")
    return (a, b)


def valida_triangolo(valore: object, nome_parametro: str) -> Triangolo2D:
    """Verifica che `valore` sia un triangolo di tre punti finiti non allineati."""
    if not isinstance(valore, (tuple, list)) or len(valore) != 3:
        raise TypeError(f"Il parametro '{nome_parametro}' richiede tre vertici (A, B, C).")
    a = valida_punto(valore[0], f"{nome_parametro}[0]")
    b = valida_punto(valore[1], f"{nome_parametro}[1]")
    c = valida_punto(valore[2], f"{nome_parametro}[2]")
    area_doppia = abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1]))
    if area_doppia == 0.0:
        raise ValueError(f"Il triangolo '{nome_parametro}' richiede vertici non allineati.")
    return (a, b, c)


def valida_livello(livello: object) -> int:
    """Verifica che `livello` sia un intero non booleano maggiore o uguale a zero."""
    return valida_intero_non_booleano(livello, "livello", minimo=0)


def somma_punti(p: Punto2D, q: Punto2D) -> Punto2D:
    """Restituisce la somma coordinata per coordinata dei punti `p` e `q`."""
    punto_p = valida_punto(p, "p")
    punto_q = valida_punto(q, "q")
    return (punto_p[0] + punto_q[0], punto_p[1] + punto_q[1])


def vettore_fra_punti(a: Punto2D, b: Punto2D) -> Punto2D:
    """Restituisce il vettore `b - a` come coppia `(dx, dy)`."""
    punto_a = valida_punto(a, "a")
    punto_b = valida_punto(b, "b")
    return (punto_b[0] - punto_a[0], punto_b[1] - punto_a[1])


def punto_medio(a: Punto2D, b: Punto2D) -> Punto2D:
    """Restituisce il punto medio del segmento di estremi `a` e `b`."""
    punto_a = valida_punto(a, "a")
    punto_b = valida_punto(b, "b")
    return ((punto_a[0] + punto_b[0]) / 2.0, (punto_a[1] + punto_b[1]) / 2.0)


def ruota_vettore_60_gradi(v: Punto2D) -> Punto2D:
    """Ruota il vettore `v` di +60 gradi in senso antiorario nel piano cartesiano.

    La formula usa `cos(60°) = 0.5` e `sin(60°) = sqrt(3)/2`:
    `(x, y)` diventa `(x * cos - y * sin, x * sin + y * cos)`.
    """
    vettore = valida_punto(v, "v")
    x, y = vettore
    return (x * COSENO_60 - y * SENO_60, x * SENO_60 + y * COSENO_60)


def vertici_sostituzione_koch(segmento: Segmento2D) -> tuple[Punto2D, ...]:
    """Restituisce i 5 punti ordinati della sostituzione di Koch del segmento dato.

    Dati `A` e `B`, con `dx = (x_B - x_A) / 3` e `dy = (y_B - y_A) / 3`, i punti
    sono `A`, `P1 = A + (dx, dy)`, `punta`, `P2 = A + 2 * (dx, dy)`, `B`, dove
    la punta si ottiene ruotando il vettore `(dx, dy)` di +60 gradi a partire
    da `P1`. Sul segmento `(0, 0) -> (3, 0)` produce i vertici canonici
    `(0, 0)`, `(1, 0)`, `(1.5, sqrt(3)/2)`, `(2, 0)`, `(3, 0)`.
    """
    (x_a, y_a), (x_b, y_b) = valida_segmento(segmento, "segmento")
    dx = (x_b - x_a) / 3.0
    dy = (y_b - y_a) / 3.0
    p_1: Punto2D = (x_a + dx, y_a + dy)
    p_2: Punto2D = (x_a + 2.0 * dx, y_a + 2.0 * dy)
    ruotato = ruota_vettore_60_gradi((dx, dy))
    punta: Punto2D = (p_1[0] + ruotato[0], p_1[1] + ruotato[1])
    return ((x_a, y_a), p_1, punta, p_2, (x_b, y_b))


def suddividi_segmento_koch(segmento: Segmento2D) -> tuple[Segmento2D, ...]:
    """Sostituisce il segmento dato con i 4 segmenti ordinati della regola di Koch."""
    a, p_1, punta, p_2, b = vertici_sostituzione_koch(segmento)
    return ((a, p_1), (p_1, punta), (punta, p_2), (p_2, b))


def _curva_koch_ricorsiva(
    segmento: Segmento2D, livello: int, accumulatore: list[Segmento2D]
) -> None:
    """Procedimento ricorsivo che aggiunge i segmenti finali in `accumulatore`.

    Caso base (`livello == 0`): aggiunge il segmento ricevuto senza dividerlo.
    Passo ricorsivo (`livello >= 1`): suddivide il segmento nei 4 segmenti
    della regola di Koch e ricorre su ciascuno con `livello - 1`, nell'ordine
    da `A` verso `B`. L'accumulatore è creato dalla funzione pubblica e qui
    viene solo esteso con `append`: nessun elemento viene copiato due volte.
    """
    if livello == 0:
        accumulatore.append(segmento)
        return
    for sotto_segmento in suddividi_segmento_koch(segmento):
        _curva_koch_ricorsiva(sotto_segmento, livello - 1, accumulatore)


def curva_koch(segmento_base: Segmento2D, livello: int) -> list[Segmento2D]:
    """Restituisce la lista ordinata dei `4**livello` segmenti della curva di Koch.

    Al livello `0` restituisce la lista con il solo segmento iniziale
    `[segmento_base]`; al livello `d >= 1` applica la sostituzione di Koch
    e ricorre sui 4 segmenti con livello `d - 1`.
    """
    base = valida_segmento(segmento_base, "segmento_base")
    d = valida_livello(livello)
    accumulatore: list[Segmento2D] = []
    _curva_koch_ricorsiva(base, d, accumulatore)
    return accumulatore


def fiocco_koch(triangolo_base: Triangolo2D, livello: int) -> list[Segmento2D]:
    """Restituisce i `3 * 4**livello` segmenti ordinati del fiocco di neve di Koch.

    Il fiocco applica la curva di Koch ai tre lati del triangolo iniziale,
    nell'ordine `V0 -> V1`, `V1 -> V2`, `V2 -> V0`. Poiché la rotazione di
    +60 gradi sposta la punta a sinistra del segmento orientato, il triangolo
    va percorso in senso orario affinché le punte siano rivolte verso
    l'esterno. La spezzata prodotta è chiusa: l'ultimo punto coincide con il
    primo e ogni segmento inizia dove finisce il precedente.
    """
    v_0, v_1, v_2 = valida_triangolo(triangolo_base, "triangolo_base")
    d = valida_livello(livello)
    accumulatore: list[Segmento2D] = []
    for lato in ((v_0, v_1), (v_1, v_2), (v_2, v_0)):
        _curva_koch_ricorsiva(lato, d, accumulatore)
    return accumulatore


def _sierpinski_ricorsivo(
    triangolo: Triangolo2D, livello: int, accumulatore: list[Triangolo2D]
) -> None:
    """Procedimento ricorsivo che aggiunge i triangoli finali in `accumulatore`.

    Caso base (`livello == 0`): aggiunge il triangolo ricevuto.
    Passo ricorsivo (`livello >= 1`): calcola i tre punti medi `M_AB`, `M_BC`
    e `M_CA` e ricorre sui tre triangoli agli angoli
    `(A, M_AB, M_CA)`, `(M_AB, B, M_BC)`, `(M_CA, M_BC, C)` con `livello - 1`,
    escludendo il triangolo centrale `(M_AB, M_BC, M_CA)`.
    """
    (a, b, c) = triangolo
    if livello == 0:
        accumulatore.append(triangolo)
        return
    m_ab = punto_medio(a, b)
    m_bc = punto_medio(b, c)
    m_ca = punto_medio(c, a)
    _sierpinski_ricorsivo((a, m_ab, m_ca), livello - 1, accumulatore)
    _sierpinski_ricorsivo((m_ab, b, m_bc), livello - 1, accumulatore)
    _sierpinski_ricorsivo((m_ca, m_bc, c), livello - 1, accumulatore)


def triangoli_sierpinski(
    triangolo_base: Triangolo2D, livello: int, stile: str = "pieno"
) -> list[Triangolo2D]:
    """Restituisce la lista dei `3**livello` triangoli finali di Sierpiński.

    Al livello `0` restituisce `[triangolo_base]`; al livello `d >= 1` ricorre
    sui tre triangoli agli angoli con livello `d - 1`, escludendo il triangolo
    centrale individuato dai tre punti medi. Il parametro `stile` vale
    `"pieno"` oppure `"contorno"`: la geometria prodotta è la stessa, mentre
    la scelta dichiara se la figura verrà disegnata con triangoli riempiti o
    con soli contorni (testo, figure e prove usano sempre la stessa scelta).
    """
    base = valida_triangolo(triangolo_base, "triangolo_base")
    d = valida_livello(livello)
    if stile not in STILI_TRIANGOLO_AMMESSI:
        raise ValueError(f"Stile '{stile}' non valido; ammessi: {STILI_TRIANGOLO_AMMESSI}.")
    accumulatore: list[Triangolo2D] = []
    _sierpinski_ricorsivo(base, d, accumulatore)
    return accumulatore


def lunghezza_segmento_finale_koch(lato_iniziale: float, livello: int) -> float:
    """Restituisce la lunghezza `L / 3**d` di ciascun segmento finale di Koch."""
    lato = valida_reale_finito(lato_iniziale, "lato_iniziale")
    if lato <= 0.0:
        raise ValueError("Il parametro 'lato_iniziale' richiede un valore positivo.")
    d = valida_livello(livello)
    return lato / (3.0**d)


def lunghezza_totale_curva_koch(lato_iniziale: float, livello: int) -> float:
    """Restituisce la lunghezza totale `L * (4/3)**d` della curva di Koch."""
    lato = valida_reale_finito(lato_iniziale, "lato_iniziale")
    if lato <= 0.0:
        raise ValueError("Il parametro 'lato_iniziale' richiede un valore positivo.")
    d = valida_livello(livello)
    return lato * ((4.0 / 3.0) ** d)


def livello_massimo_koch_curva(budget_elementi: int) -> int:
    """Restituisce il massimo livello `d` della curva con `4**d <= budget`.

    Il budget pari al conteggio esatto è accettato (`4**d == budget`); un
    budget inferiore a `1` (conteggio del livello `0`) solleva `ValueError`.
    """
    budget = valida_intero_non_booleano(budget_elementi, "budget_elementi", minimo=1)
    livello = 0
    while 4 ** (livello + 1) <= budget:
        livello += 1
    return livello


def livello_massimo_koch_fiocco(budget_elementi: int) -> int:
    """Restituisce il massimo livello `d` del fiocco con `3 * 4**d <= budget`."""
    budget = valida_intero_non_booleano(budget_elementi, "budget_elementi", minimo=1)
    if budget < 3:
        raise ValueError("Il budget per il fiocco di Koch richiede almeno 3 segmenti (livello 0).")
    livello = 0
    while 3 * (4 ** (livello + 1)) <= budget:
        livello += 1
    return livello


def livello_massimo_sierpinski(budget_elementi: int) -> int:
    """Restituisce il massimo livello `d` di Sierpiński con `3**d <= budget`."""
    budget = valida_intero_non_booleano(budget_elementi, "budget_elementi", minimo=1)
    livello = 0
    while 3 ** (livello + 1) <= budget:
        livello += 1
    return livello


def area_triangolo_equilatero(lato: float) -> float:
    """Restituisce l'area `sqrt(3)/4 * lato**2` del triangolo equilatero di lato dato."""
    valore = valida_reale_finito(lato, "lato")
    if valore <= 0.0:
        raise ValueError("Il parametro 'lato' richiede un valore positivo.")
    return (math.sqrt(3.0) / 4.0) * (valore**2)


if __name__ == "__main__":
    base_demo: Segmento2D = ((0.0, 0.0), (3.0, 0.0))
    print("Curva di Koch, livello 1:", len(curva_koch(base_demo, 1)), "segmenti")
    print("Fiocco di Koch, livello 1:", len(fiocco_koch(((0.0, 0.0), (1.5, 2.598), (3.0, 0.0)), 1)))
    print(
        "Sierpinski, livello 1:",
        len(triangoli_sierpinski(((0.0, 0.0), (4.0, 0.0), (2.0, 3.464)), 1)),
    )
