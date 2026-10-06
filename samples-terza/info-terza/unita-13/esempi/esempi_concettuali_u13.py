"""Esempi concettuali dell'Unità 13: convertitore, Contatore, Limiti, Misura.

Ogni sezione è **autonoma**: definisce ciò che usa e non importa dalle
applicazioni successive dell'unità (contatore con capacità, Articolo,
magazzino). Il file accompagna i capitoli OOP-01 e OOP-02 nell'ordine in cui
i concetti vengono spiegati.

1. `millimetri_da_centimetri` — funzione pura e responsabilità separate
   (OOP-01, sez. D–F);
2. `Contatore` — prima classe, istanze, attributi e `self` (OOP-02, sez. A–F);
3. `Limiti` — invariante, guardie e aggiornamento coerente (OOP-02, sez. G);
4. `Misura` — proiezione dei dati e ricostruzione (OOP-02, sez. J).

Ambiente: CPython sul computer. Dipende soltanto dal linguaggio.
"""

import json

# ---------------------------------------------------------------------------
# 1. Convertitore centimetri -> millimetri (OOP-01, sez. D–F)
# ---------------------------------------------------------------------------

# Formula di dominio: un centimetro vale dieci millimetri. Il calcolo non
# legge né stampa nulla: riceve una lunghezza in centimetri e restituisce la
# lunghezza equivalente in millimetri.
FATTORE_MM_PER_CM = 10


def millimetri_da_centimetri(lunghezza_cm):
    """Converte una lunghezza da centimetri a millimetri.

    Precondizione: `lunghezza_cm` è un numero che esprime centimetri.
    Restituisce la lunghezza equivalente in millimetri. Nessuna lettura da
    tastiera, nessuna stampa: il risultato è disponibile a chi chiama.
    """
    return lunghezza_cm * FATTORE_MM_PER_CM


def messaggio_conversione(lunghezza_cm, lunghezza_mm, formulazione="risultato"):
    """Restituisce la riga di presentazione della conversione.

    Riceve i due valori già calcolati e la formulazione del messaggio:
    cambiare `formulazione` cambia soltanto questa riga, non il calcolo.
    """
    return f"{formulazione}: {lunghezza_cm} cm = {lunghezza_mm} mm"


def converti_misura(lunghezza_cm, formulazione="risultato"):
    """Coordina calcolo e presentazione senza acquisire né stampare.

    Il coordinatore chiama le due funzioni precedenti e restituisce la riga
    pronta: chi legge l'input e chi stampa resta fuori da questo modulo.
    """
    lunghezza_mm = millimetri_da_centimetri(lunghezza_cm)
    return messaggio_conversione(lunghezza_cm, lunghezza_mm, formulazione)


# ---------------------------------------------------------------------------
# 2. Contatore (OOP-02, sez. A–F)
# ---------------------------------------------------------------------------


class Contatore:
    """Contatore di quantità con un solo attributo pubblico: `valore`.

    Questa è la prima classe del corso ed è volutamente semplice: rende
    visibili la definizione, la costruzione delle istanze, gli attributi e il
    significato di `self`. Le **precondizioni** sono quelle del dominio di un
    conteggio: `valore` è un intero non negativo e `quantita` è un intero non
    negativo, **forniti validi dal chiamante**. Questa versione non li
    controlla: non attribuirle garanzie di validazione che non implementa.
    Il controllo del contratto attraverso le operazioni arriva con `Limiti`.
    """

    def __init__(self, valore):
        """Associa all'istanza l'attributo `valore` con il valore ricevuto."""
        self.valore = valore

    def incrementa(self, quantita):
        """Aggiunge `quantita` al valore dell'istanza e restituisce il nuovo.

        Il candidato viene calcolato in un nome locale e assegnato
        all'attributo **dopo** il calcolo: così si vede la differenza fra il
        temporaneo della chiamata e lo stato che resta sull'istanza.
        """
        candidato = self.valore + quantita
        self.valore = candidato
        return candidato


# ---------------------------------------------------------------------------
# 3. Limiti (OOP-02, sez. G)
# ---------------------------------------------------------------------------

# Confini del dominio di Limiti: due interi non booleani con
# 0 <= minimo <= massimo <= 100.
LIMITE_INFERIORE = 0
LIMITE_SUPERIORE = 100


