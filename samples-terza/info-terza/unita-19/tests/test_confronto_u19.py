"""Prove del confronto fra strutture — Unità 19."""

from confronto_strutture_u19 import (
    ADATTATORI,
    esegui_confronto,
    genera_interi,
    misura_tempi,
    query_campione,
    salva_csv,
)


def test_stessi_dati_stesse_query():
    """Tutti gli adattatori rispondono con gli stessi esiti alle stesse query."""
    voci = genera_interi(30, famiglia="mescolati")
    campione = query_campione(voci)
    esito = esegui_confronto(voci, campione["riuscite"] + campione["fallite"])
    assert esito["coerente"] is True
    assert esito["preparazione"] == [costruttore.nome for costruttore in ADATTATORI]


def test_famiglie_riproducibili():
    """Le tre famiglie generano gli stessi insiemi con copie indipendenti."""
    for famiglia in ("crescenti", "inversi", "mescolati"):
        prima = genera_interi(20, famiglia=famiglia)
        seconda = genera_interi(20, famiglia=famiglia)
        assert sorted(prima) == sorted(seconda)
        assert prima is not seconda


def test_bst_catena_e_btree():
    """Con inserimenti crescenti il BST degenera mentre il B-tree resta basso."""
    from confronto_strutture_u19 import AdattatoreBST, AdattatoreBTree

    voci = genera_interi(10, famiglia="crescenti")
    catena = AdattatoreBST(voci)
    basso = AdattatoreBTree(voci)
    catena.cerca(10)
    basso.cerca(10)
    assert catena.ultimi_nodi == 10
    assert basso.ultimo_esito.nodi == 3


def test_tempi_con_regione_dichiarata(tmp_path):
    """Le misure temporali coprono le cinque strutture senza stampe interne."""
    voci = genera_interi(30, famiglia="crescenti")
    tempi = misura_tempi(voci, [1, 15, 30, 0, 31], ripetizioni=2)
    assert set(tempi) == {costruttore.nome for costruttore in ADATTATORI}
    assert all(secondi >= 0 for secondi in tempi.values())


def test_csv_con_colonne(tmp_path):
    """Il CSV conserva colonne, modello e risultati del confronto."""
    voci = genera_interi(10, famiglia="crescenti")
    esito = esegui_confronto(voci, [1, 10, 0, 11])
    percorso = tmp_path / "confronto.csv"
    salva_csv(esito["righe"], str(percorso))
    righe = percorso.read_text(encoding="utf-8").splitlines()
    assert righe[0] == "struttura,query,atteso,esito,metrica,coerente"
    assert len(righe) == 1 + len(ADATTATORI) * 4
