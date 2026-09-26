"""Suite di verifica dei sorgenti d'esempio dell'Unità 9.

Verifica gli attesi del capitolo PY-13 e le prove semantiche del piano di
lavoro: riepiloghi a una e due scansioni (§6.1), tabella dei cicli e
confini (§6.2), scansione con arresto (§6.3), Fibonacci, fattoriale e Hanoi
(§6.4), modello di capacità dinamica (§6.5), conservazione degli argomenti,
comportamento sul vuoto e assenza di contaminazione fra memorie
indipendenti.

Le prove sono deterministiche: non misurano tempi, non impongono che un
algoritmo sia più veloce di un altro e non verificano rapporti fra durate.
Ogni atteso numerico proviene dal piano di lavoro o da un caso indipendente:
nessuna prova si limita a ripetere la formula del sorgente.

Esecuzione dalla cartella `unita-09/`:

    uv run --with pytest python -m pytest esempi/test_esempi_u9.py -q

Le prove sui grafici richiedono matplotlib e vengono saltate in sua assenza;
tutte le altre prove non dipendono da matplotlib.
"""

import pytest

import capacita_dinamica as capacita
import conteggi_cicli as cicli
import conteggi_scansioni as scansioni
import confronto_fibonacci as fib
import misure_u9 as misure


# --- Riepiloghi a una e due scansioni (§6.1) --------------------------------


@pytest.mark.parametrize(
    "valori, atteso",
    [
        ([3, -2, 0, 5], (6, 2)),
        ([0], (0, 0)),
        ([-3, -1], (-4, 0)),
        ([2, 2], (4, 2)),
    ],
)
def test_attesi_dei_riepiloghi(valori, atteso):
    assert scansioni.riepilogo_due_scansioni(valori) == atteso
    assert scansioni.riepilogo_una_scansione(valori) == atteso


def test_riepiloghi_sul_vuoto():
    assert scansioni.riepilogo_due_scansioni([]) == (0, 0)
    assert scansioni.riepilogo_una_scansione([]) == (0, 0)


def test_riepiloghi_non_modificano_largomento():
    valori = [3, -2, 0, 5]
    fotografia = list(valori)
    scansioni.riepilogo_due_scansioni(valori)
    scansioni.riepilogo_una_scansione(valori)
    assert valori == fotografia


def test_visite_n_contro_2n():
    for n in (0, 1, 2, 4, 9):
        valori = misure.costruisci_valori(n)
        _, _, due = scansioni.riepilogo_due_scansioni_osservato(valori)
        _, _, una = scansioni.riepilogo_una_scansione_osservato(valori)
        assert due["visite"] == 2 * n
        assert una["visite"] == n


def test_addizioni_e_confronti_non_raddoppiano():
    valori = [3, -2, 0, 5]
    totale_due, positivi_due, due = scansioni.riepilogo_due_scansioni_osservato(valori)
    totale_una, positivi_una, una = scansioni.riepilogo_una_scansione_osservato(valori)
    assert (totale_due, positivi_due) == (totale_una, positivi_una) == (6, 2)
    # Le visite raddoppiano, ma addizioni e confronti restano n in entrambe.
    assert due["addizioni"] == una["addizioni"] == 4
    assert due["confronti"] == una["confronti"] == 4


def test_contatori_nuovi_adiacente_ogni_esecuzione():
    valori = [1, -1, 2]
    totale, positivi, prima = scansioni.riepilogo_una_scansione_osservato(valori)
    seconda_totale, seconda_positivi, seconda = scansioni.riepilogo_una_scansione_osservato(valori)
    assert (totale, positivi) == (seconda_totale, seconda_positivi)
    assert prima == seconda == {"visite": 3, "addizioni": 3, "confronti": 3}
    assert prima is not seconda


# --- Variante con soglia del problema svolto I ------------------------------


