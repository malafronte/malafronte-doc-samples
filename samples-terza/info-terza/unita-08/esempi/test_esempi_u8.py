"""Suite di verifica dei sorgenti d'esempio dell'Unità 8.

Verifica i contratti della §6 del piano di lavoro e i casi discriminanti della
verifica semantica: viste contro fotografie, ordine, ritorni ed effetti,
hashability, insiemi, record, pattern, frequenze e Fibonacci.

Esecuzione dalla cartella `esempi/`:

    uv run pytest -q test_esempi_u8.py

Gli insiemi si confrontano come insiemi; per le stampe riproducibili si usa
`sorted` solo su elementi confrontabili, senza pretendere una rappresentazione
testuale fissa di un insieme non ordinato.
"""

import pytest

import deduplicazione_raggruppamenti_u8 as dedup
import fibonacci_memoria_u8 as fib
import frequenze_u8 as freq
import operazioni_collezioni_u8 as ops
import record_catalogo_u8 as rec


# --- Dizionari: accesso, presenza, effetti ---------------------------------


def test_chiave_e_valore_distinti():
    assert ops.prova_chiave_e_valore() == (True, False)


def test_aggiornamento_non_cambia_len():
    lunghezza, chiavi = ops.prova_aggiornamento_e_ordine()
    assert lunghezza == 2
    assert chiavi == ["R10", "L05"]


def test_zero_e_un_valore_lecito():
    lunghezza, presente, valore = ops.prova_zero_lecito()
    assert lunghezza == 3
    assert presente is True
    assert valore == 0


def test_get_non_inserisce():
    risultato, chiave_presente = ops.prova_get_con_default()
    assert risultato == 0
    assert chiave_presente is False


def test_setdefault_non_sovrascrive():
    ritorno_prima, valore_finale, len_finale = ops.prova_setdefault_su_presente()
    assert ritorno_prima == 0
    assert valore_finale == 0
    assert len_finale == 3


def test_setdefault_su_assente_inserisce():
    ritorno, dizionario = ops.prova_setdefault_su_assente()
    assert ritorno == 9
    assert dizionario["C20"] == 9


def test_popitem_toglie_ultima_inserita():
    coppia, chiavi_rimanenti = ops.prova_popitem_ultima_inserita()
    assert coppia == ("C20", 0)
    assert chiavi_rimanenti == ["R10", "L05"]


def test_cancellazione_e_reinserimento_spostano_la_chiave():
    assert ops.prova_cancella_e_reinserisci() == ["L05", "R10"]


def test_none_non_e_assenza():
    assert ops.prova_none_non_e_assenza() == (True, True, True, False)


def test_vista_dinamica_contro_fotografia():
    vista, fotografia = ops.prova_vista_e_fotografia()
    assert len(vista) == 3
    assert len(fotografia) == 2


def test_copia_superficiale_condivide_gli_elementi():
    registro_dopo_append, copia_dopo_append, registro_dopo, copia_dopo = (
        ops.prova_copia_superficiale()
    )
    assert registro_dopo_append == [20, 21, 22]
    assert copia_dopo_append == [20, 21, 22]
    assert registro_dopo == [20, 21, 22]
    assert copia_dopo == [99]


def test_ritorno_di_update_e_clear():
    ritorno_u, stato_u = ops.prova_ritorno_di_update()
    assert ritorno_u is True
    assert stato_u == {"R10": 15, "L05": 4, "C20": 0}
    ritorno_c, stato_c = ops.prova_ritorno_di_clear()
    assert ritorno_c is True
    assert stato_c == {}


def test_pop_con_e_senza_default():
    tolto, sostitutivo, len_finale = ops.prova_pop_con_default()
    assert tolto == 12
    assert sostitutivo == 0
    assert len_finale == 1


# --- Hashability ------------------------------------------------------------


def test_chiavi_ammesse():
    chiavi = ops.prova_chiavi_ammesse()
    assert chiavi == {"testo": 1, 7: 2, (1, 2): 3}
    assert chiavi[(1, 2)] == 3


@pytest.mark.parametrize(
    "demo",
    [
        ops.demo_errore_accesso_assente,
        ops.demo_errore_pop_senza_default,
        ops.demo_errore_popitem_vuoto,
    ],
)
def test_errori_sulle_chiavi_e_sul_vuoto(demo):
    with pytest.raises(KeyError):
        demo()


