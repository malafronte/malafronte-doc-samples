"""Cinque famiglie di input e protocollo di misura dell'Unità 11.

Il modulo prepara gli input del confronto sperimentale fra MergeSort, QuickSort,
gli ordinamenti elementari del cap. PY-14 e `sorted`, e ne misura la durata
secondo il protocollo del cap. PY-13, parte IV, e della guida
«Misurare le prestazioni di Python». È la **seconda** campagna di misura del
corso: la prima, sulle sole procedure elementari, è nel LAB-PY-U10.

Le **cinque famiglie** di input sono quelle di U10, riprodotte qui con la stessa
regola di costruzione e lo stesso seme: `ordinato`, `inverso`, `quasi_ordinato`,
`molti_duplicati`, `pseudo_casuale`. La famiglia `quasi_ordinato` non è un nome
generico: viene costruita esattamente come dichiarato in `genera_famiglia`,
perché lo stesso nome può descrivere input diversi se non ne è specificata la
costruzione.

Ambiente: CPython sul computer. Il generatore è deterministico: a parità di
nome, dimensione e seme la lista è sempre la stessa, quindi gli algoritmi
confrontati ricevono gli **stessi** dati.

Regole del protocollo, non negoziabili in questa fase:

1. la correttezza si verifica **prima** di misurare;
2. ogni procedura riceve una **copia nuova** dell'originale, preparata **fuori**
   dalla regione cronometrata;
3. la verifica del risultato e le stampe restano fuori dal timer;
4. si raccolgono più campioni e si conservano i valori grezzi;
5. la sintesi dichiarata è la mediana, con minimo e massimo accanto.

Scelta esplicita sugli effetti: il costo delle copie **esterne** è escluso per
tutte le procedure, mentre l'eventuale copia **interna** di `merge_sort` o di
`sorted` fa parte dell'operazione misurata. Le versioni con contatori non si
cronometrano.

Nessun file viene scritto: i campioni si conservano copiando l'output testuale
nel documento di lavoro con l'editor.
"""

import random
import sys
import time


FAMIGLIE = ("ordinato", "inverso", "quasi_ordinato", "molti_duplicati", "pseudo_casuale")

SEME_PREDEFINITO = 20260927


def genera_famiglia(nome, n, seme=SEME_PREDEFINITO):
    """Restituisce una lista di `n` interi della famiglia `nome`.

    Costruzione esatta delle cinque famiglie, con `n` numero di elementi:

    | `nome` | Costruzione |
    |---|---|
    | `ordinato` | `list(range(n))`, già in ordine crescente |
    | `inverso` | `list(range(n, 0, -1))`, ordine strettamente decrescente |
    | `quasi_ordinato` | `list(range(n))` con due scambi dichiarati: le posizioni `(0, 1)` e `(n // 2, n // 2 + 1)`; richiede `n >= 4`, altrimenti la lista resta ordinata e il caso è dichiarato |
    | `molti_duplicati` | `n` valori estratti con `random.Random(seme).randrange(3)`, quindi solo 0, 1 e 2 |
    | `pseudo_casuale` | `n` valori estratti con `random.Random(seme).randrange(n + 1)`, con il seme esplicito |

    Il seme è parte del protocollo: due esecuzioni con lo stesso seme producono
    gli stessi dati e le misure restano confrontabili.
    """
    if nome not in FAMIGLIE:
        raise ValueError(f"famiglia sconosciuta: {nome!r}; ammesse: {FAMIGLIE}")
    if n < 0:
        raise ValueError("il numero di elementi non può essere negativo")

    if nome == "ordinato":
        return list(range(n))
    if nome == "inverso":
        return list(range(n, 0, -1))
    if nome == "quasi_ordinato":
        valori = list(range(n))
        if n >= 4:
            valori[0], valori[1] = valori[1], valori[0]
            meta = n // 2
            valori[meta], valori[meta + 1] = valori[meta + 1], valori[meta]
        return valori
    if nome == "molti_duplicati":
        casuale = random.Random(seme)
        return [casuale.randrange(3) for _ in range(n)]
    casuale = random.Random(seme)
    return [casuale.randrange(n + 1) for _ in range(n)]


def copie_indipendenti(originale, quante):
    """Restituisce `quante` copie separate di `originale`, una per chiamata.

    Le copie si preparano **fuori** dalla regione cronometrata: ogni procedura
    riceve la propria lista e non modifica quella degli altri algoritmi.
    """
    return [list(originale) for _ in range(quante)]


