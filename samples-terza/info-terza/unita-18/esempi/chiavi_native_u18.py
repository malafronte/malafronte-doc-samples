"""Chiavi hashable di Python e contratto di uguaglianza — Unità 18.

Il modulo mostra con funzioni verificabili le condizioni che permettono di
ritrovare un'associazione in `dict`: chiavi uguali producono lo stesso hash,
l'hash seleziona i candidati e l'uguaglianza riconosce la chiave. Gli esempi
usano interi, stringhe, tuple di elementi hashable e una chiave di valore
immutabile definita localmente; un esempio deliberatamente difettoso mostra
come la mutazione della chiave compromette le ricerche per valore.

Ambiente: CPython sul computer. Il modulo non esegue alcuna operazione
all'importazione.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChiaveLuogo:
    """Chiave di valore immutabile con campi hashable.

    L'uguaglianza è per contenuto sui due campi e l'hash è coerente con
    l'uguaglianza: due istanze costruite con gli stessi dati selezionano la
    stessa associazione in `dict`.
    """

    nome: str
    piano: int


def associazione_con_chiave_valore():
    """Mostra due istanze uguali usate nella stessa associazione di `dict`."""
    prima = ChiaveLuogo("aula", 1)
    seconda = ChiaveLuogo("aula", 1)
    registro = {prima: "laboratorio"}
    return {
        "istanze_uguali": prima == seconda,
        "hash_coerenti": hash(prima) == hash(seconda),
        "valore_ritrovato": registro[seconda],
    }


def equivalenza_numerica():
    """Mostra l'equivalenza numerica delle chiavi `1`, `True` e `1.0` in `dict`.

    Le tre chiavi sono uguali secondo `==` e condividono l'hash: in `dict`
    occupano un'unica associazione e l'ultimo valore assegnato prevale. Il
    modello didattico del corso adotta invece chiavi di tipo esatto `int`
    oppure `str`, così l'intero `7` e la stringa `"7"` restano associazioni
    distinte.
    """
    registro = {}
    registro[1] = "intero"
    registro[True] = "booleano"
    registro[1.0] = "reale"
    return {
        "uguaglianze": (1 == True, 1 == 1.0, hash(1) == hash(True) == hash(1.0)),
        "associazioni": len(registro),
        "valore": registro[1],
    }


def tupla_con_elemento_mutabile():
    """Mostra che una tupla con un elemento mutabile non è hashable.

    L'immutabilità del contenitore non basta: l'hash della tupla dipende dagli
    hash degli elementi e una lista non fornisce un hash stabile. La tupla di
    soli elementi hashable è invece una chiave ammessa.
    """
    try:
        hash((1, [2, 3]))
        non_hashable = False
    except TypeError:
        non_hashable = True
    return {
        "tupla_con_lista_non_hashable": non_hashable,
        "tupla_hashable": hash((1, (2, 3))) == hash((1, (2, 3))),
    }


class _ChiaveMutabileDifettosa:
    """Chiave difettosa con hash legato a un campo mutabile.

    La classe serve soltanto alla diagnosi: la mutazione del campo che
    partecipa a uguaglianza e hash rompe la condizione di stabilità richiesta
    dal contenitore. La ricerca con la stessa istanza mutata può ancora
    riuscire, secondo l'hash e il percorso interno di sondaggio; una chiave
    distinta con il codice originario perde invece l'uguaglianza con quella
    conservata. La regola corretta precede l'esempio: i campi che
    partecipano a uguaglianza e hash restano stabili durante la vita della
    chiave.
    """

    def __init__(self, codice):
        self.codice = codice

    def __eq__(self, altro):
        return isinstance(altro, _ChiaveMutabileDifettosa) and self.codice == altro.codice

    def __hash__(self):
        return hash(self.codice)


def diagnosi_chiave_mutata():
    """Confronta le ricerche dopo la mutazione di una chiave difettosa.

    La ricerca per il codice originario usa un'istanza distinta, equivalente
    prima della mutazione: questa prova ha un esito determinato. Il risultato
    della ricerca con la stessa istanza mutata è invece un'osservazione del
    processo corrente, che può variare con la randomizzazione dell'hash.
    """
    chiave = _ChiaveMutabileDifettosa("007")
    equivalente = _ChiaveMutabileDifettosa("007")
    registro = {chiave: "primo"}
    trovato_prima = registro.get(chiave)
    equivalente_prima = registro.get(equivalente)
    chiave.codice = "012"
    trovato_dopo = registro.get(chiave)
    equivalente_dopo = registro.get(equivalente)
    return {
        "trovato_prima": trovato_prima,
        "trovato_dopo": trovato_dopo,
        "equivalente_prima": equivalente_prima,
        "equivalente_dopo": equivalente_dopo,
    }
