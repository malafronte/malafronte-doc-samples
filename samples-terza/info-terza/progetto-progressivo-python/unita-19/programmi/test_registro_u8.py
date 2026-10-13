"""Suite di verifica del registro di record (tappa U8).

Casi pubblici PU8-01-PU8-09 e tre casi propri. I record hanno i campi
`codice`, `destinazione` e `totale_cent`; i totali sono interi in centesimi.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_registro_u8.py
"""
from spedizione_u5 import (
    cerca_preventivo,
    crea_registro,
    errore_dati_spedizione,
    matrice_riepilogo,
    normalizza_destinazione,
    prepara_coppie,
    riepilogo_per_destinazione,
    totale_preventivi_ric,
    totale_spedizione,
)


def registro_canonico():
    """Registro di riferimento: codici 007, 008, 009 e totali in centesimi."""
    codici = ["007", "008", "009"]
    preventivi = [("locale", 300), ("nazionale", 900), ("locale", 500)]
    return crea_registro(codici, preventivi)


# --- Casi pubblici PU8-01-PU8-03 ---


def test_pu8_01_liste_vuote():
    registro = crea_registro([], [])
    assert registro == []
    assert riepilogo_per_destinazione(registro) == {
        "locale": {"conteggio": 0, "totale_cent": 0},
        "nazionale": {"conteggio": 0, "totale_cent": 0},
    }
    assert cerca_preventivo(registro, "007") is None


def test_pu8_02_migrazione_del_dataset_canonico():
    registro = registro_canonico()
    assert len(registro) == 3
    assert registro[0] == {"codice": "007", "destinazione": "locale", "totale_cent": 300}
    assert registro[1] == {"codice": "008", "destinazione": "nazionale", "totale_cent": 900}
    assert registro[2] == {"codice": "009", "destinazione": "locale", "totale_cent": 500}


def test_pu8_03_riepilogo_del_canonico():
    registro = registro_canonico()
    riepilogo = riepilogo_per_destinazione(registro)
    assert riepilogo["locale"] == {"conteggio": 2, "totale_cent": 800}
    assert riepilogo["nazionale"] == {"conteggio": 1, "totale_cent": 900}
    totale_complessivo = (
        riepilogo["locale"]["totale_cent"] + riepilogo["nazionale"]["totale_cent"]
    )
    assert totale_complessivo == 1700


# --- Caso PU8-04: rifiuti senza risultati parziali ---


def test_pu8_04_codici_duplicati_vuoti_o_lunghezze_discordanti():
    preventivi = [("locale", 300), ("nazionale", 900), ("locale", 500)]

    codici_duplicati = ["007", "007", "009"]
    assert crea_registro(codici_duplicati, preventivi) is None
    assert codici_duplicati == ["007", "007", "009"]
    assert preventivi == [("locale", 300), ("nazionale", 900), ("locale", 500)]

    codici_con_vuoto = ["007", "", "009"]
    assert crea_registro(codici_con_vuoto, preventivi) is None
    assert codici_con_vuoto == ["007", "", "009"]

    assert crea_registro(["007", "008"], preventivi) is None
    assert crea_registro(["007", "008", "009", "010"], preventivi) is None
    assert preventivi == [("locale", 300), ("nazionale", 900), ("locale", 500)]


# --- Casi PU8-05 e PU8-06: ricerca e totali ---


def test_pu8_05_ricerca_presenti_e_assenti():
    registro = registro_canonico()
    assert cerca_preventivo(registro, "007") == {
        "codice": "007",
        "destinazione": "locale",
        "totale_cent": 300,
    }
    assert cerca_preventivo(registro, "009") == {
        "codice": "009",
        "destinazione": "locale",
        "totale_cent": 500,
    }
    assert cerca_preventivo(registro, "7") is None
    assert cerca_preventivo(registro, "X99") is None


def test_pu8_06_totali_uguali_e_importo_zero():
    codici = ["A1", "A2", "A3"]
    preventivi = [("locale", 450), ("nazionale", 450), ("locale", 0)]
    registro = crea_registro(codici, preventivi)
    riepilogo = riepilogo_per_destinazione(registro)
    assert riepilogo["locale"] == {"conteggio": 2, "totale_cent": 450}
    assert riepilogo["nazionale"] == {"conteggio": 1, "totale_cent": 450}
    assert len(registro) == 3


# --- Casi PU8-07 e PU8-08: indipendenza e alias ---


