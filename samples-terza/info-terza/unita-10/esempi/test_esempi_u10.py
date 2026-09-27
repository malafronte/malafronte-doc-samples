"""Suite di verifica dei sorgenti d'esempio dell'Unità 10.

Verifica gli attesi del capitolo PY-14 e le prove semantiche del piano di
lavoro: contratti delle tre ricerche (§6.1), casi canonici da tracciare e
asserire (§6.2), conteggi esatti delle quattro implementazioni elementari,
stabilità osservabile sui record marcati, corrispondenza fra le versioni
strumentate e quelle di riferimento, famiglie di input deterministici.

Le prove sono deterministiche: non misurano tempi, non impongono che un
algoritmo sia più veloce di un altro e non verificano rapporti fra durate.
Ogni atteso numerico proviene dal piano di lavoro o da un caso indipendente:
nessuna prova si limita a ripetere la formula del sorgente.

Esecuzione dalla cartella `unita-10/`:

    uv run --with pytest python -m pytest esempi/test_esempi_u10.py -q
"""

import inspect
import re

import pytest

import conteggi_u10 as cont
import misure_u10 as mis
import ordinamenti_u10 as ordi
import record_u10 as rec
import ricerche_u10 as ric


RICERCHE = (ric.cerca_lineare, ric.cerca_dicotomica, ric.cerca_dicotomica_ricorsiva)
ORDINAMENTI = (
    ordi.insertion_sort,
    ordi.selection_sort,
    ordi.bubble_sort,
    ordi.bubble_sort_ottimizzato,
)


# --- Contratti delle tre ricerche (§6.1 e §6.2) -----------------------------


@pytest.mark.parametrize("cerca", RICERCHE)
@pytest.mark.parametrize(
    "valori, bersaglio, atteso",
    [
        ([], 7, None),
        ([7], 7, 0),
        ([7], 3, None),
        ([7], 9, None),
        ([4, 7, 7, 9], 7, 1),
        ([4, 7, 7, 9], 8, None),
        ([1, 3, 3, 3, 8], 3, 1),
        ([1, 3, 3, 3, 8], 0, None),
        ([1, 3, 8], 0, None),
        ([1, 3, 8], 2, None),
        ([1, 3, 8], 9, None),
        ([4, 7, 7, 9], 4, 0),
        ([4, 7, 7, 9], 9, 3),
    ],
)
def test_contratti_primo_indice(cerca, valori, bersaglio, atteso):
    assert cerca(valori, bersaglio) == atteso


@pytest.mark.parametrize("cerca", RICERCHE)
def test_le_ricerche_non_modificano_largomento(cerca):
    valori = [4, 7, 7, 9]
    copia = list(valori)
    cerca(valori, 7)
    assert valori == copia


def test_il_zero_e_un_indice_valido_non_un_assenza():
    assert ric.cerca_lineare([0, 5], 0) == 0
    assert ric.cerca_dicotomica([0, 5], 0) == 0
    # Il controllo corretto è `is None`: un indice 0 è vero solo per caso.
    assert (ric.cerca_lineare([0, 5], 0) is None) is False


def test_la_sentinella_meno_uno_e_ambigua_con_gli_indici_negativi():
    # `lista[-1]` accede all'ultimo elemento: `-1` non è un marcatore neutro.
    valori = [4, 7, 9]
    assert valori[-1] == 9
    with pytest.raises(ValueError):
        valori.index(2)  # il metodo standard segnala l'assenza con un'eccezione


@pytest.mark.parametrize("cerca", RICERCHE)
@pytest.mark.parametrize("n", [0, 1, 2, 3, 5, 8])
def test_estremi_dellintervallo_su_duplicati(cerca, n):
    valori = [3] * n + [5]
    assert cerca(valori, 3) == (0 if n > 0 else None)
    assert cerca(valori, 5) == n
    assert cerca(valori, 2) is None


# --- Varianti di contratto non intercambiabili ------------------------------


def test_contratto_booleano():
    assert ric.contiene([4, 7, 7, 9], 7) is True
    assert ric.contiene([4, 7, 7, 9], 8) is False
    assert ric.contiene([], 8) is False


