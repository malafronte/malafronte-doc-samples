"""Regressioni della revisione: contratti dichiarati nelle schede U14."""

import csv
from dataclasses import FrozenInstanceError
from io import StringIO

import pytest
from articolo_proprieta_u14 import Articolo
from esercizi_base_u14 import DurataT3, Peso, PesoDataclass, Segmento, round_trip_articolo
from intervalli_u14 import Intervallo
from prenotazioni_u14 import ConflittoPrenotazione, Prenotazione, RegistroPrenotazioni
from problemi_algoritmici_u14 import applica_lotto, sposta_lotto, unisci_inventari


@pytest.mark.parametrize("ore,minuti,atteso", [(0, 0, 0), (0, 3, 180), (1, 59, 7140)])
def test_t03_factory_ore_e_minuti(ore, minuti, atteso):
    assert DurataT3.da_ore_e_minuti(ore, minuti).secondi == atteso


@pytest.mark.parametrize("ore,minuti", [(-1, 0), (True, 0), ("90", 0), (0, 60), (0, False)])
def test_t03_factory_rifiuta_argomenti_fuori_dominio(ore, minuti):
    with pytest.raises(ValueError):
        DurataT3.da_ore_e_minuti(ore, minuti)


@pytest.mark.parametrize("grammi", [0, 12, 250])
def test_t05_str_conservato_nella_dataclass(grammi):
    assert str(PesoDataclass("007", grammi)) == str(Peso("007", grammi))


def test_t05_assegnamento_bloccato():
    with pytest.raises(FrozenInstanceError):
        PesoDataclass("007", 12).grammi = 0


@pytest.mark.parametrize("inizio,fine", [(10, -1), (10, "fine"), (True, 10)])
def test_t02_rifiuto_conserva_l_intera_coppia(inizio, fine):
    segmento = Segmento(0, 20)
    with pytest.raises(ValueError):
        segmento.imposta(inizio, fine)
    assert segmento.dati() == (0, 20)


def test_t08_quoting_csv_e_confronto_del_medesimo_snapshot():
    articolo = Articolo("007", 'Caffè, "A"', 4, 25)
    prima = articolo.dati()
    riga, dopo = round_trip_articolo(articolo)
    flusso = StringIO(newline="")
    csv.writer(flusso).writerow(riga)
    assert flusso.getvalue().strip() == '007,"Caffè, ""A""",4,25'
    flusso.seek(0)
    assert next(csv.reader(flusso)) == riga
    assert prima == dopo
    assert prima is not dopo


def test_x01_soglia_valida_e_non_riassegnabile():
    from esercizi_base_u14 import Soglia

    assert Soglia(0).valore == 0
    for valore in (-1, True, "3"):
        with pytest.raises(ValueError):
            Soglia(valore)
    with pytest.raises(FrozenInstanceError):
        Soglia(3).valore = -1


def test_t12_diario_ripristina_anche_gli_alias_e_l_ordine():
    registro = RegistroPrenotazioni()
    originale = Prenotazione("F", "A", Intervallo(0, 30), 5)
    registro.registra(originale)
    prima = registro.prenotazioni()
    lotto = [
        Prenotazione("G", "A", Intervallo(30, 60), 5),
        Prenotazione("H", "A", Intervallo(40, 70), 5),
    ]
    with pytest.raises(ConflittoPrenotazione):
        applica_lotto(registro, lotto)
    assert registro.prenotazioni() == prima
    assert registro.cerca("F") is originale


def test_t12_tipo_errato_dopo_inserimento_valido_non_lascia_effetti():
    registro = RegistroPrenotazioni()
    originale = Prenotazione("F", "A", Intervallo(0, 30), 5)
    registro.registra(originale)
    with pytest.raises(ValueError):
        applica_lotto(registro, [Prenotazione("G", "A", Intervallo(30, 60), 5), None])
    assert registro.prenotazioni() == (originale,)
    assert registro.cerca("F") is originale


