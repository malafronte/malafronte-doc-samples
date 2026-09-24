"""Analizzatore di misure e di testi: versione di partenza del laboratorio LAB-PY-U7.

Stato iniziale dichiarato: il modulo contiene le COSTANTI di lavoro e tutte
le FIRME richieste dalle istruzioni, con il proprio docstring. Una sola
funzione è già completa, `presenta`: la prima esecuzione della suite di
test ha quindi un caso verde e tutti gli altri rossi. Ogni altra funzione
chiude con `NotImplementedError` e segnala la fase alla quale va affrontata.

Il percorso è quello delle fasi L1-L5: stringhe, presentazione, statistiche
sulle misure, liste, matrici. Non scrivere corpi finti e non sostituire un
TODO con un risultato calcolato a mano: il contratto del docstring è la
specifica, il corpo è il lavoro da svolgere.

Regole del laboratorio: niente dizionari, niente insiemi, niente file, niente
espressioni regolari e niente classi. Le funzioni NON chiedono input e NON
stampano: leggono gli argomenti, restituiscono un risultato e basta. Le
uniche stampe del file stanno nel main protetto dalla guardia di avvio.

Esecuzione dei test: uv run pytest -q test_analizzatore_u7.py
Esecuzione del promemoria: uv run python analizzatore_u7.py
"""

TESTO_TECNICO = (
    "Il sensore misura la corrente in microampere e invia i dati "
    "alla scheda; la scheda salva i valori e mostra la media "
    "delle misure del sensore."
)

MISURE_UA = [12, 7, 19, 7, 4]

PROVE_SENSORI = [[2, 4], [6, 8], [10, 12]]


# ---------------------------------------------------------------------------
# Fase L1 — Stringhe: normalizzazione e tokenizzazione
# ---------------------------------------------------------------------------


def normalizza(testo: str) -> str:
    """Restituisce la forma normalizzata del `testo` ricevuto.

    Riceve una stringa `testo`, in genere con spazi esterni e spazi interni
    ripetuti. Restituisce una NUOVA stringa con gli spazi esterni eliminati,
    le sequenze di spazi interne ridotte a un singolo spazio e tutte le
    lettere in forma minuscola.

    L'argomento non viene modificato: le stringhe sono immutabili e il
    valore ricevuto resta disponibile nella sua forma originale. Per testo
    vuoto, oppure composto dai soli spazi, il risultato è `""`.
    """
    # TODO (fase L1): decidere in quale ordine comporre le operazioni di
    # pulizia e quale caso limite verificare per primo.
    raise NotImplementedError("da completare")


def tokenizza(testo: str) -> list[str]:
    """Restituisce le parole del `testo`, separate dagli spazi.

    Riceve la stringa `testo` e ne restituisce l'elenco delle parole. Gli
    spazi, le tabulazioni e gli a capo agiscono da separatori e le
    sequenze ripetute NON producono elementi vuoti. Restituisce una NUOVA
    lista di stringhe; l'argomento non viene modificato. Per testo vuoto il
    risultato è `[]`.

    La punteggiatura resta attaccata alle parole: la separazione della
    punteggiatura non è richiesta a questo livello.
    """
    # TODO (fase L1): scegliere la forma di suddivisione che elimina gli
    # elementi vuoti e verificare il comportamento sul testo vuoto.
    raise NotImplementedError("da completare")


# ---------------------------------------------------------------------------
# Fase L2 — Presentazione (fornita completa, come riferimento)
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Fase L3 — Scansioni sulle misure: statistiche e selezione
# ---------------------------------------------------------------------------


def statistiche_misure(valori: list[int]) -> tuple[int, int, int] | None:
    """Restituisce somma, minimo e massimo di `valori` come tupla, oppure `None`.

    Riceve la lista `valori` e restituisce la tupla `(somma, minimo,
    massimo)`. L'argomento non viene modificato. Per lista vuota il
    risultato è `None`: somma, minimo e massimo di zero elementi non sono
    definiti e il caso mancato non va confuso con un dato uguale a 0.
    Chi chiama controlla `None` prima di usare la tupla.

    La lista ricevuta resta nell'ordine di partenza; nessuna funzione di
    questo modulo la riordina.
    """
    # TODO (fase L3): scegliere gli accumulatori della scansione e il valore
    # da cui farli partire, distinguendo il primo elemento dagli altri.
    raise NotImplementedError("da completare")


def sopra_media_misure(valori: list[int]) -> list[int]:
    """Restituisce i valori strettamente superiori alla media, nell'ordine di partenza.

    Riceve la lista `valori`. La media si calcola su TUTTI gli elementi e
    NON viene arrotondata; la selezione tiene gli elementi strettamente
    maggiori della media. Il risultato è una lista NUOVA che conserva
    l'ordine di comparizione e anche i duplicati. L'argomento non viene
    modificato. Per lista vuota il risultato è `[]`.

    Con `[12, 7, 19, 7]` la media è 11.25 e il risultato atteso è
    `[12, 19]`.
    """
    # TODO (fase L3): decidere quanti passaggi servono e perché la media va
    # nota prima di ogni confronto.
    raise NotImplementedError("da completare")


