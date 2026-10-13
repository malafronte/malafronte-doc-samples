"""Suite dell'indice BST di consultazione (tappa U17).

Casi pubblici PU17-01-PU17-10 verificabili sul dominio, tre casi propri
motivati - un confine dell'ordine lessicografico, un difetto plausibile
confrontato con un oracolo `dict` e una prova del ciclo di vita della
fotografia - e la regressione dei contratti mantenuti. I test usano soltanto
dati sintetici; per la regressione di persistenza usano file temporanei e la
regressione completa PU17-10 si verifica con la suite cumulativa U5-U17.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_indice_bst_u17.py
"""
import pytest

from coda_richieste_u16 import CodaDequeU16, RichiestaConsultazione, ServizioConsultazione
from indice_bst_u17 import IndiceBSTU17, costruisci_indice, misura_costruzione
from registro_consultazione_u15 import PoliticaSoglia
from registro_dominio import formatta_euro
from registro_modello_u14 import CodiceDuplicato, Preventivo, RegistroPreventivi
from registro_persistenza import carica_archivio, esporta_csv, salva_archivio
from spedizione_u5 import totale_spedizione

CRESCENTI = ["001", "002", "003", "004", "005", "006", "007"]
MESCOLATI = ["004", "002", "006", "001", "003", "005", "007"]


def raccolta_canonica():
    """Registro di riferimento U17: 007/locale/450, 012/nazionale/0, 003/locale/1200."""
    registro = RegistroPreventivi()
    registro.inserisci("007", "locale", 450)
    registro.inserisci("012", "nazionale", 0)
    registro.inserisci("003", "locale", 1200)
    return registro


def preventivo_sintetico(codice):
    """Record sintetico distinto: il totale deriva dal codice per il confronto."""
    return Preventivo(codice, "locale", int(codice) * 100)


def indice_su_codici(codici):
    """Indice costruito sui record sintetici dei codici indicati."""
    return costruisci_indice([preventivo_sintetico(codice) for codice in codici])


# --- Casi pubblici PU17-01 - PU17-10 ---


def test_pu17_01_vista_ordinata_e_ordine_della_raccolta():
    registro = raccolta_canonica()
    indice = costruisci_indice(registro.preventivi())
    assert indice.inordine() == ["003", "007", "012"]  # vista ordinata dell'indice
    assert [c for c, _ in indice.voci_ordinate()] == ["003", "007", "012"]
    assert [p.codice for p in registro.preventivi()] == ["007", "012", "003"]  # raccolta
    assert len(indice) == 3
    assert indice.minimo() == "003"
    assert indice.massimo() == "012"
    indice.controlla_invarianti()


def test_pu17_02_ricerca_esatta_conserva_i_dati():
    indice = costruisci_indice(raccolta_canonica().preventivi())
    trovato = indice.cerca("007")
    assert trovato == Preventivo("007", "locale", 450)
    assert trovato.destinazione == "locale"
    assert trovato.totale_cent == 450
    assert indice.cerca("012").totale_cent == 0  # importo zero conservato
    assert indice.cerca("007").codice == "007"  # zeri significativi conservati
    assert indice.contiene("007") is True


def test_pu17_03_codice_assente_secondo_contratto():
    indice = costruisci_indice(raccolta_canonica().preventivi())
    assert indice.contiene("999") is False
    with pytest.raises(KeyError):
        indice.cerca("999")


def test_pu17_03_indice_vuoto_e_interrogazioni_vuote():
    indice = costruisci_indice(RegistroPreventivi().preventivi())
    assert len(indice) == 0
    assert indice.inordine() == []
    assert indice.voci_ordinate() == []
    assert indice.intervallo("000", "999") == []
    assert indice.altezza() == -1
    with pytest.raises(KeyError):
        indice.cerca("007")
    with pytest.raises(IndexError):
        indice.minimo()
    with pytest.raises(IndexError):
        indice.massimo()


def test_pu17_04_intervallo_inclusivo_agli_estremi():
    indice = costruisci_indice(raccolta_canonica().preventivi())
    coppie = indice.intervallo("003", "007")
    assert [c for c, _ in coppie] == ["003", "007"]
    assert [r.totale_cent for _, r in coppie] == [1200, 450]
    assert [c for c, _ in indice.intervallo("007", "007")] == ["007"]  # estremi uguali
    assert [c for c, _ in indice.intervallo("001", "012")] == ["003", "007", "012"]


