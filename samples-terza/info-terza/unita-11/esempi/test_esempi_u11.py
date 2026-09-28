"""Suite di verifica dei sorgenti d'esempio dell'Unità 11.

I test controllano gli attesi dichiarati nel capitolo PY-15 e le proprietà dei
moduli `merge_quick_u11`, `conteggi_u11` e `misure_u11`: risultati uguali a
`sorted`, effetti sull'ingresso, stabilità della fusione e instabilità della
partizione, invarianti degli indici, formule dei conteggi, profondità dello
stack e protocollo di misura.

Esecuzione dalla cartella `unita-11/`:

    uv run --with pytest python -m pytest esempi/test_esempi_u11.py -q

La suite è deterministica: non misura durate reali e non dipende dal caso.
"""

import pytest

from conteggi_u11 import (
    confronti_massimi_fusione,
    copie_attese_merge_sort,
    fondi_ordinate_con_conteggi,
    merge_sort_con_conteggi,
    partiziona_lomuto_con_conteggi,
    quick_sort_con_conteggi,
)
from merge_quick_u11 import fondi_ordinate, merge_sort, partiziona_lomuto, quick_sort
from misure_u11 import (
    FAMIGLIE,
    cerca_dicotomica,
    cerca_lineare,
    copie_indipendenti,
    genera_famiglia,
    metadati_misura,
    misura_ordinamento,
    misura_ricerca,
    misura_sequenza_ricerche,
    riga_tabella,
    sintesi_campioni,
)


def prima_componente(coppia):
    """Chiave di confronto dei record marcati: la sola componente numerica."""
    return coppia[0]


# ---------------------------------------------------------------------------
# Fusione
# ---------------------------------------------------------------------------


def test_fusione_di_due_liste_vuote():
    assert fondi_ordinate([], []) == []


def test_fusione_con_un_lato_vuoto():
    assert fondi_ordinate([], [2, 4]) == [2, 4]
    assert fondi_ordinate([1, 3], []) == [1, 3]


def test_fusione_di_base_e_parita_prende_la_sinistra():
    assert fondi_ordinate([1, 3, 5], [2, 3, 6]) == [1, 2, 3, 3, 5, 6]


def test_fusione_restituisce_lista_distinta_da_entrambi_gli_ingressi():
    sinistra = [1, 3]
    destra = [2]
    risultato = fondi_ordinate(sinistra, destra)
    assert risultato is not sinistra
    assert risultato is not destra


@pytest.mark.parametrize("sinistra, destra", [
    ([], []),
    ([], [2, 4]),
    ([1, 3], []),
    ([1, 3, 5], [2, 3, 6]),
    ([1, 2], [3, 4]),
    ([3, 4], [1, 2]),
    ([2, 2], [2, 2]),
])
def test_fusione_coincide_con_sorted_e_non_modifica_gli_ingressi(sinistra, destra):
    originale_sinistra = list(sinistra)
    originale_destra = list(destra)
    risultato = fondi_ordinate(sinistra, destra)
    assert risultato == sorted(sinistra + destra)
    assert sinistra == originale_sinistra
    assert destra == originale_destra


@pytest.mark.parametrize("a, b", [(0, 0), (0, 4), (4, 0), (1, 1), (3, 3), (5, 2)])
def test_confronti_della_fusione_entro_il_limite(a, b):
    sinistra = list(range(0, 2 * a, 2))
    destra = list(range(0, 2 * b, 2))
    registro = fondi_ordinate_con_conteggi(sinistra, destra)
    assert registro["confronti"] <= confronti_massimi_fusione(a, b)
    assert registro["copie"] == a + b
    assert registro["risultato"] == sorted(sinistra + destra)


def test_confronti_fusione_con_un_lato_vuoto_sono_zero():
    assert fondi_ordinate_con_conteggi([], [1, 2, 3])["confronti"] == 0
    assert fondi_ordinate_con_conteggi([1, 2, 3], [])["confronti"] == 0


def test_confronti_massimi_fusione_rifiuta_lunghezze_negative():
    with pytest.raises(ValueError):
        confronti_massimi_fusione(-1, 3)


