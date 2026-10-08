"""Eccezione di dominio per una richiesta impossibile (OOP-03, sez. J).

Esempio autonomo su soli scalari già noti: la funzione pura
`richiedi_unita` distingue tre esiti:

1. dati fuori contratto (negativi, booleani, non interi) → `ValueError`;
2. richiesta valida ma **impossibile per lo stato**, cioè `unita > disponibili`
   → `DisponibilitaInsufficiente`, eccezione di dominio;
3. richiesta accettabile → il nuovo valore dei disponibili.

`DisponibilitaInsufficiente` nasce con la minima derivazione da `Exception`:
una classe vuota con un nome di dominio. La scelta del tipo va dichiarata
come anticipazione circoscritta: gerarchie e `super()` arrivano con
l'ereditarietà, nell'Unità 15.

Il controllo non stampa nulla: è il chiamante a presentare l'esito. Nel
chiamante la richiesta fallita compare **dentro** il `try`, come lato destro
di un assegnamento: quando la funzione solleva, l'assegnamento non avviene e
il nome conserva il valore precedente.

Ambiente: CPython sul computer. Dipende soltanto dal linguaggio.
"""


class DisponibilitaInsufficiente(Exception):
    """Richiesta valida ma non soddisfatta dai disponibili attuali."""


def _valida_intero_non_negativo(valore, nome):
    """Controlla che `valore` sia un intero non booleano non negativo."""
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(f"campo '{nome}': atteso un intero, ricevuto {type(valore).__name__}")
    if valore < 0:
        raise ValueError(f"campo '{nome}': atteso un valore non negativo, ricevuto {valore}")
    return None


def _valida_intero_positivo(valore, nome):
    """Controlla che `valore` sia un intero non booleano positivo."""
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(f"campo '{nome}': atteso un intero, ricevuto {type(valore).__name__}")
    if valore <= 0:
        raise ValueError(f"campo '{nome}': atteso un valore positivo, ricevuto {valore}")
    return None


def richiedi_unita(disponibili, unita):
    """Sottrae `unita` da `disponibili` se la richiesta è soddisfatta.

    Dominio: `disponibili` intero non booleano non negativo, `unita` intero
    non booleano positivo. Restituisce `disponibili - unita`. Se `unita`
    supera i disponibili solleva `DisponibilitaInsufficiente`; gli argomenti
    fuori dominio sollevano `ValueError`. Nessuna mutazione: lavora su
    valori ricevuti e restituisce il nuovo valore.
    """
    _valida_intero_non_negativo(disponibili, "disponibili")
    _valida_intero_positivo(unita, "unita")
    if unita > disponibili:
        raise DisponibilitaInsufficiente(f"richieste {unita} unità, disponibili {disponibili}")
    return disponibili - unita


if __name__ == "__main__":
    disponibili = 5
    print("disponibili iniziali:", disponibili)

    disponibili = richiedi_unita(disponibili, 2)
    print("dopo la richiesta di 2:", disponibili)

    try:
        disponibili = richiedi_unita(disponibili, 6)
    except DisponibilitaInsufficiente as errore:
        print("rifiuto:", errore)
    print("disponibili dopo il rifiuto:", disponibili)

    for disponibili_prova, unita_prova in ((5, 0), (5, -1), (5, True), ("5", 1)):
        try:
            richiedi_unita(disponibili_prova, unita_prova)
        except ValueError as errore:
            print("dato fuori contratto:", errore)
