"""Test pubblici del LAB-PY-U12: casi L01-L12 dell'archivio materiali.

La suite descrive **comportamenti attesi** e non dettagli dell'implementazione:
si accompagna allo starter durante le fasi e al termine della sessione. Con lo
starter incompleto è atteso un primo esito di fallimenti chiari - in genere
`NotImplementedError` che nomina la fase - e non un difetto della copia. Con il
riferimento formativo tutti i casi devono passare.

Esecuzione dalla root di `raccolta-programmi` (o dalla cartella del file):

    uv run --with pytest python -m pytest programmi/test_archivio_u12.py -q

I test creano ogni volta archivi di prova in una cartella temporanea e non
leggono le fixture d'ingresso: il file di ingresso della sessione non viene mai
modificato. Le simulazioni dei guasti sono intercettazioni deterministiche
dell'operazione di scrittura o di sostituzione: nessuna prova dipende dai
permessi della cartella.

I casi L01-L11 sono qui rappresentati; L12 è il caso progettato dallo studente
e si aggiunge in coda a questa suite, con la motivazione di che cosa discrimina.
"""

import builtins
import importlib
from pathlib import Path

import cli_archivio_u12 as cli
import dominio_archivio_u12 as dominio
import persistenza_archivio_u12 as persistenza
import pytest

INTESTAZIONE = "codice,descrizione,quantita\n"

MATERIALE_A = {"codice": "007", "descrizione": "Vite, lunga", "quantita": 4}
MATERIALE_B = {"codice": "012", "descrizione": 'Caffè "A"', "quantita": 2}


def scrivi_archivio(percorso, testo, encoding="utf-8"):
    """Scrive l'archivio di prova con i byte voluti e restituisce il percorso."""
    percorso = Path(percorso)
    percorso.write_bytes(testo.encode(encoding))
    return percorso


# ---------------------------------------------------------------------------
# L01 - schema valido: conversione, validazione e tipi ricostruiti
# ---------------------------------------------------------------------------


def test_l01_riga_valida_diventa_record_con_intero():
    materiale = dominio.riga_a_materiale(["007", "Vite, lunga", "4"], "record 1")
    assert materiale == MATERIALE_A
    assert isinstance(materiale["quantita"], int)


def test_l01_validazione_passa_su_record_ammesso():
    assert dominio.valida_materiale(dict(MATERIALE_A)) is None


def test_l01_campi_mancanti_extra_o_tipi_errati_sono_rifiutati():
    with pytest.raises(ValueError, match="descrizione"):
        dominio.valida_materiale({"codice": "007", "quantita": 4})
    with pytest.raises(ValueError, match="non previsto"):
        dominio.valida_materiale({**MATERIALE_A, "prezzo": 1})
    with pytest.raises(ValueError, match="quantita"):
        dominio.valida_materiale({"codice": "007", "descrizione": "x", "quantita": True})


# ---------------------------------------------------------------------------
# L02 - raccolta vuota: solo intestazione e totali a zero
# ---------------------------------------------------------------------------


def test_l02_archivio_con_sola_intestazione_carica_lista_vuota(tmp_path):
    percorso = scrivi_archivio(tmp_path / "vuoto.csv", INTESTAZIONE)
    assert persistenza.carica_materiali(percorso) == []


def test_l02_riepilogo_della_raccolta_vuota_e_tutto_zero():
    assert dominio.riepilogo_archivio([]) == {"materiali": 0, "quantita_totale": 0}


def test_l02_salvataggio_della_raccolta_vuota_produce_solo_intestazione(tmp_path):
    percorso = tmp_path / "vuoto.csv"
    persistenza.salva_materiali(percorso, [])
    assert percorso.read_bytes() == INTESTAZIONE.encode("utf-8")


# ---------------------------------------------------------------------------
# L03 - codice con zeri: identità esatta, mai confronti numerici
# ---------------------------------------------------------------------------


def test_l03_zeri_iniziali_sono_conservati_e_007_diverso_da_7(tmp_path):
    testo = INTESTAZIONE + "007,Forbice,1\n7,Pinza,2\n"
    percorso = scrivi_archivio(tmp_path / "zeri.csv", testo)
    materiali = persistenza.carica_materiali(percorso)
    assert [m["codice"] for m in materiali] == ["007", "7"]
    assert dominio.cerca_materiale(materiali, "007") == 0
    assert dominio.cerca_materiale(materiali, "7") == 1
    assert dominio.cerca_materiale(materiali, "0007") is None


