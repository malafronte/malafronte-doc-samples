"""Grafico a barre delle frequenze con matplotlib.

Applicazione della libreria `matplotlib` dell'Unità 12: i **dati** sono già
calcolati e separati dal **grafico**, che si limita a disegnarli e a salvare
un'immagine PNG su un percorso dichiarato. La stessa funzione accetta
qualunque dizionario `parola -> conteggio`, come quello prodotto
dall'analizzatore del [cap. PY-19](/info-terza/corso/python/moduli-persistenza-errori/19-percorsi-file-testo/).

Contratti:

- `ordina_per_grafico(frequenze)` → lista **nuova** di coppie `(parola,
  conteggio)`; conteggio decrescente, parola crescente a parità - la stessa
  chiave a due livelli del [cap. PY-19](/info-terza/corso/python/moduli-persistenza-errori/19-percorsi-file-testo/#g-il-problema-svolto-analizzare-un-file-di-testo).
- `tabella_equivalente(righe)` → righe di testo della tabella che accompagna
  il grafico: il risultato è leggibile anche senza il PNG.
- `costruisci_grafico(frequenze, percorso_png, titolo=..., massimo_y=None)` →
  salva il PNG e restituisce il percorso; nessuna finestra interattiva viene
  aperta. `massimo_y`, se fornito, è un intero positivo che contiene tutte
  le barre e permette di confrontare grafici con la stessa scala verticale.

Il backend `Agg` viene selezionato **prima** di importare `pyplot`: è il
backend senza finestra, che rende `savefig` eseguibile anche su una macchina
senza display interattivo. Le barre hanno etichette, titolo e assi con unità
dichiarata: un grafico senza unità non comunica il dominio dei dati.

Ambiente: CPython nel progetto `applicazioni-librerie` con `matplotlib`
installato in modo esplicito; nessuna installazione globale.
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def ordina_per_grafico(frequenze):
    """Restituisce le coppie ordinate per il grafico, senza mutare l'ingresso."""
    return sorted(frequenze.items(), key=lambda coppia: (-coppia[1], coppia[0]))


def tabella_equivalente(righe):
    """Restituisce le righe di testo della tabella equivalente al grafico."""
    testo = ["parola | conteggio", "-------|---------"]
    for parola, conteggio in righe:
        testo.append(f"{parola} | {conteggio}")
    return testo


def costruisci_grafico(
    frequenze, percorso_png, titolo="Frequenza delle parole", massimo_y=None
):
    """Disegna le barre delle frequenze e salva il PNG sul percorso dichiarato.

    Le barre sono ordinate con `ordina_per_grafico`; l'asse orizzontale porta
    le parole, l'asse verticale il numero di occorrenze. Il percorso di output
    è esplicito: il file non viene mai scritto in una posizione implicita.
    I dati sono conteggi interi non negativi di parole già normalizzate:
    la funzione non legge il testo e non applica `casefold`.
    """
    righe = ordina_per_grafico(frequenze)
    parole = [parola for parola, _ in righe]
    conteggi = [conteggio for _, conteggio in righe]

    maggiore = max(conteggi, default=0)
    if massimo_y is None:
        massimo_y = maggiore + 1
    if isinstance(massimo_y, bool) or not isinstance(massimo_y, int):
        raise TypeError("massimo_y: atteso un intero")
    if massimo_y <= 0 or massimo_y < maggiore:
        raise ValueError("massimo_y: deve essere positivo e contenere tutte le barre")

    figura, assi = plt.subplots(figsize=(8, 4.5))
    barre = assi.bar(parole, conteggi, color="#0e6b85", width=0.6)
    assi.bar_label(barre, padding=6, fontsize=14)
    assi.set_title(titolo, fontsize=16, fontweight="bold", pad=16)
    assi.set_xlabel("Parola", fontsize=13, labelpad=10)
    assi.set_ylabel("Numero di occorrenze", fontsize=13, labelpad=10)
    assi.set_ylim(0, massimo_y)
    # I conteggi sono interi: non si etichetta l'asse con mezze occorrenze.
    assi.yaxis.set_major_locator(MaxNLocator(integer=True))
    assi.tick_params(labelsize=12)
    assi.set_axisbelow(True)
    assi.grid(axis="y", color="#d6e0e7", linewidth=0.8)
    assi.spines["top"].set_visible(False)
    assi.spines["right"].set_visible(False)
    figura.tight_layout()
    try:
        figura.savefig(percorso_png, dpi=160)
    finally:
        plt.close(figura)
    return percorso_png


if __name__ == "__main__":
    # Dimostrazione sotto guardia: dataset già in memoria, nessuna lettura
    # da file, PNG salvato su un percorso dichiarato accanto al sorgente.
    from pathlib import Path

    FREQUENZE_CANONICHE = {"sole": 3, "luna": 2, "mare": 1}
    # sole è inserito prima di luna: il pareggio verifica il secondo criterio.
    FREQUENZE_CON_PAREGGIO = {"sole": 2, "luna": 2, "mare": 1}

    uscita = Path(__file__).with_name("output")
    uscita.mkdir(exist_ok=True)

    for nome, titolo, frequenze in (
        ("frequenze-canoniche.png", "A. Frequenze diverse", FREQUENZE_CANONICHE),
        ("frequenze-pareggio.png", "B. Parità: parola crescente", FREQUENZE_CON_PAREGGIO),
    ):
        # Stessa scala 0-4 per rendere confrontabili le altezze dei due PNG.
        percorso = costruisci_grafico(frequenze, uscita / nome, titolo, massimo_y=4)
        print(f"grafico salvato in {percorso}")
        print(f"tabella equivalente - {titolo}:")
        for riga in tabella_equivalente(ordina_per_grafico(frequenze)):
            print(" ", riga)
