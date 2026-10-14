"""Casi pubblici del laboratorio LAB-PY-U19 — ricerca e dossier comparativo.

I casi LAB19-01…LAB19-14 verificano rappresentazione, ricerca guidata,
simulazioni, record e confronto. I casi 01–05 e 12–13 richiedono `cerca` e
`contiene` completati nella fase L2 e falliscono all'inizio con
`NotImplementedError`; i casi 06–11 usano rappresentazione, modifiche e
controllo forniti; il caso 14 richiede inoltre `dossier_scelta` della fase
L6. I casi 08–11 accettano tracce e verifica degli stati, coerentemente con
il livello comune. Esecuzione dalla cartella `unita-19`:

```powershell
uv run pytest -q laboratorio/test_pubblici.py
```
"""

import pytest

from confronto_starter import dossier_scelta, esegui_confronto, salva_csv
from dati_catalogo import coppie_indice, query_laboratorio
from ricerca_btree_starter import (
    BTreeDidattico,
    NodoBTree,
    costruisci_d1,
    costruisci_d2,
    costruisci_d4,
    costruisci_d5,
    costruisci_fusione_radice,
    costruisci_prestito_destro,
    costruisci_prestito_sinistro,
    fixture_foglie_diverse,
    fixture_limite_antentato,
)


def test_lab19_01_vuoto():
    """B-tree vuoto: `len` 0, altezza -1, `contiene` `False`, `cerca` con `KeyError`."""
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    assert len(albero) == 0
    assert albero.altezza() == -1
    assert albero.contiene(1) is False
    with pytest.raises(KeyError):
        albero.cerca(1)


def test_lab19_02_radice_foglia():
    """Radice foglia: prima e ultima chiave trovate, assenze ai due lati."""
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    albero.inserisci(10, "dato-10")
    assert albero.altezza() == 0
    assert albero.cerca(10) == "dato-10"
    assert albero.contiene(4) is False
    assert albero.contiene(40) is False
    prima = NodoBTree([(1, "a")], [])
    seconda = NodoBTree([(1, "a")], [])
    prima.voci.append((2, "b"))
    assert seconda.chiavi() == [1]


def test_lab19_03_voce_interna():
    """Query `20` su D1 restituisce il dato con un solo nodo visitato."""
    albero = costruisci_d1()
    assert albero.cerca(20) == "dato-20"
    strumento = albero.ricerca_con_conteggi(20)
    assert strumento["trovato"] is True
    assert strumento["nodi"] == 1


def test_lab19_04_foglia_e_intervallo():
    """Query `17` riuscita e `15` assente sullo stesso percorso di D1."""
    albero = costruisci_d1()
    assert albero.cerca(17) == "dato-17"
    with pytest.raises(KeyError):
        albero.cerca(15)
    assert albero.ricerca_con_conteggi(17)["nodi"] == 2
    assert albero.ricerca_con_conteggi(15)["nodi"] == 2


def test_lab19_05_dati_falsy():
    """`None`, `0` e stringa vuota sono dati validi, distinti dall'assenza."""
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    albero.inserisci(1, None)
    albero.inserisci(2, 0)
    albero.inserisci(3, "")
    assert albero.cerca(1) is None
    assert albero.cerca(2) == 0
    assert albero.cerca(3) == ""
    assert albero.contiene(1) is True
    with pytest.raises(KeyError):
        albero.cerca(9)


def test_lab19_06_invarianti_globali():
    """Fixture fuori dal limite di un antenato diagnosticata dal controllo."""
    with pytest.raises(AssertionError, match="antenato"):
        fixture_limite_antentato().controlla_invarianti()


def test_lab19_07_occupazione_e_profondita():
    """Due difetti indipendenti rilevati, con vincolo nominato."""
    with pytest.raises(AssertionError, match="profondità"):
        fixture_foglie_diverse().controlla_invarianti()
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=int)
    albero.radice = NodoBTree(
        [(10, "dato-10")], [NodoBTree([(5, "dato-5")], []), NodoBTree([], [])]
    )
    albero.dimensione = 2
    with pytest.raises(AssertionError, match="voci"):
        albero.controlla_invarianti()