# ---------------------------------------------------------------------------
# L04 - quoting e accenti: il contenuto sopravvive al round-trip
# ---------------------------------------------------------------------------


def test_l04_virgole_virgolette_e_accenti_sono_preservati(tmp_path):
    percorso = tmp_path / "quoting.csv"
    persistenza.salva_materiali(percorso, [dict(MATERIALE_A), dict(MATERIALE_B)])
    materiali = persistenza.carica_materiali(percorso)
    assert materiali == [MATERIALE_A, MATERIALE_B]
    assert materiali[0]["descrizione"] == "Vite, lunga"
    assert materiali[1]["descrizione"] == 'Caffè "A"'


# ---------------------------------------------------------------------------
# L05 - duplicato: rifiuto totale, stato precedente invariato
# ---------------------------------------------------------------------------


def test_l05_inserimento_duplicato_e_rifiutato_senza_effetti():
    materiali = [dict(MATERIALE_A)]
    with pytest.raises(ValueError, match="già presente"):
        dominio.inserisci_materiale(materiali, {"codice": "007", "descrizione": "altro", "quantita": 9})
    assert materiali == [MATERIALE_A]


def test_l05_caricamento_con_codici_duplicati_non_pubblica_lista_parziale(tmp_path):
    testo = INTESTAZIONE + "007,Primo,1\n007,Secondo,2\n"
    percorso = scrivi_archivio(tmp_path / "duplicati.csv", testo)
    with pytest.raises(ValueError, match="già presente"):
        persistenza.carica_materiali(percorso)


# ---------------------------------------------------------------------------
# L06 - aggiornamento rifiutato: nessun aggiornamento parziale
# ---------------------------------------------------------------------------


def test_l06_modifica_valida_aggiorna_solo_i_campi_ammessi():
    materiali = [dict(MATERIALE_A)]
    assert dominio.modifica_materiale(materiali, "007", "Vite corta", 10) is True
    assert materiali == [{"codice": "007", "descrizione": "Vite corta", "quantita": 10}]


def test_l06_modifica_con_dato_invalido_lascia_il_record_invariato():
    materiali = [dict(MATERIALE_A)]
    with pytest.raises(ValueError, match="quantita"):
        dominio.modifica_materiale(materiali, "007", "Vite corta", -1)
    assert materiali == [MATERIALE_A]


def test_l06_modifica_di_codice_assente_restituisce_false():
    materiali = [dict(MATERIALE_A)]
    assert dominio.modifica_materiale(materiali, "999", "Fantasma", 1) is False
    assert materiali == [MATERIALE_A]


# ---------------------------------------------------------------------------
# L07 - ricerca indice 0: la posizione zero è un risultato valido
# ---------------------------------------------------------------------------


def test_l07_ricerca_del_primo_record_restituisce_indice_zero():
    materiali = [dict(MATERIALE_A), dict(MATERIALE_B)]
    assert dominio.cerca_materiale(materiali, "007") == 0
    assert dominio.cerca_materiale(materiali, "012") == 1
    assert dominio.cerca_materiale(materiali, "999") is None


def test_l07_elimina_distingue_assente_e_presente():
    materiali = [dict(MATERIALE_A), dict(MATERIALE_B)]
    assert dominio.elimina_materiale(materiali, "999") is False
    assert dominio.elimina_materiale(materiali, "007") is True
    assert materiali == [MATERIALE_B]


# ---------------------------------------------------------------------------
# L08 - caricamento invalido: diagnosi e nessun risultato parziale
# ---------------------------------------------------------------------------


def test_l08_intestazione_con_colonna_mancante_e_diagnosticata(tmp_path):
    percorso = scrivi_archivio(tmp_path / "mancante.csv", "codice,descrizione\n007,Vite,1\n")
    with pytest.raises(ValueError, match="mancante"):
        persistenza.carica_materiali(percorso)


def test_l08_intestazione_con_colonna_extra_o_nome_duplicato(tmp_path):
    extra = scrivi_archivio(tmp_path / "extra.csv", "codice,descrizione,quantita,prezzo\n007,Vite,1,2\n")
    with pytest.raises(ValueError, match="non prevista"):
        persistenza.carica_materiali(extra)
    duplicata = scrivi_archivio(
        tmp_path / "duplicata.csv", "codice,descrizione,descrizione\n007,Vite,1\n"
    )
    with pytest.raises(ValueError, match="duplicati"):
        persistenza.carica_materiali(duplicata)


