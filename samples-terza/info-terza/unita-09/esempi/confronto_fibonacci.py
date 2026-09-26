"""Fibonacci, fattoriale e Hanoi dell'Unità 9: lavoro, profondità e memoria.

Collocare il file in `programmi/confronto_fibonacci.py` della raccolta
dello studente. Il modulo contiene le tre varianti canoniche di Fibonacci
del capitolo PY-13, parte III, la strumentazione che ne misura il lavoro e
i due problemi di riferimento, fattoriale e Hanoi, con gli stessi conteggi.

Derivazione dei sorgenti: `fibonacci_mem`, `fibonacci_diretto`,
`fibonacci_iter`, `fibonacci_mem_osservata`, `fibonacci_diretto_osservato`
e `memoria_delle_basi` derivano da `unita-08/esempi/fibonacci_memoria_u8.py`
e dalle versioni canoniche dell'Unità 6; le operazioni rilevanti sono
identiche. `hanoi` deriva da `unita-06/esempi/hanoi_u6.py`, con base
n = 0 e mosse accodate alla lista ricevuta.

Definizioni dei conteggi usati dalle prove:
- C: numero di INGRESSI nella funzione, compresi la chiamata iniziale, le
  basi e gli accessi riusciti dalla memoria;
- D: massimo numero SIMULTANEO dei soli frame della funzione studiata, con
  il primo frame a profondità 1: D include il primo frame;
- S: numero di NUOVE voci scritte nella memoria, escluse le basi già presenti;
- M: moltiplicazioni eseguite (fattoriale) oppure mosse accodate (Hanoi).

Nella variante con memoria ogni addizione corrisponde a una nuova voce
scritta: le addizioni valgono S. Nella versione iterativa canonica dell'U6
le addizioni sono max(0, n-1): la variante U8 con `range(n)` e assegnamento
multiplo ne esegue n e non trasferisce i suoi conteggi in questa tabella.

Il modello conta addizioni e operazioni di dizionario a costo unitario sotto
le ipotesi dichiarate: non misura byte né istruzioni reali, e i valori
crescenti di Fibonacci richiedono comunque sempre più bit.

Nessun benchmark viene eseguito all'import: le stampe stanno nel main
protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/confronto_fibonacci.py
"""


# ---------------------------------------------------------------------------
# Problema svolto III — le tre varianti canoniche
# ---------------------------------------------------------------------------


def fibonacci_mem(n: int, memoria: dict[int, int]) -> int:
    """Restituisce F(n) usando e aggiornando la `memoria` ricevuta.

    Fissate le basi F(0) = 0 e F(1) = 1. Riceve l'indice `n` e il dizionario
    `memoria`, che associa ogni indice già calcolato al proprio valore.

    PRECONDIZIONE: `n` è un intero non negativo e `memoria` contiene già le
    due basi corrette `memoria = {0: 0, 1: 1}`; ogni altra voce presente deve
    avere il valore corretto F(k). La funzione non valida le voci ricevute.

    EFFETTO: la funzione MODIFICA la `memoria` del chiamante e vi aggiunge
    le associazioni che calcola, sullo STESSO dizionario di ogni
    sottoproblema: è questo che evita il ricalcolo. Il controllo `n in
    memoria` risponde alla domanda «questo risultato è già disponibile?» e
    non usa `get` né il confronto con `None`, perché F(0) = 0 è un
    risultato valido e non un'assenza. La chiamata a `n - 1` precede quella
    a `n - 2`.

    Nel modello didattico, a memoria nuova: C = 2n - 1 per n >= 2, con
    C = 1 sulle basi; S = max(0, n - 1) nuove scritture; D = max(1, n)
    frame simultanei; le voci finali sono 2 per n = 0 e n = 1, n + 1 per
    n >= 2.
    """
    if n in memoria:
        return memoria[n]
    precedente = fibonacci_mem(n - 1, memoria)
    ancora_precedente = fibonacci_mem(n - 2, memoria)
    memoria[n] = precedente + ancora_precedente
    return memoria[n]


