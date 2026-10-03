"""Suite di verifica dei sorgenti d'esempio dell'Unità 12 (moduli, byte, eccezioni, date, testo, record).

I test controllano gli attesi dichiarati nei capitoli PY-16, PY-17, PY-18,
PY-19, PY-20 e PY-21 e le proprietà dei moduli `utilita_u12`, `demo_import_u12`,
`codifiche_u12`, `eccezioni_date_u12`, `analisi_testo_u12`,
`percorsi_testo_u12`, `cli_testo_u12`, `dominio_magazzino_u12`,
`persistenza_magazzino_u12`, `cli_magazzino_u12`, `json_u12`,
`record_binari_u12` e `immagini_bmp_u12`: valore
dell'inventario, assenza di effetti all'import, conti separati di codepoint e
byte, comportamento del BOM con i due codec, controlli separati di conversione
e dominio, `else`/`finally`, date con riferimenti fissi, fixture di testo e
immagini nella cartella `dati/`, conteggio delle parole e classifiche con
parità alfabetica, righe, EOF, terminatori, modalità di apertura e diagnosi
delle aperture, quindi schema del magazzino, CRUD senza aggiornamenti parziali,
caricamento CSV con intestazioni e BOM, salvataggio mediante temporaneo con i
guasti simulati della matrice MAG-01-MAG-20 e serializzazione JSON con i tre
controlli separati di sintassi, struttura e dominio. La sezione sui record
binari verifica byte esatti, offset `i * 2`, domini di indice e valore,
archivio vuoto o incompleto e `seek` dalle tre origini; la sezione sulle
immagini verifica l'intestazione BMP, i pixel BGR a posizione calcolata e i
due filtri RGB dell'esempio del cap. PY-21.

Esecuzione dalla cartella `unita-12/`:

    uv run --python 3.14 --with pytest python -m pytest esempi/test_esempi_u12.py -q

La suite è deterministica: usa dati espliciti e riferimenti di data fissi,
mai `date.today()` né durate reali. I test che scrivono file usano la cartella
isolata `tmp_path` oppure copie di lavoro: le fixture di `dati/` restano
invariate. I guasti di scrittura e di sostituzione sono intercettati in modo
deterministico (monkeypatch mirato), non affidati ai permessi della cartella.
"""

