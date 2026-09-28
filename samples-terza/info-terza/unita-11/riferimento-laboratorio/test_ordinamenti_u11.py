"""Suite pubblica del LAB-PY-U11 - Estendere e verificare il confronto.

I casi L01-L12 sono **comportamenti** da verificare, non una traccia di
soluzione: la suite non contiene il corpo di nessuna funzione. Con lo starter
incompleto i fallimenti attesi riguardano soltanto i punti lasciati allo
studente - i corpi delle quattro funzioni, la strumentazione, la regione
cronometrata, la misura delle sequenze di ricerche e il caso L12 - e mai un
import mancante o una fixture errata.

La raccolta deve partire senza prompt e senza misure all'import:

    uv run pytest --collect-only -q programmi/test_ordinamenti_u11.py
    uv run pytest -q programmi/test_ordinamenti_u11.py

I test non misurano durate: verificano forma dei dati, correttezza, proprietà di
identità e coerenza dei contatori con le formule del cap. PY-15.
"""

import pytest

import conteggi_u11 as cont
import dataset_u11 as dati
import misure_u11 as mis
import ordinamenti_u11 as ordi
from ordinamenti_elementari_u11 import (
    bubble_sort,
    bubble_sort_ottimizzato,
    insertion_sort,
    selection_sort,
)
from ricerche_u11 import cerca_dicotomica, cerca_lineare

ORDINAMENTI = (ordi.merge_sort, ordi.quick_sort)
ELEMENTARI = (insertion_sort, selection_sort, bubble_sort, bubble_sort_ottimizzato)
CASI = ([], [4], [5, 2, 4, 2], [1, 2, 3, 4], [4, 3, 2, 1], [2, 2, 2], [3, -1, 0, 7, 7, 2])


def prima_componente(coppia):
    """Chiave dei record marcati: la sola componente numerica."""
    return coppia[0]


# --- L01 - Vuoto e singolo, contratti distinti ------------------------------


@pytest.mark.parametrize("originale", [[], [4]])
def test_l01_vuoto_e_singolo_merge_sort(originale):
    risultato = ordi.merge_sort(originale)
    assert risultato == sorted(originale)
    assert risultato is not originale


@pytest.mark.parametrize("originale", [[], [4]])
def test_l01_vuoto_e_singolo_quick_sort(originale):
    valori = list(originale)
    identita = id(valori)
    assert ordi.quick_sort(valori) is None
    assert valori == sorted(originale)
    assert id(valori) == identita


def test_l01_vuoto_e_singolo_fusione():
    assert ordi.fondi_ordinate([], []) == []
    assert ordi.fondi_ordinate([], [4]) == [4]
    assert ordi.fondi_ordinate([4], []) == [4]


# --- L02 - Il caso della previsione: [5, 2, 4, 2] ---------------------------


@pytest.mark.parametrize("ordina", ORDINAMENTI)
def test_l02_caso_della_previsione(ordina):
    valori = [5, 2, 4, 2]
    risultato = ordina(valori)
    assert (risultato if risultato is not None else valori) == [2, 2, 4, 5]


def test_l02_fusione_della_previsione():
    assert ordi.fondi_ordinate([1, 3, 5], [2, 3, 6]) == [1, 2, 3, 3, 5, 6]


# --- L03 - Permutazione e confronto con sorted ------------------------------


@pytest.mark.parametrize("ordina", ORDINAMENTI)
@pytest.mark.parametrize("originale", CASI)
def test_l03_risultato_e_permutazione(ordina, originale):
    valori = list(originale)
    risultato = ordina(valori)
    effettivo = valori if risultato is None else risultato
    assert effettivo == sorted(originale)
    assert sorted(effettivo) == sorted(originale)


@pytest.mark.parametrize("ordina", ORDINAMENTI)
@pytest.mark.parametrize("nome", dati.FAMIGLIE)
def test_l03_cinque_famiglie(ordina, nome):
    originale = dati.genera_famiglia(nome, 12)
    valori = list(originale)
    risultato = ordina(valori)
    effettivo = valori if risultato is None else risultato
    assert effettivo == sorted(originale)


# --- L04 - Effetti: mutazione, ritorno, identità ----------------------------


def test_l04_merge_sort_non_modifica_e_restituisce_lista_nuova():
    originale = [5, 2, 4, 2]
    atteso = list(originale)
    risultato = ordi.merge_sort(originale)
    assert originale == atteso
    assert risultato is not originale


def test_l04_quick_sort_modifica_e_restituisce_none():
    valori = [5, 2, 4, 2]
    identita = id(valori)
    assert ordi.quick_sort(valori) is None
    assert valori == [2, 2, 4, 5]
    assert id(valori) == identita


def test_l04_fusione_non_modifica_gli_ingressi():
    sinistra = [1, 3]
    destra = [2]
    risultato = ordi.fondi_ordinate(sinistra, destra)
    assert sinistra == [1, 3] and destra == [2]
    assert risultato is not sinistra and risultato is not destra


