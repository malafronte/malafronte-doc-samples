"""Riferimento del LAB-PY-U11: la strumentazione dei conteggi completata.

Controparte completa dello starter `conteggi_u11.py`, da leggere **dopo** la
fase L3. I registri sono aggiornati negli stessi punti del codice senza
contatori: la strumentazione non cambia né il risultato né gli effetti e la
prova di equivalenza resta nei test.

Ambiente: CPython sul computer, raccolta `raccolta-programmi`.
"""


def _valutatore(chiave):
    """Restituisce la funzione che produce il valore confrontabile di un elemento."""
    return (lambda elemento: elemento) if chiave is None else chiave


def _fondi_contata(sinistra, destra, chiave, stato):
    """Fonde due liste ordinate aggiornando `stato` con confronti e copie."""
    valore = _valutatore(chiave)
    risultato = []
    j = 0
    k = 0
    while j < len(sinistra) and k < len(destra):
        stato["confronti"] += 1
        if valore(sinistra[j]) <= valore(destra[k]):
            risultato.append(sinistra[j])
            stato["copie"] += 1
            j += 1
        else:
            risultato.append(destra[k])
            stato["copie"] += 1
            k += 1
    while j < len(sinistra):
        risultato.append(sinistra[j])
        stato["copie"] += 1
        j += 1
    while k < len(destra):
        risultato.append(destra[k])
        stato["copie"] += 1
        k += 1
    return risultato


def _merge_sort_contato(valori, chiave, stato, profondita):
    """Versione ricorsiva di `merge_sort` che aggiorna `stato` a ogni passo."""
    if profondita > stato["profondita_massima"]:
        stato["profondita_massima"] = profondita
    if len(valori) <= 1:
        stato["copie"] += len(valori)
        return list(valori)
    meta = len(valori) // 2
    stato["copie"] += len(valori)  # le due metà prodotte dallo slicing
    sinistra = _merge_sort_contato(valori[:meta], chiave, stato, profondita + 1)
    destra = _merge_sort_contato(valori[meta:], chiave, stato, profondita + 1)
    return _fondi_contata(sinistra, destra, chiave, stato)


def _partiziona_contata(valori, sinistra, destra, chiave, stato):
    """Versione di `partiziona_lomuto` che aggiorna `stato` con confronti e scambi."""
    valore = _valutatore(chiave)
    pivot = valori[destra]
    chiave_pivot = valore(pivot)
    confine = sinistra - 1
    for j in range(sinistra, destra):
        stato["confronti"] += 1
        if valore(valori[j]) <= chiave_pivot:
            confine += 1
            if confine != j:
                valori[confine], valori[j] = valori[j], valori[confine]
                stato["scambi"] += 1
    posizione = confine + 1
    if posizione != destra:
        valori[posizione], valori[destra] = valori[destra], valori[posizione]
        stato["scambi"] += 1
    return posizione


def _quick_sort_contato(valori, sinistra, destra, chiave, stato, profondita):
    """Versione ricorsiva di `quick_sort` che aggiorna `stato` a ogni passo.

    La profondità si registra all'ingresso di ogni chiamata, comprese quelle
    sugli intervalli di 0 o 1 elemento.
    """
    if profondita > stato["profondita_massima"]:
        stato["profondita_massima"] = profondita
    if sinistra >= destra:
        return
    p = _partiziona_contata(valori, sinistra, destra, chiave, stato)
    _quick_sort_contato(valori, sinistra, p - 1, chiave, stato, profondita + 1)
    _quick_sort_contato(valori, p + 1, destra, chiave, stato, profondita + 1)


def fondi_ordinate_con_conteggi(sinistra, destra, chiave=None):
    """Come `fondi_ordinate`, più `{"risultato", "confronti", "copie"}`."""
    stato = {"confronti": 0, "copie": 0}
    risultato = _fondi_contata(sinistra, destra, chiave, stato)
    return {
        "risultato": risultato,
        "confronti": stato["confronti"],
        "copie": stato["copie"],
    }


def merge_sort_con_conteggi(valori, chiave=None):
    """Come `merge_sort`, più `{"risultato", "confronti", "copie", "profondita_massima"}`."""
    stato = {"confronti": 0, "copie": 0, "profondita_massima": 0}
    risultato = _merge_sort_contato(valori, chiave, stato, 1)
    return {
        "risultato": risultato,
        "confronti": stato["confronti"],
        "copie": stato["copie"],
        "profondita_massima": stato["profondita_massima"],
    }


def partiziona_lomuto_con_conteggi(valori, sinistra, destra, chiave=None):
    """Come `partiziona_lomuto`, più `{"pivot_finale", "confronti", "scambi"}`."""
    stato = {"confronti": 0, "scambi": 0}
    pivot_finale = _partiziona_contata(valori, sinistra, destra, chiave, stato)
    return {
        "pivot_finale": pivot_finale,
        "confronti": stato["confronti"],
        "scambi": stato["scambi"],
    }


def quick_sort_con_conteggi(valori, chiave=None):
    """Come `quick_sort`, più `{"confronti", "scambi", "copie", "profondita_massima"}`.

    `copie` resta zero: la partizione canonica non costruisce sequenze nuove.
    """
    stato = {"confronti": 0, "scambi": 0, "copie": 0, "profondita_massima": 0}
    _quick_sort_contato(valori, 0, len(valori) - 1, chiave, stato, 1)
    return {
        "confronti": stato["confronti"],
        "scambi": stato["scambi"],
        "copie": stato["copie"],
        "profondita_massima": stato["profondita_massima"],
    }


def confronti_massimi_fusione(a, b):
    """Limite superiore dei confronti per fondere liste di `a` e `b` elementi."""
    if a < 0 or b < 0:
        raise ValueError("le lunghezze non possono essere negative")
    return 0 if a == 0 or b == 0 else a + b - 1


def copie_attese_merge_sort(n):
    """Numero esatto di copie elementari di `merge_sort` su `n` elementi."""
    if n < 0:
        raise ValueError("il numero di elementi non può essere negativo")
    if n <= 1:
        return n
    meta = n // 2
    return 2 * n + copie_attese_merge_sort(meta) + copie_attese_merge_sort(n - meta)


if __name__ == "__main__":
    print("Fusione contata:", fondi_ordinate_con_conteggi([1, 3, 5], [2, 3, 6]))
    print("MergeSort contato:", merge_sort_con_conteggi([5, 2, 4, 2]))
    valori = [5, 2, 4, 2]
    print("QuickSort contato:", quick_sort_con_conteggi(valori), valori)