def test_un_indice_qualsiasi_puo_dare_indice_diverso_dal_primo():
    valori = [1, 3, 3, 3, 8]
    assert ric.cerca_un_indice(valori, 3) == 2
    assert ric.cerca_dicotomica(valori, 3) == 1
    assert valori[ric.cerca_un_indice(valori, 3)] == 3


def test_tutti_gli_indici():
    assert ric.cerca_tutti_gli_indici([1, 3, 3, 3, 8], 3) == [1, 2, 3]
    assert ric.cerca_tutti_gli_indici([1, 3, 3, 3, 8], 8) == [4]
    assert ric.cerca_tutti_gli_indici([], 3) == []
    assert ric.cerca_tutti_gli_indici([1, 2], 3) == []


@pytest.mark.parametrize(
    "valori, valore, atteso",
    [
        ([], 5, 0),
        ([1, 3, 5], 4, 2),
        ([1, 3, 5], 3, 1),
        ([1, 3, 5], 0, 0),
        ([1, 3, 5], 9, 3),
        ([1, 3, 3, 3], 3, 1),
    ],
)
def test_posizione_di_inserimento(valori, valore, atteso):
    assert ric.posizione_di_inserimento(valori, valore) == atteso


def test_posizione_di_inserimento_mantiene_lordine():
    valori = [1, 3, 3, 5]
    posizione = ric.posizione_di_inserimento(valori, 3)
    valori.insert(posizione, 3)
    assert valori == [1, 3, 3, 3, 5]
    assert valori == sorted(valori)


# --- Ricorsione senza slicing (§15.1) ---------------------------------------


def test_la_ricorsione_non_costruisce_sottoliste():
    sorgenti = [
        inspect.getsource(ric.cerca_dicotomica_ricorsiva),
        inspect.getsource(ric._primo_indice),
    ]
    for sorgente in sorgenti:
        assert re.search(r"\w+\[[^\]]*:", sorgente) is None, "rilevato slicing nel sorgente"


def test_profondita_della_ricorsione_limitata(monkeypatch):
    profondita = {"attuale": 0, "massima": 0}
    originale = ric._primo_indice

    def contatore(valori, bersaglio, sinistra, destra):
        profondita["attuale"] += 1
        profondita["massima"] = max(profondita["massima"], profondita["attuale"])
        try:
            return originale(valori, bersaglio, sinistra, destra)
        finally:
            profondita["attuale"] -= 1

    monkeypatch.setattr(ric, "_primo_indice", contatore)
    valori = list(range(1024))
    assert ric.cerca_dicotomica_ricorsiva(valori, 1023) == 1023
    assert ric.cerca_dicotomica_ricorsiva(valori, 0) == 0
    # 1024 elementi e nessun frame oltre la decina: il logaritmo, non n.
    assert profondita["massima"] <= 20


# --- Ordinamenti: risultato, permutazione, effetti (§6.2) -------------------


CASI_ORDINAMENTO = [
    [],
    [4],
    [5, 2, 4, 2],
    [1, 2, 3, 4],
    [4, 3, 2, 1],
    [2, 2, 2],
    [3, -1, 0, 7, 7, 2],
]


@pytest.mark.parametrize("ordina", ORDINAMENTI)
@pytest.mark.parametrize("originale", CASI_ORDINAMENTO)
def test_risultato_pari_a_sorted_e_permutazione(ordina, originale):
    valori = list(originale)
    assert ordina(valori) is None
    assert valori == sorted(originale)
    assert sorted(valori) == sorted(originale)
    assert len(valori) == len(originale)


@pytest.mark.parametrize("ordina", ORDINAMENTI)
def test_lidentita_della_lista_non_cambia(ordina):
    valori = [5, 2, 4, 2]
    identita = id(valori)
    ordina(valori)
    assert id(valori) == identita
    assert valori == [2, 2, 4, 5]


