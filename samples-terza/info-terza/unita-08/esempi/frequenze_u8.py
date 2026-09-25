"""Frequenze delle parole dell'Unità 8: conteggi e graduatorie.

Collocare il file in `programmi/frequenze_u8.py` della raccolta dello
studente. Il modulo contiene il problema svolto del capitolo PY-12,
parte IV: il conteggio delle parole di un testo con un dizionario, prima con
il ramo esplicito «chiave nuova / chiave già presente» e poi con `get`,
quindi la presentazione dei risultati con due criteri di ordinamento
complementari e il breve confronto con `collections.Counter`.

Parola e normalizzazione riprendono l'Unità 7: i token sono separati dagli
spazi bianchi (`split()` senza argomenti) e il confronto usa `casefold()`;
la punteggiatura resta attaccata al token e gli accenti non vengono rimossi.
Il testo vive in una stringa in memoria, a capo compresi: in questa unità non
si leggono file. Non esiste una nozione linguistica universale di parola: il
problema definisce i propri token.

L'import non chiede input e non stampa: le dimostrazioni stanno nel main
protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/frequenze_u8.py
"""

from collections import Counter

TESTO_CANONICO = "Sole luna sole\nmare LUNA sole"


# ---------------------------------------------------------------------------
# Problema svolto — Conteggio delle parole
# ---------------------------------------------------------------------------


def conta_parole(testo: str) -> dict[str, int]:
    """Restituisce le frequenze delle parole del `testo` come dizionario.

    Riceve la stringa `testo` e restituisce un dizionario NUOVO nel quale
    ogni CHIAVE è una parola normalizzata e ogni VALORE è il numero delle
    sue occorrenze. La normalizzazione è `testo.casefold().split()`: le
    parole si separano sugli spazi bianchi e si confrontano in forma
    minuscola piena, così «Sole» e «sole» contribuiscono alla stessa chiave.

    Il procedimento usa il ramo esplicito sulla presenza della chiave: se la
    parola è già nel dizionario il valore viene incrementato, altrimenti la
    chiave viene creata con valore 1. Questo è il meccanismo che `get`
    compatta nella variante `conta_parole_con_get`.

    L'argomento non viene modificato: le stringhe sono immutabili. Per testo
    vuoto, oppure composto dai soli spazi bianchi, il risultato è `{}`:
    zero parole distinte e zero occorrenze. Il numero delle chiavi è il
    numero delle parole DISTINTE, mentre la somma dei valori è il numero
    TOTALE delle occorrenze: sono due grandezze diverse.
    """
    frequenze = {}
    for parola in testo.casefold().split():
        if parola in frequenze:
            frequenze[parola] += 1
        else:
            frequenze[parola] = 1
    return frequenze


def conta_parole_con_get(testo: str) -> dict[str, int]:
    """Restituisce le stesse frequenze di `conta_parole`, con `get` compatto.

    Stesso ricevuto, stesso risultato e stessi effetti di `conta_parole`.
    L'espressione `frequenze.get(parola, 0) + 1` sostituisce il ramo
    esplicito: legge il valore esistente oppure il default 0 e assegna alla
    stessa chiave il valore successivo. Il default di `get` NON inserisce la
    chiave: è l'assegnamento che la crea. Le due versioni concordano su ogni
    testo e la si confrontano per verificarlo.

    La forma compatta è più breve e meno esplicita: conviene padroneggiare
    prima il ramo «chiave nuova / chiave già presente», che mostra il
    meccanismo, e riconoscere poi in `get` la stessa logica abbreviata.
    """
    frequenze = {}
    for parola in testo.casefold().split():
        frequenze[parola] = frequenze.get(parola, 0) + 1
    return frequenze


# ---------------------------------------------------------------------------
# Presentazione — ordinare le coppie con chiavi nominate
# ---------------------------------------------------------------------------


