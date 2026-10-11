"""Analisi del costo di riepilogo e consultazione (tappa U9).

Oggetto dello studio: `riepilogo_per_destinazione` e `cerca_preventivo` di
`spedizione_u5.py`, le implementazioni effettivamente usate dalla raccolta.
Questo script contiene le **varianti strumentate** che contano le operazioni e
la campagna di misura con `time.perf_counter`; non modifica le funzioni di
produzione.

Modello di costo dichiarato:

- dimensione `n` = numero dei record del registro;
- lunghezza `L` dei codici = 6 caratteri per tutti i dataset generati, quindi
  il costo di un confronto fra codici si considera costante;
- operazione contata per il riepilogo: la **visita** di un record (lettura
  dell'elemento e aggiornamento dei due accumulatori);
- operazione contata per la consultazione: il **confronto** fra codici, nella
  scansione con arresto;
- spazio: il riepilogo usa due record di accumulo, la ricerca nessuno spazio
  aggiuntivo; lo stack della versione iterativa resta costante.

Comandi, dalla root del progetto:

    uv run python programmi/analisi_costi_u9.py     # conteggi, misure, campioni
    uv run python programmi/grafico_costi_u9.py     # grafico dai campioni
"""
import json
import sys
import time
from pathlib import Path

from spedizione_u5 import cerca_preventivo, riepilogo_per_destinazione

# --- Generazione deterministica dei dataset ---


def genera_registro(n: int) -> list:
    """Restituisce un registro sintetico di n record, sempre uguale.

    Codici numerici a sei cifre con zeri iniziali, destinazioni alternate e
    totali in centesimi da 0 a 600. Nessuna casualità: lo stesso `n` produce
    sempre lo stesso registro.
    """
    registro = []
    for i in range(n):
        record = {
            "codice": f"{i:06d}",
            "destinazione": "locale" if i % 2 == 0 else "nazionale",
            "totale_cent": (i % 7) * 100,
        }
        registro.append(record)
    return registro


# --- Varianti strumentate (non sostituiscono le funzioni di produzione) ---


def riepilogo_per_destinazione_conteggi(registro: list) -> tuple:
    """Riepilogo strumentato: (risultato, visite, aggiornamenti).

    Una **visita** è la lettura di un record nel ciclo; un **aggiornamento**
    è la scrittura di uno dei due campi del gruppo. Il costo fisso della
    chiamata — costruzione dei due gruppi iniziali — non rientra nei due
    contatori e si dichiara separatamente.
    """
    riepilogo = {
        "locale": {"conteggio": 0, "totale_cent": 0},
        "nazionale": {"conteggio": 0, "totale_cent": 0},
    }
    visite = 0
    aggiornamenti = 0
    for record in registro:
        visite = visite + 1
        gruppo = riepilogo[record["destinazione"]]
        gruppo["conteggio"] = gruppo["conteggio"] + 1
        gruppo["totale_cent"] = gruppo["totale_cent"] + record["totale_cent"]
        aggiornamenti = aggiornamenti + 2
    return riepilogo, visite, aggiornamenti


def cerca_preventivo_conteggi(registro: list, codice: str) -> tuple:
    """Scansione con arresto strumentata: (record_o_None, confronti).

    Un **confronto** è la valutazione di `record["codice"] == codice`. La
    scansione si ferma al primo record con il codice richiesto: un assente
    costa `n` confronti, come un presente in ultima posizione.
    """
    confronti = 0
    for record in registro:
        confronti = confronti + 1
        if record["codice"] == codice:
            return record, confronti
    return None, confronti


# --- Misure con time.perf_counter ---


def misura_lotto(chiamata, chiamate_per_lotto: int) -> float:
    """Restituisce il tempo medio per chiamata, in secondi.

    La regione cronometrata contiene le sole chiamate studiate: la preparazione
    degli argomenti e la lettura del timer restano fuori.
    """
    inizio = time.perf_counter()
    for _ in range(chiamate_per_lotto):
        chiamata()
    fine = time.perf_counter()
    return (fine - inizio) / chiamate_per_lotto


def campiona(chiamata, ripetizioni: int, chiamate_per_lotto: int) -> list:
    """Restituisce i campioni del tempo medio per chiamata, uno per ripetizione."""
    campioni = []
    for _ in range(ripetizioni):
        campioni.append(misura_lotto(chiamata, chiamate_per_lotto))
    return campioni