@pytest.mark.parametrize(
    "soglia, atteso",
    [
        (2, (6, 2)),
        (3, (6, 1)),
        (5, (6, 0)),
        (-3, (6, 4)),
    ],
)
def test_riepilogo_con_soglia(soglia, atteso):
    assert scansioni.riepilogo_con_soglia([3, -2, 0, 5], soglia) == atteso


def test_soglia_zero_coincide_con_i_positivi():
    for valori in ([3, -2, 0, 5], [0], [-3, -1], [2, 2], []):
        totale, oltre_soglia = scansioni.riepilogo_con_soglia(valori, 0)
        assert (totale, oltre_soglia) == scansioni.riepilogo_una_scansione(valori)


# --- Scansione con arresto (§6.3) ------------------------------------------


@pytest.mark.parametrize(
    "valori, esito_atteso, confronti_attesi",
    [
        ([0, 7, 7, 7], True, 1),
        ([7, 0, 7, 7], True, 2),
        ([7, 7, 0, 7], True, 3),
        ([7, 7, 7, 0], True, 4),
        ([7, 7, 7, 7], False, 4),
    ],
)
def test_attesi_della_scansione_con_arresto(valori, esito_atteso, confronti_attesi):
    esito, statistiche = scansioni.contiene_zero_osservato(valori)
    assert esito is esito_atteso
    assert scansioni.contiene_zero(valori) is esito_atteso
    assert statistiche["confronti"] == confronti_attesi


def test_arresto_sul_vuoto():
    esito, statistiche = scansioni.contiene_zero_osservato([])
    assert esito is False
    assert scansioni.contiene_zero([]) is False
    assert statistiche["confronti"] == 0


def test_confronti_dipendono_dalla_posizione_del_primo_zero():
    n = 6
    for indice_zero in range(n):
        valori = [7] * n
        valori[indice_zero] = 0
        _, statistiche = scansioni.contiene_zero_osservato(valori)
        assert statistiche["confronti"] == indice_zero + 1
    _, statistiche = scansioni.contiene_zero_osservato([7] * n)
    assert statistiche["confronti"] == n


# --- Tabella dei cicli e confini (§6.2) ------------------------------------


@pytest.mark.parametrize(
    "attesi",
    [
        (0, 0),
        (1, 1),
        (4, 4),
        (10, 10),
    ],
)
def test_attraversamento_singolo(attesi):
    n, conteggio = attesi
    assert cicli.conta_attraversamento(n) == conteggio


@pytest.mark.parametrize("n, conteggio", [(0, 0), (1, 2), (4, 8), (10, 20)])
def test_due_attraversamenti_consecutivi(n, conteggio):
    assert cicli.conta_due_consecutivi(n) == conteggio
    assert cicli.conta_due_consecutivi(n) == 2 * cicli.conta_attraversamento(n)


@pytest.mark.parametrize("n, conteggio", [(0, 0), (1, 1), (4, 16), (5, 25)])
def test_due_cicli_indipendenti(n, conteggio):
    assert cicli.conta_due_indipendenti(n) == conteggio


@pytest.mark.parametrize("n, conteggio", [(0, 0), (1, 0), (2, 1), (4, 6), (5, 10)])
def test_coppie_i_j(n, conteggio):
    assert cicli.conta_coppie_i_j(n) == conteggio


def test_coppie_i_j_escludono_diagonale_e_simmetriche():
    # Per n = 4 le coppie con i < j sono esattamente (0,1) (0,2) (0,3)
    # (1,2) (1,3) (2,3): la diagonale e le coppie invertite non si contano.
    assert cicli.conta_coppie_i_j(4) == 6
    # Le n^2 coppie del doppio ciclo indipendente si dividono in coppie con
    # i < j, coppie invertite e diagonale: 2 * 6 + 4 = 16.
    assert 2 * cicli.conta_coppie_i_j(4) + 4 == cicli.conta_due_indipendenti(4)


@pytest.mark.parametrize("n, conteggio", [(0, 0), (1, 3), (4, 12), (5, 15)])
def test_interno_fisso_tre_giri(n, conteggio):
    assert cicli.conta_interno_fisso(n) == conteggio


