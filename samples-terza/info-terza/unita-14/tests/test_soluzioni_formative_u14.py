"""Casi discriminanti delle soluzioni formative dell'Unità 14.

Verifica che i riferimenti eseguibili delle soluzioni soddisfino i casi
pubblicati nelle consegne. Non sostituisce le spiegazioni pubblicate nelle
pagine: ne controlla i casi discriminanti.
"""

import pytest
from articolo_proprieta_u14 import Articolo
from controllore_simulato_u14 import AttuatoreSimulato, SensoreSimulato
from esercizi_base_u14 import (
    Attivita,
    AttivitaParziale,
    Biglietto,
    BigliettoPerCodice,
    ControlloreConMemoria,
    DurataT3,
    LimitiCorretto,
    LimitiRicorsivo,
    Peso,
    PesoDataclass,
    Punto,
    PuntoSenzaControlli,
    RegistroVisite,
    RegistroVisiteErrato,
    Squadra,
    SquadraFrozen,
    chiama_prelievo,
    confronto_aggiornamento,
    preleva,
    round_trip_articolo,
    secondi_validi_modulo,
    tre_snapshot,
)
from intervalli_u14 import Intervallo
from misure_modello_dati_u14 import MisuraFrozen
from prenotazioni_u14 import Prenotazione, RegistroPrenotazioni
from problemi_algoritmici_u14 import (
    applica_lotto,
    coppie_in_conflitto,
    minuti_disponibili,
    prima_fascia_comune,
    prima_fascia_libera,
    riepilogo_misure,
    sposta_lotto,
    unisci_inventari,
)

# --- E01: il setter ricorsivo -----------------------------------------------


def test_e01_versione_difettosa_ricorsione():
    with pytest.raises(RecursionError):
        LimitiRicorsivo(0, 10).minimo = 5


def test_e01_versione_corretta_scrive_dopo_il_controllo():
    limite = LimitiCorretto(0, 10)
    limite.minimo = 5
    assert (limite.minimo, limite.massimo) == (5, 10)


# --- E02: aggiornamento parziale contro aggiornamento atomico -----------------


def test_e02_versione_difettosa_lascia_lo_stato_a_meta():
    attivita = AttivitaParziale(1, 8, "Lab A")
    with pytest.raises(ValueError):
        attivita.sposta(3, 9, "")
    assert attivita.dati() == (3, 9, "Lab A")  # scritture parziali avvenute


def test_e02_versione_corretta_stato_invariato():
    attivita = Attivita(1, 8, "Lab A")
    with pytest.raises(ValueError):
        attivita.sposta(3, 9, "")
    assert attivita.dati() == (1, 8, "Lab A")


# --- E03: contenitore sulla classe ---------------------------------------------


def test_e03_versione_difettosa_interferisce():
    primo = RegistroVisiteErrato("primo")
    secondo = RegistroVisiteErrato("secondo")
    primo.registra("v1")
    assert secondo.visite == ["v1"]


def test_e03_versione_corretta_indipendente():
    primo = RegistroVisite("primo")
    secondo = RegistroVisite("secondo")
    primo.registra("v1")
    primo.registra("v2")
    secondo.registra("w1")
    assert primo.visite == ["v1", "v2"]
    assert secondo.visite == ["w1"]


# --- E04: eq per solo codice contro eq completa ---------------------------------


def test_e04_versione_difettosa_confonde():
    assert BigliettoPerCodice("B01", "A", 12) == BigliettoPerCodice("B01", "C", 30)


def test_e04_versione_corretta_distingue():
    assert Biglietto("B01", "A", 12) == Biglietto("B01", "A", 12)
    assert Biglietto("B01", "A", 12) != Biglietto("B01", "C", 30)
    assert Biglietto.__eq__(Biglietto("B01", "A", 12), "B01") is NotImplemented


# --- E05: annotazione contro validazione ----------------------------------------


def test_e05_annotazione_senza_controllo_accetta():
    assert PuntoSenzaControlli("otto", 10).x == "otto"


def test_e05_controllo_scritto_rifiuta():
    for x, y in (("otto", 10), (True, 10), (-1, 10), (10, 101)):
        with pytest.raises(ValueError):
            Punto(x, y)


# --- T03: factory e validatore statico -------------------------------------------


def test_t03_factory_0_e_3_minuti():
    assert DurataT3.da_minuti(0).secondi == 0
    assert DurataT3.da_minuti(3).secondi == 180


def test_t03_validatore_statico_e_funzione_coincidono():
    for valore in (0, 3, -1, True, "90"):
        assert DurataT3.secondi_validi(valore) == secondi_validi_modulo(valore)


