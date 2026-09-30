"""Suite di verifica dei sorgenti d'esempio dell'Unità 12 (blocco moduli, byte, eccezioni, date).

I test controllano gli attesi dichiarati nei capitoli PY-16, PY-17 e PY-18 e le
proprietà dei moduli `utilita_u12`, `demo_import_u12`, `codifiche_u12` ed
`eccezioni_date_u12`: valore dell'inventario, assenza di effetti all'import,
conti separati di punti di codice e byte, comportamento del BOM con i due
codec, controlli separati di conversione e dominio, `else`/`finally`, date con
riferimenti fissi e fixture di testo e immagini nella cartella `dati/`.

Esecuzione dalla cartella `unita-12/`:

    uv run --python 3.14 --with pytest python -m pytest esempi/test_esempi_u12.py -q

La suite è deterministica: usa dati espliciti e riferimenti di data fissi,
mai `date.today()` né durate reali.
"""

import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

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
    with pytest.raises(TypeError):
        valida_quantita(None)


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
