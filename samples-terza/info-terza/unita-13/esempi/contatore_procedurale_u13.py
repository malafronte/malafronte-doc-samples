"""Contatore di eventi procedurale: materiale storico su record e funzioni.

OOP-01 usa ora `orologio_procedurale_u13.py` come esempio introduttivo.
Questo modulo conserva la **buona soluzione procedurale** confrontata nel
capitolo OOP-01: un record-dizionario con un solo campo e quattro funzioni che
lo leggono e lo aggiornano secondo un contratto esplicito. Non è una soluzione
"sbagliata": è una soluzione corretta, utile per confrontare funzioni su
record e operazioni associate alle istanze di una classe.

Dominio del contatore di eventi: una **quantità intera non negativa** che
conta gli eventi registrati. Operazioni ammesse: incremento di una quantità
non negativa, osservazione del valore corrente, azzeramento.

Schema del record (un solo campo):

| Campo | Tipo | Regola |
|---|---|---|
| `valore` | `int` | intero non booleano maggiore o uguale a zero |

Invariante dell'entità: `valore >= 0`. La precondizione della singola
operazione è più circoscritta dell'invariante: `incrementa` richiede una
quantità intera non negativa, mentre l'invariante descrive lo stato che deve
restare vero **dopo ogni operazione riuscita**.

Politica d'errore: una quantità fuori contratto solleva `ValueError` motivato
**prima** di qualunque aggiornamento; il record ricevuto non viene mai
modificato da un'operazione che rifiuta.

Ambiente: CPython sul computer. Dipende soltanto dal linguaggio.
"""

# Invariante dell'entità, enunciato una sola volta e richiamato dalle
# funzioni: il valore contato non scende mai sotto lo zero.
MINIMO_VALORE = 0


def _valida_quantita(quantita):
    """Controlla che `quantita` sia un intero non booleano non negativo.

    È la **precondizione** delle operazioni di incremento: si controlla prima
    di toccare il record, così un rifiuto lascia lo stato precedente intatto.
    """
    if isinstance(quantita, bool) or not isinstance(quantita, int):
        raise ValueError(
            f"quantita: atteso un intero, ricevuto {type(quantita).__name__}"
        )
    if quantita < MINIMO_VALORE:
        raise ValueError(
            f"quantita: atteso un valore maggiore o uguale a {MINIMO_VALORE}, "
            f"ricevuto {quantita}"
        )
    return None


def nuovo_contatore(valore_iniziale=0):
    """Restituisce un record nuovo che soddisfa l'invariante.

    `valore_iniziale` è un intero non booleano non negativo: un valore fuori
    contratto solleva `ValueError` e non produce alcun record. Il risultato è
    un dizionario nuovo: due chiamate producono due record distinti.
    """
    _valida_quantita(valore_iniziale)
    return {"valore": valore_iniziale}


def incrementa(contatore, quantita):
    """Aggiunge `quantita` al valore del contatore. Nessun risultato.

    L'ordine delle operazioni è parte del contratto: prima si controlla la
    quantità, poi si calcola il candidato e solo alla fine si aggiorna il
    campo. Un rifiuto lascia `contatore` interamente invariato.
    """
    _valida_quantita(quantita)
    candidato = contatore["valore"] + quantita
    contatore["valore"] = candidato
    return None


def leggi(contatore):
    """Restituisce il valore corrente del contatore. Nessuna modifica."""
    return contatore["valore"]


def azzera(contatore):
    """Riporta il valore del contatore a zero. Nessun risultato.

    L'azzeramento è un'operazione valida del dominio: non segnala un errore e
    non dipende dal valore precedente, che comunque rispetta l'invariante.
    """
    contatore["valore"] = MINIMO_VALORE
    return None


def descrivi(contatore):
    """Restituisce la riga di presentazione del contatore. Non stampa."""
    return f"eventi registrati: {contatore['valore']}"


if __name__ == "__main__":
    # Trascrizione della traccia del capitolo OOP-01, sez. B: due record
    # distinti, incrementi intercalati e azzeramento.
    primo = nuovo_contatore(0)
    secondo = nuovo_contatore(0)
    incrementa(primo, 3)
    incrementa(secondo, 1)
    incrementa(primo, 2)
    print("primo: ", descrivi(primo))
    print("secondo:", descrivi(secondo))
    azzera(primo)
    print("primo dopo l'azzeramento:", descrivi(primo))
    print("secondo invariato:       ", descrivi(secondo))
    try:
        incrementa(primo, -1)
    except ValueError as errore:
        print("rifiuto:", errore)
    print("primo dopo il rifiuto:", descrivi(primo))
