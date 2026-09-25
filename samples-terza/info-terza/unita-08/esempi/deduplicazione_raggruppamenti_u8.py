"""Deduplicazione e raggruppamenti dell'Unità 8: insiemi, gruppi e pattern.

Collocare il file in `programmi/deduplicazione_raggruppamenti_u8.py` della
raccolta dello studente. Il modulo contiene tre nuclei del capitolo PY-12,
parte III: la deduplicazione che conserva l'ordine di incontro (problema
svolto con insieme dei visti e lista risultato), il raggruppamento per
categoria (problema svolto con dizionario di liste) e il riconoscimento
delle misure con un pattern di dizionario in `match/case`.

Modelli ricordati: l'insieme garantisce l'unicità ma non l'ordine, mentre la
lista risultato esplicita l'ordine promesso; il raggruppamento associa ogni
chiave a una lista propria, perché le liste condivise fanno apparire
dipendenti gruppi che devono restare indipendenti; il pattern di dizionario
RICONOSCE la forma di un dato e non lo valida di per sé, perché i valori
possono avere il tipo sbagliato anche quando le chiavi sono quelle giuste.

L'import non chiede input e non stampa: le dimostrazioni stanno nel main
protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/deduplicazione_raggruppamenti_u8.py
"""

VOCI_CANONICHE = [("elettronica", "R10"), ("meccanica", "007"), ("elettronica", "L05")]


# ---------------------------------------------------------------------------
# Problema svolto 1 — Preservare la prima occorrenza
# ---------------------------------------------------------------------------


def unici_in_ordine(valori: list[int]) -> list[int]:
    """Restituisce gli elementi distinti nell'ordine della PRIMA occorrenza.

    Riceve la lista `valori` e restituisce una lista NUOVA nella quale ogni
    elemento compare una sola volta, nell'ordine con cui compare per la
    prima volta nell'argomento. L'argomento non viene modificato: duplicati
    e ordine restano nella lista ricevuta. Per lista vuota il risultato è
    `[]`.

    Il procedimento usa due strutture con ruoli diversi: l'insieme `visti`
    risponde alla domanda «l'ho già incontrato?» in tempo indipendente
    dall'elemento, mentre la lista `risultato` costruisce l'ordine promesso.
    L'invariante è: dopo ogni passaggio il risultato contiene una sola volta
    gli elementi già incontrati, nell'ordine della loro prima comparsa.

    Il solo `list(set(valori))` elimina i duplicati ma non garantisce questo
    ordine e quindi non rispetta il contratto. Gli elementi di questo primo
    problema sono interi: non si promette un algoritmo universale per liste
    di record, che richiederebbero un criterio di confronto esplicito.
    """
    visti = set()
    risultato = []
    for valore in valori:
        if valore not in visti:
            visti.add(valore)
            risultato.append(valore)
    return risultato


def unici_ultime_occorrenze(valori: list[int]) -> list[int]:
    """VARIANTE: restituisce gli elementi distinti nell'ordine delle ULTIME occorrenze.

    Stesso ricevuto e stessa forma del risultato di `unici_in_ordine`, ma
    l'ordine promesso è DIVERSO e non va confuso con quello del problema
    svolto: ogni elemento compare una sola volta, nella posizione indicata
    dalla sua ULTIMA comparsa nell'argomento. Per `[3, 1, 3, 2, 1]` il
    risultato è `[3, 2, 1]`: 3 all'indice 2, 2 all'indice 3, 1 all'indice 4.

    Il procedimento usa un dizionario e la regola dell'ordine di inserimento:
    cancellare una chiave e reinserirla la sposta in fondo. L'argomento non
    viene modificato. Per lista vuota il risultato è `[]`.
    """
    ultimi = {}
    for valore in valori:
        if valore in ultimi:
            del ultimi[valore]
        ultimi[valore] = None
    return list(ultimi)


# ---------------------------------------------------------------------------
# Problema svolto 2 — Raggruppare i codici per categoria
# ---------------------------------------------------------------------------


