"""Dominio del magazzino a oggetti: operazioni su una lista di Articolo.

Questo modulo contiene la **logica del dato** della variante a oggetti del
magazzino del cap. PY-20: ricerca, inserimento, aggiornamento ed eliminazione
su una lista di istanze `Articolo`, conversione dalle e verso le righe testuali
del CSV e riepilogo della raccolta. Nessuna lettura da file, nessuna stampa,
nessuna domanda.

Le funzioni restano **esterne**: non diventano metodi statici della classe.
Un articolo sa come validare, osservare e aggiornare **se stesso**; il
confronto fra articoli, la politica di unicità dei codici e l'organizzazione
della raccolta sono responsabilità di un altro livello, che qui resta
esplicito e leggibile.

**Differenza di aliasing rispetto a U12.** In U12 `modifica_articolo`
sostituiva il record candidato nella lista; qui aggiorna **l'istanza
esistente** attraverso il suo metodo `aggiorna`. Un alias dell'istanza osserva
quindi l'aggiornamento: è una differenza reale sugli effetti sui riferimenti
esterni, da dichiarare. Il comportamento della CLI e i dati di dominio restano
equivalenti; un rifiuto lascia immutati sia i dati sia l'identità delle
istanze.

Unicità del codice: è un vincolo della **raccolta**, non del singolo
`Articolo`. Dall'identità Python è del tutto distinto: due istanze possono
condividere il codice e restare due oggetti diversi.

Ambiente: CPython sul computer. Dipende da `articolo_u13` per la classe e per
la validazione condivisa dello schema.
"""

from articolo_u13 import CAMPI_ARTICOLO, Articolo, valida_dati_articolo


def _intero_da_testo(testo, campo, riferimento):
    """Converte un campo testuale in intero, con diagnosi su campo e riferimento.

    Conversione e controllo del dominio restano **controlli distinti**: qui
    cade soltanto la conversione; il segno viene controllato dalla validazione
    dello schema.
    """
    try:
        return int(testo)
    except ValueError:
        raise ValueError(
            f"{riferimento}, campo '{campo}': il testo {testo!r} non è un intero"
        ) from None


def riga_a_articolo(riga, riferimento_riga):
    """Converte una riga di quattro campi testuali in un `Articolo` nuovo.

    `riga` è la sequenza dei campi nell'ordine dello schema, come restituita
    dal lettore CSV; `riferimento_riga` identifica la riga nei messaggi
    d'errore. Il procedimento ha tre passaggi distinti: controllo del numero
    dei campi, conversione dei campi testuali, validazione dello schema.
    Un dato malformato solleva `ValueError` con campo e riferimento, senza
    risultati parziali.
    """
    if len(riga) != len(CAMPI_ARTICOLO):
        attesi = ", ".join(CAMPI_ARTICOLO)
        raise ValueError(
            f"{riferimento_riga}: attesi {len(CAMPI_ARTICOLO)} campi ({attesi}), "
            f"ricevuti {len(riga)}"
        )
    codice = riga[0]
    descrizione = riga[1]
    quantita = _intero_da_testo(riga[2], "quantita", riferimento_riga)
    prezzo_centesimi = _intero_da_testo(riga[3], "prezzo_centesimi", riferimento_riga)
    try:
        return Articolo(codice, descrizione, quantita, prezzo_centesimi)
    except ValueError as errore:
        raise ValueError(f"{riferimento_riga}: {errore}") from None


def articolo_a_riga(articolo):
    """Restituisce i campi testuali dell'articolo nell'ordine dello schema.

    Valida i dati della proiezione esplicita `dati()` prima della conversione
    e non modifica l'articolo. I numeri diventano testo nella forma decimale
    ordinaria: la riga risultante è pronta per il record CSV.
    """
    dati = articolo.dati()
    valida_dati_articolo(
        dati["codice"],
        dati["descrizione"],
        dati["quantita"],
        dati["prezzo_centesimi"],
    )
    return [
        dati["codice"],
        dati["descrizione"],
        str(dati["quantita"]),
        str(dati["prezzo_centesimi"]),
    ]


def cerca_articolo(articoli, codice):
    """Restituisce l'indice dell'articolo con questo codice, oppure `None`.

    Il confronto è esatto e sfrutta `ha_codice`. L'indice 0 è un risultato
    valido: non usare `if indice:` per controllare l'esito della ricerca.
    La raccolta non viene modificata. La ricerca è lineare: una classe non
    cambia automaticamente il costo dell'algoritmo.
    """
    for indice, articolo in enumerate(articoli):
        if articolo.ha_codice(codice):
            return indice
    return None