@pytest.mark.parametrize(
    "demo",
    [ops.demo_errore_chiave_lista, ops.demo_errore_chiave_tupla_con_lista],
)
def test_type_error_su_chiavi_non_hashable(demo):
    with pytest.raises(TypeError):
        demo()


# --- Insiemi ---------------------------------------------------------------


def test_prodotti_fra_insiemi():
    prodotti = ops.prova_prodotti_fra_insiemi()
    assert prodotti["unione"] == {"A", "B", "C", "D"}
    assert prodotti["intersezione"] == {"B"}
    assert prodotti["differenza_a_meno_b"] == {"A", "C"}
    assert prodotti["differenza_b_meno_a"] == {"D"}
    assert prodotti["differenza_simmetrica"] == {"A", "C", "D"}


def test_confronti_fra_insiemi():
    assert ops.prova_confronti_fra_insiemi() == (True, False, True, True)


def test_operatori_e_metodi_coincidono():
    insieme, per_metodo, coincidono = ops.prova_operatori_e_metodi()
    assert insieme == per_metodo
    assert coincidono is True


def test_aggiornamenti_in_posto():
    con_add, con_update, con_difference = ops.prova_aggiornamenti_in_posto()
    assert con_add == {"A", "AB", "B", "C"}
    assert con_update == {"A", "B"}
    assert con_difference == {"A", "B"}


def test_remove_e_discard():
    insieme, assente_ancora_assente = ops.prova_remove_e_discard()
    assert insieme == {"B"}
    assert assente_ancora_assente is False


def test_pop_insieme_senza_fissare_elemento():
    era_presente, ora_assente, diminuzione = ops.prova_pop_insieme()
    assert era_presente is True
    assert ora_assente is True
    assert diminuzione == 1


def test_insieme_vuoto_e_duplicati():
    cardinalita, distinti, lista_invariata = ops.prova_insieme_vuoto_e_duplicati()
    assert cardinalita == 0
    assert distinti == {3, 1, 2}
    assert lista_invariata == [3, 1, 3, 2, 1]


@pytest.mark.parametrize(
    "demo",
    [
        ops.demo_errore_remove_assente,
        ops.demo_errore_pop_insieme_vuoto,
        ops.demo_errore_indice_insieme,
    ],
)
def test_errori_degli_insiemi(demo):
    with pytest.raises((KeyError, TypeError)):
        demo()


# --- Deduplicazione e raggruppamento ---------------------------------------


@pytest.mark.parametrize(
    "valori, atteso",
    [
        ([], []),
        ([3, 1, 3, 2, 1], [3, 1, 2]),
        ([7, 7], [7]),
        ([0, -1, 0], [0, -1]),
    ],
)
def test_unici_in_ordine(valori, atteso):
    copia = valori.copy()
    assert dedup.unici_in_ordine(valori) == atteso
    assert valori == copia


def test_unici_ultime_occorrenze_dichiara_il_contratto():
    assert dedup.unici_ultime_occorrenze([3, 1, 3, 2, 1]) == [3, 2, 1]


def test_raggruppa_codici():
    voci = list(dedup.VOCI_CANONICHE)
    assert dedup.raggruppa_codici(voci) == {
        "elettronica": ["R10", "L05"],
        "meccanica": ["007"],
    }
    assert dedup.raggruppa_codici([]) == {}
    assert dedup.raggruppa_codici([("a", "1"), ("a", "1")]) == {"a": ["1", "1"]}


def test_gruppi_indipendenti():
    risultato = dedup.raggruppa_codici(list(dedup.VOCI_CANONICHE))
    assert risultato["elettronica"] is not risultato["meccanica"]
    risultato["elettronica"].append("X99")
    assert risultato["meccanica"] == ["007"]


def test_controsesempio_liste_condivise():
    gruppi = dedup.controsesempio_liste_condivise(["elettronica", "meccanica"])
    assert gruppi["elettronica"] is gruppi["meccanica"]


# --- Riconoscimento e validazione ------------------------------------------