# ---------------------------------------------------------------------------
# Ricerche del cap. PY-14, contratto del primo indice
# ---------------------------------------------------------------------------


def cerca_lineare(valori, bersaglio):
    """Restituisce il primo indice di `bersaglio` in `valori`, oppure `None`.

    Nessuna precondizione di ordinamento. L'uscita è al primo incontro e `0` è
    un risultato valido: l'assenza si riconosce con `is None`.
    """
    for indice in range(len(valori)):
        if valori[indice] == bersaglio:
            return indice
    return None


def cerca_dicotomica(valori, bersaglio):
    """Restituisce il primo indice di `bersaglio` in `valori` ordinato, oppure `None`.

    Precondizione: `valori` è una lista **non decrescente**; il controllo non è
    compito della funzione. Estremi inclusivi, medio `(sinistra + destra) // 2`;
    a parità si aggiorna il candidato e si prosegue nella metà **sinistra**, per
    restituire il primo indice.
    """
    sinistra = 0
    destra = len(valori) - 1
    candidato = None
    while sinistra <= destra:
        medio = (sinistra + destra) // 2
        if valori[medio] == bersaglio:
            candidato = medio
            destra = medio - 1
        elif valori[medio] < bersaglio:
            sinistra = medio + 1
        else:
            destra = medio - 1
    return candidato


# ---------------------------------------------------------------------------
# Protocollo di misura
# ---------------------------------------------------------------------------


def misura_ordinamento(procedura, originale, ripetizioni=5, chiamate_per_lotto=1):
    """Restituisce i campioni di durata, in secondi, di una chiamata di `procedura`.

    Contratto unico di misura per le procedure con effetti diversi: `procedura`
    riceve una **lista nuova** e o la ordina sul posto restituendo `None` -
    come `quick_sort`, `insertion_sort` o una lambda che chiama `list.sort` -
    oppure restituisce la lista ordinata **senza modificare** l'argomento, come
    `merge_sort` e `sorted`. `originale` è la lista di riferimento e **non** viene
    modificata. `ripetizioni` è il numero di campioni raccolti;
    `chiamate_per_lotto` è quante copie indipendenti ordinare dentro un singolo
    campione, per le prove troppo brevi.

    Il confine della regione cronometrata contiene **soltanto** le chiamate a
    `procedura`. La preparazione delle copie, la verifica del risultato e la
    restituzione dei valori restano fuori. Il valore registrato è la durata media
    di una chiamata: `(fine - inizio) / chiamate_per_lotto`.
    """
    if ripetizioni < 1:
        raise ValueError("serve almeno un campione")
    if chiamate_per_lotto < 1:
        raise ValueError("serve almeno una chiamata per lotto")

    atteso = sorted(originale)
    campioni = []
    for _ in range(ripetizioni):
        copie = copie_indipendenti(originale, chiamate_per_lotto)
        inizio = time.perf_counter()
        risultati = [procedura(copia) for copia in copie]
        fine = time.perf_counter()
        for copia, risultato in zip(copie, risultati):
            effettivo = copia if risultato is None else risultato
            if effettivo != atteso:
                raise AssertionError("la procedura ha prodotto un risultato diverso da sorted")
        campioni.append((fine - inizio) / chiamate_per_lotto)
    return campioni


def misura_ricerca(ricerca, valori, bersaglio, ripetizioni=5, chiamate_per_lotto=1):
    """Restituisce i campioni di durata, in secondi, di `ricerca(valori, bersaglio)`.

    Stesso protocollo di `misura_ordinamento`, con la differenza che la ricerca
    non modifica l'argomento e non serve alcuna copia: la stessa lista ordinata
    viene consultata da ogni chiamata del lotto. La preparazione dell'ordine -
    l'ordinamento che ha reso `valori` ordinata - resta **fuori** da questa misura
    e va cronometrata separatamente.
    """
    if ripetizioni < 1:
        raise ValueError("serve almeno un campione")
    if chiamate_per_lotto < 1:
        raise ValueError("serve almeno una chiamata per lotto")

    campioni = []
    for _ in range(ripetizioni):
        inizio = time.perf_counter()
        risultati = [ricerca(valori, bersaglio) for _ in range(chiamate_per_lotto)]
        fine = time.perf_counter()
        atteso = cerca_lineare(valori, bersaglio)
        for risultato in risultati:
            if risultato != atteso:
                raise AssertionError("la ricerca ha prodotto un risultato inatteso")
        campioni.append((fine - inizio) / chiamate_per_lotto)
    return campioni


