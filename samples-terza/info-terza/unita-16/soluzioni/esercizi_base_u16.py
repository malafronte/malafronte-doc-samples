"""Soluzioni formative degli esercizi di base - Unità 16.

Il modulo raccoglie il codice delle soluzioni PY-U16-T01…T07, X01…X03 della
raccolta `unita-16-array-liste-pile-code`. Ogni funzione dichiara il proprio
contratto; le spiegazioni complete restano nelle soluzioni guidate della pagina
degli esercizi.

Ambiente: CPython sul computer. Il modulo non apre interazioni all'import.
"""

from __future__ import annotations

from lista_concatenata_u16 import ListaConcatenata, _Nodo, controlla_invarianti
from nodi_collegamenti_u16 import Nodo


# PY-U16-T01 - Costruire e attraversare tre nodi.
def es_t01_catena_e_attraversamento() -> list:
    """Costruisce 12 -> 7 -> 19 con la classe `Nodo` e restituisce i valori in ordine."""
    nodo_c = Nodo(19)
    nodo_b = Nodo(7, nodo_c)
    nodo_a = Nodo(12, nodo_b)
    raccolti = []
    corrente = nodo_a
    while corrente is not None:
        raccolti.append(corrente.valore)
        corrente = corrente.successivo
    return raccolti


# PY-U16-T02 - Completare l'aggiunta in testa nel contenitore.
def es_t02_aggiungi_in_testa(lista: ListaConcatenata, valore) -> None:
    """Aggiunta in testa svolta, con i quattro aggiornamenti nell'ordine spiegato.

    Il nodo usa la classe interna `_Nodo` del contenitore: la corrispondenza con
    la classe `Nodo` dell'esempio sui collegamenti è soltanto nel nome.
    """
    nuovo = _Nodo(valore, lista._testa)  # 1. il nuovo nodo punta alla vecchia testa
    lista._testa = nuovo  # 2. la testa diventa il nuovo nodo
    if lista._coda is None:  # 3. la struttura era vuota: la coda coincide
        lista._coda = nuovo
    lista._dimensione += 1  # 4. la dimensione aumenta di uno


# PY-U16-T03 - Completare l'aggiunta in coda usando il riferimento mantenuto.
def es_t03_aggiungi_in_coda(lista: ListaConcatenata, valore) -> None:
    """Aggiunta in coda svolta: la `_coda` evita la ricerca dell'ultimo nodo."""
    nuovo = _Nodo(valore)
    if lista._coda is None:  # struttura vuota: il nuovo nodo è entrambi gli estremi
        lista._testa = nuovo
        lista._coda = nuovo
    else:
        lista._coda.successivo = nuovo  # l'ultimo nodo punta al nuovo
        lista._coda = nuovo  # il nuovo nodo diventa la coda
    lista._dimensione += 1


# PY-U16-T04 - Completare la rimozione in testa e `primo`.
def es_t04_primo(lista: ListaConcatenata):
    """Restituisce il primo valore; su vuoto solleva IndexError senza modificare lo stato."""
    if lista._testa is None:
        raise IndexError("primo su lista vuota")
    return lista._testa.valore


def es_t04_rimuovi_primo(lista: ListaConcatenata):
    """Restituisce il primo valore e scollega il nodo, ripristinando la coda sul vuoto."""
    if lista._testa is None:
        raise IndexError("rimozione del primo su lista vuota")
    valore = lista._testa.valore
    lista._testa = lista._testa.successivo
    if lista._testa is None:  # la catena è ora vuota
        lista._coda = None
    lista._dimensione -= 1
    return valore


# PY-U16-T05 - Ricerca e accesso per posizione sotto il contratto comune.
def es_t05_cerca(lista: ListaConcatenata, valore) -> int:
    """Restituisce la posizione della prima occorrenza di `valore`, oppure -1.

    Il controllo della presenza del nodo usa `is None`; il confronto fra valori
    usa `==`. I valori 0, False e None sono dati legittimi.
    """
    corrente = lista._testa
    posizione = 0
    while corrente is not None:
        if corrente.valore == valore:
            return posizione
        corrente = corrente.successivo
        posizione += 1
    return -1


