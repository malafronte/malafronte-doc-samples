"""Starter del LAB-PY-U9 - Il grafico: serie, etichette e tabella equivalente.

Questo file è **incompleto, e lo dichiara**: la cornice di
`grafico_scansioni` controlla già le lunghezze e la directory di
destinazione, mentre il disegno delle due serie, le etichette e la legenda
sono da completare (fase L3) e lo dichiarano con un `NotImplementedError`
che nomina la fase.

Regole del grafico, da conservare anche nella versione completata:
- il grafico viene scritto su file con `fig.savefig(percorso)`: nessuna
  finestra grafica viene aperta e non serve alcuna chiusura esplicita;
- le etichette NON sono dati: titolo, etichette degli assi e nomi delle
  serie dicono che cosa le serie rappresentano e devono corrispondere al
  confronto effettivamente disegnato;
- accanto al grafico va prodotta la TABELLA EQUIVALENTE: gli stessi valori,
  leggibili senza grafica;
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

# Fase L3 - Misurare e rappresentare: completare le etichette. Titolo,
# etichette degli assi e nomi delle serie NON sono dati: dicono che cosa le
# serie rappresentano e devono corrispondere al confronto disegnato. Il
# titolo esprime l'interpretazione del confronto; le etichette degli assi
# dichiarano grandezza e unità; i nomi delle serie distinguono le due
# procedure. Prima di ogni grafico le vengono impostate sul confronto
# effettivamente disegnato: cambiarle dopo il disegno fa dire al grafico una
# cosa diversa dai valori tracciati.
ETICHETTE = {
    "titolo": "",
    "x": "",
    "y": "",
    "serie_a": "",
    "serie_b": "",
}

PERCORSO_VISITE = os.path.join("documentazione", "unita-09", "visite-modello.png")
PERCORSO_DURATE = os.path.join("documentazione", "unita-09", "confronto-scansioni.png")


# ---------------------------------------------------------------------------
# Cornice del grafico - i punti da completare sono segnalati
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

    Dominio: le tre serie hanno la stessa lunghezza; lunghezze diverse
    sollevano `ValueError`. Nessuna finestra grafica viene aperta.
    """
    if len(dimensioni) != len(tempi_a_s) or len(dimensioni) != len(tempi_b_s):
        raise ValueError("le tre serie devono avere la stessa lunghezza")
    cartella = os.path.dirname(percorso)
    if cartella and not os.path.isdir(cartella):
        return None

    fig, ax = plt.subplots()

    # Fase L3 - Misurare e rappresentare: completare i punti segnati, in
    # quest'ordine.
    #   1. due disegni delle serie con `ax.plot(dimensioni, ...)`, con
    #      marcatori e stili di linea DIVERSI e i nomi delle serie presi da
    #      `ETICHETTE`: la serie deve restare leggibile anche senza il colore;
    #   2. `ax.set_xlabel`, `ax.set_ylabel` e `ax.set_title` con le etichette
    #      di `ETICHETTE`;
    #   3. `ax.legend()`, che usa i nomi delle serie già dichiarati;
    #   4. `fig.savefig(percorso)` e il ritorno della figura, che restano
    #      FUORI da ogni misura del timer.
    raise NotImplementedError(
        "grafico_scansioni: serie, etichette e legenda da completare nella fase L3"
    )


# ---------------------------------------------------------------------------
# Dati e tabelle equivalenti - già complete
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


# ---------------------------------------------------------------------------
# Avvio protetto dalla guardia
# ---------------------------------------------------------------------------


def main() -> None:
    """Annuncia il lavoro da completare senza produrre grafici."""
    print("LAB-PY-U9 - grafici: serie, etichette e legenda di grafico_scansioni")
    print("sono da completare (fase L3). Nessun grafico è stato prodotto.")
    print("Dopo la fase L3 questo avvio chiama misure_u9.esperimento_scansioni,")
    print("disegna i due grafici e stampa le tabelle equivalenti.")


if __name__ == "__main__":
    main()