def test_una_sola_passata_non_ordina_bubble():
    valori = [3, 2, 1]
    n = len(valori)
    for _ in range(1):  # una sola passata del bubble semplice
        for j in range(0, n - 1 - 0):
            if valori[j] > valori[j + 1]:
                valori[j], valori[j + 1] = valori[j + 1], valori[j]
    assert valori == [2, 1, 3]  # il massimo è in fondo, il resto no


# --- Stabilità osservabile (§5.4 e §6.2) -----------------------------------


def test_selection_sort_standard_non_e_stabile():
    # Controesempio canonico del capitolo: la chiave è la PRIMA componente.
    valori = [(2, "a"), (2, "b"), (1, "c")]
    rec.selection_sort_chiave(valori, lambda coppia: coppia[0])
    # Dopo il primo scambio: [(1, "c"), (2, "b"), (2, "a")], e così resta.
    assert valori == [(1, "c"), (2, "b"), (2, "a")]
    assert [etichetta for _, etichetta in valori] == ["c", "b", "a"]


def test_la_stabilita_dipende_dalla_condizione_di_confronto():
    # Con la stessa lista confrontata sulla COPPIA intera il risultato cambia:
    # la stabilità riguarda algoritmo e condizione implementata, non il nome.
    valori = [(2, "a"), (2, "b"), (1, "c")]
    ordi.selection_sort(valori)
    assert valori == [(1, "c"), (2, "a"), (2, "b")]


def test_selection_sort_con_chiave_disallinea_piu_di_una_coppia():
    valori = [(2, "a"), (2, "b"), (2, "c"), (1, "d")]
    rec.selection_sort_chiave(valori, lambda coppia: coppia[0])
    assert [etichetta for _, etichetta in valori] == ["d", "b", "c", "a"]


@pytest.mark.parametrize(
    "ordina",
    [ordi.insertion_sort, ordi.bubble_sort, ordi.bubble_sort_ottimizzato],
)
def test_insertion_e_bubble_sono_stabili(ordina):
    valori = [(2, "a"), (2, "b"), (1, "c"), (2, "c")]
    ordina(valori)
    assert valori == [(1, "c"), (2, "a"), (2, "b"), (2, "c")]


@pytest.mark.parametrize(
    "ordina",
    [rec.insertion_sort_chiave, rec.bubble_sort_chiave, rec.selection_sort_chiave],
)
def test_record_con_stessa_chiave_e_campi_associati(ordina):
    valori = [
        {"codice": "007", "totale_cent": 450},
        {"codice": "009", "totale_cent": 200},
        {"codice": "011", "totale_cent": 450},
    ]
    assert ordina(valori, rec.chiave_totale) is None
    assert [r["totale_cent"] for r in valori] == [200, 450, 450]
    # I campi restano associati al proprio record: nessuna lista parallela.
    assert {r["codice"] for r in valori} == {"007", "009", "011"}
    for record in valori:
        assert record["codice"] in {"007", "009", "011"}


def test_ordinare_i_soli_totali_perde_la_relazione_coi_record():
    # Controesempio del capitolo: si ordinano i totali, non i record.
    registro = rec.registro_di_esempio()
    soli_totali = [r["totale_cent"] for r in registro]
    soli_totali.sort()
    assert soli_totali == [200, 450, 450, 450, 1200]
    # La lista dei totali non dice più a quale record appartiene ciascun importo.
    assert soli_totali is not registro


# --- Conteggi esatti (§6.2 e §6.3) ------------------------------------------


@pytest.mark.parametrize("n", [0, 1, 2, 4, 5])
def test_selection_e_bubble_semplice_conteggio_fisso(n):
    atteso = n * (n - 1) // 2
    assert cont.confronti_attesi_semplici(n) == atteso
    for costruzione in (list(range(n)), list(range(n, 0, -1)), [7] * n):
        assert cont.selection_sort_con_conteggi(list(costruzione))["confronti"] == atteso
        assert cont.bubble_sort_con_conteggi(list(costruzione))["confronti"] == atteso


