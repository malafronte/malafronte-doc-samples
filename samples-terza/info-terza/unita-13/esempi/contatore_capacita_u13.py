"""Contatore con capacità: versione procedurale e classe (OOP-02, sez. H).

Il contatore con capacità rappresenta una **quantità di unità occupate** in un
contenitore che ne ammette un numero massimo fissato all'inizializzazione. Lo
scenario di riferimento è un deposito di unità: la `quantita` conta le unità
**contenute** — non i posti liberi — e la `capacita` è il numero massimo di
unità che il deposito può contenere. Le due grandezze non si alternano mai di
significato sullo stesso campo.

Il modulo contiene tre parti distinte:

1. la **versione procedurale**, che applica lo stesso contratto a un record
   ricevuto come argomento;
2. la **classe** `ContatoreCapacita`, che trasferisce quel contratto su
   istanze dotate di stato proprio;
3. una dimostrazione che esegue la stessa sequenza su entrambe le versioni e
   ne confronta ogni stato intermedio.

Contratto delle operazioni:

| Operazione | Contratto |
|---|---|
| costruzione `(capacita, quantita)` | interi non booleani; `0 <= quantita <= capacita` |
| `aggiungi(unita)` | intero non booleano >= 0; `True` se entra, `False` altrimenti |
| `preleva(unita)` | intero non booleano >= 0; `True` se basta, `False` altrimenti |
| `spazio_libero()` | restituisce `capacita - quantita`; nessuna modifica |
| `stato()` | nuovo dizionario `{"capacita", "quantita"}` |

Precisazioni sul contratto. La capacità è un intero **non negativo**; la
costruzione fuori contratto produce `ValueError` motivato. Su `False` lo stato
resta **invariato**: il rifiuto indica un'operazione valida ma non disponibile.
La quantità zero è un'operazione valida: restituisce `True` e lascia lo stato
invariato, e non equivale a un input assente, che è invece un errore di tipo.

La scelta di restituire `False` per un'operazione **valida ma non
disponibile** è specifica di questo esempio: distingue l'impossibilità dovuta
allo stato dall'errore di input, che resta un `ValueError`.

Ambiente: CPython sul computer. Dipende soltanto dal linguaggio.
"""


def _valida_unita(unita):
    """Controlla che `unita` sia un intero non booleano non negativo.

    Precondizione comune a `aggiungi` e `preleva`. Un valore fuori contratto è
    un **errore di input**: solleva `ValueError` e non viene tradotto in un
    rifiuto, che indicherebbe invece un'impossibilità dovuta allo stato.
    """
    if isinstance(unita, bool) or not isinstance(unita, int):
        raise ValueError(f"unita: atteso un intero, ricevuto {type(unita).__name__}")
    if unita < 0:
        raise ValueError(
            f"unita: atteso un valore maggiore o uguale a zero, ricevuto {unita}"
        )
    return None


def _valida_costruzione(capacita, quantita):
    """Controlla capacità e quantità iniziale secondo il contratto.

    Controlla prima i singoli campi, poi la relazione `quantita <= capacita`:
    solo due campi già ammessi possono formare una coppia incoerente.
    """
    for valore, nome in ((capacita, "capacita"), (quantita, "quantita")):
        if isinstance(valore, bool) or not isinstance(valore, int):
            raise ValueError(
                f"campo '{nome}': atteso un intero, ricevuto {type(valore).__name__}"
            )
        if valore < 0:
            raise ValueError(
                f"campo '{nome}': atteso un valore maggiore o uguale a zero, "
                f"ricevuto {valore}"
            )
    if quantita > capacita:
        raise ValueError(
            f"coppia ({capacita}, {quantita}): la quantita {quantita} "
            f"supera la capacita {capacita}"
        )
    return None


# ---------------------------------------------------------------------------
# Versione procedurale: lo stato è un record ricevuto come argomento
# ---------------------------------------------------------------------------


def nuovo_deposito(capacita, quantita=0):
    """Restituisce il record `{"capacita", "quantita"}` del deposito."""
    _valida_costruzione(capacita, quantita)
    return {"capacita": capacita, "quantita": quantita}


def carica(deposito, unita):
    """Aggiunge unità al deposito. `True` se applicato, `False` se non entra."""
    _valida_unita(unita)
    if deposito["quantita"] + unita > deposito["capacita"]:
        return False
    deposito["quantita"] = deposito["quantita"] + unita
    return True


def scarica(deposito, unita):
    """Preleva unità dal deposito. `True` se applicato, `False` se non bastano."""
    _valida_unita(unita)
    if unita > deposito["quantita"]:
        return False
    deposito["quantita"] = deposito["quantita"] - unita
    return True


def spazio_disponibile(deposito):
    """Restituisce i posti liberi del deposito. Nessuna modifica."""
    return deposito["capacita"] - deposito["quantita"]


def situazione(deposito):
    """Restituisce un nuovo dizionario con i due campi del deposito."""
    return {"capacita": deposito["capacita"], "quantita": deposito["quantita"]}


# ---------------------------------------------------------------------------
# Versione a oggetti: lo stato vive sull'istanza
# ---------------------------------------------------------------------------


