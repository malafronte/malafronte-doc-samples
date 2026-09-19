"""Versione completa della lezione: la sala in funzioni annotate e documentate.

Collocare il file in `programmi/sala_u5.py` della raccolta dello studente.
"""


def durata_ammessa(durata_min: int) -> bool:
    """Restituisce True se la durata è fra 1 e 240 minuti inclusi.

    Accetta qualsiasi intero; fuori 1-240 restituisce False.
    Nessun input, nessuna stampa, nessun effetto esterno.
    """
    return 1 <= durata_min <= 240


def costo_sala(durata_min: int) -> int:
    """Restituisce il costo in euro per una durata già ammessa (1-240).

    Fasce: 2 euro fino a 60 minuti, 3 fino a 120, 5 oltre.
    Il risultato è un numero intero: nessuna formattazione qui.
    """
    if durata_min <= 60:
        return 2
    if durata_min <= 120:
        return 3
    return 5


def main() -> None:
    """Legge, valida, calcola e presenta il costo. Nessun risultato utile."""
    durata_testo = input("Durata in minuti interi (da 1 a 240): ")
    durata_min = int(durata_testo)
    if not durata_ammessa(durata_min):
        print("Durata non ammessa: indicare un intero da 1 a 240.")
        return
    costo_euro = costo_sala(durata_min)
    print(f"Costo complessivo: {costo_euro:.2f} euro")


if __name__ == "__main__":
    main()
