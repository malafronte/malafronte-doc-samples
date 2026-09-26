"""Starter del LAB-PY-U9 - Conteggi, misure e interpretazione: le analisi.

Questo file è **incompleto, e lo dichiara**: contiene firme, docstring e
costanti, mentre i corpi di `riepilogo_una_scansione` e `conta_coppie` sono
da completare e lo dichiarano con un `NotImplementedError` che nomina la fase
del laboratorio. Il primo esito atteso della suite è una serie di fallimenti
chiari sui corpi mancanti, mai un difetto della copia.

Ambiente: CPython sul computer, raccolta `raccolta-programmi`, esecuzione con
`uv run python programmi/analisi_u9.py` dalla root della raccolta.

Architettura della strumentazione di Fibonacci: il blocco «Fibonacci» è una
COPIA dichiarata dal sorgente `fibonacci_memoria_u8.py` del capitolo PY-12
(nel repository degli esempi: `unita-08/esempi/fibonacci_memoria_u8.py`),
con le operazioni rilevanti identiche. Le tre varianti e i contatori C, D e S
servono al confronto del laboratorio e non sono oggetto di nuova
programmazione. La copia - e non l'import dal modulo degli esempi - mantiene
questa cartella autonoma: la suite deve raccogliere i test senza errori di
import e senza modifiche manuali di `sys.path`. Se il sorgente di origine
cambia, la copia si aggiorna insieme a lui: questa è l'unica architettura
adottata e non esistono strumentazioni indipendenti da far divergere.

Le funzioni di analisi non leggono da tastiera e non stampano: il messaggio
di avvio sta nella guardia in fondo al file.
"""


# ---------------------------------------------------------------------------
# Problema svolto I - riepiloghi equivalenti (contratto del cap. PY-13)
# ---------------------------------------------------------------------------


def riepilogo_due_scansioni(valori: list[int]) -> tuple[int, int]:
    """Restituisce `(totale, positivi)` attraversando `valori` due volte.

    Contratto comune dei due riepiloghi: `valori` è una lista di interi; il
    risultato è la tupla `(totale, positivi)`, dove `totale` è la somma
    algebrica dei valori e `positivi` è il numero dei valori strettamente
    maggiori di zero. L'argomento resta invariato; nessuna lettura da
    tastiera, nessuna stampa. Per la lista vuota il risultato è `(0, 0)`.

    Modello di costo: l'operazione contata è la visita al corpo del ciclo che
    attraversa la lista e questa versione ne esegue 2n, con n addizioni al
    totale e n confronti `valore > 0`: il doppio delle visite non significa
    il doppio di ogni istruzione né il doppio del tempo.

    Questa implementazione è fornita completa come RIFERIMENTO per il
    confronto con `riepilogo_una_scansione`.
    """
    totale = 0
    for valore in valori:
        totale += valore
    positivi = 0
    for valore in valori:
        if valore > 0:
            positivi += 1
    return totale, positivi


def riepilogo_una_scansione(valori: list[int]) -> tuple[int, int]:
    """Restituisce `(totale, positivi)` con un solo attraversamento.

    Stesso contratto, stesso risultato e stesso argomento invariato di
    `riepilogo_due_scansioni`: cambia l'organizzazione del lavoro, non la
    promessa. Ogni elemento deve essere visitato una sola volta, quindi il
    modello conta n visite, n addizioni al totale e n confronti
    `valore > 0`.

    Da completare nella fase L1 - Prevedere e verificare: un solo ciclo su
    `valori` aggiorna insieme `totale` e `positivi`.
    """
    # Fase L1 - Prevedere e verificare: sostituire questa riga con il corpo
    # del riepilogo a un solo attraversamento.
    raise NotImplementedError(
        "riepilogo_una_scansione: corpo da completare nella fase L1"
    )


def conta_coppie(n: int) -> int:
    """Restituisce quante volte viene eseguito il corpo dei due cicli annidati.

    Il procedimento considera le coppie `(i, j)` con `i < j`: `i` percorre
    `range(n)` e `j` percorre `range(i + 1, n)`. Il risultato è il numero di
    esecuzioni del corpo del ciclo interno, che per n = 0, 1, 2, 4, 5 vale
    0, 0, 1, 6, 10 e coincide con n(n-1)/2. La formula chiusa è il risultato
    atteso da confrontare e non sostituisce il procedimento: il conteggio
    nasce dall'esecuzione dei cicli. Dominio: `n` intero non negativo. Il
    contatore è una variabile locale, nuova a ogni chiamata: nessuno stato
    sopravvive fra chiamate successive.

    Da completare nella fase L2 - Contare e spiegare.
    """
    # Fase L2 - Contare e spiegare: sostituire questa riga con i due cicli
    # annidati del modello e il contatore locale delle esecuzioni del corpo.
    raise NotImplementedError("conta_coppie: corpo da completare nella fase L2")


# ---------------------------------------------------------------------------
# Fibonacci - copia dichiarata dal cap. PY-12, per i casi L05-L07
# ---------------------------------------------------------------------------


