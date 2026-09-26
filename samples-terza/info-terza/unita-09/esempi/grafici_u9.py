"""Grafici dell'Unità 9: dati teorici e misure reali con matplotlib.

Collocare il file in `programmi/grafici_u9.py` della raccolta dello studente.
Il modulo disegna tre grafici del capitolo PY-13, parte IV:

- le sei famiglie di crescita da dati teorici dichiarati, in due pannelli
  leggibili: crescite moderate ed esponenziale separate, per non schiacciare
  le serie piccole su un asse lineare;
- le visite agli elementi per una e due scansioni, da n = 2, 4, 8, 16;
- le durate reali misurate da `misure_u9`, con unità unica e sintesi.

I dati teorici sono valori di funzioni matematiche: non sono tempi in
secondi e non sono conteggi automaticamente attribuibili a qualunque
programma. I dati misurati provengono da campioni realmente raccolti e
riportano l'ambiente di esecuzione; distinguerli è parte della lettura del
grafico. Le uguaglianze per n piccoli, per esempio n e n² uguali a n = 2,
non contraddicono il diverso ordine di crescita.

Grafici leggibili senza affidarsi ai soli colori: ogni serie ha linea e
marcatore propri. Nessun titolo promozionale: i grafici mostrano dati e
non dimostrano che un algoritmo sia sempre più veloce di un altro.

Nessuna finestra interattiva: `fig.savefig(percorso)` scrive l'immagine e
non si chiama `plt.show()`. Per questo il modulo sceglie il backend `Agg`,
che esporta file senza aprire finestre: il successo dell'esportazione PNG
non richiede la disponibilità di una finestra grafica. La cartella di
destinazione va creata prima dell'esecuzione: il programma si limita a
segnalarne l'assenza e non la crea da solo. Gli import non producono figure:
i grafici si costruiscono solo nel main protetto dalla guardia di avvio.

Esecuzione: uv run python programmi/grafici_u9.py
"""

import os
import platform

import matplotlib

matplotlib.use("Agg")  # solo esportazione su file: nessuna finestra grafica

import matplotlib.pyplot as plt

import misure_u9


# ---------------------------------------------------------------------------
# Dati teorici dichiarati
# ---------------------------------------------------------------------------


def dati_crescite() -> dict[str, list[int]]:
    """Restituisce i valori esatti delle sei famiglie di crescita.

    Serie dichiarate dal capitolo per n = 2, 4, 8, 16, nell'ordine
    1, log2(n), n, n*log2(n), n^2, 2^n. Per n = 2 le sei colonne valgono
    2/1/2/2/4/4, per n = 4 valgono 4/2/4/8/16/16, per n = 8 valgono
    8/3/8/24/64/256 e per n = 16 valgono 16/4/16/64/256/65536. Sono valori
    di funzioni matematiche, non misure: non richiedono esecuzioni.
    """
    return {
        "n": [2, 4, 8, 16],
        "costante": [1, 1, 1, 1],
        "logaritmo": [1, 2, 3, 4],
        "lineare": [2, 4, 8, 16],
        "n_log_n": [2, 8, 24, 64],
        "quadratica": [4, 16, 64, 256],
        "esponenziale": [4, 16, 256, 65536],
    }


def dati_visite() -> dict[str, list[int]]:
    """Restituisce le visite agli elementi per una e due scansioni.

    n = [2, 4, 8, 16]; una scansione esegue n visite `[2, 4, 8, 16]`, due
    scansioni 2n visite `[4, 8, 16, 32]`. I punti sono conteggi esatti del
    modello; le linee che li collegano servono a leggerne l'andamento.
    """
    return {
        "n": [2, 4, 8, 16],
        "una_scansione": [2, 4, 8, 16],
        "due_scansioni": [4, 8, 16, 32],
    }


# ---------------------------------------------------------------------------
# Salvataggio esplicito
# ---------------------------------------------------------------------------


def salva_figura(fig, percorso: str) -> bool:
    """Salva la figura nel percorso ricevuto come parametro.

    La cartella di destinazione NON viene creata dal programma: è lo
    studente a crearla prima dell'esecuzione. Se la cartella non esiste,
    viene stampato un messaggio chiaro e la figura non si salva. Restituisce
    True se il salvataggio è avvenuto. Il percorso senza componente di
    cartella indica la directory di lavoro corrente.
    """
    cartella = os.path.dirname(percorso)
    if cartella and not os.path.isdir(cartella):
        print(f"Cartella non trovata: {cartella}")
        print("Creare la cartella e ripetere l'esecuzione: il programma non la crea.")
        return False
    fig.savefig(percorso)
    print(f"Grafico salvato in: {percorso}")
    return True


# ---------------------------------------------------------------------------
# Grafici
# ---------------------------------------------------------------------------