# --- T04/T05: rappresentazioni e dataclass equivalente ----------------------------


def test_t04_str_repr_con_unita_e_zeri():
    peso = Peso("007", 0)
    assert str(peso) == "007: 0 g"
    assert repr(peso) == "Peso(codice='007', grammi=0)"


def test_t05_dataclass_stesso_contratto():
    assert PesoDataclass("007", 12) == PesoDataclass("007", 12)
    assert PesoDataclass("007", 12) is not PesoDataclass("007", 12)
    assert str(PesoDataclass("007", 12)) == str(Peso("007", 12))
    with pytest.raises(ValueError):
        PesoDataclass("", 12)


# --- T06: contenitori indipendenti -----------------------------------------------


def test_t06_default_factory_indipendenti():
    squadra_a = Squadra("alfa")
    squadra_b = Squadra("beta")
    squadra_a.componenti.append("G01")
    assert squadra_b.componenti == []


# --- T07: eccezione di dominio ----------------------------------------------------


def test_t07_rifiuto_distinto_dall_errore():
    from esercizi_base_u14 import SaldoInsufficiente

    with pytest.raises(SaldoInsufficiente):
        preleva(500, 600)
    with pytest.raises(ValueError):
        preleva(-1, 10)


def test_t07_chiamante_conserva_il_saldo():
    saldo, messaggio = chiama_prelievo(500, 600)
    assert saldo == 500
    assert "rifiutato" in messaggio
    saldo, messaggio = chiama_prelievo(500, 200)
    assert (saldo, messaggio) == (300, "prelievo riuscito")


# --- T08: round-trip dell'Articolo --------------------------------------------------


def test_t08_round_trip_valori_equivalenti_identita_distinta():
    articolo = Articolo("007", "Vite, lunga", 4, 25)
    riga, dati = round_trip_articolo(articolo)
    assert riga == ["007", "Vite, lunga", "4", "25"]
    assert dati == articolo.dati()
    assert dati is not articolo.dati()


# --- X01: frozen e contenuti mutabili ------------------------------------------------


def test_x01_frozen_blocca_assegnamenti_ma_non_le_mutazioni():
    from dataclasses import FrozenInstanceError

    squadra = SquadraFrozen("alfa")
    with pytest.raises(FrozenInstanceError):
        squadra.nome = "beta"
    squadra.componenti.append("G01")
    assert squadra.componenti == ["G01"]


# --- X02: due contratti di aggiornamento ----------------------------------------------


def test_x02_alias_osservano_effetti_diversi():
    osservazioni = confronto_aggiornamento()
    assert osservazioni["alias_articolo_segue_la_mutazione"] is True
    assert osservazioni["alias_prenotazione_conserva_il_valore"] is True
    assert osservazioni["registro_punta_al_nuovo_valore"] is True


# --- X03: tre snapshot -------------------------------------------------------------------


def test_x03_tre_snapshot_con_politiche_distinte():
    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("PR-01", "Lab A", Intervallo(540, 600), 20))
    valori, copia, record = tre_snapshot(registro)
    assert valori == copia
    assert len(record) == 1
    # i valori frozen condivisi non possono essere mutati; i record sì,
    # senza effetti sul registro
    record[0]["aula"] = "manomessa"
    assert registro.cerca("PR-01").aula == "Lab A"


# --- X04: controllore con memoria ----------------------------------------------------------


def test_x04_cronologia_deterministica():
    sensore = SensoreSimulato([18, 20, 22])
    attuatore = AttuatoreSimulato()
    controllore = ControlloreConMemoria(sensore, attuatore, soglia=20)
    for _ in range(3):
        controllore.passo()
    assert controllore.cronologia() == [(18, "acceso"), (20, "spento"), (22, "spento")]
    # la copia della cronologia non tocca il controllore
    copia = controllore.cronologia()
    copia.append((0, "x"))
    assert len(controllore.cronologia()) == 3


# --- T09: prima fascia libera ---------------------------------------------------------------


def test_t09_caso_pubblico():
    libera = prima_fascia_libera(Intervallo(0, 60), 10, [Intervallo(0, 20), Intervallo(30, 40)])
    assert (libera.inizio_min, libera.fine_min) == (20, 30)


def test_t09_ordinamento_non_cronologico_e_fuori_finestra():
    libera = prima_fascia_libera(Intervallo(30, 90), 10, [Intervallo(0, 20), Intervallo(30, 40)])
    assert (libera.inizio_min, libera.fine_min) == (40, 50)


def test_t09_vuoto_inizio_libero_nessun_posto_durata_oltre():
    assert prima_fascia_libera(Intervallo(0, 60), 10, []) == Intervallo(0, 10)
    assert prima_fascia_libera(Intervallo(0, 60), 10, [Intervallo(0, 55)]) is None
    assert prima_fascia_libera(Intervallo(0, 60), 90, []) is None