def test_pu17_05_confini_dell_intervallo():
    indice = costruisci_indice(raccolta_canonica().preventivi())
    assert indice.intervallo("013", "020") == []  # nessun risultato
    assert [c for c, _ in indice.intervallo("004", "011")] == ["007"]  # estremi assenti
    with pytest.raises(ValueError):
        indice.intervallo("007", "003")  # estremi invertiti


def test_pu17_05_chiavi_invalide_secondo_il_contratto_locale():
    indice = costruisci_indice(raccolta_canonica().preventivi())
    with pytest.raises(TypeError):
        indice.cerca(7)  # la chiave non è una stringa
    with pytest.raises(ValueError):
        indice.cerca("")  # la stringa vuota è fuori dominio
    with pytest.raises(TypeError):
        indice.intervallo(1, "007")
    with pytest.raises(ValueError):
        indice.intervallo("", "007")
    vuoto = costruisci_indice(())
    with pytest.raises(TypeError):
        vuoto.contiene(True)  # il controllo vale anche sull'indice vuoto
    with pytest.raises(ValueError):
        vuoto.inserisci("", preventivo_sintetico("001"))


def test_pu17_06_sorgente_con_codice_ripetuto_rifiutata():
    sorgente = [
        Preventivo("007", "locale", 450),
        Preventivo("012", "nazionale", 0),
        Preventivo("007", "locale", 900),
    ]
    with pytest.raises(ValueError):
        costruisci_indice(sorgente)  # nessun indice parziale consegnato
    with pytest.raises(ValueError):
        misura_costruzione(sorgente)  # la stessa validazione anche per la misura
    with pytest.raises(TypeError):
        costruisci_indice([{"codice": "007", "destinazione": "locale", "totale_cent": 450}])
    # La sorgente valida che segue costruisce l'indice per intero.
    assert costruisci_indice(sorgente[:2]).inordine() == ["007", "012"]


def test_pu17_07_fotografia_vecchia_e_indice_ricostruito():
    registro = raccolta_canonica()
    indice_prima = costruisci_indice(registro.preventivi())
    registro.aggiorna("007", "locale", 500)
    indice_dopo = costruisci_indice(registro.preventivi())
    assert indice_prima.cerca("007").totale_cent == 450  # la vecchia fotografia resta
    assert indice_dopo.cerca("007").totale_cent == 500  # la nuova riflette l'aggiornamento
    assert indice_prima.cerca("007").codice == indice_dopo.cerca("007").codice == "007"
    assert indice_prima.inordine() == indice_dopo.inordine() == ["003", "007", "012"]
    indice_prima.controlla_invarianti()
    indice_dopo.controlla_invarianti()


def test_pu17_08_cancellazione_della_foglia():
    indice = indice_su_codici(MESCOLATI)
    assert indice.rimuovi("001") is True  # foglia del sottoalbero sinistro
    assert indice.contiene("001") is False
    assert len(indice) == 6
    assert indice.inordine() == ["002", "003", "004", "005", "006", "007"]
    for codice, record in indice.voci_ordinate():
        assert record == preventivo_sintetico(codice)  # associazioni preservate
    indice.controlla_invarianti()
    assert indice.rimuovi("001") is False  # rimozione ripetuta: nessun effetto
    assert len(indice) == 6


def test_pu17_08_cancellazione_con_un_figlio():
    indice = indice_su_codici(["004", "002", "006", "007"])
    # 006 ha il solo figlio destro 007: il collegamento passa al padre.
    assert indice.rimuovi("006") is True
    assert indice.inordine() == ["002", "004", "007"]
    assert indice.cerca("007") == preventivo_sintetico("007")
    assert indice.altezza() == 1
    indice.controlla_invarianti()


