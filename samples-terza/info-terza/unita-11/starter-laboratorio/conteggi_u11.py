"""Starter del LAB-PY-U11: la strumentazione dei conteggi (fase L3).

Questo file è **incompleto, e lo dichiara**: i quattro corpi sono da completare
nella fase L3 - Traccia e conteggi, dopo che le funzioni di `ordinamenti_u11.py`
sono verificate. La strumentazione è un **rifattorizzazione dichiarata**: si
riprende l'algoritmo già corretto e vi si aggiungono i contatori, senza cambiarne
né il risultato né gli effetti.

Vocabolario degli eventi, esteso dal cap. PY-14 a `<=`:

- **confronto fra chiavi**: valutazione effettiva di un operatore di confronto
  (`<`, `>`, `<=`, `>=`, `==`) fra due chiavi, compresa quella falsa che
  interrompe un ciclo. Se l'operatore non viene valutato, il confronto non si
  conta.
- **scambio**: interversione di due posizioni **diverse** della lista.
- **copia**: assegnamento che scrive un elemento di una sequenza in un'altra
  sequenza o in una nuova posizione della stessa. Comprende le metà prodotte dallo
  slicing, le copie del caso base e le scritture nella lista fusa.
- **profondità massima**: numero massimo di frame ricorsivi contemporaneamente
  attivi, con la chiamata che ordina l'intera lista che vale 1.

Registri restituiti, con lo stesso nome delle chiavi usate dal capitolo:

| Funzione | Registro |
|---|---|
| `fondi_ordinate_con_conteggi` | `{"risultato", "confronti", "copie"}` |
| `merge_sort_con_conteggi` | `{"risultato", "confronti", "copie", "profondita_massima"}` |
| `partiziona_lomuto_con_conteggi` | `{"pivot_finale", "confronti", "scambi"}` |
| `quick_sort_con_conteggi` | `{"confronti", "scambi", "copie", "profondita_massima"}` |

Ogni funzione produce lo **stesso risultato** della controparte senza contatori:
la prova di equivalenza è nei casi L09 e L10 della suite. Le versioni con
contatori **non vanno cronometrate**.

Ambiente: CPython sul computer. Nessuna lettura da tastiera, nessuna stampa.
"""


def _valutatore(chiave):
    """Restituisce la funzione che produce il valore confrontabile di un elemento."""
    return (lambda elemento: elemento) if chiave is None else chiave


def fondi_ordinate_con_conteggi(sinistra, destra, chiave=None):
    """Come `fondi_ordinate`, più il registro dei conteggi.

    Restituisce `{"risultato", "confronti", "copie"}` e non modifica gli ingressi.

    Da completare nella fase L3 - Traccia e conteggi.
    """
    raise NotImplementedError("fase L3: strumentare fondi_ordinate")


def merge_sort_con_conteggi(valori, chiave=None):
    """Come `merge_sort`, più il registro dei conteggi.

    Restituisce `{"risultato", "confronti", "copie", "profondita_massima"}` e non
    modifica `valori`. `copie` comprende anche le metà prodotte dallo slicing e le
    copie del caso base; `profondita_massima` si registra all'ingresso di ogni
    chiamata, comprese quelle con 0 o 1 elemento.

    Da completare nella fase L3 - Traccia e conteggi.
    """
    raise NotImplementedError("fase L3: strumentare merge_sort")


def partiziona_lomuto_con_conteggi(valori, sinistra, destra, chiave=None):
    """Come `partiziona_lomuto`, più il registro dei conteggi.

    Restituisce `{"pivot_finale", "confronti", "scambi"}` e modifica in posto
    l'intervallo `[sinistra, destra]`. I confronti sono `destra - sinistra`, uno
    per ogni elemento non pivot.

    Da completare nella fase L3 - Traccia e conteggi.
    """
    raise NotImplementedError("fase L3: strumentare partiziona_lomuto")


def quick_sort_con_conteggi(valori, chiave=None):
    """Come `quick_sort`, più il registro dei conteggi.

    Restituisce `{"confronti", "scambi", "copie", "profondita_massima"}` e ordina
    `valori` sul posto. `copie` resta zero: la partizione canonica scambia
    posizioni della stessa lista e non costruisce sequenze nuove.

    Da completare nella fase L3 - Traccia e conteggi.
    """
    raise NotImplementedError("fase L3: strumentare quick_sort")


def confronti_massimi_fusione(a, b):
    """Restituisce il limite superiore dei confronti per fondere liste di `a` e `b` elementi.

    Questa funzione è **fornita completa**: con entrambe le liste non vuote i
    confronti sono al più `a + b - 1`, con un lato vuoto sono zero. Il valore è
    un **limite**, non un risultato atteso: si controlla a mano su `a = b = 1`,
    su `a = 1, b = 0` e su due liste interlacciate prima di usarlo per leggere i
    registri misurati.
    """
    if a < 0 or b < 0:
        raise ValueError("le lunghezze non possono essere negative")
    return 0 if a == 0 or b == 0 else a + b - 1


def copie_attese_merge_sort(n):
    """Restituisce il numero esatto di copie elementari di `merge_sort` su `n` elementi.

    Questa funzione è **fornita completa** e segue la stessa struttura ricorsiva
    del codice: ogni chiamata su `n >= 2` elementi copia `n` elementi nelle due
    metà e `n` nel risultato della fusione, più le copie delle chiamate
    ricorsive; il caso base copia i suoi 0 o 1 elementi. Per `n` potenza di due
    il valore coincide con `2n·log2(n) + n`: `n = 1` dà 1, `n = 2` dà 6, `n = 4`
    dà 20. Le copie totali crescono come Θ(n log n), mentre la memoria occupata
    contemporaneamente resta Θ(n).
    """
    if n < 0:
        raise ValueError("il numero di elementi non può essere negativo")
    if n <= 1:
        return n
    meta = n // 2
    return 2 * n + copie_attese_merge_sort(meta) + copie_attese_merge_sort(n - meta)


if __name__ == "__main__":
    print("Starter del LAB-PY-U11: i contatori sono da completare in fase L3.")
    print("Formule fornite: fusione(3, 3) ->", confronti_massimi_fusione(3, 3))
    print("Formule fornite: copie merge_sort(4) ->", copie_attese_merge_sort(4))
