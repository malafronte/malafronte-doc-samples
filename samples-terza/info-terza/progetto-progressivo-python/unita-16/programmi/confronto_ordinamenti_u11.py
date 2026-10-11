"""Confronto fra strategie di ordinamento sullo stesso criterio (tappa U11).

Confronto: ordinamento per inserimento (U10) contro MergeSort stabile, con
`sorted` come riferimento concreto di CPython e oracolo per il risultato.
Criterio comune: `totale_cent` crescente, con parità gestita dalla stabilità.

Le famiglie di input e il seme seguono il protocollo del laboratorio U10:
`ordinato`, `inverso`, `quasi_ordinato`, `molti_duplicati`, `pseudo_casuale`,
costruite con `random.Random(seme)` dove serve il pseudo-caso. Ogni
procedimento riceve una **copia indipendente** dello stesso originale.

Comando, dalla root del progetto:

    uv run python programmi/confronto_ordinamenti_u11.py
"""
import json
import random
import sys
import time
from pathlib import Path

from spedizione_u5 import (
    chiave_totale,
    crea_registro,
    ordina_fusione,
    ordina_inserimento,
    primo_indice_per_totale,
    vista_per_totale,
)

FAMIGLIE = ("ordinato", "inverso", "quasi_ordinato", "molti_duplicati", "pseudo_casuale")
SEME = 20261003
DIMENSIONI = [200, 1000, 5000]
RIPETIZIONI = 5
CHIAMATE_PER_LOTTO = 5
Q_QUERY = 10


def genera_totali(nome: str, n: int, seme: int = SEME) -> list:
    """Restituisce `n` totali in centesimi della famiglia `nome`.

    | `nome` | Costruzione |
    |---|---|
    | `ordinato` | `list(range(n))`, già crescente |
    | `inverso` | `list(range(n, 0, -1))`, strettamente decrescente |
    | `quasi_ordinato` | `list(range(n))` con due scambi dichiarati: posizioni `(0, 1)` e `(n // 2, n // 2 + 1)` |
    | `molti_duplicati` | `n` valori da `random.Random(seme).randrange(3)`, quindi solo 0, 1 e 2 |
    | `pseudo_casuale` | `n` valori da `random.Random(seme).randrange(n + 1)`, con seme esplicito |

    Il seme è parte del protocollo: a parità di nome, `n` e seme la lista è
    sempre la stessa. Ogni chiamata restituisce una lista nuova.
    """
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
    casuale = random.Random(seme)
    if nome == "molti_duplicati":
        return [casuale.randrange(3) for _ in range(n)]
    return [casuale.randrange(n + 1) for _ in range(n)]


def genera_registro_famiglia(nome: str, n: int) -> list:
    """Restituisce un registro di n record con i totali della famiglia `nome`."""
    totali = genera_totali(nome, n)
    codici = []
    preventivi = []
    for i in range(n):
        codici.append(f"{i:06d}")
        destinazione = "locale" if i % 2 == 0 else "nazionale"
        preventivi.append((destinazione, totali[i]))
    return crea_registro(codici, preventivi)


def misura_lotto(chiamata, chiamate_per_lotto: int) -> float:
    """Tempo medio per chiamata in secondi, con sola regione cronometrata."""
    inizio = time.perf_counter()
    for _ in range(chiamate_per_lotto):
        chiamata()
    fine = time.perf_counter()
    return (fine - inizio) / chiamate_per_lotto


def campiona(chiamata, ripetizioni: int, chiamate_per_lotto: int) -> list:
    """Campioni del tempo medio per chiamata, uno per ripetizione."""
    return [misura_lotto(chiamata, chiamate_per_lotto) for _ in range(ripetizioni)]