def _valida_estremo(valore, nome):
    """Controlla che `valore` sia un intero non booleano nei confini ammessi.

    Restituisce `None` se il candidato è ammesso; solleva `ValueError` che
    nomina il campo altrimenti. Funzione pura, senza mutazioni.
    """
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(
            f"campo '{nome}': atteso un intero, ricevuto {type(valore).__name__}"
        )
    if valore < LIMITE_INFERIORE or valore > LIMITE_SUPERIORE:
        raise ValueError(
            f"campo '{nome}': atteso un valore fra {LIMITE_INFERIORE} "
            f"e {LIMITE_SUPERIORE} compresi, ricevuto {valore}"
        )
    return None


def _valida_coppia(minimo, massimo):
    """Controlla tipo, confini e ordine dei due estremi candidati.

    Prima i singoli campi (`_valida_estremo`), poi la relazione fra i due:
    solo se entrambi sono ammessi ha senso chiedere se `minimo <= massimo`.
    Un campo di tipo o intervallo invalido solleva `ValueError`; una coppia
    individualmente ammessa ma invertita non è un errore di formato e viene
    segnalata con `False` al chiamante.
    """
    _valida_estremo(minimo, "minimo")
    _valida_estremo(massimo, "massimo")
    return minimo <= massimo


class Limiti:
    """Intervallo chiuso di interi con due estremi sempre coerenti.

    Invariante dell'istanza: `0 <= _minimo <= _massimo <= 100`, con entrambi
    gli estremi interi e non booleani. L'invariante vale **sempre** per uno
    stato osservabile: la costruzione fallita non produce un'istanza, e ogni
    aggiornamento o applica tutti i campi oppure non ne applica nessuno.

    La convenzione `_nome` segnala che `_minimo` e `_massimo` sono
    **implementazione interna**: si leggono e si aggiornano attraverso
    `stato()` e `aggiorna()`. Il trattino basso non impedisce tecnicamente un
    accesso esterno, non garantisce privacy né immutabilità: è una convenzione
    di collaborazione, non un meccanismo di protezione.
    """

    def __init__(self, minimo, massimo):
        """Crea l'intervallo se la coppia rispetta l'invariante.

        Entrambi gli argomenti devono essere interi non booleani con
        `0 <= minimo <= massimo <= 100`. Un argomento non conforme solleva
        `ValueError` motivato e **nessuna istanza** viene restituita: la
        chiamata non ha successo parziale né un risultato `False`.
        """
        if not _valida_coppia(minimo, massimo):
            raise ValueError(
                f"coppia ({minimo}, {massimo}): atteso minimo <= massimo, "
                f"ricevuto {minimo} > {massimo}"
            )
        self._minimo = minimo
        self._massimo = massimo

    def stato(self):
        """Restituisce un **nuovo** dizionario con i due estremi.

        Il risultato è una proiezione dei dati del modello: modificarlo non
        modifica l'istanza, perché i due dizionari non condividono nulla.
        """
        return {"minimo": self._minimo, "massimo": self._massimo}

    def aggiorna(self, minimo, massimo):
        """Tenta di sostituire entrambi gli estremi e riferisce l'esito.

        Ordine dei controlli: tipo e confini di `minimo`, tipo e confini di
        `massimo`, poi la relazione fra i due. Solo dopo questo controllo
        completo i due campi vengono aggiornati insieme.

        - `ValueError` se un candidato è di tipo o intervallo invalido;
        - `False` se la coppia è individualmente ammessa ma invertita;
        - `True` se l'aggiornamento è applicato.

        In tutti i casi di rifiuto lo stato precedente resta **interamente**
        invariato: nessun campo viene aggiornato prima che la coppia sia
        risultata ammissibile.
        """
        if not _valida_coppia(minimo, massimo):
            return False
        self._minimo = minimo
        self._massimo = massimo
        return True


# ---------------------------------------------------------------------------
# 4. Misura (OOP-02, sez. J — prima parte)
# ---------------------------------------------------------------------------


class Misura:
    """Una lunghezza espressa in centimetri con un solo campo: `valore`.

    Dominio: `valore` è un **intero non booleano non negativo** che esprime
    centimetri. Ogni argomento fuori contratto produce `ValueError` motivato e
    nessuna istanza viene restituita. `dati()` è la proiezione esplicita dei
    dati del modello: serve a osservare, a confrontare e a costruire la
    rappresentazione esterna senza esporre l'implementazione.
    """

    def __init__(self, valore):
        """Crea la misura se `valore` è un intero non booleano non negativo."""
        _valida_estremo_non_negativo(valore, "valore")
        self._valore = valore

    def dati(self):
        """Restituisce un **nuovo** dizionario `{"valore": valore}`.

        Non è la copia dell'attributo interno: è la proiezione dichiarata del
        modello. Modificare il risultato non modifica l'istanza.
        """
        return {"valore": self._valore}


