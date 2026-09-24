"""Liste come vettori e tuple come record dell'Unità 7.

Collocare il file in `programmi/liste_tuple_u7.py` della raccolta dello
studente. Il modulo raccoglie le operazioni ordinarie sulle liste
(inserimento, rimozione, ricerca, inversione, ordinamento) e le
statistiche su un vettore di interi, con due temi ricorrenti:

1. ogni funzione dichiara se MODIFICA la lista ricevuta e se restituisce
   un valore oppure `None`: `append`, `extend`, `insert`, `remove`, `pop`,
   `clear`, `reverse` e `sort` lavorano sul posto e non restituiscono la
   lista aggiornata;
2. la copia e l'ordinamento senza modifica si ottengono con `copy()` e
   `sorted()`, che producono una lista NUOVA lasciando intatto l'argomento.

L'import non chiede input e non stampa: le dimostrazioni stanno nel main
protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/liste_tuple_u7.py
"""


# ---------------------------------------------------------------------------
# Creazione e copia
# ---------------------------------------------------------------------------


def crea_misure(valori: list[float]) -> list[float]:
    """Restituisce una nuova lista con gli stessi elementi di `valori`.

    Riceve la lista `valori` e ne restituisce una copia superficiale
    (`copy()`): la lista di arrivo è un oggetto distinto da quella di
    partenza, con gli stessi riferimenti agli elementi. Nessun argomento
    viene modificato. Per lista vuota il risultato è una lista vuota nuova,
    anch'essa distinta dall'argomento.
    """
    return valori.copy()


# ---------------------------------------------------------------------------
# Inserimento
# ---------------------------------------------------------------------------


def aggiungi_misura(misure: list[float], valore: float) -> None:
    """Aggiunge `valore` in coda a `misure` con `append` e non restituisce nulla.

    Riceve la lista `misure` e il `valore` da inserire. MODIFICA la lista
    ricevuta aggiungendo un elemento in ultima posizione; la lista
    ingrandita è la stessa di prima, non una copia. Il risultato è `None`:
    chi chiama osserva il cambiamento sulla variabile già posseduta.

    Per lista vuota il risultato è una lista di un solo elemento. La firma
    `-> None` rende visibile che NON si scrive `misure = misure.append(...)`:
    quell'assegnamento metterebbe `None` nella variabile.
    """
    misure.append(valore)


def aggiungi_piu_misure(misure: list[float], nuovi: list[float]) -> None:
    """Aggiunge in coda a `misure` tutti gli elementi di `nuovi`, uno per uno.

    Riceve la lista `misure` da estendere e la lista `nuovi` i cui elementi
    vanno aggiunti. MODIFICA `misure` in loco con `extend` e restituisce
    `None`. Con `nuovi` vuoti la lista ricevuta resta identica.

    Il contrasto con `append` è essenziale: `append(nuovi)` aggiungerebbe
    la LISTA `nuovi` come un unico elemento annidato, mentre `extend`
    scorre `nuovi` e aggiunge i suoi elementi alla stessa altezza di quelli
    già presenti.
    """
    misure.extend(nuovi)


def inserisci_misura(misure: list[float], valore: float, posizione: int) -> None:
    """Inserisce `valore` in `misure` alla `posizione` indicata, spostando gli altri.

    Riceve la lista `misure`, il `valore` da inserire e la `posizione`
    desiderata. MODIFICA la lista ricevuta con `insert` e restituisce
    `None`: gli elementi dalla `posizione` in avanti slittano a destra di
    uno. Per lista vuota il risultato è una lista di un solo elemento.

    `posizione` fuori intervallo NON produce errore: `insert` si comporta
    come Python e limita il valore ai confini ammessi. Una posizione
    negativa viene riferita alla fine della lista (`-1` inserisce prima
    dell'ultimo elemento); una posizione oltre la lunghezza inserisce in
    coda. La scelta del linguaggio è coerente con l'uso didattico: il
    controllo del dominio è compito di chi chiama, se il problema lo richiede.
    """
    misure.insert(posizione, valore)


# ---------------------------------------------------------------------------
# Rimozione
# ---------------------------------------------------------------------------


