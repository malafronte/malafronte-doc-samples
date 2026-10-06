"""Prove del magazzino a oggetti: casi MAGO-01…MAGO-12.

Le prove derivano gli attesi dal contratto U12 conservato e dalla differenza
di aliasing dichiarata per la variante a oggetti. I guasti di scrittura sono
simulati con meccanismi **deterministici** di monkeypatching: nessuna prova
dipende da permessi di cartella o da input casuali.
"""

import builtins
import csv

import cli_magazzino_u13 as cli
import persistenza_magazzino_u13 as persistenza
import pytest
from articolo_u13 import Articolo
from conversioni_json_u13 import articoli_a_dati, articoli_a_testo, testo_a_articoli
from dominio_magazzino_u13 import (
    articolo_a_riga,
    cerca_articolo,
    elimina_articolo,
    inserisci_articolo,
    modifica_articolo,
    riepilogo_magazzino,
    riga_a_articolo,
)
from persistenza_magazzino_u13 import carica_articoli, salva_articoli

CANONICI = (
    ("007", "Vite, lunga", 4, 25),
    ("012", 'Caffè "A"', 2, 350),
)


def articoli_canonici():
    """Restituisce la lista canonica di due istanze valide."""
    return [Articolo(*c) for c in CANONICI]


def scrivi_canonico(percorso, bom=False):
    """Scrive l'archivio canonico in CSV, con o senza BOM iniziale."""
    testo = "codice,descrizione,quantita,prezzo_centesimi\n"
    testo += '007,"Vite, lunga",4,25\n'
    testo += '012,"Caffè ""A""",2,350\n'
    dati = testo.encode("utf-8")
    if bom:
        dati = b"\xef\xbb\xbf" + dati
    percorso.write_bytes(dati)
    return percorso


# --- MAGO-01 --------------------------------------------------------------


def test_mago_01_caricamento_canonico(tmp_path):
    """MAGO-01: lista di istanze valide, 2 articoli, 6 unità, 800 centesimi."""
    percorso = scrivi_canonico(tmp_path / "magazzino.csv")
    articoli = carica_articoli(percorso)
    assert len(articoli) == 2
    assert all(isinstance(a, Articolo) for a in articoli)
    assert [a.dati() for a in articoli] == [
        {"codice": "007", "descrizione": "Vite, lunga", "quantita": 4, "prezzo_centesimi": 25},
        {"codice": "012", "descrizione": 'Caffè "A"', "quantita": 2, "prezzo_centesimi": 350},
    ]
    assert riepilogo_magazzino(articoli) == {
        "articoli": 2,
        "quantita_totale": 6,
        "valore_centesimi": 800,
    }


# --- MAGO-02 --------------------------------------------------------------


def test_mago_02_ricerca():
    """MAGO-02: indice 0 valido, assente `None`, confronto esatto."""
    articoli = articoli_canonici()
    assert cerca_articolo(articoli, "007") == 0
    assert cerca_articolo(articoli, "012") == 1
    assert cerca_articolo(articoli, "999") is None
    assert cerca_articolo(articoli, "7") is None
    assert cerca_articolo(articoli, "007 ") is None


# --- MAGO-03 --------------------------------------------------------------


def test_mago_03_inserimento_ordinario():
    """MAGO-03: inserimento unico e indipendente dall'argomento."""
    articoli = articoli_canonici()
    candidato = Articolo("020", "Dado", 1, 10)
    assert inserisci_articolo(articoli, candidato) is None
    assert len(articoli) == 3
    assert articoli[2] is not candidato
    assert articoli[2].dati() == candidato.dati()
    candidato.aggiorna("Dado M5", 9, 90)
    assert articoli[2].dati()["descrizione"] == "Dado"


def test_mago_03_duplicato_rifiutato():
    """MAGO-03: il duplicato solleva ValueError e la lista resta invariata."""
    articoli = articoli_canonici()
    with pytest.raises(ValueError, match="già presente"):
        inserisci_articolo(articoli, Articolo("007", "doppione", 1, 1))
    assert len(articoli) == 2
    assert articoli[0].dati()["descrizione"] == "Vite, lunga"


# --- MAGO-04 --------------------------------------------------------------


