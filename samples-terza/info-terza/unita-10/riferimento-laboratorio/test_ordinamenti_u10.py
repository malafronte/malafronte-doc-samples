"""Suite del LAB-PY-U10 - Ordinare, contare e misurare (riferimento).

Stessa suite dello starter, con il caso L12 compilato: qui i fallimenti attesi
non esistono e tutti i casi L01-L12 devono passare. La suite resta identica per
gli altri casi: se un caso cambia fra starter e riferimento, il confronto fra le
due esecuzioni non è più significativo.

Esecuzione dalla cartella `riferimento-laboratorio/`:

    uv run --with pytest python -m pytest test_ordinamenti_u10.py -q

I test non misurano durate: verificano forma dei dati, correttezza, proprietà
di identità e coerenza dei contatori con le formule del cap. PY-14.
"""

import pytest

import conteggi_u10 as cont
import dataset_u10 as dati
import misure_u10 as mis
import ordinamenti_u10 as ordi

ORDINAMENTI = (
    ordi.insertion_sort,
    ordi.selection_sort,
    ordi.bubble_sort,
    ordi.bubble_sort_ottimizzato,
)
ORDINAMENTI_CONTATI = (
    cont.insertion_sort_con_conteggi,
    cont.selection_sort_con_conteggi,
    cont.bubble_sort_con_conteggi,
    cont.bubble_sort_ottimizzato_con_conteggi,
)

CASI = ([], [4], [5, 2, 4, 2], [1, 2, 3, 4], [4, 3, 2, 1], [2, 2, 2], [3, -1, 0, 7, 7, 2])


# --- L01 - Vuoto, singolo, contratto ---------------------------------------


@pytest.mark.parametrize("ordina", ORDINAMENTI)
@pytest.mark.parametrize("originale", [[], [4]])
def test_l01_vuoto_e_singolo(ordina, originale):
    valori = list(originale)
    identita = id(valori)
    assert ordina(valori) is None
    assert valori == sorted(originale)
    assert id(valori) == identita


# --- L02 - Il caso della previsione: [5, 2, 4, 2] ---------------------------


@pytest.mark.parametrize("ordina", ORDINAMENTI)
def test_l02_caso_della_previsione(ordina):
    valori = [5, 2, 4, 2]
    assert ordina(valori) is None
    assert valori == [2, 2, 4, 5]


# --- L03 - Permutazione e confronto con sorted ------------------------------


@pytest.mark.parametrize("ordina", ORDINAMENTI)
@pytest.mark.parametrize("originale", CASI)
def test_l03_risultato_e_permutazione(ordina, originale):
    valori = list(originale)
    assert ordina(valori) is None
    assert valori == sorted(originale)
    assert sorted(valori) == sorted(originale)
    assert len(valori) == len(originale)


@pytest.mark.parametrize("ordina", ORDINAMENTI)
@pytest.mark.parametrize("nome", dati.FAMIGLIE)
def test_l03_cinque_famiglie(ordina, nome):
    originale = dati.genera_famiglia(nome, 12)
    atteso = sorted(originale)
    valori = list(originale)
    ordina(valori)
    assert valori == atteso


def prima_componente(coppia):
    """Chiave di confronto per i record marcati: la sola prima componente."""
    return coppia[0]


# --- L04 - Record marcati e stabilità --------------------------------------


def test_l04_insertion_e_bubble_stabili():
    for ordina in (ordi.insertion_sort, ordi.bubble_sort, ordi.bubble_sort_ottimizzato):
        valori = [(2, "a"), (2, "b"), (1, "c")]
        ordina(valori, chiave=prima_componente)
        assert valori == [(1, "c"), (2, "a"), (2, "b")]


def test_l04_selection_standard_non_stabile():
    # Controesempio del capitolo, confrontati sulla sola prima componente:
    # dopo il primo scambio la coppia 2a-2b resta in ordine invertito.
    valori = [(2, "a"), (2, "b"), (1, "c")]
    ordi.selection_sort(valori, chiave=prima_componente)
    assert valori == [(1, "c"), (2, "b"), (2, "a")]
    assert [etichetta for _, etichetta in valori] == ["c", "b", "a"]


