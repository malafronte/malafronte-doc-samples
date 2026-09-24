"""Analizzatore di testi: soluzione di riferimento del laboratorio LAB-PY-U7.

Collocare il file in `programmi/analizzatore_testi_u7.py` della raccolta
dello studente. Questo modulo è la versione COMPLETA dell'analizzatore
sul quale lavora lo starter `analizzatore_u7.py`: contiene le stesse idee
con i nomi della spiegazione, mentre lo starter espone le firme che
controlla la suite di test.

Le parole si contano senza dizionari e senza insiemi, perché l'unità
tratta sequenze e non ancora le strutture associate: i conteggi vivono in
due liste PARALLELE, una per le parole e una per i rispettivi numeri.

L'import non chiede input e non stampa: le dimostrazioni stanno nel main
protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/analizzatore_testi_u7.py
"""

TESTO_TECNICO = (
    "Il sensore misura la corrente in microampere e invia i dati "
    "alla scheda; la scheda salva i valori e mostra la media "
    "delle misure del sensore."
)


def normalizza(testo: str) -> str:
    """Restituisce la forma normalizzata del `testo` ricevuto.

    Riceve una stringa `testo`, in genere con spazi esterni e spazi interni
    ripetuti. Restituisce una NUOVA stringa con gli spazi esterni eliminati
    (`strip`), le sequenze di spazi interne ridotte a un singolo spazio
    (`split` seguito da `join`) e tutte le lettere in forma minuscola
    (`casefold`).

    L'argomento non viene modificato: le stringhe sono immutabili e il
    valore ricevuto resta disponibile nella sua forma originale. Per testo
    vuoto, oppure composto dai soli spazi, il risultato è `""`.
    """
    senza_esterni = testo.strip()
    parole = senza_esterni.split()
    compatta = " ".join(parole)
    return compatta.casefold()


def tokenizza(testo: str) -> list[str]:
    """Restituisce le parole del `testo`, separate dagli spazi.

    Riceve la stringa `testo` e ne restituisce l'elenco delle parole,
    prodotto da `split()` senza argomenti: spazi, tabulazioni e a capo
    agiscono da separatori e le sequenze ripetute NON producono elementi
    vuoti. Restituisce una NUOVA lista di stringhe; l'argomento non viene
    modificato. Per testo vuoto il risultato è `[]`.

    La punteggiatura resta attaccata alle parole: «scheda;» e «scheda»
    sono elementi distinti. La separazione della punteggiatura non è
    richiesta a questo livello e richiederebbe strumenti non ancora visti.
    """
    return testo.split()


def conteggio_parole(parole: list[str]) -> tuple[list[str], list[int]]:
    """Restituisce le parole distinte con i rispettivi conteggi, in due liste parallele.

    Riceve l'elenco delle `parole`. Restituisce la tupla
    `(parole_distinte, conteggi)` nella quale `parole_distinte` contiene
    ciascuna parola UNA SOLA VOLTA, nell'ordine della PRIMA occorrenza, e
    `conteggi[i]` indica quante volte `parole_distinte[i]` compare
    nell'elenco ricevuto.

    INVARIANTE DELLE LISTE PARALLELE: le due liste hanno sempre la stessa
    lunghezza e gli elementi in posizione `i` si riferiscono l'uno
    all'altra. La corrispondenza è mantenuta dalla struttura del
    procedimento e non da un oggetto che associa le chiavi ai valori: in
    questa unità i dizionari non sono ancora disponibili.

    L'argomento non viene modificato. Per elenco vuoto il risultato è
    `([], [])`, cioè due liste vuote e parallele.

    Il confronto fra parole usa l'uguaglianza delle stringhe; la
    normalizzazione è compito di chi chiama, che la applica prima con
    `normalizza`.
    """
    distinte = []
    conteggi = []
    for parola in parole:
        if parola in distinte:
            posizione = distinte.index(parola)
            conteggi[posizione] += 1
        else:
            distinte.append(parola)
            conteggi.append(1)
    return (distinte, conteggi)


