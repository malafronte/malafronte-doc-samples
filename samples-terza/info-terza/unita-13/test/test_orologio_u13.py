"""Regressioni del percorso sull'orologio: entrambe le rappresentazioni."""

import orologio_procedurale_u13 as procedurale
import pytest
from orologio_digitale_u13 import (
    Orologio,
    OrologioConLocale,
    OrologioConSelfRiassegnato,
    OrologioDigitale,
    OrologioTreMetodi,
)
from soluzioni_u13 import OrologioTreMetodi as OrologioSoluzioneX02


@pytest.mark.parametrize("ore,minuti", [(0, 0), (23, 59), (8, 5)])
def test_costruzioni_valide(ore, minuti):
    record = procedurale.nuovo_orologio(ore, minuti)
    istanza = OrologioDigitale(ore, minuti)
    assert procedurale.leggi(record) == istanza.leggi() == (ore, minuti)
    assert procedurale.testo(record) == istanza.testo() == f"{ore:02d}:{minuti:02d}"


@pytest.mark.parametrize(
    "ore,minuti",
    [(-1, 0), (24, 0), (0, -1), (0, 60), (True, 0), (0, False), (8.0, 5), (8, "5")],
)
def test_costruzioni_non_ammesse(ore, minuti):
    with pytest.raises(ValueError):
        procedurale.nuovo_orologio(ore, minuti)
    with pytest.raises(ValueError):
        OrologioDigitale(ore, minuti)


@pytest.mark.parametrize("ore,minuti", [(12, 75), (24, 30), (True, 30), (12, "30")])
def test_impostazione_fallita_conserva_entrambi_i_campi(ore, minuti):
    record = procedurale.nuovo_orologio(8, 15)
    istanza = OrologioDigitale(8, 15)
    with pytest.raises(ValueError):
        procedurale.imposta(record, ore, minuti)
    with pytest.raises(ValueError):
        istanza.imposta(ore, minuti)
    assert procedurale.leggi(record) == istanza.leggi() == (8, 15)


@pytest.mark.parametrize(
    "ore,minuti,durata,atteso",
    [(23, 58, 5, (0, 3)), (8, 15, 45, (9, 0)), (8, 15, 0, (8, 15)),
     (8, 15, 1440, (8, 15)), (23, 59, 2882, (0, 1))],
)
def test_avanzamento_e_confini(ore, minuti, durata, atteso):
    record = procedurale.nuovo_orologio(ore, minuti)
    istanza = OrologioDigitale(ore, minuti)
    assert procedurale.avanza(record, durata) is None
    assert istanza.avanza(durata) is None
    assert procedurale.leggi(record) == istanza.leggi() == atteso


@pytest.mark.parametrize("durata", [-1, True, False, 2.5, "5", None])
def test_durata_non_ammessa_non_modifica(durata):
    record = procedurale.nuovo_orologio(23, 58)
    istanza = OrologioDigitale(23, 58)
    with pytest.raises(ValueError):
        procedurale.avanza(record, durata)
    with pytest.raises(ValueError):
        istanza.avanza(durata)
    assert procedurale.leggi(record) == istanza.leggi() == (23, 58)


def test_sequenza_e_indipendenza():
    record = procedurale.nuovo_orologio(23, 58)
    altro_record = procedurale.nuovo_orologio(8, 15)
    primo = OrologioDigitale(23, 58)
    secondo = OrologioDigitale(8, 15)
    procedurale.avanza(record, 5)
    primo.avanza(5)
    procedurale.avanza(altro_record, 45)
    secondo.avanza(45)
    assert procedurale.testo(record) == primo.testo() == "00:03"
    assert procedurale.testo(altro_record) == secondo.testo() == "09:00"
    assert procedurale.imposta(record, 12, 30) is None
    assert primo.imposta(12, 30) is None
    assert procedurale.testo(record) == primo.testo() == "12:30"
    assert procedurale.testo(altro_record) == secondo.testo() == "09:00"


def test_confronto_di_tutti_gli_orari_e_durate_discriminanti():
    for totale in range(1440):
        ore, minuti = totale // 60, totale % 60
        for durata in (0, 1, 59, 60, 1440, 2881):
            record = procedurale.nuovo_orologio(ore, minuti)
            istanza = OrologioDigitale(ore, minuti)
            procedurale.avanza(record, durata)
            istanza.avanza(durata)
            atteso = (totale + durata) % 1440
            assert procedurale.leggi(record) == istanza.leggi() == (atteso // 60, atteso % 60)


def test_prima_classe_e_forma_esplicita():
    primo = Orologio(8, 15)
    secondo = Orologio(8, 15)
    assert primo.avanza(50) == Orologio.avanza(secondo, 50) == (9, 5)
    assert primo.testo() == secondo.testo() == "09:05"
    assert primo is not secondo
    assert primo != secondo


def test_alias_copia_e_nuova_costruzione():
    primo = Orologio(8, 15)
    alias = primo
    lista = [primo, Orologio(12, 40)]
    copia = lista.copy()
    nuovo = Orologio(8, 15)
    alias.avanza(5)
    assert primo.testo() == copia[0].testo() == "08:20"
    assert nuovo.testo() == "08:15"
    assert copia[1] is lista[1]
    copia.append(Orologio(0, 0))
    assert len(lista) == 2 and len(copia) == 3


def test_locale_non_modifica_e_self_riassegnato():
    difettoso = OrologioConLocale(8, 15)
    assert difettoso.avanza(50) == (9, 5)
    assert (difettoso.ore, difettoso.minuti) == (8, 15)
    altro = OrologioConSelfRiassegnato(8, 15)
    assert altro.imposta_su_altro(12, 30) == (12, 30)
    assert (altro.ore, altro.minuti) == (8, 15)


@pytest.mark.parametrize("classe", [OrologioTreMetodi, OrologioSoluzioneX02])
def test_x02_mutazione_riassegnamento_nuova_istanza(classe):
    orologio = classe(8, 15)
    alias = orologio
    assert orologio.muta(9, 5) == (9, 5)
    assert orologio.riassegna(12, 30) == (12, 30)
    nuovo = orologio.ricostruisce(18, 45)
    assert (alias.ore, alias.minuti) == (9, 5)
    assert (nuovo.ore, nuovo.minuti) == (18, 45)
    assert nuovo is not orologio


def test_valori_predefiniti_e_nuove_entita():
    record = procedurale.nuovo_orologio()
    altro_record = procedurale.nuovo_orologio()
    istanza = OrologioDigitale()
    altra_istanza = OrologioDigitale()
    assert record is not altro_record
    assert istanza is not altra_istanza
    assert procedurale.leggi(record) == istanza.leggi() == (0, 0)
    procedurale.avanza(record, 1)
    istanza.avanza(1)
    assert procedurale.leggi(altro_record) == altra_istanza.leggi() == (0, 0)
