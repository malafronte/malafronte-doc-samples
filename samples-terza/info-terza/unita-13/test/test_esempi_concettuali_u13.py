"""Prove degli esempi concettuali U13: Contatore, Limiti, Misura, convertitore.

I nomi dei test richiamano i casi di collaudo del capitolo: CONC-01…CONC-08.
Ogni prova deriva l'atteso dalla **specifica**, non da un'esecuzione precedente.
"""

import json

import pytest
from esempi_concettuali_u13 import (
    Contatore,
    Limiti,
    Misura,
    campi_a_misura,
    converti_misura,
    dati_a_misura,
    millimetri_da_centimetri,
    misura_a_campi,
    misura_a_testo_json,
    testo_json_a_misura,
)
from istanze_alias_self_u13 import ContatoreConLocale, ContatoreConSelfRiassegnato

# --- CONC-01 ---------------------------------------------------------------


def test_conc_01_due_istanze_indipendenti():
    """CONC-01: 2 e 7, incremento di 3 soltanto sul primo, attesi 5 e 7."""
    primo = Contatore(2)
    secondo = Contatore(7)
    primo.incrementa(3)
    assert primo.valore == 5
    assert secondo.valore == 7


def test_conc_01_precondizioni_dichiarate_non_validate():
    """CONC-01: la prima versione non valida; la precondizione è del chiamante."""
    con_zero = Contatore(0)
    con_zero.incrementa(0)
    assert con_zero.valore == 0
    # La classe non solleva eccezioni: non le si attribuiscano garanzie assenti.
    senza_controlli = Contatore(-1)
    assert senza_controlli.valore == -1


# --- CONC-02 ---------------------------------------------------------------


def test_conc_02_chiamata_legata_e_esplicita_coerenti():
    """CONC-02: stessa associazione dei parametri nelle due forme di chiamata."""
    legata = Contatore(2)
    esplicita = Contatore(2)
    assert legata.incrementa(3) == 5
    assert Contatore.incrementa(esplicita, 3) == 5
    assert legata.valore == esplicita.valore == 5


def test_conc_02_locale_al_posto_dell_attributo():
    """CONC-02: il metodo termina senza errori eppure lo stato non cambia."""
    difettoso = ContatoreConLocale(2)
    risultato = difettoso.incrementa(3)
    assert risultato == 5
    assert difettoso.valore == 2


def test_conc_02_self_riassegnato_non_cambia_il_chiamante():
    """CONC-02: `self = altro` sposta il nome locale, non l'associazione del chiamante."""
    c = ContatoreConSelfRiassegnato(4)
    risultato = c.incrementa_su_altro(9)
    assert risultato == 9
    assert c.valore == 4


# --- CONC-03 ---------------------------------------------------------------


def test_conc_03_alias_stessa_istanza():
    """CONC-03: due nomi per la stessa istanza, non due istanze."""
    primo = Contatore(2)
    secondo = primo
    secondo.incrementa(3)
    assert primo is secondo
    assert primo.valore == 5
    assert secondo.valore == 5


def test_conc_03_copia_lista_e_nuova_costruzione():
    """CONC-03: lista esterna nuova, elementi condivisi, costruzione distinta."""
    primo = Contatore(2)
    lista = [primo, Contatore(7)]
    copia = lista.copy()
    assert copia is not lista
    assert copia[0] is lista[0]
    assert Contatore(2) is not primo
    copia.append(Contatore(0))
    assert len(lista) == 2
    assert len(copia) == 3
    primo.incrementa(3)
    assert copia[0].valore == 5


# --- CONC-04 ---------------------------------------------------------------


def test_conc_04_aggiornamento_invertito_rifiutato():
    """CONC-04: da (10, 90), (80, 20) conserva entrambi i campi."""
    limiti = Limiti(10, 90)
    assert limiti.aggiorna(80, 20) is False
    assert limiti.stato() == {"minimo": 10, "massimo": 90}


def test_conc_04_aggiornamento_ammesso():
    """CONC-04: (20, 80) aggiorna entrambi i campi."""
    limiti = Limiti(10, 90)
    assert limiti.aggiorna(20, 80) is True
    assert limiti.stato() == {"minimo": 20, "massimo": 80}


def test_conc_04_snapshot_indipendenti():
    """CONC-04: lo stato restituito è un dizionario nuovo."""
    limiti = Limiti(10, 90)
    prima = limiti.stato()
    prima["minimo"] = 0
    assert limiti.stato() == {"minimo": 10, "massimo": 90}


# --- CONC-05 ---------------------------------------------------------------


def test_conc_05_confini_ammessi():
    """CONC-05: campi uguali e estremi 0/100 sono ammessi."""
    assert Limiti(0, 100).stato() == {"minimo": 0, "massimo": 100}
    assert Limiti(5, 5).stato() == {"minimo": 5, "massimo": 5}
    assert Limiti(0, 0).stato() == {"minimo": 0, "massimo": 0}