def _valida_estremo_non_negativo(valore, nome):
    """Controlla che `valore` sia un intero non booleano maggiore o uguale a 0."""
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(
            f"campo '{nome}': atteso un intero, ricevuto {type(valore).__name__}"
        )
    if valore < 0:
        raise ValueError(
            f"campo '{nome}': atteso un valore maggiore o uguale a zero, "
            f"ricevuto {valore}"
        )
    return None


# Le conversioni sono funzioni **esterne**: accedono ai dati della misura
# attraverso la proiezione `dati()` e non toccano gli attributi interni.

# Intestazione del CSV a un campo: il testo numerico va convertito
# esplicitamente in entrambe le direzioni.
INTESTAZIONE_MISURA = ("valore",)


def misura_a_campi(misura):
    """Restituisce i campi testuali della misura nell'ordine dello schema.

    La proiezione `dati()` fornisce il numero, che diventa testo nella forma
    decimale ordinaria: la riga è pronta per il record CSV. Nessuna mutazione.
    """
    return [str(misura.dati()["valore"])]


def campi_a_misura(campi, riferimento):
    """Ricostruisce una Misura da una riga di campi testuali CSV.

    `campi` è la sequenza dei campi nell'ordine dello schema;
    `riferimento` identifica la riga nei messaggi d'errore. Conversione e
    controllo del dominio sono passaggi distinti: un testo non numerico è un
    errore di conversione, un numero negativo è un errore di dominio, e le due
    diagnosi non vengono fuse. Restituisce un'istanza **nuova**.
    """
    if len(campi) != len(INTESTAZIONE_MISURA):
        attesi = ", ".join(INTESTAZIONE_MISURA)
        raise ValueError(
            f"{riferimento}: attesi {len(INTESTAZIONE_MISURA)} campi ({attesi}), "
            f"ricevuti {len(campi)}"
        )
    try:
        valore = int(campi[0])
    except ValueError:
        raise ValueError(
            f"{riferimento}, campo 'valore': il testo {campi[0]!r} non è un intero"
        ) from None
    try:
        return Misura(valore)
    except ValueError as errore:
        raise ValueError(f"{riferimento}: {errore}") from None


def dati_a_misura(dati):
    """Ricostruisce una Misura dal dizionario prodotto da `dati()`.

    È la strada del round-trip JSON: `json.dumps(misura.dati())` scrive un
    oggetto con il solo campo numerico `valore`, `json.loads` lo restituisce
    come dizionario e questa funzione ne ricrea l'istanza. Il campo deve
    esserci e deve essere un intero non booleano non negativo: `True`, `2.5`
    e `-1` sono rifiutati, senza coercizioni implicite.
    """
    if not isinstance(dati, dict):
        raise ValueError(
            f"dati: atteso un dizionario, ricevuto {type(dati).__name__}"
        )
    if "valore" not in dati:
        raise ValueError("campo 'valore': mancante")
    extra = [chiave for chiave in dati if chiave != "valore"]
    if extra:
        raise ValueError(f"campo '{extra[0]}': non previsto dallo schema")
    return Misura(dati["valore"])


# Il round-trip JSON di Misura usa la proiezione `dati()` come schema: il
# documento contiene un oggetto con il solo campo numerico `valore`.
FORMATO_JSON_MISURA = '{"valore": 12}'


def misura_a_testo_json(misura):
    """Restituisce la rappresentazione JSON della misura.

    `json.dumps` riceve il dizionario prodotto da `dati()`, non l'istanza:
    è la proiezione a rendere il dato serializzabile, senza esporre
    l'implementazione interna.
    """
    return json.dumps(misura.dati(), ensure_ascii=False)


def testo_json_a_misura(testo):
    """Ricostruisce una Misura da una rappresentazione JSON.

    Un testo non conforme alla sintassi JSON solleva `json.JSONDecodeError`;
    un documento conforme nella sintassi ma non nello schema solleva
    `ValueError`. Le due diagnosi restano distinte, come nel caricamento CSV.
    """
    return dati_a_misura(json.loads(testo))