@pytest.mark.parametrize("n", [0, 1, 2, 4, 5])
def test_insertion_conteggi_su_ordinato_e_inverso(n):
    ordinato = cont.insertion_sort_con_conteggi(list(range(n)))
    inverso = cont.insertion_sort_con_conteggi(list(range(n, 0, -1)))
    assert ordinato["confronti"] == max(0, n - 1)
    assert ordinato["spostamenti"] == 0
    assert ordinato["scambi"] == 0
    assert inverso["confronti"] == n * (n - 1) // 2
    assert inverso["spostamenti"] == n * (n - 1) // 2
    assert inverso["scambi"] == 0


@pytest.mark.parametrize("n", [1, 2, 4, 5, 8])
def test_bubble_ottimizzato_su_ordinato(n):
    registro = cont.bubble_sort_ottimizzato_con_conteggi(list(range(n)))
    assert registro["confronti"] == n - 1
    assert registro["scambi"] == 0


def test_bubble_ottimizzato_non_si_arresta_prematuramente_sullinverso():
    registro = cont.bubble_sort_ottimizzato_con_conteggi([4, 3, 2, 1])
    assert registro["confronti"] == 6
    assert registro["scambi"] == 6
    assert registro["spostamenti"] == 0


def test_bubble_semplice_su_ordinato_mantiene_i_confronti():
    assert cont.bubble_sort_con_conteggi([1, 2, 3, 4])["confronti"] == 6
    assert cont.bubble_sort_con_conteggi([1, 2, 3, 4])["scambi"] == 0


def test_nessuno_scambio_nelle_versioni_insertion():
    # insertion sort non interviene mai per scambio: il conteggio è strutturale.
    for originale in ([2, 1], [3, 2, 1], [5, 2, 4, 2]):
        assert cont.insertion_sort_con_conteggi(list(originale))["scambi"] == 0


def test_sondaggi_e_confronti_divergono_nella_dicotomica():
    esito = cont.cerca_dicotomica_con_conteggi([1, 3, 3, 3, 8], 3)
    assert esito["risultato"] == 1
    assert esito["sondaggi"] == 3
    # Tre sondaggi, quattro operatori Python: il secondo sondaggio valuta sia
    # l'uguaglianza sia il minore, gli altri due soltanto l'uguaglianza.
    assert esito["confronti"] == 4
    singolo = cont.cerca_dicotomica_con_conteggi([5], 5)
    assert singolo["sondaggi"] == 1
    assert singolo["confronti"] == 1
    # Con il bersaglio al primo medio la versione primo indice non si ferma:
    # il medio è un candidato, non la risposta finale.
    prolungata = cont.cerca_dicotomica_con_conteggi([3, 5, 9], 5)
    assert prolungata["risultato"] == 1
    assert prolungata["sondaggi"] == 2


def test_ricerca_lineare_esamina_solo_fino_allarresto():
    esito = cont.cerca_lineare_con_conteggi([4, 7, 7, 9], 7)
    assert esito["risultato"] == 1
    assert esito["sondaggi"] == 2
    assert esito["confronti"] == 2
    assente = cont.cerca_lineare_con_conteggi([4, 7, 7, 9], 8)
    assert assente["sondaggi"] == 4


def test_la_ricerca_dicotomica_primo_indice_non_si_arresta_alla_corrispondenza():
    esito = cont.cerca_dicotomica_con_conteggi([1, 3, 3, 3, 8], 3)
    # Il primo medio è 2 e contiene il bersaglio: la ricerca prosegue a sinistra.
    assert esito["risultato"] == 1
    assert esito["sondaggi"] > 1


# --- Equivalenza fra versioni strumentate e di riferimento ------------------


@pytest.mark.parametrize("ordina, conta", [(ordi.insertion_sort, cont.insertion_sort_con_conteggi),
                                           (ordi.selection_sort, cont.selection_sort_con_conteggi),
                                           (ordi.bubble_sort, cont.bubble_sort_con_conteggi),
                                           (ordi.bubble_sort_ottimizzato, cont.bubble_sort_ottimizzato_con_conteggi)])
