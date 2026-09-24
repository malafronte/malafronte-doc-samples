"""Suite di test del laboratorio LAB-PY-U7 — analizzatore di misure e di testi.

Collocare il file in `test_analizzatore_u7.py`, accanto a `analizzatore_u7.py`,
nella raccolta dello studente. La suite è consegnata COMPLETA: si esegue
subito dopo la prima lettura dello starter e mostra un caso verde (`presenta`)
e tutti gli altri rossi, con `NotImplementedError` sulle funzioni ancora da
scrivere. Ogni test che diventa verde chiude una parte del contratto del
docstring corrispondente.

Comando dalla root della raccolta:
uv run pytest -q test_analizzatore_u7.py

Corrispondenza fra i test e i casi pubblici del laboratorio:

- L01  normalizzazione delle etichette e argomento invariato;
- L02  tokenizzazione senza elementi vuoti e testo vuoto;
- L03  assenza gestita per confronto, mai leggendo con `-1` come indice;
- L04  statistiche sul caso pubblico e lista vuota;
- L05  selezione sopra la media senza arrotondare;
- L06  copia invertita senza effetti contro inversione sul posto;
- L07  indipendenza dei risultati fra due chiamate consecutive;
- L08  righe condivise della matrice contro righe indipendenti;
- L09  somme per riga e per colonna sul caso pubblico;
- L10  trasposizione 3x2 -> 2x3, righe indipendenti e argomento invariato;
- L11  nessuna stampa e nessuna lettura di input durante le chiamate;
- L12  import pulito e funzioni pubbliche raggiungibili;
- L13  modo di fallimento di una variante deliberatamente sbagliata;
- L14  il contratto ufficiale non ammette quel modo di fallimento.

La suite usa solo `assert` e non solleva né cattura eccezioni: ogni caso
mancante si manifesta con l'errore della funzione non completata, che è il
risultato atteso sullo starter.
"""

import contextlib
import io

from analizzatore_u7 import (
    copia_inverti,
    inverti_sul_posto,
    normalizza,
    presenta,
    somme_per_colonna,
    somme_per_riga,
    sopra_media_misure,
    statistiche_misure,
    tokenizza,
    trasponi,
)


# ---------------------------------------------------------------------------
# L13/L14 — VARIANTE DELIBERATAMENTE SBAGLIATA, ISOLATA IN QUESTO MODULO.
#
# La funzione qui sotto NON fa parte della consegna e non va copiata: serve
# soltanto a rendere visibile un modo di fallimento frequente, quello di
# una funzione che deve restituire una copia e invece modifica l'elenco
# ricevuto. Il test L13 ne fissa il comportamento, il test L14 verifica che
# il contratto ufficiale di `copia_inverti` quel comportamento non lo abbia.
# Il resto del modulo contiene i test veri e propri.
# ---------------------------------------------------------------------------


def _copia_inverti_sbagliata(valori: list[int]) -> list[int]:
    """VARIANTE SBAGLIATA: inverte l'elenco ricevuto e restituisce lo stesso oggetto.

    Il difetto è duplice: l'argomento viene modificato, contrariamente al
    contratto, e il risultato non è una lista nuova ma l'oggetto ricevuto.
    """
    valori.reverse()
    return valori


# ---------------------------------------------------------------------------
# L01 — Normalizzazione delle etichette
# ---------------------------------------------------------------------------


def test_l01_normalizza_il_caso_pubblico() -> None:
    etichetta = "  LED-12  "
    attestata = "  LED-12  "
    assert normalizza(etichetta) == "led-12"
    # L'argomento non viene modificato: le stringhe sono immutabili e la
    # normalizzazione produce una stringa nuova.
    assert etichetta == attestata


def test_l01_normalizza_non_esige_un_oggetto_nuovo() -> None:
    # Il contratto promette il VALORE normalizzato, non un oggetto diverso:
    # si confronta il contenuto e non l'identità del risultato.
    assert normalizza("led-12") == "led-12"


def test_l01_normalizza_spazi_interni_e_caso_vuoto() -> None:
    assert normalizza("LED    12") == "led 12"
    assert normalizza("led   rosso    5mm") == "led rosso 5mm"
    assert normalizza("") == ""
    assert normalizza("   ") == ""


# ---------------------------------------------------------------------------
# L02 — Tokenizzazione
# ---------------------------------------------------------------------------


def test_l02_tokenizza_non_produce_elementi_vuoti() -> None:
    assert tokenizza("a   b") == ["a", "b"]
    assert tokenizza("  le due   righe  ") == ["le", "due", "righe"]


def test_l02_tokenizza_del_testo_vuoto() -> None:
    assert tokenizza("") == []


# ---------------------------------------------------------------------------
# L03 — Assenza gestita per confronto, mai per indicizzazione
# ---------------------------------------------------------------------------


