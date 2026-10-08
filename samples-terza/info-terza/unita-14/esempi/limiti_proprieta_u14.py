"""Proprietà, valori derivati e invarianti su più campi (OOP-03, sez. B e C).

La classe `Limiti` conserva un intervallo numerico chiuso descritto da due
estremi interi. L'esempio mostra i tre strumenti del capitolo:

1. la **proprietà** `minimo` e `massimo`, con lettura e scrittura controllata;
2. la proprietà di sola lettura `ampiezza`, **derivata** e mai memorizzata;
3. l'operazione completa `imposta`, che valida la **coppia** candidata prima
   di ogni scrittura.

Contratto dell'esempio:

| Elemento | Regola |
|---|---|
| `minimo`, `massimo` | interi non booleani, con `minimo <= massimo` |
| estremi uguali | ammessi: l'ampiezza è zero |
| `ampiezza` | `massimo - minimo`, sola lettura, non memorizzata |
| `imposta(minimo, massimo)` | `None` sul successo; `ValueError` con stato invariato |
| conversioni | nessuna: stringhe e float non vengono convertiti |

Ogni rifiuto lascia l'intero stato dell'istanza esattamente com'era: i
controlli precedono ogni assegnamento.

Ambiente: CPython sul computer. Dipende soltanto dal linguaggio.
"""


def _valida_estremo(valore, nome):
    """Controlla che `valore` sia un intero non booleano. Nessun risultato."""
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(f"campo '{nome}': atteso un intero, ricevuto {type(valore).__name__}")
    return None


class Limiti:
    """Intervallo numerico chiuso con estremi interi e ampiezza derivata.

    Invariante dell'istanza: `minimo` e `massimo` sono interi non booleani e
    `minimo <= massimo` in ogni stato osservabile. La scrittura di un singolo
    estremo è permessa solo se lo stato che ne risulta resta valido; il
    trasferimento a una coppia non raggiungibile con scritture singole passa
    da `imposta`.
    """

    def __init__(self, minimo, massimo):
        """Crea i limiti dopo aver validato la coppia completa."""
        _valida_estremo(minimo, "minimo")
        _valida_estremo(massimo, "massimo")
        if minimo > massimo:
            raise ValueError(
                f"coppia (minimo, massimo): atteso minimo <= massimo, "
                f"ricevuti ({minimo}, {massimo})"
            )
        self._minimo = minimo
        self._massimo = massimo

    @property
    def minimo(self):
        """Estremo inferiore, intero. La lettura non muta lo stato."""
        return self._minimo

    @minimo.setter
    def minimo(self, valore):
        """Scrive l'estremo inferiore solo se la coppia risultante è valida.

        Il controllo coinvolge anche l'altro estremo: un valore in sé valido
        può essere rifiutato perché romperebbe la relazione `minimo <= massimo`.
        """
        _valida_estremo(valore, "minimo")
        if valore > self._massimo:
            raise ValueError(f"campo 'minimo': {valore} supera il massimo corrente {self._massimo}")
        self._minimo = valore

    @property
    def massimo(self):
        """Estremo superiore, intero. La lettura non muta lo stato."""
        return self._massimo

    @massimo.setter
    def massimo(self, valore):
        """Scrive l'estremo superiore solo se la coppia risultante è valida."""
        _valida_estremo(valore, "massimo")
        if valore < self._minimo:
            raise ValueError(f"campo 'massimo': {valore} è sotto il minimo corrente {self._minimo}")
        self._massimo = valore

    @property
    def ampiezza(self):
        """Differenza fra gli estremi. Proprietà di sola lettura, derivata.

        Non esiste un campo `_ampiezza`: il valore si calcola a ogni lettura
        e non può divergere dagli estremi.
        """
        return self._massimo - self._minimo

    def imposta(self, minimo, massimo):
        """Sostituisce l'intera coppia dopo averne validato il candidato.

        Restituisce `None` sul successo. Se la coppia candidata è invalida
        solleva `ValueError` e lascia entrambi gli estremi invariati: non
        esiste uno stato intermedio osservabile.
        """
        _valida_estremo(minimo, "minimo")
        _valida_estremo(massimo, "massimo")
        if minimo > massimo:
            raise ValueError(
                f"coppia (minimo, massimo): atteso minimo <= massimo, "
                f"ricevuti ({minimo}, {massimo})"
            )
        self._minimo = minimo
        self._massimo = massimo
        return None


if __name__ == "__main__":
    limite = Limiti(0, 10)
    print("costruzione:", (limite.minimo, limite.massimo), "ampiezza:", limite.ampiezza)

    limite.massimo = 15
    print("dopo massimo = 15:", (limite.minimo, limite.massimo))

    degenere = Limiti(5, 5)
    print("estremi uguali:", (degenere.minimo, degenere.massimo), "ampiezza:", degenere.ampiezza)

    try:
        limite.ampiezza = 4
    except AttributeError as errore:
        print("scrittura su ampiezza rifiutata:", errore)

    trasferimento = Limiti(0, 10)
    try:
        trasferimento.minimo = 20
    except ValueError as errore:
        print("minimo = 20 rifiutato:", errore)
    print("stato conservato:", (trasferimento.minimo, trasferimento.massimo))

    trasferimento.imposta(20, 30)
    print("dopo imposta(20, 30):", (trasferimento.minimo, trasferimento.massimo))

    altro = Limiti(0, 10)
    try:
        altro.imposta(20, 15)
    except ValueError as errore:
        print("imposta(20, 15) rifiutata:", errore)
    print("stato conservato:", (altro.minimo, altro.massimo))

    for candidato in (("dieci", 20), (0, 20.5), (True, 20)):
        try:
            Limiti(candidato[0], candidato[1])
        except ValueError as errore:
            print("costruzione rifiutata:", errore)