def test_fusione_stabile_su_record_marcati():
    sinistra = [(2, "a"), (2, "b")]
    destra = [(2, "c")]
    risultato = fondi_ordinate(sinistra, destra, chiave=prima_componente)
    assert [marcatore for _, marcatore in risultato] == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# MergeSort
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("valori", [
    [],
    [7],
    [5, 2, 4, 2],
    [1, 2, 3, 4],
    [4, 3, 2, 1],
    [-3, -1, -2, 0],
])
def test_merge_sort_restituisce_lista_nuova_e_non_modifica_l_ingresso(valori):
    originale = list(valori)
    risultato = merge_sort(valori)
    assert risultato == sorted(originale)
    assert valori == originale
    assert risultato is not valori


@pytest.mark.parametrize("nome", FAMIGLIE)
@pytest.mark.parametrize("n", [0, 1, 2, 5, 8])
def test_merge_sort_coincide_con_sorted_su_cinque_famiglie(nome, n):
    originale = genera_famiglia(nome, n)
    assert merge_sort(originale) == sorted(originale)


def test_merge_sort_e_stabile_su_record_marcati():
    marcati = [(2, "a"), (1, "b"), (2, "c"), (1, "d"), (2, "e")]
    ordinati = merge_sort(marcati, chiave=prima_componente)
    assert ordinati == [(1, "b"), (1, "d"), (2, "a"), (2, "c"), (2, "e")]
    assert marcati == [(2, "a"), (1, "b"), (2, "c"), (1, "d"), (2, "e")]


@pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 5, 7, 8, 16])
def test_copie_merge_sort_corrispondono_al_registro(n):
    valori = genera_famiglia("pseudo_casuale", n)
    registro = merge_sort_con_conteggi(valori)
    assert registro["copie"] == copie_attese_merge_sort(n)


def test_copie_attese_merge_sort_potenza_di_due():
    for k in range(0, 6):
        n = 2 ** k
        assert copie_attese_merge_sort(n) == 2 * n * k + n


def test_copie_attese_merge_sort_rifiuta_lunghezze_negative():
    with pytest.raises(ValueError):
        copie_attese_merge_sort(-2)


@pytest.mark.parametrize("n, attesa", [(0, 1), (1, 1), (2, 2), (4, 3), (8, 4)])
def test_profondita_merge_sort_su_potenze_di_due(n, attesa):
    registro = merge_sort_con_conteggi(genera_famiglia("ordinato", n))
    assert registro["profondita_massima"] == attesa


# ---------------------------------------------------------------------------
# Partizione
# ---------------------------------------------------------------------------


def test_partiziona_colloca_il_pivot_in_posizione_definitiva():
    valori = [7, 2, 9, 4, 6, 1, 8]
    originale = list(valori)
    sinistra, destra = 1, 5
    pivot_finale = partiziona_lomuto(valori, sinistra, destra)
    chiave_pivot = originale[destra]
    assert valori[pivot_finale] == chiave_pivot
    assert all(valori[i] <= chiave_pivot for i in range(sinistra, pivot_finale))
    assert all(valori[i] > chiave_pivot for i in range(pivot_finale + 1, destra + 1))
    assert sorted(valori) == sorted(originale)
    assert valori[0] == originale[0] and valori[6] == originale[6]


def test_partiziona_manda_uguali_nel_lato_sinistro():
    valori = [3, 1, 3, 2, 3]
    pivot_finale = partiziona_lomuto(valori, 0, len(valori) - 1)
    assert pivot_finale == 4
    assert valori == [3, 1, 3, 2, 3]


def test_partiziona_non_modifica_elementi_fuori_dall_intervallo():
    valori = [11, 5, 3, 8, 2, 13]
    fuori = (valori[0], valori[5])
    partiziona_lomuto(valori, 1, 4)
    assert (valori[0], valori[5]) == fuori


@pytest.mark.parametrize("n", [1, 2, 3, 6])
def test_partiziona_preserva_il_multinsieme(n):
    valori = genera_famiglia("pseudo_casuale", n)
    originale = list(valori)
    pivot_finale = partiziona_lomuto(valori, 0, n - 1)
    assert sorted(valori) == sorted(originale)
    assert 0 <= pivot_finale < n
    assert valori[pivot_finale] == originale[n - 1]


def test_partiziona_con_pivot_minimo_e_massimo():
    crescente = [1, 2, 3, 4]
    assert partiziona_lomuto(crescente, 0, 3) == 3
    decrescente = [4, 3, 2, 1]
    assert partiziona_lomuto(decrescente, 0, 3) == 0