def test_lab19_08_split_propagato():
    """D2 fino a `10`: dimensione 10, altezza 2 e figli attesi."""
    albero = costruisci_d2()
    albero.controlla_invarianti()
    assert len(albero) == 10
    assert albero.altezza() == 2
    assert albero.radice.chiavi() == [4]
    assert albero.radice.figli[0].chiavi() == [2]
    assert albero.radice.figli[1].chiavi() == [6, 8]


def test_lab19_09_redistribuzione():
    """D3b e D3c mantengono associazioni e occupazione dopo il prestito."""
    destro = costruisci_prestito_destro()
    destro.rimuovi(5)
    destro.controlla_invarianti()
    assert destro.radice.chiavi() == [25]
    assert destro.radice.figli[0].chiavi() == [20]
    assert destro.radice.figli[1].chiavi() == [30]
    sinistro = costruisci_prestito_sinistro()
    sinistro.rimuovi(25)
    sinistro.controlla_invarianti()
    assert sinistro.radice.chiavi() == [10]
    assert sinistro.radice.figli[0].chiavi() == [5]
    assert sinistro.radice.figli[1].chiavi() == [20]


def test_lab19_10_fusione_e_radice():
    """D3e e D4: stato e altezza finali corretti dopo fusione."""
    fusione = costruisci_fusione_radice()
    fusione.rimuovi(5)
    fusione.controlla_invarianti()
    assert fusione.radice.chiavi() == [10, 15]
    assert fusione.altezza() == 0
    propagata = costruisci_d4()
    propagata.rimuovi(10)
    propagata.controlla_invarianti()
    assert propagata.radice.chiavi() == [40, 60]
    assert propagata.altezza() == 1
    assert len(propagata) == 6


def test_lab19_11_figli_trasferiti():
    """D5 include il figlio `[35]` nel nuovo intervallo dopo il prestito."""
    albero = costruisci_d5()
    albero.rimuovi(50)
    albero.controlla_invarianti()
    assert albero.radice.chiavi() == [30]
    destro = albero.radice.figli[1]
    assert destro.chiavi() == [40]
    assert destro.figli[0].chiavi() == [35]
    assert destro.figli[1].chiavi() == [60, 70]


def test_lab19_12_record_e_unicita():
    """D6: `007` e `7` distinti, duplicato rifiutato, sorgente invariata."""
    coppie = coppie_indice()
    originali = list(coppie)
    albero = BTreeDidattico(grado_minimo=2, tipo_chiave=str)
    for chiave, dato in coppie:
        albero.inserisci(chiave, dato)
    albero.controlla_invarianti()
    assert albero.cerca("007") == ("007", "cavetto USB", 4)
    assert albero.cerca("007") != albero.cerca("7")
    with pytest.raises(ValueError):
        albero.inserisci("007", ("007", "duplicato", 1))
    assert len(albero) == 8
    assert coppie == originali


def test_lab19_13_risultati_equivalenti():
    """Query esatte e assenze coincidono fra lista, B-tree e `dict`."""
    esito = esegui_confronto()
    assert esito["coerente"] is True
    interrogazioni = query_laboratorio()
    assert len(esito["righe"]) == 3 * (
        len(interrogazioni["riuscite"]) + len(interrogazioni["fallite"])
    )


def test_lab19_14_costi_e_dossier(tmp_path):
    """CSV con colonne fissate e dossier con decisione motivata."""
    esito = esegui_confronto()
    percorso = tmp_path / "confronto.csv"
    salva_csv(esito["righe"], str(percorso))
    contenuto = percorso.read_text(encoding="utf-8").splitlines()
    assert contenuto[0] == "struttura,query,esito,metrica"
    assert any("nodi=" in riga and "confronti=" in riga for riga in contenuto[1:])
    dossier = dossier_scelta(
        {
            "nome": "consultazioni",
            "operazioni": ["cerca"],
            "frequenza": "alta",
            "organizzazione": "codici sparsi",
        }
    )
    for sezione in ("requisiti", "ipotesi", "evidenze", "decisione", "alternativa", "limite"):
        assert sezione in dossier