@pytest.mark.parametrize("n, conteggio", [(1, 0), (2, 1), (7, 2), (8, 3), (9, 3), (20, 4)])
def test_dimezzamenti(n, conteggio):
    assert cicli.conta_dimezzamenti(n) == conteggio


@pytest.mark.parametrize("n, conteggio", [(1, 0), (2, 1), (7, 3), (8, 3), (9, 4), (20, 5)])
def test_raddoppiamenti(n, conteggio):
    assert cicli.conta_raddoppiamenti(n) == conteggio


def test_dimezzamento_e_raddoppio_sulle_potenze_di_due():
    for k in range(1, 7):
        n = 2**k
        assert cicli.conta_dimezzamenti(n) == k
        assert cicli.conta_raddoppiamenti(n) == k


@pytest.mark.parametrize("n, conteggio", [(0, 0), (1, 0), (8, 24), (16, 64)])
def test_n_ripetizioni_del_dimezzamento(n, conteggio):
    assert cicli.conta_n_dimezzamenti(n) == conteggio


def test_n_dimezzamenti_e_prodotto_dei_due_conteggi():
    for n in (2, 3, 8, 9, 20):
        assert cicli.conta_n_dimezzamenti(n) == n * cicli.conta_dimezzamenti(n)


@pytest.mark.parametrize(
    "righe, colonne, atteso",
    [(2, 3, 6), (3, 3, 9), (4, 5, 20), (0, 3, 0), (2, 0, 0)],
)
def test_visite_matrice_rettangolare(righe, colonne, atteso):
    assert cicli.conta_visite_matrice(righe, colonne) == atteso


def test_tabella_dei_conteggi_copre_i_procedimenti_del_piano():
    tabella = cicli.tabella_dei_conteggi()
    chiavi = [riga["chiave"] for riga in tabella]
    assert chiavi == [
        "conta_attraversamento",
        "conta_due_consecutivi",
        "conta_due_indipendenti",
        "conta_coppie_i_j",
        "conta_interno_fisso",
        "conta_dimezzamenti",
        "conta_raddoppiamenti",
        "conta_n_dimezzamenti",
        "conta_visite_matrice",
    ]
    per_chiave = {riga["chiave"]: riga for riga in tabella}
    # Casi di riferimento del piano, con i parametri previsti.
    assert [parametri for parametri, _ in per_chiave["conta_attraversamento"]["casi"]] == [
        0,
        1,
        4,
    ]
    assert [parametri for parametri, _ in per_chiave["conta_dimezzamenti"]["casi"]] == [
        1,
        7,
        8,
        9,
        20,
    ]
    assert [conteggio for _, conteggio in per_chiave["conta_dimezzamenti"]["casi"]] == [
        0,
        2,
        3,
        3,
        4,
    ]
    assert per_chiave["conta_visite_matrice"]["casi"] == [((2, 3), 6), ((3, 3), 9)]
    assert per_chiave["conta_n_dimezzamenti"]["casi"] == [(0, 0), (8, 24)]


# --- Fibonacci, fattoriale e Hanoi (§6.4) ----------------------------------


@pytest.mark.parametrize(
    "n, valore, c_diretta, d_diretta, addizioni_iter, c_memoria, s_memoria, d_memoria",
    [
        (0, 0, 1, 1, 0, 1, 0, 1),
        (1, 1, 1, 1, 0, 1, 0, 1),
        (2, 1, 3, 2, 1, 3, 1, 2),
        (4, 3, 9, 4, 3, 7, 3, 4),
        (5, 5, 15, 5, 4, 9, 4, 5),
        (10, 55, 177, 10, 9, 19, 9, 10),
    ],
)
def test_tabella_fibonacci_memoria_nuova(
    n, valore, c_diretta, d_diretta, addizioni_iter, c_memoria, s_memoria, d_memoria
):
    assert fib.fibonacci_diretto(n) == valore
    assert fib.fibonacci_iter(n) == valore
    assert fib.fibonacci_mem(n, fib.memoria_delle_basi()) == valore

    diretto = [0, 0]
    assert fib.fibonacci_diretto_osservato(n, diretto) == valore
    assert diretto == [c_diretta, d_diretta]

    addizioni = [0]
    assert fib.fibonacci_iter_osservata(n, addizioni) == valore
    assert addizioni == [addizioni_iter]

    memoria = fib.memoria_delle_basi()
    statistiche = [0, 0, 0]
    assert fib.fibonacci_mem_osservata(n, memoria, statistiche) == valore
    assert statistiche == [c_memoria, d_memoria, s_memoria]


