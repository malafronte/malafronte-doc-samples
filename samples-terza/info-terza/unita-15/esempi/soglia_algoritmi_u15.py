"""Stessa operazione e stessa validazione per scansione e dicotomia."""

from politiche_duck_u15 import valida_intero, valida_valori


def valida_ingressi(valori, minimo):
    valida_valori(valori)
    valida_intero(minimo)
    for indice in range(1, len(valori)):
        if valori[indice] < valori[indice - 1]:
            raise ValueError("lista: atteso ordine non decrescente")


def da_soglia_scansione(valori_ordinati, minimo):
    valida_ingressi(valori_ordinati, minimo)
    risultato = []
    for valore in valori_ordinati:
        if valore >= minimo:
            risultato.append(valore)
    return risultato


def da_soglia_dicotomica(valori_ordinati, minimo):
    valida_ingressi(valori_ordinati, minimo)
    sinistra = 0
    destra = len(valori_ordinati)
    while sinistra < destra:
        centro = (sinistra + destra) // 2
        if valori_ordinati[centro] < minimo:
            sinistra = centro + 1
        else:
            destra = centro
    risultato = []
    for indice in range(sinistra, len(valori_ordinati)):
        risultato.append(valori_ordinati[indice])
    return risultato


class StrategiaScansione:
    def da_soglia(self, valori_ordinati, minimo):
        return da_soglia_scansione(valori_ordinati, minimo)


class StrategiaDicotomica:
    def da_soglia(self, valori_ordinati, minimo):
        return da_soglia_dicotomica(valori_ordinati, minimo)