def test_t09_input_non_mutati():
    occupati = [Intervallo(0, 20), Intervallo(30, 40)]
    copia = list(occupati)
    prima_fascia_libera(Intervallo(0, 60), 10, occupati)
    assert occupati == copia


# --- T10: riepilogo misure ---------------------------------------------------------------------


def test_t10_caso_pubblico_e_vuoto():
    misure = [MisuraFrozen("M1", 0), MisuraFrozen("M2", 12), MisuraFrozen("M3", 12)]
    assert riepilogo_misure(misure) == {
        "quantita": 3,
        "totale_cm": 24,
        "minimo_cm": 0,
        "massimo_cm": 12,
    }
    assert riepilogo_misure([]) == {
        "quantita": 0,
        "totale_cm": 0,
        "minimo_cm": None,
        "massimo_cm": None,
    }


def test_t10_duplicati_non_eliminati():
    misure = [MisuraFrozen("M1", 12), MisuraFrozen("M2", 12)]
    assert riepilogo_misure(misure)["quantita"] == 2


# --- T11: coppie in conflitto ---------------------------------------------------------------------


def test_t11_caso_pubblico_una_sola_coppia():
    prenotazioni = [
        Prenotazione("A", "Lab 1", Intervallo(0, 20), 5),
        Prenotazione("B", "Lab 1", Intervallo(10, 30), 5),
        Prenotazione("C", "Lab 1", Intervallo(30, 40), 5),
    ]
    assert coppie_in_conflitto(prenotazioni) == [(0, 1)]


def test_t11_aula_diversa_uguaglianza_contenimento():
    diverse = [
        Prenotazione("A", "Lab 1", Intervallo(0, 20), 5),
        Prenotazione("B", "Lab 2", Intervallo(10, 30), 5),
    ]
    assert coppie_in_conflitto(diverse) == []
    contenute = [
        Prenotazione("A", "Lab 1", Intervallo(0, 30), 5),
        Prenotazione("B", "Lab 1", Intervallo(10, 20), 5),
    ]
    assert coppie_in_conflitto(contenute) == [(0, 1)]
    uguali = [
        Prenotazione("A", "Lab 1", Intervallo(0, 20), 5),
        Prenotazione("B", "Lab 1", Intervallo(0, 20), 5),
    ]
    assert coppie_in_conflitto(uguali) == [(0, 1)]


# --- T12: lotto senza effetti parziali -------------------------------------


def test_t12_primo_valido_secondo_in_conflitto():
    from prenotazioni_u14 import ConflittoPrenotazione

    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("F", "Lab 1", Intervallo(0, 30), 5))
    lotto = [
        Prenotazione("G", "Lab 1", Intervallo(30, 60), 5),
        Prenotazione("H", "Lab 1", Intervallo(40, 70), 5),
    ]
    with pytest.raises(ConflittoPrenotazione):
        applica_lotto(registro, lotto)
    assert [p.codice for p in registro.prenotazioni()] == ["F"]


def test_t12_lotto_vuoto_e_duplicati():
    from prenotazioni_u14 import CodiceDuplicato

    registro = RegistroPrenotazioni()
    applica_lotto(registro, [])
    assert registro.riepilogo()["numero_prenotazioni"] == 0
    lotto = [
        Prenotazione("X", "Lab 1", Intervallo(0, 30), 5),
        Prenotazione("X", "Lab 2", Intervallo(30, 60), 5),
    ]
    with pytest.raises(CodiceDuplicato):
        applica_lotto(registro, lotto)
    assert registro.riepilogo()["numero_prenotazioni"] == 0


# --- T13: unione di inventari ----------------------------------------------


def magazzino_con(*records):
    from magazzino_composto_u14 import Magazzino

    magazzino = Magazzino()
    for record in records:
        magazzino.inserisci(*record)
    return magazzino


def test_t13_unione_ordinata_e_rifiuto_del_duplicato():
    primo = magazzino_con(("007", "Vite, lunga", 4, 25))
    secondo = magazzino_con(("012", 'Caffè "A"', 2, 350))
    unito = unisci_inventari(primo, secondo)
    assert [dat.codice for dat in unito.articoli()] == ["007", "012"]
    assert unito.riepilogo()["valore_centesimi"] == 800

    con_stesso_codice = magazzino_con(("7", "Altro", 1, 1))
    unito_distinti = unisci_inventari(primo, con_stesso_codice)
    assert [dat.codice for dat in unito_distinti.articoli()] == ["007", "7"]

    duplicato = magazzino_con(("007", "Vite, lunga", 4, 25))
    with pytest.raises(ValueError):
        unisci_inventari(primo, duplicato)
    # le raccolte di partenza restano invariate
    assert primo.riepilogo()["articoli"] == 1
    assert duplicato.riepilogo()["articoli"] == 1


