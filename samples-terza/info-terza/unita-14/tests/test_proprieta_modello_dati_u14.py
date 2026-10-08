"""Prove semantiche su proprietà, attributi, metodi, repr, eq e dataclass (U14).

Casi dei gruppi PROP-01/02, CLASSE-01, METODI-01, REPR-01, EQ-01, DATA-01/02
del piano di collaudo dell'Unità 14. Gli attesi derivano dai contratti
pubblicati nei capitoli, non dall'implementazione.
"""

from dataclasses import FrozenInstanceError

import pytest
from attributi_metodi_u14 import Durata, Scheda, SchedaCondivisa, minuti_validi_funzione
from eccezioni_dominio_u14 import DisponibilitaInsufficiente, richiedi_unita
from limiti_proprieta_u14 import Limiti
from misure_modello_dati_u14 import (
    DiarioFrozen,
    MisuraCheStampa,
    MisuraDataclass,
    MisuraEsplicita,
    MisuraFrozen,
    SchedaMisurazioni,
)

# --- PROP-01: proprietà, valori derivati e rifiuti senza stato parziale -----


def test_prop_01_lettura_scrittura_controllata():
    limite = Limiti(0, 10)
    assert (limite.minimo, limite.massimo, limite.ampiezza) == (0, 10, 10)
    limite.massimo = 15
    assert (limite.minimo, limite.massimo) == (0, 15)


def test_prop_01_estremi_uguali_ampiezza_zero():
    limite = Limiti(5, 5)
    assert limite.ampiezza == 0


def test_prop_01_ampiezza_sola_lettura():
    limite = Limiti(0, 10)
    with pytest.raises(AttributeError):
        limite.ampiezza = 4


def test_prop_01_rifiuto_senza_scrittura_parziale():
    limite = Limiti(0, 10)
    with pytest.raises(ValueError):
        limite.minimo = "venti"
    with pytest.raises(ValueError):
        limite.minimo = 20
    assert (limite.minimo, limite.massimo) == (0, 10)


def test_prop_01_nessun_campo_ampiezza():
    assert not hasattr(Limiti(0, 10), "_ampiezza")


# --- PROP-02: aggiornamento completo della coppia ---------------------------


def test_prop_02_trasferimento_con_imposta():
    limite = Limiti(0, 10)
    limite.imposta(20, 30)
    assert (limite.minimo, limite.massimo) == (20, 30)


def test_prop_02_setter_singolo_incompatibile_rifiutato():
    limite = Limiti(0, 10)
    with pytest.raises(ValueError):
        limite.minimo = 20
    assert (limite.minimo, limite.massimo) == (0, 10)


def test_prop_02_candidato_invalido_lascia_lo_stato():
    limite = Limiti(0, 10)
    with pytest.raises(ValueError):
        limite.imposta(20, 15)
    assert (limite.minimo, limite.massimo) == (0, 10)


def test_prop_02_coppia_inversa_in_costruzione():
    with pytest.raises(ValueError):
        Limiti(30, 20)


# --- CLASSE-01: attributi di classe, mascheramento, contenitori --------------


def test_classe_01_dato_di_classe_condiviso():
    prima = Scheda("a")
    seconda = Scheda("b")
    assert prima.categoria == seconda.categoria == Scheda.categoria


def test_classe_01_mascheramento_sull_istanza():
    prima = Scheda("a")
    seconda = Scheda("b")
    prima.categoria = "verifica"
    assert prima.categoria == "verifica"
    assert seconda.categoria == "generale"
    assert Scheda.categoria == "generale"


def test_classe_01_liste_indipendendi_nella_versione_corretta():
    prima = Scheda("a")
    seconda = Scheda("b")
    prima.annotazioni.append("nota")
    assert prima.annotazioni == ["nota"]
    assert seconda.annotazioni == []


def test_classe_01_contenitore_condiviso_nella_versione_difettosa():
    prima = SchedaCondivisa("a")
    seconda = SchedaCondivisa("b")
    prima.annotazioni.append("oops")
    assert "oops" in seconda.annotazioni


# --- METODI-01: factory, self/cls, statico -----------------------------------


def test_metodi_01_factory_da_minuti():
    assert Durata.da_minuti(0).secondi == 0
    assert Durata.da_minuti(3).secondi == 180


def test_metodi_01_factory_rifiuta_dati_fuori_dominio():
    for minuti in (-1, True, "90"):
        with pytest.raises(ValueError):
            Durata.da_minuti(minuti)


def test_metodi_01_costruzione_rifiuta_dati_fuori_dominio():
    for secondi in (-1, True, "90"):
        with pytest.raises(ValueError):
            Durata(secondi)


def test_metodi_01_validatore_statico_senza_istanza():
    assert Durata.minuti_validi(3) is True
    assert Durata.minuti_validi(-1) is False
    assert Durata.minuti_validi(True) is False
    assert Durata.minuti_validi(3) == minuti_validi_funzione(3)


# --- REPR-01: rappresentazioni deterministiche --------------------------------