def test_t13_indipendenza_con_mutazione_pubblica_non_con_snapshot_is():
    from magazzino_composto_u14 import Magazzino

    primo = Magazzino()
    primo.inserisci("007", "Vite", 4, 25)
    secondo = Magazzino()
    unito = unisci_inventari(primo, secondo)
    unito.modifica("007", "Vite", 9, 25)
    assert primo.cerca("007").quantita == 4
    assert unito.cerca("007").quantita == 9


@pytest.mark.parametrize("delta", [-20, 20])
def test_x05_traslazione_comune_preserva_la_non_sovrapposizione(delta):
    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("L1", "A", Intervallo(100, 130), 5))
    registro.registra(Prenotazione("L2", "A", Intervallo(140, 170), 5))
    risultato = sposta_lotto(registro, ["L1", "L2"], delta)
    assert not risultato.cerca("L1").sovrapposta_a(risultato.cerca("L2"))
    assert registro.cerca("L1").intervallo == Intervallo(100, 130)


def test_x05_lotto_vuoto_produce_un_registro_distinto():
    originale = RegistroPrenotazioni()
    risultato = sposta_lotto(originale, [], 20)
    assert risultato is not originale
    assert risultato.prenotazioni() == ()


@pytest.mark.parametrize("delta", [-101, True, "20", 0])
def test_x05_rifiuto_non_modifica_i_valori_originali(delta):
    registro = RegistroPrenotazioni()
    originale = Prenotazione("L1", "A", Intervallo(100, 130), 5)
    registro.registra(originale)
    with pytest.raises(ValueError):
        sposta_lotto(registro, ["L1"], delta)
    assert registro.prenotazioni() == (originale,)
    assert registro.cerca("L1") is originale


def test_x03_lista_interna_diversa_da_copia_superficiale():
    from esercizi_base_u14 import tre_snapshot

    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("F", "A", Intervallo(0, 30), 5))
    valori, copia, record = tre_snapshot(registro)
    assert valori is not copia
    assert valori[0] is copia[0]
    copia.clear()
    assert len(registro.prenotazioni()) == 1
    record[0]["aula"] = "B"
    assert registro.cerca("F").aula == "A"
    valori.clear()
    assert registro.prenotazioni() == ()


def test_x03_magazzino_condivide_gli_elementi_della_copia_superficiale():
    from esercizi_base_u14 import tre_snapshot_magazzino
    from magazzino_composto_u14 import Magazzino

    magazzino = Magazzino()
    magazzino.inserisci("007", "Vite", 4, 25)
    valori, copia, record = tre_snapshot_magazzino(magazzino)
    assert valori is not copia
    assert valori[0] is copia[0]
    copia[0].aggiorna("Vite", 9, 25)
    assert magazzino.cerca("007").quantita == 9
    record[0]["quantita"] = 100
    assert magazzino.cerca("007").quantita == 9
    copia.clear()
    assert magazzino.riepilogo()["articoli"] == 1
    valori.clear()
    assert magazzino.riepilogo()["articoli"] == 0


@pytest.mark.parametrize(
    "errore,testo", [(None, "registrazione riuscita"), (ValueError("vuoto"), "codice non valido")]
)
def test_e06_messaggio_coerente_con_esito(errore, testo, capsys):
    from esercizi_base_u14 import registra_socio

    class RegistroProva:
        def registra(self, codice):
            if errore is not None:
                raise errore

    assert registra_socio(RegistroProva(), "A") is None
    assert testo in capsys.readouterr().out


def test_e06_duplicato_non_annuncia_successo(capsys):
    from esercizi_base_u14 import registra_socio
    from prenotazioni_u14 import CodiceDuplicato

    class RegistroProva:
        def registra(self, codice):
            raise CodiceDuplicato(codice)

    assert registra_socio(RegistroProva(), "A") is None
    testo = capsys.readouterr().out
    assert "registrazione rifiutata" in testo
    assert "riuscita" not in testo


def test_e06_errore_inatteso_si_propaga(capsys):
    from esercizi_base_u14 import registra_socio

    with pytest.raises(AttributeError):
        registra_socio(object(), "A")
    assert capsys.readouterr().out == ""