# --- T14: minuti disponibili per aula ---------------------------------------


def test_t14_caso_pubblico():
    prenotazioni = [
        Prenotazione("A", "Lab A", Intervallo(510, 570), 5),
        Prenotazione("B", "Lab A", Intervallo(600, 690), 5),
    ]
    risultato = minuti_disponibili(Intervallo(540, 660), prenotazioni, ["Lab A", "Lab B"])
    assert risultato == {"Lab A": 30, "Lab B": 120}


def test_t14_finestra_senza_occupazione():
    risultato = minuti_disponibili(Intervallo(540, 660), [], ["Lab A"])
    assert risultato == {"Lab A": 120}


# --- X05: spostare un lotto --------------------------------------------------


def registro_base():
    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("L1", "Lab 1", Intervallo(540, 600), 5))
    registro.registra(Prenotazione("L2", "Lab 2", Intervallo(540, 600), 5))
    return registro


def test_x05_spostamento_riuscito_e_originale_intatto():
    registro = registro_base()
    spostato = sposta_lotto(registro, ["L1"], 60)
    assert [p.testo_riepilogo() for p in spostato.prenotazioni()] == [
        "L2, aula Lab 2, 540-600, 5 partecipanti",
        "L1, aula Lab 1, 600-660, 5 partecipanti",
    ]
    assert [p.testo_riepilogo() for p in registro.prenotazioni()] == [
        "L1, aula Lab 1, 540-600, 5 partecipanti",
        "L2, aula Lab 2, 540-600, 5 partecipanti",
    ]


def test_x05_superamento_della_giornata():
    registro = registro_base()
    with pytest.raises(ValueError):
        sposta_lotto(registro, ["L1"], 900)


def test_x05_conflitto_con_non_spostata():
    from prenotazioni_u14 import ConflittoPrenotazione

    registro = registro_base()
    registro.registra(Prenotazione("L3", "Lab 1", Intervallo(660, 720), 5))
    # L1 spostata di 120 minuti va su [660, 720): stessa aula di L3
    with pytest.raises(ConflittoPrenotazione):
        sposta_lotto(registro, ["L1"], 120)


def test_x05_sovrapposizione_con_le_posizioni_originarie_escluse():
    # L1 spostata di 20 minuti va su [20, 50), che si sovrappone alla
    # posizione ORIGINARIA di L2 [40, 70) nella stessa aula. L2 però è nel
    # lotto: le posizioni originarie sono escluse e lo spostamento riesce,
    # perché le nuove posizioni [20, 50) e [60, 90) non si sovrappongono.
    registro = RegistroPrenotazioni()
    registro.registra(Prenotazione("L1", "Lab 1", Intervallo(0, 30), 5))
    registro.registra(Prenotazione("L2", "Lab 1", Intervallo(40, 70), 5))
    spostato = sposta_lotto(registro, ["L1", "L2"], 20)
    posizioni = [
        (p.codice, p.intervallo.inizio_min, p.intervallo.fine_min) for p in spostato.prenotazioni()
    ]
    assert posizioni == [("L1", 20, 50), ("L2", 60, 90)]


def test_x05_spostamento_nullo_rifiutato():
    registro = registro_base()
    with pytest.raises(ValueError):
        sposta_lotto(registro, ["L1"], 0)


# --- X06: prima fascia comune --------------------------------------------------


def test_x06_prima_fascia_libera_su_a_non_lo_e_su_b():
    fascia = prima_fascia_comune(
        Intervallo(540, 660), 30, [Intervallo(540, 570)], [Intervallo(540, 600)]
    )
    assert (fascia.inizio_min, fascia.fine_min) == (600, 630)


def test_x06_intersezione_vuota_e_estremi_adiacenti():
    assert prima_fascia_comune(Intervallo(540, 660), 60, [Intervallo(540, 660)], []) is None
    adiacenti = prima_fascia_comune(
        Intervallo(540, 660), 30, [Intervallo(540, 570)], [Intervallo(570, 540 + 60)]
    )
    assert adiacenti is not None
    assert adiacente_valido(adiacenti, [Intervallo(540, 570), Intervallo(570, 600)])


def adiacente_valido(fascia, blocchi):
    return not any(fascia.sovrapposto_a(blocco) for blocco in blocchi)


def test_x06_durata_oltre_la_finestra():
    assert prima_fascia_comune(Intervallo(540, 660), 200, [], []) is None