def test_mago_04_modifica_valida():
    """MAGO-04: aggiornamento valido restituisce True e muta l'istanza."""
    articoli = articoli_canonici()
    assert modifica_articolo(articoli, "007", "Vite, corta", 6, 30) is True
    assert articoli[0].dati() == {
        "codice": "007",
        "descrizione": "Vite, corta",
        "quantita": 6,
        "prezzo_centesimi": 30,
    }


def test_mago_04_modifica_invalida():
    """MAGO-04: dato invalido, nessuna modifica parziale."""
    articoli = articoli_canonici()
    with pytest.raises(ValueError):
        modifica_articolo(articoli, "007", "Vite, corta", -1, 30)
    assert articoli[0].dati()["descrizione"] == "Vite, lunga"
    assert articoli[0].dati()["quantita"] == 4


def test_mago_04_modifica_assente():
    """MAGO-04: codice assente, nessuna modifica e risultato False."""
    articoli = articoli_canonici()
    assert modifica_articolo(articoli, "999", "inesistente", 1, 1) is False
    assert len(articoli) == 2


# --- MAGO-05 --------------------------------------------------------------


def test_mago_05_eliminazione():
    """MAGO-05: assente False, presente True e lista accorciata."""
    articoli = articoli_canonici()
    assert elimina_articolo(articoli, "999") is False
    assert elimina_articolo(articoli, "007") is True
    assert len(articoli) == 1
    assert cerca_articolo(articoli, "007") is None


def test_mago_05_nessuna_conferma_nel_dominio(monkeypatch):
    """MAGO-05: la funzione di dominio non interroga l'utente."""
    articoli = articoli_canonici()

    def nessun_input(_prompt=""):
        raise AssertionError("la funzione di dominio non deve chiedere conferma")

    monkeypatch.setattr(builtins, "input", nessun_input)
    assert elimina_articolo(articoli, "007") is True


def test_mago_05_conferma_nella_cli(tmp_path, monkeypatch, capsys):
    """MAGO-05: la CLI gestisce la conferma, con esiti diversi per s e n."""
    percorso = scrivi_canonico(tmp_path / "magazzino.csv")
    risposte = iter(["5", "007", "n", "5", "007", "s", "1", "0"])
    monkeypatch.setattr(builtins, "input", lambda _prompt="": next(risposte))
    assert cli.main([str(percorso)]) == 0
    uscita = capsys.readouterr().out
    assert "eliminazione annullata" in uscita
    assert "articolo '007' eliminato" in uscita


# --- MAGO-06 --------------------------------------------------------------


def test_mago_06_round_trip_csv(tmp_path):
    """MAGO-06: virgole, virgolette, accenti e zero preservati; output senza BOM."""
    articoli = [
        Articolo("007", "Vite, lunga", 4, 25),
        Articolo("012", 'Caffè "A"', 2, 350),
        Articolo("020", "Àncora", 0, 10),
    ]
    percorso = tmp_path / "magazzino.csv"
    salva_articoli(percorso, articoli)
    byte = percorso.read_bytes()
    assert not byte.startswith(b"\xef\xbb\xbf")
    assert b"\r\n" not in byte
    testo = byte.decode("utf-8")
    # Nel CSV le virgolette interne al campo sono raddoppiate: il dato
    # effettivo resta `Caffè "A"`, come verificato dal round-trip qui sotto.
    assert "Caffè" in testo
    assert '""A""' in testo
    ricaricati = carica_articoli(percorso)
    assert [a.dati() for a in ricaricati] == [a.dati() for a in articoli]
    assert all(isinstance(a.dati()["quantita"], int) for a in ricaricati)
    assert all(ricaricati[i] is not articoli[i] for i in range(3))


def test_mago_06_zero_significativo(tmp_path):
    """MAGO-06: quantità zero e zeri iniziali dei codici sopravvivono al round-trip."""
    articoli = [Articolo("007", "Vite", 0, 0)]
    percorso = tmp_path / "magazzino.csv"
    salva_articoli(percorso, articoli)
    ricaricati = carica_articoli(percorso)
    assert ricaricati[0].dati() == {
        "codice": "007",
        "descrizione": "Vite",
        "quantita": 0,
        "prezzo_centesimi": 0,
    }


# --- MAGO-07 --------------------------------------------------------------