def es_t05_valore_in_posizione(lista: ListaConcatenata, indice: int):
    """Accesso per posizione con il dominio del contratto: intero esatto, 0 <= indice < len."""
    if type(indice) is not int:
        raise TypeError("l'indice deve essere un intero")
    if not 0 <= indice < len(lista):
        raise IndexError(f"indice fuori dominio: {indice}")
    corrente = lista._testa
    for _ in range(indice):
        corrente = corrente.successivo
    assert corrente is not None
    return corrente.valore


# PY-U16-T06 - Wrapper pila e coda sullo stesso contratto.
class es_t06_PilaLista:
    """Pila LIFO sulla lista Python; la cima è l'estremo destro."""

    def __init__(self) -> None:
        self._elementi: list = []

    def __len__(self) -> int:
        return len(self._elementi)

    def vuota(self) -> bool:
        return not self._elementi

    def inserisci(self, valore) -> None:
        self._elementi.append(valore)

    def estrai(self):
        if not self._elementi:
            raise IndexError("estrazione da pila vuota")
        return self._elementi.pop()

    def cima(self):
        if not self._elementi:
            raise IndexError("cima di pila vuota")
        return self._elementi[-1]


class es_t06_CodaConcatenata:
    """Coda FIFO sulla lista concatenata: accodamento in coda, rimozione in testa."""

    def __init__(self) -> None:
        self._elementi = ListaConcatenata()

    def __len__(self) -> int:
        return len(self._elementi)

    def vuota(self) -> bool:
        return len(self._elementi) == 0

    def accoda(self, valore) -> None:
        self._elementi.aggiungi_in_coda(valore)

    def estrai(self):
        return self._elementi.rimuovi_primo()

    def fronte(self):
        return self._elementi.primo()


# PY-U16-T07 - Prove per stato indipendente e snapshot superficiale.
def es_t07_prove_indipendenza_e_snapshot() -> None:
    """Prove da cui dipende l'accettazione di T07: due contenitori e uno snapshot."""
    prima = ListaConcatenata()
    prima.aggiungi_in_coda(12)
    seconda = ListaConcatenata()
    seconda.aggiungi_in_coda(19)
    prima.rimuovi_primo()
    assert seconda.a_lista() == [19]  # le catene sono indipendenti
    assert controlla_invarianti(prima) == []
    assert controlla_invarianti(seconda) == []

    valore_condiviso = ["registro"]
    terza = ListaConcatenata()
    terza.aggiungi_in_coda(valore_condiviso)
    terza.aggiungi_in_coda(7)
    snapshot = terza.a_lista()
    snapshot.append("estraneo")  # il nuovo contenitore non modifica la catena
    assert terza.a_lista() == [["registro"], 7]
    valore_condiviso.append("aggiunto")  # la copia superficiale condivide i valori
    assert terza.a_lista() == [["registro", "aggiunto"], 7]


# PY-U16-X01 - Confronto fra accodamento con sola testa e con testa e coda.
def es_x01_confronto_accodamenti(quanti: int = 4) -> dict:
    """Conta gli avanzamenti dell'attraversamento con sola testa e gli aggiornamenti locali.

    Entrambe le versioni costruiscono la catena 10, 20, 30, ... fino a `quanti`
    valori; il risultato confronta il lavoro di raggiungimento dell'ultimo nodo
    con gli aggiornamenti costanti della versione con `_coda`.
    """
    testa = None
    avanzamenti_sola_testa = 0
    for valore in range(1, quanti + 1):
        nuovo = _Nodo(valore * 10)
        if testa is None:
            testa = nuovo
            continue
        corrente = testa
        while corrente.successivo is not None:  # si raggiunge l'ultimo nodo
            corrente = corrente.successivo
            avanzamenti_sola_testa += 1
        corrente.successivo = nuovo
        avanzamenti_sola_testa += 1

    lista = ListaConcatenata()
    for valore in range(1, quanti + 1):
        lista.aggiungi_in_coda(valore * 10)  # O(1) con la coda mantenuta
    assert lista.a_lista() == [valore * 10 for valore in range(1, quanti + 1)]
    return {
        "accodamenti": quanti,
        "avanzamenti_sola_testa": avanzamenti_sola_testa,
        "aggiornamenti_locali_con_coda": quanti,
    }
