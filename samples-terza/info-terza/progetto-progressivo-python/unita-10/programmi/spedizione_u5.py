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


# --- Coppie e tabelle di sintesi (tappa U7) ---


def normalizza_destinazione(destinazione: str) -> str:
    """Riconduce il testo della destinazione a uno dei due valori ammessi.

    Elimina gli spazi esterni con `strip()` e applica `casefold()`.
    Precondizione: il risultato è "locale" oppure "nazionale". Non elimina gli
    spazi interni, non cambia gli accenti, non traduce sinonimi. La stringa
    ricevuta resta invariata: le stringhe sono immutabili.
    """
    return destinazione.strip().casefold()


def prepara_coppie(dati_spedizione: list) -> list:
    """Costruisce le coppie (destinazione, totale_cent) dai dati di spedizione.

    Ogni elemento di `dati_spedizione` è una terna
    `(peso_g, destinazione_testo, urgenza)` nel dominio U5, con destinazione
    normalizzabile. Per ogni spedizione si normalizza la destinazione, si
    calcola il totale in euro con `totale_spedizione` e lo si converte **una
    sola volta** in centesimi. Precondizione: dopo la normalizzazione i dati
    sono ammessi da `errore_dati_spedizione`, che resta il controllo del
    rifiuto e si esercita separatamente. La lista delle spedizioni resta
    invariata.
    """
    coppie = []
    for peso_g, destinazione_testo, urgenza in dati_spedizione:
        destinazione = normalizza_destinazione(destinazione_testo)
        totale_euro = totale_spedizione(peso_g, destinazione, urgenza)
        coppie.append((destinazione, totale_euro * 100))
    return coppie


def preventivi_sopra_media(preventivi: list) -> list:
    """Restituisce una lista nuova con le coppie strettamente sopra la media.

    Riceve coppie già normalizzate `(destinazione, totale_cent)` e conserva
    ordine e duplicati. La media è la media aritmetica dei totali in
    centesimi, senza arrotondamento: il confronto è stretto, quindi una lista
    con tutti i totali uguali restituisce `[]`. L'input resta invariato; le
    tuple selezionate possono essere condivise, perché i loro elementi sono
    immutabili. Lista vuota in ingresso → lista vuota in uscita.
    """
    if len(preventivi) == 0:
        return []
    somma = 0
    for destinazione, totale_cent in preventivi:
        somma = somma + totale_cent
    numero = len(preventivi)
    sopra = []
    for coppia in preventivi:
        # totale > somma / numero equivale a totale * numero > somma.
        # Il confronto fra interi evita l'arrotondamento della divisione.
        if coppia[1] * numero > somma:
            sopra.append(coppia)
    return sopra


def matrice_riepilogo(preventivi: list) -> tuple:
    """Restituisce (conteggi, somme_cent) per `locale` e `nazionale`, in quest'ordine.

    Riceve coppie già normalizzate. Entrambe le liste del risultato hanno due
    elementi — la prima colonna `locale`, la seconda `nazionale` — sono nuove,
    distinte fra loro e fra chiamate successive. I conteggi sono numeri di
    spedizioni, le somme sono importi in centesimi: le due grandezze non si
    sommano fra loro. L'input resta invariato; lista vuota → `([0, 0], [0, 0])`.
    """
    conteggi = [0, 0]
    somme_cent = [0, 0]
    for destinazione, totale_cent in preventivi:
        if destinazione == "locale":
            posizione = 0
        else:
            posizione = 1
        conteggi[posizione] = conteggi[posizione] + 1
        somme_cent[posizione] = somme_cent[posizione] + totale_cent
    return (conteggi, somme_cent)


# --- Registro di record (tappa U8) ---


def crea_registro(codici: list, preventivi: list):
    """Migra liste parallele in una lista di record, senza risultati parziali.

    `codici` contiene stringhe non vuote e uniche; `preventivi` contiene le
    coppie `(destinazione, totale_cent)` già nel dominio U7, in centesimi. Le
    due liste devono avere la stessa lunghezza. Restituisce una **lista nuova
    di dizionari nuovi** con i campi `codice`, `destinazione` e `totale_cent`,
    conservando l'ordine; gli argomenti restano invariati. Lunghezze
    discordanti, codice vuoto o codice duplicato → `None`: i codici sono
    stringhe e `"007"` è diverso da `"7"`. Due liste vuote → lista vuota.
    """
    if len(codici) != len(preventivi):
        return None
    codici_visti = []
    for codice in codici:
        if codice == "":
            return None
        if codice in codici_visti:
            return None
        codici_visti.append(codice)
    registro = []
    for posizione in range(len(codici)):
        destinazione, totale_cent = preventivi[posizione]
        registro.append(
            {
                "codice": codici[posizione],
                "destinazione": destinazione,
                "totale_cent": totale_cent,
            }
        )
    return registro


