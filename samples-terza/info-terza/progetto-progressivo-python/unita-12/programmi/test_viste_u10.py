"""Suite di verifica delle viste ordinate (tappa U10).

Casi pubblici PU10-01-PU10-08 e due casi propri. Dataset di riferimento:
record con codici ["007", "009", "012", "003", "011"], totali in centesimi
450, 1200, 450, 200, 450 — tre record con lo stesso totale sono deliberati,
perché la stabilità si osserva solo sui duplicati.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_viste_u10.py
"""
from spedizione_u5 import (
    cerca_per_codice,
    chiave_codice,
    chiave_totale,
    crea_registro,
    vista_per_codice,
    vista_per_totale,
)


def registro_ordini():
    """Registro di riferimento U10, con tre totali pari a 450 centesimi."""
    codici = ["007", "009", "012", "003", "011"]
    preventivi = [
        ("locale", 450),
        ("nazionale", 1200),
        ("locale", 450),
        ("nazionale", 200),
        ("locale", 450),
    ]
    return crea_registro(codici, preventivi)


def codici_nell_ordine(record_list):
    """Restituisce i codici dei record nell'ordine ricevuto."""
    codici = []
    for record in record_list:
        codici.append(record["codice"])
    return codici


# --- PU10-01 e PU10-02: vuoto e singolo record ---


def test_pu10_01_registro_vuoto():
    vista_codice = vista_per_codice([])
    vista_totale = vista_per_totale([])
    assert vista_codice == []
    assert vista_totale == []
    assert cerca_per_codice(vista_codice, "007") is None


def test_pu10_02_un_solo_record():
    registro = crea_registro(["007"], [("locale", 450)])
    vista_codice = vista_per_codice(registro)
    assert vista_codice == registro
    assert vista_codice is not registro
    assert vista_codice[0] is registro[0]
    assert cerca_per_codice(vista_codice, "007") is registro[0]
    assert cerca_per_codice(vista_codice, "008") is None


# --- PU10-03 e PU10-04: ordine dei codici e ricerca ---


def test_pu10_03_codici_in_ingresso_invertito():
    registro = crea_registro(["009", "007"], [("nazionale", 900), ("locale", 300)])
    vista_codice = vista_per_codice(registro)
    assert codici_nell_ordine(vista_codice) == ["007", "009"]
    assert cerca_per_codice(vista_codice, "007")["totale_cent"] == 300
    assert cerca_per_codice(vista_codice, "7") is None


def test_pu10_04_primo_ultimo_e_assente():
    registro = registro_ordini()
    vista_codice = vista_per_codice(registro)
    assert codici_nell_ordine(vista_codice) == ["003", "007", "009", "011", "012"]

    assert cerca_per_codice(vista_codice, "003")["totale_cent"] == 200
    assert cerca_per_codice(vista_codice, "012")["totale_cent"] == 450
    assert cerca_per_codice(vista_codice, "010") is None

    # La ricerca non modifica la vista.
    assert codici_nell_ordine(vista_codice) == ["003", "007", "009", "011", "012"]


# --- PU10-05 e PU10-06: stabilità e associazione dei campi ---


def test_pu10_05_totali_uguali_stabili_e_codici_ordinati():
    registro = registro_ordini()
    vista_totale = vista_per_totale(registro)
    # I tre record con 450 centesimi — 007, 012, 011 — conservano l'ordine
    # relativo di ingresso: l'ordinamento per totale è stabile.
    assert codici_nell_ordine(vista_totale) == ["003", "007", "012", "011", "009"]

    vista_codice = vista_per_codice(registro)
    assert codici_nell_ordine(vista_codice) == ["003", "007", "009", "011", "012"]


def test_pu10_06_campi_associati_al_proprio_record():
    registro = registro_ordini()
    vista_totale = vista_per_totale(registro)
    # Ogni record della vista conserva tutti i campi del record di origine:
    # nessuna lista parallela e nessun campo perso o riassociato.
    for record in vista_totale:
        originale = None
        for candidato in registro:
            if candidato["codice"] == record["codice"]:
                originale = candidato
        assert record == originale
        assert record is originale


# --- PU10-07 e PU10-08: invarianza della sorgente e viste non aggiornate ---


def test_pu10_07_lista_originale_invariata():
    registro = registro_ordini()
    codici_prima = codici_nell_ordine(registro)
    identita_lista = id(registro)

    vista_per_codice(registro)
    vista_per_totale(registro)

    assert id(registro) == identita_lista
    assert codici_nell_ordine(registro) == codici_prima
    assert registro[0]["totale_cent"] == 450
    assert registro[3]["totale_cent"] == 200


def test_pu10_08_record_aggiunto_alla_sorgente_dopo_la_vista():
    registro = registro_ordini()
    vista_codice = vista_per_codice(registro)

    registro.append({"codice": "020", "destinazione": "locale", "totale_cent": 100})

    # La vista NON si aggiorna: è stata costruita prima.
    assert len(vista_codice) == 5
    assert cerca_per_codice(vista_codice, "020") is None
    # La sorgente, invece, contiene il nuovo record.
    assert len(registro) == 6

    # Un record condiviso è lo stesso oggetto: la mutazione di un campo si vede
    # sia nella sorgente sia nella vista, anche se può invalidarne l'ordinamento.
    registro[0]["totale_cent"] = 1
    assert registro[0]["codice"] == "007"
    assert cerca_per_codice(vista_codice, "007")["totale_cent"] == 1
    assert len(vista_codice) == 5


# --- Confronto con sorted come oracolo ---


def test_oracolo_sorted_sugli_stessi_criteri():
    registro = registro_ordini()
    assert codici_nell_ordine(vista_per_codice(registro)) == codici_nell_ordine(
        sorted(registro, key=chiave_codice)
    )
    assert codici_nell_ordine(vista_per_totale(registro)) == codici_nell_ordine(
        sorted(registro, key=chiave_totale)
    )


# --- Casi propri motivati ---


def test_proprio_1_tutti_i_totali_uguali():
    """PR-1: con chiavi tutte uguali la vista per totale è l'ordine di ingresso.

    Discrimina un ordinamento instabile: qualunque riordino dei marcatori
    sarebbe visibile.
    """
    registro = crea_registro(
        ["A1", "A2", "A3", "A4"],
        [("locale", 100), ("nazionale", 100), ("locale", 100), ("nazionale", 100)],
    )
    vista_totale = vista_per_totale(registro)
    assert codici_nell_ordine(vista_totale) == ["A1", "A2", "A3", "A4"]


def test_proprio_2_mutazione_del_record_condiviso():
    """PR-2: la mutazione di un campo si vede nella vista, l'ordine no.

    Dopo la mutazione la precondizione della ricerca dicotomica non è più
    garantita: la vista va ricostruita prima di usarla.
    """
    registro = crea_registro(
        ["B1", "B2"], [("locale", 100), ("nazionale", 200)]
    )
    vista_totale = vista_per_totale(registro)
    assert codici_nell_ordine(vista_totale) == ["B1", "B2"]

    registro[0]["totale_cent"] = 999
    assert vista_totale[0]["totale_cent"] == 999
    # La vista ricostruita riprende la precondizione dell'ordinamento.
    ricostruita = vista_per_totale(registro)
    assert codici_nell_ordine(ricostruita) == ["B2", "B1"]
    assert codici_nell_ordine(vista_totale) == ["B1", "B2"]