def fibonacci_diretto(n: int) -> int:
    """Restituisce F(n) secondo la definizione ricorsiva diretta.

    Stesso dominio e stesso risultato di `fibonacci_mem`, senza memoria:
    ogni chiamata ricalcola da zero i due sottoproblemi e lo stesso F(k)
    viene calcolato più volte. Contando ogni INGRESSO, basi e radice
    comprese: C(0) = C(1) = 1 e C(n) = 1 + C(n - 1) + C(n - 2) per n >= 2,
    con crescita esponenziale. Le addizioni valgono (C - 1) / 2. La
    profondità include il primo frame: D(0) = D(1) = 1 e D(n) = n per
    n >= 2. Lo stack cresce con n, non con il numero totale di chiamate.
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    precedente = fibonacci_diretto(n - 1)
    ancora_precedente = fibonacci_diretto(n - 2)
    return precedente + ancora_precedente


def fibonacci_iter(n: int) -> int:
    """Restituisce F(n) con la coppia di valori consecutivi già nota.

    Stesso dominio e stesso risultato della versione ricorsiva. È la
    variante canonica del capitolo PY-10: ritorno immediato per n <= 1 e
    ciclo `range(2, n + 1)`. La coppia `(precedente, corrente)` rappresenta
    F(i-1) e F(i) all'inizio di ogni iterazione con indice i. Le addizioni
    sono max(0, n - 1). La versione conserva un numero costante di valori:
    i bit degli interi Python crescono comunque con n.
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


def memoria_delle_basi() -> dict[int, int]:
    """Restituisce una memoria NUOVA con le sole due basi corrette.

    Il chiamante prepara la memoria come `memoria_delle_basi()`, che produce
    `{0: 0, 1: 1}`: i valori di F(0) e F(1) sono già disponibili e non
    diventano scritture. Ogni prova parte da una memoria propria oppure da
    una memoria il cui stato è dichiarato: non si mescolano i conteggi di
    stati iniziali diversi.
    """
    return {0: 0, 1: 1}


# ---------------------------------------------------------------------------
# Strumentazione — C, D, S e addizioni senza alterare il procedimento
# ---------------------------------------------------------------------------


def fibonacci_diretto_osservato(n: int, statistiche: list[int], profondita: int = 1) -> int:
    """Restituisce F(n) come `fibonacci_diretto`, contando ingressi e profondità.

    Stesso ricevuto e stesso risultato di `fibonacci_diretto`. La lista
    `statistiche` è `[ingressi, profondita_massima]` e va azzerata prima di
    ogni prova; il primo frame ha profondità 1. Serve a ricavare la colonna
    «C diretta» del confronto con la versione a memoria: gli ingressi qui
    sono molti di più perché nessun risultato viene salvato.
    """
    statistiche[0] += 1
    statistiche[1] = max(statistiche[1], profondita)
    if n == 0:
        return 0
    if n == 1:
        return 1
    precedente = fibonacci_diretto_osservato(n - 1, statistiche, profondita + 1)
    ancora_precedente = fibonacci_diretto_osservato(n - 2, statistiche, profondita + 1)
    return precedente + ancora_precedente


def fibonacci_iter_osservata(n: int, statistiche: list[int]) -> int:
    """Restituisce F(n) come `fibonacci_iter`, contando le addizioni eseguite.

    CONTRATTO DIVERSO: oltre al risultato aggiorna la lista `statistiche`,
    che è `[addizioni]` e va azzerata prima di ogni prova. Una addizione
    corrisponde a ogni `precedente + corrente` realmente eseguito: per
    n <= 1 il totale è 0, per n >= 2 vale n - 1. A questa versione iterativa
    non corrisponde alcun conteggio di frame ricorsivi.
    """
    if n <= 1:
        return n
    precedente = 0
    corrente = 1
    for indice in range(2, n + 1):
        statistiche[0] += 1
        successivo = precedente + corrente
        precedente = corrente
        corrente = successivo
    return corrente


