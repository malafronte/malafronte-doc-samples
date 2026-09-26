"""Riferimento formativo del LAB-PY-U9 - Il misuratore completo e spiegato.

Da leggere **dopo** la fase L3, come confronto con il proprio lavoro.
Implementa le stesse interfacce dello starter con la regione cronometrata
completa: `misura_scansione` apre e chiude il timer intorno al solo lotto di
chiamate e raccoglie un campione per ripetizione.

Protocollo del file, che il riferimento rispetta integralmente:
- la preparazione dei dati, la verifica del risultato e le stampe restano
  FUORI dalla regione cronometrata: il timer racchiude il solo lotto di
  chiamate alla funzione misurata;
- cinque ripetizioni per ogni coppia algoritmo/dimensione, con la stessa
  lista di valori per le funzioni che non la modificano;
- la sintesi usa la mediana dei cinque campioni, con minimo e massimo come
  variabilità descrittiva;
- nessun file viene aperto: i dati vivono in liste e dizionari e la tabella
  testuale viene stampata a schermo; lo studente la conserva nella scheda
  con l'editor.

Colonne della tabella, in quest'ordine: `esperimento`, `algoritmo`,
`dimensione`, `significato_dimensione`, `famiglia_input`, `stato_memoria`,
`ripetizione`, `chiamate_per_lotto`, `durata_lotto_s`,
`durata_per_chiamata_s`. I campi non pertinenti - la memoria, per le
scansioni - portano il valore «non applicabile».

I tempi raccolti sono un'esecuzione di esempio: un'altra macchina ottiene
durate e rapporti diversi conservando la correttezza del metodo. Nessun
confronto fra algoritmi si decide sull'ordinamento di pochi campioni.

Ambiente: CPython sul computer, raccolta `raccolta-programmi`, esecuzione con
`uv run python programmi/misure_u9.py` dalla root della raccolta. L'import di
questo modulo non esegue misure.
"""

import time

from analisi_u9 import riepilogo_due_scansioni, riepilogo_una_scansione

# ---------------------------------------------------------------------------
# Costanti del protocollo. Da registrare insieme ai risultati.
# ---------------------------------------------------------------------------

RIPETIZIONI = 5
CHIAMATE_PER_LOTTO = 10
DIMENSIONI = (100, 1000, 10000, 100000)

ESPERIMENTO = "scansioni equivalenti"
SIGNIFICATO_DIMENSIONE = "elementi della lista"
FAMIGLIA_INPUT = "pattern ripetuto [-2, -1, 0, 1, 2]"
STATO_MEMORIA_NON_PERTINENTE = "non applicabile"

COLONNE_TABELLA = (
    "esperimento",
    "algoritmo",
    "dimensione",
    "significato_dimensione",
    "famiglia_input",
    "stato_memoria",
    "ripetizione",
    "chiamate_per_lotto",
    "durata_lotto_s",
    "durata_per_chiamata_s",
)


# ---------------------------------------------------------------------------
# Preparazione dei dati - fuori dal timer
# ---------------------------------------------------------------------------


def costruisci_valori(n: int) -> list[int]:
    """Restituisce una lista riproducibile di n interi del laboratorio.

    Il pattern `[-2, -1, 0, 1, 2]` si ripete fino a raggiungere la lunghezza
    `n`. La costruzione avviene FUORI dal timer e la stessa lista viene
    riusata per le funzioni che non la modificano. Dominio: `n` intero non
    negativo.
    """
    pattern = [-2, -1, 0, 1, 2]
    return [pattern[indice % len(pattern)] for indice in range(n)]


# ---------------------------------------------------------------------------
# Misura - regione cronometrata completa
# ---------------------------------------------------------------------------


