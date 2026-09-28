"""Fusione, partizione e i due ordinamenti per divide et impera dell'Unità 11.

Il modulo contiene le **quattro funzioni canoniche** del capitolo PY-15:

| Funzione | Ingresso, risultato ed effetti |
|---|---|
| `fondi_ordinate(sinistra, destra, chiave=None)` | due liste già non decrescenti; restituisce una **nuova** lista; non modifica gli ingressi |
| `merge_sort(valori, chiave=None)` | restituisce una **nuova** lista ordinata; non modifica `valori` |
| `partiziona_lomuto(valori, sinistra, destra, chiave=None)` | intervallo **inclusivo** `[sinistra, destra]` non vuoto; modifica solo quell'intervallo; restituisce l'indice finale del pivot |
| `quick_sort(valori, chiave=None)` | ordina **sul posto** e restituisce `None` |

Le prime due funzioni sono stabili, le altre no: la scelta `<=` sui valori
uguali preserva l'ordine relativo nella fusione, mentre uno scambio della
partizione può invertire due record con la stessa chiave. La stabilità di
`merge_sort` è dichiarata per gli elementi che provengono dalle due metà
consecutive della lista di partenza.

Il parametro `chiave` è quello già incontrato nel cap. PY-14: senza di esso gli
elementi si confrontano fra loro; con esso si confrontano le immagini prodotte
da `chiave`, mentre gli elementi restano interi o record. Una chiave costosa può
essere ricalcolata durante più confronti: le versioni didattiche non la
conservano, a differenza di `sorted`, che la valuta una sola volta per elemento.

Ambiente: CPython sul computer. Nessuna lettura da tastiera, nessuna stampa
all'infuori della guardia in fondo al file.
"""


def _valutatore(chiave):
    """Restituisce la funzione che estrae la chiave di confronto da un elemento."""
    return (lambda elemento: elemento) if chiave is None else chiave


def fondi_ordinate(sinistra, destra, chiave=None):
    """Restituisce la lista nuova che fonde `sinistra` e `destra`, entrambe già ordinate.

    Precondizione: `sinistra` e `destra` sono liste **già non decrescenti**
    secondo la stessa `chiave`. La funzione non modifica gli ingressi e
    restituisce sempre una lista distinta da entrambi, anche quando uno dei due
    è vuoto.

    Procedimento a **due indici**: `j` scorre `sinistra`, `k` scorre `destra`;
    a ogni passo si prende l'elemento con la chiave minore e quando una delle
    due liste si esaurisce il **resto** dell'altra viene copiato in coda senza
    altri confronti.

    Scelta sui valori uguali: si prende l'elemento di **sinistra** (il confronto
    è `<=` fra le chiavi). Se le due liste provengono da metà consecutive della
    stessa lista di partenza, questa regola preserva l'ordine relativo degli
    elementi con la stessa chiave ed è la ragione della stabilità di MergeSort.

    Confronti fra chiavi: al massimo `len(sinistra) + len(destra) - 1` quando
    entrambe le liste non sono vuote, perché ogni confronto colloca almeno un
    elemento e l'ultimo elemento si inserisce senza confronto. Con un lato vuoto
    i confronti sono zero. Spazio ausiliario Θ(a+b) per il risultato.
    """
    valore = _valutatore(chiave)
    risultato = []
    j = 0
    k = 0
    while j < len(sinistra) and k < len(destra):
        if valore(sinistra[j]) <= valore(destra[k]):
            risultato.append(sinistra[j])
            j += 1
        else:
            risultato.append(destra[k])
            k += 1
    risultato.extend(sinistra[j:])
    risultato.extend(destra[k:])
    return risultato


def merge_sort(valori, chiave=None):
    """Restituisce la lista nuova che contiene `valori` in ordine non decrescente.

    `valori` **non** viene modificato e il risultato è sempre una lista distinta,
    anche per zero o un elemento: il caso base `len(valori) <= 1` restituisce la
    copia `list(valori)`.

    Procedimento per **divide et impera**: si divide la lista a metà con lo
    slicing, si ordinano ricorsivamente le due metà e si **fondono** i risultati
    con `fondi_ordinate`, che è stabile. L'albero di divisione di
    `[5, 2, 4, 2]` ha al primo livello `[5, 2]` e `[4, 2]`, poi i quattro
    elementi singoli; le fusioni avvengono nell'ordine inverso della divisione.

    Correttezza per induzione su `n = len(valori)`: per `n <= 1` il risultato è
    già ordinato; per `n >= 2` le due metà hanno meno di `n` elementi, per
    ipotesi induttiva sono restituite ordinate e la fusione di due liste
    ordinate è ordinata. La terminazione è garantita dalla riduzione: ogni
    chiamata ricorsiva riceve una lista più corta, fino al caso base.

    Tempo Θ(n log n) per `n >= 2` nel modello dei confronti e delle copie
    elementari. Spazio ausiliario: picco Θ(n) per il risultato della fusione più
    Θ(log n) per lo stack; le copie complessive lungo l'esecuzione sono
    Θ(n log n), perché ogni livello dell'albero copia tutti gli `n` elementi.

    Versione **stabile**: la regola `<=` di `fondi_ordinate` conserva l'ordine
    relativo degli elementi con la stessa chiave.
    """
    if len(valori) <= 1:
        return list(valori)
    meta = len(valori) // 2
    sinistra = merge_sort(valori[:meta], chiave)
    destra = merge_sort(valori[meta:], chiave)
    return fondi_ordinate(sinistra, destra, chiave)