def test_mago_07_bom_accettato(tmp_path):
    """MAGO-07: il caricamento accetta UTF-8 con BOM."""
    percorso = scrivi_canonico(tmp_path / "con_bom.csv", bom=True)
    assert len(carica_articoli(percorso)) == 2


def test_mago_07_righe_vuote_ignorate(tmp_path):
    """MAGO-07: le righe fisiche vuote non sono record."""
    percorso = tmp_path / "magazzino.csv"
    percorso.write_text(
        "codice,descrizione,quantita,prezzo_centesimi\n"
        '007,"Vite, lunga",4,25\n'
        "\n"
        '012,"Caffè ""A""",2,350\n',
        encoding="utf-8",
    )
    assert len(carica_articoli(percorso)) == 2


def test_mago_07_record_su_piu_righe(tmp_path):
    """MAGO-07: un campo fra virgolette può contenere un a capo."""
    percorso = tmp_path / "magazzino.csv"
    # write_bytes: il terminatore di riga deve essere esattamente \n, senza
    # la traduzione del modo testo su Windows.
    percorso.write_bytes(
        (
            "codice,descrizione,quantita,prezzo_centesimi\n"
            '007,"Vite,\nlunga",4,25\n'
            '012,"Caffè ""A""",2,350\n'
        ).encode()
    )
    articoli = carica_articoli(percorso)
    assert articoli[0].dati()["descrizione"] == "Vite,\nlunga"
    assert riepilogo_magazzino(articoli)["articoli"] == 2


# --- MAGO-08 --------------------------------------------------------------


@pytest.mark.parametrize(
    "contenuto",
    [
        "codice,descrizione,quantita\n007,Vite,4\n",
        "descrizione,codice,quantita,prezzo_centesimi\nVite,007,4,25\n",
        "codice,codice,quantita,prezzo_centesimi\n007,007,4,25\n",
        "codice,descrizione,quantita,prezzo_centesimi,extra\n007,Vite,4,25,x\n",
    ],
)
def test_mago_08_intestazione_invalida(tmp_path, contenuto):
    """MAGO-08: intestazione errata, con diagnosi sul colpevole."""
    percorso = tmp_path / "magazzino.csv"
    percorso.write_text(contenuto, encoding="utf-8")
    with pytest.raises(ValueError):
        carica_articoli(percorso)


def test_mago_08_quoting_malformato(tmp_path):
    """MAGO-08: un campo non chiuso produce `csv.Error`."""
    percorso = tmp_path / "magazzino.csv"
    percorso.write_text(
        "codice,descrizione,quantita,prezzo_centesimi\n007,\"Vite,4,25\n",
        encoding="utf-8",
    )
    with pytest.raises(csv.Error):
        carica_articoli(percorso)


