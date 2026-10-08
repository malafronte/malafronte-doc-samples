"""Soluzioni formative dei problemi di algoritmica dell'Unità 14.

Riferimenti eseguibili dei problemi della famiglia
`oggetti-composizione-intervalli` (PY-U14-T09…T14 e X05–X06). Le spiegazioni
complete — scelta dello stato, algoritmo, costo, prove ed errore da evitare
— sono pubblicate nelle soluzioni della pagina; qui vivono le versioni
eseguibili, con un docstring che richiama il problema.

Nessuna funzione modifica gli argomenti ricevuti dove la consegna dichiara
l'invarianza degli input; nessuna funzione stampa o legge input.

Ambiente: CPython sul computer. Dipende dai valori e dal registro di
`esempi/`.
"""

from intervalli_u14 import Intervallo
from magazzino_composto_u14 import Magazzino
from misure_modello_dati_u14 import MisuraFrozen
from prenotazioni_u14 import Prenotazione, RegistroPrenotazioni

# --- PY-U14-T09: la prima fascia libera per una risorsa --------------------


def prima_fascia_libera(finestra, durata, occupati):
    """PY-U14-T09: primo intervallo libero di `durata` dentro `finestra`.

    `occupati` è una lista di intervalli validi, a due a due non
    sovrapposti, eventualmente in ordine non cronologico e in parte fuori
    dalla finestra: si considerano per la loro intersezione con la finestra.
    Restituisce il primo `Intervallo` disponibile oppure `None`; input e
    lista restano invariati.
    """
    if isinstance(durata, bool) or not isinstance(durata, int) or durata <= 0:
        raise ValueError(f"durata: intero positivo atteso, ricevuto {durata!r}")
    if durata > finestra.durata_min:
        return None
    intersezioni = []
    for occupato in occupati:
        inizio = max(finestra.inizio_min, occupato.inizio_min)
        fine = min(finestra.fine_min, occupato.fine_min)
        if inizio < fine:
            intersezioni.append((inizio, fine))
    intersezioni.sort()
    candidato = finestra.inizio_min
    for inizio, fine in intersezioni:
        if inizio - candidato >= durata:
            return Intervallo(candidato, candidato + durata)
        candidato = max(candidato, fine)
    if finestra.fine_min - candidato >= durata:
        return Intervallo(candidato, candidato + durata)
    return None


# --- PY-U14-T10: riepilogo di misure valide --------------------------------


def riepilogo_misure(misure):
    """PY-U14-T10: quantità, totale, minimo e massimo; `None` sugli estremi se vuoto.

    Gli oggetti ricevuti non vengono mutati né filtrati: due misure uguali
    restano due record, perché l'uguaglianza di valore non è unicità.
    """
    quantita = 0
    totale_cm = 0
    minimo_cm = None
    massimo_cm = None
    for misura in misure:
        valore = misura.valore_cm
        quantita = quantita + 1
        totale_cm = totale_cm + valore
        if minimo_cm is None or valore < minimo_cm:
            minimo_cm = valore
        if massimo_cm is None or valore > massimo_cm:
            massimo_cm = valore
    return {
        "quantita": quantita,
        "totale_cm": totale_cm,
        "minimo_cm": minimo_cm,
        "massimo_cm": massimo_cm,
    }


# --- PY-U14-T11: tutte le coppie in conflitto ------------------------------


def coppie_in_conflitto(prenotazioni):
    """PY-U14-T11: coppie `(i, j)` con `i < j` in conflitto, nell'ordine degli indici.

    L'elenco può contenere conflitti: non è un registro valido, è un
    insieme di prenotazioni individualmente valide. Ogni coppia compare una
    sola volta; nessuna coppia con se stessa; aule diverse non confliggono.
    """
    coppie = []
    for i, prima in enumerate(prenotazioni):
        for j in range(i + 1, len(prenotazioni)):
            if prima.sovrapposta_a(prenotazioni[j]):
                coppie.append((i, j))
    return coppie


# --- PY-U14-T12: applicare un lotto senza effetti parziali -----------------


def applica_lotto(registro, candidati):
    """PY-U14-T12: applica i candidati per intero oppure lascia lo stato precedente.

    Strategia del diario di annullamento: ogni candidato registrato con
    successo viene ricordato; al primo rifiuto i candidati già applicati
    vengono annullati **in ordine inverso** e l'eccezione originale sale al
    chiamante. È un'alternativa pubblicabile alla copia-candidato usata da
    `registra_lotto`: funziona con le sole operazioni pubbliche del
    registro, a condizione che `annulla` sia affidabile come lo è qui.
    """
    applicati = []
    try:
        for candidato in candidati:
            registro.registra(candidato)
            applicati.append(candidato.codice)
    except Exception:
        for codice in reversed(applicati):
            registro.annulla(codice)
        raise
    return None


