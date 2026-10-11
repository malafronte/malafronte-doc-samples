"""Suite di verifica di spedizione_u5.py (tappa U5).

Casi pubblici SP01-SP18, SP20-SP22 e SP-L01-SP-L06, più tre casi propri
(PR-1, PR-2, PR-3). Il caso SP19 riguarda la conversione fallita della CLI e
si verifica con la sessione manuale documentata in
documentazione/unita-05/progetto/casi-di-prova.md.

Ogni funzione di test verifica un caso dichiarato: la discovery della suite
coincide con il numero di casi elencati nella sezione «Mappa delle prove» del
README. Nessuna parametrizzazione e nessuna fixture complessa: la suite usa
soltanto chiamate dirette e asserzioni esplicite.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_spedizione_u5.py
"""
from spedizione_u5 import (
    anteprima_preventivo,
    costo_base_spedizione,
    errore_dati_spedizione,
    registra_preventivo,
    riepilogo_preventivi,
    supplemento_destinazione,
    supplemento_urgenza,
    totale_spedizione,
)


# --- Casi SP01-SP07: fasce di peso, senza supplementi ---


def test_sp01_peso_1_fascia_minima():
    assert errore_dati_spedizione(1, "locale", "n") == ""
    assert costo_base_spedizione(1) == 3
    assert totale_spedizione(1, "locale", "n") == 3


def test_sp02_peso_499_fascia_minima():
    assert costo_base_spedizione(499) == 3
    assert totale_spedizione(499, "locale", "n") == 3


def test_sp03_peso_500_confine_inferiore_seconda_fascia():
    assert costo_base_spedizione(500) == 3
    assert totale_spedizione(500, "locale", "n") == 3


def test_sp04_peso_501_primo_della_seconda_fascia():
    assert costo_base_spedizione(501) == 5
    assert totale_spedizione(501, "locale", "n") == 5


def test_sp05_peso_1999_seconda_fascia():
    assert costo_base_spedizione(1999) == 5
    assert totale_spedizione(1999, "locale", "n") == 5


def test_sp06_peso_2000_confine_inferiore_terza_fascia():
    assert costo_base_spedizione(2000) == 5
    assert totale_spedizione(2000, "locale", "n") == 5


def test_sp07_peso_2001_primo_della_terza_fascia():
    assert costo_base_spedizione(2001) == 8
    assert totale_spedizione(2001, "locale", "n") == 8


# --- Casi SP08-SP11 e SP21: supplementi e composizione ---


def test_sp08_massimo_con_entrambi_i_supplementi():
    assert costo_base_spedizione(10000) == 8
    assert supplemento_destinazione("nazionale") == 4
    assert supplemento_urgenza("s") == 2
    assert totale_spedizione(10000, "nazionale", "s") == 14


def test_sp09_supplemento_solo_destinazione():
    assert supplemento_destinazione("nazionale") == 4
    assert supplemento_urgenza("n") == 0
    assert totale_spedizione(500, "nazionale", "n") == 7


def test_sp10_supplemento_solo_urgenza():
    assert supplemento_destinazione("locale") == 0
    assert supplemento_urgenza("s") == 2
    assert totale_spedizione(500, "locale", "s") == 5


def test_sp11_supplementi_indipendenti_e_sommati():
    assert totale_spedizione(500, "nazionale", "s") == 9


def test_sp21_peso_9999_terza_fascia_con_supplementi():
    assert costo_base_spedizione(9999) == 8
    assert totale_spedizione(9999, "nazionale", "s") == 14


# --- Casi SP12-SP18, SP20, SP22: validazione e priorità ---


def test_sp12_peso_zero_non_ammesso():
    assert errore_dati_spedizione(0, "locale", "n") == "Peso non ammesso"


def test_sp13_peso_negativo_non_ammesso():
    assert errore_dati_spedizione(-1, "locale", "s") == "Peso non ammesso"


