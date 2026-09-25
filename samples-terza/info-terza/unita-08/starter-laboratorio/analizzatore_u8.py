"""Starter del LAB-PY-U8 - Analizzare frequenze e raggruppare dati in memoria.

Questo file è **incompleto, e lo dichiara**: contiene costanti, firme e docstring,
mentre i corpi delle quattro funzioni sono da completare. Il primo esito atteso
della suite è una serie di fallimenti chiari, non un difetto della copia.

Ambiente: CPython sul computer, raccolta `raccolta-programmi`, esecuzione con
`uv run python programmi/analizzatore_u8.py` dalla root della raccolta.

Le funzioni di logica non usano `input` né `print`: la demo è protetta dalla
guardia di avvio in fondo al file.
"""

# ---------------------------------------------------------------------------
# Costanti sintetiche della sessione. Non vanno modificate.
# ---------------------------------------------------------------------------

TESTO_CANONICO = "Sole luna sole\nmare LUNA sole"

VOCI_CANONICHE = [
    ("elettronica", "R10"),
    ("meccanica", "007"),
    ("elettronica", "L05"),
]


# ---------------------------------------------------------------------------
# Funzioni da completare
# ---------------------------------------------------------------------------


def conta_parole(testo: str) -> dict[str, int]:
    """Restituisce la frequenza dei token normalizzati del testo.

    Token: `testo.casefold().split()`, cioè la punteggiatura resta nei token e
    gli accenti non vengono alterati. Il testo vuoto o di soli spazi produce `{}`.
    Il testo ricevuto non viene modificato.

    Da completare: costruire il dizionario `parola -> conteggio` con un ramo
    esplicito sulla chiave nuova, senza usare `collections.Counter`.
    """
    pass


def ordina_frequenze(
    frequenze: dict[str, int], decrescente: bool = False
) -> list[tuple[str, int]]:
    """Restituisce una lista nuova di coppie `(parola, conteggio)` ordinate.

    Criterio: conteggio crescente, oppure decrescente se `decrescente` è True;
    in entrambe le modalità **la parola resta crescente** a parità di conteggio.
    Il dizionario ricevuto non viene modificato. Dizionario vuoto -> [].

    Da completare: costruire la funzione chiave e passarla a `sorted` senza
    parentesi, oppure usare una `lambda` equivalente.
    """
    pass


def unici_in_ordine(codici: list[str]) -> list[str]:
    """Restituisce i codici senza ripetizioni, nell'ordine della prima occorrenza.

    La lista ricevuta resta invariata. Lista vuota -> [].

    Da completare: separare la responsabilità del risultato - una lista che
    accumula nell'ordine voluto - da quella dell'appartenenza.
    """
    pass


def raggruppa_codici(voci: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Associa ogni categoria alla lista dei suoi codici, nell'ordine di incontro.

    Ogni gruppo ha la **propria** lista; le ripetizioni di una coppia restano nel
    gruppo. La lista ricevuta resta invariata. Lista di coppie vuota -> {}.
    L'ordine delle chiavi segue la prima comparsa delle categorie.

    Da completare: creare la lista del gruppo alla prima comparsa della categoria.
    """
    pass


# ---------------------------------------------------------------------------
# Demo protetta dalla guardia di avvio
# ---------------------------------------------------------------------------


def main() -> None:
    """Mostra i dataset della sessione senza sostituire le prove."""
    print("Testo canonico:", repr(TESTO_CANONICO))
    print("Voci canoniche:", VOCI_CANONICHE)
    print("Le quattro funzioni sono da completare: la suite deve prima fallire.")


if __name__ == "__main__":
    main()
