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
- `costruisci_grafico(frequenze, percorso_png, titolo=...)` → salva il PNG e
  restituisce il percorso; nessuna finestra interattiva viene aperta.

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


def ordina_per_grafico(frequenze):
    """Restituisce le coppie ordinate per il grafico, senza mutare l'ingresso."""
    return sorted(frequenze.items(), key=lambda coppia: (-coppia[1], coppia[0]))


def tabella_equivalente(righe):
    """Restituisce le righe di testo della tabella equivalente al grafico."""
    testo = ["parola | conteggio", "-------|---------"]
    for parola, conteggio in righe:
        testo.append(f"{parola} | {conteggio}")
    return testo


def costruisci_grafico(frequenze, percorso_png, titolo="Frequenza delle parole"):
    """Disegna le barre delle frequenze e salva il PNG sul percorso dichiarato.

    Le barre sono ordinate con `ordina_per_grafico`; l'asse orizzontale porta
    le parole, l'asse verticale il numero di occorrenze. Il percorso di output
    è esplicito: il file non viene mai scritto in una posizione implicita.
    """
    righe = ordina_per_grafico(frequenze)
    parole = [parola for parola, _ in righe]
    conteggi = [conteggio for _, conteggio in righe]

    figura, assi = plt.subplots(figsize=(8, 4.5))
    assi.bar(parole, conteggi, color="#0e6b85")
    assi.set_title(titolo)
    assi.set_xlabel("parola (normalizzazione: casefold)")
    assi.set_ylabel("occorrenze")
    assi.set_ylim(bottom=0)
    figura.tight_layout()
    figura.savefig(percorso_png, dpi=120)
    plt.close(figura)
    return percorso_png


if __name__ == "__main__":
    # Dimostrazione sotto guardia: dataset già in memoria, nessuna lettura
    # da file, PNG salvato su un percorso dichiarato accanto al sorgente.
    from pathlib import Path

    FREQUENZE_CANONICHE = {"sole": 3, "luna": 2, "mare": 1}
    FREQUENZE_CON_PAREGGIO = {"luna": 2, "sole": 2, "mare": 1}

    uscita = Path(__file__).with_name("output")
    uscita.mkdir(exist_ok=True)

    for nome, frequenze in (
        ("frequenze-canoniche.png", FREQUENZE_CANONICHE),
        ("frequenze-pareggio.png", FREQUENZE_CON_PAREGGIO),
    ):
        percorso = costruisci_grafico(frequenze, uscita / nome)
        print(f"grafico salvato in {percorso}")

    print("tabella equivalente del dataset canonico:")
    for riga in tabella_equivalente(ordina_per_grafico(FREQUENZE_CANONICHE)):
        print(" ", riga)