def test_l08_record_non_convertibile_riporta_campo_e_riferimento(tmp_path):
    percorso = scrivi_archivio(tmp_path / "nonnum.csv", INTESTAZIONE + "007,Vite,tre\n")
    with pytest.raises(ValueError, match="quantita"):
        persistenza.carica_materiali(percorso)
    with pytest.raises(ValueError, match="record 1"):
        persistenza.carica_materiali(percorso)


def test_l08_percorso_assente_e_byte_incompatibili_hanno_diagnosi_distinte(tmp_path):
    with pytest.raises(FileNotFoundError):
        persistenza.carica_materiali(tmp_path / "assente.csv")
    binario = tmp_path / "binario.csv"
    binario.write_bytes(b"codice,descrizione,quantita\n\x00\x01\xff\n")
    with pytest.raises(UnicodeDecodeError):
        persistenza.carica_materiali(binario)


def test_l08_bom_dingresso_e_accettato_e_la_prima_intestazione_resta_corretta(tmp_path):
    percorso = scrivi_archivio(tmp_path / "con_bom.csv", INTESTAZIONE + "007,Vite,1\n", encoding="utf-8-sig")
    materiali = persistenza.carica_materiali(percorso)
    assert materiali == [{"codice": "007", "descrizione": "Vite", "quantita": 1}]


# ---------------------------------------------------------------------------
# L09 - round-trip: stessi dati, stessi tipi, nessun BOM in uscita
# ---------------------------------------------------------------------------


def test_l09_round_trip_byte_identico_e_senza_bom(tmp_path):
    percorso = tmp_path / "archivio.csv"
    materiali = [dict(MATERIALE_A), dict(MATERIALE_B)]
    persistenza.salva_materiali(percorso, materiali)
    byte = percorso.read_bytes()
    assert not byte.startswith(b"\xef\xbb\xbf")
    assert b"\r\n" not in byte
    assert persistenza.carica_materiali(percorso) == materiali


def test_l09_riga_a_materiale_e_materiale_a_riga_sono_inversi():
    riga = ["012", 'Caffè "A"', "2"]
    assert dominio.materiale_a_riga(dominio.riga_a_materiale(riga, "record 1")) == riga


# ---------------------------------------------------------------------------
# L10 - guasto senza perdita della destinazione
# ---------------------------------------------------------------------------


def test_l10_guasto_durante_la_scrittura_preserva_la_destinazione(tmp_path, monkeypatch):
    percorso = tmp_path / "archivio.csv"
    persistenza.salva_materiali(percorso, [dict(MATERIALE_A)])
    prima = percorso.read_bytes()

    originale = persistenza.materiale_a_riga
    chiamate = {"n": 0}

    def guasto(materiale):
        chiamate["n"] += 1
        if chiamate["n"] >= 2:
            raise OSError("guasto simulato durante la scrittura")
        return originale(materiale)

    monkeypatch.setattr(persistenza, "materiale_a_riga", guasto)
    with pytest.raises(OSError, match="guasto simulato"):
        persistenza.salva_materiali(percorso, [dict(MATERIALE_A), dict(MATERIALE_B)])
    assert percorso.read_bytes() == prima
    assert list(tmp_path.glob("*.tmp")) == []


def test_l10_guasto_alla_sostituzione_preserva_la_destinazione(tmp_path, monkeypatch):
    percorso = tmp_path / "archivio.csv"
    persistenza.salva_materiali(percorso, [dict(MATERIALE_A)])
    prima = percorso.read_bytes()

    def guasto(self, target):
        raise OSError("guasto simulato alla sostituzione")

    monkeypatch.setattr(Path, "replace", guasto)
    with pytest.raises(OSError, match="sostituzione"):
        persistenza.salva_materiali(percorso, [dict(MATERIALE_B)])
    assert percorso.read_bytes() == prima
    monkeypatch.undo()
    assert list(tmp_path.glob("*.tmp")) == []


# ---------------------------------------------------------------------------
# L11 - import non interattivo
# ---------------------------------------------------------------------------