@pytest.mark.parametrize(
    ("minimo", "massimo"),
    [
        (True, 50),
        (10, False),
        (1.5, 50),
        (10, "50"),
        (-1, 50),
        (10, 101),
    ],
)
def test_conc_05_costruzione_fuori_contratto(minimo, massimo):
    """CONC-05: booleani, tipi invalidi e campi fuori intervallo rifiutano."""
    with pytest.raises(ValueError):
        Limiti(minimo, massimo)


def test_conc_05_errore_nell_aggiornamento_conserva_tutti_i_campi():
    """CONC-05: un candidato invalido non aggiorna neppure il campo valido."""
    limiti = Limiti(10, 90)
    with pytest.raises(ValueError):
        limiti.aggiorna(20, 200)
    assert limiti.stato() == {"minimo": 10, "massimo": 90}
    with pytest.raises(ValueError):
        limiti.aggiorna(True, 80)
    assert limiti.stato() == {"minimo": 10, "massimo": 90}


# --- CONC-06 ---------------------------------------------------------------


def test_conc_06_proiezione_e_ricostruzione_in_memoria():
    """CONC-06: Misura 12, proiezione modificata, ricostruzione da dati."""
    originale = Misura(12)
    dati = originale.dati()
    assert dati == {"valore": 12}
    dati["valore"] = 99
    assert originale.dati() == {"valore": 12}
    ricostruita = dati_a_misura({"valore": 12})
    assert ricostruita is not originale
    assert ricostruita.dati() == {"valore": 12}


def test_conc_06_round_trip_csv():
    """CONC-06: campi testuali e ricostruzione, con tipo interno intero."""
    originale = Misura(12)
    campi = misura_a_campi(originale)
    assert campi == ["12"]
    ricostruita = campi_a_misura(campi, "record 1")
    assert ricostruita is not originale
    assert isinstance(ricostruita.dati()["valore"], int)
    assert ricostruita.dati() == originale.dati()


def test_conc_06_round_trip_json():
    """CONC-06: il JSON conserva il valore numerico e produce un'istanza nuova."""
    originale = Misura(12)
    testo = misura_a_testo_json(originale)
    assert json.loads(testo) == {"valore": 12}
    ricostruita = testo_json_a_misura(testo)
    assert ricostruita is not originale
    assert ricostruita.dati() == {"valore": 12}


def test_conc_06_zero_ammesso():
    """CONC-06: lo zero è un valore valido del dominio."""
    assert Misura(0).dati() == {"valore": 0}
    assert misura_a_campi(Misura(0)) == ["0"]


# --- CONC-07 ---------------------------------------------------------------


def test_conc_07_campo_mancante():
    """CONC-07: il campo assente viene nominato nella diagnosi."""
    with pytest.raises(ValueError, match="valore.*mancante"):
        dati_a_misura({})


def test_conc_07_testo_non_numerico():
    """CONC-07: il testo non convertibile è un errore di conversione."""
    with pytest.raises(ValueError, match="non è un intero"):
        campi_a_misura(["dodici"], "record 1")


def test_conc_07_valore_negativo():
    """CONC-07: il negativo è un errore di dominio, distinto dal precedente."""
    with pytest.raises(ValueError, match="maggiore o uguale a zero"):
        campi_a_misura(["-1"], "record 1")


def test_conc_07_booleano_json():
    """CONC-07: `true` JSON non diventa 1 per coercizione implicita."""
    with pytest.raises(ValueError, match="atteso un intero"):
        dati_a_misura({"valore": True})


def test_conc_07_float_json():
    """CONC-07: il float non viene troncato a intero."""
    with pytest.raises(ValueError, match="atteso un intero"):
        dati_a_misura({"valore": 2.5})


def test_conc_07_campi_in_più_e_numero_di_campi():
    """CONC-07: campi non previsti e numero di campi errato sono diagnosi distinte."""
    with pytest.raises(ValueError, match="non previsto"):
        dati_a_misura({"valore": 1, "unita": "cm"})
    with pytest.raises(ValueError, match="attesi 1 campi"):
        campi_a_misura(["1", "2"], "record 1")


# --- CONC-08 ---------------------------------------------------------------


def test_conc_08_formula_e_risultati():
    """CONC-08: 12 -> 120 e 0 -> 0, senza I/O."""
    assert millimetri_da_centimetri(12) == 120
    assert millimetri_da_centimetri(0) == 0


def test_conc_08_presentazione_modificabile():
    """CONC-08: cambiare la formulazione non cambia il calcolo."""
    standard = converti_misura(12)
    alternativa = converti_misura(12, "lunghezza convertita")
    assert standard == "risultato: 12 cm = 120 mm"
    assert alternativa == "lunghezza convertita: 12 cm = 120 mm"
    assert millimetri_da_centimetri(12) == 120