# --- L05 - Contatori sui casi n = 0, 1, 2, 4 --------------------------------


@pytest.mark.parametrize("n", [0, 1, 2, 4])
def test_l05_selection_e_bubble_semplice_conteggio_fisso(n):
    atteso = cont.formule_attese(n)["triangolare"]
    assert atteso == n * (n - 1) // 2
    for originale in (list(range(n)), list(range(n, 0, -1)), [7] * n):
        assert cont.selection_sort_con_conteggi(list(originale))["confronti"] == atteso
        assert cont.bubble_sort_con_conteggi(list(originale))["confronti"] == atteso


@pytest.mark.parametrize("n", [0, 1, 2, 4])
def test_l05_bubble_ottimizzato_e_insertion_su_ordinato(n):
    atteso = cont.formule_attese(n)["lineare_ordinato"]
    assert atteso == max(0, n - 1)
    assert cont.bubble_sort_ottimizzato_con_conteggi(list(range(n)))["confronti"] == atteso
    assert cont.insertion_sort_con_conteggi(list(range(n)))["confronti"] == atteso


# --- L06 - Insertion su lista inversa: spostamenti, non scambi -------------


@pytest.mark.parametrize("n", [0, 1, 2, 4])
def test_l06_insertion_su_inverso(n):
    registro = cont.insertion_sort_con_conteggi(list(range(n, 0, -1)))
    atteso = n * (n - 1) // 2
    assert registro["confronti"] == atteso
    assert registro["spostamenti"] == atteso
    assert registro["scambi"] == 0


# --- L07 - Bubble ottimizzato: arresto vero o falso ------------------------


def test_l07_bubble_ottimizzato_su_gia_ordinato():
    registro = cont.bubble_sort_ottimizzato_con_conteggi([1, 2, 3, 4])
    assert registro["confronti"] == 3
    assert registro["scambi"] == 0


def test_l07_bubble_ottimizzato_su_quasi_ordinato():
    registro = cont.bubble_sort_ottimizzato_con_conteggi([1, 3, 2, 4])
    assert registro["scambi"] == 1
    assert registro["confronti"] < 6  # meno della versione a passaggi fissi


def test_l07_bubble_ottimizzato_non_si_ferma_sullinverso():
    valori = [4, 3, 2, 1]
    registro = cont.bubble_sort_ottimizzato_con_conteggi(list(valori))
    assert registro["scambi"] == 6
    assert registro["confronti"] == 6


# --- L08 - Dataset: stessi originali, copie indipendenti, seme --------------


def test_l08_le_famiglie_sono_deterministiche():
    for nome in dati.FAMIGLIE:
        assert dati.genera_famiglia(nome, 10) == dati.genera_famiglia(nome, 10)


def test_l08_copie_indipendenti():
    originale = dati.genera_famiglia("inverso", 6)
    copie = dati.copie_indipendenti(originale, 4)
    assert len(copie) == 4
    assert copie == [originale] * 4
    copie[0].sort()
    assert copie[1] != copie[0]
    assert originale != copie[0]


def test_l08_costruzione_dichiarata_della_famiglia_quasi_ordinato():
    assert dati.genera_famiglia("quasi_ordinato", 4) == [1, 0, 3, 2]
    assert dati.genera_famiglia("quasi_ordinato", 3) == [0, 1, 2]
    quasi = dati.genera_famiglia("quasi_ordinato", 8)
    assert sorted(quasi) == sorted(dati.genera_famiglia("ordinato", 8))


# --- L09 - Equivalenza fra versioni con e senza contatori -------------------


@pytest.mark.parametrize("ordina, conta", list(zip(ORDINAMENTI, ORDINAMENTI_CONTATI)))
@pytest.mark.parametrize("originale", CASI)
def test_l09_stesso_risultato_e_registro_completo(ordina, conta, originale):
    atteso = sorted(originale)
    base = list(originale)
    strumentata = list(originale)
    assert ordina(base) is None
    registro = conta(strumentata)
    assert base == atteso
    assert strumentata == atteso
    assert set(registro) == {"confronti", "scambi", "spostamenti"}
    assert all(registro[voce] >= 0 for voce in registro)