# --- L05 - Stabilità e valori uguali ---------------------------------------


def test_l05_merge_sort_e_stabile_su_record_marcati():
    marcati = [(2, "a"), (1, "b"), (2, "c"), (1, "d"), (2, "e")]
    ordinati = ordi.merge_sort(marcati, chiave=prima_componente)
    assert ordinati == [(1, "b"), (1, "d"), (2, "a"), (2, "c"), (2, "e")]


def test_l05_quick_sort_non_e_stabile_su_record_marcati():
    marcati = [(2, "a"), (2, "b"), (1, "c")]
    ordi.quick_sort(marcati, chiave=prima_componente)
    assert marcati == [(1, "c"), (2, "b"), (2, "a")]


def test_l05_fusione_stabile_a_parita():
    sinistra = [(2, "a"), (2, "b")]
    destra = [(2, "c")]
    risultato = ordi.fondi_ordinate(sinistra, destra, chiave=prima_componente)
    assert [marcatore for _, marcatore in risultato] == ["a", "b", "c"]


# --- L06 - Partizione: indici, intervalli, elementi esterni -----------------


def test_l06_pivot_nella_posizione_definitiva():
    valori = [7, 2, 9, 4, 6, 1, 8]
    originale = list(valori)
    pivot_finale = ordi.partiziona_lomuto(valori, 1, 5)
    chiave_pivot = originale[5]
    assert valori[pivot_finale] == chiave_pivot
    assert all(valori[i] <= chiave_pivot for i in range(1, pivot_finale))
    assert all(valori[i] > chiave_pivot for i in range(pivot_finale + 1, 6))
    assert (valori[0], valori[6]) == (originale[0], originale[6])
    assert sorted(valori) == sorted(originale)


def test_l06_intervalli_brevi_e_pivot_estremi():
    crescente = [1, 2, 3, 4]
    assert ordi.partiziona_lomuto(crescente, 0, 3) == 3
    decrescente = [4, 3, 2, 1]
    assert ordi.partiziona_lomuto(decrescente, 0, 3) == 0
    coppia = [2, 1]
    assert ordi.partiziona_lomuto(coppia, 0, 1) == 0
    assert ordi.partiziona_lomuto([5], 0, 0) == 0


# --- L07 - Casi sfavorevoli e profondità -----------------------------------


@pytest.mark.parametrize("valori", [[0, 1, 2, 3, 4], [4, 3, 2, 1, 0], [2, 2, 2, 2, 2]])
def test_l07_casi_sfavorevoli_profondita_lineare(valori):
    registro = cont.quick_sort_con_conteggi(list(valori))
    assert registro["profondita_massima"] == len(valori)


def test_l07_profondita_merge_sort_logaritmica():
    registro = cont.merge_sort_con_conteggi(dati.genera_famiglia("ordinato", 8))
    assert registro["profondita_massima"] == 4
    assert registro["copie"] == cont.copie_attese_merge_sort(8)


# --- L08 - Dataset: determinismo, copie, costruzione dichiarata -------------


def test_l08_le_famiglie_sono_deterministiche():
    for nome in dati.FAMIGLIE:
        assert dati.genera_famiglia(nome, 9) == dati.genera_famiglia(nome, 9)


def test_l08_copie_indipendenti():
    originale = dati.genera_famiglia("pseudo_casuale", 10)
    copie = dati.copie_indipendenti(originale, 3)
    assert len(copie) == 3
    copie[0][0] = 999
    assert copie[1] == originale
    assert copie[2] == originale


def test_l08_costruzione_dichiarata_della_famiglia_quasi_ordinato():
    assert dati.genera_famiglia("quasi_ordinato", 6) == [1, 0, 2, 4, 3, 5]
    assert dati.genera_famiglia("quasi_ordinato", 3) == [0, 1, 2]


# --- L09 - Conteggi: equivalenza e formule ---------------------------------


@pytest.mark.parametrize("originale", CASI)
def test_l09_stesso_risultato_e_registro_completo(originale):
    atteso = sorted(originale)
    base = list(originale)
    strumentata = list(originale)

    risultato_base = ordi.merge_sort(base)
    registro_merge = cont.merge_sort_con_conteggi(strumentata)
    assert risultato_base == atteso
    assert registro_merge["risultato"] == atteso
    assert set(registro_merge) == {"risultato", "confronti", "copie", "profondita_massima"}

    in_place = list(originale)
    contata = list(originale)
    ordi.quick_sort(in_place)
    registro_quick = cont.quick_sort_con_conteggi(contata)
    assert in_place == atteso
    assert contata == atteso
    assert set(registro_quick) == {"confronti", "scambi", "copie", "profondita_massima"}
    assert registro_quick["copie"] == 0


