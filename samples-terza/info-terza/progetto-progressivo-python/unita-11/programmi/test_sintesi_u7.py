"""Suite di verifica delle tabelle di sintesi (tappa U7).

Casi pubblici PU01-PU09 e tre casi propri. I test unitari usano liste di
coppie già normalizzate; i test di raccordo partono dai dati di spedizione e
verificano anche la normalizzazione e la conversione singola euro -> centesimi.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_sintesi_u7.py
"""
from spedizione_u5 import (
    anteprima_preventivo,
    errore_dati_spedizione,
    matrice_riepilogo,
    normalizza_destinazione,
    prepara_coppie,
    preventivi_sopra_media,
    registra_preventivo,
    riepilogo_preventivi,
    totale_preventivi_ric,
    totale_spedizione,
)


# --- Casi pubblici PU01-PU06 ---


def test_pu01_lista_vuota():
    assert preventivi_sopra_media([]) == []
    assert matrice_riepilogo([]) == ([0, 0], [0, 0])


def test_pu02_preparazione_e_analisi_del_canonico():
    dati_spedizione = [
        (100, " Locale ", "n"),
        (1000, "NAZIONALE", "n"),
        (100, "locale", "s"),
    ]
    coppie = prepara_coppie(dati_spedizione)
    assert coppie == [("locale", 300), ("nazionale", 900), ("locale", 500)]
    assert preventivi_sopra_media(coppie) == [("nazionale", 900)]
    assert matrice_riepilogo(coppie) == ([2, 1], [800, 900])


def test_pu03_riepilogo_con_colonne_distinte():
    preventivi = [("locale", 300), ("locale", 700), ("nazionale", 900)]
    assert matrice_riepilogo(preventivi) == ([2, 1], [1000, 900])


def test_pu04_media_esatta_nessun_sopra_media():
    preventivi = [("locale", 700), ("nazionale", 700)]
    assert preventivi_sopra_media(preventivi) == []
    assert matrice_riepilogo(preventivi) == ([1, 1], [700, 700])


def test_pu05_duplicati_conservati():
    preventivi = [("locale", 300), ("nazionale", 900), ("nazionale", 900)]
    assert preventivi_sopra_media(preventivi) == [
        ("nazionale", 900),
        ("nazionale", 900),
    ]
    assert matrice_riepilogo(preventivi) == ([1, 2], [300, 1800])


def test_pu06_alias_chiamate_multiple_e_indipendenza_dei_risultati():
    preventivi = [("locale", 300), ("nazionale", 900), ("nazionale", 900)]
    alias = preventivi
    prima_sopra = preventivi_sopra_media(preventivi)
    seconda_sopra = preventivi_sopra_media(preventivi)
    primi_conteggi, prime_somme = matrice_riepilogo(preventivi)
    secondi_conteggi, seconde_somme = matrice_riepilogo(preventivi)

    assert preventivi == [("locale", 300), ("nazionale", 900), ("nazionale", 900)]
    assert alias == preventivi
    assert prima_sopra == seconda_sopra
    assert prima_sopra is not seconda_sopra
    assert primi_conteggi is not secondi_conteggi
    assert prime_somme is not seconde_somme

    primi_conteggi[0] = 99
    assert secondi_conteggi == [1, 2]
    assert prime_somme == [300, 1800]


# --- Caso PU07: raccordo con U5 e U6 ---


def test_pu07_raccordo_u5_u6_u7():
    dati_spedizione = [
        (100, " Locale ", "n"),
        (1000, "NAZIONALE", "n"),
        (100, "locale", "s"),
    ]
    coppie = prepara_coppie(dati_spedizione)

    importi_cent = []
    for destinazione, totale_cent in coppie:
        importi_cent.append(totale_cent)

    preventivi_euro = []
    for peso_g, destinazione_testo, urgenza in dati_spedizione:
        destinazione = normalizza_destinazione(destinazione_testo)
        preventivi_euro.append(totale_spedizione(peso_g, destinazione, urgenza))

    numero, somma_euro = riepilogo_preventivi(preventivi_euro)
    assert importi_cent == [300, 900, 500]
    assert preventivi_euro == [3, 9, 5]
    assert totale_preventivi_ric(importi_cent, 3) == 1700
    assert numero == 3
    assert somma_euro == 17
    assert 1700 == somma_euro * 100


# --- Casi PU08-PU09: normalizzazione e regressione ---