def grafico_crescite(percorso: str) -> bool:
    """Disegna le sei famiglie di crescita e salva l'immagine nel `percorso`.

    Due pannelli affiancati su assi lineari: il primo contiene le famiglie
    che restano leggibili insieme, il secondo la sola esponenziale, che su
    lo stesso asse renderebbe invisibili le altre. I dati provengono da
    `dati_crescite()` e sono valori teorici dichiarati.
    """
    dati = dati_crescite()
    n = dati["n"]
    fig, (ax_moderate, ax_esponenziale) = plt.subplots(1, 2, figsize=(12, 5))

    ax_moderate.plot(n, dati["costante"], marker="o", linestyle="-", label="1")
    ax_moderate.plot(n, dati["logaritmo"], marker="s", linestyle="--", label="log2 n")
    ax_moderate.plot(n, dati["lineare"], marker="^", linestyle="-.", label="n")
    ax_moderate.plot(n, dati["n_log_n"], marker="v", linestyle=":", label="n * log2 n")
    ax_moderate.plot(n, dati["quadratica"], marker="D", linestyle="-", label="n^2")
    ax_moderate.set_title("Crescite moderate, asse lineare")
    ax_moderate.set_xlabel("n")
    ax_moderate.set_ylabel("Valore della funzione")
    ax_moderate.legend()
    ax_moderate.grid(True, alpha=0.3)

    ax_esponenziale.plot(
        n, dati["esponenziale"], marker="*", linestyle="-", color="firebrick", label="2^n"
    )
    ax_esponenziale.set_title("Crescita esponenziale, asse lineare")
    ax_esponenziale.set_xlabel("n")
    ax_esponenziale.set_ylabel("Valore della funzione")
    ax_esponenziale.legend()
    ax_esponenziale.grid(True, alpha=0.3)

    fig.suptitle("Sei famiglie di crescita: valori teorici dichiarati per n = 2, 4, 8, 16")
    fig.text(
        0.01,
        0.01,
        "Sintesi: i valori sono funzioni matematiche, non tempi; "
        "le uguaglianze per n piccolo non contraddicono gli ordini di crescita.",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    salvato = salva_figura(fig, percorso)
    plt.close(fig)
    return salvato


def grafico_visite(percorso: str) -> bool:
    """Disegna le visite agli elementi di una e due scansioni nel `percorso`.

    Dati esatti di `dati_visite()`: n contro 2n per n = 2, 4, 8, 16.
    Entrambe le serie sono lineari: la distanza fra di esse riguarda le
    costanti, non l'ordine di crescita.
    """
    dati = dati_visite()
    fig, ax = plt.subplots()
    ax.plot(
        dati["n"],
        dati["una_scansione"],
        marker="o",
        linestyle="-",
        label="Una scansione: n visite",
    )
    ax.plot(
        dati["n"],
        dati["due_scansioni"],
        marker="s",
        linestyle="--",
        label="Due scansioni: 2n visite",
    )
    ax.set_title("Visite agli elementi: una e due scansioni della stessa lista")
    ax.set_xlabel("Numero di elementi n")
    ax.set_ylabel("Visite agli elementi")
    ax.legend()
    ax.grid(True, alpha=0.3)
    salvato = salva_figura(fig, percorso)
    plt.close(fig)
    return salvato


def grafico_durate(percorso: str, dati: dict) -> bool:
    """Disegna le durate reali misurate e salva l'immagine nel `percorso`.

    `dati` è il risultato di `misure_u9.esegui_esperimenti()` o di
    `misure_u9.main()`; vengono usate le sole righe dell'esperimento
    «scansioni equivalenti». Unità unica: ogni durata per chiamata è
    convertita in millisecondi con la stessa scala, dichiarata sugli assi.
    Ogni punto è la MEDIANA dei cinque campioni raccolti; minimo e massimo
    sono nella tabella di `misure_u9` e descrivono i campioni, non un
    intervallo di confidenza. L'ambiente di esecuzione e la sintesi sono
    annotati nella figura.
    """
    punti = [
        punto
        for punto in dati["punti"]
        if punto["esperimento"] == "scansioni equivalenti"
    ]
    if not punti:
        print("Nessun dato di durata disponibile: eseguire prima gli esperimenti.")
        return False

    ambiente = dati["ambiente"]
    fig, ax = plt.subplots(figsize=(9, 6))
    for algoritmo, marcatore, linea, etichetta in (
        ("riepilogo_una_scansione", "o", "-", "Una scansione (mediana di 5 campioni)"),
        ("riepilogo_due_scansioni", "s", "--", "Due scansioni (mediana di 5 campioni)"),
    ):
        serie = [punto for punto in punti if punto["algoritmo"] == algoritmo]
        serie.sort(key=lambda punto: punto["dimensione"])
        dimensioni = [punto["dimensione"] for punto in serie]
        millisecondi = [1000 * punto["mediana_chiamata_s"] for punto in serie]
        ax.plot(dimensioni, millisecondi, marker=marcatore, linestyle=linea, label=etichetta)

    ax.set_title("Durata per chiamata delle due scansioni (mediana di 5 campioni)")
    ax.set_xlabel("Numero di elementi n")
    ax.set_ylabel("Durata per chiamata (ms)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.text(
        0.01,
        0.01,
        f"Ambiente: {ambiente['interprete']} su {ambiente['sistema']}, "
        f"timer {ambiente['timer']}, {ambiente['ripetizioni']} ripetizioni.\n"
        "Sintesi: le due serie crescono entrambe in modo lineare; la distanza fra di esse "
        "riguarda\nle costanti dell'implementazione, non l'ordine di crescita.",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    salvato = salva_figura(fig, percorso)
    plt.close(fig)
    return salvato


if __name__ == "__main__":
    # Nessun grafico viene prodotto all'import: questa è l'unica sede che
    # costruisce le figure. Le cartelle di destinazione vanno create prima.
    dati = misure_u9.esegui_esperimenti()
    grafico_crescite(os.path.join("figure_u9", "06-crescite-conteggi.png"))
    grafico_visite(os.path.join("figure_u9", "visite-scansioni.png"))
    grafico_durate(os.path.join("figure_u9", "07-scansioni-misure.png"), dati)
