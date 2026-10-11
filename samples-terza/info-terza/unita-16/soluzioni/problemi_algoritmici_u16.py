"""Soluzioni formative dei problemi di algoritmica - Unità 16.

Il modulo raccoglie il codice delle soluzioni PY-U16-T08…T12 e X04…X06 della
famiglia `strutture-lineari-pile-code`. Le spiegazioni complete restano nelle
soluzioni guidate della pagina della famiglia.

Ambiente: CPython sul computer. Il modulo non apre interazioni all'import.
"""

from __future__ import annotations

from collections import deque

from lista_concatenata_u16 import _Nodo


# PY-U16-T08 - Cancellare la prima occorrenza da una catena con duplicati.
def t08_rimuovi_prima_occorrenza(testa: _Nodo | None, valore) -> tuple[_Nodo | None, bool]:
    """Rimuove il primo nodo il cui valore è uguale a `valore` e restituisce (testa, rimosso).

    Su assenza la catena resta identica e il secondo elemento del risultato è
    False. Il predecessore è tenuto durante l'attraversamento; il successore del
    nodo da scollegare è già noto nel nodo stesso.
    """
    precedente = None
    corrente = testa
    while corrente is not None:
        if corrente.valore == valore:
            if precedente is None:  # il nodo da rimuovere è la testa
                testa = corrente.successivo
            else:
                precedente.successivo = corrente.successivo
            return testa, True
        precedente = corrente
        corrente = corrente.successivo
    return testa, False


# PY-U16-T09 - Invertire una lista riusando i nodi.
def t09_inverti_catena(testa: _Nodo | None) -> _Nodo | None:
    """Inverte i collegamenti della catena e restituisce la nuova testa.

    Tre riferimenti guidano il passaggio: `precedente` raccoglie il prefisso già
    invertito, `corrente` è il nodo da elaborare e `successivo` conserva il
    suffisso ancora da visitare.
    """
    precedente = None
    corrente = testa
    while corrente is not None:
        successivo = corrente.successivo
        corrente.successivo = precedente
        precedente = corrente
        corrente = successivo
    return precedente


# PY-U16-T10 - Aggiornamenti e annullamenti di un contatore.
def t10_sequenza_canonica() -> list:
    """Riproduce la sequenza canonica: +3, +4, poi due annullamenti e un terzo tentativo."""
    from annullamenti_u16 import ContatoreAnnullabile

    contatore = ContatoreAnnullabile(5)
    esiti = []
    contatore.aggiorna(3)
    contatore.aggiorna(4)
    esiti.append(contatore.valore)  # 12
    esiti.append(contatore.annulla())  # True, valore 8
    esiti.append(contatore.annulla())  # True, valore 5
    esiti.append(contatore.annulla())  # False, valore conservato 5
    esiti.append(contatore.valore)
    return esiti


# PY-U16-T11 - Elaborazione di richieste con inserimenti intercalati.
def t11_elaborazione_intercalata(fabbrica_coda) -> list[str]:
    """Accoda R01/R02, ne elabora una, accoda R03 e restituisce gli esiti in ordine.

    `fabbrica_coda` è una funzione che restituisce una coda vuota compatibile
    con il contratto del servizio; lo stesso corpo di prova si applica a
    `CodaDeque` e `CodaConcatenata`.
    """
    from richieste_u16 import Richiesta, ServizioRichieste

    servizio = ServizioRichieste(fabbrica_coda())
    servizio.accoda_richiesta(Richiesta("R01", 2))
    servizio.accoda_richiesta(Richiesta("R02", 1))
    primo = servizio.elabora_prossima()  # completata a 2
    servizio.accoda_richiesta(Richiesta("R03", 3))
    esiti = [primo.codice]
    for esito in servizio.elabora_tutte():
        esiti.append(esito.codice)
    return esiti  # ['R01', 'R02', 'R03'] con R03 accodata dopo la prima estrazione


# PY-U16-T12 - Verifica dei delimitatori con una pila.
APERTURE = "([{"
CHIUSURE = ")]}"
COPPIE = {")": "(", "]": "[", "}": "{"}


def t12_delimitatori_bilanciati(testo: str) -> bool:
    """Restituisce True se le parentesi di `testo` sono correttamente annidate.

    Politica sui caratteri: i sei delimitatori sono controllati; ogni altro
    carattere viene ignorato dalla verifica di bilanciamento. Una chiusura senza
    la corrispondente apertura e un'apertura residua producono False.
    """
    pila: deque[str] = deque()
    for carattere in testo:
        if carattere in APERTURE:
            pila.append(carattere)
        elif carattere in CHIUSURE:
            if not pila or pila.pop() != COPPIE[carattere]:
                return False
    return not pila


