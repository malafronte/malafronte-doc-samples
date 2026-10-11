"""Prove della lista concatenata - Unità 16 (PY-30).

Le prove verificano risultati, ordine, dimensione, estremi e invarianti dopo
ogni mutazione significativa, usando la funzione autoriale
`controlla_invarianti`. La strumentazione di controllo è separata dai costi
delle operazioni della struttura.
"""

from __future__ import annotations

import pytest

from lista_concatenata_u16 import ListaConcatenata, controlla_invarianti

DATASET_DUPLICATI = [12, 7, 7, 19]


def costruisci(valori: list) -> ListaConcatenata:
    """Costruisce una lista concatenata aggiungendo in coda, con controllo finale."""
    lista = ListaConcatenata()
    for valore in valori:
        lista.aggiungi_in_coda(valore)
    assert controlla_invarianti(lista) == []
    return lista


def test_vuoto_iniziale():
    lista = ListaConcatenata()
    assert len(lista) == 0
    assert lista.a_lista() == []
    assert controlla_invarianti(lista) == []


def test_aggiunta_in_testa_da_vuoto_a_tre_valori():
    lista = ListaConcatenata()
    for valore in (19, 7, 12):  # inseriti in testa: l'ordine risultante è inverso
        lista.aggiungi_in_testa(valore)
        assert controlla_invarianti(lista) == []
    assert lista.a_lista() == [12, 7, 19]
    assert len(lista) == 3


def test_aggiunte_miste_aggiornano_entrambi_gli_estremi():
    lista = ListaConcatenata()
    lista.aggiungi_in_coda(12)
    lista.aggiungi_in_testa(7)
    lista.aggiungi_in_coda(19)
    assert lista.a_lista() == [7, 12, 19]
    assert lista._testa.valore == 7
    assert lista._coda.valore == 19
    assert controlla_invarianti(lista) == []


def test_unico_nodo_e_testa_coda_coincidenti():
    lista = costruisci([12])
    assert lista._testa is lista._coda
    assert lista._testa.successivo is None
    assert len(lista) == 1


def test_primo_e_rimuovi_primo_restituiscono_valore_e_aggiornano():
    lista = costruisci(DATASET_DUPLICATI)
    assert lista.primo() == 12
    assert controlla_invarianti(lista) == []
    assert lista.rimuovi_primo() == 12
    assert lista.a_lista() == [7, 7, 19]
    assert controlla_invarianti(lista) == []


def test_rimuovi_primo_sul_vuoto_solleva_e_conserva_lo_stato():
    lista = ListaConcatenata()
    with pytest.raises(IndexError):
        lista.rimuovi_primo()
    with pytest.raises(IndexError):
        lista.primo()
    assert len(lista) == 0
    assert controlla_invarianti(lista) == []


def test_passaggio_a_vuoto_ripristina_gli_estremi():
    lista = costruisci([12])
    assert lista.rimuovi_primo() == 12
    assert len(lista) == 0
    assert lista._testa is None and lista._coda is None
    assert controlla_invarianti(lista) == []
    lista.aggiungi_in_coda(7)  # la struttura torna utilizzabile
    assert lista.a_lista() == [7]
    assert controlla_invarianti(lista) == []


def test_rimuovi_cancella_solo_la_prima_occorrenza():
    lista = costruisci(DATASET_DUPLICATI)
    assert lista.rimuovi(7) is True
    assert lista.a_lista() == [12, 7, 19]
    assert controlla_invarianti(lista) == []


def test_rimuovi_in_coda_e_assenza_con_restituzione_booleana():
    lista = costruisci(DATASET_DUPLICATI)
    assert lista.rimuovi(19) is True
    assert lista.a_lista() == [12, 7, 7]
    assert controlla_invarianti(lista) == []
    assert lista.rimuovi(99) is False
    assert lista.a_lista() == [12, 7, 7]  # lo stato è conservato
    assert controlla_invarianti(lista) == []


def test_rimuovi_l_unico_nodo_mantiene_coerente_la_coda():
    lista = costruisci([12])
    assert lista.rimuovi(12) is True
    assert lista._testa is None and lista._coda is None
    assert controlla_invarianti(lista) == []
    lista.aggiungi_in_coda(7)  # il successivo accodamento deve funzionare
    assert lista.a_lista() == [7]


