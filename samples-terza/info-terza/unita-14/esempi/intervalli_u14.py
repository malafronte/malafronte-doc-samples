"""L'intervallo di tempo come valore frozen (OOP-03, sez. H; OOP-04, sez. D).

Una giornata inizia a mezzanotte e ogni istante è rappresentato dai **minuti
trascorsi da mezzanotte**: le 9:00 sono 540, le 10:30 sono 630, la fine
giornata è 1440. L'intervallo `[540, 600)` occupa l'aula dalle 9:00 alle
10:00.

L'intervallo è **semiaperto**: l'estremo iniziale appartiene all'intervallo,
quello finale no. Due intervalli che si toccano in un punto, come `[540, 600)`
e `[600, 660)`, non condividono nessun minuto e possono occupare la stessa
aula. Il valore `1440` è ammesso solo come confine finale: rappresenta la
fine giornata, non un orario di inizio.

Contratto del valore:

| Campo | Regola |
|---|---|
| `inizio_min` | intero non booleano, `0 <= inizio_min` |
| `fine_min` | intero non booleano, `inizio_min < fine_min <= 1440` |
| `durata_min` | proprietà derivata `fine_min - inizio_min`, non memorizzata |

`sovrapposto_a` decide se due intervalli condividono almeno un minuto. La
condizione si ricava per casi (OOP-04, sez. D): gli intervalli `[a, b)` e
`[c, d)` sono separati quando `b <= c` oppure `d <= a`; negando i due casi
si ottiene la forma compatta `a < d and c < b`, simmetrica nei due operandi.

Il confronto riguarda **solo il tempo**: se due occupazioni riguardano aule
diverse non sono in conflitto, anche con gli stessi minuti. La combinazione
aula + tempo appartiene a `Prenotazione`, non a questo valore.

Ambiente: CPython sul computer. Dipende soltanto dal linguaggio.
"""

from dataclasses import dataclass


def _valida_minuto(valore, nome):
    """Controlla che `valore` sia un intero non booleano compreso in [0, 1440]."""
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(f"campo '{nome}': atteso un intero, ricevuto {type(valore).__name__}")
    if valore < 0 or valore > 1440:
        raise ValueError(f"campo '{nome}': atteso un valore fra 0 e 1440 minuti, ricevuto {valore}")
    return None


@dataclass(frozen=True)
class Intervallo:
    """Finestra temporale semiaperta `[inizio_min, fine_min)` di una giornata.

    Valore frozen: gli assegnamenti dei campi sono bloccati e i contenuti
    sono due interi immutabili. La validazione avviene in `__post_init__`,
    alla costruzione: un intervallo invalido non esiste come oggetto e non
    arriva mai agli algoritmi come caso ordinario.
    """

    inizio_min: int
    fine_min: int

    def __post_init__(self):
        _valida_minuto(self.inizio_min, "inizio_min")
        _valida_minuto(self.fine_min, "fine_min")
        if self.inizio_min >= self.fine_min:
            raise ValueError(
                f"coppia (inizio_min, fine_min): atteso inizio_min < fine_min, "
                f"ricevuti ({self.inizio_min}, {self.fine_min})"
            )

    @property
    def durata_min(self):
        """Durata in minuti: `fine_min - inizio_min`, sempre positiva."""
        return self.fine_min - self.inizio_min

    def sovrapposto_a(self, altro):
        """Restituisce `True` se i due intervalli condividono almeno un minuto.

        Contratto: `altro` è un `Intervallo` valido. Il confronto è simmetrico:
        `a.sovrapposto_a(b) == b.sovrapposto_a(a)`. L'adiacenza esatta
        (`fine` di uno uguale a `inizio` dell'altro) **non** è sovrapposizione.
        """
        return self.inizio_min < altro.fine_min and altro.inizio_min < self.fine_min


if __name__ == "__main__":
    prima_ora = Intervallo(540, 600)
    adiacente = Intervallo(600, 660)
    parziale = Intervallo(570, 630)
    contenuto = Intervallo(550, 560)
    confine = Intervallo(1439, 1440)

    print("9:00-10:00, durata:", prima_ora.durata_min, "minuti")
    print("con confine di fine giornata:", confine, "durata:", confine.durata_min)

    print("[540,600) vs [600,660):", prima_ora.sovrapposto_a(adiacente))
    print("[540,600) vs [570,630):", prima_ora.sovrapposto_a(parziale))
    print("[540,600) vs [550,560):", prima_ora.sovrapposto_a(contenuto))
    print("[570,630) vs [540,600):", parziale.sovrapposto_a(prima_ora))

    uguale = Intervallo(540, 600)
    print("[540,600) vs [540,600):", prima_ora.sovrapposto_a(uguale))
    print("valori uguali, istanze distinte:", prima_ora == uguale, prima_ora is uguale)

    for inizio, fine in ((600, 540), (540, 540), (-1, 10), (0, 1441), (1440, 1440), (True, 60)):
        try:
            Intervallo(inizio, fine)
        except ValueError as errore:
            print("costruzione rifiutata:", errore)