def test_pu8_07_chiamate_multiple_e_indipendenza_dei_risultati():
    codici = ["007", "008", "009"]
    preventivi = [("locale", 300), ("nazionale", 900), ("locale", 500)]

    prima_migrazione = crea_registro(codici, preventivi)
    seconda_migrazione = crea_registro(codici, preventivi)
    assert prima_migrazione == seconda_migrazione
    assert prima_migrazione is not seconda_migrazione
    assert prima_migrazione[0] is not seconda_migrazione[0]

    primo_riepilogo = riepilogo_per_destinazione(prima_migrazione)
    secondo_riepilogo = riepilogo_per_destinazione(prima_migrazione)
    assert primo_riepilogo == secondo_riepilogo
    assert primo_riepilogo["locale"] is not secondo_riepilogo["locale"]

    primo_riepilogo["locale"]["conteggio"] = 99
    assert secondo_riepilogo["locale"] == {"conteggio": 2, "totale_cent": 800}
    assert prima_migrazione[0] == {
        "codice": "007",
        "destinazione": "locale",
        "totale_cent": 300,
    }


def test_pu8_08_alias_del_record_restituito_dalla_ricerca():
    # Fixture separata: la modifica non contamina gli altri test.
    registro = crea_registro(["X1", "X2"], [("locale", 100), ("nazionale", 200)])
    record = cerca_preventivo(registro, "X1")
    assert record is registro[0]

    record["totale_cent"] = 150
    assert registro[0]["totale_cent"] == 150
    assert registro[1] == {"codice": "X2", "destinazione": "nazionale", "totale_cent": 200}

    # La ricerca da sola non modifica nulla: un secondo accesso non altera i dati.
    assert cerca_preventivo(registro, "X9") is None
    assert len(registro) == 2


# --- Caso PU8-09: preparazione dalle spedizioni U5 ---


def test_pu8_09_preparazione_canonica_dalle_spedizioni():
    dati_spedizione = [
        (100, " Locale ", "n"),
        (1000, "NAZIONALE", "n"),
        (100, "locale", "s"),
    ]
    coppie = prepara_coppie(dati_spedizione)

    importi_euro = []
    for peso_g, destinazione_testo, urgenza in dati_spedizione:
        destinazione = normalizza_destinazione(destinazione_testo)
        importi_euro.append(totale_spedizione(peso_g, destinazione, urgenza))

    codici = ["007", "008", "009"]
    registro = crea_registro(codici, coppie)

    assert importi_euro == [3, 9, 5]
    assert totali_delle_coppie(coppie) == [300, 900, 500]
    assert matrice_riepilogo(coppie) == ([2, 1], [800, 900])
    riepilogo = riepilogo_per_destinazione(registro)
    assert riepilogo["locale"] == {"conteggio": 2, "totale_cent": 800}
    assert riepilogo["nazionale"] == {"conteggio": 1, "totale_cent": 900}
    assert totale_preventivi_ric(totali_delle_coppie(coppie), 3) == 1700
    assert errore_dati_spedizione(100, "estero", "n") == "Destinazione non ammessa"


def totali_delle_coppie(coppie):
    """Restituisce la lista dei soli totali in centesimi, senza convertirli."""
    totali_cent = []
    for destinazione, totale_cent in coppie:
        totali_cent.append(totale_cent)
    return totali_cent


# --- Casi propri motivati ---


def test_proprio_1_codici_con_zeri_iniziali_distinti():
    """PR-1: "007" e "7" sono codici diversi e convivono nello stesso registro."""
    registro = crea_registro(["007", "7"], [("locale", 100), ("locale", 200)])
    assert len(registro) == 2
    assert cerca_preventivo(registro, "007")["totale_cent"] == 100
    assert cerca_preventivo(registro, "7")["totale_cent"] == 200


def test_proprio_2_registro_a_un_record_e_ricerca_assente():
    """PR-2: il caso minimo non vuoto distingue assenza e record."""
    registro = crea_registro(["B1"], [("nazionale", 0)])
    assert registro == [{"codice": "B1", "destinazione": "nazionale", "totale_cent": 0}]
    riepilogo = riepilogo_per_destinazione(registro)
    assert riepilogo["nazionale"] == {"conteggio": 1, "totale_cent": 0}
    assert riepilogo["locale"] == {"conteggio": 0, "totale_cent": 0}
    assert cerca_preventivo(registro, "B2") is None


def test_proprio_3_riepilogo_su_una_sola_destinazione():
    """PR-3: tutti i record su `locale` lasciano il gruppo `nazionale` a zero."""
    codici = ["C1", "C2"]
    preventivi = [("locale", 300), ("locale", 500)]
    riepilogo = riepilogo_per_destinazione(crea_registro(codici, preventivi))
    assert riepilogo["locale"] == {"conteggio": 2, "totale_cent": 800}
    assert riepilogo["nazionale"] == {"conteggio": 0, "totale_cent": 0}
