"""Starter del LAB-PY-U10 - Ordinare, contare e misurare: gli ordinamenti.

Questo file è **incompleto, e lo dichiara**: contiene firme, docstring e
contratti, mentre i corpi delle quattro funzioni sono da completare nella fase
L2 e lo dichiarano con un `NotImplementedError` che nomina la fase del
laboratorio. Il primo esito atteso della suite è una serie di fallimenti chiari
sui corpi mancanti, mai un difetto della copia.

Ambiente: CPython sul computer, raccolta `raccolta-programmi`, esecuzione con
`uv run python programmi/ordinamenti_u10.py` dalla root della raccolta.

Tutte e quattro le funzioni condividono lo **stesso contratto** del cap. PY-14:
ricevono una `list`, la ordinano sul posto in ordine non decrescente e
restituiscono `None`. Le quattro implementazioni restano separate, con nomi
espliciti: non si uniscono in una sola funzione parametrizzata.

Il parametro opzionale `chiave` è quello già incontrato nel cap. PY-14, parte
III: senza di esso gli elementi si confrontano fra loro; con esso si confrontano
le immagini prodotte da `chiave`, mentre gli elementi restano interi. Serve per
verificare la stabilità su record marcati, dove la chiave è un solo campo.

Le funzioni non leggono da tastiera e non stampano: il messaggio di avvio sta
nella guardia in fondo al file.
"""


def insertion_sort(valori, chiave=None):
    """Ordina `valori` sul posto con l'inserimento diretto; restituisce `None`.

    Invariante: dopo l'iterazione `i` il prefisso `valori[0:i+1]` è ordinato e
    contiene gli stessi elementi che aveva all'inizio. Salvo la chiave,
    spostare a destra soltanto gli elementi **strettamente maggiori**, poi
    scrivere la chiave nella posizione liberata.

    Versione stabile: l'uguaglianza non provoca spostamenti.

    Da completare nella fase L2 - Implementazioni.
    """
    raise NotImplementedError("fase L2: completare il corpo di insertion_sort")


def selection_sort(valori, chiave=None):
    """Ordina `valori` sul posto col minimo del suffisso; restituisce `None`.

    Invariante: dopo l'iterazione `i` il prefisso `valori[0:i+1]` contiene i
    `i+1` valori più piccoli dell'intera lista. Cercare il minimo del suffisso
    e scambiarlo con la posizione corrente **solo se diverso**.

    Versione standard **non stabile**: lo scambio può invertire due elementi
    con la stessa chiave.

    Da completare nella fase L2 - Implementazioni.
    """
    raise NotImplementedError("fase L2: completare il corpo di selection_sort")


def bubble_sort(valori, chiave=None):
    """Ordina `valori` sul posto con passaggi fissi; restituisce `None`.

    `n - 1` passate; ad ogni coppia adiacente si scambia solo se la chiave di
    sinistra è **strettamente maggiore**. Una sola passata non completa
    l'ordinamento.

    Versione stabile.

    Da completare nella fase L2 - Implementazioni.
    """
    raise NotImplementedError("fase L2: completare il corpo di bubble_sort")


def bubble_sort_ottimizzato(valori, chiave=None):
    """Come `bubble_sort`, con la zona ridotta e l'arresto; restituisce `None`.

    Due effetti distinti: la zona esaminata si restringe a ogni passata e il
    ciclo si interrompe quando una passata **non compie alcuno scambio**. La
    condizione di arresto è «nessuno scambio nell'intera passata».

    Versione stabile.

    Da completare nella fase L2 - Implementazioni.
    """
    raise NotImplementedError("fase L2: completare il corpo di bubble_sort_ottimizzato")


if __name__ == "__main__":
    print("Starter del LAB-PY-U10: i corpi sono da completare nelle fasi indicate.")