def riepilogo_per_destinazione(registro: list) -> dict:
    """Restituisce il riepilogo del registro con entrambe le destinazioni.

    Il risultato è un dizionario con le chiavi `locale` e `nazionale`, ciascuna
    associata a un **record nuovo** con i campi interi `conteggio` e
    `totale_cent`. Le due grandezze hanno significati diversi e non si
    sommano. L'argomento resta invariato; senza record, entrambi i campi di
    entrambi i gruppi valgono 0. Precondizione: destinazioni ammesse.
    """
    riepilogo = {
        "locale": {"conteggio": 0, "totale_cent": 0},
        "nazionale": {"conteggio": 0, "totale_cent": 0},
    }
    for record in registro:
        gruppo = riepilogo[record["destinazione"]]
        gruppo["conteggio"] = gruppo["conteggio"] + 1
        gruppo["totale_cent"] = gruppo["totale_cent"] + record["totale_cent"]
    return riepilogo


def cerca_preventivo(registro: list, codice: str):
    """Restituisce il record del codice richiesto oppure None.

    La ricerca non modifica il registro. Il record restituito è
    **dichiaratamente** quello contenuto nella lista, non una copia: chi lo
    riceve può osservarlo e modificarlo come alias del registro stesso. I
    codici si confrontano come stringhe, zeri iniziali compresi.
    """
    for record in registro:
        if record["codice"] == codice:
            return record
    return None


# --- Viste ordinate per la consultazione (tappa U10) ---


def chiave_codice(record: dict) -> str:
    """Criterio di ordinamento: il codice stringa del record."""
    return record["codice"]


def chiave_totale(record: dict) -> int:
    """Criterio di ordinamento: il totale in centesimi del record."""
    return record["totale_cent"]


def ordina_inserimento(elementi: list, chiave) -> list:
    """Restituisce una lista nuova ordinata con l'ordinamento per inserimento.

    Procedimento elementare: si estrae un elemento e lo si sposta verso
    sinistra finché gli elementi precedenti sono maggiori secondo la `chiave`;
    il confronto è stretto, quindi l'ordinamento è **stabile**: elementi con
    la stessa chiave conservano l'ordine relativo di ingresso. La lista
    ricevuta non è modificata e i record restano gli stessi oggetti.
    """
    ordinati = list(elementi)
    for posizione in range(1, len(ordinati)):
        corrente = ordinati[posizione]
        indice = posizione - 1
        while indice >= 0 and chiave(ordinati[indice]) > chiave(corrente):
            ordinati[indice + 1] = ordinati[indice]
            indice = indice - 1
        ordinati[indice + 1] = corrente
    return ordinati


def vista_per_codice(registro: list) -> list:
    """Restituisce una lista nuova dei record ordinata per `codice` crescente.

    L'ordine è lessicografico sulle stringhe: gli zeri iniziali sono
    conservati e `"007"` non coincide con `"7"`. `registro` e i record non
    sono mutati; la lista è nuova ma contiene gli **stessi riferimenti** ai
    record, come dichiarato dal contratto.
    """
    return ordina_inserimento(registro, chiave_codice)


def vista_per_totale(registro: list) -> list:
    """Restituisce una lista nuova ordinata per `totale_cent` crescente.

    L'ordinamento è stabile: i record con lo stesso totale conservano l'ordine
    relativo del registro di origine. `registro` e i record non sono mutati;
    la lista è nuova e condivide i riferimenti ai record.
    """
    return ordina_inserimento(registro, chiave_totale)


def cerca_per_codice(vista: list, codice: str):
    """Restituisce il record del codice oppure None con ricerca dicotomica.

    Precondizione: `vista` è ordinata per codice crescente, come restituito da
    `vista_per_codice`. La ricerca dimezza a ogni passo l'intervallo da
    esaminare e non modifica né la vista né i record. I codici sono unici nel
    registro valido; si confrontano come stringhe, zeri iniziali compresi.
    """
    basso = 0
    alto = len(vista) - 1
    while basso <= alto:
        mezzo = (basso + alto) // 2
        if vista[mezzo]["codice"] == codice:
            return vista[mezzo]
        if vista[mezzo]["codice"] < codice:
            basso = mezzo + 1
        else:
            alto = mezzo - 1
    return None


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