def test_l11_import_dei_tre_moduli_non_pone_domande(monkeypatch):
    def nessuna_domanda(*args, **kwargs):
        raise AssertionError("l'import non deve chiedere input")

    monkeypatch.setattr(builtins, "input", nessuna_domanda)
    for modulo in (dominio, persistenza, cli):
        importlib.reload(modulo)


# ---------------------------------------------------------------------------
# Comportamenti della CLI (sessione, flag e recupero)
# ---------------------------------------------------------------------------


def test_cli_uso_senza_argomenti_restituisce_codice_2(capsys):
    assert cli.main(["cli_archivio_u12.py"]) == 2
    assert "uso:" in capsys.readouterr().out


def test_cli_comando_sconosciuto_non_modifica_lo_stato(tmp_path, monkeypatch, capsys):
    percorso = tmp_path / "archivio.csv"
    persistenza.salva_materiali(percorso, [dict(MATERIALE_A)])
    risposte = iter(["9", "0"])
    monkeypatch.setattr(builtins, "input", lambda messaggio: next(risposte))
    assert cli.main(["cli_archivio_u12.py", str(percorso)]) == 0
    uscita = capsys.readouterr().out
    assert "comando sconosciuto" in uscita
    assert percorso.read_bytes() == (INTESTAZIONE + "007,\"Vite, lunga\",4\n").encode("utf-8")


def test_cli_ricerca_in_posizione_zero_e_assente_distinte(tmp_path, monkeypatch, capsys):
    percorso = tmp_path / "archivio.csv"
    persistenza.salva_materiali(percorso, [dict(MATERIALE_A), dict(MATERIALE_B)])
    risposte = iter(["2", "007", "2", "999", "0"])
    monkeypatch.setattr(builtins, "input", lambda messaggio: next(risposte))
    assert cli.main(["cli_archivio_u12.py", str(percorso)]) == 0
    uscita = capsys.readouterr().out
    assert "in posizione 0" in uscita
    assert "assente" in uscita


def test_cli_aggiornamento_rifiutato_lascia_dati_e_flag_invariati(tmp_path, monkeypatch, capsys):
    percorso = tmp_path / "archivio.csv"
    persistenza.salva_materiali(percorso, [dict(MATERIALE_A)])
    prima = percorso.read_bytes()
    risposte = iter(["4", "007", "Vite corta", "-1", "0"])
    monkeypatch.setattr(builtins, "input", lambda messaggio: next(risposte))
    assert cli.main(["cli_archivio_u12.py", str(percorso)]) == 0
    assert "aggiornamento rifiutato" in capsys.readouterr().out
    assert percorso.read_bytes() == prima


def test_cli_eliminazione_annullata_non_elimina(tmp_path, monkeypatch):
    percorso = tmp_path / "archivio.csv"
    persistenza.salva_materiali(percorso, [dict(MATERIALE_A), dict(MATERIALE_B)])
    risposte = iter(["5", "007", "n", "0"])
    monkeypatch.setattr(builtins, "input", lambda messaggio: next(risposte))
    assert cli.main(["cli_archivio_u12.py", str(percorso)]) == 0
    assert persistenza.carica_materiali(percorso) == [MATERIALE_A, MATERIALE_B]


def test_cli_salvataggio_fallito_non_dichiara_successo(tmp_path, monkeypatch, capsys):
    percorso = tmp_path / "archivio.csv"
    persistenza.salva_materiali(percorso, [dict(MATERIALE_A)])
    originale = cli.salva_materiali
    chiamate = {"n": 0}

    def guasto_poi_regolare(percorso, materiali):
        chiamate["n"] += 1
        if chiamate["n"] == 1:
            raise OSError("guasto simulato")
        return originale(percorso, materiali)

    monkeypatch.setattr(cli, "salva_materiali", guasto_poi_regolare)
    risposte = iter(["3", "020", "Guanto", "3", "6", "0"])
    monkeypatch.setattr(builtins, "input", lambda messaggio: next(risposte))
    assert cli.main(["cli_archivio_u12.py", str(percorso)]) == 0
    uscita = capsys.readouterr().out
    assert "salvataggio non riuscito" in uscita
    assert "dati e modifiche pendenti restano in memoria" in uscita
    # Il successo è dichiarato solo dal secondo salvataggio, andato a buon fine.
    assert uscita.index("salvataggio non riuscito") < uscita.index("archivio salvato")