def test_l09_conteggi_attesi_di_fusione_e_merge_sort():
    registro_fusione = cont.fondi_ordinate_con_conteggi([1, 3, 5], [2, 3, 6])
    assert registro_fusione["risultato"] == [1, 2, 3, 3, 5, 6]
    assert registro_fusione["confronti"] <= cont.confronti_massimi_fusione(3, 3)
    assert registro_fusione["copie"] == 6

    registro_merge = cont.merge_sort_con_conteggi([5, 2, 4, 2])
    assert registro_merge["copie"] == cont.copie_attese_merge_sort(4)

    registro_partizione = cont.partiziona_lomuto_con_conteggi([5, 2, 4, 2], 0, 3)
    assert registro_partizione["confronti"] == 3
    assert set(registro_partizione) == {"pivot_finale", "confronti", "scambi"}


# --- L10 - Misure: campioni e sintesi --------------------------------------


def test_l10_sintesi_su_campioni_artificiali():
    sintesi = mis.sintesi_campioni([5, 1, 4, 2, 3])
    assert sintesi["mediana"] == 3
    assert sintesi["minimo"] == 1
    assert sintesi["massimo"] == 5
    assert sintesi["numero"] == 5


def test_l10_campioni_della_misura_su_effetti_diversi():
    originale = dati.genera_famiglia("inverso", 20)
    atteso = list(originale)
    campioni_in_place = mis.misura_ordinamento(ordi.quick_sort, originale, ripetizioni=5)
    campioni_nuova = mis.misura_ordinamento(ordi.merge_sort, originale, ripetizioni=5)
    campioni_elementare = mis.misura_ordinamento(insertion_sort, originale, ripetizioni=5, chiamate_per_lotto=3)
    for campioni in (campioni_in_place, campioni_nuova, campioni_elementare):
        assert len(campioni) == 5
        assert all(c >= 0 for c in campioni)
    assert originale == atteso


@pytest.mark.parametrize("ordina", ELEMENTARI)
def test_l10_gli_ordinamenti_elementari_confermano_il_protocollo(ordina):
    originale = dati.genera_famiglia("quasi_ordinato", 12)
    atteso = list(originale)
    campioni = mis.misura_ordinamento(ordina, originale, ripetizioni=2)
    assert len(campioni) == 2
    assert originale == atteso


def test_l10_sequenza_di_ricerche_dopo_la_preparazione():
    originale = dati.genera_famiglia("inverso", 60)
    preparata = sorted(originale)
    assert originale != preparata  # la preparazione dell'ordine è un'operazione a sé
    bersagli = [preparata[5], preparata[30], 999999]
    campioni = mis.misura_sequenza_ricerche(cerca_lineare, preparata, bersagli, ripetizioni=2)
    campioni_dicotomica = mis.misura_sequenza_ricerche(cerca_dicotomica, preparata, bersagli, ripetizioni=2)
    for campioni_attuali in (campioni, campioni_dicotomica):
        assert len(campioni_attuali) == 2
        assert all(c >= 0 for c in campioni_attuali)


def test_l10_la_verifica_del_risultato_e_fuori_dal_timer():
    # Con una procedura che ordina male la misura deve rifiutare il campione:
    # la verifica è parte del protocollo e non può essere omessa per velocità.
    def ordina_male(valori):
        valori.reverse()
        return None

    with pytest.raises(AssertionError):
        mis.misura_ordinamento(ordina_male, [1, 2, 3], ripetizioni=1)


# --- L11 - Tabella e metadati ----------------------------------------------


def test_l11_metadati_completi():
    meta = mis.metadati_misura()
    assert meta["timer"] == "time.perf_counter"
    assert meta["unita"] == "secondi per chiamata"
    assert meta["python"]
    assert meta["seme"] == dati.SEME


def test_l11_riga_della_tabella_leggibile():
    sintesi = mis.sintesi_campioni([0.001, 0.002, 0.0015])
    riga = mis.riga_tabella("merge_sort", "inverso", 100, sintesi)
    assert "merge_sort" in riga
    assert "inverso" in riga
    assert "n=100" in riga
    assert "mediana=" in riga
    assert "campioni=3" in riga


# --- L12 - Caso progettato dallo studente ----------------------------------


def test_l12_caso_progettato_dallo_studente():
    """Caso compilato nel riferimento: fusione con pari sui due lati e resto finale.

    Discrimina insieme tre difetti che gli altri casi lasciano passare: una
    fusione che usa `<` invece di `<=` e inverte l'ordine dei pari, una che
    dimentica il **resto** del lato sinistro quando il destro si esaurisce e un
    contatore che non considera il confronto falso. La previsione, verificata a
    mano, è: risultato `[(2, 'a'), (2, 'c'), (3, 'd'), (4, 'b')]`, `confronti = 3`
    (= `a + b - 1`, perché l'ultimo elemento entra senza confronto) e `copie = 4`.
    """
    registro = cont.fondi_ordinate_con_conteggi(
        [(2, "a"), (4, "b")], [(2, "c"), (3, "d")], chiave=prima_componente
    )
    assert registro["risultato"] == [(2, "a"), (2, "c"), (3, "d"), (4, "b")]
    assert registro["confronti"] == 3 == cont.confronti_massimi_fusione(2, 2)
    assert registro["copie"] == 4
