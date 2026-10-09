"""Regressione dei contratti dei nuovi esempi OOP-03 e OOP-04."""

from dataclasses import FrozenInstanceError, fields

import pytest
from colori_espliciti_u14 import ColoreRGB as ColoreEsplicito
from colori_espliciti_u14 import componente_valida
from colori_modello_dati_u14 import ColoreRGB, ColoreRGBDataclass, DiarioFrozen, SchedaColori
from palette_composizione_u14 import Palette, PannelloAudio, testo_colori
from volume_audio_base_u14 import VolumeAudio as VolumeBase
from volume_audio_u14 import VolumeAudio


@pytest.mark.parametrize("valore", [-1, 101, True, False, 30.0, "30", None])
def test_volume_base_rifiuta_senza_modifiche(valore):
    with pytest.raises(ValueError):
        VolumeBase(valore)
    volume = VolumeBase(30)
    with pytest.raises(ValueError):
        volume.livello = valore
    assert volume.livello == 30
    assert volume.silenzioso is False


def test_volume_base_derivato_e_sola_lettura():
    volume = VolumeBase(30)
    volume.livello = 0
    assert volume.silenzioso is True
    with pytest.raises(AttributeError):
        volume.silenzioso = False
    volume.livello = 100
    assert volume.silenzioso is False


@pytest.mark.parametrize("candidato", [(60, 50), (40, 120), (True, 80), (40, "80")])
def test_configurazione_rifiutata_conserva_tutto_lo_stato(candidato):
    volume = VolumeAudio(70, 80)
    with pytest.raises(ValueError):
        volume.configura(*candidato)
    assert (volume.livello, volume.limite_massimo) == (70, 80)


@pytest.mark.parametrize("candidato", [(40, 50), (90, 100), (0, 0), (100, 100)])
def test_configurazione_valida_usa_il_candidato_completo(candidato):
    volume = VolumeAudio(70, 80)
    assert volume.configura(*candidato) is None
    assert (volume.livello, volume.limite_massimo) == candidato


def test_setter_controllano_la_relazione_e_alias_vede_mutazione():
    volume = VolumeAudio(70, 80)
    alias = volume
    with pytest.raises(ValueError):
        volume.limite_massimo = 50
    with pytest.raises(ValueError):
        volume.livello = 90
    assert (volume.livello, volume.limite_massimo) == (70, 80)
    volume.configura(40, 50)
    assert (alias.livello, alias.limite_massimo) == (40, 50)


def test_due_setter_non_garantiscono_richiesta_indivisibile():
    volume = VolumeAudio(70, 80)
    volume.livello = 40
    with pytest.raises(ValueError):
        volume.limite_massimo = 120
    assert (volume.livello, volume.limite_massimo) == (40, 80)


@pytest.mark.parametrize("tipo", [ColoreEsplicito, ColoreRGBDataclass, ColoreRGB])
@pytest.mark.parametrize("valore", [-1, 256, True, 80.0, "80", None])
def test_componenti_rifiutate_in_ogni_posizione(tipo, valore):
    for indice in range(3):
        candidato = [12, 80, 160]
        candidato[indice] = valore
        with pytest.raises(ValueError):
            tipo(*candidato)


@pytest.mark.parametrize("tipo", [ColoreEsplicito, ColoreRGB])
def test_factory_proiezione_e_regola_senza_istanza(tipo):
    assert tipo.nero().come_tupla() == (0, 0, 0)
    assert tipo.bianco().come_tupla() == (255, 255, 255)
    assert tipo.nero() is not tipo.nero()
    for valore in (0, 80, 255, -1, 256, True, "80"):
        assert tipo.componente_valida(valore) is componente_valida(valore)


@pytest.mark.parametrize("tipo", [ColoreEsplicito, ColoreRGBDataclass, ColoreRGB])
def test_rappresentazioni_e_uguaglianza_completa(tipo):
    a = tipo(12, 80, 160)
    b = tipo(12, 80, 160)
    assert a == b and a is not b
    assert str(a) == "RGB(12, 80, 160)"
    assert repr(a) == f"{tipo.__name__}(rosso=12, verde=80, blu=160)"
    assert repr([a]) == f"[{repr(a)}]"
    for componenti in ((13, 80, 160), (12, 81, 160), (12, 80, 200)):
        diverso = tipo(*componenti)
        assert a != diverso and diverso != a
    assert a.__eq__((12, 80, 160)) is NotImplemented
    assert (a == (12, 80, 160)) is False
    assert ((12, 80, 160) == a) is False