def rimuovi_prima_occorrenza(misure: list[float], valore: float) -> bool:
    """Toglie la prima occorrenza di `valore` da `misure` e indica se ha trovato.

    Riceve la lista `misure` e il `valore` da eliminare. MODIFICA la lista
    ricevuta con `remove`, che toglie la PRIMA occorrenza e compatta gli
    elementi successivi. Restituisce `True` se il valore era presente,
    `False` se non c'era. Per lista vuota il risultato è `False` e la lista
    resta vuota.

    In assenza del valore `list.remove` solleverebbe `ValueError`; qui la
    presenza viene accertata prima con l'operatore `in`, così il caso
    mancante diventa un valore di ritorno e non un'interruzione. La stessa
    lista può contenere duplicati: le altre occorrenze restano al loro posto.
    """
    if valore not in misure:
        return False
    misure.remove(valore)
    return True


def rimuovi_per_posizione(misure: list[float], posizione: int) -> float:
    """Toglie da `misure` l'elemento in `posizione` e lo restituisce.

    Riceve la lista `misure` e la `posizione` dell'elemento da eliminare.
    MODIFICA la lista ricevuta con `pop`: l'elemento viene rimosso e gli
    elementi successivi slittano a sinistra. Restituisce il valore rimosso, che
    resta disponibile al chiamante. Per lista vuota la chiamata non è
    applicabile: non esiste alcuna posizione valida.

    Il contrasto con `rimuovi_prima_occorrenza` è il criterio di scelta:
    `remove` riceve il VALORE e ne toglie la prima occorrenza senza
    restituirlo, `pop` riceve la POSIZIONE e restituisce l'elemento tolto.
    `posizione` fuori intervallo produce `IndexError`, quindi la validazione
    della posizione è parte della consegna quando il problema la richiede.
    """
    return misure.pop(posizione)


def svuota(misure: list[float]) -> None:
    """Elimina tutti gli elementi da `misure` e non restituisce nulla.

    Riceve la lista `misure` e la MODIFICA con `clear`, che la lascia vuota
    conservando lo stesso oggetto: le alias della lista osservano una lista
    vuota. Il risultato è `None`. Per lista già vuota non accade nulla.
    """
    misure.clear()


# ---------------------------------------------------------------------------
# Ricerca
# ---------------------------------------------------------------------------


def numero_occorrenze(misure: list[float], valore: float) -> int:
    """Restituisce quante volte `valore` compare in `misure`.

    Riceve la lista `misure` e il `valore` da cercare. Restituisce il
    conteggio prodotto da `count`, comprese le ripetizioni. L'argomento non
    viene modificato. Per lista vuota, oppure valore assente, il risultato
    è 0.
    """
    return misure.count(valore)


def posizione_valore(misure: list[float], valore: float) -> int:
    """Restituisce la posizione della prima occorrenza di `valore`, oppure `-1`.

    Riceve la lista `misure` e il `valore` da cercare. Restituisce l'indice
    del primo elemento uguale a `valore`; se il valore non compare
    restituisce la sentinella `-1`. L'argomento non viene modificato. Per
    lista vuota il risultato è `-1`.

    Il corpo controlla prima la presenza con `in` e chiama `index` solo se
    il valore c'è. Questa scelta sostituisce qui l'uso di `try/except`,
    che non è ancora un argomento dell'unità: `list.index` senza il
    controllo preventivo solleverebbe `ValueError` in assenza del valore.
    Non si usa invece il criterio di `str.find`, che restituisce `-1`
    direttamente: le liste non hanno `find`, e la sentinella `-1` resta un
    VALORE da confrontare (`posizione == -1`) e non un indice da usare.
    Scrivere `misure[posizione]` con `posizione == -1` restituirebbe
    l'ULTIMO elemento della lista e non segnalerebbe alcuna assenza.
    """
    if valore not in misure:
        return -1
    return misure.index(valore)


# ---------------------------------------------------------------------------
# Inversione e ordinamento
# ---------------------------------------------------------------------------


def copia_e_inverti(misure: list[float]) -> list[float]:
    """Restituisce una nuova lista con gli elementi di `misure` in ordine inverso.

    Riceve la lista `misure` e costruisce la lista inversa scorrendola
    dall'ultimo elemento al primo con un ciclo esplicito. L'argomento non
    viene modificato: la lista di arrivo è nuova. Per lista vuota il
    risultato è una lista vuota nuova.
    """
    inversa = []
    for posizione in range(len(misure) - 1, -1, -1):
        inversa.append(misure[posizione])
    return inversa