def test_nodi_distinti_possono_conservare_valori_uguali():
    lista = costruisci([7, 7])
    assert lista._testa is not lista._testa.successivo
    assert lista._testa.valore == lista._testa.successivo.valore


def test_contiene_e_accesso_per_posizione_ai_confini():
    lista = costruisci(DATASET_DUPLICATI)
    assert lista.contiene(12) is True
    assert lista.contiene(7) is True
    assert lista.contiene(99) is False
    assert lista.valore_in_posizione(0) == 12
    assert lista.valore_in_posizione(3) == 19
    with pytest.raises(IndexError):
        lista.valore_in_posizione(4)
    with pytest.raises(IndexError):
        lista.valore_in_posizione(-1)


def test_accesso_per_posizione_rifiuta_tipo_errato_incluso_bool():
    lista = costruisci([12])
    with pytest.raises(TypeError):
        lista.valore_in_posizione(True)  # bool è sottoclasse di int, ma non è ammesso
    with pytest.raises(TypeError):
        lista.valore_in_posizione("0")


def test_dati_falsi_e_none_sono_valori_legittimi():
    lista = costruisci([0, False, None, 7])
    assert lista.contiene(0) is True
    assert lista.contiene(None) is True
    assert lista.valore_in_posizione(2) is None
    assert lista.rimuovi(None) is True
    assert lista.a_lista() == [0, False, 7]
    assert controlla_invarianti(lista) == []


def test_a_lista_restituisce_contenitore_indipendente_con_valori_condivisi():
    contenuto = ["registro"]
    lista = costruisci([contenuto, 12])
    copia = lista.a_lista()
    copia.append("estraneo")
    assert lista.a_lista() == [["registro"], 12]
    contenuto.append("aggiunto")  # la mutazione del valore è visibile da entrambi i riferimenti
    assert lista.a_lista() == [["registro", "aggiunto"], 12]


def test_inversione_conserva_nodi_dimensione_e_valori():
    lista = costruisci(DATASET_DUPLICATI)
    nodi_prima = []
    corrente = lista._testa
    while corrente is not None:
        nodi_prima.append(id(corrente))
        corrente = corrente.successivo
    lista.inverti()
    assert lista.a_lista() == [19, 7, 7, 12]
    assert len(lista) == 4
    nodi_dopo = []
    corrente = lista._testa
    while corrente is not None:
        nodi_dopo.append(id(corrente))
        corrente = corrente.successivo
    assert nodi_dopo == list(reversed(nodi_prima))  # stessi nodi, ordine inverso
    assert controlla_invarianti(lista) == []
    lista.inverti()  # la doppia inversione ripristina l'ordine
    assert lista.a_lista() == DATASET_DUPLICATI
    assert controlla_invarianti(lista) == []


def test_inversione_su_vuoto_e_nodo_unico():
    vuota = ListaConcatenata()
    vuota.inverti()
    assert vuota.a_lista() == []
    assert controlla_invarianti(vuota) == []
    unica = costruisci([12])
    unica.inverti()
    assert unica.a_lista() == [12]
    assert unica._testa is unica._coda
    assert controlla_invarianti(unica) == []


def test_contenitori_indipendenti():
    prima = costruisci([12, 7])
    seconda = costruisci([19])
    prima.rimuovi_primo()
    assert seconda.a_lista() == [19]
    assert controlla_invarianti(prima) == []
    assert controlla_invarianti(seconda) == []


def test_sequenza_intercalata_lunga_conserva_gli_invarianti():
    lista = ListaConcatenata()
    atteso = []
    for valore in range(1, 8):
        lista.aggiungi_in_coda(valore * 10)
        atteso.append(valore * 10)
        assert controlla_invarianti(lista) == []
    for valore in (30, 50, 10):
        assert lista.rimuovi(valore) is True
        atteso.remove(valore)
        assert controlla_invarianti(lista) == []
    lista.aggiungi_in_testa(5)
    atteso.insert(0, 5)
    lista.inverti()
    atteso.reverse()
    assert lista.a_lista() == atteso
    assert controlla_invarianti(lista) == []