def test_cli_uscita_con_salvataggio_fallito_resta_al_menu(tmp_path, monkeypatch, capsys):
    percorso = tmp_path / "archivio.csv"
    persistenza.salva_materiali(percorso, [dict(MATERIALE_A)])
    originale = cli.salva_materiali
    chiamate = {"n": 0}

    def guasto_poi_regolare(percorso, materiali):
        chiamate["n"] += 1
        if chiamate["n"] == 1:
            raise OSError("guasto simulato")
        return originale(percorso, materiali)

    monkeypatch.setattr(cli, "salva_materiali", guasto_poi_regolare)
    risposte = iter(["3", "020", "Guanto", "3", "0", "6", "0"])
    monkeypatch.setattr(builtins, "input", lambda messaggio: next(risposte))
    assert cli.main(["cli_archivio_u12.py", str(percorso)]) == 0
    uscita = capsys.readouterr().out
    assert "si resta nel menu con i dati ancora in memoria" in uscita
    assert persistenza.carica_materiali(percorso) == [
        dict(MATERIALE_A),
        {"codice": "020", "descrizione": "Guanto", "quantita": 3},
    ]


def test_cli_eof_con_modifiche_pendenti_avvisa_e_non_scrive(tmp_path, monkeypatch, capsys):
    percorso = tmp_path / "archivio.csv"
    persistenza.salva_materiali(percorso, [dict(MATERIALE_A)])
    prima = percorso.read_bytes()
    risposte = iter(["3", "020", "Guanto", "3"])

    def domanda(messaggio):
        try:
            return next(risposte)
        except StopIteration:
            raise EOFError from None

    monkeypatch.setattr(builtins, "input", domanda)
    assert cli.main(["cli_archivio_u12.py", str(percorso)]) == 1
    uscita = capsys.readouterr().out
    assert "sessione interrotta" in uscita
    assert "modifiche non salvate" in uscita
    assert percorso.read_bytes() == prima


def test_cli_primo_avvio_con_archivio_assente_parte_vuoto(tmp_path, monkeypatch, capsys):
    percorso = tmp_path / "assente.csv"
    risposte = iter(["1", "0"])
    monkeypatch.setattr(builtins, "input", lambda messaggio: next(risposte))
    assert cli.main(["cli_archivio_u12.py", str(percorso)]) == 0
    assert "archivio assente" in capsys.readouterr().out
    assert not percorso.exists()


@pytest.mark.parametrize("modifiche_pendenti", [False, True])
@pytest.mark.parametrize(
    "risposte_parziali",
    [
        ["2"],
        ["3"],
        ["3", "020"],
        ["3", "020", "Guanto"],
        ["4"],
        ["4", "007"],
        ["4", "007", "Descrizione nuova"],
        ["5"],
        ["5", "007"],
    ],
)
def test_cli_eof_in_ogni_domanda_interrompe_senza_scrivere(
    tmp_path, monkeypatch, capsys, risposte_parziali, modifiche_pendenti
):
    """L'EOF può arrivare in ogni campo, non soltanto alla scelta del menu."""
    percorso = tmp_path / "archivio.csv"
    persistenza.salva_materiali(percorso, [dict(MATERIALE_A)])
    prima = percorso.read_bytes()
    prefisso = ["3", "030", "Materiale nuovo", "1"] if modifiche_pendenti else []
    risposte = iter(prefisso + risposte_parziali)

    def domanda(messaggio):
        try:
            return next(risposte)
        except StopIteration:
            raise EOFError from None

    monkeypatch.setattr(builtins, "input", domanda)
    assert cli.main(["cli_archivio_u12.py", str(percorso)]) == 1
    uscita = capsys.readouterr().out
    assert "sessione interrotta: fine dell'input" in uscita
    assert ("modifiche non salvate" in uscita) is modifiche_pendenti
    assert "archivio salvato" not in uscita
    assert percorso.read_bytes() == prima


def test_cli_archivio_non_valido_arresta_senza_menu(tmp_path, capsys):
    percorso = scrivi_archivio(tmp_path / "corrotto.csv", "codice,descrizione\n007,Vite,1\n")
    assert cli.main(["cli_archivio_u12.py", str(percorso)]) == 1
    uscita = capsys.readouterr().out
    assert "archivio non valido" in uscita
    assert "scelta>" not in uscita