def test_repr_01_str_e_repr_deterministici():
    misura = MisuraEsplicita("007", 12)
    assert str(misura) == "007: 12 cm"
    assert repr(misura) == "MisuraEsplicita(codice='007', valore_cm=12)"


def test_repr_01_print_di_una_lista_usa_repr():
    a = MisuraEsplicita("007", 12)
    b = MisuraEsplicita("012", 12)
    rappresentazione = repr([a, b])
    assert "MisuraEsplicita(codice='007', valore_cm=12)" in rappresentazione
    assert "MisuraEsplicita(codice='012', valore_cm=12)" in rappresentazione


def test_repr_01_versione_che_stampa_fallisce(capsys):
    misura = MisuraCheStampa("012", 30)
    with pytest.raises(TypeError):
        str(misura)  # __str__ deve restituire una stringa, non None
    assert capsys.readouterr().out == "012: 30 cm\n"


# --- EQ-01: uguaglianza, identità e tipi estranei ------------------------------


def test_eq_01_uguali_non_identici():
    a = MisuraEsplicita("007", 12)
    b = MisuraEsplicita("007", 12)
    assert a == b
    assert a is not b


def test_eq_01_alias_identico():
    a = MisuraEsplicita("007", 12)
    alias = a
    assert alias is a
    assert alias == a


def test_eq_01_campo_diverso():
    a = MisuraEsplicita("007", 12)
    c = MisuraEsplicita("012", 12)
    d = MisuraEsplicita("007", 13)
    assert a != c
    assert a != d


def test_eq_01_simmetria():
    a = MisuraEsplicita("007", 12)
    b = MisuraEsplicita("007", 12)
    assert (a == b) == (b == a)


def test_eq_01_notimplemented_distinto_da_false():
    a = MisuraEsplicita("007", 12)
    assert a.__eq__("007") is NotImplemented
    assert (a == "007") is False


def test_eq_01_tipi_diversi_non_confrontabili():
    a = MisuraEsplicita("007", 12)
    d = MisuraDataclass("007", 12)
    assert (a == d) is False
    assert (d == a) is False


# --- DATA-01: dataclass, post_init, default_factory ----------------------------


def test_data_01_costruzione_validata():
    misura = MisuraDataclass("007", 12)
    assert (misura.codice, misura.valore_cm) == ("007", 12)


def test_data_01_dato_invalido_rifiutato_dal_controllo_scritto():
    for codice, valore in (("", 12), (" 7", 12), ("007", -1), ("007", True), ("007", "12")):
        with pytest.raises(ValueError):
            MisuraDataclass(codice, valore)


def test_data_01_annotation_senza_controllo_non_basta():
    # la stessa coppia è rifiutata da MisuraDataclass (post_init scritto):
    with pytest.raises(ValueError):
        MisuraDataclass("007", "12")


def test_data_01_default_factory_liste_indipendenti():
    s1 = SchedaMisurazioni("prima")
    s2 = SchedaMisurazioni("seconda")
    assert s1.misure is not s2.misure
    s1.misure.append(MisuraDataclass("007", 12))
    assert s2.misure == []


def test_data_01_dataclass_rifiuta_il_default_mutabile():
    from dataclasses import dataclass

    with pytest.raises(ValueError, match="mutable default"):

        @dataclass
        class NonDefinibile:
            voci: list = []


def test_data_01_post_init_non_intercetta_le_modifiche_future():
    misura = MisuraDataclass("007", 12)
    misura.valore_cm = -5  # dataclass mutabile: l'assegnamento è permesso
    assert misura.valore_cm == -5


# --- DATA-02: frozen e i suoi limiti -------------------------------------------


def test_data_02_frozen_blocca_assegnamento():
    misura = MisuraFrozen("007", 12)
    with pytest.raises(FrozenInstanceError):
        misura.valore_cm = 20


def test_data_02_frozen_valida_in_costruzione():
    with pytest.raises(ValueError):
        MisuraFrozen("007", -1)


def test_data_02_frozen_con_contenuto_mutabile():
    diario = DiarioFrozen("prove")
    diario.voci.append("una voce")
    assert diario.voci == ["una voce"]


def test_data_02_frozen_uguaglianza_di_valore():
    assert MisuraFrozen("007", 12) == MisuraFrozen("007", 12)
    assert MisuraFrozen("007", 12) is not MisuraFrozen("007", 12)


# --- ECC-01: eccezione di dominio e gestione nel chiamante ---------------------


def test_ecc_01_richiesta_possibile():
    assert richiedi_unita(5, 2) == 3


def test_ecc_01_richiesta_impossibile_eccezione_specifica():
    with pytest.raises(DisponibilitaInsufficiente):
        richiedi_unita(5, 6)


def test_ecc_01_assegnamento_fallito_conserva_il_valore():
    disponibili = 5
    try:
        disponibili = richiedi_unita(disponibili, 6)
    except DisponibilitaInsufficiente:
        pass
    assert disponibili == 5


def test_ecc_01_dati_fuori_contratto_valueerror():
    for disponibili, unita in ((5, 0), (5, -1), (5, True), ("5", 1), (-1, 1)):
        with pytest.raises(ValueError):
            richiedi_unita(disponibili, unita)
