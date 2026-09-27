"""Record, criteri di ordinamento e forme idiomatiche dell'Unità 10.

Il modulo applica gli ordinamenti elementari a una **lista di record**, ovvero
di dizionari con gli stessi campi, e confronta il procedimento esplicito con le
forme standard `sorted` e `list.sort`. I record sono quelli del registro
sintetico già usato nelle unità precedenti: `codice` stringa con zeri iniziali
significativi, `destinazione` fra `locale` e `nazionale`, `totale_cent` intero
in centesimi.

Ambiente: CPython sul computer. Nessuna lettura da tastiera, nessuna stampa.

Qui non compaiono le funzioni della tappa autonoma del progetto progressivo:
quella tappa va progettata dallo studente e il corso non ne pubblica una
soluzione integrale.
"""


def registro_di_esempio():
    """Restituisce una lista nuova di record del registro sintetico.

    Gli importi sono in centesimi. I codici sono stringhe: `"007"` e `"7"` sono
    codici diversi e gli zeri iniziali non si perdono convertendo in intero. La
    lista è nuova a ogni chiamata, così ogni esempio parte da uno stato noto.
    """
    return [
        {"codice": "012", "destinazione": "locale", "totale_cent": 450},
        {"codice": "007", "destinazione": "nazionale", "totale_cent": 1200},
        {"codice": "009", "destinazione": "locale", "totale_cent": 450},
        {"codice": "003", "destinazione": "locale", "totale_cent": 200},
        {"codice": "011", "destinazione": "nazionale", "totale_cent": 450},
    ]


# ---------------------------------------------------------------------------
# Ordinamento di record con una funzione chiave
# ---------------------------------------------------------------------------


def insertion_sort_chiave(valori, chiave):
    """Ordina `valori` sul posto secondo `chiave`; restituisce `None`.

    `chiave` è una funzione che a un record associa il valore confrontabile da
    usare nell'ordinamento, per esempio `lambda record: record["totale_cent"]`.
    I record vengono spostati **interi**: nessun campo si separa dagli altri.

    La stabilità è la stessa di `insertion_sort`: si spostano soltanto i record
    con chiave strettamente maggiore, quindi due record con la stessa chiave
    conservano l'ordine relativo di ingresso.
    """
    for indice in range(1, len(valori)):
        record = valori[indice]
        valore_chiave = chiave(record)
        posizione = indice - 1
        while posizione >= 0 and chiave(valori[posizione]) > valore_chiave:
            valori[posizione + 1] = valori[posizione]
            posizione -= 1
        valori[posizione + 1] = record
    return None


def selection_sort_chiave(valori, chiave):
    """Ordina `valori` sul posto secondo `chiave`; restituisce `None`.

    Stesso effetto di `selection_sort`: versione standard **non stabile**. Due
    record con la stessa chiave possono invertire l'ordine relativo a causa
    dello scambio fra la posizione corrente e la posizione del minimo.
    """
    n = len(valori)
    for indice in range(n - 1):
        minimo = indice
        for j in range(indice + 1, n):
            if chiave(valori[j]) < chiave(valori[minimo]):
                minimo = j
        if minimo != indice:
            valori[indice], valori[minimo] = valori[minimo], valori[indice]
    return None


def bubble_sort_chiave(valori, chiave):
    """Ordina `valori` sul posto secondo `chiave`; restituisce `None`.

    Versione stabile a passaggi fissi, come `bubble_sort`: si scambia solo se
    la chiave di sinistra è strettamente maggiore.
    """
    n = len(valori)
    for passata in range(n - 1):
        for j in range(0, n - 1 - passata):
            if chiave(valori[j]) > chiave(valori[j + 1]):
                valori[j], valori[j + 1] = valori[j + 1], valori[j]
    return None


# ---------------------------------------------------------------------------
# Criteri semplici e criteri composti
# ---------------------------------------------------------------------------


def chiave_totale(record):
    """Restituisce il totale in centesimi del record: criterio semplice."""
    return record["totale_cent"]