@pytest.mark.parametrize("originale", CASI_ORDINAMENTO)
def test_le_varianti_contate_ordinano_come_il_riferimento(ordina, conta, originale):
    atteso = sorted(originale)
    base = list(originale)
    strumentata = list(originale)
    assert ordina(base) is None
    registro = conta(strumentata)
    assert base == atteso
    assert strumentata == atteso
    assert set(registro) == {"confronti", "scambi", "spostamenti"}


def test_le_ricerche_contate_danno_lo_stesso_risultato():
    valori = [1, 3, 3, 3, 8]
    for bersaglio in (0, 1, 3, 8, 9):
        assert cont.cerca_lineare_con_conteggi(valori, bersaglio)["risultato"] == ric.cerca_lineare(valori, bersaglio)
        assert cont.cerca_dicotomica_con_conteggi(valori, bersaglio)["risultato"] == ric.cerca_dicotomica(valori, bersaglio)


# --- Record, zeri iniziali e criteri composti (§6.2) ------------------------


def test_i_codici_conservano_gli_zeri_iniziali():
    registro = rec.registro_di_esempio()
    vista = rec.ordina_per_totale_e_codice(registro)
    codici = [r["codice"] for r in vista]
    assert codici == ["003", "009", "011", "012", "007"]
    assert all(isinstance(r["codice"], str) for r in vista)
    assert [r["totale_cent"] for r in vista] == [200, 450, 450, 450, 1200]


def test_lordinamento_stabile_per_totale_non_coincide_col_criterio_composto():
    registro = rec.registro_di_esempio()
    stabile = [r["codice"] for r in rec.ordina_per_totale(registro)]
    composto = [r["codice"] for r in rec.ordina_per_totale_e_codice(registro)]
    assert stabile == ["003", "012", "009", "011", "007"]
    assert composto == ["003", "009", "011", "012", "007"]
    assert stabile != composto


def test_le_viste_non_modificano_il_registro():
    registro = rec.registro_di_esempio()
    originale = [dict(r) for r in registro]
    rec.ordina_per_totale(registro)
    rec.ordina_per_totale_e_codice(registro)
    assert registro == originale
    assert [r["codice"] for r in registro] == ["012", "007", "009", "003", "011"]


def test_la_lista_della_vista_e_nuova_e_i_record_sono_condivisi():
    registro = rec.registro_di_esempio()
    vista = rec.ordina_per_totale(registro)
    assert vista is not registro
    assert all(any(vista[i] is registro[j] for j in range(len(registro))) for i in range(len(vista)))


def test_sorted_e_list_sort_effetti_diversi():
    registro = rec.registro_di_esempio()
    nuovo = sorted(registro, key=rec.chiave_totale)
    assert nuovo is not registro
    assert registro == rec.registro_di_esempio()
    esito = registro.sort(key=rec.chiave_totale)
    assert esito is None  # list.sort modifica e restituisce None
    assert [r["codice"] for r in registro] == ["003", "012", "009", "011", "007"]


def test_reverse_inverte_lintera_chiave():
    registro = rec.registro_di_esempio()
    inverso = sorted(registro, key=rec.chiave_totale_poi_codice, reverse=True)
    assert [(r["totale_cent"], r["codice"]) for r in inverso] == [
        (1200, "007"),
        (450, "012"),
        (450, "011"),
        (450, "009"),
        (200, "003"),
    ]
    misto = rec.totale_decrescente_codice_crescente(registro)
    assert [(r["totale_cent"], r["codice"]) for r in misto] == [
        (1200, "007"),
        (450, "009"),
        (450, "011"),
        (450, "012"),
        (200, "003"),
    ]


def test_gli_ordinamenti_con_chiave_producono_la_stessa_sequenza_di_chiavi():
    registro = rec.registro_di_esempio()
    attese = [r["totale_cent"] for r in sorted(registro, key=rec.chiave_totale)]
    for ordina in (rec.insertion_sort_chiave, rec.bubble_sort_chiave, rec.selection_sort_chiave):
        copia = list(registro)
        assert ordina(copia, rec.chiave_totale) is None
        assert [r["totale_cent"] for r in copia] == attese
        assert {r["codice"] for r in copia} == {r["codice"] for r in registro}


