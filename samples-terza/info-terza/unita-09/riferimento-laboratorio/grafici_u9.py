"""Riferimento formativo del LAB-PY-U9 - Il grafico completo del laboratorio.

Da leggere **dopo** la fase L3, come confronto con il proprio lavoro.
Implementa la stessa interfaccia dello starter con il disegno completo:
due serie con marcatori e stili diversi, etichette coerenti con i dati
tracciati, legenda, salvataggio su file e tabella equivalente.

Regole del grafico, rispettate integralmente:
- il grafico viene scritto su file con `fig.savefig(percorso)`: nessuna
  finestra grafica viene aperta e non serve alcuna chiusura esplicita;
- le etichette NON sono dati: titolo, etichette degli assi e nomi delle
  serie dicono che cosa le serie rappresentano e devono corrispondere al
  confronto effettivamente disegnato. Il programma le imposta PRIMA di ogni
  grafico: la stessa cornice disegna le serie esatte del modello e le durate
  misurate, che hanno unità diverse;
- accanto al grafico viene prodotta la TABELLA EQUIVALENTE: gli stessi
  valori, leggibili senza grafica;
- se la directory del percorso non esiste, la funzione non scrive nulla, non
  solleva eccezioni non spiegate e restituisce `None`; il messaggio chiaro da
  annunciare si ottiene con `messaggio_directory_mancante`. La directory si
  crea nell'editor o dal file system, prima di rieseguire.

Ambiente: CPython sul computer, raccolta `raccolta-programmi`, esecuzione con
`uv run python programmi/grafici_u9.py` dalla root della raccolta. L'import
di questo modulo non produce grafici.
"""

import os

import matplotlib.pyplot as plt

from misure_u9 import esperimento_scansioni, sintetizza_campioni

# ---------------------------------------------------------------------------
# Etichette del grafico - interpretazione del confronto scelto
# ---------------------------------------------------------------------------

# Titolo, etichette degli assi e nomi delle serie NON sono dati: dicono che
# cosa le serie rappresentano e devono corrispondere al confronto disegnato.
# I valori qui sotto descrivono il primo grafico del laboratorio, quello delle
# serie esatte del modello (le visite n e 2n). Prima di disegnare le durate
# misurate il programma adatta il titolo e l'etichetta dell'asse y: la stessa
# cornice serve a confronti con unità diverse e un'etichetta incoerente fa
# dire al grafico una cosa diversa dai valori tracciati.
ETICHETTE = {
    "titolo": "Visite agli elementi per due procedure di scansione",
    "x": "Numero di elementi n",
    "y": "Visite agli elementi",
    "serie_a": "una scansione",
    "serie_b": "due scansioni",
}

PERCORSO_VISITE = os.path.join("documentazione", "unita-09", "visite-modello.png")
PERCORSO_DURATE = os.path.join("documentazione", "unita-09", "confronto-scansioni.png")


# ---------------------------------------------------------------------------
# Grafico completo
# ---------------------------------------------------------------------------


def messaggio_directory_mancante(percorso: str) -> str:
    """Restituisce il messaggio chiaro da annunciare quando la directory manca.

    La funzione di disegno non scrive nulla e non solleva eccezioni quando la
    directory del `percorso` non esiste: chiama questo costruttore di
    messaggi e lo annuncia. La directory si crea nell'editor o dal file
    system, poi l'esecuzione si ripete.
    """
    cartella = os.path.dirname(percorso) or "la directory di lavoro"
    return (
        f"La directory {cartella} non esiste: crearla nell'editor o dal file "
        "system, poi rieseguire il programma."
    )


def grafico_scansioni(dimensioni, tempi_a_s, tempi_b_s, percorso):
    """Disegna e salva il confronto fra due serie al variare della dimensione.

    Riceve le `dimensioni` comuni e le due serie di valori delle due
    procedure - nel laboratorio: durate per chiamata in secondi, oppure
    conteggi esatti del modello - e il `percorso` del file da scrivere.
    Restituisce la figura costruita, per consentire i controlli su titolo,
    etichette e serie; restituisce `None` senza sollevare eccezioni quando la
    directory del `percorso` non esiste.

    Le due serie usano marcatori e stili di linea diversi: la distinzione
    resta leggibile anche senza il colore. Le etichette arrivano da
    `ETICHETTE`, che il chiamante imposta sul confronto effettivamente
    disegnato.

    Dominio: le tre serie hanno la stessa lunghezza; lunghezze diverse
    sollevano `ValueError`. Nessuna finestra grafica viene aperta: il file
    viene scritto e la figura restituita al chiamante.
    """
    if len(dimensioni) != len(tempi_a_s) or len(dimensioni) != len(tempi_b_s):
        raise ValueError("le tre serie devono avere la stessa lunghezza")
    cartella = os.path.dirname(percorso)
    if cartella and not os.path.isdir(cartella):
        return None

    fig, ax = plt.subplots()
    ax.plot(
        dimensioni, tempi_a_s, marker="o", linestyle="-", label=ETICHETTE["serie_a"]
    )
    ax.plot(
        dimensioni, tempi_b_s, marker="s", linestyle="--", label=ETICHETTE["serie_b"]
    )
    ax.set_xlabel(ETICHETTE["x"])
    ax.set_ylabel(ETICHETTE["y"])
    ax.set_title(ETICHETTE["titolo"])
    ax.legend()
    fig.savefig(percorso)
    return fig


