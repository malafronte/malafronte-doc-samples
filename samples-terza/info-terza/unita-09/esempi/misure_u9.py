"""Misure di riferimento dell'Unità 9: timer, ripetizioni e campioni.

Collocare il file in `programmi/misure_u9.py` della raccolta dello studente.
Il modulo raccoglie tre esperimenti distinti del capitolo PY-13, parte IV,
e non un unico confronto di velocità:

1. scansioni equivalenti: `riepilogo_una_scansione` contro
   `riepilogo_due_scansioni` sugli stessi dati, più l'arresto anticipato di
   `contiene_zero` con lo zero iniziale, intermedio, finale o assente;
2. tre varianti di Fibonacci: diretta, iterativa e con memoria, con la
   memoria NUOVA e la memoria GIÀ POPOLATA tenute in esperimenti separati;
3. conteggi dei cicli: tabelle esatte del modello, senza eseguire algoritmi
   quadratici su dati enormi e senza timer.

Timer: `import time` e due letture con `time.perf_counter()`; la durata è la
differenza fra le due letture ed è espressa in SECONDI. Non si usa
`time.time()`, che fornisce un istante di calendario e non una durata.

Regione cronometrata: le sole chiamate alla funzione studiata. Costruzione
dei dati, preparazione della memoria, verifica dei risultati, stampe e
grafici stanno fuori dal timer e non ci sono `assert` dentro la regione
cronometrata. Quando un lotto ripete K chiamate, il dato comprende anche il
costo del ciclo che le ripete e delle chiamate Python: è il costo del lotto,
dichiarato nella tabella, e non viene sottratto alcun ciclo vuoto.

Campioni: cinque ripetizioni per ogni punto di misura, con tutti i campioni
conservati. La mediana è l'elemento centrale dei campioni ordinati; minimo e
massimo descrivono la variabilità dei campioni raccolti e non sono un
intervallo di confidenza. Un singolo campione non è un tempo medio.

Le durate dipendono dall'ambiente e dal momento dell'esecuzione: questi dati
descrivono UNA esecuzione sull'ambiente dichiarato e non stabiliscono che un
algoritmo sia più veloce di un altro. Gli esempi deliberatamente errati non
compariscono: ogni funzione misurata è una versione corretta.

Nessun dato viene scritto su file: `open`, `csv` e `json` non compaiono. I
risultati vivono in liste e dizionari e il main li stampa come tabella
testuale, pronta per essere copiata nella scheda di laboratorio.

Esecuzione: uv run python programmi/misure_u9.py
"""

import platform
import time

from conteggi_cicli import (
    conta_attraversamento,
    conta_coppie_i_j,
    conta_dimezzamenti,
    conta_due_consecutivi,
    conta_due_indipendenti,
)
from conteggi_scansioni import (
    contiene_zero,
    contiene_zero_osservato,
    riepilogo_due_scansioni,
    riepilogo_una_scansione,
)
from confronto_fibonacci import fibonacci_diretto, fibonacci_iter, fibonacci_mem, memoria_delle_basi


# ---------------------------------------------------------------------------
# Configurazione dichiarata — dimensioni, ripetizioni, chiamate per lotto
# ---------------------------------------------------------------------------

# Cinque ripetizioni, numero dispari: così la mediana è l'elemento centrale
# dei campioni ordinati e non richiede una convenzione sui casi pari.
RIPETIZIONI = 5

# Esperimento 1: scansioni. La sequenza a raddoppi permette di osservare
# come cambiano le durate quando la dimensione raddoppia; il quarto valore
# rende il lotto più lungo e va tarato sull'ambiente disponibile.
DIMENSIONI_SCANSIONI = [100, 1_000, 10_000, 100_000]
CHIAMATE_PER_LOTTO_SCANSIONI = 20