def chiave_crescente(voce: tuple[str, int]) -> tuple[int, str]:
    """Restituisce la chiave di ordinamento crescente della coppia `voce`.

    Riceve una coppia `(parola, conteggio)` prodotta da `frequenze.items()`
    e restituisce la tupla `(conteggio, parola)`. Confrontando queste chiavi
    si ordinano prima le occorrenze crescenti e, a parità di conteggio, le
    parole in ordine crescente secondo il confronto Python sulle stringhe.

    Il parametro `key` di `sorted` richiede la FUNZIONE da applicare a ogni
    elemento: si scrive quindi `key=chiave_crescente` e non
    `key=chiave_crescente(...)`, che chiamerebbe subito la funzione una sola
    volta e passerebbe a `sorted` il risultato di quella chiamata.

    L'ordine delle parole è quello del confronto Python sulle stringhe
    normalizzate e non una collazione linguistica italiana.
    """
    return (voce[1], voce[0])


def chiave_decrescente(voce: tuple[str, int]) -> tuple[int, str]:
    """Restituisce la chiave di ordinamento decrescente della coppia `voce`.

    Riceve una coppia `(parola, conteggio)` e restituisce la tupla
    `(-conteggio, parola)`. Il SEGNO MENO inverte il solo conteggio, così i
    valori più frequenti compaiono per primi; la parola resta in ordine
    crescente anche a parità di conteggio. Usare `reverse=True` sull'intera
    chiave invertirebbe anche le parole e cambierebbe il criterio promesso.

    Si confronti sul testo canonico: crescente `mare, luna, sole`;
    decrescente `sole, luna, mare`.
    """
    return (-voce[1], voce[0])


# ---------------------------------------------------------------------------
# Confronto con collections.Counter
# ---------------------------------------------------------------------------


def frequenze_counter(testo: str) -> dict[str, int]:
    """Restituisce le frequenze calcolate da `Counter`, come dizionario.

    Riceve la stringa `testo` e restituisce `dict(Counter(testo.casefold().split()))`.
    `Counter` è una classe della libreria standard, raccolta in
    `collections`, e non richiede installazione separata: conta gli elementi
    di un iterabile e produce un mapping fra elemento e occorrenze.

    Il confronto con `conta_parole` verifica che i due procedimenti
    producano le stesse associazioni. La presentazione resta però quella del
    problema: `Counter.most_common()` ordina per conteggio decrescente e, a
    parità, secondo l'ordine di incontro; non garantisce quindi il criterio
    alfabetico sulle parità richiesto da `chiave_crescente` e da
    `chiave_decrescente`, che si applicano ugualmente alle sue coppie.
    """
    return dict(Counter(testo.casefold().split()))


if __name__ == "__main__":
    # Le uniche stampe del modulo stanno qui: ogni funzione sopra restituisce
    # e non scrive nulla.
    testi = {
        "canonico": TESTO_CANONICO,
        "parita sole/luna": "Sole luna mare LUNA sole",
        "vuoto": "",
        "soli spazi": "   \t\n  ",
        "punteggiatura": "sole sole, SOLE",
        "accenti": "È è",
    }
    for etichetta, testo in testi.items():
        frequenze = conta_parole(testo)
        totale = sum(frequenze.values())
        distinte = len(frequenze)
        crescente = sorted(frequenze.items(), key=chiave_crescente)
        decrescente = sorted(frequenze.items(), key=chiave_decrescente)
        print(f"Testo «{etichetta}»: {testo!r}")
        print("  frequenze          :", frequenze)
        print("  totale / distinte  :", totale, "/", distinte)
        print("  ordinamento crescente   :", crescente)
        print("  ordinamento decrescente :", decrescente)
        print("  variante con get concorda:", conta_parole_con_get(testo) == frequenze)
        print("  Counter concorda         :", frequenze_counter(testo) == frequenze)
        print("  most_common di Counter   :", Counter(testo.casefold().split()).most_common())
        print()
