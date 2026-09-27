"""Starter del LAB-PY-U10: la strumentazione dei conteggi (fase L4).

Questo file è **incompleto, e lo dichiara**: i quattro corpi sono da completare
nella fase L4 - Strumentazione, dopo che le funzioni di `ordinamenti_u10.py`
sono verificate. La strumentazione è un **rifattorizzazione dichiarata**: si
riprende l'algoritmo già corretto e vi si aggiungono i contatori, senza cambiarne
né il risultato né gli effetti.

Vocabolario degli eventi, identico a quello del cap. PY-14:

- **confronto fra chiavi**: valutazione effettiva di `>` o `<` fra due chiavi.
  Se l'operatore non viene valutato, il confronto non si conta.
- **scambio**: interversione di due posizioni della lista.
- **spostamento**: assegnamento che trasla di una posizione un elemento
  durante l'inserimento.

Ogni funzione restituisce un dizionario con le sole chiavi `confronti`,
`scambi` e `spostamenti` e ordina la lista **esattamente** come la controparte
senza contatori. La prova di equivalenza è fra i casi L05, L09 e L10 della
suite: prima si verifica che il risultato coincide, poi si leggono i numeri.

Ambiente: CPython sul computer. Nessuna lettura da tastiera, nessuna stampa.
"""


def insertion_sort_con_conteggi(valori, chiave=None):
    """Come `insertion_sort`, più il registro dei conteggi.

    Restituisce `{"confronti", "scambi", "spostamenti"}` e ordina sul posto.
    Insertion sort sposta e poi scrive la chiave: gli `scambi` sono zero per
    costruzione e i `spostamenti` contano le traslazioni. Il parametro `chiave`
    ha lo stesso significato di `ordinamenti_u10.py`.

    Da completare nella fase L4 - Strumentazione.
    """
    raise NotImplementedError("fase L4: strumentare insertion_sort")


def selection_sort_con_conteggi(valori, chiave=None):
    """Come `selection_sort`, più il registro dei conteggi.

    Restituisce `{"confronti", "scambi", "spostamenti"}` e ordina sul posto. Il
    numero di confronti è fisso per ogni disposizione di `n` elementi:
    `n(n-1)/2`. Le assegnazioni `minimo = j` non sono né confronti né scambi.

    Da completare nella fase L4 - Strumentazione.
    """
    raise NotImplementedError("fase L4: strumentare selection_sort")


def bubble_sort_con_conteggi(valori, chiave=None):
    """Come `bubble_sort`, più il registro dei conteggi.

    Restituisce `{"confronti", "scambi", "spostamenti"}` e ordina sul posto. Le
    passate sono fisse: `n(n-1)/2` confronti per ogni disposizione, compresa la
    lista già ordinata. Gli `spostamenti` sono zero.

    Da completare nella fase L4 - Strumentazione.
    """
    raise NotImplementedError("fase L4: strumentare bubble_sort")


def bubble_sort_ottimizzato_con_conteggi(valori, chiave=None):
    """Come `bubble_sort_ottimizzato`, più il registro dei conteggi.

    Restituisce `{"confronti", "scambi", "spostamenti"}` e ordina sul posto. Sul
    già ordinato il conteggio è `n-1` confronti per `n >= 1` e zero scambi; sul
    caso peggiore è `n(n-1)/2`.

    Da completare nella fase L4 - Strumentazione.
    """
    raise NotImplementedError("fase L4: strumentare bubble_sort_ottimizzato")


def formule_attese(n):
    """Restituisce i conteggi attesi per una lista di `n` elementi.

    Questa funzione è **fornita completa**: le formule sono quelle del cap.
    PY-14 e si controllano a mano su `n = 0, 1, 2, 4` prima di usarle per
    leggere i registri misurati.

    | Procedimento | Confronti | Dove |
    |---|---|---|
    | selection sort | `n(n-1)/2` | ogni disposizione |
    | bubble semplice | `n(n-1)/2` | ogni disposizione |
    | bubble ottimizzato, già ordinato | `n-1` per `n >= 1` | solo il caso ordinato |
    | insertion, già ordinato | `n-1` per `n >= 1` | solo il caso ordinato |
    | insertion, inverso | `n(n-1)/2` | solo il caso inverso |
    """
    return {
        "triangolare": n * (n - 1) // 2,
        "lineare_ordinato": max(0, n - 1),
    }


if __name__ == "__main__":
    print("Starter del LAB-PY-U10: i contatori sono da completare nella fase L4.")