class ContatoreCapacita:
    """Quantità contenuta in un insieme di capacità fissata.

    Invariante dell'istanza: `0 <= _quantita <= _capacita`, con `_capacita`
    intero non negativo immutato dal nucleo delle operazioni. L'invariante
    vale per ogni stato osservabile: la costruzione fallita non produce
    un'istanza e ogni operazione o aggiorna la quantità oppure non la tocca.

    `_capacita` e `_quantita` sono **implementazione interna**: si osservano
    con `stato()` e `spazio_libero()`. Il trattino basso è una convenzione di
    collaborazione, non una protezione tecnica.
    """

    def __init__(self, capacita, quantita=0):
        """Crea il contatore se capacità e quantità rispettano il contratto.

        Entrambi gli argomenti sono interi non booleani con `capacita >= 0` e
        `0 <= quantita <= capacita`. Un valore fuori contratto solleva
        `ValueError` motivato e **nessuna istanza** viene restituita.
        """
        _valida_costruzione(capacita, quantita)
        self._capacita = capacita
        self._quantita = quantita

    def aggiungi(self, unita):
        """Aggiunge unità se entrano nella capacità.

        `unita` è un intero non booleano non negativo: fuori contratto
        solleva `ValueError`. Se `unita` entra nello spazio libero la quantità
        viene aggiornata e il metodo restituisce `True`; se non entra
        restituisce `False` e lo stato resta **invariato**. La quantità zero è
        valida e restituisce `True` senza cambiare lo stato.
        """
        _valida_unita(unita)
        if self._quantita + unita > self._capacita:
            return False
        candidato = self._quantita + unita
        self._quantita = candidato
        return True

    def preleva(self, unita):
        """Preleva unità se la quantità contenuta basta.

        Stesso dominio di `aggiungi`. Se `unita` è disponibile la quantità
        viene aggiornata e il metodo restituisce `True`; altrimenti restituisce
        `False` senza toccare lo stato.
        """
        _valida_unita(unita)
        if unita > self._quantita:
            return False
        candidato = self._quantita - unita
        self._quantita = candidato
        return True

    def spazio_libero(self):
        """Restituisce i posti liberi: `capacita - quantita`. Nessuna modifica.

        È un **calcolo significativo** sullo stato, non un accessorio
        meccanico: deriva dall'invariante e non apre l'accesso ai campi.
        """
        return self._capacita - self._quantita

    def stato(self):
        """Restituisce un **nuovo** dizionario con `capacita` e `quantita`.

        Osservazione complessiva dei dati del modello, utile a tracce e test:
        modificare il risultato non modifica l'istanza.
        """
        return {"capacita": self._capacita, "quantita": self._quantita}


# ---------------------------------------------------------------------------
# Dimostrazione: la sequenza canonica su entrambe le versioni
# ---------------------------------------------------------------------------

# Sequenza canonica del capitolo: ogni passo dichiara l'operazione, il
# risultato atteso e lo stato atteso dopo il passo.
SEQUENZA_CANONICA = (
    ("aggiungi", 3, True, {"capacita": 5, "quantita": 3}),
    ("preleva", 4, False, {"capacita": 5, "quantita": 3}),
    ("aggiungi", 2, True, {"capacita": 5, "quantita": 5}),
    ("aggiungi", 1, False, {"capacita": 5, "quantita": 5}),
    ("preleva", 5, True, {"capacita": 5, "quantita": 0}),
    ("aggiungi", 0, True, {"capacita": 5, "quantita": 0}),
)


def esegui_sequenza_classe(capacita, quantita, sequenza):
    """Esegue la sequenza su un `ContatoreCapacita` e ne registra ogni passo.

    Restituisce la lista dei passi effettuati, ciascuno nella forma
    `(operazione, unita, risultato, stato_dopo)`. Una `ValueError` interrompe
    la registrazione: la gestione dell'errore spetta al chiamante.
    """
    contatore = ContatoreCapacita(capacita, quantita)
    passi = []
    for operazione, unita, _risultato_atteso, _stato_atteso in sequenza:
        metodo = contatore.aggiungi if operazione == "aggiungi" else contatore.preleva
        risultato = metodo(unita)
        passi.append((operazione, unita, risultato, contatore.stato()))
    return passi


def esegui_sequenza_procedurale(capacita, quantita, sequenza):
    """Esegue la stessa sequenza sulla versione procedurale.

    Il confronto con `esegui_sequenza_classe` verifica l'equivalenza **passo
    per passo**, non soltanto sul risultato finale.
    """
    deposito = nuovo_deposito(capacita, quantita)
    passi = []
    for operazione, unita, _risultato_atteso, _stato_atteso in sequenza:
        funzione = carica if operazione == "aggiungi" else scarica
        risultato = funzione(deposito, unita)
        passi.append((operazione, unita, risultato, situazione(deposito)))
    return passi


if __name__ == "__main__":
    for numero, (operazione, unita, risultato, stato) in enumerate(
        esegui_sequenza_classe(5, 0, SEQUENZA_CANONICA), start=1
    ):
        print(f"passo {numero}: {operazione}({unita}) -> {risultato}  stato {stato}")
    equivalente = esegui_sequenza_classe(5, 0, SEQUENZA_CANONICA) == (
        esegui_sequenza_procedurale(5, 0, SEQUENZA_CANONICA)
    )
    print("le due versioni coincidono passo per passo:", equivalente)
    try:
        ContatoreCapacita(5, 0).aggiungi(-1)
    except ValueError as errore:
        print("rifiuto:", errore)
