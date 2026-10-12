"""Soluzioni formative dei problemi di algoritmica — Unità 18.

Il modulo realizza gli otto problemi canonici della famiglia **Hashing,
collisioni e indici**: costruzione di chiavi con lo stesso indice,
distribuzione delle associazioni, deduplicazione, aggregazione, indice con
unicità, sequenza di verifica delle modifiche, scelta dell'indice e lettura
dei conteggi. Ogni soluzione è verificata dalla suite
`tests/test_soluzioni_u18.py`; ragionamenti completi e limiti restano nelle
soluzioni guidate della pagina della famiglia.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from __future__ import annotations

from confronto_indici_u18 import confronta_strategie
from hash_chiavi_u18 import famiglia_stesso_indice, indice_per, riepilogo_distribuzione
from indice_record_u18 import RecordMateriale, costruisci_indice, fotografia
from tabella_hash_u18 import TabellaHashConcatenata


def chiavi_stesso_indice(capacita, resto, quantita):
    """Soluzione T09: costruisce e verifica `quantita` chiavi con indice `resto`."""
    chiavi = famiglia_stesso_indice(capacita, resto, quantita)
    assert len(set(chiavi)) == len(chiavi)
    for chiave in chiavi:
        assert indice_per(chiave, capacita) == resto
    return chiavi


def distribuzione_associazioni(lunghezze):
    """Soluzione T10: riepiloga dimensione, carico, vuoti, massimo e indici del massimo."""
    return riepilogo_distribuzione(lunghezze)


def deduplica_codici(codici, capacita=5):
    """Soluzione T11: codici distinti nell'ordine della prima comparsa.

    La verifica di presenza usa la tabella studiata; il risultato conserva
    l'ordine del primo incontro, distinto dall'organizzazione dei bucket. Il
    confronto successivo con una struttura nativa appartiene alla consegna.
    """
    tabella = TabellaHashConcatenata(capacita)
    distinti = []
    for codice in codici:
        if not tabella.contiene(codice):
            tabella.assegna(codice, True)
            distinti.append(codice)
    return distinti


def aggrega_quantita(movimenti, capacita=5):
    """Soluzione T12: totale per codice con segno ammesso, zero conservato.

    Il risultato è la coppia `(totali, ordine)`: il dizionario dei totali,
    dove il totale zero resta una voce presente, e la lista dei codici
    nell'ordine della prima comparsa. La distinzione fra assenza e valore zero
    usa `contiene`, non il valore letto.
    """
    tabella = TabellaHashConcatenata(capacita)
    ordine = []
    for codice, quantita in movimenti:
        if tabella.contiene(codice):
            tabella.assegna(codice, tabella.cerca(codice) + quantita)
        else:
            tabella.assegna(codice, quantita)
            ordine.append(codice)
    return dict(tabella.coppie()), ordine


def indice_con_univita(record, queries, capacita=5):
    """Soluzione T13: indice completo e risposte a una sequenza di query.

    Un duplicato solleva `ValueError` prima della consegna; la raccolta
    sorgente resta conservata. Ogni risposta è `(codice, esito)`, dove l'esito
    è il record oppure la stringa `"assente"`.
    """
    indice = costruisci_indice(record, capacita)
    risposte = []
    for codice in queries:
        try:
            risposte.append((codice, indice.cerca(codice)))
        except KeyError:
            risposte.append((codice, "assente"))
    return fotografia(indice), risposte


def sequenza_verifica_modifiche():
    """Soluzione T14: sequenza di esempio con stati attesi e motivi.

    La sequenza riusa lo stesso bucket con collisioni deliberate e attraversa
    una crescita; ogni passo dichiara che cosa distingue. Il confronto di ogni
    passo con un `dict` di riferimento copre le associazioni ammesse, mentre
    capacità e conteggi restano propri del modello.
    """
    tabella = TabellaHashConcatenata(5)
    riferimento = {}
    passi = []
    for operazione, chiave, valore in [
        ("assegna", 12, "A"),
        ("assegna", 7, "B"),
        ("assegna", 7, "B2"),
        ("rimuovi", 12, None),
        ("assegna", 22, "C"),
        ("assegna", 17, "D"),
        ("assegna", 3, "E"),
        ("assegna", 27, "G"),
        ("assegna", 8, "F"),
    ]:
        if operazione == "assegna":
            tabella.assegna(chiave, valore)
            riferimento[chiave] = valore
            motivo = "unicità e dimensione" if chiave == 7 else "collisione conservata"
        else:
            tabella.rimuovi(chiave)
            del riferimento[chiave]
            motivo = "collegamenti della catena"
        uguali = sorted(map(repr, tabella.coppie())) == sorted(map(repr, riferimento.items()))
        passi.append(
            {
                "operazione": f"{operazione}({chiave})",
                "dimensione": len(tabella),
                "capacita": tabella.capacita,
                "coerente_con_dict": uguali,
                "motivo": motivo,
            }
        )
    return passi


def scegli_indice(numero_record, query_esatte, richieste_intervallo, inserimenti):
    """Soluzione X05: scelta motivata fra scansione, lista ordinata, BST e hash.

    La scelta non individua un vincitore universale: ogni carico dichiara
    preparazione, operazioni richieste e ipotesi. Una sola query non ripaga la
    preparazione; molte query esatte premiano l'hash; gli intervalli
    richiedono un ordine delle chiavi.
    """
    if richieste_intervallo > 0:
        if query_esatte + inserimenti == 0:
            return ("lista ordinata o BST", "i soli intervalli richiedono chiavi ordinate")
        return ("BST", "intervalli e visite ordinate con aggiornamenti dinamici")
    if query_esatte <= 1 and inserimenti == 0:
        return ("scansione", "una sola query non ripaga alcuna preparazione")
    if inserimenti > query_esatte and numero_record < 50:
        return ("scansione", "pochi record con scritture frequenti e poche letture")
    return ("hash", "molte query esatte con costo atteso limitato e preparazione lineare")


def interpreta_conteggi(coppie_distribuite, coppie_concentrate, queries, capacita=5):
    """Soluzione X06: conteggi su famiglie distribuite e concentrate.

    Le due famiglie hanno stesso `n` e stesso `m`; la tabella dei risultati
    separa generazione e misura e dichiara capacità e funzione hash. Le
    conclusioni restano limitate alle prove: osservazione di un campione,
    modello teorico e tempo del codice sono piani distinti.
    """
    distribuite = confronta_strategie(coppie_distribuite, queries, capacita)
    concentrate = confronta_strategie(coppie_concentrate, queries, capacita)
    return {
        "capacita": capacita,
        "funzione_hash": "hash_didattico con indice hash % m",
        "distribuite": [r for r in distribuite if r["strategia"] == "hash"],
        "concentrate": [r for r in concentrate if r["strategia"] == "hash"],
    }


def _record_esempio():
    """Dataset di esempio condiviso dalle prove della soluzione."""
    return [
        RecordMateriale("007", "cavetto USB", 4),
        RecordMateriale("012", "tastiera", 2),
        RecordMateriale("003", "mouse", 6),
        RecordMateriale("017", "webcam", 1),
    ]