def mediana(valori: list) -> float:
    """Elemento centrale dei valori ordinati; con pari elementi, media dei due."""
    ordinati = sorted(valori)
    lunghezza = len(ordinati)
    if lunghezza == 0:
        return 0.0
    if lunghezza % 2 == 1:
        return ordinati[lunghezza // 2]
    return (ordinati[lunghezza // 2 - 1] + ordinati[lunghezza // 2]) / 2


def esegui_confronto() -> dict:
    """Esegue il confronto e restituisce il documento con i campioni.

    Ordine del protocollo: generazione, copie indipendenti per ogni
    procedimento, verifica di correttezza e parità, poi misura. La
    preparazione dell'ordine è separata dal costo delle query.
    """
    documento = {
        "metadati": {
            "strumento": "time.perf_counter, due letture e differenza",
            "seme": SEME,
            "famiglie": list(FAMIGLIE),
            "dimensioni": DIMENSIONI,
            "ripetizioni": RIPETIZIONI,
            "chiamate_per_lotto": CHIAMATE_PER_LOTTO,
            "q_query": Q_QUERY,
            "criterio": "totale_cent crescente",
            "python": sys.version.split()[0],
        },
        "ordinamenti": [],
        "query": [],
    }

    for nome in FAMIGLIE:
        for n in DIMENSIONI:
            originale = genera_registro_famiglia(nome, n)

            # Copie indipendenti dello stesso originale per i tre procedimenti.
            risultato_inserimento = ordina_inserimento(originale, chiave_totale)
            risultato_fusione = ordina_fusione(originale, chiave_totale)
            risultato_sorted = sorted(originale, key=chiave_totale)

            # Correttezza e parità PRIMA del timer.
            assert len(risultato_inserimento) == n
            assert len(risultato_fusione) == n
            assert stesso_multinsieme(originale, risultato_inserimento)
            assert stesso_multinsieme(originale, risultato_fusione)
            assert codici_dei_record(risultato_inserimento) == codici_dei_record(
                risultato_fusione
            )
            assert codici_dei_record(risultato_fusione) == codici_dei_record(
                risultato_sorted
            )
            assert len(originale) == n

            for etichetta, procedimento in (
                ("inserimento", lambda: ordina_inserimento(originale, chiave_totale)),
                ("fusione", lambda: ordina_fusione(originale, chiave_totale)),
                ("sorted", lambda: sorted(originale, key=chiave_totale)),
            ):
                campioni = campiona(procedimento, RIPETIZIONI, CHIAMATE_PER_LOTTO)
                documento["ordinamenti"].append(
                    {
                        "famiglia": nome,
                        "n": n,
                        "procedimento": etichetta,
                        "campioni_s": campioni,
                        "mediana_s": mediana(campioni),
                    }
                )

            # Query sul catalogo ordinato: preparazione separata dal costo.
            vista = vista_per_totale(originale)
            totali_query = []
            for i in range(Q_QUERY):
                totali_query.append((i * max(1, n // Q_QUERY)) % (n + 1))
            preparazione = misura_lotto(
                lambda: vista_per_totale(originale), 1
            )
            campioni_query = campiona(
                lambda: esegui_sequenza_query(vista, totali_query),
                RIPETIZIONI,
                1,
            )
            documento["query"].append(
                {
                    "famiglia": nome,
                    "n": n,
                    "q": Q_QUERY,
                    "preparazione_s": preparazione,
                    "campioni_s": campioni_query,
                    "mediana_s": mediana(campioni_query),
                }
            )

    return documento


def esegui_sequenza_query(vista: list, totali_query: list) -> int:
    """Esegue q consultazioni sul primo indice e restituisce il numero di indici trovati."""
    trovati = 0
    for totale_cent in totali_query:
        if primo_indice_per_totale(vista, totale_cent) is not None:
            trovati = trovati + 1
    return trovati


def stesso_multinsieme(originale: list, ordinato: list) -> bool:
    """True se le due liste contengono gli stessi record, per totali e codici."""
    chiavi_originali = []
    for record in originale:
        chiavi_originali.append((record["codice"], record["totale_cent"]))
    chiavi_ordinate = []
    for record in ordinato:
        chiavi_ordinate.append((record["codice"], record["totale_cent"]))
    return sorted(chiavi_originali) == sorted(chiavi_ordinate)


def codici_dei_record(record_list: list) -> list:
    """Codici dei record nell'ordine ricevuto: i marcatori della stabilità."""
    codici = []
    for record in record_list:
        codici.append(record["codice"])
    return codici


def main() -> None:
    """Esegue il confronto, stampa le tabelle e conserva i campioni in JSON."""
    documento = esegui_confronto()

    print("Confronto fra strategie di ordinamento sul criterio totale_cent")
    print(f"Famiglie: {', '.join(FAMIGLIE)}; seme {SEME}")
    print()
    print(f"{'famiglia':16} {'n':>6} {'procedimento':14} {'mediana s':>12}")
    for campione in documento["ordinamenti"]:
        print(
            f"{campione['famiglia']:16} {campione['n']:>6} "
            f"{campione['procedimento']:14} {campione['mediana_s']:>12.6f}"
        )
    print()
    print(f"{'famiglia':16} {'n':>6} {'preparazione s':>16} {'q query s':>12}")
    for campione in documento["query"]:
        print(
            f"{campione['famiglia']:16} {campione['n']:>6} "
            f"{campione['preparazione_s']:>16.6f} {campione['mediana_s']:>12.6f}"
        )

    percorso = Path(__file__).resolve().parent.parent / "risultati" / "unita-11"
    percorso.mkdir(parents=True, exist_ok=True)
    file_campioni = percorso / "misure_u11.json"
    file_campioni.write_text(
        json.dumps(documento, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Campioni conservati in: {file_campioni}")


if __name__ == "__main__":
    main()
