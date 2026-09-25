"""Fibonacci con memoria dell'Unità 8: risultati salvati e conteggi.

Collocare il file in `programmi/fibonacci_memoria_u8.py` della raccolta
dello studente. Il modulo contiene il problema svolto del capitolo PY-12,
parte V: la versione di Fibonacci che MEMORIZZA i risultati già calcolati in
un dizionario esplicito, e la strumentazione che misura il lavoro fatto.

Modelli distinti con cura: il RISULTATO salvato è una associazione nella
memoria, per esempio `memoria[4] = 3`; il FRAME di chiamata è lo stato della
ricorsione ancora in corso e vive nello stack dell'interprete. La
memorizzazione riduce il ricalcolo, non elimina la ricorsione: i frame
continuano a crescere con la profondità delle chiamate e non vanno
confusi con le voci della memoria.

Definizioni dei conteggi usati dalle prove:
- C: numero di INGRESSI nella funzione, compresi la chiamata iniziale e gli
  accessi riusciti dalla memoria;
- D: massimo numero SIMULTANEO dei soli frame Fibonacci, senza contare
  wrapper né funzioni di stampa;
- S: numero di NUOVE voci scritte nella memoria, escluse le basi già presenti.

L'import non chiede input e non stampa: le dimostrazioni stanno nel main
protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/fibonacci_memoria_u8.py
"""


# ---------------------------------------------------------------------------
# Problema svolto — Fibonacci con memoria esplicita
# ---------------------------------------------------------------------------


def fibonacci_mem(n: int, memoria: dict[int, int]) -> int:
    """Restituisce F(n) usando e aggiornando la `memoria` ricevuta.

    Riceve l'indice `n` e il dizionario `memoria`, che associa ogni indice
    già calcolato al proprio valore di Fibonacci. Restituisce F(n).

    PRECONDIZIONE: `n` è un intero non negativo e `memoria` contiene già le
    due basi corrette `memoria = {0: 0, 1: 1}`; ogni altra voce eventualmente
    presente deve avere il valore corretto F(k). La funzione non riconosce
    automaticamente una memoria corrotta: non valida le voci ricevute.

    EFFETTO: la funzione MODIFICA la `memoria` del chiamante e vi aggiunge
    le associazioni che calcola. Non costruisce una memoria nuova a ogni
    chiamata e non la copia da un ramo all'altro: i sottoproblemi lavorano
    sullo STESSO dizionario ed è questo che evita il ricalcolo.

    INVARIANTE: ogni associazione memorizzata resta un risultato corretto e
    le voci preesistenti non vengono invalidate. Il controllo `n in memoria`
    risponde alla domanda «questo risultato è già disponibile?»: per n = 0 il
    valore 0 è un risultato valido e non un'assenza, quindi il controllo non
    usa `get` né il confronto con `None`.
    """
    if n in memoria:
        return memoria[n]
    precedente = fibonacci_mem(n - 1, memoria)
    ancora_precedente = fibonacci_mem(n - 2, memoria)
    memoria[n] = precedente + ancora_precedente
    return memoria[n]


# ---------------------------------------------------------------------------
# Versioni di riferimento dell'Unità 6, per confrontare i risultati
# ---------------------------------------------------------------------------


def fibonacci_diretto(n: int) -> int:
    """Restituisce F(n) secondo la definizione ricorsiva diretta (Unità 6).

    Stesso dominio e stesso risultato di `fibonacci_mem`, senza memoria:
    ogni chiamata ricalcola da zero i due sottoproblemi e lo stesso F(k)
    viene calcolato più volte. Serve da riferimento per verificare che la
    memorizzazione non cambi il VALORE restituito.
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    precedente = fibonacci_diretto(n - 1)
    ancora_precedente = fibonacci_diretto(n - 2)
    return precedente + ancora_precedente


def fibonacci_iter(n: int) -> int:
    """Restituisce F(n) con la coppia di valori consecutivi già nota (Unità 6).

    Stesso dominio e stesso risultato della versione ricorsiva. La coppia
    `(precedente, corrente)` rappresenta F(i-1) e F(i) all'inizio di ogni
    iterazione con indice i. Il confronto con la ricorsione riguarda il
    RISULTATO e il diverso stato conservato: a questa versione non
    corrisponde alcun conteggio di frame ricorsivi.
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


# ---------------------------------------------------------------------------
# Strumentazione — C, D e S senza alterare il procedimento
# ---------------------------------------------------------------------------


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
    di questa funzione: wrapper e funzioni di stampa non la chiamano in
    ricorsione e quindi non alterano il conteggio. S incrementa soltanto
    quando un'associazione NUOVA viene scritta: le basi già presenti nella
    memoria non sono scritture.

    È una versione dichiaratamente osservatoria della funzione svolta e non
    ne cambia il contratto.
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


def memoria_delle_basi() -> dict[int, int]:
    """Restituisce una memoria NUOVA con le sole due basi corrette.

    Il chiamante prepara la memoria come `memoria_delle_basi()`, che produce
    `{0: 0, 1: 1}`: il risultato di F(0) e F(1) è già disponibile e non
    viene conteggiato come scrittura. Ogni prova parte da una memoria
    propria oppure da una memoria il cui stato è dichiarato: non si
    mescolano i conteggi di stati iniziali diversi.
    """
    return {0: 0, 1: 1}


if __name__ == "__main__":
    # Le uniche stampe del modulo stanno qui: ogni funzione sopra restituisce
    # e non scrive nulla.
    print("Tabella dei confronti — memoria ripartita dalle sole basi")
    print("n  F(n)  C diretta  C memoria  D  S")
    for n in (0, 1, 2, 4, 5):
        memoria = memoria_delle_basi()
        statistiche = [0, 0, 0]
        valore = fibonacci_mem_osservata(n, memoria, statistiche)
        diretto = [0, 0]
        fibonacci_diretto_osservato(n, diretto)
        print(f"{n:<2} {valore:<5} {diretto[0]:<10} {statistiche[0]:<10} {statistiche[1]}  {statistiche[2]}")

    print()
    print("Traccia degli ingressi per n = 4")
    memoria = memoria_delle_basi()
    statistiche = [0, 0, 0]
    traccia = []
    fibonacci_mem_osservata(4, memoria, statistiche, traccia=traccia)
    print("ingressi nell'ordine:", traccia)
    print("C, D, S             :", statistiche)
    print("memoria finale      :", memoria)

    print()
    print("Ripetizione di n = 4 sulla stessa memoria (cache calda)")
    statistiche = [0, 0, 0]
    traccia = []
    valore = fibonacci_mem_osservata(4, memoria, statistiche, traccia=traccia)
    print("F(4) =", valore, "ingressi:", traccia, "C, D, S:", statistiche)

    print()
    print("Aggiunta di n = 5 alla memoria che arriva fino a 4")
    statistiche = [0, 0, 0]
    traccia = []
    valore = fibonacci_mem_osservata(5, memoria, statistiche, traccia=traccia)
    print("F(5) =", valore, "ingressi:", traccia, "C, D, S:", statistiche)
    print("memoria finale      :", memoria)

    print()
    print("Confronto dei valori 0...10 fra le tre versioni")
    print("diretta :", [fibonacci_diretto(n) for n in range(11)])
    print("iterativa:", [fibonacci_iter(n) for n in range(11)])
    memorizzata = memoria_delle_basi()
    print("con memoria:", [fibonacci_mem(n, memorizzata) for n in range(11)])
    print("concordano:", all(
        fibonacci_diretto(n) == fibonacci_iter(n) == fibonacci_mem(n, memoria_delle_basi())
        for n in range(11)
    ))
