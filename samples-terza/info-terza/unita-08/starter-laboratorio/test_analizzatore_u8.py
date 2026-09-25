"""Suite del LAB-PY-U8 - versione di partenza, casi L01-L13.

I primi esecuzione della suite **devono fallire**: lo starter è incompleto e lo
dichiara. I fallimenti attesi sono per risultato `None` o per `TypeError`, mai
per errori di import o di sintassi. Se compare un prompt interattivo durante la
raccolta, l'import non è ancora pulito.

Il caso L13 è lasciato incompleto: è il caso progettato dallo studente.
"""

import pytest

from analizzatore_u8 import (
    TESTO_CANONICO,
    VOCI_CANONICHE,
    conta_parole,
    ordina_frequenze,
    raggruppa_codici,
    unici_in_ordine,
)


# --- L01 - L05: frequenze e graduatorie ------------------------------------


def test_l01_testo_canonico():
    frequenze = conta_parole(TESTO_CANONICO)
    assert frequenze == {"sole": 3, "luna": 2, "mare": 1}
    assert sum(frequenze.values()) == 6
    assert len(frequenze) == 3


def test_l02_parita_in_decrescente():
    frequenze = conta_parole("Sole luna mare LUNA sole")
    assert frequenze == {"sole": 2, "luna": 2, "mare": 1}
    assert ordina_frequenze(frequenze, decrescente=True) == [
        ("luna", 2),
        ("sole", 2),
        ("mare", 1),
    ]
    assert ordina_frequenze(frequenze) == [
        ("mare", 1),
        ("luna", 2),
        ("sole", 2),
    ]


def test_l03_vuoto_e_soli_spazi():
    for testo in ["", "   \n\t "]:
        assert conta_parole(testo) == {}
        assert ordina_frequenze(conta_parole(testo)) == []
        assert ordina_frequenze(conta_parole(testo), decrescente=True) == []


def test_l04_punteggiatura_conservata():
    assert conta_parole("sole sole, SOLE") == {"sole": 2, "sole,": 1}


def test_l05_accenti_invariati():
    assert conta_parole("è è") == {"è": 2}


# --- L06: ordinamento senza effetti ----------------------------------------


def test_l06_ordinare_due_volte():
    frequenze = conta_parole(TESTO_CANONICO)
    prima_lista = ordina_frequenze(frequenze)
    seconda_lista = ordina_frequenze(frequenze)

    assert frequenze == {"sole": 3, "luna": 2, "mare": 1}
    assert list(frequenze) == ["sole", "luna", "mare"]
    assert prima_lista == seconda_lista
    assert prima_lista is not seconda_lista


# --- L07 - L08: unicità -----------------------------------------------------


def test_l07_prima_occorrenza():
    assert unici_in_ordine(["007", "7", "007", "A"]) == ["007", "7", "A"]


def test_l08_vuoto_e_tutti_uguali():
    assert unici_in_ordine([]) == []
    assert unici_in_ordine(["X", "X", "X"]) == ["X"]


# --- L09 - L12: gruppi ------------------------------------------------------


def test_l09_coppie_canoniche():
    assert raggruppa_codici(VOCI_CANONICHE) == {
        "elettronica": ["R10", "L05"],
        "meccanica": ["007"],
    }


def test_l10_ripetizione_conservata():
    assert raggruppa_codici([("a", "1"), ("a", "1")]) == {"a": ["1", "1"]}


def test_l11_coppie_vuote():
    assert raggruppa_codici([]) == {}


def test_l12_indipendenza_dei_gruppi():
    risultato = raggruppa_codici(VOCI_CANONICHE)

    assert risultato["elettronica"] is not risultato["meccanica"]

    risultato["elettronica"].append("X99")
    assert risultato["meccanica"] == ["007"]
    assert VOCI_CANONICHE == [
        ("elettronica", "R10"),
        ("meccanica", "007"),
        ("elettronica", "L05"),
    ]
    assert raggruppa_codici(VOCI_CANONICHE) == {
        "elettronica": ["R10", "L05"],
        "meccanica": ["007"],
    }


# --- L13: caso progettato dallo studente -----------------------------------


def test_l13_caso_dello_studente():
    """Caso progettato e motivato dallo studente: da completare.

    TODO dello studente:
    1. scegliere un caso nuovo su vuoto, confine, duplicati o alias;
    2. scrivere l'atteso **prima** di eseguire, motivandolo;
    3. dichiarare quale difetto plausibile il caso deve distinguere;
    4. sostituire questo corpo con le asserzioni del caso.

    Il caso qui sotto è un segnaposto e non è un test valido.
    """
    raise AssertionError("PY-U8-L13: caso proprio non ancora progettato")


# --- controlli di servizio --------------------------------------------------


def test_ordinamento_non_modifica_il_dizionario():
    frequenze = {"sole": 3, "luna": 2, "mare": 1}
    ordinato = ordina_frequenze(frequenze)
    assert frequenze == {"sole": 3, "luna": 2, "mare": 1}
    assert sorted(ordinato) == sorted([("mare", 1), ("luna", 2), ("sole", 3)])


def test_funzioni_disponibili():
    assert callable(conta_parole)
    assert callable(ordina_frequenze)
    assert callable(unici_in_ordine)
    assert callable(raggruppa_codici)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
