"""Suite di verifica dei sorgenti d'esempio dell'Unità 12 (moduli, byte, eccezioni, date, testo).

I test controllano gli attesi dichiarati nei capitoli PY-16, PY-17, PY-18 e
PY-19 e le proprietà dei moduli `utilita_u12`, `demo_import_u12`,
`codifiche_u12`, `eccezioni_date_u12`, `analisi_testo_u12`,
`percorsi_testo_u12` e `cli_testo_u12`: valore dell'inventario, assenza di
effetti all'import, conti separati di codepoint e byte, comportamento del BOM
con i due codec, controlli separati di conversione e dominio, `else`/`finally`,
date con riferimenti fissi, fixture di testo e immagini nella cartella `dati/`,
conteggio delle parole e classifiche con parità alfabetica, righe, EOF,
terminatori, modalità di apertura e diagnosi delle aperture.

Esecuzione dalla cartella `unita-12/`:

    uv run --python 3.14 --with pytest python -m pytest esempi/test_esempi_u12.py -q

La suite è deterministica: usa dati espliciti e riferimenti di data fissi,
mai `date.today()` né durate reali. I test che scrivono file usano la cartella
isolata `tmp_path` oppure copie di lavoro: le fixture di `dati/` restano
invariate.
"""

import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from analisi_testo_u12 import analizza_file, conta_parole, ordina_frequenze
from cli_testo_u12 import main as cli_main
from cli_testo_u12 import righe_presentazione
from codifiche_u12 import BOM_UTF8, confronto_bytearray, decodifiche_con_firma, sommario_testo
from demo_import_u12 import genera_inventario, presentazione_riga, presentazione_tabella
from eccezioni_date_u12 import (
    compleanno_anno,
    data_da_formato,
    eta_anni,
    giorni_tra,
    prezzo_totale,
    prova_conversione,
    valida_quantita,
)
from percorsi_testo_u12 import (
    byte_iniziali,
    esperimento_modalita,
    leggi_con_iterazione,
    leggi_con_readline,
    leggi_con_readlines,
    prova_apertura,
    radici_di_lavoro,
    riepilogo_percorso,
)
from utilita_u12 import valore_magazzino

CARTELLA_ESEMPI = Path(__file__).resolve().parent
CARTELLA_UNITA = CARTELLA_ESEMPI.parent
DATI = CARTELLA_UNITA / "dati"

RECORD_CANONICI = [
    {"codice": "007", "descrizione": "Vite, lunga", "quantita": 4, "prezzo_centesimi": 25},
    {"codice": "012", "descrizione": 'Caffè "A"', "quantita": 2, "prezzo_centesimi": 350},
]


# ---------------------------------------------------------------------------
# Moduli e import (cap. PY-16)
# ---------------------------------------------------------------------------


def test_valore_magazzino_sul_dataset_canonico():
    assert valore_magazzino(RECORD_CANONICI) == 800


def test_valore_magazzino_sulla_lista_vuota_e_zero():
    assert valore_magazzino([]) == 0


def test_valore_magazzino_non_modifica_la_lista_ricevuta():
    articoli = [dict(record) for record in RECORD_CANONICI]
    prima = [dict(record) for record in articoli]
    valore_magazzino(articoli)
    assert articoli == prima


def test_valore_magazzino_con_un_solo_articolo_a_quantita_zero():
    assert valore_magazzino([{"quantita": 0, "prezzo_centesimi": 350}]) == 0


def test_inventario_riproducibile_con_lo_stesso_seme():
    assert genera_inventario(seed=7, numero=4) == genera_inventario(seed=7, numero=4)


def test_inventario_con_semi_diversi_puo_differire():
    assert genera_inventario(seed=7, numero=4) != genera_inventario(seed=8, numero=4)


def test_inventario_di_quattro_record_ha_i_campi_previsti():
    articoli = genera_inventario(seed=7, numero=4)
    assert len(articoli) == 4
    assert [articolo["codice"] for articolo in articoli] == ["001", "002", "003", "004"]
    for articolo in articoli:
        assert set(articolo) == {"codice", "descrizione", "quantita", "prezzo_centesimi"}
        assert isinstance(articolo["quantita"], int) and articolo["quantita"] >= 0
        assert isinstance(articolo["prezzo_centesimi"], int) and articolo["prezzo_centesimi"] > 0