# Esperimento 1b: arresto anticipato. Una sola dimensione, quattro famiglie
# di input che discriminano caso migliore, intermedio, peggiore e assenza.
DIMENSIONE_ARRESTO = 10_000
CHIAMATE_PER_LOTTO_ARRESTO = 20

# Esperimento 2: Fibonacci. Gli indici sono gli stessi per le tre varianti,
# così la domanda resta comparativa; per la sola diretta si usano 5, 10, 15,
# 20 e 25, mai 40 o 50 come impostazione predefinita. Il limite di
# ricorsione non viene aumentato.
INDICI_FIBONACCI = [5, 10, 15, 20, 25]
# Le chiamate per lotto crescono al diminuire del lavoro per chiamata:
# una singola chiamata piccola dura troppo poco per essere letta da sola.
CHIAMATE_PER_LOTTO_DIRETTA = {5: 2_000, 10: 500, 15: 50, 20: 5, 25: 1}
CHIAMATE_PER_LOTTO_ITERATIVA = 2_000
# Memoria nuova: una sola chiamata per lotto, con la memoria preparata prima
# del timer. Un lotto con K > 1 richiederebbe K memorie indipendenti.
CHIAMATE_PER_LOTTO_MEMORIA_NUOVA = 1
# Memoria già popolata: la stessa richiesta ripetuta su una memoria che non
# viene modificata, quindi le K chiamate del lotto sono equivalenti.
CHIAMATE_PER_LOTTO_MEMORIA_PIENA = 2_000

# Esperimento 3: conteggi dei cicli, dimensioni piccole e valore esatto.
N_CONTEGGI_CICLI = [2, 4, 8, 16]

# Regola riproducibile dei dati di scansione: ripetizione di questi cinque
# valori. Stessa regola e stessa dimensione producono sempre la stessa
# lista; la riproducibilità dei dati non rende riproducibili i tempi.
VALORI_BASE = [-2, -1, 0, 1, 2]


# ---------------------------------------------------------------------------
# Costruzione dei dati — sempre fuori dalla regione cronometrata
# ---------------------------------------------------------------------------


def costruisci_valori(n: int) -> list[int]:
    """Restituisce la lista dei dati costruiti con la regola dichiarata.

    Ripete `VALORI_BASE` fino a raggiungere n elementi. Dominio: n intero
    non negativo; per n = 0 la lista è vuota. La funzione viene sempre
    chiamata prima del timer: il costo della costruzione non entra nelle
    durate misurate.
    """
    return [VALORI_BASE[indice % len(VALORI_BASE)] for indice in range(n)]


