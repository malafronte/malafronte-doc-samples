"""Confronto sperimentale e grafico delle prestazioni degli ordinamenti (U11).

Il modulo misura le procedure di ordinamento sulle cinque famiglie di input di
`misure_u11.py` e produce tre oggetti:

1. **tabelle testuali** su stdout, con mediana, minimo e massimo di cinque
   campioni per ogni tripletta procedimento/famiglia/dimensione: sono la tabella
   equivalente del grafico e la base di ogni conclusione;
2. **la tabella dei tempi relativi**, che divide ogni mediana per quella di
   `sorted` sulla stessa famiglia e dimensione: è un'unità di misura meno
   dipendente dalla macchina dei tempi assoluti;
3. **due grafici PNG** - tempi assoluti e tempi relativi a `sorted` - ciascuno
   con due riquadri, per la famiglia `pseudo_casuale` e per la famiglia
   `ordinato`, e con **tutte e sette** le procedure confrontate, distinte da
   colore e da marcatore;
4. **un file JSON** con le medesime misure grezze, così che tabelle e grafici si
   possano ridisegnare senza ripetere la cronometratura.

Entrambi i grafici usano una scala **logaritmica** sull'asse verticale: le durate
coprono più di quattro ordini di grandezza e su scala lineare le curve più basse
schiaccierebbero sull'asse, diventando invisibili. Sulla scala logaritmica ogni
passo verticale uguale corrisponde allo **stesso fattore** moltiplicativo: due
curve parallele crescono con lo stesso ordine, quella più ripida cresce più in
fretta.

Le durate appartengono a chi esegue: la **forma** delle tabelle e dei grafici è
riproducibile, i valori no. Il grafico non sostituisce la tabella: ogni
affermazione della relazione si appoggia ai numeri, il grafico li rende
leggibili.

Ambiente: CPython sul computer, sola libreria standard per le misure;
`matplotlib` è richiesto **solo** per disegnare, e si installa in un progetto
locale con `uv add matplotlib` oppure, per una sola esecuzione, con
`uv run --with matplotlib python esempi/grafico_u11.py`.

Esecuzione dalla cartella `unita-11/`:

    uv run python esempi/grafico_u11.py                    # solo tabelle
    uv run --with matplotlib python esempi/grafico_u11.py  # tabelle e grafici
    uv run --with matplotlib python esempi/grafico_u11.py --da-json misure.json

L'ultima forma salta la misura e ridisegna tabelle e grafici dai dati già
raccolti nel file JSON.

I due file PNG vengono scritti nella cartella indicata come primo argomento
della riga di comando, oppure nella cartella corrente, con i nomi
`confronto-ordinamenti-u11.png` e `tempi-relativi-u11.png`; accanto a essi viene
scritto `misure-u11.json` con le misure grezze.
"""

import os
import platform
import sys