# --- L10 - Misure: campioni e sintesi ---------------------------------------


def test_l10_sintesi_su_campioni_artificiali():
    sintesi = mis.sintesi_campioni([5, 1, 4, 2, 3])
    assert sintesi["mediana"] == 3
    assert sintesi["minimo"] == 1
    assert sintesi["massimo"] == 5
    assert sintesi["numero"] == 5


def test_l10_campioni_della_misura():
    originale = dati.genera_famiglia("inverso", 20)
    campioni = mis.misura_ordinamento(ordi.bubble_sort_ottimizzato, originale, ripetizioni=5)
    assert len(campioni) == 5
    assert all(c >= 0 for c in campioni)
    assert originale == dati.genera_famiglia("inverso", 20)


def test_l10_la_verifica_del_risultato_e_fuori_dal_timer():
    # La funzione di misura deve accettare anche un algoritmo che ordina
    # correttamente: se la verifica fosse dentro il timer sarebbe ancora
    # corretta, ma il tempo la includerebbe. Il contratto richiesto è che la
    # lista di riferimento non venga modificata.
    originale = dati.genera_famiglia("molti_duplicati", 16)
    copia = list(originale)
    mis.misura_ordinamento(ordi.insertion_sort, originale, ripetizioni=2, chiamate_per_lotto=3)
    assert originale == copia


# --- L11 - Tabella e metadati -----------------------------------------------


def test_l11_metadati_completi():
    meta = mis.metadati_misura()
    assert meta["timer"] == "time.perf_counter"
    assert meta["unita"] == "secondi per chiamata"
    assert meta["python"]
    assert meta["seme"] == dati.SEME


def test_l11_riga_della_tabella_leggibile():
    sintesi = mis.sintesi_campioni([0.001, 0.002, 0.0015])
    riga = mis.riga_tabella("insertion_sort", "inverso", 100, sintesi)
    assert "insertion_sort" in riga
    assert "inverso" in riga
    assert "n=100" in riga
    assert "mediana=" in riga
    assert "campioni=3" in riga


# --- L12 - Caso progettato dallo studente ----------------------------------


def _bubble_falsamente_ottimizzato(valori, chiave=None):
    """ERRORE DELIBERATO: si arresta alla prima passata che **compie** scambi.

    La condizione di arresto è invertita rispetto a `bubble_sort_ottimizzato`.
    Questa funzione deve fallire per la causa spiegata nel caso L12 e non viene
    usata da nessun altro caso della suite.
    """
    valore = (lambda elemento: elemento) if chiave is None else chiave
    n = len(valori)
    for passata in range(n - 1):
        scambi_avvenuti = False
        for j in range(0, n - 1 - passata):
            if valore(valori[j]) > valore(valori[j + 1]):
                valori[j], valori[j + 1] = valori[j + 1], valori[j]
                scambi_avvenuti = True
        if scambi_avvenuti:
            break
    return None


def test_l12_caso_progettato_dallo_studente():
    """Caso L12: l'input `[3, 2, 1]` smaschera l'arresto prematuro.

    Il caso è stato scelto perché **non** è discriminato da `[1, 2, 3]`: su una
    lista già ordinata anche la versione falsamente ottimizzata produce il
    risultato corretto. Servono invece input che richiedono almeno due passate
    **con** scambi nella prima, come `[3, 2, 1]` o `[2, 3, 1]`. La proprietà
    osservata non è il solo risultato ordinato, ma il fatto che la versione
    corretta completa tutte le passate necessarie.
    """
    assert cont.bubble_sort_ottimizzato_con_conteggi([3, 2, 1])["scambi"] == 3

    corretto = [3, 2, 1]
    ordi.bubble_sort_ottimizzato(corretto)
    assert corretto == [1, 2, 3]

    falso = [3, 2, 1]
    _bubble_falsamente_ottimizzato(falso)
    assert falso != [1, 2, 3]  # arresto prematuro: la passata era conclusa

    non_discriminante = [1, 2, 3]
    _bubble_falsamente_ottimizzato(non_discriminante)
    assert non_discriminante == [1, 2, 3]  # il caso non distingue le due versioni