def test_pu17_08_cancellazione_con_due_figli_e_successore_con_figlio():
    indice = indice_su_codici(MESCOLATI)
    # 004 ha due figli; il successore inordine 005 ha il figlio destro 007.
    assert indice.rimuovi("004") is True
    assert indice.inordine() == ["001", "002", "003", "005", "006", "007"]
    for codice, record in indice.voci_ordinate():
        assert record == preventivo_sintetico(codice)  # nessun record trasferito
    assert indice.cerca("005") == preventivo_sintetico("005")
    assert indice.cerca("007") == preventivo_sintetico("007")
    assert indice.minimo() == "001"
    assert len(indice) == 6
    assert indice.altezza() == 2
    indice.controlla_invarianti()


def test_pu17_09_forma_e_costi_di_costruzione():
    indice_crescente, esaminati_crescente = misura_costruzione(
        [preventivo_sintetico(codice) for codice in CRESCENTI]
    )
    indice_mescolato, esaminati_mescolato = misura_costruzione(
        [preventivo_sintetico(codice) for codice in MESCOLATI]
    )
    assert indice_crescente.altezza() == 6  # forma degenerata
    assert indice_mescolato.altezza() == 2  # forma bilanciata
    assert esaminati_crescente == 21  # 0+1+2+3+4+5+6 nodi esaminati
    assert esaminati_mescolato == 10  # 0+1+1+2+2+2+2 nodi esaminati
    assert indice_crescente.inordine() == indice_mescolato.inordine() == CRESCENTI
    indice_crescente.controlla_invarianti()
    indice_mescolato.controlla_invarianti()


def test_pu17_09_costi_delle_interrogazioni_separati():
    indice_crescente, esaminati_crescente = misura_costruzione(
        [preventivo_sintetico(codice) for codice in CRESCENTI]
    )
    indice_mescolato, esaminati_mescolato = misura_costruzione(
        [preventivo_sintetico(codice) for codice in MESCOLATI]
    )
    assert indice_crescente.misura_ricerca("007") == (7, preventivo_sintetico("007"))
    assert indice_mescolato.misura_ricerca("007") == (3, preventivo_sintetico("007"))
    assert indice_crescente.misura_ricerca("008") == (7, None)  # codice assente
    assert indice_mescolato.misura_ricerca("008") == (3, None)
    # Il costo di costruzione resta separato e non cambia con le interrogazioni.
    assert (esaminati_crescente, esaminati_mescolato) == (21, 10)


def test_pu17_10_regressione_registro_e_ordini():
    registro = RegistroPreventivi()
    assert registro.inserisci("007", "locale", 450).codice == "007"
    registro.inserisci("012", "nazionale", 0)
    registro.inserisci("003", "locale", 1200)
    assert [p.codice for p in registro.preventivi()] == ["007", "012", "003"]
    assert registro.per_lista()[0] == {
        "codice": "007",
        "destinazione": "locale",
        "totale_cent": 450,
    }
    assert registro.totale_complessivo_cent == 1650
    assert formatta_euro(1200) == "12,00"  # importi in centesimi
    with pytest.raises(CodiceDuplicato):
        registro.inserisci("007", "locale", 1)  # rifiuto conservativo
    assert registro.numero == 3
    registro.aggiorna("012", "nazionale", 10)
    assert registro.per_codice("012").totale_cent == 10
    registro.elimina("012")
    assert registro.numero == 2


def test_pu17_10_regressione_schema_json_e_csv(tmp_path):
    registro = raccolta_canonica()
    percorso_json = tmp_path / "archivio.json"
    assert salva_archivio(percorso_json, registro.per_lista()) is True
    caricato, esito, dettaglio = carica_archivio(percorso_json)
    assert esito == ""
    assert dettaglio == ""
    assert caricato == registro.per_lista()  # schema JSON invariato
    assert set(caricato[0].keys()) == {"codice", "destinazione", "totale_cent"}
    percorso_csv = tmp_path / "consultazione.csv"
    assert esporta_csv(percorso_csv, registro.per_lista()) is True
    with open(percorso_csv, encoding="utf-8") as file_csv:
        prime_righe = [riga.strip() for riga in file_csv.readlines()[:2]]
    assert prime_righe == ["codice,destinazione,totale_cent", "007,locale,450"]