def parole_piu_lunghe(parole: list[str]) -> list[str]:
    """Restituisce tutte le parole di lunghezza massima, nell'ordine di prima occorrenza.

    Riceve l'elenco delle `parole` e restituisce una lista NUOVA con tutte
    le parole che raggiungono la lunghezza massima, nell'ordine con cui
    compaiono nell'elenco ricevuto; le ripetizioni della stessa parola più
    lunga sono conservate. L'argomento non viene modificato. Per elenco
    vuoto il risultato è `[]`.

    Il procedimento usa due passaggi: il primo determina la lunghezza
    massima su tutti gli elementi, il secondo raccoglie quelli che la
    raggiungono. Un solo passaggio con massimo parziale raccoglierebbe
    parole che poi risultano superate, e dovrebbe buttarle via.
    """
    if not parole:
        return []
    massima = 0
    for parola in parole:
        if len(parola) > massima:
            massima = len(parola)
    raccolte = []
    for parola in parole:
        if len(parola) == massima:
            raccolte.append(parola)
    return raccolte


def presenta(parole: list[str], separatore: str = ", ") -> str:
    """Restituisce le `parole` composte in una sola riga, separate da `separatore`.

    Riceve l'elenco delle `parole` e il `separatore` da porre fra l'una e
    l'altra, `", "` se omesso. Restituisce la stringa composta, senza
    separatore né iniziale né finale. L'argomento non viene modificato.
    Per elenco vuoto il risultato è `""`, perché non ci sono elementi da
    separare.

    Il metodo `join` si chiama sul SEPARATORE e riceve le parole:
    `separatore.join(parole)`.
    """
    return separatore.join(parole)


def media_lunghezze(parole: list[str]) -> float | None:
    """Restituisce la lunghezza media delle `parole`, oppure `None` se l'elenco è vuoto.

    Riceve l'elenco delle `parole` e restituisce la media delle loro
    lunghezze come numero a virgola mobile, senza arrotondamenti.
    L'argomento non viene modificato. Per elenco vuoto il risultato è
    `None`, perché la media di zero elementi non è definita: chi chiama
    controlla `None` prima di usare il valore.
    """
    if not parole:
        return None
    somma = 0
    for parola in parole:
        somma += len(parola)
    return somma / len(parole)


def sopra_media_lunghezza(parole: list[str]) -> list[str]:
    """Restituisce le parole strettamente più lunghe della media, nell'ordine ricevuto.

    Riceve l'elenco delle `parole`. Il procedimento usa DUE passaggi: il
    primo calcola la lunghezza media su tutti gli elementi, il secondo
    seleziona le parole con `len(parola) > media`, senza arrotondare la
    media. Il risultato è una lista NUOVA che conserva l'ordine di
    comparizione e i duplicati. L'argomento non viene modificato. Per
    elenco vuoto il risultato è `[]`.

    La selezione riguarda le PAROLE e non le loro lunghezze: il risultato
    contiene gli elementi dell'elenco ricevuto che superano la soglia.
    """
    media_valori = media_lunghezze(parole)
    if media_valori is None:
        return []
    selezionate = []
    for parola in parole:
        if len(parola) > media_valori:
            selezionate.append(parola)
    return selezionate


if __name__ == "__main__":
    # Le uniche stampe del modulo stanno qui: le funzioni sopra restituiscono
    # e non scrivono nulla.
    print("Testo di partenza")
    print(TESTO_TECNICO)
    print()

    normalizzato = normalizza(TESTO_TECNICO)
    print("normalizza :", normalizzato)

    parole = tokenizza(normalizzato)
    print("tokenizza  :", parole)
    print("quante parole:", len(parole))
    print()

    distinte, conteggi = conteggio_parole(parole)
    print("Parole distinte e conteggi (liste parallele)")
    for posizione in range(len(distinte)):
        print(f"  {distinte[posizione]:<12} {conteggi[posizione]}")
    print("lunghezze parallele:", len(distinte) == len(conteggi))
    print()

    print("parole_piu_lunghe :", parole_piu_lunghe(parole))
    print("presenta          :", presenta(parole, " | "))
    print("presenta vuota    :", repr(presenta([])))
    print("media_lunghezze   :", media_lunghezze(parole))
    print("media_lunghezze([]):", media_lunghezze([]))
    print("sopra_media_lunghezza:", sopra_media_lunghezza(parole))
    print("sopra_media_lunghezza([]):", sopra_media_lunghezza([]))