def test_insertion_sort_chiave_e_stabile_selection_no():
    valori = [{"k": 2, "id": "a"}, {"k": 2, "id": "b"}, {"k": 1, "id": "c"}]
    stabile = list(valori)
    rec.insertion_sort_chiave(stabile, lambda r: r["k"])
    assert [r["id"] for r in stabile] == ["c", "a", "b"]
    instabile = list(valori)
    rec.selection_sort_chiave(instabile, lambda r: r["k"])
    assert [r["id"] for r in instabile] == ["c", "b", "a"]


# --- Famiglie di input e sintesi dei campioni (§5.5 e §15.1) ----------------


def test_le_famiglie_sono_deterministiche():
    for nome in mis.FAMIGLIE:
        prima = mis.genera_famiglia(nome, 12)
        seconda = mis.genera_famiglia(nome, 12)
        assert prima == seconda
        assert len(prima) == 12


def test_costruzione_delle_famiglie():
    assert mis.genera_famiglia("ordinato", 5) == [0, 1, 2, 3, 4]
    assert mis.genera_famiglia("inverso", 5) == [5, 4, 3, 2, 1]
    assert mis.genera_famiglia("quasi_ordinato", 4) == [1, 0, 3, 2]
    assert mis.genera_famiglia("quasi_ordinato", 3) == [0, 1, 2]
    duplicati = mis.genera_famiglia("molti_duplicati", 20)
    assert set(duplicati) <= {0, 1, 2}
    casuale = mis.genera_famiglia("pseudo_casuale", 20)
    assert all(0 <= v <= 20 for v in casuale)


def test_la_famiglia_quasi_ordinato_differisce_per_due_scambi():
    ordinato = mis.genera_famiglia("ordinato", 8)
    quasi = mis.genera_famiglia("quasi_ordinato", 8)
    assert sorted(quasi) == sorted(ordinato)
    assert sum(1 for a, b in zip(ordinato, quasi) if a != b) == 4


def test_famiglia_sconosciuta_e_dimensione_negativa():
    with pytest.raises(ValueError):
        mis.genera_famiglia("casuale", 5)
    with pytest.raises(ValueError):
        mis.genera_famiglia("ordinato", -1)


def test_sintesi_campioni_pari_e_dispari():
    assert mis.sintesi_campioni([3])["mediana"] == 3
    assert mis.sintesi_campioni([5, 1, 4, 2, 3])["mediana"] == 3
    pari = mis.sintesi_campioni([4, 1, 3, 2])
    assert pari["mediana"] == 2.5
    assert pari["minimo"] == 1
    assert pari["massimo"] == 4
    assert pari["numero"] == 4


def test_misura_ordinamento_raccoglie_campioni_e_verifica():
    campioni = mis.misura_ordinamento(
        ordi.bubble_sort_ottimizzato, mis.genera_famiglia("inverso", 20), ripetizioni=3
    )
    assert len(campioni) == 3
    assert all(c >= 0 for c in campioni)
    assert mis.sintesi_campioni(campioni)["numero"] == 3


def test_misura_ricerca_non_modifica_la_lista():
    valori = [1, 3, 3, 3, 8]
    copia = list(valori)
    campioni = mis.misura_ricerca(ric.cerca_dicotomica, valori, 3, ripetizioni=2)
    assert len(campioni) == 2
    assert valori == copia


def test_metadati_della_misura():
    meta = mis.metadati_misura()
    assert meta["timer"] == "time.perf_counter"
    assert meta["unita"] == "secondi per chiamata"
    assert meta["seme"] == mis.SEME_PREDEFINITO


# --- Formule verificate su n piccoli (§6.2) ---------------------------------


@pytest.mark.parametrize(
    "n, atteso",
    [(0, 0), (1, 0), (2, 1), (4, 6), (5, 10)],
)
def test_formula_triangolare_su_n_piccoli(n, atteso):
    assert n * (n - 1) // 2 == atteso
    assert cont.confronti_attesi_semplici(n) == atteso