def test_sp14_peso_oltre_il_massimo_non_ammesso():
    assert errore_dati_spedizione(10001, "nazionale", "n") == "Peso non ammesso"


def test_sp15_destinazione_non_ammessa():
    assert errore_dati_spedizione(100, "estero", "n") == "Destinazione non ammessa"


def test_sp16_urgenza_maiuscola_non_ammessa():
    assert errore_dati_spedizione(100, "locale", "S") == "Urgenza non ammessa"


def test_sp17_priorita_peso_prima_di_destinazione_e_urgenza():
    assert errore_dati_spedizione(0, "estero", "forse") == "Peso non ammesso"


def test_sp18_priorita_destinazione_prima_di_urgenza():
    assert errore_dati_spedizione(100, "estero", "forse") == "Destinazione non ammessa"


def test_sp20_destinazione_vuota_non_ammessa():
    assert errore_dati_spedizione(100, "", "n") == "Destinazione non ammessa"


def test_sp22_urgenza_forse_non_ammessa():
    assert errore_dati_spedizione(100, "locale", "forse") == "Urgenza non ammessa"


# --- Casi SP-L01-SP-L06: effetti sulle liste di preventivi ---


def test_sp_l01_registrazione_in_lista_vuota():
    preventivi = []
    risultato = registra_preventivo(preventivi, 3)
    assert risultato is None
    assert preventivi == [3]


def test_sp_l02_registrazione_in_lista_non_vuota():
    preventivi = [3, 5]
    identita_prima = id(preventivi)
    risultato = registra_preventivo(preventivi, 7)
    assert risultato is None
    assert preventivi == [3, 5, 7]
    assert id(preventivi) == identita_prima


def test_sp_l03_anteprima_lascia_invariato_l_originale():
    preventivi = [3, 5]
    anteprima = anteprima_preventivo(preventivi, 7)
    assert anteprima == [3, 5, 7]
    assert preventivi == [3, 5]
    assert anteprima is not preventivi


def test_sp_l04_anteprima_da_lista_vuota():
    preventivi = []
    anteprima = anteprima_preventivo(preventivi, 3)
    assert anteprima == [3]
    assert preventivi == []


def test_sp_l05_riepilogo_lista_non_vuota():
    preventivi = [3, 5, 7]
    assert riepilogo_preventivi(preventivi) == (3, 15)
    assert preventivi == [3, 5, 7]


def test_sp_l06_riepilogo_lista_vuota():
    preventivi = []
    assert riepilogo_preventivi(preventivi) == (0, 0)
    assert preventivi == []


# --- Casi propri motivati ---


def test_proprio_1_seconda_fascia_con_entrambi_i_supplementi():
    """PR-1: 1200 g, nazionale, s — peso interno alla seconda fascia.

    Discrimina la composizione completa lontano dai confini: atteso
    5 + 4 + 2 = 11 euro.
    """
    assert errore_dati_spedizione(1200, "nazionale", "s") == ""
    assert costo_base_spedizione(1200) == 5
    assert totale_spedizione(1200, "nazionale", "s") == 11


def test_proprio_2_token_urgenza_vuoto():
    """PR-2: token di urgenza vuoto.

    Discrimina l'assenza di normalizzazione: la stringa vuota non è "n".
    """
    assert errore_dati_spedizione(100, "locale", "") == "Urgenza non ammessa"


def test_proprio_3_totale_non_omette_il_supplemento_di_urgenza():
    """PR-3: 501 g, locale, s.

    Il caso avrebbe rilevato il difetto descritto in
    documentazione/unita-05/progetto/diagnosi.md: un totale che somma costo
    base e supplemento destinazione ma dimentica il supplemento di urgenza.
    Atteso 5 + 0 + 2 = 7 euro, mentre il difetto darebbe 5.
    """
    assert totale_spedizione(501, "locale", "s") == 7
    assert totale_spedizione(501, "locale", "s") == (
        costo_base_spedizione(501)
        + supplemento_destinazione("locale")
        + supplemento_urgenza("s")
    )
