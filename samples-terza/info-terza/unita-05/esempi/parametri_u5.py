"""Funzioni canoniche sui parametri ed effetti (cap. PY-08, sez. A ed E).

Collocare il file in `programmi/parametri_u5.py`.
Importare il modulo non produce input né output: contiene soltanto definizioni.
Le firme annotate usano le forme composte introdotte nel cap. PY-08 F.
"""


def sostituisci_locale(valori: list[int]) -> None:
    """Esempio di meccanismo: riassegna il parametro a [99].

    Il chiamante non osserva alcun cambiamento: l'assegnamento cambia la
    sola associazione locale. Restituisce None.
    """
    valori = [99]
    return None


def aggiungi_in_posto(valori: list[int], valore: int) -> None:
    """Aggiunge valore in fondo alla lista ricevuta, modificandola.

    Dominio: lista di interi, lista vuota compresa. Effetto: la lista
    ricevuta cambia, il chiamante lo osserva attraverso i propri nomi.
    Restituisce None. Nessun input, nessuna stampa.
    """
    valori.append(valore)
    return None


def con_aggiunta(valori: list[int], valore: int) -> list[int]:
    """Restituisce una nuova lista con valore aggiunto in fondo.

    Dominio: lista di interi, lista vuota compresa. L'argomento ricevuto
    resta invariato; il risultato è una lista nuova, non lo stesso oggetto.
    Nessun input, nessuna stampa.
    """
    risultato = valori.copy()
    risultato.append(valore)
    return risultato


def riepilogo(valori: list[int]) -> tuple[int, int]:
    """Restituisce (numero_elementi, totale) della lista ricevuta.

    Dominio: lista di interi, anche negativi, lista vuota compresa: per []
    il risultato è (0, 0). L'argomento ricevuto resta invariato.
    Nessun input, nessuna stampa.
    """
    totale = 0
    for valore in valori:
        totale = totale + valore
    return len(valori), totale


def raccogli(valore: int, valori: list[int] | None = None) -> list[int]:
    """Aggiunge valore a valori e restituisce la lista.

    Con argomento omesso o None: crea una lista nuova per quella chiamata,
    vi aggiunge il valore e la restituisce; ogni chiamata ottiene una lista
    indipendente. Con lista fornita: la modifica e restituisce proprio
    quella lista. Nessun input, nessuna stampa.
    """
    if valori is None:
        valori = []
    valori.append(valore)
    return valori


def scambia(a: int, b: int) -> tuple[int, int]:
    """Restituisce (b, a), senza modificare i nomi del chiamante.

    Il chiamante decide se spacchettare il risultato nei propri nomi con
    a, b = scambia(a, b). Nessun input, nessuna stampa.
    """
    return b, a