def test_addizioni_uguali_alle_scritture_nella_versione_con_memoria():
    for n in (0, 1, 2, 4, 5, 10):
        statistiche = [0, 0, 0]
        fib.fibonacci_mem_osservata(n, fib.memoria_delle_basi(), statistiche)
        # Ogni addizione corrisponde a una nuova scrittura: S le riassume.
        assert statistiche[2] == max(0, n - 1)


def test_f4_ripetuto_su_memoria_gia_popolata():
    memoria = fib.memoria_delle_basi()
    fib.fibonacci_mem(4, memoria)
    statistiche = [0, 0, 0]
    assert fib.fibonacci_mem_osservata(4, memoria, statistiche) == 3
    assert statistiche == [1, 1, 0]  # C = 1, D = 1, S = 0: nessuna addizione


def test_f5_dopo_f4_nella_stessa_memoria():
    memoria = fib.memoria_delle_basi()
    fib.fibonacci_mem(4, memoria)
    statistiche = [0, 0, 0]
    assert fib.fibonacci_mem_osservata(5, memoria, statistiche) == 5
    assert statistiche == [3, 2, 1]  # ingressi 5, 4, 3; una sola scrittura


def test_memorie_indipendenti_non_si_contaminano():
    prima = fib.memoria_delle_basi()
    seconda = fib.memoria_delle_basi()
    fib.fibonacci_mem(5, prima)
    assert sorted(prima) == [0, 1, 2, 3, 4, 5]
    assert seconda == {0: 0, 1: 1}

    statistiche = [0, 0, 0]
    assert fib.fibonacci_mem_osservata(4, seconda, statistiche) == 3
    assert statistiche == [7, 4, 3]  # la seconda riparte davvero dalle sole basi
    assert sorted(prima) == [0, 1, 2, 3, 4, 5]


@pytest.mark.parametrize(
    "n, valore, moltiplicazioni, ingressi, frame",
    [
        (0, 1, 0, 1, 1),
        (1, 1, 1, 2, 2),
        (3, 6, 3, 4, 4),
        (5, 120, 5, 6, 6),
    ],
)
def test_fattoriale_conteggi(n, valore, moltiplicazioni, ingressi, frame):
    assert fib.fattoriale(n) == valore
    statistiche = [0, 0, 0]
    assert fib.fattoriale_osservato(n, statistiche) == valore
    assert statistiche == [ingressi, moltiplicazioni, frame]


@pytest.mark.parametrize(
    "n, mosse_attese, ingressi_attesi, frame_attesi",
    [
        (0, 0, 1, 1),
        (1, 1, 3, 2),
        (3, 7, 15, 4),
        (4, 15, 31, 5),
    ],
)
def test_hanoi_conteggi(n, mosse_attese, ingressi_attesi, frame_attesi):
    mosse = []
    statistiche = [0, 0]
    fib.hanoi_osservato(n, "A", "C", "B", mosse, statistiche)
    assert len(mosse) == mosse_attese
    assert statistiche == [ingressi_attesi, frame_attesi]


def test_hanoi_mosse_di_n3():
    mosse = []
    fib.hanoi(3, "A", "C", "B", mosse)
    assert len(mosse) == 7  # gli elementi dell'output sono 2^n - 1
    assert mosse[3] == (3, "A", "C")  # il disco 3 si muove una volta sola
    assert mosse[0] == (1, "A", "C")