def test_le_due_presentazioni_mostrano_lo_stesso_totale():
    articoli = genera_inventario(seed=7, numero=4)
    atteso = f"valore complessivo: {valore_magazzino(articoli)} centesimi"
    assert atteso in presentazione_riga(articoli)
    assert atteso in presentazione_tabella(articoli)


def test_presentazione_riga_ha_una_riga_per_articolo_piu_il_totale():
    righe = presentazione_riga(RECORD_CANONICI).splitlines()
    assert len(righe) == 3
    assert righe[0].startswith("007 Vite, lunga:")
    assert righe[2] == "valore complessivo: 800 centesimi"


def test_l_import_di_demo_import_non_produce_output():
    """L'import del modulo CLI non avvia domande né stampa nulla (processo separato)."""
    esito = subprocess.run(
        [sys.executable, "-c", "import demo_import_u12"],
        cwd=CARTELLA_ESEMPI,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert esito.returncode == 0
    assert esito.stdout == ""
    assert esito.stderr == ""


def test_l_esecuzione_diretta_avvia_il_menu_e_termina_con_zero():
    """Il processo che esegue il file mostra il menu e accetta lo 0 di uscita."""
    esito = subprocess.run(
        [sys.executable, "demo_import_u12.py"],
        cwd=CARTELLA_ESEMPI,
        input="0\n",
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert esito.returncode == 0
    assert "presentazione per riga" in esito.stdout
    assert "presentazione a tabella" in esito.stdout


# ---------------------------------------------------------------------------
# Byte, Unicode e BOM (cap. PY-17)
# ---------------------------------------------------------------------------


def test_accento_precomposto_un_punto_di_codice_e_due_byte():
    sommario = sommario_testo("è")
    assert sommario["punti_codice"] == 1
    assert sommario["punti"] == [0xE8]
    assert sommario["byte_utf8"] == b"\xc3\xa8"
    assert sommario["byte_hex"] == "C3 A8"


def test_accento_combinante_due_punti_di_codice_e_tre_byte():
    sommario = sommario_testo("e\u0300")
    assert sommario["punti_codice"] == 2
    assert sommario["punti"] == [0x65, 0x300]
    assert sommario["byte_utf8"] == b"\x65\xcc\x80"
    assert sommario["byte_hex"] == "65 CC 80"


def test_testo_vuoto_zero_punti_e_zero_byte():
    sommario = sommario_testo("")
    assert sommario["punti_codice"] == 0
    assert sommario["byte_utf8"] == b""
    assert sommario["byte_hex"] == ""


def test_precomposto_e_combinante_diversi_anche_se_simili_nella_resa():
    assert sommario_testo("è")["byte_utf8"] != sommario_testo("e\u0300")["byte_utf8"]
    assert len("è") != len("e\u0300")


def test_la_firma_utf8_sono_i_tre_byte_ef_bb_bf():
    assert BOM_UTF8 == b"\xef\xbb\xbf"
    assert sommario_testo("\ufeff")["byte_utf8"] == BOM_UTF8


def test_con_utf8_il_bom_iniziale_diventa_uffff():
    dati = BOM_UTF8 + "sole".encode("utf-8")
    esiti = decodifiche_con_firma(dati)
    assert esiti["utf8"] == "\ufeffsole"
    assert esiti["utf8_sig"] == "sole"


def test_utf8_sig_omette_la_sola_firma_iniziale():
    dati = "a\ufeffb".encode("utf-8")
    esiti = decodifiche_con_firma(dati)
    assert esiti["utf8"] == "a\ufeffb"
    assert esiti["utf8_sig"] == "a\ufeffb"


def test_utf8_sig_senza_firma_restuisce_il_testo_invariato():
    assert decodifiche_con_firma("sole".encode("utf-8")) == {"utf8": "sole", "utf8_sig": "sole"}


def test_bytes_immutabile_e_bytearray_modificabile():
    registro = confronto_bytearray()
    assert registro["bytes_originale"] == b"ABCD"
    assert registro["bytes_dopo"] == b"ABCD"
    assert "does not support item assignment" in registro["esito_assegnamento"]
    assert registro["bytearray_dopo"] == b"ZBCD"
    assert registro["tipo_finale"] == "bytearray"


# ---------------------------------------------------------------------------
# Eccezioni e diagnosi (cap. PY-18)
# ---------------------------------------------------------------------------


def test_valida_quantita_zero_e_un_dato_valido():
    assert valida_quantita("0") == 0
    assert valida_quantita("42") == 42


def test_valida_quantita_formato_non_convertibile():
    with pytest.raises(ValueError) as raccolta:
        valida_quantita("tre")
    assert "negativa" not in str(raccolta.value)


def test_valida_quantita_dominio_negativo_diagnosticato_a_parte():
    with pytest.raises(ValueError, match="negativa"):
        valida_quantita("-2")


def test_valida_quantita_reale_non_e_un_intero():
    with pytest.raises(ValueError):
        valida_quantita("3.5")


def test_valida_quantita_con_argomento_non_testo_e_un_uso_sbagliato():
    """Un difetto di programmazione non diventa «dato non valido»."""
    for argomento in (None, 42, 42.9, b"42", True):
        with pytest.raises(TypeError):
            valida_quantita(argomento)


def test_prezzo_totale_lascia_propagare_l_errore_di_conversione():
    with pytest.raises(ValueError):
        prezzo_totale("tre", 250)


def test_prezzo_totale_calcola_in_centesimi():
    assert prezzo_totale("4", 25) == 100


def test_altro_e_finally_sulla_conversione_riuscita():
    assert prova_conversione("42") == [
        "try: provo la conversione",
        "else: conversione riuscita, valore 42",
        "finally: sempre eseguito",
    ]


def test_altro_e_finally_sulla_conversione_fallita():
    assert prova_conversione("quarantadue") == [
        "try: provo la conversione",
        "except: il testo non è un intero",
        "finally: sempre eseguito",
    ]


# ---------------------------------------------------------------------------
# Date e durate (cap. PY-18)
# ---------------------------------------------------------------------------


def test_date_rifiutano_le_altre_forme_iso_e_le_cifre_non_ascii():
    for testo in ("20240228", "2024-W09-3", "2024-2-28", "２０２４-02-28"):
        with pytest.raises(ValueError, match="formato atteso AAAA-MM-GG"):
            giorni_tra(testo, "2024-03-01")
        with pytest.raises(ValueError, match="formato atteso AAAA-MM-GG"):
            giorni_tra("2024-02-28", testo)
        with pytest.raises(ValueError, match="formato atteso AAAA-MM-GG"):
            eta_anni(testo, "2026-03-01")
        with pytest.raises(ValueError, match="formato atteso AAAA-MM-GG"):
            eta_anni("2010-01-01", testo)


def test_date_separano_il_calendario_dal_formato():
    with pytest.raises(ValueError, match="giorno inesistente nel calendario"):
        giorni_tra("2024-02-30", "2024-03-01")


def test_date_rifiutano_argomenti_non_stringa():
    with pytest.raises(TypeError, match="stringa"):
        giorni_tra(None, "2024-03-01")


def test_giorni_tra_sull_anno_bisestile():
    assert giorni_tra("2024-02-28", "2024-03-01") == 2


def test_giorni_tra_sull_anno_non_bisestile():
    assert giorni_tra("2025-02-28", "2025-03-01") == 1


def test_giorni_tra_lo_stesso_giorno_e_zero():
    assert giorni_tra("2024-02-28", "2024-02-28") == 0


def test_giorni_tra_rifiuta_la_seconda_data_precedente():
    with pytest.raises(ValueError, match="precede"):
        giorni_tra("2024-03-01", "2024-02-28")


def test_giorni_tra_rifiuta_il_formato_invalido():
    with pytest.raises(ValueError):
        giorni_tra("28/02/2024", "2024-03-01")


def test_eta_anni_prima_e_dopo_il_compleanno():
    assert eta_anni("2010-10-20", "2026-10-19") == 15
    assert eta_anni("2010-10-20", "2026-10-20") == 16


def test_eta_anni_con_nascita_il_29_febbraio():
    assert eta_anni("2012-02-29", "2026-02-28") == 13
    assert eta_anni("2012-02-29", "2026-03-01") == 14


def test_eta_anni_nello_stesso_giorno_e_zero():
    assert eta_anni("2010-10-20", "2010-10-20") == 0


def test_eta_anni_rifiuta_la_nascita_futura():
    with pytest.raises(ValueError, match="successiva"):
        eta_anni("2030-01-01", "2026-12-31")


def test_compleanno_anno_applica_la_convenzione_del_1_marzo():
    assert compleanno_anno(date(2012, 2, 29), 2026) == date(2026, 3, 1)
    assert compleanno_anno(date(2012, 2, 29), 2024) == date(2024, 2, 29)
    assert compleanno_anno(date(2010, 10, 20), 2026) == date(2026, 10, 20)


def test_data_da_formato_esplicito():
    assert data_da_formato("20/10/2010", "%d/%m/%Y") == date(2010, 10, 20)


def test_data_da_formato_rifiuta_il_formato_diverso():
    with pytest.raises(ValueError):
        data_da_formato("2010-10-20", "%d/%m/%Y")


# ---------------------------------------------------------------------------
# Fixture di testo e immagini (cartella dati/)
# ---------------------------------------------------------------------------


def test_le_due_fixture_di_testo_hanno_lo_stesso_contenuto():
    senza_bom = (DATI / "testi" / "frase_senza_bom.txt").read_bytes()
    con_bom = (DATI / "testi" / "frase_con_bom.txt").read_bytes()
    assert con_bom == BOM_UTF8 + senza_bom
    assert not senza_bom.startswith(BOM_UTF8)


def test_la_fixture_senza_bom_decodifica_pulita_con_utf8():
    senza_bom = (DATI / "testi" / "frase_senza_bom.txt").read_bytes()
    assert senza_bom.decode("utf-8") == "caffè precomposto\ncaffe\u0300 combinante\na\ufeffb interna\n"


def test_la_fixture_con_bom_chiede_i_due_codec_diversi():
    con_bom = (DATI / "testi" / "frase_con_bom.txt").read_bytes()
    esiti = decodifiche_con_firma(con_bom)
    assert esiti["utf8"].startswith("\ufeff")
    assert esiti["utf8_sig"] == esiti["utf8"][1:]


def test_immagine_rinominata_ha_gli_stessi_byte_e_nome_diverso():
    originale = (DATI / "immagini" / "immagine_originale.bmp").read_bytes()
    rinominata = (DATI / "immagini" / "immagine_rinominata.dat").read_bytes()
    assert rinominata == originale
    assert originale[:2] == b"BM"


def test_immagine_troncata_ha_la_firma_ma_non_la_lunghezza_dichiarata():
    originale = (DATI / "immagini" / "immagine_originale.bmp").read_bytes()
    troncata = (DATI / "immagini" / "immagine_troncata.bmp").read_bytes()
    lunghezza_dichiarata = int.from_bytes(originale[2:6], "little")
    assert lunghezza_dichiarata == len(originale)
    assert troncata[:2] == b"BM"
    assert int.from_bytes(troncata[2:6], "little") == lunghezza_dichiarata
    assert len(troncata) < lunghezza_dichiarata


# ---------------------------------------------------------------------------
# Analisi di testo: parole, frequenze e classifiche (cap. PY-19)
# ---------------------------------------------------------------------------

RIGHE_CANONICHE = ["Sole luna sole", "mare LUNA sole"]
FREQUENZE_PARITA = {"luna": 2, "sole": 2, "mare": 1}


def test_conta_parole_sul_dataset_canonico():
    totale, frequenze = conta_parole(RIGHE_CANONICHE)
    assert totale == 6
    assert frequenze == {"sole": 3, "luna": 2, "mare": 1}


def test_conta_parole_attraversa_l_iterabile_una_sola_volta():
    class UnaSolaVolta:
        def __init__(self, righe):
            self.righe = list(righe)
            self.passaggi = 0

        def __iter__(self):
            self.passaggi += 1
            if self.passaggi > 1:
                raise AssertionError("iterabile attraversato più di una volta")
            return iter(self.righe)

    sorgente = UnaSolaVolta(RIGHE_CANONICHE)
    assert conta_parole(sorgente) == (6, {"sole": 3, "luna": 2, "mare": 1})
    assert sorgente.passaggi == 1


def test_conta_parole_normalizza_maiuscole_e_accenti():
    assert conta_parole(["Città CITTÀ città"]) == (3, {"città": 3})


def test_conta_parole_su_righe_vuote_e_su_soli_spazi():
    assert conta_parole([]) == (0, {})
    assert conta_parole(["", " ", "\t\n"]) == (0, {})


def test_ordina_frequenze_crescente_con_parita_alfabetica():
    assert ordina_frequenze(FREQUENZE_PARITA) == [("mare", 1), ("luna", 2), ("sole", 2)]


def test_ordina_frequenze_decrescente_mantiene_la_parita_alfabetica():
    assert ordina_frequenze(FREQUENZE_PARITA, decrescente=True) == [
        ("luna", 2),
        ("sole", 2),
        ("mare", 1),
    ]


def test_l_ordinamento_sulla_coppia_intera_non_rispetta_la_parita():
    naive = sorted(FREQUENZE_PARITA.items(), reverse=True)
    assert naive == [("sole", 2), ("mare", 1), ("luna", 2)]
    assert naive != ordina_frequenze(FREQUENZE_PARITA, decrescente=True)


def test_ordina_frequenze_non_modifica_il_dizionario():
    frequenze = {"sole": 3, "luna": 1}
    elenco = ordina_frequenze(frequenze)
    assert elenco == [("luna", 1), ("sole", 3)]
    elenco.append(("aggiunta", 9))
    assert frequenze == {"sole": 3, "luna": 1}


def test_ordina_frequenze_sul_dizionario_vuoto():
    assert ordina_frequenze({}) == []
    assert ordina_frequenze({}, decrescente=True) == []


# ---------------------------------------------------------------------------
# File di testo: fixture, EOF, BOM e diagnosi (cap. PY-19)
# ---------------------------------------------------------------------------

TESTI = DATI / "testi"


def test_analizza_file_sul_canonico():
    risultato = analizza_file(TESTI / "analisi_canonica.txt")
    assert risultato["totale"] == 6
    assert risultato["frequenze"] == {"sole": 3, "luna": 2, "mare": 1}
    assert risultato["classifica_crescente"] == [("mare", 1), ("luna", 2), ("sole", 3)]
    assert risultato["classifica_decrescente"] == [("sole", 3), ("luna", 2), ("mare", 1)]


def test_analizza_file_sul_dataset_di_parita():
    risultato = analizza_file(TESTI / "analisi_parita.txt")
    assert risultato["totale"] == 5
    assert risultato["classifica_crescente"] == [("mare", 1), ("luna", 2), ("sole", 2)]
    assert risultato["classifica_decrescente"] == [("luna", 2), ("sole", 2), ("mare", 1)]


def test_file_vuoto_e_soli_spazi_danno_zeri_e_classifiche_vuote():
    atteso = {
        "totale": 0,
        "frequenze": {},
        "classifica_crescente": [],
        "classifica_decrescente": [],
    }
    assert analizza_file(TESTI / "analisi_vuota.txt") == atteso
    assert analizza_file(TESTI / "analisi_spazi.txt") == atteso


def test_ultima_riga_senza_terminatore_non_perde_token():
    risultato = analizza_file(TESTI / "analisi_no_newline.txt")
    assert risultato["totale"] == 6
    assert risultato["frequenze"] == {"sole": 3, "luna": 2, "mare": 1}


def test_sole_e_sole_con_la_virgola_restano_distinti():
    risultato = analizza_file(TESTI / "analisi_punteggiatura.txt")
    assert risultato["totale"] == 2
    assert risultato["frequenze"] == {"sole": 1, "sole,": 1}


def test_bom_non_ammesso_separa_la_prima_parola():
    risultato = analizza_file(TESTI / "analisi_con_bom.txt")
    assert risultato["totale"] == 6
    assert risultato["frequenze"] == {"\ufeffsole": 1, "luna": 2, "sole": 2, "mare": 1}


def test_bom_ammesso_con_utf8_sig_restituisce_il_canonico():
    with open(TESTI / "analisi_con_bom.txt", "r", encoding="utf-8-sig") as sorgente:
        assert conta_parole(sorgente) == (6, {"sole": 3, "luna": 2, "mare": 1})


def test_analizza_file_non_modifica_il_file_di_ingresso():
    percorso = TESTI / "analisi_canonica.txt"
    byte_prima = percorso.read_bytes()
    analizza_file(percorso)
    assert percorso.read_bytes() == byte_prima


def test_percorso_assente_solleva_file_not_found():
    with pytest.raises(FileNotFoundError):
        analizza_file(TESTI / "non_esiste.txt")


def test_directory_al_posto_del_file_solleva_un_os_error():
    # la classe esatta dipende dal sistema operativo: PermissionError su
    # Windows, IsADirectoryError sui sistemi Unix
    with pytest.raises((PermissionError, IsADirectoryError)):
        analizza_file(TESTI)


def test_byte_incompatibili_sollevano_unicode_decode_error():
    with pytest.raises(UnicodeDecodeError):
        analizza_file(TESTI / "byte_incompatibili.txt")


# ---------------------------------------------------------------------------
# Percorsi, righe, modalità e chiusura (cap. PY-19)
# ---------------------------------------------------------------------------


def test_riepilogo_percorso_distingue_file_directory_e_assente():
    fatti_file = riepilogo_percorso(TESTI / "analisi_canonica.txt")
    assert fatti_file["esiste"] is True
    assert fatti_file["e_file"] is True
    assert fatti_file["e_directory"] is False
    assert fatti_file["nome"] == "analisi_canonica.txt"
    assert fatti_file["suffisso"] == ".txt"
    fatti_cartella = riepilogo_percorso(TESTI)
    assert fatti_cartella["e_directory"] is True
    assert fatti_cartella["e_file"] is False
    fatti_assente = riepilogo_percorso(TESTI / "non_esiste.txt")
    assert fatti_assente["esiste"] is False
    assert fatti_assente["e_file"] is False
    assert fatti_assente["e_directory"] is False


def test_stesso_percorso_relativo_da_radici_diverse():
    fatti = radici_di_lavoro()
    assert fatti["os.getcwd()"] == fatti["Path.cwd()"]
    assert fatti["relativo da Path.cwd()"] != fatti["relativo dalla cartella del sorgente"]
    assert fatti["cartella del sorgente"] != fatti["os.getcwd()"]


def test_variabile_di_ambiente_con_default(monkeypatch):
    monkeypatch.delenv("CORSO_UTENTE", raising=False)
    assert radici_di_lavoro()["CORSO_UTENTE (default: ospite)"] == "ospite"
    monkeypatch.setenv("CORSO_UTENTE", "anna")
    assert radici_di_lavoro()["CORSO_UTENTE (default: ospite)"] == "anna"


def test_le_tre_letture_concordano_sul_canonico():
    percorso = TESTI / "analisi_canonica.txt"
    attese = ["Sole luna sole\n", "mare LUNA sole\n"]
    assert leggi_con_iterazione(percorso) == attese
    assert leggi_con_readline(percorso) == (attese, True)
    assert leggi_con_readlines(percorso) == attese


def test_ultima_riga_senza_terminatore_non_ha_il_newline():
    righe, ultima_terminata = leggi_con_readline(TESTI / "analisi_no_newline.txt")
    assert righe == ["Sole luna sole\n", "mare LUNA sole"]
    assert ultima_terminata is False


def test_readline_su_file_vuoto_restituisce_subito_stringa_vuota():
    righe, ultima_terminata = leggi_con_readline(TESTI / "analisi_vuota.txt")
    assert righe == []
    assert ultima_terminata is False


def test_eof_e_riga_vuota_sono_valori_diversi(tmp_path):
    percorso = tmp_path / "riga_vuota.txt"
    percorso.write_bytes(b"\n")
    with open(percorso, "r", encoding="utf-8") as sorgente:
        assert sorgente.readline() == "\n"
        assert sorgente.readline() == ""


def test_la_modalita_w_tronca_un_file_esistente(tmp_path):
    percorso = tmp_path / "appunti.txt"
    percorso.write_text("contenuto lungo da non perdere\n", encoding="utf-8")
    with open(percorso, "w", encoding="utf-8") as destinazione:
        destinazione.write("breve\n")
    assert percorso.read_text(encoding="utf-8") == "breve\n"


def test_esperimento_modalita_descrive_creazione_troncatura_e_rifiuto(tmp_path):
    osservazioni = esperimento_modalita(tmp_path)
    assert [passo for passo, _ in osservazioni] == [
        "w su file assente: crea",
        "a su file esistente: aggiunge in fondo",
        "w su file esistente: tronca e riscrive",
        "x su file esistente: rifiuta",
        "contenuto finale di prova_modalita.txt",
        "x su nome libero: crea",
    ]
    assert (tmp_path / "prova_modalita.txt").read_text(encoding="utf-8") == "riscrittura\n"
    assert (tmp_path / "secondo_prova.txt").read_text(encoding="utf-8") == "creato da x\n"


def test_byte_iniziali_della_firma_utf8():
    assert byte_iniziali(TESTI / "analisi_con_bom.txt", 3) == BOM_UTF8
    assert byte_iniziali(TESTI / "analisi_canonica.txt", 3) == b"Sol"


def test_byte_iniziali_su_file_vuoto_e_una_sequenza_vuota():
    assert byte_iniziali(TESTI / "analisi_vuota.txt") == b""


def test_prova_apertura_nomina_le_classi_degli_errori():
    assert prova_apertura(TESTI / "analisi_canonica.txt") == "apertura riuscita"
    assert prova_apertura(TESTI / "non_esiste.txt") == "apertura non riuscita: FileNotFoundError"
    assert prova_apertura(TESTI) in (
        "apertura non riuscita: PermissionError",
        "apertura non riuscita: IsADirectoryError",
    )


def test_apertura_riuscita_non_decodifica():
    # il file con byte incompatibili si apre e fallisce soltanto alla lettura
    assert prova_apertura(TESTI / "byte_incompatibili.txt") == "apertura riuscita"


def test_il_with_chiude_il_file_anche_in_uscita_anomala(tmp_path):
    percorso = tmp_path / "prova.txt"
    percorso.write_text("prima\nseconda\n", encoding="utf-8")
    with pytest.raises(ValueError):
        with open(percorso, "r", encoding="utf-8") as sorgente:
            sorgente.readline()
            raise ValueError("guasto previsto dal test")
    assert sorgente.closed is True


# ---------------------------------------------------------------------------
# CLI dell'analisi di testo (cap. PY-19)
# ---------------------------------------------------------------------------


def test_cli_sul_canonico_stampa_il_riepilogo_e_codice_zero(capsys):
    codice = cli_main([str(TESTI / "analisi_canonica.txt")])
    uscita = capsys.readouterr().out
    assert codice == 0
    assert "parole totali: 6" in uscita
    assert "parole distinte: 3" in uscita
    assert "  mare 1\n  luna 2\n  sole 3" in uscita
    assert "  sole 3\n  luna 2\n  mare 1" in uscita


def test_cli_sul_vuoto_dichiara_le_classifiche_vuote(capsys):
    codice = cli_main([str(TESTI / "analisi_vuota.txt")])
    uscita = capsys.readouterr().out
    assert codice == 0
    assert "parole totali: 0" in uscita
    assert uscita.count("(vuota)") == 2


def test_cli_sui_casi_di_errore_codici_e_messaggi(capsys):
    assert cli_main([str(TESTI / "non_esiste.txt")]) == 1
    assert "file non trovato" in capsys.readouterr().out
    assert cli_main([str(TESTI)]) == 1
    assert "non leggibile" in capsys.readouterr().out
    assert cli_main([str(TESTI / "byte_incompatibili.txt")]) == 1
    assert "byte non UTF-8" in capsys.readouterr().out
    assert cli_main([]) == 2
    assert "uso:" in capsys.readouterr().out


def test_righe_presentazione_non_stampa_ma_restituisce_righe():
    risultato = {
        "totale": 2,
        "frequenze": {"a": 1, "b": 1},
        "classifica_crescente": [("a", 1), ("b", 1)],
        "classifica_decrescente": [("a", 1), ("b", 1)],
    }
    righe = righe_presentazione(risultato)
    assert righe[0] == "parole totali: 2"
    assert righe[1] == "parole distinte: 2"
    assert "  a 1" in righe
    assert "  b 1" in righe


def test_l_import_dei_moduli_nuovi_non_produce_output():
    esito = subprocess.run(
        [sys.executable, "-c", "import cli_testo_u12; import percorsi_testo_u12"],
        cwd=CARTELLA_ESEMPI,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert esito.returncode == 0
    assert esito.stdout == ""
    assert esito.stderr == ""