# ---------------------------------------------------------------------------
# Fase L4 — Liste: copia, inversione ed effetti sul parametro
# ---------------------------------------------------------------------------


def copia_inverti(valori: list[int]) -> list[int]:
    """Restituisce una nuova lista con gli elementi di `valori` in ordine inverso.

    Riceve la lista `valori` e ne restituisce una copia invertita. L'elenco
    di partenza NON viene modificato: il risultato è una lista NUOVA, con
    gli stessi elementi in ordine opposto. Per lista vuota il risultato è
    una lista vuota nuova.

    La firma `-> list[int]` indica che qui serve un risultato: sono ammesse
    più costruzioni, purché l'argomento resti intatto.
    """
    # TODO (fase L4): scegliere la costruzione della lista inversa e
    # verificare che l'argomento non venga toccato.
    raise NotImplementedError("da completare")


def inverti_sul_posto(valori: list[int]) -> None:
    """Inverte l'ordine degli elementi di `valori` sul posto e non restituisce nulla.

    Riceve la lista `valori` e la MODIFICA in loco: la lista è la stessa di
    prima, con gli elementi in ordine opposto. Le alias della lista
    osservano subito l'inversione. Il risultato è `None`. Per lista vuota,
    e per lista di un solo elemento, non accade nulla.

    La firma `-> None` segnala che la funzione non restituisce la lista
    aggiornata: assegnare il risultato della chiamata a `valori`
    metterebbe `None` nella variabile.
    """
    # TODO (fase L4): decidere quale effetto produrre e dove, distinguendo
    # la modifica della lista dal rimando a una lista diversa.
    raise NotImplementedError("da completare")


# ---------------------------------------------------------------------------
# Fase L5 — Matrici: somme e trasposizione
# ---------------------------------------------------------------------------


def somme_per_riga(matrice: list[list[int]]) -> list[int]:
    """Restituisce l'elenco delle somme, una per ogni riga della `matrice`.

    Riceve la `matrice` rettangolare come lista di liste e costruisce una
    lista NUOVA con la somma di ogni riga, nello stesso ordine delle righe.
    Non modifica l'argomento. Per matrice vuota il risultato è `[]`; per
    matrice con righe vuote la lista contiene uno 0 per ogni riga.

    La lunghezza del risultato è pari al numero di righe.
    """
    # TODO (fase L5): scegliere come percorrere la matrice e quale somma
    # parziale raccogliere a ogni riga.
    raise NotImplementedError("da completare")


def somme_per_colonna(matrice: list[list[int]]) -> list[int]:
    """Restituisce l'elenco delle somme, una per ogni colonna della `matrice`.

    Riceve la `matrice` rettangolare come lista di liste e costruisce una
    lista NUOVA con la somma di ogni colonna, nell'ordine delle colonne.
    Non modifica l'argomento. Per matrice vuota il risultato è `[]`; per
    matrice con righe vuote il risultato è `[]`, perché non ci sono colonne.

    La lunghezza del risultato è pari al numero di colonne, NON a quello
    delle righe.
    """
    # TODO (fase L5): decidere quale indice percorrere dall'esterno e quale
    # dall'interno, e come ricavare il numero di colonne.
    raise NotImplementedError("da completare")


def trasponi(matrice: list[list[int]]) -> list[list[int]]:
    """Restituisce la trasposta della `matrice`, in una struttura nuova e indipendente.

    Riceve la `matrice` rettangolare e ne costruisce la trasposta: la
    colonna `j` dell'originale diventa la riga `j` del risultato, quindi
    una matrice `righe` x `colonne` dà una matrice `colonne` x `righe`.
    Ogni riga del risultato è una lista NUOVA: l'argomento non viene
    modificato e nessuna riga è condivisa con esso.

    Per matrice vuota il risultato è `[]`. Per matrice di una sola riga
    (1xN) il risultato è una matrice di N righe di un solo elemento (Nx1).
    """
    # TODO (fase L5): decidere quale dei due indici diventa quello esterno
    # del risultato e come costruire righe indipendenti.
    raise NotImplementedError("da completare")


if __name__ == "__main__":
    print("Laboratorio LAB-PY-U7: analizzatore di misure e di testi.")
    print("Le funzioni di questo modulo sono da completare.")
    print("Le costanti di lavoro sono già disponibili:")
    print("  TESTO_TECNICO:", TESTO_TECNICO)
    print("  MISURE_UA    :", MISURE_UA)
    print("  PROVE_SENSORI:", PROVE_SENSORI)
    print("Eseguire la suite di test per vedere quali funzioni mancano:")
    print("  uv run pytest -q test_analizzatore_u7.py")
