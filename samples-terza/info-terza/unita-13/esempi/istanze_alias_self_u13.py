"""Istanze, alias e `self`: varianti storiche complete sul contatore.

Il percorso attuale usa gli orologi di `orologio_digitale_u13.py`.
Questo modulo conserva le **varianti** originarie di OOP-02 per rendere
osservabili i meccanismi di attributi, nomi locali, `self`, alias e copie.
Ogni variante è una definizione completa ed eseguibile: nessun frammento
isolato e nessun programma che contiene omissioni.

Le classi qui definite sono deliberatamente **didattiche**: servono a
confrontare esecuzioni corrette e difettose, non sono il modello da imitare.
La classe `Contatore` corretta di riferimento è in `esempi_concettuali_u13.py`.

Ambiente: CPython sul computer. Dipende soltanto dal linguaggio.
"""


class Contatore:
    """Copia locale della classe corretta, per confronti autonomi.

    Attributo pubblico `valore`; `incrementa(quantita)` calcola un candidato
    in un nome locale, lo assegna all'attributo e restituisce il nuovo valore.
    Le precondizioni sono quelle dichiarate nel capitolo: quantità intere non
    negative fornite valide dal chiamante.
    """

    def __init__(self, valore):
        self.valore = valore

    def incrementa(self, quantita):
        candidato = self.valore + quantita
        self.valore = candidato
        return candidato


class ContatoreConLocale:
    """Variante difettosa: aggiorna un nome locale, non l'istanza.

    Il metodo calcola correttamente il nuovo valore, ma lo scrive in `valore`,
    che è un **nome locale della chiamata**. Alla fine del metodo quel nome
    scompare e l'attributo `self.valore` non è mai stato toccato: la chiamata
    termina senza errori eppure lo stato dell'istanza non cambia.
    """

    def __init__(self, valore):
        self.valore = valore

    def incrementa(self, quantita):
        # Difetto intenzionale: `valore` è un locale, non `self.valore`.
        valore = self.valore + quantita
        return valore


class ContatoreConSelfRiassegnato:
    """Variante didattica: riassegna il nome `self` dentro il metodo.

    `self` non è una parola chiave: è il nome convenzionale del parametro che
    riceve l'istanza. Riassegnarlo sposta quel nome locale su un altro oggetto
    e **non** cambia l'associazione del nome usato dal chiamante.
    """

    def __init__(self, valore):
        self.valore = valore

    def incrementa_su_altro(self, quantita):
        """Aggiorna un contatore diverso da quello ricevuto.

        Dopo `self = altro` il nome `self` indica `altro`: le assegnazioni
        seguenti modificano `altro`, mentre il contatore del chiamante resta
        invariato. Il valore restituito è quello di `altro`.
        """
        altro = Contatore(0)
        self = altro
        self.valore = quantita
        return self.valore


def traccia_chiamata_legata():
    """Restituisce la traccia della chiamata legata `c.incrementa(3)`.

    Con `c` inizialmente a 2: l'argomento `3` arriva al parametro `quantita`,
    l'istanza `c` arriva al primo parametro `self`, il candidato locale vale
    5, l'attributo `c.valore` diventa 5 e il metodo restituisce 5.
    """
    c = Contatore(2)
    ricevente_prima = c.valore
    risultato = c.incrementa(3)
    return {
        "ricevente_prima": ricevente_prima,
        "argomento_quantita": 3,
        "risultato": risultato,
        "ricevente_dopo": c.valore,
    }


def traccia_chiamata_esplicita():
    """Restituisce la traccia della chiamata esplicita `Contatore.incrementa(c, 3)`.

    Stessa associazione dei parametri della forma legata, scritta in modo
    esplicito: il primo argomento dopo la classe è l'istanza che la forma
    legata usa come ricevente. Istanza fresca inizializzata a 2, come sopra.
    """
    c = Contatore(2)
    ricevente_prima = c.valore
    risultato = Contatore.incrementa(c, 3)
    return {
        "ricevente_prima": ricevente_prima,
        "argomento_istanza": "c",
        "argomento_quantita": 3,
        "risultato": risultato,
        "ricevente_dopo": c.valore,
    }


def alias_e_copia():
    """Restituisce la traccia di alias, lista, copia e nuova costruzione.

    Distinzioni rese osservabili:
    - `secondo = primo` crea un **secondo nome** per la stessa istanza;
    - `lista.copy()` crea un contenitore nuovo che contiene gli **stessi**
      oggetti della lista originaria;
    - `Contatore(...)` crea un'istanza nuova, che non condivide nulla con le
      precedenti anche se i dati iniziali sono uguali.
    """
    primo = Contatore(2)
    secondo = primo
    lista = [primo, Contatore(7)]
    copia = lista.copy()
    risultato = {
        "alias_stessa_istanza": secondo is primo,
        "copia_contenitore_distinto": copia is not lista,
        "copia_elementi_condivisi": copia[0] is lista[0],
        "nuova_costruzione_stessi_dati": Contatore(2) is primo,
    }
    # Mutare l'elemento attraverso l'alias si vede da ogni nome collegato.
    secondo.incrementa(3)
    risultato["primo_dopo_alias"] = primo.valore
    # Modificare la lista esterna non tocca gli oggetti referenziati.
    copia.append(Contatore(0))
    risultato["lista_originale_lunghezza"] = len(lista)
    risultato["copia_lunghezza"] = len(copia)
    return risultato


def traccia_self_riassegnato():
    """Restituisce la traccia del metodo che riassegna `self`."""
    c = ContatoreConSelfRiassegnato(4)
    prima = c.valore
    risultato = c.incrementa_su_altro(9)
    return {
        "chiamante_prima": prima,
        "risultato": risultato,
        "chiamante_dopo": c.valore,
    }


if __name__ == "__main__":
    print("chiamata legata:   ", traccia_chiamata_legata())
    print("chiamata esplicita:", traccia_chiamata_esplicita())
    difettoso = ContatoreConLocale(2)
    print("locale difettoso, risultato:", difettoso.incrementa(3))
    print("locale difettoso, stato:    ", difettoso.valore)
    print("self riassegnato:", traccia_self_riassegnato())
    print("alias e copia:   ", alias_e_copia())