def raggruppa_codici(voci: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Restituisce i codici raggruppati per categoria, in un dizionario nuovo.

    Riceve la lista di coppie `(categoria, codice)` e restituisce un
    dizionario NUOVO che associa ogni categoria alla lista dei propri
    codici. Ciascuna lista è NUOVA e indipendente dalle altre; i codici di
    ogni gruppo seguono l'ordine di INCONTRO; le chiavi del dizionario
    seguono la prima comparsa della categoria. L'argomento non viene
    modificato. Per lista vuota il risultato è `{}`.

    Il gruppo nasce alla prima comparsa della categoria con l'assegnamento
    `gruppi[categoria] = []`, e soltanto dopo il codice viene aggiunto con
    `append`. La ripetizione di una coppia viene conservata come ripetizione
    nel gruppo: raggruppare e deduplicare sono operazioni diverse.

    La presentazione alfabetica delle categorie, se richiesta, è un
    passaggio separato e successivo: questo contratto conserva l'ordine di
    prima comparsa.
    """
    gruppi = {}
    for categoria, codice in voci:
        if categoria not in gruppi:
            gruppi[categoria] = []
        gruppi[categoria].append(codice)
    return gruppi


# ---------------------------------------------------------------------------
# Controesempio — la stessa lista assegnata a due chiavi
# ---------------------------------------------------------------------------


def controsesempio_liste_condivise(categorie: list[str]) -> dict[str, list[str]]:
    """CONTROESEMPIO: assegna la STESSA lista vuota a tutte le `categorie`.

    NON È LA SOLUZIONE del problema e non va usata per il raggruppamento.
    `dict.fromkeys(categorie, [])` costruisce il dizionario delle categorie
    usando UN SOLO oggetto lista come valore di ogni chiave: i gruppi non
    sono indipendenti e ogni `append` su una chiave modifica anche tutte le
    altre. La struttura appare corretta — ogni chiave ha la propria voce —
    ma le voci condividono il contenuto.

    La forma corretta crea una lista NUOVA per ogni categoria, come fa
    `raggruppa_codici`, e la assegna soltanto alla propria chiave. Il
    difetto si osserva anche nei risultati di due chiamate distinte quando
    la lista condivisa viene poi modificata.
    """
    return dict.fromkeys(categorie, [])


# ---------------------------------------------------------------------------
# Riconoscimento delle misure con pattern di dizionario
# ---------------------------------------------------------------------------


def esito_misura(dato) -> str:
    """Restituisce l'esito del riconoscimento della misura `dato` ricevuta.

    Riceve un valore di qualunque tipo e restituisce una delle tre stringhe
    `"valida"`, `"valori non validi"`, `"struttura non riconosciuta"`.

    Il pattern `case {"sensore": sensore, "valore": valore}` riconosce i
    mapping che contengono almeno le chiavi `sensore` e `valore` e ne cattura
    i valori; l'ordine di scrittura dei campi non conta e le chiavi
    ulteriori, come `"istante_ms"`, sono metadati non interpretati e non
    impediscono il riconoscimento. Il pattern `{}` oppure il caso residuale
    `case _` copre i soggetti che non hanno quella struttura: campi
    mancanti oppure un oggetto che non è un mapping, per esempio una lista.

    Il riconoscimento della struttura NON basta: i valori catturati vengono
    validati con una normale condizione nel corpo del ramo. Il dominio della
    misura è sintetico: `sensore` è una stringa non vuota e `valore` è un
    intero in centesimi di grado Celsius fra -4000 e 12500 compresi. Il
    controllo `type(valore) is int` sceglie gli interi ESATTI e quindi `True`
    non viene accettato come misura: è una condizione nel corpo e non un
    pattern di classe. Se la validazione fallisce non si usano i nomi
    catturati oltre il ramo corrispondente.
    """
    match dato:
        case {"sensore": sensore, "valore": valore}:
            if (
                type(sensore) is str
                and sensore != ""
                and type(valore) is int
                and -4000 <= valore <= 12500
            ):
                return "valida"
            return "valori non validi"
        case _:
            return "struttura non riconosciuta"


if __name__ == "__main__":
    # Le uniche stampe del modulo stanno qui: ogni funzione sopra restituisce
    # e non scrive nulla.
    print("Deduplicazione che conserva la prima occorrenza")
    for valori in ([], [3, 1, 3, 2, 1], [7, 7], [0, -1, 0]):
        print(f"  {str(valori):<16} ->", unici_in_ordine(valori))
    print("variante sulle ultime occorrenze")
    for valori in ([], [3, 1, 3, 2, 1], [7, 7], [0, -1, 0]):
        print(f"  {str(valori):<16} ->", unici_ultime_occorrenze(valori))

    print()
    print("Raggruppamento per categoria")
    print("voci        :", VOCI_CANONICHE)
    gruppi = raggruppa_codici(VOCI_CANONICHE)
    print("gruppi      :", {nome: gruppi[nome] for nome in gruppi})
    print("vuoto       :", raggruppa_codici([]))
    ripetuti = raggruppa_codici([("elettronica", "R10"), ("elettronica", "R10")])
    print("ripetizione :", ripetuti)
    gruppi["elettronica"].append("X99")
    print("gruppi indipendenti: meccanica resta", gruppi["meccanica"],
          "dopo l'append su elettronica")
    print("seconda chiamata invariata:", raggruppa_codici(VOCI_CANONICHE))

    print()
    print("Controesempio: la stessa lista per ogni categoria")
    condivisi = controsesempio_liste_condivise(["elettronica", "meccanica"])
    condivisi["elettronica"].append("R10")
    print("dopo l'append su elettronica:", condivisi)
    print("le due liste sono lo stesso oggetto:",
          condivisi["elettronica"] is condivisi["meccanica"])

    print()
    print("Riconoscimento delle misure")
    prove = [
        {"sensore": "S1", "valore": 2150},
        {"valore": 2150, "sensore": "S1"},
        {"sensore": "S1", "valore": 2150, "istante_ms": 0},
        {"sensore": 2150, "valore": "S1"},
        {"sensore": "S1"},
        {},
        ["S1", 2150],
        {"sensore": "S1", "valore": "2150"},
        {"sensore": "S1", "valore": -4000},
        {"sensore": "S1", "valore": 12500},
        {"sensore": "S1", "valore": 12501},
        {"sensore": "S1", "valore": True},
        {"sensore": "", "valore": 2150},
    ]
    for dato in prove:
        print(f"  {str(dato):<52} -> {esito_misura(dato)}")