def test_l03_lassenza_si_confronta_e_non_si_legge_con_meno_uno() -> None:
    parole = tokenizza("led rosso")
    assert parole == ["led", "rosso"]

    cercata = "batteria"
    if cercata in parole:
        posizione = parole.index(cercata)
    else:
        posizione = -1

    # L'unico uso ammesso della sentinella `-1` è il confronto.
    assert posizione == -1
    assert posizione != 0

    # Leggere con `parole[posizione]` restituirebbe l'ULTIMO elemento e non
    # un'assenza: la riga qui sotto non si esegue apposta, e il controllo
    # dell'assenza resta affidato al confronto.
    assert cercata not in parole

    # Un'assenza non genera elenchi da indicizzare: la lista resta intatta e
    # la presentazione di un elenco vuoto è la stringa vuota.
    assert parole == ["led", "rosso"]
    assert presenta([]) == ""


# ---------------------------------------------------------------------------
# L04 — Statistiche sulle misure
# ---------------------------------------------------------------------------


def test_l04_statistiche_misure_sul_caso_pubblico() -> None:
    valori = [12, 7, 19, 7]
    attestata = [12, 7, 19, 7]
    assert statistiche_misure(valori) == (45, 7, 19)
    assert valori == attestata


def test_l04_statistiche_misure_sulla_lista_vuota() -> None:
    assert statistiche_misure([]) is None


# ---------------------------------------------------------------------------
# L05 — Selezione sopra la media
# ---------------------------------------------------------------------------


def test_l05_sopra_media_misure_sul_caso_pubblico() -> None:
    # Media di [12, 7, 19, 7] = 45 / 4 = 11.25, NON arrotondata:
    # soltanto 12 e 19 sono strettamente superiori.
    valori = [12, 7, 19, 7]
    attestata = [12, 7, 19, 7]
    assert sopra_media_misure(valori) == [12, 19]
    assert valori == attestata


def test_l05_sopra_media_misure_su_casi_confini() -> None:
    assert sopra_media_misure([]) == []
    assert sopra_media_misure([2, 2, 2]) == []
    assert sopra_media_misure([1, 1, 5]) == [5]


# ---------------------------------------------------------------------------
# L06 — Copia invertita contro inversione sul posto
# ---------------------------------------------------------------------------


def test_l06_copia_inverti_non_modifica_largomento() -> None:
    originale = [1, 2, 3, 4]
    attestata = [1, 2, 3, 4]
    inversa = copia_inverti(originale)
    assert inversa == [4, 3, 2, 1]
    assert originale == attestata
    assert inversa is not originale


def test_l06_inverti_sul_posto_modifica_e_non_restituisce() -> None:
    originale = [1, 2, 3, 4]
    identita = originale
    risultato = inverti_sul_posto(originale)
    assert risultato is None
    assert originale == [4, 3, 2, 1]
    # La lista è la stessa di prima: la modifica è avvenuta in loco.
    assert originale is identita


def test_l06_casi_confini_delle_due_funzioni() -> None:
    assert copia_inverti([]) == []
    assert copia_inverti([7]) == [7]
    vuoto = []
    assert inverti_sul_posto(vuoto) is None
    assert vuoto == []
    singolo = [7]
    inverti_sul_posto(singolo)
    assert singolo == [7]


# ---------------------------------------------------------------------------
# L07 — Indipendenza dei risultati fra chiamate consecutive
# ---------------------------------------------------------------------------


def test_l07_due_chiamate_consecutive_non_condividono_risultati() -> None:
    prima_lista = [12, 7, 19, 7]
    seconda_lista = [3, 3, 8]

    prima_risposta = sopra_media_misure(prima_lista)
    seconda_risposta = sopra_media_misure(seconda_lista)

    assert prima_risposta == [12, 19]
    assert seconda_risposta == [8]
    assert prima_risposta is not seconda_risposta

    # Una modifica sul primo risultato non si ripercuote sul secondo.
    prima_risposta.append(1000)
    assert seconda_risposta == [8]

    # La seconda chiamata riparte dalle proprie condizioni iniziali.
    assert sopra_media_misure(seconda_lista) == [8]


def test_l07_anche_le_matrici_restituite_sono_indipendenti() -> None:
    prima = trasponi([[1, 2], [3, 4]])
    seconda = trasponi([[5, 6], [7, 8]])
    assert prima is not seconda
    prima[0][0] = 999
    assert seconda == [[5, 7], [6, 8]]


# ---------------------------------------------------------------------------
# L08 — Righe condivise contro righe indipendenti
# ---------------------------------------------------------------------------


def test_l08_matrice_a_righe_condivise_e_matrice_indipendente() -> None:
    # [[0] * 3] * 2 ripete lo STESSO riferimento di riga: la scrittura su
    # una cella appare in tutte le righe.
    condivisa = [[0] * 3] * 2
    assert condivisa[0] is condivisa[1]
    condivisa[0][0] = 99
    assert condivisa == [[99, 0, 0], [99, 0, 0]]

    # La costruzione per righe indipendenti non presenta questo difetto.
    indipendente = [[0 for _ in range(3)] for _ in range(2)]
    assert indipendente[0] is not indipendente[1]
    indipendente[0][0] = 99
    assert indipendente == [[99, 0, 0], [0, 0, 0]]