def test_hanoi_conserva_il_prefisso_gia_presente():
    mosse = [(9, "X", "Y")]
    fib.hanoi(1, "A", "C", "B", mosse)
    assert mosse == [(9, "X", "Y"), (1, "A", "C")]


# --- Capacità dinamica (§6.5) ----------------------------------------------


def test_tabella_degli_otto_inserimenti():
    righe = capacita.simula_accodamenti(8)
    assert [riga["inserimento"] for riga in righe] == [1, 2, 3, 4, 5, 6, 7, 8]
    assert [riga["capacita_dopo"] for riga in righe] == [1, 2, 4, 4, 8, 8, 8, 8]
    assert [riga["copie"] for riga in righe] == [0, 1, 2, 0, 4, 0, 0, 0]
    assert [riga["scrittura_nuova"] for riga in righe] == [1, 1, 1, 1, 1, 1, 1, 1]
    assert [riga["costo_passo"] for riga in righe] == [1, 2, 3, 1, 5, 1, 1, 1]
    assert [riga["cumulativo"] for riga in righe] == [1, 3, 6, 7, 12, 13, 14, 15]


@pytest.mark.parametrize(
    "m, copie_attese, costo_atteso",
    [
        (0, 0, 0),
        (1, 0, 1),
        (2, 1, 3),
        (3, 3, 6),
        (5, 7, 12),
        (8, 7, 15),
    ],
)
def test_copie_e_costo_su_casi_piccoli(m, copie_attese, costo_atteso):
    riepilogo = capacita.riepilogo_ammortizzato(m)
    assert riepilogo["copie_totali"] == copie_attese
    assert riepilogo["costo_totale"] == costo_atteso
    assert riepilogo["scritture_totali"] == m


def test_limiti_della_somma_geometrica_fino_a_128():
    for m in range(1, 129):
        riepilogo = capacita.riepilogo_ammortizzato(m)
        copie = riepilogo["copie_totali"]
        # Somma geometrica: le copie avvengono a 2, 3, 5, 9, ... = 2^k + 1
        # e sommano a 2^(K+1) - 1 con 2^K < m, quindi restano sotto 2m.
        copie_attese = 0 if m < 2 else 2 ** ((m - 1).bit_length()) - 1
        assert copie == copie_attese
        assert copie < 2 * m
        assert riepilogo["costo_totale"] == m + copie
        assert riepilogo["costo_totale"] < 3 * m
        assert riepilogo["capacita_finale"] == 1 << (m - 1).bit_length()


def test_simulazione_e_riepilogo_coerenti():
    for m in (1, 4, 9):
        righe = capacita.simula_accodamenti(m)
        assert righe[-1]["cumulativo"] == capacita.riepilogo_ammortizzato(m)["costo_totale"]
    assert capacita.simula_accodamenti(0) == []
    assert capacita.riepilogo_ammortizzato(0)["capacita_finale"] == 1


# --- Dati e sintesi delle misure (senza misurare tempi) --------------------


def test_dati_di_scansione_riproducibili():
    assert misure.costruisci_valori(0) == []
    assert misure.costruisci_valori(7) == [-2, -1, 0, 1, 2, -2, -1]
    assert misure.costruisci_valori(5) == [-2, -1, 0, 1, 2]


def test_casi_di_arresto_distinguibili():
    n = 6
    attesi = {"iniziale": 1, "intermedia": 4, "finale": 6, "assente": 6}
    for posizione_zero, confronti_attesi in attesi.items():
        valori = misure.costruisci_caso_arresto(n, posizione_zero)
        assert len(valori) == n
        esito, statistiche = scansioni.contiene_zero_osservato(valori)
        assert esito is (posizione_zero != "assente")
        assert statistiche["confronti"] == confronti_attesi


