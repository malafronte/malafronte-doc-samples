"""Analisi di un testo: conteggio delle parole e classifica delle frequenze.

Questo modulo contiene **solo calcolo** sull'analisi di un file di testo:
le funzioni ricevono righe già decodificate oppure un percorso e restituiscono
risultati. Nessuna domanda, nessuna presentazione: la stampa e la gestione dei
messaggi sono della CLI `cli_testo_u12.py`.

Contratto di tokenizzazione: una **parola** è un token separato da spazi
bianchi (`str.split`), normalizzato con `casefold`. La punteggiatura resta
parte della parola: `sole` e `sole,` sono parole diverse. Il contratto si può
estendere con una tokenizzazione diversa, ma ogni estensione deve dichiararlo
e verificarlo con casi discriminanti.

Nuclei:

- `conta_parole(righe)` - attraversa una sola volta l'iterabile di righe e
  restituisce la coppia `(totale, frequenze)`;
- `ordina_frequenze(frequenze, decrescente=False)` - classifica le coppie
  `(parola, frequenza)` con la parola crescente a parità;
- `analizza_file(percorso)` - apre il file in UTF-8 e compone i due passaggi
  nel dizionario di risultato usato dalla CLI.

Ambiente: CPython sul computer. Nessuna lettura da tastiera, nessuna stampa.
"""


def conta_parole(righe):
    """Conta le parole di un iterabile di righe già decodificate.

    L'iterabile viene attraversato **una volta**: ogni riga viene normalizzata
    con `casefold()` e suddivisa con `split()`, e i token aggiornano un
    contatore. Nessuna lista di tutte le parole viene accumulata: la memoria
    aggiuntiva dipende dalle parole distinte, non dal numero di token.

    Il risultato è la coppia `(totale, frequenze)`: `totale` è il numero di
    token incontrati, `frequenze` è un **dizionario nuovo** che associa ogni
    parola normalizzata al suo conteggio. L'argomento non viene modificato.
    """
    totale = 0
    frequenze = {}
    for riga in righe:
        for parola in riga.casefold().split():
            totale = totale + 1
            if parola in frequenze:
                frequenze[parola] = frequenze[parola] + 1
            else:
                frequenze[parola] = 1
    return totale, frequenze


def ordina_frequenze(frequenze, decrescente=False):
    """Ordina le frequenze e restituisce una lista nuova di coppie.

    Il contratto di ordine ha due livelli: la **frequenza** cresce, oppure
    decresce se `decrescente` è `True`; a parità di frequenza la **parola**
    cresce sempre in ordine alfabetico, in entrambe le direzioni. Per questo la
    funzione non usa `reverse=True` sull'intera coppia, che invece
    capovolgerebbe anche l'ordine delle parole a parità.

    `frequenze` non viene modificato; la lista restituita è nuova.
    """
    if decrescente:
        return sorted(frequenze.items(), key=lambda coppia: (-coppia[1], coppia[0]))
    return sorted(frequenze.items(), key=lambda coppia: (coppia[1], coppia[0]))


def analizza_file(percorso):
    """Analizza un file di testo UTF-8 e restituisce il risultato completo.

    Il file viene aperto in lettura con `encoding="utf-8"` e chiuso dal
    `with` anche in caso di errore durante la scansione. Le righe del file sono
    già stringhe decodificate e vengono passate direttamente a `conta_parole`,
    che le attraversa una sola volta.

    Il risultato è un dizionario nuovo con quattro chiavi:
    - `totale`: numero di token complessivi;
    - `frequenze`: dizionario `parola -> conteggio`;
    - `classifica_crescente`: lista di coppie `(parola, frequenza)` per
      frequenza crescente, parola crescente a parità;
    - `classifica_decrescente`: stessa lista per frequenza decrescente, parola
      sempre crescente a parità.

    Gli errori di I/O e di decodifica **non vengono catturati**: si propagano
    al coordinatore, che sceglie il messaggio e il recupero.
    """
    with open(percorso, "r", encoding="utf-8") as sorgente:
        totale, frequenze = conta_parole(sorgente)
    return {
        "totale": totale,
        "frequenze": frequenze,
        "classifica_crescente": ordina_frequenze(frequenze),
        "classifica_decrescente": ordina_frequenze(frequenze, decrescente=True),
    }


if __name__ == "__main__":
    # Dimostrazione minima sul dataset canonico, senza I/O di file.
    righe_canoniche = ["Sole luna sole", "mare LUNA sole"]
    totale, frequenze = conta_parole(righe_canoniche)
    print(f"totale: {totale}, distinte: {len(frequenze)}")
    print(f"frequenze: {frequenze}")
    print(f"crescente: {ordina_frequenze(frequenze)}")
    print(f"decrescente: {ordina_frequenze(frequenze, decrescente=True)}")