def costruisci_caso_arresto(n: int, posizione_zero: str) -> list[int]:
    """Restituisce l'input di `contiene_zero` per lo studio dell'arresto.

    Dominio: n >= 1 e `posizione_zero` una fra "iniziale", "intermedia",
    "finale" e "assente". Lo zero viene collocato in posizione 0, n // 2 o
    n - 1; nel caso "assente" la lista non contiene zeri. Tutti gli altri
    valori sono 7. I confronti attesi valgono 1, n // 2 + 1, n ed n: la
    casualità non sostituisce questi casi discriminanti.
    """
    if n < 1:
        raise ValueError("il caso di arresto richiede almeno un elemento")
    if posizione_zero not in ("iniziale", "intermedia", "finale", "assente"):
        raise ValueError(f"posizione_zero non ammessa: {posizione_zero}")
    valori = [7] * n
    if posizione_zero == "iniziale":
        valori[0] = 0
    elif posizione_zero == "intermedia":
        valori[n // 2] = 0
    elif posizione_zero == "finale":
        valori[n - 1] = 0
    return valori


# ---------------------------------------------------------------------------
# Timer minimo — due letture, differenza in secondi, nessun assert nel misurato
# ---------------------------------------------------------------------------


def misura_lotti(esegui_lotto, ripetizioni: int = RIPETIZIONI) -> list[float]:
    """Esegue `ripetizioni` lotti e restituisce le durate in secondi.

    La regione cronometrata copre la sola chiamata a `esegui_lotto`, che
    deve contenere esclusivamente le chiamate alla funzione studiata e, per
    i lotti con K > 1, il ciclo che le ripete. Due letture con
    `time.perf_counter()` e differenza fra le due: la durata ha come punto
    zero un istante privo di significato assoluto. I campioni restano tutti,
    nell'ordine in cui sono stati raccolti.
    """
    campioni = []
    for _ripetizione in range(ripetizioni):
        inizio = time.perf_counter()
        esegui_lotto()
        campioni.append(time.perf_counter() - inizio)
    return campioni


def punto_di_misura(
    esperimento: str,
    algoritmo: str,
    dimensione: int,
    significato_dimensione: str,
    famiglia_input: str,
    stato_memoria: str,
    chiamate_per_lotto: int,
    campioni: list[float],
    nota: str = "non applicabile",
) -> dict:
    """Riassume un punto di misura con campioni grezzi e sintesi descrittiva.

    `campioni` contiene le durate dei lotti in secondi, nell'ordine di
    raccolta; `chiamate_per_lotto` è il K dichiarato. Il risultato conserva
    tutti i campioni, la durata per chiamata di ciascun campione e la
    sintesi: mediana, minimo e massimo. La mediana è l'elemento centrale
    dell'elenco ordinato; con cinque campioni equivale a
    `sorted(campioni)[2]`, come mostrato qui sotto in forma generale per un
    numero dispari di ripetizioni. Minimo e massimo descrivono i campioni
    raccolti e non sono un intervallo di confidenza.
    """
    if len(campioni) != RIPETIZIONI:
        raise ValueError("il punto di misura richiede esattamente RIPETIZIONI campioni")
    ordinati = sorted(campioni)
    mediana = ordinati[len(ordinati) // 2]  # con cinque campioni: sorted(campioni)[2]
    return {
        "esperimento": esperimento,
        "algoritmo": algoritmo,
        "dimensione": dimensione,
        "significato_dimensione": significato_dimensione,
        "famiglia_input": famiglia_input,
        "stato_memoria": stato_memoria,
        "nota": nota,
        "chiamate_per_lotto": chiamate_per_lotto,
        "campioni_lotto_s": list(campioni),
        "campioni_chiamata_s": [durata / chiamate_per_lotto for durata in campioni],
        "mediana_chiamata_s": mediana / chiamate_per_lotto,
        "minimo_chiamata_s": min(campioni) / chiamate_per_lotto,
        "massimo_chiamata_s": max(campioni) / chiamate_per_lotto,
    }


def tabella_grezza(punti: list[dict]) -> list[dict]:
    """Espande i punti nella tabella minima di misure, una riga per ripetizione.

    Ogni riga ha le chiavi dello schema minimo: `esperimento`, `algoritmo`,
    `dimensione`, `significato_dimensione`, `famiglia_input`, `stato_memoria`,
    `ripetizione`, `chiamate_per_lotto`, `durata_lotto_s` e
    `durata_per_chiamata_s`. I campi non pertinenti, per esempio la memoria
    per una scansione, sono marcati «non applicabile».
    """
    righe = []
    for punto in punti:
        for indice, durata_lotto_s in enumerate(punto["campioni_lotto_s"], start=1):
            righe.append(
                {
                    "esperimento": punto["esperimento"],
                    "algoritmo": punto["algoritmo"],
                    "dimensione": punto["dimensione"],
                    "significato_dimensione": punto["significato_dimensione"],
                    "famiglia_input": punto["famiglia_input"],
                    "stato_memoria": punto["stato_memoria"],
                    "ripetizione": indice,
                    "chiamate_per_lotto": punto["chiamate_per_lotto"],
                    "durata_lotto_s": durata_lotto_s,
                    "durata_per_chiamata_s": durata_lotto_s / punto["chiamate_per_lotto"],
                }
            )
    return righe


# ---------------------------------------------------------------------------
# Esperimento 1 — scansioni equivalenti
# ---------------------------------------------------------------------------


def esperimento_scansioni() -> list[dict]:
    """Misura una e due scansioni sullo stesso input costruito a regola.

    Domanda: quanto dura ciascuna delle due procedure equivalenti sugli
    stessi dati? Input: liste di interi costruite ripetendo `VALORI_BASE`,
    con dimensione n; famiglia di input fissa e riproducibile; nessun dato
    casuale. Variante dell'algoritmo: le due funzioni ORDINARIE di
    `conteggi_scansioni`, senza contatori, perché strumentare altererebbe il
    tempo. Unità contata dal modello: la visita a un elemento (n contro 2n);
    unità misurata: secondi per chiamata. Ipotesi: operazioni su numeri di
    dimensione limitata a costo unitario; input e output esclusi dal timer.

    L'ordine delle due misure alterna fra le ripetizioni: riduce l'effetto
    sistematico dell'ordine senza promettere l'eliminazione del rumore. La
    stessa lista viene passata a entrambe le funzioni, che non la mutano.
    """
    punti = []
    for n in DIMENSIONI_SCANSIONI:
        valori = costruisci_valori(n)

        # Verifica preliminare FUORI dal timer: la correttezza precede la
        # misura e non è la misura a certificare la correttezza.
        atteso = riepilogo_due_scansioni(valori)
        if riepilogo_una_scansione(valori) != atteso:
            raise ValueError(f"i due riepiloghi non concordano per n = {n}")

        campioni_una: list[float] = []
        campioni_due: list[float] = []

        def lotto_una():
            for _ripetizione in range(CHIAMATE_PER_LOTTO_SCANSIONI):
                riepilogo_una_scansione(valori)

        def lotto_due():
            for _ripetizione in range(CHIAMATE_PER_LOTTO_SCANSIONI):
                riepilogo_due_scansioni(valori)

        for ripetizione in range(RIPETIZIONI):
            if ripetizione % 2 == 0:
                sequenza = [(campioni_una, lotto_una), (campioni_due, lotto_due)]
            else:
                sequenza = [(campioni_due, lotto_due), (campioni_una, lotto_una)]
            for raccolta, lotto in sequenza:
                inizio = time.perf_counter()
                lotto()
                raccolta.append(time.perf_counter() - inizio)

        for algoritmo, campioni in (
            ("riepilogo_una_scansione", campioni_una),
            ("riepilogo_due_scansioni", campioni_due),
        ):
            punti.append(
                punto_di_misura(
                    esperimento="scansioni equivalenti",
                    algoritmo=algoritmo,
                    dimensione=n,
                    significato_dimensione="numero di elementi della lista",
                    famiglia_input="ripetizione di [-2, -1, 0, 1, 2]",
                    stato_memoria="non applicabile",
                    chiamate_per_lotto=CHIAMATE_PER_LOTTO_SCANSIONI,
                    campioni=campioni,
                    nota=f"visite attese: {n} per una scansione, {2 * n} per due",
                )
            )
    return punti


def esperimento_arresto() -> list[dict]:
    """Misura `contiene_zero` con lo zero in quattro posizioni diverse.

    Domanda: come cambia la durata quando l'arresto anticipato è più o meno
    vicino? Input: liste di n = `DIMENSIONE_ARRESTO` valori con lo zero
    iniziale, intermedio, finale o assente, costruite fuori dal timer.
    Variante: la funzione ORDINARIA `contiene_zero`, senza contatori.
    Unità contata dal modello: il confronto `valore == 0`, da 1 a n;
    unità misurata: secondi per chiamata. La colonna `nota` riporta i
    confronti attesi, verificati a parte con la versione strumentata.
    """
    punti = []
    for posizione_zero in ("iniziale", "intermedia", "finale", "assente"):
        valori = costruisci_caso_arresto(DIMENSIONE_ARRESTO, posizione_zero)

        # Verifica preliminare FUORI dal timer, con la versione strumentata
        # usata solo per contare: il tempo misurato resta quello della
        # versione ordinaria.
        esito, statistiche = contiene_zero_osservato(valori)
        atteso = posizione_zero != "assente"
        if esito is not atteso or contiene_zero(valori) is not atteso:
            raise ValueError(f"esito inatteso per il caso {posizione_zero}")

        def lotto():
            for _ripetizione in range(CHIAMATE_PER_LOTTO_ARRESTO):
                contiene_zero(valori)

        campioni = misura_lotti(lotto)
        punti.append(
            punto_di_misura(
                esperimento="arresto anticipato",
                algoritmo="contiene_zero",
                dimensione=DIMENSIONE_ARRESTO,
                significato_dimensione="numero di elementi della lista",
                famiglia_input=f"zero {posizione_zero}",
                stato_memoria="non applicabile",
                chiamate_per_lotto=CHIAMATE_PER_LOTTO_ARRESTO,
                campioni=campioni,
                nota=f"confronti attesi per chiamata: {statistiche['confronti']}",
            )
        )
    return punti


# ---------------------------------------------------------------------------
# Esperimento 2 — le tre varianti di Fibonacci
# ---------------------------------------------------------------------------


def esperimento_fibonacci() -> list[dict]:
    """Misura le tre varianti di Fibonacci sulla memoria dichiarata.

    Domanda: come cambiano le durate al crescere dell'indice n, a parità di
    risultato atteso? Input: gli indici `INDICI_FIBONACCI`, gli stessi per le
    tre varianti; n è l'indice richiesto e non una lunghezza di lista.
    Varianti: `fibonacci_diretto`, `fibonacci_iter` e `fibonacci_mem`, tutte
    ordinarie e senza contatori. Unità contata dal modello: addizioni e
    operazioni di dizionario a costo unitario; unità misurata: secondi per
    chiamata. Nessun aumento del limite di ricorsione.

    La memoria NUOVA e la memoria GIÀ POPOLATA sono due esperimenti distinti
    e non si aggregano mai in una mediana. Per la memoria nuova ogni calcolo
    riceve un `{0: 0, 1: 1}` indipendente, preparato prima del timer con
    K = 1: si misura il solo nucleo della funzione. Per la memoria già
    popolata la memoria viene riempita fino a n PRIMA del timer e la
    richiesta ripetuta legge la voce già disponibile senza modificare il
    dizionario; gli indici presenti vanno da 0 a n inclusi.
    """
    punti = []
    for n in INDICI_FIBONACCI:
        significato = "indice di Fibonacci n"

        # Verifica preliminare FUORI dal timer: le tre varianti devono
        # concordare sul valore prima di essere misurate.
        atteso = fibonacci_iter(n)
        if fibonacci_diretto(n) != atteso or fibonacci_mem(n, memoria_delle_basi()) != atteso:
            raise ValueError(f"le varianti di Fibonacci non concordano per n = {n}")

        # 1) versione diretta: chiamate indipendenti, lotti dichiarati
        def lotto_diretta():
            for _ripetizione in range(CHIAMATE_PER_LOTTO_DIRETTA[n]):
                fibonacci_diretto(n)

        punti.append(
            punto_di_misura(
                esperimento="varianti di Fibonacci",
                algoritmo="fibonacci_diretto",
                dimensione=n,
                significato_dimensione=significato,
                famiglia_input="indice n",
                stato_memoria="non applicabile",
                chiamate_per_lotto=CHIAMATE_PER_LOTTO_DIRETTA[n],
                campioni=misura_lotti(lotto_diretta),
            )
        )

        # 2) versione iterativa: nessuno stato fra le chiamate del lotto
        def lotto_iterativa():
            for _ripetizione in range(CHIAMATE_PER_LOTTO_ITERATIVA):
                fibonacci_iter(n)

        punti.append(
            punto_di_misura(
                esperimento="varianti di Fibonacci",
                algoritmo="fibonacci_iter",
                dimensione=n,
                significato_dimensione=significato,
                famiglia_input="indice n",
                stato_memoria="non applicabile",
                chiamate_per_lotto=CHIAMATE_PER_LOTTO_ITERATIVA,
                campioni=misura_lotti(lotto_iterativa),
            )
        )

        # 3) memoria NUOVA: K = 1 e memoria preparata prima del timer
        campioni_memoria_nuova = []
        for _ripetizione in range(RIPETIZIONI):
            memoria = memoria_delle_basi()  # preparazione FUORI dal timer
            inizio = time.perf_counter()
            fibonacci_mem(n, memoria)  # sola chiamata cronometrata
            campioni_memoria_nuova.append(time.perf_counter() - inizio)

        punti.append(
            punto_di_misura(
                esperimento="varianti di Fibonacci",
                algoritmo="fibonacci_mem",
                dimensione=n,
                significato_dimensione=significato,
                famiglia_input="indice n",
                stato_memoria="nuova dalle sole basi {0: 0, 1: 1}",
                chiamate_per_lotto=CHIAMATE_PER_LOTTO_MEMORIA_NUOVA,
                campioni=campioni_memoria_nuova,
            )
        )

        # 4) memoria GIÀ POPOLATA: esperimento separato, mai aggregato
        memoria = memoria_delle_basi()
        fibonacci_mem(n, memoria)  # popolamento FUORI dal timer
        voci_presenti = sorted(memoria)

        def lotto_memoria_piena():
            for _ripetizione in range(CHIAMATE_PER_LOTTO_MEMORIA_PIENA):
                fibonacci_mem(n, memoria)

        punti.append(
            punto_di_misura(
                esperimento="varianti di Fibonacci",
                algoritmo="fibonacci_mem",
                dimensione=n,
                significato_dimensione=significato,
                famiglia_input="richiesta ripetuta dello stesso indice",
                stato_memoria=f"già popolata fino a n = {n}",
                chiamate_per_lotto=CHIAMATE_PER_LOTTO_MEMORIA_PIENA,
                campioni=misura_lotti(lotto_memoria_piena),
                nota=f"indici presenti: da {voci_presenti[0]} a {voci_presenti[-1]}",
            )
        )
    return punti


# ---------------------------------------------------------------------------
# Esperimento 3 — conteggi esatti dei cicli, senza timer
# ---------------------------------------------------------------------------


def esperimento_conteggi_cicli() -> list[dict]:
    """Calcola i conteggi esatti di quattro procedimenti, senza misurarli.

    Domanda: come crescono i conteggi esatti al crescere di n? Le tabelle
    dei conteggi possono essere esatte: non è necessario eseguire algoritmi
    quadratici su dataset enormi per disegnarne le funzioni. Si usano le
    funzioni di `conteggi_cicli` su n piccoli (`N_CONTEGGI_CICLI`): i valori
    sono conteggi del modello, non durate, e non vanno confusi con i tempi.
    """
    righe = []
    for n in N_CONTEGGI_CICLI:
        righe.append(
            {
                "n": n,
                "attraversamento_singolo": conta_attraversamento(n),
                "due_attraversamenti": conta_due_consecutivi(n),
                "due_cicli_indipendenti": conta_due_indipendenti(n),
                "coppie_i_j": conta_coppie_i_j(n),
                "dimezzamenti": conta_dimezzamenti(n),
            }
        )
    return righe


# ---------------------------------------------------------------------------
# Raccolta, stampa e avvio
# ---------------------------------------------------------------------------


def esegui_esperimenti() -> dict:
    """Esegue i tre esperimenti e restituisce tutti i dati in memoria.

    Il risultato ha le chiavi `ambiente`, `punti`, `tabella_grezza` e
    `conteggi_cicli`. Nessun file viene aperto o scritto. I dati possono
    passarsi direttamente a `grafici_u9`, che disegna le durate senza
    ritrascrivere i campioni a mano.
    """
    punti = esperimento_scansioni() + esperimento_arresto() + esperimento_fibonacci()
    return {
        "ambiente": {
            "interprete": f"CPython {platform.python_version()}",
            "sistema": platform.platform(),
            "ripetizioni": RIPETIZIONI,
            "timer": "time.perf_counter()",
        },
        "punti": punti,
        "tabella_grezza": tabella_grezza(punti),
        "conteggi_cicli": esperimento_conteggi_cicli(),
    }


def stampa_risultati(dati: dict) -> None:
    """Stampa le tabelle testuali dei dati raccolti.

    Le durate sono espresse in secondi con notazione scientifica, così
    valori piccoli non vengono azzerati dall'arrotondamento. La prima
    tabella descrive la configurazione di ogni punto di misura, la seconda
    riassume le durate per chiamata, la terza conserva tutti i campioni
    grezzi con lo schema minimo, la quarta riporta i conteggi esatti dei
    cicli. Stampa e formattazione stanno fuori da ogni misura.
    """
    ambiente = dati["ambiente"]
    print("Ambiente di misura")
    for chiave, valore in ambiente.items():
        print(f"  {chiave}: {valore}")

    print()
    print("Configurazione dei punti di misura")
    print(
        "esperimento              algoritmo              n       "
        "famiglia_input                         stato_memoria                      nota"
    )
    for punto in dati["punti"]:
        print(
            f"{punto['esperimento']:<25} {punto['algoritmo']:<22} "
            f"{punto['dimensione']:<7} {punto['famiglia_input']:<38} "
            f"{punto['stato_memoria']:<33} {punto['nota']}"
        )

    print()
    print("Sintesi per punto di misura — durata per chiamata in secondi")
    print(
        "esperimento              algoritmo              n       K      "
        "mediana    minimo     massimo"
    )
    for punto in dati["punti"]:
        print(
            f"{punto['esperimento']:<25} {punto['algoritmo']:<22} "
            f"{punto['dimensione']:<7} {punto['chiamate_per_lotto']:<6} "
            f"{punto['mediana_chiamata_s']:.3e}  "
            f"{punto['minimo_chiamata_s']:.3e}  "
            f"{punto['massimo_chiamata_s']:.3e}"
        )

    print()
    print("Campioni grezzi — tutti i campioni conservati, durate in secondi")
    print(
        "esperimento              algoritmo              n       rip  K      "
        "durata lotto  durata per chiamata"
    )
    for riga in dati["tabella_grezza"]:
        print(
            f"{riga['esperimento']:<25} {riga['algoritmo']:<22} "
            f"{riga['dimensione']:<7} {riga['ripetizione']:<4} "
            f"{riga['chiamate_per_lotto']:<6} "
            f"{riga['durata_lotto_s']:.3e}     {riga['durata_per_chiamata_s']:.3e}"
        )

    print()
    print("Conteggi esatti dei cicli — valori del modello, non durate")
    print("n     attravers.  2 attravers.  n^2     coppie i<j  dimezzamenti")
    for riga in dati["conteggi_cicli"]:
        print(
            f"{riga['n']:<5} {riga['attraversamento_singolo']:<11} "
            f"{riga['due_attraversamenti']:<13} {riga['due_cicli_indipendenti']:<7} "
            f"{riga['coppie_i_j']:<11} {riga['dimezzamenti']}"
        )


def main() -> dict:
    """Esegue gli esperimenti, stampa le tabelle e restituisce i dati.

    Il valore restituito può essere passato a `grafici_u9.grafico_durate`.
    """
    dati = esegui_esperimenti()
    stampa_risultati(dati)
    return dati


if __name__ == "__main__":
    # Nessuna misura viene eseguita all'import: questa è l'unica sede di avvio.
    main()