import csv
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from analisi_testo_u12 import analizza_file, conta_parole, ordina_frequenze
from cli_magazzino_u12 import main as cli_magazzino_main
from cli_magazzino_u12 import riga_articolo, righe_situazione
from cli_testo_u12 import main as cli_main
from cli_testo_u12 import righe_presentazione
from codifiche_u12 import BOM_UTF8, confronto_bytearray, decodifiche_con_firma, sommario_testo
from demo_import_u12 import genera_inventario, presentazione_riga, presentazione_tabella
from dominio_magazzino_u12 import (
    CAMPI_ARTICOLO,
    articolo_a_riga,
    cerca_articolo,
    elimina_articolo,
    formatta_centesimi,
    inserisci_articolo,
    modifica_articolo,
    riga_a_articolo,
    riepilogo_magazzino,
    valida_articolo,
)
from eccezioni_date_u12 import (
    compleanno_anno,
    data_da_formato,
    eta_anni,
    giorni_tra,
    prezzo_totale,
    prova_conversione,
    valida_quantita,
)
from immagini_bmp_u12 import (
    intestazione_bmp,
    inverti_colori,
    leggi_pixel,
    scambia_blu_rosso,
)
from json_u12 import (
    carica_json,
    deserializza_articoli,
    deserializza_articoli_strict,
    salva_json,
    serializza_articoli,
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
from persistenza_magazzino_u12 import carica_articoli, salva_articoli
from record_binari_u12 import aggiorna_record_due_byte, leggi_record_due_byte, traccia_seek
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


def test_cli_non_dichiara_una_posizione_assoluta_dal_buffer(tmp_path, capsys):
    percorso = tmp_path / "incompatibile_dopo_piu_blocchi.txt"
    dati = b"sole\n" * 2000 + b"\xe8"
    percorso.write_bytes(dati)
    assert cli_main([str(percorso)]) == 1
    assert capsys.readouterr().out == f"byte non UTF-8 nel file: {percorso}\n"
    assert percorso.read_bytes() == dati


@pytest.mark.skipif(sys.platform != "win32", reason="nome non ammesso su Windows")
def test_cli_diagnostica_un_nome_non_valido_su_windows(tmp_path, capsys):
    percorso = tmp_path / "nome<non_valido>.txt"
    assert cli_main([str(percorso)]) == 1
    uscita = capsys.readouterr().out
    assert "errore di accesso o lettura" in uscita
    assert str(percorso) in uscita
    assert "parole totali" not in uscita


def test_cli_diagnostica_gli_altri_errori_di_io(monkeypatch, capsys):
    def lettura_fallita(percorso):
        raise OSError("guasto di lettura simulato")

    monkeypatch.setattr("cli_testo_u12.analizza_file", lettura_fallita)
    assert cli_main(["registro.txt"]) == 1
    uscita = capsys.readouterr().out
    assert "errore di accesso o lettura" in uscita
    assert "guasto di lettura simulato" in uscita
    assert "parole totali" not in uscita


@pytest.mark.parametrize("tipo_errore", (TypeError, ValueError))
def test_cli_lascia_visibili_i_difetti_di_programmazione(tipo_errore, monkeypatch, capsys):
    def calcolo_errato(percorso):
        raise tipo_errore("difetto di programmazione simulato")

    monkeypatch.setattr("cli_testo_u12.analizza_file", calcolo_errato)
    with pytest.raises(tipo_errore, match="difetto di programmazione simulato"):
        cli_main(["registro.txt"])
    assert capsys.readouterr().out == ""


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


# ---------------------------------------------------------------------------
# Magazzino CSV: schema, CRUD e persistenza (cap. PY-20) - matrice MAG
# ---------------------------------------------------------------------------

CSV_DATI = DATI / "csv"
JSON_DATI = DATI / "json"

ARTICOLO_020 = {"codice": "020", "descrizione": "Bullone", "quantita": 1, "prezzo_centesimi": 7}


def _copia_canonico(tmp_path):
    """Copia di lavoro dell'archivio canonico: la fixture resta invariata."""
    destinazione = tmp_path / "magazzino.csv"
    destinazione.write_bytes((CSV_DATI / "magazzino_canonico.csv").read_bytes())
    return destinazione


def _input_finto(comandi):
    """Sostituisce `input` con una sequenza finita di risposte, poi EOF."""
    rimanenti = iter(comandi)

    def leggi(messaggio=""):
        try:
            return next(rimanenti)
        except StopIteration:
            raise EOFError

    return leggi


def _esegui_cli(archivio, testo):
    """Avvia la CLI in un processo proprio, con uno script di input."""
    return subprocess.run(
        [sys.executable, str(CARTELLA_ESEMPI / "cli_magazzino_u12.py"), str(archivio)],
        input=testo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
    )


# --- conversione e schema -------------------------------------------------


def test_riga_a_articolo_converte_i_tipi_e_conserva_gli_zeri():
    articolo = riga_a_articolo(["007", "Vite, lunga", "4", "25"], "record 1")
    assert articolo == RECORD_CANONICI[0]
    assert isinstance(articolo["quantita"], int)
    assert isinstance(articolo["prezzo_centesimi"], int)
    assert articolo_a_riga(articolo) == ["007", "Vite, lunga", "4", "25"]


def test_riga_a_articolo_diagnostica_campo_e_riferimento():
    with pytest.raises(ValueError, match="record 2, campo 'quantita'"):
        riga_a_articolo(["007", "x", "tre", "1"], "record 2")
    with pytest.raises(ValueError, match="attesi 4 campi"):
        riga_a_articolo(["007", "x", "1"], "record 2")


def test_valida_articolo_rifiuta_bool_e_float_come_quantita():
    for valore in (True, False, 1.0, "1", None):
        with pytest.raises(ValueError, match="atteso un intero"):
            valida_articolo(
                {"codice": "007", "descrizione": "x", "quantita": valore, "prezzo_centesimi": 0}
            )


def test_valida_articolo_separa_campi_mancanti_non_previsti_e_domini():
    with pytest.raises(ValueError, match="mancante"):
        valida_articolo({"codice": "007", "descrizione": "x", "quantita": 1})
    with pytest.raises(ValueError, match="non previsto"):
        valida_articolo(
            {"codice": "007", "descrizione": "x", "quantita": 1, "prezzo_centesimi": 0, "note": "n"}
        )
    with pytest.raises(ValueError, match="spazi iniziali"):
        valida_articolo(
            {"codice": " 007", "descrizione": "x", "quantita": 1, "prezzo_centesimi": 0}
        )
    with pytest.raises(ValueError, match="non bianco"):
        valida_articolo(
            {"codice": "007", "descrizione": "   ", "quantita": 1, "prezzo_centesimi": 0}
        )
    with pytest.raises(ValueError, match="maggiore o uguale a zero"):
        valida_articolo(
            {"codice": "007", "descrizione": "x", "quantita": -1, "prezzo_centesimi": 0}
        )


def test_formatta_centesimi_gestisce_zero_e_resti_piccoli():
    assert formatta_centesimi(0) == "0,00 €"
    assert formatta_centesimi(5) == "0,05 €"
    assert formatta_centesimi(800) == "8,00 €"
    assert formatta_centesimi(1234) == "12,34 €"


# --- MAG-01-MAG-10: avvio, ricerche, CRUD e stato -------------------------


def test_mag01_primo_avvio_con_archivio_assente(monkeypatch, tmp_path, capsys):
    archivio = tmp_path / "nuovo.csv"
    monkeypatch.setattr("builtins.input", _input_finto(["1", "0"]))
    assert cli_magazzino_main([str(archivio)]) == 0
    uscita = capsys.readouterr().out
    assert "archivio assente" in uscita
    assert "(magazzino vuoto)" in uscita
    assert not archivio.exists()


def test_mag02_il_canonico_ricostruisce_i_tipi_e_il_valore():
    articoli = carica_articoli(CSV_DATI / "magazzino_canonico.csv")
    assert articoli == RECORD_CANONICI
    for articolo in articoli:
        assert isinstance(articolo["quantita"], int)
        assert isinstance(articolo["prezzo_centesimi"], int)
    assert riepilogo_magazzino(articoli) == {
        "articoli": 2,
        "quantita_totale": 6,
        "valore_centesimi": 800,
    }


def test_mag03_ricerca_prima_ultima_posizione_e_assente():
    articoli = [dict(record) for record in RECORD_CANONICI]
    prima = [dict(record) for record in articoli]
    assert cerca_articolo(articoli, "007") == 0
    assert cerca_articolo(articoli, "012") == 1
    assert cerca_articolo(articoli, "999") is None
    assert cerca_articolo(articoli, "7") is None
    assert articoli == prima


def test_mag04_inserimento_ordinario_e_duplicato_rifiutato():
    articoli = [dict(record) for record in RECORD_CANONICI]
    assert inserisci_articolo(articoli, dict(ARTICOLO_020)) is None
    assert len(articoli) == 3
    assert articoli[2] == ARTICOLO_020
    articoli[2]["descrizione"] = "cambiata solo nella lista"
    assert ARTICOLO_020["descrizione"] == "Bullone"
    prima = [dict(record) for record in articoli]
    with pytest.raises(ValueError, match="già presente"):
        inserisci_articolo(articoli, dict(RECORD_CANONICI[0]))
    assert articoli == prima


def test_mag05_modifica_valida_aggiorna_i_tre_campi():
    articoli = [dict(record) for record in RECORD_CANONICI]
    assert modifica_articolo(articoli, "007", "Vite, corta", 9, 30) is True
    assert articoli[0] == {
        "codice": "007",
        "descrizione": "Vite, corta",
        "quantita": 9,
        "prezzo_centesimi": 30,
    }


def test_mag06_modifica_con_campo_invalido_non_applica_nulla():
    articoli = [dict(record) for record in RECORD_CANONICI]
    prima = [dict(record) for record in articoli]
    with pytest.raises(ValueError, match="quantita"):
        modifica_articolo(articoli, "007", "nuova", -1, 30)
    assert articoli == prima
    with pytest.raises(ValueError, match="descrizione"):
        modifica_articolo(articoli, "007", "   ", 1, 30)
    assert articoli == prima
    assert modifica_articolo(articoli, "999", "x", 1, 1) is False
    assert articoli == prima


def test_mag06b_cli_con_modifica_rifiutata_non_scritto_nulla(monkeypatch, tmp_path, capsys):
    archivio = _copia_canonico(tmp_path)
    originali = archivio.read_bytes()

    def vietato(percorso, articoli):
        raise AssertionError("nessuna modifica pendente: non si deve scrivere")

    monkeypatch.setattr("cli_magazzino_u12.salva_articoli", vietato)
    monkeypatch.setattr("builtins.input", _input_finto(["4", "007", "Nuova", "-1", "5", "0"]))
    assert cli_magazzino_main([str(archivio)]) == 0
    assert "aggiornamento rifiutato" in capsys.readouterr().out
    assert archivio.read_bytes() == originali


def test_mag07_elimina_restituisce_true_o_false_senza_domande():
    articoli = [dict(record) for record in RECORD_CANONICI]
    assert elimina_articolo(articoli, "007") is True
    assert articoli == [RECORD_CANONICI[1]]
    assert elimina_articolo(articoli, "007") is False
    assert articoli == [RECORD_CANONICI[1]]


def test_mag07b_cli_annulla_conferma_non_ammessa_e_assente(monkeypatch, tmp_path, capsys):
    archivio = _copia_canonico(tmp_path)
    originali = archivio.read_bytes()
    monkeypatch.setattr("builtins.input", _input_finto(["5", "007", "x", "5", "007", "n", "5", "999", "0"]))
    assert cli_magazzino_main([str(archivio)]) == 0
    uscita = capsys.readouterr().out
    assert uscita.count("eliminazione annullata") == 2
    assert "articolo assente: nessun codice '999'" in uscita
    assert archivio.read_bytes() == originali


def test_mag07c_cli_conferma_s_elimina_e_poi_salva(monkeypatch, tmp_path, capsys):
    archivio = _copia_canonico(tmp_path)
    monkeypatch.setattr("builtins.input", _input_finto(["5", "007", "s", "0"]))
    assert cli_magazzino_main([str(archivio)]) == 0
    assert "articolo '007' eliminato" in capsys.readouterr().out
    assert [articolo["codice"] for articolo in carica_articoli(archivio)] == ["012"]


def test_mag08_salvataggio_esplicito_e_prosecuzione(monkeypatch, tmp_path, capsys):
    archivio = _copia_canonico(tmp_path)
    chiamate = []
    reale = salva_articoli

    def spia(percorso, articoli):
        chiamate.append(Path(percorso))
        return reale(percorso, articoli)

    monkeypatch.setattr("cli_magazzino_u12.salva_articoli", spia)
    monkeypatch.setattr("builtins.input", _input_finto(["3", "020", "Bullone", "1", "7", "6", "1", "0"]))
    assert cli_magazzino_main([str(archivio)]) == 0
    uscita = capsys.readouterr().out
    assert "archivio salvato" in uscita
    assert "articoli: 3" in uscita
    assert len(chiamate) == 1


def test_mag09_uscita_con_modifiche_salva_e_il_riavvio_e_equivalente(monkeypatch, tmp_path, capsys):
    archivio = _copia_canonico(tmp_path)
    monkeypatch.setattr("builtins.input", _input_finto(["3", "020", "Bullone", "1", "7", "0"]))
    assert cli_magazzino_main([str(archivio)]) == 0
    assert "archivio salvato" in capsys.readouterr().out
    ricaricati = carica_articoli(archivio)
    assert [articolo["codice"] for articolo in ricaricati] == ["007", "012", "020"]
    monkeypatch.setattr("builtins.input", _input_finto(["0"]))
    assert cli_magazzino_main([str(archivio)]) == 0
    assert carica_articoli(archivio) == ricaricati


def test_mag10_uscita_senza_modifiche_non_riscrive(monkeypatch, tmp_path):
    archivio = _copia_canonico(tmp_path)
    originali = archivio.read_bytes()

    def vietato(percorso, articoli):
        raise AssertionError("il salvataggio non deve essere richiesto")

    monkeypatch.setattr("cli_magazzino_u12.salva_articoli", vietato)
    monkeypatch.setattr("builtins.input", _input_finto(["1", "2", "007", "0"]))
    assert cli_magazzino_main([str(archivio)]) == 0
    assert archivio.read_bytes() == originali


# --- MAG-11 e MAG-15: caricamento, diagnosi e stato precedente ------------


def test_mag11_intestazione_colonne_tipo_dominio_e_duplicato(tmp_path):
    casi = [
        (b"codice,descrizione,quantita\n007,x,1\n", "colonna mancante"),
        (b"codice,descrizione,quantita,prezzo_centesimi,note\n007,x,1,2,n\n", "colonna non prevista"),
        (b"codice,codice,quantita,prezzo_centesimi\n007,x,1,2\n", "duplicati"),
        (b"descrizione,codice,quantita,prezzo_centesimi\nx,007,1,2\n", "ordine"),
        (b"codice,descrizione,quantita,prezzo_centesimi\n007,x,tre,2\n", "non è un intero"),
        (b"codice,descrizione,quantita,prezzo_centesimi\n007,x,-1,2\n", "maggiore o uguale a zero"),
    ]
    percorso = tmp_path / "archivio.csv"
    for contenuto, atteso in casi:
        percorso.write_bytes(contenuto)
        with pytest.raises(ValueError, match=atteso):
            carica_articoli(percorso)


def test_mag11_fixture_di_errore_e_file_assente_distinto_da_corrotto(tmp_path):
    with pytest.raises(ValueError, match="colonna mancante"):
        carica_articoli(CSV_DATI / "magazzino_schema_errato.csv")
    with pytest.raises(ValueError, match="già presente"):
        carica_articoli(CSV_DATI / "magazzino_duplicati.csv")
    with pytest.raises(FileNotFoundError):
        carica_articoli(tmp_path / "assente.csv")
    vuoto = tmp_path / "vuoto.csv"
    vuoto.write_bytes(b"")
    with pytest.raises(ValueError, match="senza intestazione"):
        carica_articoli(vuoto)


def test_mag11b_strict_true_segnala_quello_che_strict_false_accetta():
    righe = ['007,"Vite,4,25']
    assert list(csv.reader(righe, strict=False)) == [["007", "Vite,4,25"]]
    with pytest.raises(csv.Error):
        list(csv.reader(righe, strict=True))


def test_mag11c_cli_con_archivio_corrotto_diagnostica_e_ferma(monkeypatch, tmp_path, capsys):
    archivio = tmp_path / "corrotto.csv"
    originali = (CSV_DATI / "magazzino_duplicati.csv").read_bytes()
    archivio.write_bytes(originali)
    monkeypatch.setattr("cli_magazzino_u12.salva_articoli", lambda p, a: None)
    assert cli_magazzino_main([str(archivio)]) == 1
    uscita = capsys.readouterr().out
    assert "archivio non valido" in uscita
    assert "già presente" in uscita
    assert "1 - elenco e riepilogo" not in uscita
    assert archivio.read_bytes() == originali


def test_mag15_fallimento_e_raccolta_vuota_valida_sono_casi_diversi(tmp_path):
    # Il caricatore non pubblica liste parziali: il record valido in testa al
    # file dei duplicati non viene reso disponibile quando il secondo fallisce.
    percorso = tmp_path / "duplicati.csv"
    percorso.write_bytes((CSV_DATI / "magazzino_duplicati.csv").read_bytes())
    with pytest.raises(ValueError):
        carica_articoli(percorso)
    solo_intestazione = tmp_path / "solo_intestazione.csv"
    solo_intestazione.write_bytes(b"codice,descrizione,quantita,prezzo_centesimi\n")
    assert carica_articoli(solo_intestazione) == []


def test_righe_fisiche_vuote_ignorate_e_record_vuoti_rifiutati(tmp_path):
    percorso = tmp_path / "righe_vuote.csv"
    percorso.write_bytes(b"codice,descrizione,quantita,prezzo_centesimi\n\n007,x,1,2\n\n")
    assert [articolo["codice"] for articolo in carica_articoli(percorso)] == ["007"]
    casi = [
        (b",x,1,2\n", "campo 'codice'"),
        (b"007,,1,2\n", "campo 'descrizione'"),
        (b"007,x,,2\n", "non è un intero"),
    ]
    altro = tmp_path / "vuoti.csv"
    for riga, atteso in casi:
        altro.write_bytes(b"codice,descrizione,quantita,prezzo_centesimi\n" + riga)
        with pytest.raises(ValueError, match=atteso):
            carica_articoli(altro)


# --- MAG-12-MAG-14: guasti di scrittura e di sostituzione -----------------


def test_mag12_guasto_durante_la_scrittura_del_temporaneo(monkeypatch, tmp_path):
    archivio = _copia_canonico(tmp_path)
    originali = archivio.read_bytes()
    articoli = carica_articoli(archivio)
    reale = csv.writer
    scritte = {"n": 0}

    class ScrittoreGuasto:
        def __init__(self, vero):
            self.vero = vero

        def writerow(self, riga):
            scritte["n"] += 1
            if scritte["n"] > 2:
                # Il guasto arriva dopo intestazione e primo record scritti.
                raise OSError("guasto simulato durante la scrittura")
            self.vero.writerow(riga)

    monkeypatch.setattr(
        csv, "writer", lambda uscita, **opzioni: ScrittoreGuasto(reale(uscita, **opzioni))
    )
    with pytest.raises(OSError, match="guasto simulato durante la scrittura"):
        salva_articoli(archivio, articoli)
    assert scritte["n"] == 3
    assert archivio.read_bytes() == originali
    assert list(tmp_path.glob("*.tmp")) == []


def test_mag13_guasto_alla_sostituzione_con_temporaneo_pulito(monkeypatch, tmp_path):
    archivio = _copia_canonico(tmp_path)
    originali = archivio.read_bytes()
    articoli = carica_articoli(archivio)

    def sostituzione_fallita(self, destinazione):
        raise OSError("guasto simulato alla sostituzione")

    monkeypatch.setattr(Path, "replace", sostituzione_fallita)
    with pytest.raises(OSError, match="guasto simulato alla sostituzione"):
        salva_articoli(archivio, articoli)
    assert archivio.read_bytes() == originali
    assert list(tmp_path.glob("*.tmp")) == []


def test_mag13b_residuo_di_pulizia_non_maschera_il_guasto_primario(monkeypatch, tmp_path):
    archivio = _copia_canonico(tmp_path)
    originali = archivio.read_bytes()
    articoli = carica_articoli(archivio)

    def sostituzione_fallita(self, destinazione):
        raise OSError("guasto simulato alla sostituzione")

    def pulizia_fallita(self, missing_ok=False):
        raise OSError("pulizia fallita")

    monkeypatch.setattr(Path, "replace", sostituzione_fallita)
    monkeypatch.setattr(Path, "unlink", pulizia_fallita)
    with pytest.raises(OSError, match="guasto simulato alla sostituzione") as sollevata:
        salva_articoli(archivio, articoli)
    note = getattr(sollevata.value, "__notes__", [])
    assert any("temporaneo non rimosso" in nota for nota in note)
    assert archivio.read_bytes() == originali
    residui = list(tmp_path.glob("*.tmp"))
    assert len(residui) == 1


@pytest.mark.parametrize("voce", ("6", "0"))
def test_mag13c_cli_mostra_il_percorso_del_residuo(voce, monkeypatch, tmp_path, capsys):
    archivio = _copia_canonico(tmp_path)
    originali = archivio.read_bytes()

    def sostituzione_fallita(self, destinazione):
        raise OSError("guasto simulato alla sostituzione")

    def pulizia_fallita(self, missing_ok=False):
        raise OSError("pulizia fallita")

    # Il context limita i guasti alla sessione: la pulizia di pytest resta reale.
    with monkeypatch.context() as guasti:
        guasti.setattr(Path, "replace", sostituzione_fallita)
        guasti.setattr(Path, "unlink", pulizia_fallita)
        guasti.setattr("builtins.input", _input_finto(["3", "020", "Bullone", "1", "7", voce]))
        assert cli_magazzino_main([str(archivio)]) == 1
    uscita = capsys.readouterr().out
    residui = list(tmp_path.glob("*.tmp"))
    assert len(residui) == 1
    assert "salvataggio non riuscito: guasto simulato alla sostituzione" in uscita
    assert f"temporaneo non rimosso: {residui[0]}" in uscita
    assert "archivio salvato" not in uscita
    assert "modifiche non salvate" in uscita
    assert archivio.read_bytes() == originali


def test_mag14_guasto_del_salvataggio_alla_voce_zero(monkeypatch, tmp_path, capsys):
    archivio = _copia_canonico(tmp_path)
    originali = archivio.read_bytes()

    def guasto(percorso, articoli):
        raise OSError("guasto simulato al salvataggio")

    monkeypatch.setattr("cli_magazzino_u12.salva_articoli", guasto)
    monkeypatch.setattr(
        "builtins.input", _input_finto(["3", "020", "Bullone", "1", "7", "0", "0"])
    )
    assert cli_magazzino_main([str(archivio)]) == 1
    uscita = capsys.readouterr().out
    assert uscita.count("salvataggio non riuscito") == 2
    assert "si resta nel menu con le modifiche in memoria" in uscita
    assert "archivio salvato" not in uscita
    assert "sessione interrotta" in uscita
    assert "modifiche non salvate" in uscita
    assert archivio.read_bytes() == originali


# --- MAG-16-MAG-20: round-trip, comandi, EOF, riavvii, import -------------


def test_mag16_round_trip_byte_identico_sul_canonico(tmp_path):
    articoli = carica_articoli(CSV_DATI / "magazzino_canonico.csv")
    copia = tmp_path / "copia.csv"
    salva_articoli(copia, articoli)
    assert copia.read_bytes() == (CSV_DATI / "magazzino_canonico.csv").read_bytes()
    assert not copia.read_bytes().startswith(b"\xef\xbb\xbf")
    assert carica_articoli(copia) == articoli


def test_mag16b_bom_ammesso_in_entrata_e_mai_in_uscita(tmp_path):
    con_bom = CSV_DATI / "magazzino_con_bom.csv"
    prima_riga = con_bom.read_text(encoding="utf-8").splitlines()[0]
    assert prima_riga == "\ufeffcodice,descrizione,quantita,prezzo_centesimi"
    articoli = carica_articoli(con_bom)
    assert articoli == RECORD_CANONICI
    uscita = tmp_path / "uscita.csv"
    salva_articoli(uscita, articoli)
    assert not uscita.read_bytes().startswith(b"\xef\xbb\xbf")


def test_mag16c_quoting_multilinea_record_e_righe_fisiche_distinte(tmp_path):
    articoli = carica_articoli(CSV_DATI / "magazzino_quoting.csv")
    assert len(articoli) == 3
    assert articoli[2]["descrizione"] == "Riga uno\nRiga due"
    righe_fisiche = (CSV_DATI / "magazzino_quoting.csv").read_text(encoding="utf-8").count("\n")
    assert righe_fisiche == 5
    copia = tmp_path / "quoting.csv"
    salva_articoli(copia, articoli)
    assert carica_articoli(copia) == articoli


def test_mag17_comando_sconosciuto_e_input_numerico_non_valido(monkeypatch, tmp_path, capsys):
    archivio = _copia_canonico(tmp_path)
    monkeypatch.setattr(
        "builtins.input", _input_finto(["7", "abc", "3", "030", "Dado", "tre", "1", "0"])
    )
    assert cli_magazzino_main([str(archivio)]) == 0
    uscita = capsys.readouterr().out
    assert uscita.count("comando non riconosciuto") == 2
    assert "inserimento rifiutato" in uscita
    assert "non è un intero" in uscita
    assert carica_articoli(archivio) == RECORD_CANONICI


def test_mag18_eof_con_modifiche_pendenti_avvisa_e_non_salva(tmp_path):
    archivio = _copia_canonico(tmp_path)
    originali = archivio.read_bytes()
    esito = _esegui_cli(archivio, "3\n020\nBullone\n1\n7\n")
    assert esito.returncode == 1
    assert "sessione interrotta" in esito.stdout
    assert "modifiche non salvate" in esito.stdout
    assert "archivio salvato" not in esito.stdout
    assert archivio.read_bytes() == originali


def test_mag18b_eof_senza_modifiche_avvisa_senza_allarme(tmp_path):
    archivio = _copia_canonico(tmp_path)
    esito = _esegui_cli(archivio, "")
    assert esito.returncode == 1
    assert "sessione interrotta" in esito.stdout
    assert "modifiche non salvate" not in esito.stdout


def test_mag19_più_avvii_consecutivi_non_duplicano_i_dati(tmp_path):
    archivio = _copia_canonico(tmp_path)
    assert _esegui_cli(archivio, "3\n020\nBullone\n1\n7\n0\n").returncode == 0
    assert [articolo["codice"] for articolo in carica_articoli(archivio)] == ["007", "012", "020"]
    secondo = _esegui_cli(archivio, "1\n0\n")
    assert secondo.returncode == 0
    assert "articoli: 3" in secondo.stdout
    assert _esegui_cli(archivio, "1\n0\n").returncode == 0
    ricaricati = carica_articoli(archivio)
    assert len(ricaricati) == 3
    for articolo in ricaricati:
        assert isinstance(articolo["quantita"], int)


def test_mag20_import_dei_tre_moduli_senza_effetti():
    esito = subprocess.run(
        [
            sys.executable,
            "-c",
            "import dominio_magazzino_u12; import persistenza_magazzino_u12; import cli_magazzino_u12",
        ],
        cwd=CARTELLA_ESEMPI,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert esito.returncode == 0
    assert esito.stdout == ""
    assert esito.stderr == ""
    assert list(CARTELLA_ESEMPI.glob("*.csv")) == []
    assert list(CARTELLA_UNITA.glob("*.csv")) == []


# --- presentazione della CLI ----------------------------------------------


def test_righe_situazione_mostra_conversione_e_record():
    righe = righe_situazione(RECORD_CANONICI)
    assert righe[0] == '007 - Vite, lunga - quantita 4 - prezzo 0,25 €'
    assert righe[1] == '012 - Caffè "A" - quantita 2 - prezzo 3,50 €'
    assert "valore complessivo: 800 centesimi = 8,00 €" in righe
    assert righe_situazione([])[0] == "(magazzino vuoto)"
    assert riga_articolo(ARTICOLO_020) == "020 - Bullone - quantita 1 - prezzo 0,07 €"


def test_carica_restituisce_liste_nuove_e_salva_non_modifica(tmp_path):
    primi = carica_articoli(CSV_DATI / "magazzino_canonico.csv")
    secondi = carica_articoli(CSV_DATI / "magazzino_canonico.csv")
    assert primi == secondi
    assert primi is not secondi
    prima = [dict(record) for record in primi]
    salva_articoli(tmp_path / "magazzino.csv", primi)
    assert primi == prima


# ---------------------------------------------------------------------------
# JSON: serializzazione e controlli separati (cap. PY-20)
# ---------------------------------------------------------------------------


def test_json_round_trip_canonico_e_byte_del_file():
    articoli = carica_articoli(CSV_DATI / "magazzino_canonico.csv")
    testo = serializza_articoli(articoli)
    assert (JSON_DATI / "magazzino_canonico.json").read_text(encoding="utf-8") == testo + "\n"
    ricostruiti = deserializza_articoli(testo)
    assert ricostruiti == articoli
    for articolo in ricostruiti:
        assert isinstance(articolo["quantita"], int)


def test_json_sintassi_struttura_e_dominio_sono_diagnosi_distinte():
    with pytest.raises(json.JSONDecodeError):
        carica_json(JSON_DATI / "magazzino_sintassi_errata.json")
    with pytest.raises(ValueError, match="radice errata"):
        carica_json(JSON_DATI / "magazzino_struttura_errata.json")
    with pytest.raises(ValueError, match="record 2"):
        carica_json(JSON_DATI / "magazzino_domini_errati.json")
    assert issubclass(json.JSONDecodeError, ValueError)


def test_json_tipi_non_ammessi_e_campi_mancanti_o_extra():
    base = {"codice": "007", "descrizione": "Vite", "quantita": 1, "prezzo_centesimi": 2}
    for campo, valore in [
        ("quantita", True),
        ("quantita", 1.0),
        ("quantita", None),
        ("prezzo_centesimi", -1),
    ]:
        record = dict(base)
        record[campo] = valore
        with pytest.raises(ValueError, match=campo):
            deserializza_articoli(json.dumps([record]))
    mancante = dict(base)
    del mancante["prezzo_centesimi"]
    with pytest.raises(ValueError, match="mancante"):
        deserializza_articoli(json.dumps([mancante]))
    extra = dict(base)
    extra["note"] = "n"
    with pytest.raises(ValueError, match="non previsto"):
        deserializza_articoli(json.dumps([extra]))


def test_json_duplicati_di_codice_e_nomi_doppi():
    primo = {"codice": "007", "descrizione": "x", "quantita": 1, "prezzo_centesimi": 0}
    doppio = dict(primo, descrizione="y")
    with pytest.raises(ValueError, match="già presente"):
        deserializza_articoli(json.dumps([primo, doppio]))
    con_nome_doppio = (
        '[{"codice": "007", "descrizione": "x", "quantita": 1,'
        ' "quantita": 2, "prezzo_centesimi": 0}]'
    )
    assert deserializza_articoli(con_nome_doppio) == [
        {"codice": "007", "descrizione": "x", "quantita": 2, "prezzo_centesimi": 0}
    ]
    with pytest.raises(ValueError, match="nome JSON duplicato"):
        deserializza_articoli_strict(con_nome_doppio)


def test_json_nan_non_e_valore_interoperabile():
    record = {"codice": "007", "descrizione": "x", "quantita": 1, "prezzo_centesimi": 0}
    record["prezzo_centesimi"] = float("nan")
    with pytest.raises(ValueError, match="Out of range float"):
        serializza_articoli([record])


def test_json_bom_in_entrata_segnalato_dal_parser(tmp_path):
    percorso = tmp_path / "con_bom.json"
    percorso.write_bytes(b"\xef\xbb\xbf" + b"[]\n")
    with pytest.raises(json.JSONDecodeError, match="BOM"):
        carica_json(percorso)


def test_salva_json_non_modifica_la_lista_e_non_lascia_bom(tmp_path):
    articoli = [dict(RECORD_CANONICI[0]), dict(RECORD_CANONICI[1])]
    prima = [dict(record) for record in articoli]
    percorso = tmp_path / "magazzino.json"
    salva_json(percorso, articoli)
    assert articoli == prima
    assert not percorso.read_bytes().startswith(b"\xef\xbb\xbf")
    assert carica_json(percorso) == articoli


# ---------------------------------------------------------------------------
# Record binari e accesso per posizione (cap. PY-21)
# ---------------------------------------------------------------------------

BIN_DATI = DATI / "binari"
BYTE_CANONICI = bytes([0x0A, 0x00, 0xF4, 0x01, 0xFF, 0xFF])
IMMAGINI = DATI / "immagini"


def test_fixture_binaria_canonica_ha_i_byte_attesi():
    percorso = BIN_DATI / "record_canonici.bin"
    assert percorso.read_bytes() == BYTE_CANONICI
    assert percorso.read_bytes().hex(" ").upper() == "0A 00 F4 01 FF FF"
    assert len(BYTE_CANONICI) == 6
    assert (BIN_DATI / "record_vuoto.bin").read_bytes() == b""
    assert (BIN_DATI / "record_troncato.bin").read_bytes() == bytes([0x0A, 0x00, 0xF4, 0x01, 0xFF])


def test_lettura_dei_tre_record_canonici():
    percorso = BIN_DATI / "record_canonici.bin"
    assert leggi_record_due_byte(percorso, 0) == 10
    assert leggi_record_due_byte(percorso, 1) == 500
    assert leggi_record_due_byte(percorso, 2) == 65535


def test_aggiornamento_indice_1_byte_lunghezza_e_altri_record(tmp_path):
    percorso = tmp_path / "record.bin"
    percorso.write_bytes(BYTE_CANONICI)
    assert aggiorna_record_due_byte(percorso, 1, 42) is None
    assert percorso.read_bytes().hex(" ").upper() == "0A 00 2A 00 FF FF"
    assert percorso.stat().st_size == 6
    assert percorso.read_bytes()[2:4] == (42).to_bytes(2, "little")
    assert leggi_record_due_byte(percorso, 0) == 10
    assert leggi_record_due_byte(percorso, 1) == 42
    assert leggi_record_due_byte(percorso, 2) == 65535


def test_estremi_del_dominio_su_primo_e_ultimo_record(tmp_path):
    percorso = tmp_path / "record.bin"
    percorso.write_bytes(BYTE_CANONICI)
    aggiorna_record_due_byte(percorso, 0, 0)
    aggiorna_record_due_byte(percorso, 2, 65535)
    assert percorso.read_bytes().hex(" ").upper() == "00 00 F4 01 FF FF"
    aggiorna_record_due_byte(percorso, 2, 0)
    aggiorna_record_due_byte(percorso, 0, 65535)
    assert percorso.read_bytes().hex(" ").upper() == "FF FF F4 01 00 00"


def test_valore_fuori_dominio_rifiutato_prima_della_scrittura(tmp_path):
    percorso = tmp_path / "record.bin"
    percorso.write_bytes(BYTE_CANONICI)
    for valore, diagnosi in [(-1, "fuori dominio"), (65536, "fuori dominio")]:
        with pytest.raises(ValueError, match=diagnosi):
            aggiorna_record_due_byte(percorso, 1, valore)
    # un argomento di tipo sbagliato è un difetto di programmazione: TypeError
    for valore in [True, "42", 1.0, None]:
        with pytest.raises(TypeError, match="atteso un intero"):
            aggiorna_record_due_byte(percorso, 1, valore)
    assert percorso.read_bytes() == BYTE_CANONICI


def test_indice_fuori_dominio_rifiutato_in_lettura_e_scrittura(tmp_path):
    percorso = tmp_path / "record.bin"
    percorso.write_bytes(BYTE_CANONICI)
    with pytest.raises(ValueError, match="negativo"):
        leggi_record_due_byte(percorso, -1)
    with pytest.raises(ValueError, match="fuori intervallo"):
        leggi_record_due_byte(percorso, 3)
    with pytest.raises(TypeError, match="atteso un intero"):
        leggi_record_due_byte(percorso, "1")
    with pytest.raises(TypeError, match="atteso un intero"):
        aggiorna_record_due_byte(percorso, True, 42)
    with pytest.raises(ValueError, match="fuori intervallo"):
        aggiorna_record_due_byte(percorso, 3, 42)
    assert percorso.read_bytes() == BYTE_CANONICI


def test_archivio_vuoto_non_offre_alcun_record(tmp_path):
    percorso = tmp_path / "vuoto.bin"
    percorso.write_bytes(b"")
    with pytest.raises(ValueError, match="contiene 0 record"):
        leggi_record_due_byte(percorso, 0)
    with pytest.raises(ValueError, match="contiene 0 record"):
        aggiorna_record_due_byte(percorso, 0, 1)
    assert percorso.read_bytes() == b""


def test_archivio_troncato_diagnosticato_senza_zero_sintetico(tmp_path):
    percorso = BIN_DATI / "record_troncato.bin"
    with pytest.raises(ValueError, match="archivio incompleto: 5 byte"):
        leggi_record_due_byte(percorso, 0)
    with pytest.raises(ValueError, match="archivio incompleto: 5 byte"):
        aggiorna_record_due_byte(percorso, 0, 7)
    assert percorso.read_bytes() == bytes([0x0A, 0x00, 0xF4, 0x01, 0xFF])


def test_percorso_assente_propaga_file_not_found_e_non_crea_file(tmp_path):
    percorso = tmp_path / "assente.bin"
    with pytest.raises(FileNotFoundError):
        leggi_record_due_byte(percorso, 0)
    with pytest.raises(FileNotFoundError):
        aggiorna_record_due_byte(percorso, 0, 1)
    assert not percorso.exists()


def test_seek_dalle_tre_origini_e_fine_file_binaria():
    traccia = traccia_seek(BIN_DATI / "record_canonici.bin")
    assert traccia == [
        ("apertura", 0, None),
        ("seek(4) da inizio", 4, None),
        ("read(2)", 6, b"\xff\xff"),
        ("seek(-4, 1) da posizione corrente", 2, None),
        ("read(2)", 4, b"\xf4\x01"),
        ("seek(-2, 2) da fine", 4, None),
        ("read(2)", 6, b"\xff\xff"),
        ("read(2) a fine file", 6, b""),
    ]


# ---------------------------------------------------------------------------
# Immagini come file binari: intestazione BMP e filtri RGB (cap. PY-21, sez. G)
# ---------------------------------------------------------------------------


def test_intestazione_bmp_canonica_e_completezza():
    campi = intestazione_bmp(IMMAGINI / "immagine_originale.bmp")
    assert campi["firma"] == "BM"
    assert campi["dimensione_dichiarata"] == 246
    assert campi["dimensione_effettiva"] == 246
    assert campi["offset_pixel"] == 54
    assert (campi["larghezza"], campi["altezza"], campi["bit_per_pixel"]) == (8, 8, 24)
    assert campi["completo"] is True


def test_intestazione_bmp_troncata_indice_leggibile_contenuto_incompleto():
    campi = intestazione_bmp(IMMAGINI / "immagine_troncata.bmp")
    assert campi["firma"] == "BM"
    assert campi["dimensione_dichiarata"] == 246
    assert campi["dimensione_effettiva"] == 94
    assert campi["completo"] is False


def test_lettura_pixel_bgr_e_indici():
    percorso = IMMAGINI / "immagine_originale.bmp"
    assert leggi_pixel(percorso, 0) == (160, 20, 200)   # BGR: file A0 14 C8
    assert leggi_pixel(percorso, 63) == (20, 160, 200)  # ultimo pixel: file 14 A0 C8
    with pytest.raises(ValueError, match="fuori intervallo"):
        leggi_pixel(percorso, 64)
    with pytest.raises(TypeError, match="atteso un intero"):
        leggi_pixel(percorso, "0")


def test_inversione_dei_colori_byte_e_lunghezza_invariati(tmp_path):
    originale = IMMAGINI / "immagine_originale.bmp"
    invertita = tmp_path / "invertita.bmp"
    assert inverti_colori(originale, invertita) == 64
    assert leggi_pixel(invertita, 0) == (95, 235, 55)   # 255 - (160, 20, 200)
    assert invertita.stat().st_size == originale.stat().st_size
    # header e byte di sorgente invariati
    assert invertita.read_bytes()[:54] == originale.read_bytes()[:54]
    assert leggi_pixel(originale, 0) == (160, 20, 200)


def test_scambio_blu_rosso_rivela_l_ordine_bgr(tmp_path):
    scambiata = tmp_path / "scambiata.bmp"
    assert scambia_blu_rosso(IMMAGINI / "immagine_originale.bmp", scambiata) == 64
    assert leggi_pixel(scambiata, 0) == (200, 20, 160)


def test_scrittura_su_copia_di_lavoro_non_sulla_sorgente():
    with pytest.raises(ValueError, match="coincide con la sorgente"):
        inverti_colori(IMMAGINI / "immagine_originale.bmp", IMMAGINI / "immagine_originale.bmp")
    assert leggi_pixel(IMMAGINI / "immagine_originale.bmp", 0) == (160, 20, 200)