def mediana(valori: list) -> float:
    """Restituisce l'elemento centrale dei valori ordinati.

    Con un numero pari di valori la mediana è la media dei due centrali. Non
    è un intervallo di confidenza: minimo e massimo descrivono la variabilità
    osservata.
    """
    ordinati = sorted(valori)
    lunghezza = len(ordinati)
    if lunghezza == 0:
        return 0.0
    if lunghezza % 2 == 1:
        return ordinati[lunghezza // 2]
    return (ordinati[lunghezza // 2 - 1] + ordinati[lunghezza // 2]) / 2


# --- Campagna di misura ---

DIMENSIONI = [100, 1000, 10000]
RIPETIZIONI = 5
CHIAMATE_PER_LOTTO = 20
Q_QUERY = 10


def esegui_campagna() -> dict:
    """Esegue conteggi e misure e restituisce il documento dei campioni.

    Ordine del protocollo: generazione del dataset, verifica della correttezza,
    poi misura. Generazione, stampe e grafico restano fuori dalla regione
    cronometrata; le stesse istanze di registro si usano per tutte le
    procedure confrontate.
    """
    documento = {
        "metadati": {
            "strumento": "time.perf_counter, due letture e differenza",
            "ripetizioni": RIPETIZIONI,
            "chiamate_per_lotto": CHIAMATE_PER_LOTTO,
            "q_query": Q_QUERY,
            "lunghezza_codici": 6,
            "generatore": "algoritmico deterministico, senza casualità",
            "python": sys.version.split()[0],
        },
        "campioni": [],
    }

    for n in DIMENSIONI:
        registro = genera_registro(n)
        ultimo_codice = f"{n - 1:06d}"
        codice_assente = "999999"

        # Correttezza PRIMA del timer: risultati e conteggi attesi.
        riepilogo, visite, aggiornamenti = riepilogo_per_destinazione_conteggi(registro)
        assert riepilogo == riepilogo_per_destinazione(registro)
        assert visite == n
        assert aggiornamenti == 2 * n
        record, confronti = cerca_preventivo_conteggi(registro, ultimo_codice)
        assert record == registro[n - 1]
        assert confronti == n
        record, confronti = cerca_preventivo_conteggi(registro, codice_assente)
        assert record is None
        assert confronti == n

        campioni_riepilogo = campiona(
            lambda: riepilogo_per_destinazione(registro), RIPETIZIONI, CHIAMATE_PER_LOTTO
        )
        campioni_ultima = campiona(
            lambda: cerca_preventivo(registro, ultimo_codice),
            RIPETIZIONI,
            CHIAMATE_PER_LOTTO,
        )
        campioni_assente = campiona(
            lambda: cerca_preventivo(registro, codice_assente),
            RIPETIZIONI,
            CHIAMATE_PER_LOTTO,
        )

        documento["campioni"].append(
            {
                "operazione": "riepilogo_per_destinazione",
                "n": n,
                "visite": visite,
                "aggiornamenti": aggiornamenti,
                "campioni_s": campioni_riepilogo,
                "mediana_s": mediana(campioni_riepilogo),
            }
        )
        documento["campioni"].append(
            {
                "operazione": "cerca_preventivo_ultima_posizione",
                "n": n,
                "confronti": n,
                "campioni_s": campioni_ultima,
                "mediana_s": mediana(campioni_ultima),
            }
        )
        documento["campioni"].append(
            {
                "operazione": "cerca_preventivo_assente",
                "n": n,
                "confronti": n,
                "campioni_s": campioni_assente,
                "mediana_s": mediana(campioni_assente),
            }
        )

    # Consultazioni ripetute: q query sullo stesso registro, preparazione separata.
    n = DIMENSIONI[-1]
    registro = genera_registro(n)
    codici_query = []
    for i in range(Q_QUERY):
        codici_query.append(f"{(i * 37) % n:06d}")
    totale_confronti = 0
    for codice in codici_query:
        record, confronti = cerca_preventivo_conteggi(registro, codice)
        assert record is not None
        totale_confronti = totale_confronti + confronti
    documento["sequenza_query"] = {
        "n": n,
        "q": Q_QUERY,
        "codici": codici_query,
        "confronti_totali": totale_confronti,
    }
    return documento


def main() -> None:
    """Esegue la campagna, stampa le tabelle e conserva i campioni in JSON."""
    documento = esegui_campagna()

    print("Conteggi e misure - riepilogo e consultazione del registro")
    print(f"Ripetizioni: {RIPETIZIONI}; chiamate per lotto: {CHIAMATE_PER_LOTTO}")
    print()
    print(f"{'operazione':38} {'n':>6} {'op. contate':>12} {'mediana s':>12}")
    for campione in documento["campioni"]:
        if "visite" in campione:
            operazioni = campione["visite"]
        else:
            operazioni = campione["confronti"]
        print(
            f"{campione['operazione']:38} {campione['n']:>6} {operazioni:>12} "
            f"{campione['mediana_s']:>12.9f}"
        )
    sequenza = documento["sequenza_query"]
    print()
    print(
        f"Sequenza di {sequenza['q']} query sul registro di {sequenza['n']} record: "
        f"{sequenza['confronti_totali']} confronti complessivi"
    )

    percorso = Path(__file__).resolve().parent.parent / "risultati" / "unita-09"
    percorso.mkdir(parents=True, exist_ok=True)
    file_campioni = percorso / "misure_u9.json"
    file_campioni.write_text(
        json.dumps(documento, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Campioni conservati in: {file_campioni}")


if __name__ == "__main__":
    main()