def inserisci_articolo(articoli, articolo):
    """Aggiunge un articolo in fondo alla raccolta, come istanza nuova.

    L'articolo ricevuto non viene inserito così com'è: se ne costruisce una
    **nuova istanza** dai dati espliciti della proiezione, così la raccolta
    resta indipendente dall'argomento, come la copia del record in U12.
    L'unicità del codice viene controllata **prima** dell'aggiunta. Su
    successo restituisce `None`; su codice già presente solleva `ValueError` e
    la lista resta invariata.
    """
    dati = articolo.dati()
    valida_dati_articolo(
        dati["codice"],
        dati["descrizione"],
        dati["quantita"],
        dati["prezzo_centesimi"],
    )
    if cerca_articolo(articoli, dati["codice"]) is not None:
        raise ValueError(f"campo 'codice': il codice {dati['codice']!r} è già presente")
    articoli.append(Articolo(**dati))
    return None


def modifica_articolo(articoli, codice, descrizione, quantita, prezzo_centesimi):
    """Aggiorna descrizione, quantità e prezzo dell'articolo con questo codice.

    Il codice è identità dell'articolo e non viene modificato. L'aggiornamento
    viene **delegato all'istanza**, che valida il candidato completo prima di
    toccare i propri campi: un dato non valido lascia lo stato invariato e
    solleva `ValueError`. Restituisce `False` se il codice non esiste, `True`
    se l'aggiornamento è applicato.

    Rispetto a U12 l'istanza non viene sostituita ma modificata: un alias
    dell'articolo osserva i nuovi dati.
    """
    indice = cerca_articolo(articoli, codice)
    if indice is None:
        return False
    articoli[indice].aggiorna(descrizione, quantita, prezzo_centesimi)
    return True


def elimina_articolo(articoli, codice):
    """Elimina l'articolo con questo codice. Nessuna domanda all'utente.

    Restituisce `False` se il codice non esiste, `True` se l'articolo è stato
    eliminato. La conferma all'utente è responsabilità di chi presenta
    l'interfaccia, non di questa funzione.
    """
    indice = cerca_articolo(articoli, codice)
    if indice is None:
        return False
    del articoli[indice]
    return True


def riepilogo_magazzino(articoli):
    """Restituisce un record nuovo con i totali della raccolta.

    Precondizione: gli articoli sono istanze valide. Le stesse chiavi di U12 —
    `articoli`, `quantita_totale`, `valore_centesimi` — permettono il confronto
    con la versione precedente; la lista vuota produce tre zeri. La scansione
    è esplicita, prima di qualunque forma compatta.
    """
    quantita_totale = 0
    valore_centesimi = 0
    for articolo in articoli:
        dati = articolo.dati()
        quantita_totale += dati["quantita"]
        valore_centesimi += articolo.valore_centesimi()
    return {
        "articoli": len(articoli),
        "quantita_totale": quantita_totale,
        "valore_centesimi": valore_centesimi,
    }


def formatta_centesimi(centesimi):
    """Converte un importo in centesimi nella stringa monetaria in euro.

    La conversione resta visibile nel codice: `centesimi // 100` dà gli euro e
    `centesimi % 100` i centesimi residui, scritti sempre con due cifre.
    Resta una **funzione**: nessun beneficio dall'introdurre un oggetto per una
    conversione pura. Precondizione: intero non negativo.
    """
    euro = centesimi // 100
    resto = centesimi % 100
    return f"{euro},{resto:02d} €"


if __name__ == "__main__":
    # Dimostrazione minima: i due articoli canonici del capitolo.
    magazzino = [
        Articolo("007", "Vite, lunga", 4, 25),
        Articolo("012", 'Caffè "A"', 2, 350),
    ]
    print("indice di 007:", cerca_articolo(magazzino, "007"))
    print("indice di 7:  ", cerca_articolo(magazzino, "7"))
    print("indice di 999:", cerca_articolo(magazzino, "999"))
    riepilogo = riepilogo_magazzino(magazzino)
    print("riepilogo:", riepilogo)
    print("valore:", formatta_centesimi(riepilogo["valore_centesimi"]))
    try:
        inserisci_articolo(magazzino, Articolo("007", "doppione", 1, 1))
    except ValueError as errore:
        print("rifiuto:", errore)