def test_partiziona_non_e_stabile_su_record_marcati():
    marcati = [(2, "a"), (2, "b"), (1, "c")]
    pivot_finale = partiziona_lomuto(marcati, 0, 2, chiave=prima_componente)
    assert marcati == [(1, "c"), (2, "b"), (2, "a")]
    assert pivot_finale == 0


def test_conteggi_della_partizione_corrispondono_agli_elementi_non_pivot():
    valori = [7, 2, 9, 4, 6, 1, 8]
    registro = partiziona_lomuto_con_conteggi(valori, 1, 5)
    assert registro["pivot_finale"] == 1
    assert registro["confronti"] == 4
    assert registro["scambi"] >= 0


# ---------------------------------------------------------------------------
# QuickSort
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("valori", [
    [],
    [7],
    [2, 1],
    [1, 2],
    [5, 2, 4, 2],
    [1, 2, 3, 4],
    [4, 3, 2, 1],
    [-3, -1, -2, 0],
])
def test_quick_sort_ordina_sul_posto_e_restituisce_none(valori):
    originale = list(valori)
    esito = quick_sort(valori)
    assert esito is None
    assert valori == sorted(originale)


@pytest.mark.parametrize("nome", FAMIGLIE)
@pytest.mark.parametrize("n", [0, 1, 2, 5, 8])
def test_quick_sort_coincide_con_sorted_su_cinque_famiglie(nome, n):
    valori = genera_famiglia(nome, n)
    originale = list(valori)
    quick_sort(valori)
    assert valori == sorted(originale)


def test_quick_sort_non_e_stabile_su_record_marcati():
    marcati = [(2, "a"), (2, "b"), (1, "c")]
    quick_sort(marcati, chiave=prima_componente)
    assert marcati == [(1, "c"), (2, "b"), (2, "a")]


def test_quick_sort_ordina_record_con_chiave():
    registro = [("007", 450), ("003", 200), ("011", 450), ("009", 1200)]
    originale = list(registro)
    quick_sort(registro, chiave=lambda record: record[1])
    assert registro == [("003", 200), ("007", 450), ("011", 450), ("009", 1200)]
    assert sorted(registro) == sorted(originale)


@pytest.mark.parametrize("valori", [
    [0, 1, 2, 3, 4],
    [4, 3, 2, 1, 0],
    [2, 2, 2, 2, 2],
])
def test_casi_sfavorevoli_hanno_profondita_lineare(valori):
    registro = quick_sort_con_conteggi(list(valori))
    assert registro["profondita_massima"] == len(valori)
    assert registro["copie"] == 0


def test_profondita_quick_sort_su_caso_bilanciato():
    valori = [3, 1, 4, 1, 5, 9, 2, 6]
    registro = quick_sort_con_conteggi(valori)
    assert registro["profondita_massima"] < len(valori)
    assert valori == sorted(valori)


def test_quick_sort_su_intervalli_di_lunghezza_zero_uno_due():
    vuoto = []
    quick_sort(vuoto)
    assert vuoto == []
    singolo = [5]
    quick_sort(singolo)
    assert singolo == [5]
    coppia = [2, 1]
    quick_sort(coppia)
    assert coppia == [1, 2]


# ---------------------------------------------------------------------------
# Equivalenza fra versioni con e senza contatori
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("valori", [
    [],
    [7],
    [5, 2, 4, 2],
    [1, 3, 5, 2, 3, 6],
])
def test_le_varianti_contate_ordinano_como_il_riferimento(valori):
    atteso = merge_sort(valori)
    ancora_integro = list(valori)
    registro_merge = merge_sort_con_conteggi(valori)
    assert registro_merge["risultato"] == atteso
    assert valori == ancora_integro

    in_place = list(valori)
    quick_sort(in_place)
    contata = list(valori)
    registro_quick = quick_sort_con_conteggi(contata)
    assert contata == in_place
    assert registro_quick["copie"] == 0


def test_fusione_contata_coincide_con_la_fusione():
    registro = fondi_ordinate_con_conteggi([1, 3, 5], [2, 3, 6])
    assert registro["risultato"] == fondi_ordinate([1, 3, 5], [2, 3, 6])
    assert registro["copie"] == 6


