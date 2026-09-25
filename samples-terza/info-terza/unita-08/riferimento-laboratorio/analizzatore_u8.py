"""Riferimento formativo del LAB-PY-U8 - versione completa.

Da leggere **dopo** le fasi L2 e L3, come confronto con il proprio lavoro.
Ogni funzione dichiara ricevuto, restituito, effetti e comportamento sul vuoto.
Le funzioni di logica non usano `input` né `print`.
"""

TESTO_CANONICO = "Sole luna sole\nmare LUNA sole"

VOCI_CANONICHE = [
    ("elettronica", "R10"),
    ("meccanica", "007"),
    ("elettronica", "L05"),
]


def conta_parole(testo: str) -> dict[str, int]:
    """Restituisce la frequenza dei token normalizzati del testo.

    Token: `testo.casefold().split()`; punteggiatura conservata, accenti invariati.
    Testo vuoto o di soli spazi -> `{}`. Il testo ricevuto non viene modificato.
    """
    frequenze: dict[str, int] = {}
    for parola in testo.casefold().split():
        if parola in frequenze:
            frequenze[parola] += 1
        else:
            frequenze[parola] = 1
    return frequenze


def ordina_frequenze(
    frequenze: dict[str, int], decrescente: bool = False
) -> list[tuple[str, int]]:
    """Restituisce una lista nuova di coppie `(parola, conteggio)` ordinate.

    Conteggio crescente, oppure decrescente se `decrescente` è True; la parola
    resta crescente in entrambe le modalità. Il dizionario ricevuto non viene
    modificato. Dizionario vuoto -> [].
    """

    def chiave_crescente(voce: tuple[str, int]) -> tuple[int, str]:
        return (voce[1], voce[0])

    def chiave_decrescente(voce: tuple[str, int]) -> tuple[int, str]:
        return (-voce[1], voce[0])

    if decrescente:
        return sorted(frequenze.items(), key=chiave_decrescente)
    return sorted(frequenze.items(), key=chiave_crescente)


def unici_in_ordine(codici: list[str]) -> list[str]:
    """Restituisce i codici senza ripetizioni, nell'ordine della prima occorrenza.

    La lista ricevuta resta invariata. Lista vuota -> [].
    """
    visti: set[str] = set()
    risultato: list[str] = []
    for codice in codici:
        if codice not in visti:
            visti.add(codice)
            risultato.append(codice)
    return risultato


def raggruppa_codici(voci: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Associa ogni categoria alla lista dei suoi codici, nell'ordine di incontro.

    Ogni gruppo ha la propria lista; le ripetizioni restano nel gruppo.
    La lista ricevuta resta invariata. Lista di coppie vuota -> {}.
    """
    gruppi: dict[str, list[str]] = {}
    for categoria, codice in voci:
        if categoria not in gruppi:
            gruppi[categoria] = []
        gruppi[categoria].append(codice)
    return gruppi


def main() -> None:
    """Mostra i risultati attesi sul dataset canonico."""
    print("Frequenze:", conta_parole(TESTO_CANONICO))
    print("Crescente:", ordina_frequenze(conta_parole(TESTO_CANONICO)))
    print("Decrescente:", ordina_frequenze(conta_parole(TESTO_CANONICO), True))
    print("Unici:", unici_in_ordine(["007", "7", "007", "A"]))
    print("Gruppi:", raggruppa_codici(VOCI_CANONICHE))


if __name__ == "__main__":
    main()