def fibonacci_mem(n: int, memoria: dict[int, int]) -> int:
    """Restituisce F(n) usando e aggiornando la `memoria` ricevuta.

    Fissate le basi F(0) = 0 e F(1) = 1. Riceve l'indice `n` e il dizionario
    `memoria`, che associa ogni indice già calcolato al proprio valore.

    PRECONDIZIONE: `n` è un intero non negativo e `memoria` contiene già le
    due basi corrette `memoria = {0: 0, 1: 1}`; ogni altra voce presente deve
    avere il valore corretto F(k). La funzione non valida le voci ricevute.

    EFFETTO: la funzione MODIFICA la `memoria` del chiamante e vi aggiunge le
    associazioni che calcola, sullo STESSO dizionario di ogni sottoproblema:
    è questo che evita il ricalcolo. Il controllo `n in memoria` risponde
    alla domanda «questo risultato è già disponibile?»: per n = 0 il valore 0
    è un risultato valido e non un'assenza, quindi il controllo non usa `get`
    né il confronto con `None`. La chiamata a `n - 1` precede quella a
    `n - 2`.
    """
    if n in memoria:
        return memoria[n]
    precedente = fibonacci_mem(n - 1, memoria)
    ancora_precedente = fibonacci_mem(n - 2, memoria)
    memoria[n] = precedente + ancora_precedente
    return memoria[n]


def fibonacci_diretto(n: int) -> int:
    """Restituisce F(n) secondo la definizione ricorsiva diretta (cap. PY-10).

    Stesso dominio e stesso risultato di `fibonacci_mem`, senza memoria:
    ogni chiamata ricalcola da zero i due sottoproblemi e lo stesso F(k)
    viene calcolato più volte. Contando ogni ingresso, basi e radice
    comprese: C(0) = C(1) = 1 e C(n) = 1 + C(n - 1) + C(n - 2) per n >= 2.
    La profondità include il primo frame: D(0) = D(1) = 1 e D(n) = n per
    n >= 2. Serve da riferimento per verificare che la memorizzazione non
    cambi il VALORE restituito.
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    precedente = fibonacci_diretto(n - 1)
    ancora_precedente = fibonacci_diretto(n - 2)
    return precedente + ancora_precedente


def fibonacci_iter(n: int) -> int:
    """Restituisce F(n) con la coppia di valori consecutivi già nota (cap. PY-10).

    Stesso dominio e stesso risultato della versione ricorsiva. È la variante
    canonica: ritorno immediato per n <= 1 e ciclo `range(2, n + 1)`. La
    coppia `(precedente, corrente)` rappresenta F(i-1) e F(i) all'inizio di
    ogni iterazione con indice i; le addizioni sono max(0, n - 1). La
    versione conserva un numero costante di valori: i bit degli interi
    Python crescono comunque con n. A questa versione non corrisponde alcun
    conteggio di frame ricorsivi.
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


def fibonacci_mem_osservata(
    n: int,
    memoria: dict[int, int],
    statistiche: list[int],
    profondita: int = 1,
    traccia: list[int] | None = None,
) -> int:
    """Restituisce F(n) come `fibonacci_mem`, aggiornando i conteggi ricevuti.

    Stesso ricevuto, stesso risultato e stessi effetti di `fibonacci_mem`,
    con l'aggiunta di strumenti di osservazione che il chiamante fornisce e
    la funzione aggiorna:
    - `statistiche` è la lista `[ingressi, profondita_massima,
      nuove_scritture]`, cioè C, D e S, da azzerare prima di ogni prova;
    - `profondita` è la posizione del frame corrente: il primo frame ha
      profondità 1 e ogni figlio riceve `profondita + 1`;
    - `traccia`, se fornita, è una lista nella quale viene annotato l'indice
      di ogni ingresso, nell'ordine in cui avviene.

    Ogni ingresso incrementa C, compresi la chiamata iniziale e gli accessi
    riusciti dalla memoria. D misura la massima profondità dei soli frame di
    questa funzione: wrapper e funzioni di stampa non la chiamano in
    ricorsione e quindi non alterano il conteggio. S incrementa soltanto
    quando un'associazione NUOVA viene scritta: le basi già presenti nella
    memoria non sono scritture.

    È una versione dichiaratamente osservatoria della funzione svolta e non
    ne cambia il contratto. I contatori descrivono il lavoro del modello e la
    misura dei tempi resta un esperimento distinto.
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


# ---------------------------------------------------------------------------
# Avvio protetto dalla guardia
# ---------------------------------------------------------------------------


def main() -> None:
    """Annuncia il lavoro da completare senza eseguire esperimenti."""
    print("LAB-PY-U9 - analisi: riepilogo_una_scansione e conta_coppie sono")
    print("da completare (fasi L1 e L2).")
    print("La suite deve prima fallire sui corpi mancanti: prima i test, poi il timer.")


if __name__ == "__main__":
    main()
