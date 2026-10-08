"""Attributi di classe e di istanza; metodi di classe e statici (OOP-03, sez. D ed E).

Il modulo contiene tre esempi autonomi:

1. la coppia `SchedaCondivisa` (deliberatamente difettosa) e `Scheda`:
   un dato di classe è condiviso, un contenitore sulla classe è condiviso
   **anche nelle mutazioni**, e la correzione sposta la creazione della lista
   in `__init__`;
2. la classe `Durata`, con la factory di classe `da_minuti` che costruisce
   attraverso `cls`;
3. il validatore statico `Durata.minuti_validi`, confrontato con la funzione
   pura di modulo `minuti_validi_funzione`.

Contratto di `Durata`: `secondi` intero non booleano non negativo; zero è
valido; negativi, booleani e testo sono rifiutati con `ValueError`.

La variante difettosa è marcata e serve a costruire prove che distinguono
condivisione e indipendenza: non è una versione corretta da riusare.

Ambiente: CPython sul computer. Dipende soltanto dal linguaggio.
"""


class SchedaCondivisa:
    """DELIBERATAMENTE DIFETTOSA: il contenitore vive sulla classe.

    `annotazioni = []` nella classe crea **una sola lista** condivisa da tutte
    le istanze: un `append` eseguito su un'istanza è visibile anche
    dall'altra. La classe serve solo a mostrare il difetto.
    """

    categoria = "generale"
    annotazioni = []

    def __init__(self, titolo):
        self.titolo = titolo


class Scheda:
    """Scheda con dato di classe condiviso e stato proprio per istanza.

    `categoria` è un attributo di classe: un valore condiviso, uguale per
    tutte le istanze finché nessuno lo riassegna. `titolo` e `annotazioni`
    sono attributi di istanza creati in `__init__`: ogni scheda ha il proprio.
    """

    categoria = "generale"

    def __init__(self, titolo):
        self.titolo = titolo
        self.annotazioni = []


def _valida_secondi(secondi):
    """Controlla che `secondi` sia un intero non booleano non negativo."""
    if isinstance(secondi, bool) or not isinstance(secondi, int):
        raise ValueError(f"campo 'secondi': atteso un intero, ricevuto {type(secondi).__name__}")
    if secondi < 0:
        raise ValueError(f"campo 'secondi': atteso un valore non negativo, ricevuto {secondi}")
    return None


def minuti_validi_funzione(minuti):
    """Funzione pura di modulo: dice se `minuti` è nel dominio delle durate.

    Non usa lo stato di nessuna istanza: è il termine di confronto per
    decidere se lo stesso controllo merita di vivere dentro il tipo.
    """
    return isinstance(minuti, int) and not isinstance(minuti, bool) and minuti >= 0


class Durata:
    """Durata espressa in secondi interi non negativi.

    Lo stato è un solo campo; la classe offre una **factory di classe**
    `da_minuti`, che riceve la classe stessa in `cls` e la usa per costruire,
    e il **validatore statico** `minuti_validi`, che non riceve né istanza né
    classe.
    """

    def __init__(self, secondi):
        """Crea la durata dopo la validazione del valore."""
        _valida_secondi(secondi)
        self._secondi = secondi

    @property
    def secondi(self):
        """Valore in secondi, intero non negativo. Sola lettura."""
        return self._secondi

    @classmethod
    def da_minuti(cls, minuti):
        """Costruisce una durata da un numero intero di minuti.

        `cls` è la classe ricevuta dalla chiamata: qui coincide con `Durata`.
        Costruire con `cls(...)` invece di `Durata(...)` è la forma che la
        factory di classe rende disponibile.
        """
        if isinstance(minuti, bool) or not isinstance(minuti, int):
            raise ValueError(f"campo 'minuti': atteso un intero, ricevuto {type(minuti).__name__}")
        if minuti < 0:
            raise ValueError(f"campo 'minuti': atteso un valore non negativo, ricevuto {minuti}")
        return cls(minuti * 60)

    @staticmethod
    def minuti_validi(minuti):
        """Dice se `minuti` è nel dominio delle durate, senza istanze.

        Metodo statico: nessun `self` e nessun `cls`. Sta nel tipo perché
        esprime una regola del dominio di `Durata`, non un calcolo generico.
        """
        return minuti_validi_funzione(minuti)


if __name__ == "__main__":
    prima = Scheda("esercizi")
    seconda = Scheda("ripasso")
    print("categoria condivisa:", prima.categoria, seconda.categoria, Scheda.categoria)

    prima.categoria = "verifica"
    print(
        "dopo il mascheramento:",
        prima.categoria,
        seconda.categoria,
        Scheda.categoria,
    )

    prima.annotazioni.append("ripassare le proprietà")
    print("annotazioni della prima:", prima.annotazioni)
    print("annotazioni della seconda:", seconda.annotazioni)

    difettosa_a = SchedaCondivisa("a")
    difettosa_b = SchedaCondivisa("b")
    difettosa_a.annotazioni.append("oops")
    print("versione difettosa, la seconda vede l'aggiunta:", difettosa_b.annotazioni)

    zero = Durata(0)
    breve = Durata.da_minuti(3)
    print("durata zero:", zero.secondi, "s; da_minuti(3):", breve.secondi, "s")

    print("minuti_validi(3):", Durata.minuti_validi(3))
    print("minuti_validi_funzione(3):", minuti_validi_funzione(3))
    print("minuti_validi(-1):", Durata.minuti_validi(-1))
    print("minuti_validi(True):", Durata.minuti_validi(True))

    for candidato in (-1, True, "90"):
        try:
            Durata(candidato)
        except ValueError as errore:
            print("costruzione rifiutata:", errore)
    try:
        Durata.da_minuti(-5)
    except ValueError as errore:
        print("da_minuti(-5) rifiutata:", errore)