from merge_quick_u11 import merge_sort, quick_sort
from misure_u11 import (
    FAMIGLIE,
    genera_famiglia,
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

# Tutte le procedure rappresentate nei grafici, nell'ordine della legenda.
NEL_GRAFICO = (
    "insertion_sort",
    "selection_sort",
    "bubble_sort",
    "bubble_sort_ottimizzato",
    "merge_sort",
    "quick_sort",
    "sorted",
)

DIMENSIONI = (100, 200, 400, 800)
RIPETIZIONI = 5
FAMIGLIE_NEL_GRAFICO = ("pseudo_casuale", "ordinato")


def metadati_hardware():
    """Restituisce le informazioni sull'ambiente che influenzano le durate.

    Processore e numero di core fanno parte del risultato: le durate assolute
    cambiano da macchina a macchina, mentre i **rapporti** fra procedure sono più
    stabili. La quantità di memoria non è rilevabile senza dipendenze esterne e
    la dichiara chi esegue la prova.
    """
    return {
        "timer": "time.perf_counter",
        "unita": "millisecondi per chiamata",
        "python": platform.python_version(),
        "processore": platform.processor() or "non rilevato",
        "core": os.cpu_count(),
        "piattaforma": platform.platform(),
    }


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


def tempi_relativi(risultati, riferimento="sorted", dimensioni=DIMENSIONI):
    """Restituisce `{(procedimento, famiglia, n): rapporto}` rispetto al riferimento.

    Il rapporto è `mediana(procedimento) / mediana(riferimento)` sulla stessa
    famiglia e sulla stessa dimensione: un'unità di misura **adimensionale**,
    più trasferibile della durata assoluta, perché parte delle costanti
    dell'ambiente si semplifica.
    """
    relativi = {}
    for famiglia in FAMIGLIE:
        for n in dimensioni:
            base = risultati.get((riferimento, famiglia, n))
            if not base:
                continue
            for nome, _ in PROCEDURE:
                sintesi = risultati.get((nome, famiglia, n))
                if sintesi:
                    relativi[(nome, famiglia, n)] = (
                        sintesi["mediana"] / base["mediana"]
                    )
    return relativi


def stampa_tabelle(risultati, dimensioni=DIMENSIONI):
    """Stampa le tabelle equivalenti dei grafici: assoluti e relativi a `sorted`."""
    print()
    print("Metadati:", metadati_hardware())
    print("Ripetizioni per cella:", RIPETIZIONI)
    for famiglia in FAMIGLIE:
        print()
        print(f"Famiglia {famiglia} - durate medie in millisecondi")
        for n in dimensioni:
            for nome, _ in PROCEDURE:
                sintesi = risultati.get((nome, famiglia, n))
                if sintesi is None:
                    print(f"{nome:<24} {famiglia:<15} n={n:<6} non misurato")
                    continue
                print(riga_tabella(nome, famiglia, n, sintesi))

    relativi = tempi_relativi(risultati, dimensioni=dimensioni)
    for famiglia in FAMIGLIE:
        print()
        print(f"Famiglia {famiglia} - tempi relativi a `sorted` (mediana / mediana di sorted)")
        for n in dimensioni:
            righe = []
            for nome, _ in PROCEDURE:
                rapporto = relativi.get((nome, famiglia, n))
                if rapporto is None:
                    righe.append(f"{nome}=non misurato")
                else:
                    righe.append(f"{nome}={rapporto:.1f}x")
            print(f"n={n:<6} " + "  ".join(righe))


def _disegna_pannello(asse, famiglia, valori_per_procedura, ylabel, titolo):
    """Disegna un riquadro con scala logaritmica verticale e marcatori distinti."""
    colori = {
        "insertion_sort": ("#b3402a", "o"),
        "selection_sort": ("#d97706", "v"),
        "bubble_sort": ("#a21caf", "s"),
        "bubble_sort_ottimizzato": ("#c2185b", "^"),
        "merge_sort": ("#0e6b85", "D"),
        "quick_sort": ("#5b3e96", "x"),
        "sorted": ("#2e7d32", "P"),
    }
    for nome, xs, ys in valori_per_procedura:
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
    asse.set_title(titolo)
    asse.set_xlabel("numero di record n")
    asse.set_ylabel(ylabel)
    asse.set_yscale("log")
    asse.grid(True, alpha=0.3, which="both")
    asse.legend()


def disegna_grafico(risultati, percorso, dimensioni=DIMENSIONI):
    """Disegna i tempi assoluti in millisecondi e salva il PNG."""
    import matplotlib.pyplot as plt

    figura, assi = plt.subplots(1, 2, figsize=(12, 5))
    for asse, famiglia in zip(assi, FAMIGLIE_NEL_GRAFICO):
        serie = []
        for nome in NEL_GRAFICO:
            xs = [n for n in dimensioni if risultati.get((nome, famiglia, n))]
            ys = [risultati[(nome, famiglia, n)]["mediana"] * 1000 for n in xs]
            serie.append((nome, xs, ys))
        _disegna_pannello(
            asse, famiglia, serie, "mediana della durata (ms, scala log)", "famiglia " + famiglia
        )
    figura.suptitle(
        "Durata mediana di quattro procedure di ordinamento - cinque campioni per punto"
    )
    figura.tight_layout()
    figura.savefig(percorso, dpi=120)
    print()
    print("Grafico dei tempi assoluti salvato in:", percorso)
    return percorso


def disegna_grafico_relativo(risultati, percorso, dimensioni=DIMENSIONI):
    """Disegna i tempi relativi a `sorted` e salva il PNG."""
    import matplotlib.pyplot as plt

    relativi = tempi_relativi(risultati, dimensioni=dimensioni)
    figura, assi = plt.subplots(1, 2, figsize=(12, 5))
    for asse, famiglia in zip(assi, FAMIGLIE_NEL_GRAFICO):
        serie = []
        for nome in NEL_GRAFICO:
            xs = [n for n in dimensioni if relativi.get((nome, famiglia, n))]
            ys = [relativi[(nome, famiglia, n)] for n in xs]
            serie.append((nome, xs, ys))
        _disegna_pannello(
            asse,
            famiglia,
            serie,
            "tempo relativo a `sorted` (rapporto, scala log)",
            "famiglia " + famiglia,
        )
    figura.suptitle(
        "Quanto ogni procedimento è più lento di `sorted` - stesso ambiente, stessi dati"
    )
    figura.tight_layout()
    figura.savefig(percorso, dpi=120)
    print("Grafico dei tempi relativi salvato in:", percorso)
    return percorso


def salva_json(risultati, percorso):
    """Scrive le misure grezze in JSON, una riga per procedimento/famiglia/dimensione.

    Il file conserva mediana, minimo, massimo e campioni di ogni cella, più i
    metadati dell'ambiente: è il documento dei dati su cui tabelle e grafici
    sono disegnati, e permette di ridisegnarli senza ripetere la misura.
    """
    import json

    righe = []
    for (nome, famiglia, n), sintesi in sorted(risultati.items()):
        righe.append(
            {
                "procedimento": nome,
                "famiglia": famiglia,
                "n": n,
                "sintesi": sintesi,
            }
        )
    documento = {
        "metadati": metadati_hardware(),
        "ripetizioni": RIPETIZIONI,
        "misure": righe,
    }
    with open(percorso, "w", encoding="utf-8") as file:
        json.dump(documento, file, indent=2, ensure_ascii=False)
    print("Misure grezze salvate in:", percorso)


def carica_json(percorso):
    """Ricostruisce il dizionario delle misure da un file prodotto da `salva_json`."""
    import json

    with open(percorso, encoding="utf-8") as file:
        documento = json.load(file)
    risultati = {}
    for riga in documento["misure"]:
        risultati[(riga["procedimento"], riga["famiglia"], riga["n"])] = riga["sintesi"]
    return risultati


if __name__ == "__main__":
    import os.path as _percorso

    argomenti = sys.argv[1:]
    sorgente = None
    if "--da-json" in argomenti:
        posizione = argomenti.index("--da-json")
        sorgente = argomenti[posizione + 1]
        del argomenti[posizione : posizione + 2]
    cartella = argomenti[0] if argomenti else "."

    if sorgente is not None:
        raccolti = carica_json(sorgente)
        print("Misure lette da:", sorgente)
    else:
        raccolti = misura_completa()
    stampa_tabelle(raccolti)
    if sorgente is None:
        salva_json(raccolti, _percorso.join(cartella, "misure-u11.json"))
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        print("matplotlib non è installato: le tabelle sono complete lo stesso.")
    else:
        disegna_grafico(
            raccolti, _percorso.join(cartella, "confronto-ordinamenti-u11.png")
        )
        disegna_grafico_relativo(
            raccolti, _percorso.join(cartella, "tempi-relativi-u11.png")
        )