def misura_scansione(funzione, valori: list[int], ripetizioni: int, chiamate_per_lotto: int) -> list[float]:
    """Restituisce i campioni di durata per chiamata, in secondi.

    Riceve la `funzione` da misurare - che riceve la lista `valori` e NON la
    modifica - e due numeri: le `ripetizioni` del protocollo (cinque) e le
    `chiamate_per_lotto` di ogni ripetizione. Restituisce una lista di
    `ripetizioni` campioni: ognuno è la durata del lotto divisa per le
    chiamate del lotto, in secondi. La stessa lista `valori` viene riusata a
    ogni chiamata proprio perché la funzione non la modifica.

    Ogni campione comprende il costo del ciclo e delle chiamate Python: non
    viene sottratto alcun tempo di ciclo vuoto, che sarebbe instabile e
    potrebbe produrre durate negative. La preparazione dei dati, la verifica
    del risultato e le stampe restano fuori da questa funzione.

    Dominio: `ripetizioni` e `chiamate_per_lotto` interi maggiori o uguali a
    1; i valori fuori dominio sollevano `ValueError`.
    """
    if ripetizioni < 1:
        raise ValueError("ripetizioni deve essere almeno 1")
    if chiamate_per_lotto < 1:
        raise ValueError("chiamate_per_lotto deve essere almeno 1")

    campioni: list[float] = []
    for _ in range(ripetizioni):
        inizio = time.perf_counter()
        for _ in range(chiamate_per_lotto):
            funzione(valori)
        durata_lotto_s = time.perf_counter() - inizio
        campioni.append(durata_lotto_s / chiamate_per_lotto)
    return campioni


# ---------------------------------------------------------------------------
# Sintesi e tabella - fuori dal timer
# ---------------------------------------------------------------------------


def sintetizza_campioni(campioni: list[float]) -> dict[str, float]:
    """Restituisce la sintesi descrittiva dei campioni: mediana, minimo, massimo.

    Con i cinque campioni del laboratorio la mediana è l'elemento centrale
    dei campioni ordinati: per `campioni = [5, 1, 4, 2, 3]` gli ordinati sono
    `[1, 2, 3, 4, 5]` e la mediana vale 3. Con un numero dispari di campioni
    la mediana è il valore centrale; con un numero pari è la media dei due
    valori centrali, scelta dichiarata qui perché la funzione accetta
    lunghezze diverse da cinque. Minimo e massimo descrivono la variabilità
    dei campioni raccolti e non sono un intervallo di confidenza.

    Dominio: lista non vuota di numeri; lista vuota -> `ValueError`.
    """
    if not campioni:
        raise ValueError("campioni deve contenere almeno un valore")
    ordinati = sorted(campioni)
    # Mediana dei cinque campioni del protocollo: `sorted(campioni)[2]`,
    # cioè il valore centrale dei campioni ordinati.
    centro = len(ordinati) // 2
    if len(ordinati) % 2 == 1:
        mediana = ordinati[centro]
    else:
        mediana = (ordinati[centro - 1] + ordinati[centro]) / 2
    return {"mediana": mediana, "minimo": ordinati[0], "massimo": ordinati[-1]}


