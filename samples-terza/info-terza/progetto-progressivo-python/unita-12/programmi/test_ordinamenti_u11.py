"""Suite di verifica del confronto fra strategie di ordinamento (tappa U11).

Casi pubblici PU11-01-PU11-08 e due casi propri. Entrambe le strategie
consigliate — ordinamento per inserimento e MergeSort — sono stabili e
producono lo stesso ordine dei marcatori; `sorted` serve da riferimento.

Si esegue dalla root del progetto con:
    uv run pytest -q programmi/test_ordinamenti_u11.py
"""
from spedizione_u5 import (
    chiave_totale,
    crea_registro,
    fondi_ordinate,
    ordina_fusione,
    ordina_inserimento,
    primo_indice_per_totale,
    vista_per_codice,
    vista_per_totale,
)


def registro_ordini():
    """Registro di riferimento U10-U11, con tre totali pari a 450 centesimi."""
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
    """Codici dei record nell'ordine ricevuto."""
    codici = []
    for record in record_list:
        codici.append(record["codice"])
    return codici


def strategie(registro):
    """Le due strategie sul criterio totale_cent, più il riferimento sorted."""
    return {
        "inserimento": ordina_inserimento(registro, chiave_totale),
        "fusione": ordina_fusione(registro, chiave_totale),
        "sorted": sorted(registro, key=chiave_totale),
    }


# --- PU11-01 e PU11-02: vuoto e singolo record ---


def test_pu11_01_registro_vuoto():
    for risultato in strategie([]).values():
        assert risultato == []
    assert primo_indice_per_totale([], 450) is None
    assert primo_indice_per_totale([], 0) is None


def test_pu11_02_un_solo_record():
    registro = crea_registro(["007"], [("locale", 450)])
    risultati = strategie(registro)
    for nome, risultato in risultati.items():
        assert risultato == registro
        assert risultato is not registro, nome
    assert primo_indice_per_totale(risultati["fusione"], 450) == 0
    assert primo_indice_per_totale(risultati["fusione"], 100) is None


# --- PU11-03 e PU11-04: parità con marcatori e ordine inverso ---


def test_pu11_03_parita_con_marcatori_osservabili():
    registro = registro_ordini()
    risultati = strategie(registro)
    atteso = ["003", "007", "012", "011", "009"]
    # Le due strategie stabili e sorted concordano sull'ordine dei marcatori.
    assert codici_nell_ordine(risultati["inserimento"]) == atteso
    assert codici_nell_ordine(risultati["fusione"]) == atteso
    assert codici_nell_ordine(risultati["sorted"]) == atteso


def test_pu11_04_ordine_inverso_sul_criterio():
    codici = ["001", "002", "003", "004"]
    preventivi = [("locale", 400), ("nazionale", 300), ("locale", 200), ("nazionale", 100)]
    registro = crea_registro(codici, preventivi)
    atteso = ["004", "003", "002", "001"]
    for risultato in strategie(registro).values():
        assert codici_nell_ordine(risultato) == atteso


# --- PU11-05: più interrogazioni sullo stesso catalogo ordinato ---


def test_pu11_05_interrogazioni_sul_catalogo_ordinato():
    registro = registro_ordini()
    vista = vista_per_totale(registro)
    # Primo indice anche con duplicati: il primo dei tre record da 450 è 007.
    assert primo_indice_per_totale(vista, 450) == 1
    assert vista[1]["codice"] == "007"
    assert primo_indice_per_totale(vista, 200) == 0
    assert primo_indice_per_totale(vista, 1200) == 4
    assert primo_indice_per_totale(vista, 999) is None

    # La somma dei costi delle query è separata dal costo di preparazione:
    # qui si verifica che le ripetizioni siano indipendenti e riproducibili.
    primi = []
    for totale_cent in (200, 450, 450, 1200):
        primi.append(primo_indice_per_totale(vista, totale_cent))
    secondi = []
    for totale_cent in (200, 450, 450, 1200):
        secondi.append(primo_indice_per_totale(vista, totale_cent))
    assert primi == secondi == [0, 1, 1, 4]


# --- PU11-06: record aggiunto o modificato dopo la vista ---


def test_pu11_06_vista_non_si_aggiorna_da_sola():
    registro = registro_ordini()
    vista = vista_per_totale(registro)

    registro.append({"codice": "020", "destinazione": "locale", "totale_cent": 100})
    assert len(vista) == 5
    assert primo_indice_per_totale(vista, 100) is None

    # La mutazione di un record condiviso si vede nella vista — gli oggetti
    # sono gli stessi — ma ne invalida l'ordinamento: nessuna ricerca sulla
    # vista è più garantita finché non viene ricostruita.
    registro[0]["totale_cent"] = 999
    assert vista[1]["codice"] == "007"
    assert vista[1]["totale_cent"] == 999

    ricostruita = vista_per_totale(registro)
    assert ricostruita[0]["codice"] == "020"
    assert primo_indice_per_totale(ricostruita, 450) == 2
    assert ricostruita[2]["codice"] == "012"


# --- PU11-07 e PU11-08: zeri iniziali e confronto con sorted ---


def test_pu11_07_codici_007_e_7_distinti():
    registro = crea_registro(["7", "007"], [("locale", 100), ("nazionale", 200)])
    vista = vista_per_codice(registro)
    # Ordine lessicografico: "007" precede "7".
    assert codici_nell_ordine(vista) == ["007", "7"]
    assert vista[0]["totale_cent"] == 200
    assert vista[1]["totale_cent"] == 100


def test_pu11_08_confronto_con_sorted():
    registro = registro_ordini()
    risultati = strategie(registro)
    assert risultati["inserimento"] == risultati["sorted"]
    assert risultati["fusione"] == risultati["sorted"]
    # `sorted` è un riferimento per il risultato: le funzioni richieste
    # implementano il proprio procedimento e non delegano a `sorted`.
    assert ordina_fusione is not sorted


# --- Casi propri motivati ---


def test_proprio_1_fusione_stabile_e_indipendente():
    """PR-1: la fusione preserva l'ordine dei duplicati e non muta gli input.

    Discrimina una fusione che a parità di chiave prenda dalla destra.
    """
    prima = crea_registro(["001", "003"], [("locale", 100), ("locale", 100)])
    seconda = crea_registro(["002", "004"], [("locale", 100), ("locale", 100)])
    fusa = fondi_ordinate(prima, seconda, chiave_totale)
    assert codici_nell_ordine(fusa) == ["001", "003", "002", "004"]
    assert codici_nell_ordine(prima) == ["001", "003"]
    assert codici_nell_ordine(seconda) == ["002", "004"]


def test_proprio_2_primo_indice_su_totali_tutti_uguali():
    """PR-2: con tutti i totali uguali il primo indice è 0 e l'ultimo è n-1.

    Discrimina una ricerca che restituisce un indice qualsiasi invece del primo.
    """
    codici = ["001", "002", "003", "004"]
    preventivi = [("locale", 100), ("nazionale", 100), ("locale", 100), ("nazionale", 100)]
    vista = vista_per_totale(crea_registro(codici, preventivi))
    assert primo_indice_per_totale(vista, 100) == 0
    assert primo_indice_per_totale(vista, 0) is None
    assert primo_indice_per_totale(vista, 200) is None
