"""Suite del LAB-PY-U8 - versione di riferimento, casi L01-L13 completa.

I casi L sono locali al laboratorio e non sono nuovi codici del catalogo PY.
La suite non si affida alla rappresentazione testuale dei set né a misure
temporali; per L06 e L12 controlla separatamente uguaglianza e identità.
"""

import inspect

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
    """Caso progettato e motivato dallo studente (versione di riferimento).

    Cosa distingue: un testo in cui il primo token è anche l'ultimo, così una
    deduplicazione che perde la prima occorrenza non coinciderebbe con l'atteso.
    Difetto plausibile che rileva: `list(set(codici))` al posto della scansione
    con memoria dei visti.
    """
    codici = ["Z", "A", "Z", "M", "A"]
    assert unici_in_ordine(codici) == ["Z", "A", "M"]
    assert codici == ["Z", "A", "Z", "M", "A"]


# --- controlli di servizio --------------------------------------------------


def test_ordinamento_non_modifica_il_dizionario():
    frequenze = {"sole": 3, "luna": 2, "mare": 1}
    ordinato = ordina_frequenze(frequenze)
    assert frequenze == {"sole": 3, "luna": 2, "mare": 1}
    assert sorted(ordinato) == sorted([("mare", 1), ("luna", 2), ("sole", 3)])


def test_nessuna_scrittura_o_lettura_interattiva():
    funzioni = [conta_parole, ordina_frequenze, unici_in_ordine, raggruppa_codici]
    for funzione in funzioni:
        sorgente = inspect.getsource(funzione)
        assert "input(" not in sorgente
        assert "print(" not in sorgente


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
