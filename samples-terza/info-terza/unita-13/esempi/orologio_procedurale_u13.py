"""Orologio digitale procedurale (OOP-01): stato, operazioni e controlli.

Modello software di un orologio a 24 ore con precisione al minuto.
Non legge l'ora del computer e non avanza da solo: il chiamante fornisce
esplicitamente il numero di minuti trascorsi. Non conserva una data.

Record: {"ore": int, "minuti": int}. Invariante: interi non booleani,
0 <= ore < 24 e 0 <= minuti < 60. Le operazioni ricevono un record valido;
non ricontrollano né riparano uno stato alterato esternamente.

API: nuovo_orologio, imposta, avanza, leggi, testo.
Creazione e impostazione controllano l'intera coppia prima delle scritture.
Avanzamento: durata intera non booleana non negativa; anche zero e durate
oltre un giorno sono ammesse. Successo delle modifiche: None; dati non
ammessi: ValueError, senza modifiche. leggi restituisce una coppia,
testo restituisce HH:MM. Nessuna lettura o stampa nelle operazioni.
Ambiente: CPython sul computer, nessuna dipendenza esterna.
"""

MINUTI_PER_ORA = 60
ORE_PER_GIORNO = 24
MINUTI_PER_GIORNO = ORE_PER_GIORNO * MINUTI_PER_ORA


def _valida_intero_non_negativo(valore, nome):
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ValueError(f"{nome}: atteso un intero, ricevuto {type(valore).__name__}")
    if valore < 0:
        raise ValueError(f"{nome}: atteso un valore non negativo, ricevuto {valore}")
    return None


def _valida_orario(ore, minuti):
    _valida_intero_non_negativo(ore, "ore")
    _valida_intero_non_negativo(minuti, "minuti")
    if ore >= ORE_PER_GIORNO:
        raise ValueError(f"ore: atteso un valore da 0 a 23, ricevuto {ore}")
    if minuti >= MINUTI_PER_ORA:
        raise ValueError(f"minuti: atteso un valore da 0 a 59, ricevuto {minuti}")
    return None


def nuovo_orologio(ore=0, minuti=0):
    """Restituisce un record nuovo dopo il controllo dell'orario completo."""
    _valida_orario(ore, minuti)
    return {"ore": ore, "minuti": minuti}


def imposta(orologio, ore, minuti):
    """Imposta l'intera coppia; su errore conserva entrambi i campi."""
    _valida_orario(ore, minuti)
    orologio["ore"] = ore
    orologio["minuti"] = minuti
    return None


def avanza(orologio, minuti_trascorsi):
    """Avanza della durata ammessa, ripartendo da 00:00 oltre mezzanotte."""
    _valida_intero_non_negativo(minuti_trascorsi, "minuti_trascorsi")
    totale = orologio["ore"] * MINUTI_PER_ORA + orologio["minuti"]
    candidato = (totale + minuti_trascorsi) % MINUTI_PER_GIORNO
    nuove_ore = candidato // MINUTI_PER_ORA
    nuovi_minuti = candidato % MINUTI_PER_ORA
    orologio["ore"] = nuove_ore
    orologio["minuti"] = nuovi_minuti
    return None


def leggi(orologio):
    """Restituisce (ore, minuti), senza modificare il record."""
    return orologio["ore"], orologio["minuti"]


def testo(orologio):
    """Restituisce HH:MM, senza stampare né modificare il record."""
    return f"{orologio['ore']:02d}:{orologio['minuti']:02d}"


if __name__ == "__main__":
    primo = nuovo_orologio(23, 58)
    secondo = nuovo_orologio(8, 15)
    avanza(primo, 5)
    avanza(secondo, 45)
    print(testo(primo), testo(secondo))
    imposta(primo, 12, 30)
    print(testo(primo), testo(secondo))