def esperimento_scansioni(
    dimensioni: tuple[int, ...] | list[int] = DIMENSIONI,
    ripetizioni: int = RIPETIZIONI,
    chiamate_per_lotto: int = CHIAMATE_PER_LOTTO,
) -> list[dict]:
    """Restituisce le righe della tabella del confronto fra i due riepiloghi.

    Per ogni dimensione e per ogni algoritmo raccoglie `ripetizioni` campioni
    con `misura_scansione` e li espande in righe con tutti i metadati del
    protocollo. La verifica del risultato - i due riepiloghi devono
    concordare sugli stessi valori - avviene PRIMA di ogni serie di misure e
    resta fuori dal timer.

    Ogni riga è un dizionario con le chiavi di `COLONNE_TABELLA`: la durata
    del lotto si ricava dal campione moltiplicando per le chiamate del lotto,
    così il dato resta rintracciabile accanto al campione. Le durate sono in
    secondi. L'ordine di misura è fisso - prima la scansione singola, poi la
    doppia - e va dichiarato: alternare l'ordine nelle ripetizioni limita un
    effetto sistematico dell'ordine senza eliminare il rumore.
    """
    righe: list[dict] = []
    for dimensione in dimensioni:
        valori = costruisci_valori(dimensione)
        # Verifica del risultato, FUORI dal timer.
        if riepilogo_una_scansione(valori) != riepilogo_due_scansioni(valori):
            raise RuntimeError(f"i due riepiloghi non concordano per n = {dimensione}")
        for nome_algoritmo, funzione in (
            ("riepilogo_una_scansione", riepilogo_una_scansione),
            ("riepilogo_due_scansioni", riepilogo_due_scansioni),
        ):
            campioni = misura_scansione(funzione, valori, ripetizioni, chiamate_per_lotto)
            for indice, campione in enumerate(campioni, start=1):
                righe.append(
                    {
                        "esperimento": ESPERIMENTO,
                        "algoritmo": nome_algoritmo,
                        "dimensione": dimensione,
                        "significato_dimensione": SIGNIFICATO_DIMENSIONE,
                        "famiglia_input": FAMIGLIA_INPUT,
                        "stato_memoria": STATO_MEMORIA_NON_PERTINENTE,
                        "ripetizione": indice,
                        "chiamate_per_lotto": chiamate_per_lotto,
                        "durata_lotto_s": campione * chiamate_per_lotto,
                        "durata_per_chiamata_s": campione,
                    }
                )
    return righe


def stampa_tabella(righe: list[dict]) -> None:
    """Stampa la tabella testuale dei campioni, nell'ordine di `COLONNE_TABELLA`.

    I numeri decimali usano il punto e la notazione compatta: le unità sono
    dichiarate dai nomi delle colonne, tutte le durate sono in secondi.
    """
    print(" | ".join(COLONNE_TABELLA))
    for riga in righe:
        campi = []
        for colonna in COLONNE_TABELLA:
            valore = riga[colonna]
            if isinstance(valore, float):
                campi.append(f"{valore:.6g}")
            else:
                campi.append(str(valore))
        print(" | ".join(campi))


def stampa_sintesi(righe: list[dict]) -> None:
    """Stampa la sintesi per algoritmo e dimensione: mediana, minimo, massimo.

    La sintesi riassume i campioni già stampati nella tabella grezza: non li
    sostituisce e non aggrega fra loro dimensioni o algoritmi diversi.
    """
    algoritmi = sorted({riga["algoritmo"] for riga in righe})
    dimensioni = sorted({riga["dimensione"] for riga in righe})
    print("algoritmo | dimensione | mediana_s | minimo_s | massimo_s")
    for algoritmo in algoritmi:
        for dimensione in dimensioni:
            campioni = [
                riga["durata_per_chiamata_s"]
                for riga in righe
                if riga["algoritmo"] == algoritmo and riga["dimensione"] == dimensione
            ]
            sintesi = sintetizza_campioni(campioni)
            print(
                f"{algoritmo} | {dimensione} | {sintesi['mediana']:.6g} | "
                f"{sintesi['minimo']:.6g} | {sintesi['massimo']:.6g}"
            )


# ---------------------------------------------------------------------------
# Avvio protetto dalla guardia
# ---------------------------------------------------------------------------


def main() -> list[dict]:
    """Esegue il confronto, stampa tabella e sintesi, restituisce i dati.

    La restituzione serve a passare i campioni al modulo `grafici_u9` senza
    trascrivere a mano i valori: il grafico si costruisce dagli stessi dati
    stampati nella tabella. I controlli di correttezza precedono ogni misura.
    """
    print("Esperimento:", ESPERIMENTO)
    print("Input:", FAMIGLIA_INPUT, "- dimensione =", SIGNIFICATO_DIMENSIONE)
    print("Ripetizioni:", RIPETIZIONI, "- chiamate per lotto:", CHIAMATE_PER_LOTTO)
    righe = esperimento_scansioni()
    print()
    stampa_tabella(righe)
    print()
    stampa_sintesi(righe)
    return righe


if __name__ == "__main__":
    main()