def fibonacci_mem_osservata(
    n: int,
    memoria: dict[int, int],
    statistiche: list[int],
    profondita: int = 1,
    traccia: list[int] | None = None,
) -> int:
    """Restituisce F(n) come `fibonacci_mem`, aggiornando i conteggi ricevuti.

    Stesso ricevuto, stesso risultato e stessi effetti di `fibonacci_mem`,
    con l'aggiunta di tre strumenti di osservazione che il chiamante
    fornisce e la funzione aggiorna:
    - `statistiche` è la lista `[ingressi, profondita_massima,
      nuove_scritture]`, cioè C, D e S, da azzerare prima di ogni prova;
    - `profondita` è la posizione del frame corrente: il primo frame ha
      profondità 1 e ogni figlio riceve `profondita + 1`;
    - `traccia`, se fornita, è una lista nella quale viene annotato l'indice
      di ogni ingresso, nell'ordine in cui avviene.

    Ogni ingresso incrementa C, compresi la chiamata iniziale e gli accessi
    riusciti dalla memoria. D misura la massima profondità dei soli frame
    di questa funzione. S incrementa soltanto quando un'associazione NUOVA
    viene scritta: le basi già presenti nella memoria non sono scritture e
    nemmeno addizioni, perché il valore si legge e basta.

    È una versione dichiaratamente osservatoria della funzione svolta e non
    ne cambia il contratto algoritmico.
    """
    statistiche[0] += 1
    statistiche[1] = max(statistiche[1], profondita)
    if traccia is not None:
        traccia.append(n)
    if n in memoria:
        return memoria[n]
    precedente = fibonacci_mem_osservata(n - 1, memoria, statistiche, profondita + 1, traccia)
    ancora_precedente = fibonacci_mem_osservata(n - 2, memoria, statistiche, profondita + 1, traccia)
    memoria[n] = precedente + ancora_precedente
    statistiche[2] += 1
    return memoria[n]


# ---------------------------------------------------------------------------
# Fattoriale — ricorsione lineare con moltiplicazioni e frame
# ---------------------------------------------------------------------------


def fattoriale(n: int) -> int:
    """Restituisce il fattoriale di n, con base n = 0.

    Dominio: n intero non negativo (0! = 1 per definizione). Base: n == 0.
    Riduzione: n - 1. Ricomposizione: n * parziale. Con la base n = 0 la
    ricorsione esegue n moltiplicazioni, n + 1 ingressi e raggiunge n + 1
    frame simultanei: per n = 3, 3 moltiplicazioni, 4 ingressi e 4 frame.
    Nessun input, nessuna stampa, nessun effetto: funzione pura.
    """
    if n == 0:
        return 1
    parziale = fattoriale(n - 1)
    return n * parziale


def fattoriale_osservato(n: int, statistiche: list[int], profondita: int = 1) -> int:
    """Restituisce n! come `fattoriale`, aggiornando i conteggi ricevuti.

    CONTRATTO DIVERSO: la lista `statistiche` è `[ingressi, moltiplicazioni,
    profondita_massima]` e va azzerata prima di ogni prova; il primo frame
    ha profondità 1. Con la base n = 0 si hanno n + 1 ingressi, n
    moltiplicazioni e n + 1 frame massimi; per n = 0 la lista diventa
    `[1, 0, 1]`.
    """
    statistiche[0] += 1
    statistiche[2] = max(statistiche[2], profondita)
    if n == 0:
        return 1
    parziale = fattoriale_osservato(n - 1, statistiche, profondita + 1)
    statistiche[1] += 1
    return n * parziale


# ---------------------------------------------------------------------------
# Hanoi — mosse in output, ingressi e frame
# ---------------------------------------------------------------------------


def hanoi(
    n: int,
    origine: str,
    destinazione: str,
    appoggio: str,
    mosse: list[tuple[int, str, str]],
) -> None:
    """Accoda alla lista ricevuta le mosse del trasferimento di n dischi.

    Dominio: n intero non negativo; etichette dei tre pioli distinte;
    stato logico iniziale con n dischi ordinati sull'origine. Base: n == 0.
    Effetto: aggiunge 2**n - 1 tuple (disco, origine, destinazione) in coda,
    conservando l'eventuale prefisso già presente. Restituisce None.

    I conteggi del problema, con la base n = 0, sono M = 2**n - 1 mosse,
    C = 2**(n + 1) - 1 ingressi e D = n + 1 frame simultanei: per n = 3,
    7 mosse, 15 ingressi e 4 frame. La lista delle mosse è OUTPUT: i suoi
    elementi sono Θ(2**n) e rendono esponenziale la memoria totale del
    programma, anche se lo stack dei frame resta Θ(n).
    """
    if n == 0:
        return
    hanoi(n - 1, origine, appoggio, destinazione, mosse)
    mosse.append((n, origine, destinazione))
    hanoi(n - 1, appoggio, destinazione, origine, mosse)