def partiziona_lomuto(valori, sinistra, destra, chiave=None):
    """Riordina `valori[sinistra:destra+1]` attorno al pivot e ne restituisce l'indice.

    Precondizione: `0 <= sinistra <= destra < len(valori)`, quindi l'intervallo
    `[sinistra, destra]` è **inclusivo** e non vuoto. Vengono modificati soltanto
    gli elementi dell'intervallo; il resto della lista resta identico.

    Il pivot è l'elemento **finale** `valori[destra]`; la sua chiave si valuta
    una sola volta. Ad ogni elemento dell'intervallo, pivot escluso, si chiede
    se la sua chiave è `<=` di quella del pivot: gli elementi con la chiave
    minore o **uguale** confluiscono nella zona di sinistra.

    Invariante, **prima** del confronto sull'indice `j`:

    - `valori[sinistra .. confine]` ha chiave `<= pivot`;
    - `valori[confine + 1 .. j - 1]` ha chiave `> pivot`;
    - `valori[j .. destra - 1]` non è ancora stato esaminato;
    - `valori[destra]` contiene il pivot.

    Dopo l'ultimo confronto il pivot viene scambiato nella posizione
    `confine + 1`, che diventa la sua collocazione **definitiva**: a sinistra gli
    elementi con chiave `<= pivot`, a destra quelli con chiave `> pivot`. Lo
    scambio viene eseguito solo se le due posizioni differiscono, come negli
    ordinamenti del cap. PY-14.

    Gli elementi con chiave uguale a quella del pivot entrano nel lato sinistro:
    la scelta `<=` non rende la partizione stabile e il caso
    `[(2, "a"), (2, "b"), (1, "c")]` ne è il controesempio. Confronti fra chiavi:
    `destra - sinistra`, uno per ogni elemento non pivot. Scambi: al più
    `destra - sinistra + 1`. Spazio ausiliario Θ(1).
    """
    valore = _valutatore(chiave)
    pivot = valori[destra]
    chiave_pivot = valore(pivot)
    confine = sinistra - 1
    for j in range(sinistra, destra):
        if valore(valori[j]) <= chiave_pivot:
            confine += 1
            if confine != j:
                valori[confine], valori[j] = valori[j], valori[confine]
    posizione = confine + 1
    if posizione != destra:
        valori[posizione], valori[destra] = valori[destra], valori[posizione]
    return posizione


def quick_sort(valori, chiave=None):
    """Ordina `valori` sul posto in ordine non decrescente; restituisce `None`.

    Il risultato è la lista di ingresso, modificata: per ottenere una lista
    nuova serve una copia esplicita **prima** della chiamata. Zero o un elemento
    sono già ordinati e non richiedono alcuna partizione.

    Procedimento per **divide et impera senza fase di fusione**: la partizione
    colloca il pivot nella sua posizione definitiva e lascia due sottoproblemi
    indipendenti, `[sinistra, p - 1]` e `[p + 1, destra]`, che **non comprendono
    più il pivot**. Ciascuno viene ordinato con una chiamata ricorsiva su
    estremi inclusivi; non si copiano sottoliste.

    Correttezza per induzione sulla lunghezza dell'intervallo: se l'intervallo
    ha 0 o 1 elemento è già ordinato; altrimenti la partizione fissa il pivot
    nella posizione finale e i due sottointervalli hanno entrambi meno elementi,
    quindi per ipotesi induttiva l'intero intervallo risulta ordinato. La
    terminazione è garantita dalla riduzione: ogni chiamata ricorsiva agisce su
    un intervallo che esclude il pivot.

    Il caso peggiore con pivot finale produce partizioni molto sbilanciate: una
    lista già ordinata, una lista inversa e una lista di soli valori uguali
    riducono l'intervallo di uno solo per chiamata, con profondità Θ(n) dello
    stack e tempo Θ(n²). Con partizioni circa bilanciate la profondità è
    Θ(log n) e il tempo Θ(n log n). Memoria della partizione Θ(1).

    Versione **non stabile**: lo scambio finale può invertire due elementi con
    la stessa chiave.
    """
    _quick_sort_intervallo(valori, 0, len(valori) - 1, chiave)
    return None


def _quick_sort_intervallo(valori, sinistra, destra, chiave):
    """Ordina sul posto `valori[sinistra:destra+1]`; uscita per intervalli di 0 o 1 elemento."""
    if sinistra >= destra:
        return
    p = partiziona_lomuto(valori, sinistra, destra, chiave)
    _quick_sort_intervallo(valori, sinistra, p - 1, chiave)
    _quick_sort_intervallo(valori, p + 1, destra, chiave)


if __name__ == "__main__":
    print("Fusione di due liste ordinate:")
    print(fondi_ordinate([1, 3, 5], [2, 3, 6]))  # [1, 2, 3, 3, 5, 6]

    print("MergeSort non modifica l'ingresso e restituisce una lista nuova:")
    originali = [5, 2, 4, 2]
    ordinati = merge_sort(originali)
    print(originali, ordinati, ordinati is not originali)  # [5, 2, 4, 2] [2, 2, 4, 5] True

    print("Partizione con pivot finale 1c su record marcati:")
    marcati = [(2, "a"), (2, "b"), (1, "c")]
    indice = partiziona_lomuto(marcati, 0, len(marcati) - 1, chiave=lambda r: r[0])
    print(marcati, indice)  # [(1, 'c'), (2, 'b'), (2, 'a')] 0

    print("QuickSort ordina sul posto e restituisce None:")
    valori = [5, 2, 4, 2]
    print(quick_sort(valori), valori)  # None [2, 2, 4, 5]