def copia_e_inverti_slice(misure: list[float]) -> list[float]:
    """Stesso risultato di `copia_e_inverti`, con la forma compatta dello slicing.

    Riceve la lista `misure` e restituisce la copia inversa prodotta dalla
    slicing `misure[::-1]`, che legge la lista dall'ultimo elemento al
    primo. L'argomento non viene modificato. Per lista vuota il risultato è
    una lista vuota nuova.

    La forma compatta è ammissibile DOPO aver visto il ciclo: la slicing
    nasconde lo stesso movimento indietro di `copia_e_inverti` e non va
    confusa con l'inversione sul posto.
    """
    return misure[::-1]


def inverti_sul_posto(misure: list[float]) -> None:
    """Inverte l'ordine degli elementi di `misure` e non restituisce nulla.

    Riceve la lista `misure` e la MODIFICA in loco con `reverse()`: la lista
    è la stessa di prima, con gli elementi in ordine opposto. Le alias della
    lista osservano subito l'inversione. Il risultato è `None`. Per lista
    vuota non accade nulla.

    La firma `-> None` segnala che NON si scrive `misure = misure.reverse()`:
    quell'assegnamento metterebbe `None` nella variabile.
    """
    misure.reverse()


def ordina_crescente(misure: list[float]) -> None:
    """Ordina `misure` in senso crescente sul posto e non restituisce nulla.

    Riceve la lista `misure` e la MODIFICA con `sort()`, che dispone gli
    elementi in ordine crescente nello stesso oggetto. Le alias osservano
    subito l'ordinamento. Il risultato è `None`. Per lista vuota non accade
    nulla; con elementi tutti uguali la lista resta equivalente.

    ATTENZIONE: `misure = misure.sort()` assegna `None` alla variabile
    `misure`, perché `sort` non restituisce la lista. La chiamata corretta
    è `misure.sort()` da sola, oppure l'assegnamento `misure = sorted(misure)`
    quando serve una lista nuova.
    """
    misure.sort()


def crescente_copia(misure: list[float]) -> list[float]:
    """Restituisce una nuova lista con gli elementi di `misure` in ordine crescente.

    Riceve la lista `misure` e ne restituisce una copia ordinata prodotta da
    `sorted()`. L'argomento non viene modificato: l'ordine di partenza resta
    disponibile. Per lista vuota il risultato è una lista vuota nuova.

    `sorted` e `sort` hanno lo stesso criterio di ordinamento e si
    distinguono soltanto per l'effetto: `sorted` costruisce una lista nuova,
    `sort` dispone gli elementi della lista già esistente.
    """
    return sorted(misure)


# ---------------------------------------------------------------------------
# Scansioni: somma, minimo, massimo, media, selezione
# ---------------------------------------------------------------------------


def statistiche_misure(valori: list[int]) -> tuple[int, int, int] | None:
    """Restituisce somma, minimo e massimo di `valori` come tupla, oppure `None`.

    Riceve la lista `valori` e restituisce la tupla
    `(somma, minimo, massimo)` calcolata con una sola scansione esplicita,
    nella quale l'accumulatore parte da 0 e i due estremi dal primo
    elemento. L'argomento non viene modificato.

    Per lista vuota il risultato è `None`: somma, minimo e massimo di un
    insieme di elementi senza elementi non sono definiti, e restituire 0
    come minimo confonderebbe un dato mancante con un dato uguale a 0. La
    scelta è deliberata e dichiarata: chi chiama controlla `None` prima di
    usare la tupla.

    La stessa scansione si può scrivere con `sum(valori)`, `min(valori)` e
    `max(valori)`; queste funzioni sollevano `ValueError` su lista vuota e
    non producono il caso `None` qui scelto.
    """
    if not valori:
        return None
    somma = 0
    minimo = valori[0]
    massimo = valori[0]
    for valore in valori:
        somma += valore
        if valore < minimo:
            minimo = valore
        if valore > massimo:
            massimo = valore
    return (somma, minimo, massimo)


def media(valori: list[int]) -> float | None:
    """Restituisce la media aritmetica di `valori`, oppure `None` se è vuota.

    Riceve la lista `valori` e restituisce la media come numero a virgola
    mobile, senza arrotondamenti. L'argomento non viene modificato. Per
    lista vuota il risultato è `None`, perché la media di zero elementi non
    è definita e la divisione per zero non è ammessa.
    """
    if not valori:
        return None
    somma = 0
    for valore in valori:
        somma += valore
    return somma / len(valori)