def test_pu08_normalizzazione_conserva_gli_originali():
    coppie = prepara_coppie([(100, "locale", "n")])
    assert coppie == [("locale", 300)]

    testo_con_spazi = " nazionale "
    testo_maiuscolo = "NAZIONALE"
    assert normalizza_destinazione(testo_con_spazi) == "nazionale"
    assert normalizza_destinazione(testo_maiuscolo) == "nazionale"
    assert testo_con_spazi == " nazionale "
    assert testo_maiuscolo == "NAZIONALE"


def test_pu09_regressione_u5_u6_e_rifiuto_di_estero():
    # Regressione U5: la tarifazione e le collezioni sono invariate.
    assert totale_spedizione(500, "nazionale", "s") == 9
    assert errore_dati_spedizione(100, "estero", "n") == "Destinazione non ammessa"
    preventivi = []
    registra_preventivo(preventivi, 3)
    registra_preventivo(preventivi, 9)
    registra_preventivo(preventivi, 5)
    assert riepilogo_preventivi(preventivi) == (3, 17)
    assert anteprima_preventivo(preventivi, 7) == [3, 9, 5, 7]
    assert preventivi == [3, 9, 5]
    # Regressione U6: il totale ricorsivo è invariato e lavora in centesimi.
    assert totale_preventivi_ric([300, 900, 500], 3) == 1700


# --- Casi propri motivati ---


def test_proprio_1_lista_vuota_e_indipendenza_dei_risultati():
    """PR-1: due riepiloghi di una lista vuota producono liste distinte.

    Discrimina la tentazione di riusare una lista di accumulo fra le chiamate.
    """
    primi_conteggi, prime_somme = matrice_riepilogo([])
    secondi_conteggi, seconde_somme = matrice_riepilogo([])
    assert primi_conteggi == [0, 0]
    assert prime_somme == [0, 0]
    assert primi_conteggi is not secondi_conteggi
    assert prime_somme is not seconde_somme


def test_proprio_2_duplicati_tutti_sopra_la_media_o_nessuno():
    """PR-2: tre totali uguali sono tre elementi distinti.

    Con media uguale ai totali nessuna coppia è strettamente sopra la media;
    con un quarto totale minore le tre uguali entrano tutte, in ordine.
    """
    uguali = [("locale", 100), ("locale", 100), ("nazionale", 100)]
    assert preventivi_sopra_media(uguali) == []
    con_minore = uguali + [("nazionale", 0)]
    assert preventivi_sopra_media(con_minore) == [
        ("locale", 100),
        ("locale", 100),
        ("nazionale", 100),
    ]


def test_proprio_3_conversione_euro_centesimi_eseguita_una_sola_volta():
    """PR-3: 5 euro diventano 500 centesimi, non 50000.

    Discrimina la doppia conversione: il caso PU02 è il modello del confine.
    """
    coppie = prepara_coppie([(1000, "locale", "n")])
    assert coppie == [("locale", 500)]
    somma_cent = 0
    for destinazione, totale_cent in coppie:
        somma_cent = somma_cent + totale_cent
    assert somma_cent == 500


# --- Regressioni: confronto esatto anche oltre la precisione dei float ---


def test_sopra_media_totali_grandi_uguali():
    """Totali uguali non sono sopra la media, anche oltre 2**53."""
    preventivi = [("locale", 9007199254740993), ("nazionale", 9007199254740993)]
    risultato = preventivi_sopra_media(preventivi)
    assert risultato == []
    assert risultato is not preventivi
    assert preventivi == [("locale", 9007199254740993), ("nazionale", 9007199254740993)]


def test_sopra_media_totali_grandi_distanti_un_centesimo():
    """La media fra due interi consecutivi non va arrotondata al maggiore."""
    preventivi = [("locale", 9007199254740993), ("nazionale", 9007199254740994)]
    assert preventivi_sopra_media(preventivi) == [("nazionale", 9007199254740994)]


def test_sopra_media_interi_non_convertibili_in_float():
    """Il dominio degli interi non impone il limite di rappresentazione dei float."""
    totale_cent = 10**400
    preventivi = [("locale", 0), ("nazionale", totale_cent), ("nazionale", totale_cent)]
    assert preventivi_sopra_media(preventivi) == [
        ("nazionale", totale_cent),
        ("nazionale", totale_cent),
    ]