def misura_sequenza_ricerche(ricerca, valori, bersagli, ripetizioni=5):
    """Restituisce i campioni di durata, in secondi, di una **serie** di ricerche.

    `bersagli` è una lista di chiavi: un campione registra la durata complessiva
    di `len(bersagli)` interrogazioni successive sulla **stessa** lista `valori`,
    che non viene modificata. Serve a confrontare la somma delle interrogazioni
    con il costo della preparazione dell'ordine, che resta fuori dal timer.

    La verifica del risultato è fuori dal timer e confronta ogni esito con
    `cerca_lineare`.
    """
    if ripetizioni < 1:
        raise ValueError("serve almeno un campione")
    if not bersagli:
        raise ValueError("serve almeno una interrogazione")

    campioni = []
    for _ in range(ripetizioni):
        inizio = time.perf_counter()
        risultati = [ricerca(valori, bersaglio) for bersaglio in bersagli]
        fine = time.perf_counter()
        attesi = [cerca_lineare(valori, bersaglio) for bersaglio in bersagli]
        if risultati != attesi:
            raise AssertionError("la sequenza ha prodotto esiti inattesi")
        campioni.append(fine - inizio)
    return campioni


def sintesi_campioni(campioni):
    """Restituisce la sintesi descrittiva: numero, minimo, mediana, massimo.

    Per `m` dispari la mediana è il valore centrale; per `m` pari è la media dei
    due centrali, e la convenzione va dichiarata. È una **scelta descrittiva**,
    non una stima del «vero tempo»: il valore grezzo resta la prova principale.
    """
    if not campioni:
        raise ValueError("nessun campione da riassumere")
    ordinati = sorted(campioni)
    m = len(ordinati)
    meta = m // 2
    if m % 2 == 1:
        mediana = ordinati[meta]
    else:
        mediana = (ordinati[meta - 1] + ordinati[meta]) / 2
    return {
        "numero": m,
        "minimo": ordinati[0],
        "mediana": mediana,
        "massimo": ordinati[-1],
        "campioni": ordinati,
    }


def metadati_misura():
    """Restituisce i metadati da conservare accanto a ogni serie di campioni."""
    return {
        "timer": "time.perf_counter",
        "unita": "secondi per chiamata",
        "python": sys.version.split()[0],
        "piattaforma": sys.platform,
        "seme": SEME_PREDEFINITO,
    }


def riga_tabella(algoritmo, famiglia, n, sintesi):
    """Restituisce una riga di testo della tabella dei risultati."""
    return (
        f"{algoritmo:<28} {famiglia:<15} n={n:<7} "
        f"mediana={sintesi['mediana'] * 1000:10.4f} ms  "
        f"min={sintesi['minimo'] * 1000:10.4f} ms  "
        f"max={sintesi['massimo'] * 1000:10.4f} ms  "
        f"campioni={sintesi['numero']}"
    )


if __name__ == "__main__":
    from merge_quick_u11 import merge_sort, quick_sort

    print("Metadati della misura:")
    print(metadati_misura())

    print()
    print("Confronto di esempio su due famiglie e due dimensioni.")
    print("Le durate appartengono a chi esegue: la FORMA della tabella è riproducibile, non i valori.")
    procedure = [
        ("merge_sort", merge_sort),
        ("quick_sort", quick_sort),
        ("sorted", lambda valori: sorted(valori)),
    ]
    for famiglia in ("ordinato", "pseudo_casuale"):
        for n in (200, 400):
            originale = genera_famiglia(famiglia, n)
            for nome, procedura in procedure:
                campioni = misura_ordinamento(procedura, originale, ripetizioni=5)
                print(riga_tabella(nome, famiglia, n, sintesi_campioni(campioni)))

    print()
    print("Preparazione dell'ordine e interrogazioni successive:")
    originale = genera_famiglia("pseudo_casuale", 2000)
    ordinata = sorted(originale)
    preparazione = misura_ordinamento(lambda valori: sorted(valori), originale, ripetizioni=5)
    bersagli = [ordinata[i * 7] for i in range(200)]
    serie = misura_sequenza_ricerche(cerca_dicotomica, ordinata, bersagli, ripetizioni=5)
    print(riga_tabella("sorted (preparazione)", "pseudo_casuale", 2000, sintesi_campioni(preparazione)))
    print(riga_tabella("dicotomica x 200", "pseudo_casuale", 2000, sintesi_campioni(serie)))
