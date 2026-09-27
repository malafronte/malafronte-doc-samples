"""Dataset delle cinque famiglie e protocollo di misura dell'Unità 10.

Il modulo prepara gli input del confronto sperimentale fra le quattro
implementazioni elementari e ne misura la durata secondo il protocollo del
cap. PY-13, parte IV. Il confronto qui non è definitivo: l'Unità 11 estenderà
la stessa matrice a MergeSort e QuickSort.

Le **cinque famiglie** di input sono: `ordinato`, `inverso`, `quasi_ordinato`,
`molti_duplicati`, `pseudo_casuale`. La famiglia `quasi_ordinato` non è un
nome generico: viene costruita esattamente come dichiarato in `genera_famiglia`,
perché lo stesso nome può descrivere input diversi se non ne è specificata la
costruzione.

Ambiente: CPython sul computer. Il generatore è deterministico: a parità di
nome, dimensione e seme la lista è sempre la stessa, quindi gli algoritmi
confrontati ricevono gli **stessi** dati.

Regole del protocollo, non negoziabili in questa fase:

1. la correttezza si verifica **prima** di misurare;
2. la lista di lavoro è una copia separata dell'originale, preparata **fuori**
   dalla regione cronometrata;
3. la verifica del risultato e le stampe restano fuori dal timer;
4. si raccolgono più campioni e si conservano i valori grezzi;
5. la sintesi dichiarata è la mediana, con minimo e massimo accanto.
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

    Il seme è parte del protocollo: due esecuzioni con lo stesso seme
    producono gli stessi dati e le misure restano confrontabili.
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


# ---------------------------------------------------------------------------
# Protocollo di misura
# ---------------------------------------------------------------------------


def misura_ordinamento(ordinamento, originale, ripetizioni=5, chiamate_per_lotto=1):
    """Restituisce i campioni di durata, in secondi, di una chiamata di `ordinamento`.

    `ordinamento` è una funzione con il contratto degli ordinamenti didattici:
    ordina una lista sul posto e restituisce `None`. `originale` è la lista di
    riferimento, che **non** viene modificata. `ripetizioni` è il numero di
    campioni raccolti; `chiamate_per_lotto` è quante copie indipendenti
    ordinare dentro un singolo campione, per le prove troppo brevi.

    Il confine della regione cronometrata contiene **soltanto** le chiamate ad
    `ordinamento`. La preparazione delle copie, la verifica del risultato e la
    restituzione dei valori restano fuori. Il valore registrato è la durata
    media di una chiamata: `(fine - inizio) / chiamate_per_lotto`.
    """
    if ripetizioni < 1:
        raise ValueError("serve almeno un campione")
    if chiamate_per_lotto < 1:
        raise ValueError("serve almeno una chiamata per lotto")

    campioni = []
    for _ in range(ripetizioni):
        copie = [list(originale) for _ in range(chiamate_per_lotto)]
        inizio = time.perf_counter()
        for copia in copie:
            ordinamento(copia)
        fine = time.perf_counter()
        for copia in copie:
            if copia != sorted(originale):
                raise AssertionError("l'ordinamento ha prodotto un risultato diverso da sorted")
        campioni.append((fine - inizio) / chiamate_per_lotto)
    return campioni


def misura_ricerca(ricerca, valori, bersaglio, ripetizioni=5, chiamate_per_lotto=1):
    """Restituisce i campioni di durata, in secondi, di `ricerca(valori, bersaglio)`.

    Stesso protocollo di `misura_ordinamento`, con la differenza che la ricerca
    non modifica l'argomento e non serve alcuna copia: la stessa lista viene
    consultata da ogni chiamata del lotto. Il primo campione che non restituisce
    il risultato atteso viene segnalato con un'eccezione.
    """
    if ripetizioni < 1:
        raise ValueError("serve almeno un campione")
    if chiamate_per_lotto < 1:
        raise ValueError("serve almeno una chiamata per lotto")

    atteso = None
    for indice in range(len(valori)):
        if valori[indice] == bersaglio:
            atteso = indice
            break

    campioni = []
    for _ in range(ripetizioni):
        inizio = time.perf_counter()
        for _ in range(chiamate_per_lotto):
            risultato = ricerca(valori, bersaglio)
        fine = time.perf_counter()
        if risultato != atteso:
            raise AssertionError(f"la ricerca ha restituito {risultato}, atteso {atteso}")
        campioni.append((fine - inizio) / chiamate_per_lotto)
    return campioni


def sintesi_campioni(campioni):
    """Restituisce la sintesi descrittiva dei campioni: numero, minimo, mediana, massimo.

    La mediana dei campioni ordinati per m dispari è il valore centrale; per
    m pari è la media dei due centrali, e la convenzione va dichiarata. È una
    **scelta descrittiva**, non una stima del «vero tempo»: il valore grezzo
    resta la prova principale.
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
    # Prima tabella di controllo: due algoritmi, due famiglie, n = 200, cinque
    # campioni. I valori di durata appartengono alla macchina che esegue: qui si
    # verificano la FORMA della riga, la coerenza di sintesi e metadati e il
    # fatto che nessun algoritmo modifichi l'originale, non il numero stampato.
    import ordinamenti_u10 as ordi

    print("metadati:", metadati_misura())
    for nome, ordinamento in (("bubble_sort", ordi.bubble_sort),
                              ("insertion_sort", ordi.insertion_sort)):
        for famiglia in ("ordinato", "inverso"):
            originale = genera_famiglia(famiglia, 200)
            campioni = misura_ordinamento(ordinamento, originale, ripetizioni=5)
            print(riga_tabella(nome, famiglia, 200, sintesi_campioni(campioni)))
            assert originale == genera_famiglia(famiglia, 200)