@pytest.mark.parametrize(
    "dato, atteso",
    [
        ({"sensore": "S1", "valore": 2150}, "valida"),
        ({"valore": 2150, "sensore": "S1"}, "valida"),
        ({"sensore": "S1", "valore": 2150, "istante_ms": 0}, "valida"),
        ({"sensore": "S1", "valore": -4000}, "valida"),
        ({"sensore": "S1", "valore": 12500}, "valida"),
        ({"sensore": 2150, "valore": "S1"}, "valori non validi"),
        ({"sensore": "S1", "valore": "2150"}, "valori non validi"),
        ({"sensore": "S1", "valore": 12501}, "valori non validi"),
        ({"sensore": "S1", "valore": True}, "valori non validi"),
        ({"sensore": "", "valore": 2150}, "valori non validi"),
        ({"sensore": "S1"}, "struttura non riconosciuta"),
        ({}, "struttura non riconosciuta"),
        (["S1", 2150], "struttura non riconosciuta"),
    ],
)
def test_esito_misura(dato, atteso):
    assert dedup.esito_misura(dato) == atteso


# --- Record e catalogo -----------------------------------------------------


def test_crea_articoli_canonico():
    articoli = rec.crea_articoli(
        rec.CODICI_CANONICI, rec.DESCRIZIONI_CANONICHE, rec.QUANTITA_CANONICHE
    )
    assert articoli == [
        {"codice": "R10", "descrizione": "Resistore", "quantita": 12},
        {"codice": "007", "descrizione": "Vite, lunga", "quantita": 4},
        {"codice": "L05", "descrizione": "LED", "quantita": 8},
    ]


def test_crea_articoli_rifiuta_senza_risultato_parziale():
    assert rec.crea_articoli(["R10", "R10"], ["A", "B"], [1, 2]) is None
    assert rec.crea_articoli(["R10", "007"], ["A"], [1, 2]) is None
    assert rec.crea_articoli([], [], []) == []


def test_codice_007_distinto_da_7():
    articoli = rec.crea_articoli(["007", "7"], ["Vite", "Sette"], [1, 2])
    assert rec.cerca_indice_articolo(articoli, "007") == 0
    assert rec.cerca_indice_articolo(articoli, "7") == 1


def test_ricerca_assente_restituisce_none():
    articoli = rec.crea_articoli(
        rec.CODICI_CANONICI, rec.DESCRIZIONI_CANONICHE, rec.QUANTITA_CANONICHE
    )
    assert rec.cerca_indice_articolo(articoli, "X99") is None
    assert rec.cerca_indice_articolo(articoli, "R10") == 0


def test_imposta_quantita_atomica():
    articoli = rec.crea_articoli(
        rec.CODICI_CANONICI, rec.DESCRIZIONI_CANONICHE, rec.QUANTITA_CANONICHE
    )
    assert rec.imposta_quantita(articoli, "007", 0) is True
    assert articoli[1]["quantita"] == 0
    stato = [dict(a) for a in articoli]
    assert rec.imposta_quantita(articoli, "007", -1) is False
    assert articoli == stato


def test_inserisci_non_sovrascrive():
    articoli = rec.crea_articoli(
        rec.CODICI_CANONICI, rec.DESCRIZIONI_CANONICHE, rec.QUANTITA_CANONICHE
    )
    assert rec.inserisci_articolo(articoli, "007", "Vite", 1) is False
    assert len(articoli) == 3
    assert rec.inserisci_articolo(articoli, "C20", "Condensatore", 5) is True
    assert articoli[-1]["codice"] == "C20"


def test_elimina_articolo():
    articoli = rec.crea_articoli(
        rec.CODICI_CANONICI, rec.DESCRIZIONI_CANONICHE, rec.QUANTITA_CANONICHE
    )
    assert rec.elimina_articolo(articoli, "X99") is False
    assert len(articoli) == 3
    assert rec.elimina_articolo(articoli, "R10") is True
    assert [a["codice"] for a in articoli] == ["007", "L05"]


def test_ordinamento_con_parita_e_record_condivisi():
    articoli = rec.crea_articoli(
        rec.CODICI_CANONICI, rec.DESCRIZIONI_CANONICHE, rec.QUANTITA_CANONICHE
    )
    originali = [dict(a) for a in articoli]
    ordinati = rec.ordina_articoli(articoli)
    assert [a["codice"] for a in ordinati] == ["L05", "R10", "007"]
    assert [a["quantita"] for a in ordinati] == [8, 12, 4]
    assert articoli == originali
    assert ordinati[0] is articoli[2]
    assert [a["codice"] for a in rec.ordina_articoli_lambda(articoli)] == [
        "L05",
        "R10",
        "007",
    ]