def hanoi_osservato(
    n: int,
    origine: str,
    destinazione: str,
    appoggio: str,
    mosse: list[tuple[int, str, str]],
    statistiche: list[int],
    profondita: int = 1,
) -> None:
    """Come `hanoi`, contando ingressi e profondità massima dei frame.

    CONTRATTO DIVERSO: la lista `statistiche` è `[ingressi,
    profondita_massima]` e va azzerata prima di ogni prova; il primo frame
    ha profondità 1 e ogni chiamata ricorsiva riceve `profondita + 1`. Le
    mosse accodate restano l'output del problema e si contano con
    `len(mosse)`, senza entrare nelle statistiche dello stack.
    """
    statistiche[0] += 1
    statistiche[1] = max(statistiche[1], profondita)
    if n == 0:
        return
    hanoi_osservato(n - 1, origine, appoggio, destinazione, mosse, statistiche, profondita + 1)
    mosse.append((n, origine, destinazione))
    hanoi_osservato(n - 1, appoggio, destinazione, origine, mosse, statistiche, profondita + 1)


if __name__ == "__main__":
    # Nessun benchmark all'import: questa è l'unica sede con stampe.
    print("Tabella del capitolo — ogni calcolo con memoria NUOVA dalle basi")
    print("n  F(n)  C dirett  D dirett  addiz. iter  C memb  S memb  D memb")
    for n in (0, 1, 2, 4, 5, 10):
        valore = fibonacci_iter(n)

        diretto = [0, 0]
        fibonacci_diretto_osservato(n, diretto)

        addizioni = [0]
        fibonacci_iter_osservata(n, addizioni)

        memoria = memoria_delle_basi()
        mem = [0, 0, 0]
        fibonacci_mem_osservata(n, memoria, mem)

        # mem è [C, D, S]; le colonne seguono l'ordine del capitolo: C, S, D.
        print(
            f"{n:<2} {valore:<5} {diretto[0]:<8} {diretto[1]:<8} "
            f"{addizioni[0]:<11} {mem[0]:<6} {mem[2]:<6} {mem[1]}"
        )

    print()
    print("Memoria già popolata — richiesta ripetuta, distinta dalla memoria nuova")
    memoria = memoria_delle_basi()
    fibonacci_mem(4, memoria)
    print("voci presenti prima della richiesta:", sorted(memoria))
    mem = [0, 0, 0]
    traccia = []
    valore = fibonacci_mem_osservata(4, memoria, mem, traccia=traccia)
    print(f"F(4) = {valore}, ingressi {traccia}, C D S = {mem}  (nessuna addizione)")

    mem = [0, 0, 0]
    traccia = []
    valore = fibonacci_mem_osservata(5, memoria, mem, traccia=traccia)
    print(f"F(5) = {valore}, ingressi {traccia}, C D S = {mem}  (una sola scrittura)")
    print("voci presenti dopo la richiesta:", sorted(memoria))

    print()
    print("Fattoriale — moltiplicazioni, ingressi e frame con base n = 0")
    print("n  n!    moltiplicazioni  ingressi  frame")
    for n in (0, 1, 3, 5):
        statistiche = [0, 0, 0]
        valore = fattoriale_osservato(n, statistiche)
        print(f"{n:<2} {valore:<5} {statistiche[1]:<16} {statistiche[0]:<8} {statistiche[2]}")

    print()
    print("Hanoi — mosse, ingressi e frame con base n = 0")
    print("n  mosse  ingressi  frame")
    for n in (0, 1, 3, 4):
        mosse = []
        statistiche = [0, 0]
        hanoi_osservato(n, "A", "C", "B", mosse, statistiche)
        print(f"{n:<2} {len(mosse):<6} {statistiche[0]:<8} {statistiche[1]}")