def test_mago_08_nessuna_lista_paziale(tmp_path):
    """MAGO-08: un record invalido in fondo non consegna i record precedenti."""
    percorso = tmp_path / "magazzino.csv"
    percorso.write_text(
        "codice,descrizione,quantita,prezzo_centesimi\n"
        '007,"Vite, lunga",4,25\n'
        '012,"Caffè",due,350\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="non è un intero"):
        carica_articoli(percorso)


def test_mago_08_duplicato_nel_file(tmp_path):
    """MAGO-08: due record con lo stesso codice fanno fallire il caricamento."""
    percorso = tmp_path / "magazzino.csv"
    percorso.write_text(
        "codice,descrizione,quantita,prezzo_centesimi\n"
        "007,Vite,4,25\n"
        "007,Dado,1,10\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="già presente"):
        carica_articoli(percorso)


# --- MAGO-09 --------------------------------------------------------------


def test_mago_09_file_assente(tmp_path):
    """MAGO-09: il file assente è `FileNotFoundError`, non un archivio vuoto."""
    with pytest.raises(FileNotFoundError):
        carica_articoli(tmp_path / "inesistente.csv")


def test_mago_09_file_corrotto(tmp_path):
    """MAGO-09: byte non UTF-8 producono `UnicodeDecodeError`, non un magazzino vuoto."""
    percorso = tmp_path / "corrotto.csv"
    percorso.write_bytes(b"codice,descrizione,quantita,prezzo_centesimi\n\xff\xfe\n")
    with pytest.raises(UnicodeDecodeError):
        carica_articoli(percorso)


def test_mago_09_cli_distingue_i_due_casi(tmp_path, monkeypatch, capsys):
    """MAGO-09: avvio con file assente e con file corrotto danno esiti diversi."""
    monkeypatch.setattr(builtins, "input", lambda _prompt="": "0")
    assert cli.main([str(tmp_path / "inesistente.csv")]) == 0
    assert "archivio assente" in capsys.readouterr().out
    percorso = tmp_path / "corrotto.csv"
    percorso.write_bytes(b"\xff\xfe")
    assert cli.main([str(percorso)]) == 1
    assert "non leggibile come UTF-8" in capsys.readouterr().out


# --- MAGO-10 --------------------------------------------------------------


def test_mago_10_guasto_all_apertura_del_temporaneo(tmp_path, monkeypatch):
    """MAGO-10: guasto prima della scrittura, destinazione invariata."""
    percorso = scrivi_canonico(tmp_path / "magazzino.csv")
    byte_prima = percorso.read_bytes()
    articoli = carica_articoli(percorso)

    def guasto(*_args, **_kwargs):
        raise OSError("guasto simulato all'apertura")

    monkeypatch.setattr(persistenza.tempfile, "NamedTemporaryFile", guasto)
    with pytest.raises(OSError, match="guasto simulato"):
        salva_articoli(percorso, articoli)
    assert percorso.read_bytes() == byte_prima


def test_mago_10_guasto_durante_la_scrittura(tmp_path, monkeypatch):
    """MAGO-10: guasto in scrittura, temporaneo rimosso e destinazione invariata."""
    percorso = scrivi_canonico(tmp_path / "magazzino.csv")
    byte_prima = percorso.read_bytes()
    articoli = carica_articoli(percorso)

    def guasto(*_args, **_kwargs):
        raise OSError("guasto simulato in scrittura")

    monkeypatch.setattr(persistenza.csv, "writer", guasto)
    with pytest.raises(OSError, match="guasto simulato"):
        salva_articoli(percorso, articoli)
    assert percorso.read_bytes() == byte_prima
    assert list(tmp_path.glob("*.tmp")) == []


def test_mago_10_guasto_alla_sostituzione(tmp_path, monkeypatch):
    """MAGO-10: guasto alla sostituzione, nessun successo falso."""
    percorso = scrivi_canonico(tmp_path / "magazzino.csv")
    byte_prima = percorso.read_bytes()
    articoli = carica_articoli(percorso)

    def guasto(_self, _destinazione):
        raise OSError("guasto simulato in sostituzione")

    monkeypatch.setattr(persistenza.Path, "replace", guasto)
    with pytest.raises(OSError, match="guasto simulato"):
        salva_articoli(percorso, articoli)
    assert percorso.read_bytes() == byte_prima
    assert list(tmp_path.glob("*.tmp")) == []


def test_mago_10_dati_e_flag_conservati(tmp_path, monkeypatch, capsys):
    """MAGO-10: un salvataggio fallito lascia le modifiche in memoria."""
    percorso = scrivi_canonico(tmp_path / "magazzino.csv")
    risposte = iter(["3", "020", "Dado", "1", "10", "6", "0"])

    def con_eof(_prompt=""):
        try:
            return next(risposte)
        except StopIteration:
            raise EOFError from None

    monkeypatch.setattr(builtins, "input", con_eof)

    def guasto(*_args, **_kwargs):
        raise OSError("guasto simulato in scrittura")

    monkeypatch.setattr(persistenza.csv, "writer", guasto)
    assert cli.main([str(percorso)]) == 1
    uscita = capsys.readouterr().out
    assert "salvataggio non riuscito" in uscita
    assert "le modifiche restano in memoria" in uscita
    assert "si resta nel menu con le modifiche in memoria" in uscita
    assert "attenzione: restano modifiche non salvate in memoria" in uscita


# --- MAGO-11 --------------------------------------------------------------


def test_mago_11_salvataggio_esplicito_e_riavvio(tmp_path, monkeypatch, capsys):
    """MAGO-11: la voce 6 salva e resta, la voce 0 termina senza riscrivere."""
    percorso = scrivi_canonico(tmp_path / "magazzino.csv")
    risposte = iter(["3", "020", "Dado", "1", "10", "6", "0"])
    monkeypatch.setattr(builtins, "input", lambda _prompt="": next(risposte))
    assert cli.main([str(percorso)]) == 0
    uscita = capsys.readouterr().out
    assert "archivio salvato" in uscita
    assert "chiusura senza modifiche pendenti" in uscita
    ricaricati = carica_articoli(percorso)
    assert len(ricaricati) == 3


def test_mago_11_uscita_con_modifiche_salva(tmp_path, monkeypatch, capsys):
    """MAGO-11: la voce 0 salva le modifiche pendenti e termina."""
    percorso = scrivi_canonico(tmp_path / "magazzino.csv")
    risposte = iter(["5", "007", "s", "0"])
    monkeypatch.setattr(builtins, "input", lambda _prompt="": next(risposte))
    assert cli.main([str(percorso)]) == 0
    assert "archivio salvato" in capsys.readouterr().out
    assert len(carica_articoli(percorso)) == 1


def test_mago_11_uscita_senza_modifiche(tmp_path, monkeypatch, capsys):
    """MAGO-11: senza modifiche la chiusura non riscrive il file."""
    percorso = scrivi_canonico(tmp_path / "magazzino.csv")
    byte_prima = percorso.read_bytes()
    risposte = iter(["0"])
    monkeypatch.setattr(builtins, "input", lambda _prompt="": next(risposte))
    assert cli.main([str(percorso)]) == 0
    assert "chiusura senza modifiche pendenti" in capsys.readouterr().out
    assert percorso.read_bytes() == byte_prima


def test_mago_11_nessuna_scrittura_implicita_a_fine_input(tmp_path, monkeypatch, capsys):
    """MAGO-11: l'EOF termina senza scrittura e avvisa delle modifiche pendenti."""
    percorso = scrivi_canonico(tmp_path / "magazzino.csv")
    byte_prima = percorso.read_bytes()
    risposte = iter(["3", "020", "Dado", "1", "10"])

    def con_eof(_prompt=""):
        try:
            return next(risposte)
        except StopIteration:
            raise EOFError from None

    monkeypatch.setattr(builtins, "input", con_eof)
    assert cli.main([str(percorso)]) == 1
    uscita = capsys.readouterr().out
    assert "sessione interrotta" in uscita
    assert "attenzione: restano modifiche non salvate in memoria" in uscita
    assert percorso.read_bytes() == byte_prima


# --- MAGO-12 --------------------------------------------------------------


def test_mago_12_proiezione_json_e_ricostruzione():
    """MAGO-12: schema e tipi validati, dati equivalenti, istanze nuove."""
    originali = articoli_canonici()
    testo = articoli_a_testo(originali)
    ricostruiti = testo_a_articoli(testo)
    assert [a.dati() for a in ricostruiti] == [a.dati() for a in originali]
    assert ricostruiti[0] is not originali[0]
    assert articoli_a_dati(originali)["versione_schema"] == 1


def test_mago_12_dati_invalidi_rifiutati():
    """MAGO-12: nessuna serializzazione implicita della classe e nessuna coercizione."""
    with pytest.raises(ValueError, match="atteso un intero"):
        testo_a_articoli(
            '{"versione_schema": 1, "articoli": '
            '[{"codice": "007", "descrizione": "Vite", "quantita": true, '
            '"prezzo_centesimi": 25}]}'
        )
    with pytest.raises(ValueError, match="versione_schema"):
        testo_a_articoli('{"versione_schema": 9, "articoli": []}')


# --- Conversioni di riga --------------------------------------------------


def test_conversioni_di_riga():
    """Le conversioni testuali preservano l'ordine dello schema e le diagnosi."""
    articolo = Articolo(*CANONICI[0])
    assert articolo_a_riga(articolo) == ["007", "Vite, lunga", "4", "25"]
    ricostruito = riga_a_articolo(["007", "Vite, lunga", "4", "25"], "record 1")
    assert ricostruito.dati() == articolo.dati()
    with pytest.raises(ValueError, match="attesi 4 campi"):
        riga_a_articolo(["007", "Vite"], "record 1")
    with pytest.raises(ValueError, match="record 1"):
        riga_a_articolo(["007", "Vite", "quattro", "25"], "record 1")