# --- PY-U14-T13: unione di due inventari composti --------------------------


def unisci_inventari(primo, secondo):
    """PY-U14-T13: nuovo `Magazzino` con primo seguito dal secondo, o rifiuto.

    Qualsiasi codice duplicato — anche con dati identici — solleva
    `ValueError`: niente somme implicite di quantità. Le raccolte di
    partenza non vengono modificate; il risultato contiene istanze nuove.
    """
    unito = Magazzino()
    for dat in primo.articoli():
        unito.inserisci(dat.codice, dat.descrizione, dat.quantita, dat.prezzo_centesimi)
    for dat in secondo.articoli():
        try:
            unito.inserisci(dat.codice, dat.descrizione, dat.quantita, dat.prezzo_centesimi)
        except ValueError as errore:
            raise ValueError(f"unione rifiutata: {errore}") from None
    return unito


# --- PY-U14-T14: minuti disponibili per aula dentro una finestra -----------


def minuti_disponibili(finestra, prenotazioni, aule):
    """PY-U14-T14: minuti liberi nella finestra per ogni aula del catalogo.

    Precondizione dichiarata: le prenotazioni di una stessa aula non sono a
    due a due sovrapposte. Si interseca ogni intervallo con la finestra e si
    sottrae l'occupazione dalla durata della finestra: sommare
    sovrapposizioni conterebbe due volte la stessa occupazione. Le aule del
    catalogo senza prenotazioni conservano l'intera durata.
    """
    occupazione = {aula: 0 for aula in aule}
    for prenotazione in prenotazioni:
        if prenotazione.aula not in occupazione:
            continue
        inizio = max(finestra.inizio_min, prenotazione.intervallo.inizio_min)
        fine = min(finestra.fine_min, prenotazione.intervallo.fine_min)
        if inizio < fine:
            occupazione[prenotazione.aula] = occupazione[prenotazione.aula] + (fine - inizio)
    return {aula: finestra.durata_min - minuti for aula, minuti in occupazione.items()}


# --- PY-U14-X05: spostare un lotto di prenotazioni --------------------------


def sposta_lotto(registro, codici, spostamento_min):
    """PY-U14-X05: nuovo registro con il lotto spostato, oppure eccezione.

    Strategia funzionale: si costruisce un registro candidato con le
    prenotazioni **non** spostate e le versioni spostate del lotto (stessi
    codici, stesse aule, stessi partecipanti, intervalli traslati). Un
    superamento della giornata viene rifiutato dalla costruzione dell'
    `Intervallo`; i conflitti con le prenotazioni rimaste vengono rifiutati
    da `registra`. Una traslazione comune preserva la non sovrapposizione
    interna del lotto già valido. Codici distinti ed esistenti sono una
    precondizione; l'ordine finale è non spostate, poi spostate, ciascun
    gruppo nell'ordine originale. Il registro originale non viene mai
    toccato: adottare il risultato è il singolo assegnamento del chiamante,
    quindi non esistono stati intermedi.
    """
    if isinstance(spostamento_min, bool) or not isinstance(spostamento_min, int):
        raise ValueError(
            f"spostamento_min: atteso un intero, ricevuto {type(spostamento_min).__name__}"
        )
    if spostamento_min == 0:
        raise ValueError("spostamento_min: nullo, nessun spostamento richiesto")
    da_spostare = set(codici)
    candidato = RegistroPrenotazioni()
    for presente in registro.prenotazioni():
        if presente.codice not in da_spostare:
            candidato.registra(presente)
    for presente in registro.prenotazioni():
        if presente.codice in da_spostare:
            nuovo_intervallo = Intervallo(
                presente.intervallo.inizio_min + spostamento_min,
                presente.intervallo.fine_min + spostamento_min,
            )
            candidato.registra(
                Prenotazione(
                    presente.codice, presente.aula, nuovo_intervallo, presente.partecipanti
                )
            )
    return candidato


# --- PY-U14-X06: prima fascia comune a due risorse --------------------------