def test_versioni_diverse_confrontano_proiezioni_non_istanze():
    esplicito = ColoreEsplicito(12, 80, 160)
    mutabile = ColoreRGBDataclass(12, 80, 160)
    frozen = ColoreRGB(12, 80, 160)
    assert esplicito != mutabile and mutabile != esplicito
    assert esplicito != frozen and frozen != esplicito
    assert mutabile != frozen and frozen != mutabile
    assert esplicito.come_tupla() == frozen.come_tupla()


def test_post_init_non_controlla_assegnamenti_successivi():
    colore = ColoreRGBDataclass(12, 80, 160)
    colore.blu = -1
    assert colore.blu == -1


def test_frozen_sostituzione_alias_classvar_e_hash():
    colore = ColoreRGB(12, 80, 160)
    alias = colore
    with pytest.raises(FrozenInstanceError):
        colore.blu = 200
    colore = ColoreRGB(colore.rosso, colore.verde, 200)
    assert alias.come_tupla() == (12, 80, 160)
    assert colore.come_tupla() == (12, 80, 200)
    assert alias is not colore
    assert [campo.name for campo in fields(ColoreRGB)] == ["rosso", "verde", "blu"]
    assert {ColoreRGB.nero(): "nero"}[ColoreRGB(0, 0, 0)] == "nero"
    with pytest.raises(TypeError):
        hash(ColoreRGBDataclass(0, 0, 0))


def test_default_factory_e_limite_superficiale_frozen():
    prima, seconda = SchedaColori("prima"), SchedaColori("seconda")
    prima.colori.append(ColoreRGB.nero())
    assert prima.colori is not seconda.colori and seconda.colori == []
    esterna = []
    assert SchedaColori("esterna", esterna).colori is esterna
    diario = DiarioFrozen("prove")
    diario.voci.append("nota")
    assert diario.voci == ["nota"]
    with pytest.raises(FrozenInstanceError):
        diario.titolo = "altro"
    with pytest.raises(TypeError):
        hash(diario)


def test_palette_copia_contenitore_condivide_valori_e_cerca_per_uguaglianza():
    blu = ColoreRGB(12, 80, 160)
    elenco = [blu, ColoreRGB.bianco(), ColoreRGB(12, 80, 160)]
    palette = Palette(elenco)
    elenco.clear()
    assert len(palette.colori()) == 3
    assert palette.colori()[0] is blu
    assert palette.indice_di(ColoreRGB(12, 80, 160)) == 0
    assert palette.indice_di(ColoreRGB.nero()) is None
    assert Palette([]).colori() == ()
    assert Palette([]).indice_di(blu) is None
    assert testo_colori([]) == ""
    assert testo_colori([blu]) == "RGB(12, 80, 160)"


@pytest.mark.parametrize("invalido", [(12, 80, 160), "blu", ColoreEsplicito(12, 80, 160)])
def test_palette_rifiuta_elementi_e_ricerche_di_altro_tipo(invalido):
    with pytest.raises(ValueError):
        Palette([ColoreRGB.nero(), invalido])
    with pytest.raises(ValueError):
        Palette([]).indice_di(invalido)


def test_pannelli_compongono_volumi_distinti_e_aggregano_stessa_palette():
    palette = Palette([ColoreRGB(12, 80, 160), ColoreRGB.bianco()])
    primo = PannelloAudio(70, 80, palette)
    secondo = PannelloAudio(20, 80, palette)
    assert primo.configura_volume(40, 50) is None
    assert (primo.livello, secondo.livello) == (40, 20)
    assert primo._volume is not secondo._volume
    assert primo._palette is secondo._palette is palette
    assert primo.testo_posizione(ColoreRGB(12, 80, 160)) == "colore in posizione 0"
    assert secondo.testo_posizione(ColoreRGB.nero()) == "colore assente"
    with pytest.raises(ValueError):
        primo.configura_volume(40, 120)
    assert (primo.livello, primo._volume.limite_massimo) == (40, 50)
    primo.configura_volume(0, 0)
    assert primo.silenzioso is True and secondo.silenzioso is False
    del primo
    assert len(palette.colori()) == 2 and secondo.livello == 20


def test_pannello_rifiuta_collaboratore_sbagliato():
    with pytest.raises(ValueError):
        PannelloAudio(30, 80, [])