def chiave_totale_poi_codice(record):
    """Restituisce la tupla `(totale_cent, codice)`: criterio composto.

    La tupla si confronta componente per componente, da sinistra: prima il
    totale crescente, poi - a totale uguale - il codice crescente. Il codice è
    una stringa, quindi il confronto è **lessicografico**: `"007"` viene prima
    di `"009"` e gli zeri iniziali sono parte del confronto, non rumore da
    eliminare.
    """
    return (record["totale_cent"], record["codice"])


def ordina_per_totale(registro):
    """Restituisce una lista nuova dei record ordinata per totale crescente.

    L'ordinamento usa `insertion_sort_chiave`, quindi è **stabile**: a totale
    uguale resta l'ordine relativo del registro di origine. Il registro ricevuto
    non viene modificato; i record della lista risultante sono gli **stessi
    oggetti** dell'ingresso, non copie: il corso non richiede copie profonde e
    la condivisione dei riferimenti va dichiarata nel contratto.
    """
    vista = list(registro)
    insertion_sort_chiave(vista, chiave_totale)
    return vista


def ordina_per_totale_e_codice(registro):
    """Restituisce una lista nuova ordinata per totale e, a parità, per codice.

    Il criterio composto **non** è la stessa cosa della stabilità su una sola
    chiave: in un ordinamento stabile per totale i record pari conservano
    l'ordine di ingresso, mentre qui a parità di totale si impone l'ordine dei
    codici, che può essere diverso.
    """
    vista = list(registro)
    insertion_sort_chiave(vista, chiave_totale_poi_codice)
    return vista


# ---------------------------------------------------------------------------
# Forme idiomatiche di Python - dopo il procedimento esplicito
# ---------------------------------------------------------------------------


def ordina_per_totale_idiomatico(registro):
    """Stessa funzionalità di `ordina_per_totale` con `sorted`.

    `sorted(iterabile, key=...)` restituisce una **lista nuova** e non modifica
    l'iterabile ricevuto. `lista.sort(...)` agisce invece **sul posto** e
    restituisce `None`: se il risultato della chiamata viene usato come valore,
    quel valore è `None`, non la lista.

    Entrambe le forme standard sono **stabili** nel Python adottato: a chiave
    uguale conservano l'ordine dell'ingresso.
    """
    return sorted(registro, key=chiave_totale)


def totale_decrescente_codice_crescente(registro):
    """Totali decrescenti e, a parità, codici crescenti.

    `reverse=True` inverte l'ordine dell'**intera** chiave e mantiene la
    stabilità per le chiavi uguali: su `key=chiave_totale_poi_codice` produrrebbe
    totali **e** codici decrescenti. Per il criterio misto serve una chiave
    esplicita adatta: qui `(-totale_cent, codice)`, che funziona perché i totali
    sono numerici e l'opposto di un intero inverte il suo ordine. Con chiavi non
    numeriche la stessa tecnica non si applica e serve un confronto dedicato.
    """
    return sorted(registro, key=lambda record: (-record["totale_cent"], record["codice"]))


if __name__ == "__main__":
    # Le viste dello stesso registro non coincidono: la stabilità conserva
    # l'ordine di ingresso dei totali pari, il criterio composto impone il
    # codice crescente. Uscita attesa:
    #   originale  -> 012 007 009 003 011
    #   per totale -> 003 012 009 011 007
    #   totale+cod -> 003 009 011 012 007
    #   reverse    -> 007 012 011 009 003
    registro = registro_di_esempio()
    print("originale  ->", " ".join(r["codice"] for r in registro))
    print("per totale ->", " ".join(r["codice"] for r in ordina_per_totale(registro)))
    print("totale+cod ->", " ".join(r["codice"] for r in ordina_per_totale_e_codice(registro)))
    inverso = sorted(registro, key=chiave_totale_poi_codice, reverse=True)
    print("reverse    ->", " ".join(r["codice"] for r in inverso))