def prima_fascia_comune(finestra, durata, occupati_a, occupati_b):
    """PY-U14-X06: prima fascia in cui **entrambe** le risorse sono libere.

    I candidati inizio sono l'inizio della finestra e i minuti di fine
    delle occupazioni delle due risorse, intercettate con la finestra. Il
    primo candidato che lascia `durata` minuti prima della fine e non si
    sovrappone a nessuna occupazione di nessuna delle due risorse è la
    risposta; se non esiste, `None`. Nessuna mutazione degli input: la sola
    ricerca non prenota nulla.
    """
    if isinstance(durata, bool) or not isinstance(durata, int) or durata <= 0:
        raise ValueError(f"durata: intero positivo atteso, ricevuto {durata!r}")
    if durata > finestra.durata_min:
        return None

    def intersezioni(occupati):
        risultato = []
        for occupato in occupati:
            inizio = max(finestra.inizio_min, occupato.inizio_min)
            fine = min(finestra.fine_min, occupato.fine_min)
            if inizio < fine:
                risultato.append(Intervallo(inizio, fine))
        return risultato

    blocchi = intersezioni(occupati_a) + intersezioni(occupati_b)
    candidati = sorted({finestra.inizio_min} | {blocco.fine_min for blocco in blocchi})
    for inizio in candidati:
        fine = inizio + durata
        if fine > finestra.fine_min:
            continue
        fascia = Intervallo(inizio, fine)
        if not any(fascia.sovrapposto_a(blocco) for blocco in blocchi):
            return fascia
    return None


if __name__ == "__main__":
    finestra = Intervallo(0, 60)
    libera = prima_fascia_libera(finestra, 10, [Intervallo(0, 20), Intervallo(30, 40)])
    print("T09:", libera, "| vuoto:", prima_fascia_libera(finestra, 10, []))
    print(
        "T09 nessun posto:",
        prima_fascia_libera(finestra, 10, [Intervallo(0, 55)]),
        "| durata oltre:",
        prima_fascia_libera(finestra, 90, []),
    )

    misure = [MisuraFrozen("M1", 0), MisuraFrozen("M2", 12), MisuraFrozen("M3", 12)]
    print("T10:", riepilogo_misure(misure), "| vuoto:", riepilogo_misure([]))

    tre = [
        Prenotazione("A", "Lab 1", Intervallo(0, 20), 5),
        Prenotazione("B", "Lab 1", Intervallo(10, 30), 5),
        Prenotazione("C", "Lab 1", Intervallo(30, 40), 5),
    ]
    print("T11:", coppie_in_conflitto(tre))
    in_altra_aula = [
        Prenotazione("A", "Lab 1", Intervallo(0, 20), 5),
        Prenotazione("B", "Lab 2", Intervallo(10, 30), 5),
    ]
    print("T11 aule diverse:", coppie_in_conflitto(in_altra_aula))

    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("F", "Lab 1", Intervallo(0, 30), 5))
    lotto = [
        Prenotazione("G", "Lab 1", Intervallo(30, 60), 5),
        Prenotazione("H", "Lab 1", Intervallo(40, 70), 5),
    ]
    try:
        applica_lotto(registro, lotto)
    except Exception as errore:
        print("T12:", type(errore).__name__, "-", errore)
    print("T12 stato precedente:", [p.codice for p in registro.prenotazioni()])
    applica_lotto(registro, [Prenotazione("G", "Lab 1", Intervallo(30, 60), 5)])
    print("T12 dopo il lotto valido:", [p.codice for p in registro.prenotazioni()])

    primo = Magazzino()
    primo.inserisci("007", "Vite, lunga", 4, 25)
    secondo = Magazzino()
    secondo.inserisci("012", 'Caffè "A"', 2, 350)
    unito = unisci_inventari(primo, secondo)
    print("T13:", unito.riepilogo())
    secondo_doppio = Magazzino()
    secondo_doppio.inserisci("007", "Vite, lunga", 4, 25)
    try:
        unisci_inventari(primo, secondo_doppio)
    except ValueError as errore:
        print("T13 duplicato:", errore)

    occupate = [
        Prenotazione("A", "Lab A", Intervallo(510, 570), 5),
        Prenotazione("B", "Lab A", Intervallo(600, 690), 5),
    ]
    print(
        "T14:",
        minuti_disponibili(Intervallo(540, 660), occupate, ["Lab A", "Lab B"]),
    )

    base = RegistroPrenotazioni()
    base.registra(Prenotazione("L1", "Lab 1", Intervallo(540, 600), 5))
    base.registra(Prenotazione("L2", "Lab 2", Intervallo(540, 600), 5))
    spostato = sposta_lotto(base, ["L1"], 60)
    print("X05:", [p.testo_riepilogo() for p in spostato.prenotazioni()])
    print("X05 originale intatto:", [p.testo_riepilogo() for p in base.prenotazioni()])
    try:
        sposta_lotto(base, ["L1"], 900)
    except ValueError as errore:
        print("X05 oltre la giornata:", errore)

    comune = prima_fascia_comune(
        Intervallo(540, 660),
        30,
        [Intervallo(540, 570)],
        [Intervallo(540, 600)],
    )
    print("X06:", comune)
    print(
        "X06 intersezione vuota:",
        prima_fascia_comune(Intervallo(540, 660), 60, [Intervallo(540, 660)], []),
    )