# ---------------------------------------------------------------------------
# Protocollo di misura
# ---------------------------------------------------------------------------


def test_misura_ordinamento_accetta_effetti_diversi():
    originale = genera_famiglia("pseudo_casuale", 50)
    in_place = misura_ordinamento(quick_sort, originale, ripetizioni=3)
    nuova_lista = misura_ordinamento(merge_sort, originale, ripetizioni=3)
    con_sorted = misura_ordinamento(lambda valori: sorted(valori), originale, ripetizioni=3)
    for campioni in (in_place, nuova_lista, con_sorted):
        assert len(campioni) == 3
        assert all(campione > 0 for campione in campioni)


def test_misura_ordinamento_non_modifica_originale():
    originale = genera_famiglia("inverso", 20)
    atteso = list(originale)
    misura_ordinamento(quick_sort, originale, ripetizioni=2)
    misura_ordinamento(merge_sort, originale, ripetizioni=2)
    assert originale == atteso


def test_misura_ordinamento_rileva_un_risultato_sbagliato():
    def ordina_male(valori):
        valori.reverse()
        return None

    with pytest.raises(AssertionError):
        misura_ordinamento(ordina_male, [1, 2, 3], ripetizioni=1)


def test_misura_ordinamento_richiede_almeno_un_campione():
    with pytest.raises(ValueError):
        misura_ordinamento(quick_sort, [2, 1], ripetizioni=0)


def test_sintesi_campioni_su_campioni_artificiali():
    sintesi = sintesi_campioni([0.3, 0.1, 0.2, 0.4])
    assert sintesi["numero"] == 4
    assert sintesi["minimo"] == 0.1
    assert sintesi["mediana"] == 0.25
    assert sintesi["massimo"] == 0.4
    assert sintesi["campioni"] == [0.1, 0.2, 0.3, 0.4]


def test_sintesi_campioni_rifiuta_lista_vuota():
    with pytest.raises(ValueError):
        sintesi_campioni([])


def test_metadati_completi():
    metadati = metadati_misura()
    assert metadati["timer"] == "time.perf_counter"
    assert metadati["unita"] == "secondi per chiamata"
    assert metadati["seme"] == 20260927
    assert "python" in metadati and "piattaforma" in metadati


def test_riga_tabella_leggibile():
    riga = riga_tabella("merge_sort", "ordinato", 100, sintesi_campioni([0.01, 0.02, 0.03]))
    assert "merge_sort" in riga
    assert "ordinato" in riga
    assert "n=100" in riga
    assert "mediana=" in riga and "min=" in riga and "max=" in riga


def test_misura_ricerca_conferma_primo_indice():
    ordinata = [1, 3, 3, 3, 8]
    campioni = misura_ricerca(cerca_dicotomica, ordinata, 3, ripetizioni=2)
    assert len(campioni) == 2
    assert cerca_dicotomica(ordinata, 3) == 1
    assert cerca_dicotomica(ordinata, 7) is None
    assert cerca_lineare(ordinata, 3) == 1


def test_misura_sequenza_ricerche_somma_le_interrogazioni():
    originale = genera_famiglia("pseudo_casuale", 200)
    ordinata = sorted(originale)
    bersagli = [ordinata[10], ordinata[20], 999999]
    campioni = misura_sequenza_ricerche(cerca_lineare, ordinata, bersagli, ripetizioni=2)
    assert len(campioni) == 2
    assert all(campione > 0 for campione in campioni)


def test_misura_sequenza_ricerche_richiede_almeno_una_interrogazione():
    with pytest.raises(ValueError):
        misura_sequenza_ricerche(cerca_lineare, [1, 2, 3], [], ripetizioni=1)


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------


def test_le_famiglie_sono_deterministiche():
    for nome in FAMIGLIE:
        assert genera_famiglia(nome, 7) == genera_famiglia(nome, 7)


def test_copie_indipendenti_sono_separate():
    originale = genera_famiglia("pseudo_casuale", 10)
    copie = copie_indipendenti(originale, 3)
    assert len(copie) == 3
    copie[0].append(999)
    assert copie[1] == originale
    assert len(copie[1]) == 10


def test_costruzione_dichiarata_della_famiglia_quasi_ordinato():
    valori = genera_famiglia("quasi_ordinato", 6)
    atteso = [1, 0, 2, 4, 3, 5]
    assert valori == atteso