# PY-U16-X04 - Confronto del lavoro per m inserimenti e m estrazioni FIFO.
def x04_confronto_lavoro(m: int = 4) -> dict:
    """Conta gli spostamenti di `list.pop(0)` e le operazioni agli estremi di deque.

    Il modello conta ciascuno spostamento del primo elemento dell'array: con
    `pop(0)` gli elementi restanti si muovono a ogni estrazione, per un totale
    quadratico in m; la coda sugli estremi esegue 2m operazioni costanti.
    """
    if m < 1:
        raise ValueError("m deve essere almeno 1")
    elementi = [f"R{i:02d}" for i in range(1, m + 1)]
    spostamenti_list = 0
    for _ in range(m):
        elementi.pop(0)
        spostamenti_list += len(elementi)  # ogni elemento restante si sposta di una posizione

    coda = deque(f"R{i:02d}" for i in range(1, m + 1))
    for _ in range(m):
        coda.popleft()
    return {
        "m": m,
        "spostamenti_pop0": spostamenti_list,  # m*(m-1)/2
        "operazioni_estremi_deque": 2 * m,  # m accodamenti + m estrazioni
    }


# PY-U16-X05 - Estensione a lista doppiamente concatenata.
class X05NodoDoppio:
    """Nodo di una lista doppia: conserva valore, successivo e precedente."""

    def __init__(self, valore, precedente: X05NodoDoppio | None = None) -> None:
        self.valore = valore
        self.precedente = precedente
        self.successivo: X05NodoDoppio | None = None


class X05ListaDoppia:
    """Lista doppiamente concatenata minimale: estremi mantenuti e rimozione locale."""

    def __init__(self) -> None:
        self.testa: X05NodoDoppio | None = None
        self.coda: X05NodoDoppio | None = None

    def aggiungi_in_coda(self, valore) -> X05NodoDoppio:
        nuovo = X05NodoDoppio(valore)
        if self.coda is None:
            self.testa = nuovo
            self.coda = nuovo
        else:
            nuovo.precedente = self.coda
            self.coda.successivo = nuovo
            self.coda = nuovo
        return nuovo

    def rimuovi_nodo(self, nodo: X05NodoDoppio) -> None:
        """Rimuove `nodo` usando i soli suoi riferimenti, estremi compresi."""
        if nodo.precedente is None:
            self.testa = nodo.successivo
        else:
            nodo.precedente.successivo = nodo.successivo
        if nodo.successivo is None:
            self.coda = nodo.precedente
        else:
            nodo.successivo.precedente = nodo.precedente

    def a_lista(self) -> list:
        valori = []
        corrente = self.testa
        while corrente is not None:
            valori.append(corrente.valore)
            corrente = corrente.successivo
        return valori


# PY-U16-X06 - Crescita geometrica e incremento fisso della capacità.
def x06_confronto_crescita(accodamenti: int = 100, incremento: int = 2) -> dict:
    """Confronta i modelli di crescita sullo stesso numero di accodamenti.

    Modello geometrico: raddoppio della capacità. Modello a incremento fisso:
    `incremento` posti aggiunti a ogni ridimensionamento. Il conteggio separa
    le copie dei riferimenti dalle scritture dei nuovi valori e conserva tutti
    i valori in entrambe le simulazioni.
    """
    if accodamenti < 0 or incremento < 1:
        raise ValueError("parametri del modello fuori dominio")

    def simula(crescita) -> tuple[int, int, list]:
        capacita = 0
        dimensione = 0
        array: list = []
        copie = 0
        for numero in range(accodamenti):
            if dimensione == capacita:
                nuova = crescita(capacita)
                nuovo_array = [None] * nuova
                for indice in range(dimensione):
                    nuovo_array[indice] = array[indice]
                    copie += 1
                array = nuovo_array
                capacita = nuova
            array[dimensione] = numero
            dimensione += 1
        return copie, capacita, array[:dimensione]

    copie_geometriche, cap_geometrica, valori_a = simula(lambda cap: max(cap * 2, 1))
    copie_fisse, cap_fissa, valori_b = simula(lambda cap: cap + incremento)
    assert valori_a == valori_b == list(range(accodamenti))
    return {
        "accodamenti": accodamenti,
        "copie_geometrico": copie_geometriche,
        "capacita_finale_geometrico": cap_geometrica,
        "copie_incremento_fisso": copie_fisse,
        "capacita_finale_incremento_fisso": cap_fissa,
        "incremento": incremento,
    }
