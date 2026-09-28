"""Confronto sperimentale e grafico delle prestazioni degli ordinamenti (U11).

Il modulo misura le procedure di ordinamento sulle cinque famiglie di input di
`misure_u11.py` e produce due oggetti:

1. **tabelle testuali** su stdout, con mediana, minimo e massimo di cinque
   campioni per ogni tripletta procedimento/famiglia/dimensione: sono la tabella
   equivalente del grafico e la base di ogni conclusione;
2. **un grafico PNG** con due riquadri - la famiglia `pseudo_casuale` e la
   famiglia `ordinato` - che confronta le durate medie di quattro procedure.

Le durate appartengono a chi esegue: la **forma** delle tabelle e del grafico è
riproducibile, i valori no. Il grafico non sostituisce la tabella: ogni
affermazione della relazione si appoggia ai numeri, il grafico li rende
leggibili.

Ambiente: CPython sul computer, sola libreria standard per le misure;
`matplotlib` è richiesto **solo** per disegnare, e si installa in un progetto
locale con `uv add matplotlib` oppure, per una sola esecuzione, con
`uv run --with matplotlib python esempi/grafico_u11.py`.

Esecuzione dalla cartella `unita-11/`:

    uv run python esempi/grafico_u11.py                    # solo tabelle
    uv run --with matplotlib python esempi/grafico_u11.py  # tabelle e grafico

Il file PNG viene scritto nella cartella corrente con il nome
`confronto-ordinamenti-u11.png`, salvo indicare un percorso diverso come primo
argomento della riga di comando.
"""

import sys

from merge_quick_u11 import merge_sort, quick_sort
from misure_u11 import (
    FAMIGLIE,
    genera_famiglia,
    metadati_misura,
    misura_ordinamento,
    riga_tabella,
    sintesi_campioni,
)
from ordinamenti_elementari_u11 import (
    bubble_sort,
    bubble_sort_ottimizzato,
    insertion_sort,
    selection_sort,
)

# Procedure confrontate: nome pubblico e funzione con il contratto di misura.
# Le procedure che restituiscono una lista nuova sono avvolte in una lambda che
# scarta il risultato: il contratto unico di `misura_ordinamento` accetta sia
# procedure in-place sia procedure che restituiscono la lista ordinata.
PROCEDURE = (
    ("insertion_sort", insertion_sort),
    ("selection_sort", selection_sort),
    ("bubble_sort", bubble_sort),
    ("bubble_sort_ottimizzato", bubble_sort_ottimizzato),
    ("merge_sort", merge_sort),
    ("quick_sort", quick_sort),
    ("sorted", lambda valori: sorted(valori)),
)

# Le quattro procedure rappresentate nel grafico, nell'ordine della legenda.
NEL_GRAFICO = ("insertion_sort", "merge_sort", "quick_sort", "sorted")

DIMENSIONI = (100, 200, 400, 800)
RIPETIZIONI = 5
FAMIGLIE_NEL_GRAFICO = ("pseudo_casuale", "ordinato")


def misura_completa(procedure=PROCEDURE, famiglie=FAMIGLIE, dimensioni=DIMENSIONI):
    """Restituisce `{(procedimento, famiglia, n): sintesi}` con cinque campioni per cella.

    Una coppia procedimento/famiglia che solleva `RecursionError` - QuickSort
    canonica su `ordinato`, `inverso` o `molti_duplicati` oltre il limite di
    ricorsione - viene registrata come `None`: «non misurato», con la causa
    dichiarata, non come durata.
    """
    risultati = {}
    for famiglia in famiglie:
        for n in dimensioni:
            originale = genera_famiglia(famiglia, n)
            for nome, procedura in procedure:
                try:
                    campioni = misura_ordinamento(
                        procedura, originale, ripetizioni=RIPETIZIONI
                    )
                except RecursionError:
                    risultati[(nome, famiglia, n)] = None
                    print(
                        f"{nome:<24} {famiglia:<15} n={n:<6} non misurato: "
                        "RecursionError, profondità della ricorsione lineare"
                    )
                    continue
                risultati[(nome, famiglia, n)] = sintesi_campioni(campioni)
    return risultati


def stampa_tabelle(risultati, dimensioni=DIMENSIONI):
    """Stampa le tabelle equivalenti del grafico, una riga per misura."""
    print()
    print("Metadati:", metadati_misura())
    print("Ripetizioni per cella:", RIPETIZIONI, "- unità: millisecondi per chiamata")
    for famiglia in FAMIGLIE:
        print()
        print(f"Famiglia {famiglia}")
        for n in dimensioni:
            for nome, _ in PROCEDURE:
                sintesi = risultati.get((nome, famiglia, n))
                if sintesi is None:
                    print(f"{nome:<24} {famiglia:<15} n={n:<6} non misurato")
                    continue
                print(riga_tabella(nome, famiglia, n, sintesi))


def disegna_grafico(risultati, percorso="confronto-ordinamenti-u11.png", dimensioni=DIMENSIONI):
    """Disegna il grafico a due riquadri e lo salva come PNG.

    Asse orizzontale: numero di record `n`. Asse verticale: mediana della durata
    in millisecondi. Scala lineare su entrambi gli assi: la lettura interessata è
    la **forma** delle curve - crescita lenta contro crescita rapida - e i valori
    restano nella tabella equivalente. I marcatori distinguono le serie anche
    senza il colore.
    """
    import matplotlib.pyplot as plt

    colori = {
        "insertion_sort": ("#b3402a", "o"),
        "merge_sort": ("#0e6b85", "s"),
        "quick_sort": ("#5b3e96", "^"),
        "sorted": ("#2e7d32", "D"),
    }
    figura, assi = plt.subplots(1, 2, figsize=(12, 5))
    for asse, famiglia in zip(assi, FAMIGLIE_NEL_GRAFICO):
        for nome in NEL_GRAFICO:
            xs = [n for n in dimensioni if risultati.get((nome, famiglia, n))]
            ys = [
                risultati[(nome, famiglia, n)]["mediana"] * 1000 for n in xs
            ]
            colore, marcatore = colori[nome]
            asse.plot(
                xs,
                ys,
                color=colore,
                marker=marcatore,
                linestyle="-",
                linewidth=2,
                markersize=7,
                label=nome,
            )
        asse.set_title("famiglia " + famiglia)
        asse.set_xlabel("numero di record n")
        asse.set_ylabel("mediana della durata (ms)")
        asse.grid(True, alpha=0.3)
        asse.legend()
    figura.suptitle(
        "Durata mediana di quattro procedure di ordinamento - cinque campioni per punto"
    )
    figura.tight_layout()
    figura.savefig(percorso, dpi=120)
    print()
    print("Grafico salvato in:", percorso)
    return percorso


if __name__ == "__main__":
    destinazione = sys.argv[1] if len(sys.argv) > 1 else "confronto-ordinamenti-u11.png"
    raccolti = misura_completa()
    stampa_tabelle(raccolti)
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        print("matplotlib non è installato: le tabelle sono complete lo stesso.")
    else:
        disegna_grafico(raccolti, destinazione)
