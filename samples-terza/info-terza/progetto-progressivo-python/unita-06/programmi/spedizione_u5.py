"""Preventivo di spedizione in funzioni pure, con test automatici (tappa U5).

La tariffa è quella della versione U3, invariata: fasce di peso esclusive e
supplementi indipendenti, importi interi in euro. Le funzioni di logica non
leggono input, non stampano e non dipendono da globali variabili; la CLI sta
soltanto in `main`, protetto dalla guardia di avvio.

La parte M26-M27 aggiunge tre operazioni su una lista di importi interi in
euro: registrazione in posto, anteprima con lista nuova e riepilogo con tupla.

Si esegue la CLI dalla root del progetto con:
    uv run python programmi/spedizione_u5.py
La suite si esegue con:
    uv run pytest -q programmi/test_spedizione_u5.py
"""


def errore_dati_spedizione(peso_g: int, destinazione: str, urgenza: str) -> str:
    """Restituisce "" se i tre dati sono ammessi, altrimenti il primo errore.

    Priorità del controllo: peso, poi destinazione, poi urgenza. Peso ammesso:
    intero da 1 a 10000 grammi. Destinazione ammessa: la stringa esatta
    "locale" oppure "nazionale". Urgenza ammessa: la stringa esatta "s"
    oppure "n". Nessuna normalizzazione: maiuscole, spazi e token vuoti non
    sono ammessi.
    """
    if peso_g < 1 or peso_g > 10000:
        return "Peso non ammesso"
    if destinazione != "locale" and destinazione != "nazionale":
        return "Destinazione non ammessa"
    if urgenza != "s" and urgenza != "n":
        return "Urgenza non ammessa"
    return ""


def costo_base_spedizione(peso_g: int) -> int:
    """Restituisce il costo base in euro interi per un peso ammesso (1-10000).

    Fasce esclusive: 3 euro fino a 500 g, 5 euro fino a 2000 g, 8 euro oltre.
    Il risultato è un importo intero: nessuna formattazione.
    """
    if peso_g <= 500:
        return 3
    if peso_g <= 2000:
        return 5
    return 8


def supplemento_destinazione(destinazione: str) -> int:
    """Restituisce il supplemento in euro interi per una destinazione ammessa.

    "locale" vale 0 euro, "nazionale" vale 4 euro. Precondizione: il token è
    uno di quelli ammessi dal validatore.
    """
    if destinazione == "nazionale":
        return 4
    return 0


def supplemento_urgenza(urgenza: str) -> int:
    """Restituisce il supplemento in euro interi per un'urgenza ammessa.

    "n" vale 0 euro, "s" vale 2 euro. Precondizione: il token è uno di quelli
    ammessi dal validatore.
    """
    if urgenza == "s":
        return 2
    return 0


def totale_spedizione(peso_g: int, destinazione: str, urgenza: str) -> int:
    """Restituisce il totale in euro interi per dati tutti ammessi.

    Somma il costo base e i due supplementi chiamando le funzioni pertinenti.
    Precondizione: `errore_dati_spedizione` restituisce "" sugli stessi dati.
    """
    return (
        costo_base_spedizione(peso_g)
        + supplemento_destinazione(destinazione)
        + supplemento_urgenza(urgenza)
    )


# --- Operazioni sulle collezioni di preventivi (milestone M26-M27) ---


def registra_preventivo(preventivi: list[int], importo_euro: int) -> None:
    """Aggiunge l'importo in coda alla lista ricevuta e restituisce None.

    Effetto: la lista ricevuta è modificata in posto; il risultato della
    chiamata è None. Dominio: lista di importi interi non negativi in euro,
    lista vuota compresa, e importo intero non negativo in euro.
    """
    preventivi.append(importo_euro)


def anteprima_preventivo(preventivi: list[int], importo_euro: int) -> list[int]:
    """Restituisce una lista nuova con gli importi noti e quello aggiuntivo.

    La lista ricevuta resta invariata e il risultato è un oggetto diverso da
    essa. La copia è costruita elemento per elemento: le forme compatte di
    copia arrivano con il capitolo sulle sequenze. Dominio come
    `registra_preventivo`.
    """
    anteprima = []
    for importo in preventivi:
        anteprima.append(importo)
    anteprima.append(importo_euro)
    return anteprima


def riepilogo_preventivi(preventivi: list[int]) -> tuple[int, int]:
    """Restituisce (numero dei preventivi, somma degli importi in euro).

    Nessun effetto sulla lista ricevuta. La lista vuota restituisce (0, 0).
    Le due grandezze della tupla hanno significati diversi e non si sommano.
    """
    somma = 0
    for importo in preventivi:
        somma = somma + importo
    return (len(preventivi), somma)


# --- Totale ricorsivo sui preventivi in centesimi (tappa U6) ---


def totale_preventivi_ric(importi_cent: list[int], quanti: int) -> int:
    """Restituisce la somma dei primi `quanti` importi, senza modificare la lista.

    Dominio: lista di interi non negativi in centesimi e `quanti` intero con
    0 <= quanti <= len(importi_cent); per le prove pubbliche al massimo 100
    elementi. `quanti` è una **quantità** di elementi, non l'indice
    dell'ultimo: l'indice dell'ultimo elemento del prefisso è `quanti - 1`.
    Procedimento: base con `quanti = 0` che vale 0; riduzione che toglie
    l'ultimo elemento del prefisso; ricomposizione che lo somma al totale del
    prefisso più corto. I valori fuori contratto non sono gestiti.
    """
    if quanti == 0:
        return 0
    return importi_cent[quanti - 1] + totale_preventivi_ric(importi_cent, quanti - 1)


# --- Interazione a riga di comando ---


def main() -> None:
    """Legge i tre dati, valida, calcola e presenta il preventivo.

    Su dato non ammesso stampa il solo messaggio del validatore e nessuna riga
    di costo. Nessun valore utile restituito.
    """
    peso_testo = input("Peso del kit in grammi interi (da 1 a 10000): ")
    destinazione = input("Destinazione (locale o nazionale): ")
    urgenza = input("Urgenza (s o n): ")
    peso_g = int(peso_testo)

    errore = errore_dati_spedizione(peso_g, destinazione, urgenza)
    if errore != "":
        print(errore)
        return

    costo_base = costo_base_spedizione(peso_g)
    supplemento_dest = supplemento_destinazione(destinazione)
    supplemento_urg = supplemento_urgenza(urgenza)
    totale = totale_spedizione(peso_g, destinazione, urgenza)

    print(f"Peso: {peso_g} g")
    print(f"Destinazione: {destinazione}")
    print(f"Urgenza: {urgenza}")
    print(f"Costo base: {costo_base:.2f} euro")
    print(f"Supplemento destinazione: {supplemento_dest:.2f} euro")
    print(f"Supplemento urgenza: {supplemento_urg:.2f} euro")
    print(f"Totale: {totale:.2f} euro")


if __name__ == "__main__":
    main()