def test_caso_di_arresto_rifiuta_posizione_non_ammessa():
    with pytest.raises(ValueError):
        misure.costruisci_caso_arresto(4, "centrale")
    with pytest.raises(ValueError):
        misure.costruisci_caso_arresto(0, "iniziale")


def test_mediana_di_cinque_campioni_noti():
    campioni = [0.5, 0.1, 0.3, 0.4, 0.2]
    punto = misure.punto_di_misura(
        esperimento="prova",
        algoritmo="funzione",
        dimensione=1,
        significato_dimensione="unita",
        famiglia_input="nota",
        stato_memoria="non applicabile",
        chiamate_per_lotto=2,
        campioni=campioni,
    )
    # Mediana di cinque valori: sorted(campioni)[2] = 0.3.
    assert punto["mediana_chiamata_s"] == pytest.approx(0.15)
    assert punto["minimo_chiamata_s"] == pytest.approx(0.05)
    assert punto["massimo_chiamata_s"] == pytest.approx(0.25)
    assert punto["campioni_lotto_s"] == campioni  # tutti i campioni conservati


def test_tabella_grezza_espande_i_campioni():
    punto = misure.punto_di_misura(
        esperimento="prova",
        algoritmo="funzione",
        dimensione=2,
        significato_dimensione="unita",
        famiglia_input="nota",
        stato_memoria="non applicabile",
        chiamate_per_lotto=2,
        campioni=[0.2, 0.4, 0.6, 0.8, 1.0],
    )
    righe = misure.tabella_grezza([punto])
    assert [riga["ripetizione"] for riga in righe] == [1, 2, 3, 4, 5]
    assert [riga["durata_lotto_s"] for riga in righe] == [0.2, 0.4, 0.6, 0.8, 1.0]
    assert [riga["durata_per_chiamata_s"] for riga in righe] == [0.1, 0.2, 0.3, 0.4, 0.5]
    for riga in righe:
        assert riga["esperimento"] == "prova"
        assert riga["chiamate_per_lotto"] == 2
        assert riga["stato_memoria"] == "non applicabile"


# --- Grafici (richiedono matplotlib) ---------------------------------------


def test_dati_crescite_coincidono_con_la_tabella_del_piano():
    pytest.importorskip("matplotlib")
    import grafici_u9 as graf

    dati = graf.dati_crescite()
    assert dati["n"] == [2, 4, 8, 16]
    assert dati["costante"] == [1, 1, 1, 1]
    assert dati["logaritmo"] == [1, 2, 3, 4]
    assert dati["lineare"] == [2, 4, 8, 16]
    assert dati["n_log_n"] == [2, 8, 24, 64]
    assert dati["quadratica"] == [4, 16, 64, 256]
    assert dati["esponenziale"] == [4, 16, 256, 65536]


def test_dati_visite_n_e_2n():
    pytest.importorskip("matplotlib")
    import grafici_u9 as graf

    dati = graf.dati_visite()
    assert dati["una_scansione"] == [2, 4, 8, 16]
    assert dati["due_scansioni"] == [4, 8, 16, 32]
    for una, due in zip(dati["una_scansione"], dati["due_scansioni"]):
        assert due == 2 * una


def test_salvataggio_grafico_su_cartella_esistente(tmp_path):
    pytest.importorskip("matplotlib")
    import grafici_u9 as graf
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot([1, 2], [1, 2])
    percorso = str(tmp_path / "prova.png")
    assert graf.salva_figura(fig, percorso) is True
    plt.close(fig)
    assert (tmp_path / "prova.png").exists()


def test_salvataggio_grafico_su_cartella_mancante(tmp_path):
    pytest.importorskip("matplotlib")
    import grafici_u9 as graf
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot([1, 2], [1, 2])
    percorso = str(tmp_path / "mancante" / "prova.png")
    assert graf.salva_figura(fig, percorso) is False
    plt.close(fig)
    assert not (tmp_path / "mancante" / "prova.png").exists()
