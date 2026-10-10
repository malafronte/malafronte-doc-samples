import pytest

from client_orologi_u15 import descrizioni
from orologi_base_u15 import OrologioDigitale
from orologi_derivati_u15 import OrologioConEtichetta, OrologioConSveglia

FACTORY = [
    OrologioDigitale,
    lambda ore, minuti: OrologioConEtichetta(ore, minuti, " Laboratorio "),
    lambda ore, minuti: OrologioConSveglia(ore, minuti, 7, 0),
]


@pytest.mark.parametrize("factory", FACTORY)
def test_contratto(factory, capsys):
    orologio = factory(23, 58)
    altro = factory(8, 15)
    assert orologio.avanza(5) is None
    assert orologio.leggi() == (0, 3)
    assert orologio.testo() == "00:03"
    assert orologio.avanza(1440) is None
    assert orologio.leggi() == (0, 3)
    assert orologio.imposta(8, 15) is None
    prima = orologio.leggi()
    assert "08:15" in orologio.descrizione()
    assert orologio.leggi() == prima
    assert altro.leggi() == (8, 15)
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("factory", FACTORY)
@pytest.mark.parametrize("ore,minuti", [(24, 0), (-1, 0), (12, 75), (True, 0), (1, "0")])
def test_orario_invalido(factory, ore, minuti):
    with pytest.raises(ValueError):
        factory(ore, minuti)
    orologio = factory(8, 15)
    with pytest.raises(ValueError):
        orologio.imposta(ore, minuti)
    assert orologio.leggi() == (8, 15)


@pytest.mark.parametrize("factory", FACTORY)
@pytest.mark.parametrize("durata", [True, -1, "5", 2.5])
def test_durata_invalida(factory, durata):
    orologio = factory(8, 15)
    with pytest.raises(ValueError):
        orologio.avanza(durata)
    assert orologio.testo() == "08:15"


def test_descrizioni_sveglia():
    orologi = [factory(8, 15) for factory in FACTORY]
    assert descrizioni(orologi) == [
        "Ora 08:15",
        "Laboratorio — 08:15",
        "Ora 08:15; sveglia 07:00",
    ]
    sveglia = orologi[2]
    sveglia.avanza(120)
    assert sveglia.leggi_sveglia() == (7, 0)
    with pytest.raises(ValueError):
        sveglia.imposta_sveglia(6, 80)
    assert sveglia.leggi() == (10, 15)
    assert sveglia.leggi_sveglia() == (7, 0)
    assert sveglia.imposta_sveglia(6, 30) is None
    assert sveglia.leggi_sveglia() == (6, 30)


@pytest.mark.parametrize("etichetta", ["", "  ", None, 5])
def test_etichetta(etichetta):
    with pytest.raises(ValueError):
        OrologioConEtichetta(8, 15, etichetta)


def test_controesempi_discriminati(capsys):
    class DurataLimitata(OrologioDigitale):
        def avanza(self, minuti_trascorsi):
            if minuti_trascorsi > 60:
                raise ValueError("limite incompatibile")
            return super().avanza(minuti_trascorsi)

    class FormatoAlterato(OrologioConEtichetta):
        def testo(self):
            return "Laboratorio — " + super().testo()

    class StampaAggiunta(OrologioDigitale):
        def descrizione(self):
            print("effetto estraneo")
            return super().descrizione()

    with pytest.raises(ValueError):
        DurataLimitata().avanza(1440)
    assert FormatoAlterato(8, 15, "Laboratorio").testo() != "08:15"
    StampaAggiunta().descrizione()
    assert capsys.readouterr().out == "effetto estraneo\n"
