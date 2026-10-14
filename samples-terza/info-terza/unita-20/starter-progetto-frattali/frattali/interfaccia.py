"""Finestra minima e comandi dell'applicazione (in parte da completare).

Stato dello starter:

- fornita: `costruisci_finestra_minima` con campi, comandi, canvas ed
  etichette, senza alcuna logica di frattali (tappa FR-M6);
- da completare: `avvia_generazione`, `annulla_generazione`, `applica_zoom`
  ed `esporta_png` con fotografia, stati e invalidazione (tappa FR-M6,
  requisiti FR-07, FR-08 e FR-10).

L'importazione di `tkinter` avviene dentro le funzioni, così l'importazione
del modulo non apre finestre né richiede un display. Il contributo dello
starter (finestra minima e test pubblici) è dichiarato nella rubrica della
consegna e non sostituisce progettazione e integrazione dello studente.
"""

ZONA_ANTEPRIMA = (320, 240)
OFFSET_IMMAGINE = (8, 8)


def costruisci_finestra_minima():
    """Costruisce la finestra minima e restituisce i riferimenti (fornita, FR-M6).

    La finestra contiene i campi di larghezza, altezza e limite, i comandi
    Genera e Annulla, il canvas con la zona dell'immagine e le etichette di
    stato e messaggio. Nessun comando avvia calcoli di frattali.
    """
    import tkinter as tk
    from tkinter import ttk

    radice = tk.Tk()
    radice.title("Laboratorio dei frattali — finestra minima")
    cornice = ttk.Frame(radice, padding=8)
    cornice.grid(row=0, column=0, sticky="nsew")
    campi = {}
    for riga, (nome, valore) in enumerate(
        (("larghezza", "80"), ("altezza", "60"), ("limite", "25"))
    ):
        etichetta = ttk.Label(cornice, text=f"{nome}:")
        etichetta.grid(row=riga, column=0, sticky="w")
        campo = ttk.Entry(cornice, width=8)
        campo.insert(0, valore)
        campo.grid(row=riga, column=1, sticky="w")
        campi[nome] = campo
    comandi = {
        "genera": ttk.Button(cornice, text="Genera"),
        "annulla": ttk.Button(cornice, text="Annulla"),
    }
    comandi["genera"].grid(row=3, column=0, sticky="ew", pady=4)
    comandi["annulla"].grid(row=3, column=1, sticky="ew", pady=4)
    stato = ttk.Label(cornice, text="Finestra minima: collegare i comandi (FR-M6).")
    stato.grid(row=4, column=0, columnspan=2, sticky="w")
    messaggio = ttk.Label(cornice, text="")
    messaggio.grid(row=5, column=0, columnspan=2, sticky="w")
    tela = tk.Canvas(cornice, width=ZONA_ANTEPRIMA[0], height=ZONA_ANTEPRIMA[1], bg="white")
    tela.grid(row=0, column=2, rowspan=6, padx=(12, 0))
    return {
        "radice": radice,
        "cornice": cornice,
        "campi": campi,
        "comandi": comandi,
        "stato": stato,
        "messaggio": messaggio,
        "tela": tela,
    }


def avvia_generazione(finestra: object, configurazione: object):
    """Avvia un lavoro con fotografia dei campi (da completare, FR-M6)."""
    raise NotImplementedError("FR-M6: validare i campi, fotografare e programmare i blocchi.")


def annulla_generazione(finestra: object):
    """Annulla il lavoro in corso (da completare, FR-M6)."""
    raise NotImplementedError("FR-M6: invalidare le callback senza toccare il nuovo lavoro.")


def applica_zoom(finestra: object, fattore: object):
    """Cambia la vista con fattore e ripristino (da completare, FR-M6/FR-08)."""
    raise NotImplementedError("FR-M6: zoom con centro conservato e nuovo lavoro.")


def esporta_png(finestra: object, percorso: object):
    """Esporta l'ultimo risultato completo (da completare, FR-M6/FR-10)."""
    raise NotImplementedError("FR-M6: rifiutare i parziali, verificare il PNG.")