def test_l08_trasponi_non_propaga_le_righe_condivise() -> None:
    indipendente = [[99, 0, 0], [0, 0, 0]]
    attestata = [[99, 0, 0], [0, 0, 0]]
    trasposta = trasponi(indipendente)
    assert trasposta == [[99, 0], [0, 0], [0, 0]]
    assert trasposta[0] is not trasposta[1]
    trasposta[0][0] = -1
    assert trasposta[1] == [0, 0]
    assert indipendente == attestata


# ---------------------------------------------------------------------------
# L09 — Somme per riga e per colonna
# ---------------------------------------------------------------------------


def test_l09_somme_per_riga_e_per_colonna() -> None:
    matrice = [[2, 4], [6, 8], [10, 12]]
    attestata = [[2, 4], [6, 8], [10, 12]]
    assert somme_per_riga(matrice) == [6, 14, 22]
    assert somme_per_colonna(matrice) == [18, 24]
    assert matrice == attestata


def test_l09_lunghezze_dei_risultati() -> None:
    matrice = [[2, 4], [6, 8], [10, 12]]
    assert len(somme_per_riga(matrice)) == 3
    assert len(somme_per_colonna(matrice)) == 2


# ---------------------------------------------------------------------------
# L10 — Trasposizione 3x2 -> 2x3
# ---------------------------------------------------------------------------


def test_l10_trasponi_scambia_le_dimensioni() -> None:
    matrice = [[2, 4], [6, 8], [10, 12]]
    attestata = [[2, 4], [6, 8], [10, 12]]
    trasposta = trasponi(matrice)
    assert trasposta == [[2, 6, 10], [4, 8, 12]]
    assert len(trasposta) == 2
    assert len(trasposta[0]) == 3
    assert matrice == attestata


def test_l10_righe_indipendenti_nel_risultato() -> None:
    trasposta = trasponi([[2, 4], [6, 8], [10, 12]])
    assert trasposta == [[2, 6, 10], [4, 8, 12]]
    # Verifica dell'indipendenza per mutazione: scrivere su una riga non
    # tocca le altre e non tocca la matrice di partenza.
    trasposta[0][0] = 999
    assert trasposta[1] == [4, 8, 12]


# ---------------------------------------------------------------------------
# L11 — Nessuna stampa e nessuna lettura di input durante le chiamate
# ---------------------------------------------------------------------------


def test_l11_le_funzioni_non_scrivono_sullo_standard_output() -> None:
    # Le funzioni leggono gli argomenti e restituiscono un risultato: non
    # chiedono input e non stampano. Il buffer intercetta qualunque scrittura
    # accidentale e deve restare vuoto.
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        normalizza("  prova  ")
        tokenizza("a b")
        presenta(["a", "b"])
        statistiche_misure([1, 2, 3])
        sopra_media_misure([1, 2, 3])
        copia_inverti([1, 2])
        inverti_sul_posto([1, 2])
        somme_per_riga([[1, 2]])
        somme_per_colonna([[1, 2]])
        trasponi([[1, 2]])
    assert buffer.getvalue() == ""


# ---------------------------------------------------------------------------
# L12 — Import pulito e funzioni pubbliche raggiungibili
# ---------------------------------------------------------------------------


def test_l12_funzioni_pubbliche_importabili() -> None:
    elenco = [
        normalizza,
        tokenizza,
        presenta,
        statistiche_misure,
        sopra_media_misure,
        copia_inverti,
        inverti_sul_posto,
        somme_per_riga,
        somme_per_colonna,
        trasponi,
    ]
    for funzione in elenco:
        assert callable(funzione)


def test_l12_presenta_e_completa_fin_dalla_prima_esecuzione() -> None:
    # `presenta` è l'unica funzione fornita completa: questo test è verde
    # anche sullo starter e serve da riferimento per il primo avvio.
    assert presenta(["led", "rosso", "5mm"]) == "led, rosso, 5mm"
    assert presenta(["led"], " | ") == "led"
    assert presenta([]) == ""


# ---------------------------------------------------------------------------
# L13/L14 — Modo di fallimento documentato
# ---------------------------------------------------------------------------


def test_l13_la_variante_sbagliata_modifica_largomento() -> None:
    # Modo di fallimento atteso della variante sbagliata: la funzione
    # promette una lista nuova e invece modifica e restituisce l'elenco
    # ricevuto. Il test ne fissa il comportamento per renderlo visibile.
    originale = [1, 2, 3]
    risultato = _copia_inverti_sbagliata(originale)
    assert risultato is originale
    assert originale == [3, 2, 1]


def test_l14_il_contratto_di_copia_inverti_non_ammette_quel_fallimento() -> None:
    # Il contratto ufficiale richiede il contrario: elenco di partenza
    # intatto e lista nuova come risultato.
    originale = [1, 2, 3]
    attestata = [1, 2, 3]
    risultato = copia_inverti(originale)
    assert originale == attestata
    assert risultato == [3, 2, 1]
    assert risultato is not originale