def test_pu17_10_regressione_tariffe_e_fifo_u16():
    # Tariffe U3/U5 invariate: base 3 + nazionale 4 + urgenza 2, base 8 oltre 2000 g.
    assert totale_spedizione(500, "nazionale", "s") == 9
    assert totale_spedizione(2500, "locale", "n") == 8
    # Coda U16: le richieste restano elaborate nell'ordine di arrivo.
    servizio = ServizioConsultazione(CodaDequeU16())
    servizio.accoda_richiesta(RichiestaConsultazione("R01", PoliticaSoglia(500)))
    servizio.accoda_richiesta(RichiestaConsultazione("R02", PoliticaSoglia(0)))
    esiti = servizio.elabora_tutte(raccolta_canonica())
    assert [e.codice for e in esiti] == ["R01", "R02"]
    assert [e.codici_ammessi for e in esiti] == [("003",), ("007", "012", "003")]


# --- Casi propri motivati ---


def test_caso_proprio_ordine_lessicografico_di_codici_di_lunghezza_diversa():
    """Caso proprio 1: la regola dichiarata è l'ordine lessicografico di Python.

    I codici `007` e `7` sono chiavi diverse e `"10"` precede `"9"`: una
    lettura numerica dell'ordine produrrebbe risultati diversi.
    """
    indice = costruisci_indice(
        [
            Preventivo("10", "locale", 1000),
            Preventivo("9", "locale", 900),
            Preventivo("007", "locale", 700),
            Preventivo("7", "locale", 7),
        ]
    )
    assert indice.inordine() == ["007", "10", "7", "9"]
    assert indice.minimo() == "007"
    assert indice.massimo() == "9"
    assert [c for c, _ in indice.intervallo("008", "9")] == ["10", "7", "9"]
    assert indice.cerca("007").totale_cent == 700
    assert indice.cerca("7").totale_cent == 7


def test_caso_proprio_oracolo_dict_su_operazioni_miste():
    """Caso proprio 2: sequenza mista confrontata con un oracolo `dict`.

    Il difetto plausibile è il record trasferito sotto la chiave sbagliata:
    un inordine ordinato da solo non lo rivela, e si confrontano chiavi e dati
    dopo ogni modifica.
    """
    indice = IndiceBSTU17()
    oracolo = {}
    operazioni = [
        ("inserisci", "004", 400),
        ("inserisci", "002", 200),
        ("inserisci", "006", 600),
        ("inserisci", "001", 100),
        ("inserisci", "003", 300),
        ("inserisci", "005", 500),
        ("inserisci", "007", 700),
        ("aggiorna", "003", 350),
        ("rimuovi", "004", None),
        ("rimuovi", "001", None),
        ("inserisci", "008", 800),
    ]
    for operazione, codice, totale in operazioni:
        if operazione == "inserisci":
            indice.inserisci(codice, Preventivo(codice, "locale", totale))
            oracolo[codice] = totale
        elif operazione == "aggiorna":
            indice.aggiorna(codice, Preventivo(codice, "locale", totale))
            oracolo[codice] = totale
        else:
            assert indice.rimuovi(codice) is True
            del oracolo[codice]
        assert len(indice) == len(oracolo)
        assert indice.voci_ordinate() == [
            (c, Preventivo(c, "locale", t)) for c, t in sorted(oracolo.items())
        ]
        assert indice.inordine() == sorted(oracolo)
        for c, t in oracolo.items():
            assert indice.cerca(c).totale_cent == t
        indice.controlla_invarianti()


def test_caso_proprio_fotografia_conservata_dopo_eliminazione():
    """Caso proprio 3: il ciclo di vita della fotografia con la nuova costruzione."""
    registro = raccolta_canonica()
    prima = costruisci_indice(registro.preventivi())
    registro.elimina("012")
    dopo = costruisci_indice(registro.preventivi())
    assert prima.inordine() == ["003", "007", "012"]  # la vecchia fotografia resta
    assert prima.cerca("012").totale_cent == 0
    assert dopo.inordine() == ["003", "007"]  # la nuova riflette l'eliminazione
    assert dopo.contiene("012") is False
    assert [p.codice for p in registro.preventivi()] == ["007", "003"]
    # Le interrogazioni non modificano né l'indice né la raccolta.
    prima.intervallo("001", "012")
    dopo.intervallo("001", "012")
    assert prima.inordine() == ["003", "007", "012"]
    assert [p.codice for p in registro.preventivi()] == ["007", "003"]