def sopra_media(valori: list[int]) -> list[int]:
    """Restituisce i valori strettamente superiori alla media, nell'ordine di partenza.

    Riceve la lista `valori`. Il procedimento usa DUE passaggi separati: il
    primo calcola la media su tutti gli elementi, il secondo seleziona gli
    elementi con `valore > media`, senza arrotondare la media. Il risultato
    è una lista NUOVA che conserva l'ordine di comparizione e anche i
    duplicati. L'argomento non viene modificato. Per lista vuota il
    risultato è `[]`.

    I due passaggi sono distinti per una ragione di modello: la media serve
    a decidere per TUTTI gli elementi e non è nota prima della prima
    scansione. Un solo passaggio con media parziale selezionerebbe
    confrontando con un valore che cambia a ogni elemento.
    """
    if not valori:
        return []
    somma = 0
    for valore in valori:
        somma += valore
    media_valori = somma / len(valori)
    selezionati = []
    for valore in valori:
        if valore > media_valori:
            selezionati.append(valore)
    return selezionati


if __name__ == "__main__":
    # Le uniche stampe del modulo stanno qui: ogni funzione sopra restituisce
    # e non scrive nulla.
    originali = [12.5, 7.0, 19.5, 7.0, 4.5]
    print("Copia e inserimento")
    copia = crea_misure(originali)
    print("originale:", originali)
    print("copia    :", copia, "-> oggetti distinti:", copia is not originali)

    lavorazione = crea_misure(originali)
    aggiungi_misura(lavorazione, 3.0)
    print("append di 3.0        :", lavorazione, "-> restituisce None")
    aggiungi_piu_misure(lavorazione, [100.0, 101.0])
    print("extend di [100, 101] :", lavorazione)
    inserisci_misura(lavorazione, 0.5, 0)
    print("insert di 0.5 in 0   :", lavorazione)
    inserisci_misura(lavorazione, 99.0, 1000)
    print("insert di 99.0 in 1000:", lavorazione, "-> posizione limitata in coda")

    print()
    print("Rimozione")
    rimossa = rimuovi_prima_occorrenza(lavorazione, 7.0)
    print("remove di 7.0        :", rimossa, lavorazione)
    assente = rimuovi_prima_occorrenza(lavorazione, -1.0)
    print("remove di -1.0       :", assente, "-> nessun errore, lista invariata")
    tolto = rimuovi_per_posizione(lavorazione, 0)
    print("pop di 0             :", tolto, lavorazione)

    print()
    print("Ricerca")
    prova = [4, 7, 4, 9]
    print("count di 4 in", prova, "->", numero_occorrenze(prova, 4))
    print("index di 9 in", prova, "->", posizione_valore(prova, 9))
    print("index di 5 in", prova, "->", posizione_valore(prova, 5), "(sentinella da confrontare)")

    print()
    print("Inversione e ordinamento")
    base = [3, 1, 2]
    print("base                 :", base)
    print("copia invertita (ciclo) :", copia_e_inverti(base), "-> base:", base)
    print("copia invertita (slice) :", copia_e_inverti_slice(base), "-> base:", base)
    inverti_sul_posto(base)
    print("inverti_sul_posto    :", base, "-> restituisce None")
    ordina_crescente(base)
    print("ordina_crescente     :", base, "-> restituisce None")
    ordinata = crescente_copia([5, 2, 8])
    print("crescente_copia      :", ordinata)

    print()
    print("Scansioni")
    valori = [12, 7, 19, 7]
    print("valori               :", valori)
    print("statistiche_misure   :", statistiche_misure(valori))
    print("statistiche_misure([]):", statistiche_misure([]))
    print("media                :", media(valori))
    print("media([])            :", media([]))
    print("sopra_media          :", sopra_media(valori), "-> originale:", valori)

    # Controesempio informativo (non richiesto).
    # Il modulo `array` offre una sequenza MUTABILE a tipo omogeneo: ogni
    # elemento deve avere lo stesso tipo dichiarato alla creazione. Non è il
    # modello usato dal corso, che per i vettori usa le liste: qui serve solo
    # a mostrare che in Python esistono anche sequenze con vincolo di tipo.
    import array

    vettore = array.array("i", [12, 7, 19])
    vettore.append(4)
    print()
    print("Controesempio informativo (non richiesto): array.array")
    print("array.array('i', ...) :", list(vettore), "-> solo interi, tipo omogeneo")
    # vettore.append(3.5) -> TypeError: integer argument expected