# ---------------------------------------------------------------------------
# Dati e tabelle equivalenti
# ---------------------------------------------------------------------------


def dati_visite_esatte() -> tuple[list[int], list[int], list[int]]:
    """Restituisce `(dimensioni, visite_una, visite_due)` del modello di costo.

    Serie ESATTE del capitolo: per n = 2, 4, 8, 16 una scansione visita gli
    elementi n volte e due scansioni ne visitano 2n. Non sono misure di tempo
    e non vanno confuse con le durate raccolte dal misuratore: servono a
    verificare il grafico e la tabella su valori senza rumore.
    """
    dimensioni = [2, 4, 8, 16]
    visite_una = [n for n in dimensioni]
    visite_due = [2 * n for n in dimensioni]
    return dimensioni, visite_una, visite_due


def tabella_equivalente(dimensioni, tempi_a_s, tempi_b_s) -> list[dict]:
    """Restituisce le righe di tabella che esprimono gli stessi dati del grafico.

    Ogni riga associa la dimensione al valore della prima e della seconda
    serie. Il grafico e la tabella devono dire la stessa cosa: la tabella
    resta leggibile senza grafica ed è l'oggetto della verifica.
    """
    righe = []
    for posizione in range(len(dimensioni)):
        righe.append(
            {
                "dimensione": dimensioni[posizione],
                "serie_a": tempi_a_s[posizione],
                "serie_b": tempi_b_s[posizione],
            }
        )
    return righe


def serie_mediane(righe: list[dict], algoritmo: str, dimensioni) -> list[float]:
    """Restituisce la mediana dei campioni di `algoritmo` per ogni dimensione.

    Le righe arrivano da `misure_u9.esperimento_scansioni`: per ogni
    dimensione raccoglie i campioni dell'algoritmo indicato e ne restituisce
    la mediana. Il grafico delle durate rappresenta così la sintesi dei
    campioni, mentre i campioni grezzi restano nella tabella.
    """
    mediane = []
    for dimensione in dimensioni:
        campioni = [
            riga["durata_per_chiamata_s"]
            for riga in righe
            if riga["algoritmo"] == algoritmo and riga["dimensione"] == dimensione
        ]
        mediane.append(sintetizza_campioni(campioni)["mediana"])
    return mediane


def stampa_tabella_equivalente(righe: list[dict]) -> None:
    """Stampa la tabella equivalente al grafico, riga per riga."""
    print("dimensione | serie_a | serie_b")
    for riga in righe:
        print(f"{riga['dimensione']} | {riga['serie_a']} | {riga['serie_b']}")


# ---------------------------------------------------------------------------
# Avvio protetto dalla guardia
# ---------------------------------------------------------------------------


def main(
    percorso_visite: str = PERCORSO_VISITE,
    percorso_durate: str = PERCORSO_DURATE,
) -> None:
    """Produce i due grafici del laboratorio con le loro tabelle equivalenti.

    Prima il grafico delle serie esatte del modello, poi quello delle durate
    medie misurate dal modulo `misure_u9`: i due confronti hanno unità diverse
    e le etichette vengono adattate prima di ciascun disegno.
    """
    # Primo grafico: le serie esatte del modello, n e 2n visite.
    dimensioni, visite_una, visite_due = dati_visite_esatte()
    fig = grafico_scansioni(dimensioni, visite_una, visite_due, percorso_visite)
    if fig is None:
        print(messaggio_directory_mancante(percorso_visite))
        return
    print("Grafico scritto:", percorso_visite)
    stampa_tabella_equivalente(tabella_equivalente(dimensioni, visite_una, visite_due))

    # Secondo grafico: le durate per chiamata misurate sulle due procedure.
    # Le etichette descrivono le serie effettivamente disegnate: l'unità del
    # secondo confronto è il secondo, non la visita.
    ETICHETTE["titolo"] = "Durata per chiamata delle due procedure di scansione"
    ETICHETTE["y"] = "Durata per chiamata (s)"
    righe = esperimento_scansioni()
    dimensioni = sorted({riga["dimensione"] for riga in righe})
    mediane_una = serie_mediane(righe, "riepilogo_una_scansione", dimensioni)
    mediane_due = serie_mediane(righe, "riepilogo_due_scansioni", dimensioni)
    fig = grafico_scansioni(dimensioni, mediane_una, mediane_due, percorso_durate)
    if fig is None:
        print(messaggio_directory_mancante(percorso_durate))
        return
    print("Grafico scritto:", percorso_durate)
    print("Mediane in secondi per chiamata:")
    stampa_tabella_equivalente(tabella_equivalente(dimensioni, mediane_una, mediane_due))


if __name__ == "__main__":
    main()
