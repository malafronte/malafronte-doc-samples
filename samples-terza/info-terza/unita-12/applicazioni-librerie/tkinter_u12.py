"""Interfaccia grafica con tkinter: calcolo noto separato dalla finestra.

Applicazione della libreria `tkinter` dell'Unità 12 - **Approfondimento**: il
calcolo e la sua validazione restano funzioni pure della libreria standard,
l'interfaccia si limita a leggere i campi, invocare il calcolo e mostrare il
risultato o il messaggio d'errore. Nessuna classe definita da noi: la finestra
è costruita in modo procedurale con `tkinter.ttk` e il ciclo degli eventi è
`mainloop()`.

Contratti delle funzioni pure:

- `centesimi_da_testo(testo)` → intero non negativo; solleva `ValueError` con
  il motivo se il testo non è un intero ammesso. La conversione e il controllo
  del dominio sono controlli separati.
- `valore_in_centesimi(quantita, prezzo_centesimi)` → prodotto dei due interi
  non negativi, come nel [cap. PY-16](/info-terza/corso/python/moduli-persistenza-errori/16-moduli-organizzazione-progetto/);
  nessun I/O.
- `formatta_euro(centesimi)` → stringa monetaria a due decimali con la virgola
  decimale, come `formatta_centesimi` del [cap. PY-20](/info-terza/corso/python/moduli-persistenza-errori/20-csv-json-record-persistenti/).

La callback dei pulsanti è passata **senza parentesi**: `command=calcola`
registra la funzione da richiamare al clic, mentre `command=calcola()`
chiamerebbe la funzione subito, alla costruzione della finestra. La finestra
non si blocca durante il calcolo: la callback termina prima che `mainloop`
prosegua. `calcola` legge i widget creati nel blocco di avvio, che esistono
solo quando il file viene eseguito: le funzioni pure in alto si provano anche
senza finestra, la callback no.

Ambiente: CPython sul computer con Tcl/Tk disponibile. La disponibilità di
Tk si controlla con `uv run python -m tkinter`; importare questo modulo non
apre finestre.
"""

import tkinter as tk
from tkinter import ttk


def centesimi_da_testo(testo):
    """Converte il testo di un campo in centesimi interi non negativi."""
    valore = testo.strip()
    if valore == "":
        raise ValueError("campo vuoto: inserire un numero intero")
    try:
        centesimi = int(valore)
    except ValueError:
        raise ValueError(f"valore non valido: {valore!r} non è un intero") from None
    if centesimi < 0:
        raise ValueError(f"valore non valido: {centesimi} è negativo")
    return centesimi


def valore_in_centesimi(quantita, prezzo_centesimi):
    """Restituisce il valore complessivo in centesimi di quantità × prezzo."""
    for nome, valore in (("quantita", quantita), ("prezzo_centesimi", prezzo_centesimi)):
        if isinstance(valore, bool) or not isinstance(valore, int):
            raise TypeError(f"{nome}: atteso un intero, ricevuto {type(valore).__name__}")
        if valore < 0:
            raise ValueError(f"{nome}: negativo ({valore})")
    return quantita * prezzo_centesimi


def formatta_euro(centesimi):
    """Formatta i centesimi come importo in euro con due decimali."""
    euro, resto = divmod(centesimi, 100)
    return f"{euro},{resto:02d} €"


def calcola():
    """Callback del pulsante: legge i campi, calcola e aggiorna la finestra."""
    testo_quantita = campo_quantita.get()
    testo_prezzo = campo_prezzo.get()
    try:
        quantita = centesimi_da_testo(testo_quantita)
        prezzo = centesimi_da_testo(testo_prezzo)
        totale = valore_in_centesimi(quantita, prezzo)
    except ValueError as errore:
        etichetta_risultato.configure(text=f"input non valido: {errore}")
        return
    etichetta_risultato.configure(text=f"valore complessivo: {formatta_euro(totale)}")


if __name__ == "__main__":
    # Costruzione procedurale della finestra: la parte qui sotto è
    # presentazione, il calcolo resta nelle funzioni pure in alto.
    finestra = tk.Tk()
    finestra.title("LAB-PY-U12 - valore dell'inventario")

    etichetta_quantita = ttk.Label(finestra, text="quantita")
    campo_quantita = ttk.Entry(finestra, width=12)
    campo_quantita.insert(0, "4")
    etichetta_prezzo = ttk.Label(finestra, text="prezzo in centesimi")
    campo_prezzo = ttk.Entry(finestra, width=12)
    campo_prezzo.insert(0, "25")
    pulsante = ttk.Button(finestra, text="calcola", command=calcola)
    etichetta_risultato = ttk.Label(finestra, text="valore complessivo: -")

    etichetta_quantita.grid(row=0, column=0, padx=8, pady=4, sticky="e")
    campo_quantita.grid(row=0, column=1, padx=8, pady=4)
    etichetta_prezzo.grid(row=1, column=0, padx=8, pady=4, sticky="e")
    campo_prezzo.grid(row=1, column=1, padx=8, pady=4)
    pulsante.grid(row=2, column=0, columnspan=2, padx=8, pady=8)
    etichetta_risultato.grid(row=3, column=0, columnspan=2, padx=8, pady=4)

    finestra.mainloop()