def test_controsesempio_ordinamento_delle_sole_descrizioni():
    assert rec.controsesempio_ordina_descrizioni(
        ["Resistore", "Vite, lunga", "LED"]
    ) == ["LED", "Resistore", "Vite, lunga"]


# --- Frequenze e presentazione ---------------------------------------------


def test_frequenze_canoniche():
    atteso = {"sole": 3, "luna": 2, "mare": 1}
    assert freq.conta_parole(freq.TESTO_CANONICO) == atteso
    assert freq.conta_parole_con_get(freq.TESTO_CANONICO) == atteso
    assert sum(atteso.values()) == 6
    assert len(atteso) == 3


@pytest.mark.parametrize(
    "testo",
    ["", "   \n\t ", "sole sole, SOLE", "è è", "Sole luna mare LUNA sole"],
)
def test_le_due_versioni_coincidono(testo):
    assert freq.conta_parole(testo) == freq.conta_parole_con_get(testo)


def test_punteggiatura_e_accenti():
    assert freq.conta_parole("sole sole, SOLE") == {"sole": 2, "sole,": 1}
    assert freq.conta_parole("è è") == {"è": 2}


def test_doppio_ordinamento_con_parita():
    frequenze = freq.conta_parole("Sole luna mare LUNA sole")
    assert sorted(frequenze.items(), key=freq.chiave_crescente) == [
        ("mare", 1),
        ("luna", 2),
        ("sole", 2),
    ]
    assert sorted(frequenze.items(), key=freq.chiave_decrescente) == [
        ("luna", 2),
        ("sole", 2),
        ("mare", 1),
    ]


def test_counter_coincide_con_il_conteggio_esplicito():
    assert freq.frequenze_counter(freq.TESTO_CANONICO) == freq.conta_parole(
        freq.TESTO_CANONICO
    )


# --- Fibonacci con memoria -------------------------------------------------


@pytest.mark.parametrize("n", range(11))
def test_fibonacci_con_memoria_coincide_con_le_altre_versioni(n):
    memoria = fib.memoria_delle_basi()
    assert fib.fibonacci_mem(n, memoria) == fib.fibonacci_diretto(n)
    assert fib.fibonacci_mem(n, fib.memoria_delle_basi()) == fib.fibonacci_iter(n)


def test_memoria_finale_di_n4():
    memoria = fib.memoria_delle_basi()
    assert fib.fibonacci_mem(4, memoria) == 3
    assert memoria == {0: 0, 1: 1, 2: 1, 3: 2, 4: 3}


def test_conteggi_di_n4():
    memoria = fib.memoria_delle_basi()
    statistiche = [0, 0, 0]
    risultato = fib.fibonacci_mem_osservata(4, memoria, statistiche)
    assert risultato == 3
    assert statistiche == [7, 4, 3]        # C = 7, D = 4, S = 3


def test_cache_calda_e_nuova_sessione():
    memoria = fib.memoria_delle_basi()
    fib.fibonacci_mem(4, memoria)
    statistiche = [0, 0, 0]
    assert fib.fibonacci_mem_osservata(4, memoria, statistiche) == 3
    assert statistiche == [1, 1, 0]        # un solo accesso riuscito

    seconda = fib.memoria_delle_basi()
    statistiche = [0, 0, 0]
    assert fib.fibonacci_mem_osservata(4, seconda, statistiche) == 3
    assert statistiche == [7, 4, 3]


def test_n5_su_memoria_calda_fino_a_4():
    memoria = fib.memoria_delle_basi()
    fib.fibonacci_mem(4, memoria)
    statistiche = [0, 0, 0]
    assert fib.fibonacci_mem_osservata(5, memoria, statistiche) == 5
    assert statistiche == [3, 2, 1]        # ingressi 5, 4, 3


def test_traccia_degli_ingressi_di_n4():
    memoria = fib.memoria_delle_basi()
    statistiche = [0, 0, 0]
    traccia: list[int] = []
    fib.fibonacci_mem_osservata(4, memoria, statistiche, traccia=traccia)
    assert traccia == [4, 3, 2, 1, 0, 1, 2]


def test_conteggi_della_versione_diretta():
    for n, atteso in [(0, 1), (1, 1), (2, 3), (4, 9), (5, 15)]:
        statistiche = [0, 0]
        assert fib.fibonacci_diretto_osservato(n, statistiche) == fib.fibonacci_iter(n)
        assert statistiche[0] == atteso


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
